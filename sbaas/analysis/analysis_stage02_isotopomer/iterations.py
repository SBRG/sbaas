# Dependencies
import operator, json, csv
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra.io.sbml import write_cobra_model_to_sbml_file
from cobra.io.mat import save_matlab_model_isotopomer
from cobra.core import Metabolite, Reaction
from cobra.manipulation.modify import convert_to_irreversible, revert_to_reversible
from cobra.flux_analysis.objective import update_objective
from cobra.flux_analysis.variability import flux_variability_analysis
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
# Dependencies from data_stage02
from isotopomer import *
from reduce_model import *
# Dependencies from workspace
from workspace.load_model import load_ALEWt
# Dependiencies from Scipy
import scipy
import numpy
from scipy.sparse.linalg import svds

def null(A, eps=1e-6):
    u, s, vh = numpy.linalg.svd(A,full_matrices=1,compute_uv=1)
    null_rows = [];
    rank = numpy.linalg.matrix_rank(A)
    for i in range(A.shape[1]):
        if i<rank:
            null_rows.append(False);
        else:
            null_rows.append(True);
    null_space = scipy.compress(null_rows, vh, axis=0)
    return null_space.T

def isotopomer_model_iteration1():
    '''iteration 1:
    identification of reactions that can be lumped in pathways outside the model scope'''
    cobra_model = load_ALEWt();
    # Make the model irreversible for downstream manipulations:
    convert_to_irreversible(cobra_model);
    # Add lumped isotopomer reactions
    add_net_reaction(cobra_model,isotopomer_rxns_net_irreversible);
    # Find minimal flux solution:
    pfba = optimize_minimal_flux(cobra_model,True,solver='gurobi');
    # Write pfba solution to file
    with open('data/iteration1_140407_ijo1366_reduced_modified_pfba.csv',mode='wb') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Reaction','Flux'])
        for k,v in cobra_model.solution.x_dict.iteritems():
            writer.writerow([k,v]);
    # Read in pfba solution 
    pfba_sol = {};
    with open('data/iteration1_140407_ijo1366_reduced_modified_pfba.csv',mode='r') as infile:
        dictreader = csv.DictReader(infile)
        for r in dictreader:
            pfba_sol[r['Reaction']] = r['Flux'];
    # Make net reactions for pathways outside of the scope
    # of the isotopomer model
    subs = ['Cell Envelope Biosynthesis',
	    'Glycerophospholipid Metabolism',
	    'Lipopolysaccharide Biosynthesis / Recycling',
	    'Membrane Lipid Metabolism',
	    'Murein Biosynthesis'
        'Murein Recycling',
        'Cofactor and Prosthetic Group Biosynthesis',
        #'Transport, Inner Membrane',
        #'Transport, Outer Membrane',
        #'Transport, Outer Membrane Porin',
        'tRNA Charging',
        'Unassigned',
        'Exchange',
        'Inorganic Ion Transport and Metabolism',
        'Nitrogen Metabolism'];
    add_net_reaction_subsystem(cobra_model,pfba_sol,subs);
    remove_noflux_reactions(cobra_model,pfba_sol,['Transport, Outer Membrane Porin','Transport, Inner Membrane','Transport, Outer Membrane'])
    revert_to_reversible(cobra_model);
    # write model to sbml
    write_cobra_model_to_sbml_file(cobra_model,'data/iteration1_140407_ijo1366_netrxn_irreversible.xml')
    # Reduce model using FVA:
    reduce_model(cobra_model,"data/iteration1_140407_ijo1366_reduced.xml")
    # Remove all reactions with 0 flux
    remove_noflux_reactions(cobra_model);
    with open('data/iteration1_140407_ijo1366_reduced_netrxn_lbub.csv',mode='wb') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Reaction','Formula','LB','UB','Subsystem'])
        for r in cobra_model.reactions:
            writer.writerow([r.id,
                             r.build_reaction_string(),
                            r.lower_bound,
                            r.upper_bound,
                            r.subsystem]);

