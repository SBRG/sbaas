# Dependencies
import operator, json, csv
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra.io.sbml import write_cobra_model_to_sbml_file
from cobra.io.mat import save_matlab_model
from cobra.manipulation.modify import convert_to_irreversible, revert_to_reversible
from cobra.flux_analysis.objective import update_objective
from cobra.flux_analysis.variability import flux_variability_analysis
from cobra.flux_analysis.parsimonious import optimize_minimal_flux

def reduce_model(cobra_model,cobra_model_outFileName=None):
    '''reduce model'''
    # Input: cobra_model
    # Output: cobra_model 
    #         the lower and upper bounds have been set to 0.0
    #         for all reactions that cannot carry a flux
    cobra_model.optimize()
    sol_f = cobra_model.solution.f

    fva_data = flux_variability_analysis(cobra_model, fraction_of_optimum=0.9,
                                          objective_sense='maximize', the_reactions=None,
                                          allow_loops=True, solver='gurobi',
                                          the_problem='return', tolerance_optimality=1e-6,
                                          tolerance_feasibility=1e-6, tolerance_barrier=1e-8,
                                          lp_method=1, lp_parallel=0, new_objective=None,
                                          relax_b=None, error_reporting=None,
                                          number_of_processes=1, copy_model=False);
    #with open("data\\ijo1366_irrev_fva.json", 'w') as outfile:
    #    json.dump(data, outfile, indent=4);

    #fva_data = json.load(open("data\\ijo1366_irrev_fva.json"));

    # Reduce model
    rxns_noflux = [];
    for k,v in fva_data.iteritems():
        if v['minimum'] == 0.0 and v['maximum'] == 0.0:
            cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
            cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
            rxns_noflux.append(k);

    if cobra_model_outFileName:
        write_cobra_model_to_sbml_file(cobra_model,cobra_model_outFileName)

    cobra_model.optimize()
    sol_reduced_f = cobra_model.solution.f

    # Check that the reduced model is consistent with the original model
    if not sol_f == sol_reduced_f:
        print 'reduced model is inconsistent with the original model'
        print 'original model solution: ' + str(sol_f)
        print 'reduced model solution: ' + str(sol_reduced_f)

def reduce_model_pfba(cobra_model,cobra_model_outFileName=None,fba_outFileName=None,subs=[]):
    '''reduce model using pfba'''
    # Input: cobra_model
    #        cobra_model_outFileName
    #        subs = string of specific subsystems to reduce
    # Output: cobra_model 
    #         the lower and upper bounds have been set to 0.0
    #         for all reactions that cannot carry a flux
    cobra_model.optimize()
    sol_f = cobra_model.solution.f

    # Find minimal flux solution:
    pfba = optimize_minimal_flux(cobra_model,True,solver='gurobi');

    # Reduce model
    rxns_noflux = [];
    # set lb and ub for all reactions with 0 flux to 0;
    for k,v in cobra_model.solution.x_dict.iteritems():
        if (v < 0.0 or v == 0.0) and cobra_model.reactions.get_by_id(k).subsystem in subs:
            cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
            cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
            rxns_noflux.append(k);

    if cobra_model_outFileName:
        write_cobra_model_to_sbml_file(cobra_model,cobra_model_outFileName)

    if pfba_outFileName:
        # Write pfba solution to file
        with open(pfba_outFileName,mode='wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Reaction','Flux'])
            for k,v in cobra_model.solution.x_dict.iteritems():
                writer.writerow([k,v]);

    cobra_model.optimize()
    sol_reduced_f = cobra_model.solution.f

    # Check that the reduced model is consistent with the original model
    if not sol_f == sol_reduced_f:
        print 'reduced model is inconsistent with the original model'
        print 'original model solution: ' + str(sol_f)
        print 'reduced model solution: ' + str(sol_reduced_f)

def add_net_reaction(cobra_model_IO, rxn_dict_I,remove_reverse=False):
    '''add a net reaction to the model after removing
    the individual reactions'''
    # input: rxn_dict_I = dictionary of net reaction ids and
    #                       corresponding list of individual reaction ids
    # output: cobra_model_IO = individual reactions replaced with a
    #                           net reaction

    cobra_model_IO.optimize();
    sol_orig = cobra_model_IO.solution.f;
    print "original model solution", sol_orig

    try:
        cobra_model_tmp = cobra_model_IO.copy2();
    except KeyError as e:
        print e; 

    # make net reactions:
    rxn_dict_net = {};
    for k,v in rxn_dict_I.iteritems():
        rxn_net = make_net_reaction(cobra_model_tmp, k, v['reactions'],v['stoichiometry']);
        if rxn_net:
            rxn_net.lower_bound = 0.0;
            rxn_net.upper_bound = 1000.0;
            rxn_net.objective_coefficient = 0.0;
        else:
            print 'an error occured in add_net_reaction'
            exit(-1)

        #rxn_net.reversibility = False;
        rxn_dict_net[k] = (v['reactions'],rxn_net);

    # add replace individual reactions with net reaction
    for k,v in rxn_dict_net.iteritems():
        cobra_model_IO.remove_reactions(v[0]);
        # remove the reverse reaction if it exists for irreversible models
        if remove_reverse:
            for rxn in v[0]:
                if '_reverse' in rxn:
                    rxn_rev = rxn.replace('_reverse','')
                    if cobra_model_IO.reactions.has_id(rxn_rev): cobra_model_IO.remove_reactions(rxn_rev);
                else:
                    rxn_rev = rxn+'_reverse';
                    if cobra_model_IO.reactions.has_id(rxn_rev): cobra_model_IO.remove_reactions(rxn_rev);
        cobra_model_IO.add_reaction(v[1]);
        cobra_model_IO.optimize();
        sol_new = cobra_model_IO.solution.f;
        print k, sol_new

def make_net_reaction(cobra_model_I, rxn_id_I, rxn_list_I,stoich_list_I):
    '''generate a net reaction from a list of individual reactions'''
    # input: rxn_list_I = list of reaction IDs
    # output: rxn_net_O = net reaction (cobra Reaction object)
    from cobra.core.Reaction import Reaction

    #rxn_net_O = cobra_model_I.reactions.get_by_id(rxn_list_I[0]);
    #for r in rxn_list_I[1:]:
    #    if cobra_model_I.reactions.get_by_id(r).reversibility:
    #        print r + " is reversible!";
    #        print "continue?"
    #    rxn_net_O += cobra_model_I.reactions.get_by_id(r);

    # check input:
    if not len(stoich_list_I) == len(rxn_list_I):
        print "error in " + rxn_id_I + ": there are " + str(len(rxn_list_I)) + " rxn ids and " + str(len(stoich_list_I)) + " coefficients";
        exit(-1);

    rxn_net_O = Reaction(rxn_id_I);
    for i,r in enumerate(rxn_list_I):
        mets = {};
        metlist = [];
        metlist = cobra_model_I.reactions.get_by_id(r).products + cobra_model_I.reactions.get_by_id(r).reactants;
        for met in metlist:
            mets[met] = cobra_model_I.reactions.get_by_id(r).get_coefficient(met)*stoich_list_I[i];
        rxn_net_O.add_metabolites(mets);
        rxn_net_O.subsystem = cobra_model_I.reactions.get_by_id(r).subsystem; #copy over the subsystem
    
    # check net reaction
    #if not rxn_net_O.check_mass_balance():  
        #print "error: " + rxn_id_I + " is not elementally balanced";

    #print rxn_net_O.id;
    #print rxn_net_O.build_reaction_string();
    return rxn_net_O;

def get_solBySub(cobra_model_I,sol_I,sub_I):

    sol_O = {};
    for k,v in sol_I.iteritems():
        try:
            if cobra_model_I.reactions.get_by_id(k).subsystem == sub_I:
                sol_O[k] = v;
        except:
            print k + ' reaction not found'

    return sol_O;