def isotopomer_model_iteration2(pfba_filename,fva_reduced_model_filename,netrxn_irreversible_model_filename,reduced_lbub_filename):
    '''iteration 2:
    addition of finalized lumped reactions that are in pathways that are within the scope of the model
    and reduction by removing reactions with zero optimal minimal flux outside the scope of the model'''
    cobra_model = load_ALEWt();
    # Make the model irreversible for downstream manipulations:
    convert_to_irreversible(cobra_model);
    cobra_model.optimize();
    # Add lumped isotopomer reactions
    add_net_reaction(cobra_model,isotopomer_rxns_net_irreversible,True);
    cobra_model.optimize();
    # Find minimal flux solution:
    pfba = optimize_minimal_flux(cobra_model,True,solver='gurobi');
    # Write pfba solution to file
    with open(pfba_filename,mode='wb') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Reaction','Flux','Subsystem'])
        for k,v in cobra_model.solution.x_dict.iteritems():
            writer.writerow([k,v,cobra_model.reactions.get_by_id(k).subsystem]);
    # Read in pfba solution 
    pfba_sol = {};
    with open(pfba_filename,mode='r') as infile:
        dictreader = csv.DictReader(infile)
        for r in dictreader:
            pfba_sol[r['Reaction']] = r['Flux'];
    # remove noflux reactions for pathways outside of the scope
    # of the isotopomer model
    subs = ['Cell Envelope Biosynthesis',
	    'Glycerophospholipid Metabolism',
	    'Lipopolysaccharide Biosynthesis / Recycling',
	    'Membrane Lipid Metabolism',
	    'Murein Biosynthesis'
        'Murein Recycling',
        'Cofactor and Prosthetic Group Biosynthesis',
        'Transport, Inner Membrane',
        'Transport, Outer Membrane',
        'Transport, Outer Membrane Porin',
        'tRNA Charging',
        'Unassigned',
        #'Exchange',
        'Inorganic Ion Transport and Metabolism',
        'Nitrogen Metabolism',
        'Alternate Carbon Metabolism'];
    remove_noflux_reactions(cobra_model,pfba_sol,subs)
    # Reduce model using FVA:
    reduce_model(cobra_model,fva_reduced_model_filename)
    # Reset secretion products that may have been turned off
    secrete = ['EX_meoh_LPAREN_e_RPAREN_',
                'EX_5mtr_LPAREN_e_RPAREN_',
                'EX_h_LPAREN_e_RPAREN_',
                'EX_co2_LPAREN_e_RPAREN_',
                'EX_co_LPAREN_e_RPAREN_',
                'EX_h2o_LPAREN_e_RPAREN_',
                'EX_ac_LPAREN_e_RPAREN_',
                'EX_fum_LPAREN_e_RPAREN_',
                'EX_for_LPAREN_e_RPAREN_',
                'EX_etoh_LPAREN_e_RPAREN_',
                'EX_lac_DASH_L_LPAREN_e_RPAREN_',
                'EX_pyr_LPAREN_e_RPAREN_',
                'EX_succ_LPAREN_e_RPAREN_'];
    for s in secrete:
        cobra_model.reactions.get_by_id(s).upper_bound = 1000.0;
    # Remove all reactions with 0 flux
    r1,r2 = get_reactionsInfo(cobra_model);
    while r2 !=0:
        remove_noflux_reactions(cobra_model);
        r1,r2 = get_reactionsInfo(cobra_model);
        print r1,r2;
    # write model to sbml
    write_cobra_model_to_sbml_file(cobra_model,netrxn_irreversible_model_filename)
    with open(reduced_lbub_filename,mode='wb') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Reaction','Formula','LB','UB','Subsystem'])
        for r in cobra_model.reactions:
            writer.writerow([r.id,
                             r.build_reaction_string(),
                            r.lower_bound,
                            r.upper_bound,
                            r.subsystem]);

def isotopomer_model_iteration3(model_filename,xml_filename,mat_filename,csv_filename,isotopomer_mapping_filename,ko_list=[],flux_dict={},description=None):
    '''iteration 3:
    Remove reactions that are thermodynamically unfavorable and add isotopomer data'''
    # Read in the sbml file and define the model conditions
    cobra_model = create_cobra_model_from_sbml_file(model_filename, print_time=True)
    # Modify glucose uptake:
    if cobra_model.reactions.has_id('EX_glc_LPAREN_e_RPAREN__reverse'):
        lb,ub = cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN__reverse').lower_bound,cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN__reverse').upper_bound;
        EX_glc_mets = {};
        EX_glc_mets[cobra_model.metabolites.get_by_id('glc_DASH_D_e')] = -1;
        EX_glc = Reaction('EX_glc_LPAREN_e_RPAREN_');
        EX_glc.add_metabolites(EX_glc_mets);
        cobra_model.add_reaction(EX_glc)
        cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN_').lower_bound = -ub;
        cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN_').upper_bound = lb;
        cobra_model.remove_reactions(['EX_glc_LPAREN_e_RPAREN__reverse'])
    ## Remove thermodynamically infeasible reactions:
    #infeasible = [];
    #loops = [];
    #cobra_model.remove_reactions(infeasible + loops);
    # Apply KOs, if any:
    for ko in ko_list:
        cobra_model.reactions.get_by_id(ko).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(ko).upper_bound = 0.0;
    # Apply flux constraints, if any:
    for rxn,flux in flux_dict.iteritems():
        cobra_model.reactions.get_by_id(rxn).lower_bound = flux['lb'];
        cobra_model.reactions.get_by_id(rxn).upper_bound = flux['ub'];
    # Change description, if any:
    if description:
        cobra_model.description = description;
    # Read in isotopomer model
    isotopomer_mapping = read_isotopomer_mapping_csv(isotopomer_mapping_filename);
    isotopomer_str = build_isotopomer_str(isotopomer_mapping);
    # write model to sbml
    write_cobra_model_to_sbml_file(cobra_model,xml_filename)
    # Add isotopomer field to model
    for r in cobra_model.reactions:
        if isotopomer_str.has_key(r.id):
            cobra_model.reactions.get_by_id(r.id).isotopomer = isotopomer_str[r.id];
        else:
            cobra_model.reactions.get_by_id(r.id).isotopomer = '';
    # Add null basis:
    cobra_model_array = cobra_model.to_array_based_model();
    N = null(cobra_model_array.S.todense()) #convert S from sparse to full and compute the nullspace
    cobra_model.N = N;
    # solve and save pFBA for later use:
    optimize_minimal_flux(cobra_model,True,solver='gurobi');
    # add match field:
    match = numpy.zeros(len(cobra_model.reactions));
    cobra_model.match = match;
    # write model to mat
    save_matlab_model_isotopomer(cobra_model,mat_filename);
    with open(csv_filename,mode='wb') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Reaction','Formula','LB','UB','Genes','Subsystem','Isotopomer'])
        for r in cobra_model.reactions:
            writer.writerow([r.id,
                             r.build_reaction_string(),
                            r.lower_bound,
                            r.upper_bound,
                            r.gene_reaction_rule,
                            r.subsystem,
                            r.isotopomer]);