def groupBySameFlux(cobra_model_I,sol_I):

    flux_list = [];
    for r,f in sol_I.iteritems():
        if not f in flux_list and float(f)>0.0:
            flux_list.append(f)
            
    sameFlux_O = {};
    for f in flux_list:
        rxn_list = [];
        for r,v in sol_I.iteritems():
            if v==f:
                rxn_list.append(r);
        stoich = [1]*len(rxn_list)
        rxnName = '';
        for rxn in rxn_list:
            rxnName = rxnName + rxn + '_';
        rxnName = rxnName[:-1];
        # check that the reaction name is less than 225 characters
        if len(rxnName)>224:
            rxnName = rxnName[:224];
        sameFlux_O[rxnName] = {'reactions':rxn_list,
                           'stoichiometry':stoich,
                            'flux':f};
        #netRxn = make_net_reaction(cobra_model_copy,rxnName,rxn_list,stoich)
        #sameFlux_O[rxnName] = {'reactions':rxn_list,
        #                   'stoichiometry':stoich,
        #                    'flux':f,
        #                    'net':netRxn};

    return sameFlux_O

def add_net_reaction_subsystem(cobra_model_IO,sol_I,subs_I):
    '''make net reactions for specific subsystems grouped 
    by reactions that have the same flux from pfba'''
    #input: cobra_model
    #       sol_I = pfba solution
    #       sub_I = list of model subsystems
    #output: cobra_model
    
    # convert model to irreversible
    # convert_to_irreversible(cobra_model_IO);
    # Make net reactions for pathways outside of the scope
    # of the isotopomer model
    for s in subs_I:
        sol = get_solBySub(cobra_model_IO,sol_I,s)
        sameFlux = groupBySameFlux(cobra_model_IO,sol)
        netRxns = {};
        for k,v in sameFlux.iteritems():
            if len(v['reactions'])>1: 
                netRxns[k] = v;
        add_net_reaction(cobra_model_IO,netRxns);
        # add subsystem information back in
        for k in sameFlux.iterkeys():
            cobra_model_IO.reactions.get_by_id(k).subsystem = s
        remove_noflux_reactions(cobra_model_IO,sol_I,subs_I)
    # convert model back to reversible
    # revert_to_reversible(cobra_model_IO);

def remove_noflux_reactions(cobra_model,sol=None,subs=[]):
    '''remove noflux reactions'''
    # Input: cobra_model
    #        sol = pfba solution
    #        subs = string of specific subsystems to reduce
    # Output: cobra_model 
    #         if the lower and upper bounds are zero, the reactions
    #         are removed
    cobra_model.optimize()
    sol_f = cobra_model.solution.f
    
    # Reduce model
    rxns_noflux = [];
    # set lb and ub for all reactions with 0 flux to 0;
    if sol:
        if subs:
            for k,v in sol.iteritems():
                try:
                    if (float(v) < 0.0 or float(v) == 0.0) and cobra_model.reactions.get_by_id(k).subsystem in subs:
                        cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
                        cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
                        cobra_model.remove_reactions(k)
                        rxns_noflux.append(k);
                except:
                    print 'reaction is not in model: ' + k
        else:
            for k,v in sol.iteritems():
                try:
                    if (float(v) < 0.0 or float(v) == 0.0):
                        cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
                        cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
                        cobra_model.remove_reactions(k)
                        rxns_noflux.append(k);
                except:
                    print 'reaction is not in model: ' + k
    else:
        if subs:
            for r in cobra_model.reactions:
                if r.lower_bound == 0.0 and r.upper_bound == 0.0 and cobra_model.reactions.get_by_id(r.id).subsystem in subs:
                    cobra_model.remove_reactions(r.id)
        else:
            for r in cobra_model.reactions:
                if r.lower_bound == 0.0 and r.upper_bound == 0.0:
                    cobra_model.remove_reactions(r.id)
                
    cobra_model.optimize()
    sol_reduced_f = cobra_model.solution.f

    # Check that the reduced model is consistent with the original model
    if not sol_f == sol_reduced_f:
        print 'reduced model is inconsistent with the original model'
        print 'original model solution: ' + str(sol_f)
        print 'reduced model solution: ' + str(sol_reduced_f)

def get_reactionsInfo(cobra_model):
    '''return the number of reactions and the number of reactions 
    that cannot carry a flux (i.e. lb and ub of 0.0)'''
    nrxn_O = len(cobra_model.reactions);
    nrxn_noflux_O = 0;
    for r in cobra_model.reactions:
        if r.lower_bound == 0.0 and r.upper_bound == 0.0:
            nrxn_noflux_O += 1;
    return nrxn_O, nrxn_noflux_O
