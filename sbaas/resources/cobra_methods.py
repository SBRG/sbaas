
# Dependencies
import operator, json, csv
from copy import copy
# Dependencies from 3rd party
import scipy.io
from numpy import histogram, mean, std, loadtxt
import matplotlib as mpl
import matplotlib.pyplot as plt
import h5py
from sbaas.resources.molmass import Formula
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra.io.sbml import write_cobra_model_to_sbml_file
from cobra.io.mat import save_matlab_model
from cobra.manipulation.modify import convert_to_irreversible, revert_to_reversible
from cobra.flux_analysis.objective import update_objective
from cobra.flux_analysis.variability import flux_variability_analysis
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis import flux_variability_analysis, single_deletion
from cobra.core.Reaction import Reaction
from cobra.core.Metabolite import Metabolite

class cobra_methods():
    def __init__(self):
        self.model = None;
    def load_ALEWt(self,anoxic = False, oxic = True, update_ampms2 = True, convert2irreversible = False):
        '''load iJO1366 with the following changes:
	    1. update to AMPMS2 to account for carbon monoxide
	    2. changes to uptake bounds for glucose M9 media
	    3. constrain the model to use 'PFK' instead of 'F6PA', 'DHAPT' when grown on glucose
	    4. constrain the model to use the physiologically perferred glutamate synthesis enzymes
	    5. depending on oxygen availability, constrain the model to use the correct RNR enzymes
	    6. depending on oxygen availability, constrain the model to use the correct Dihydroorotate dehydrogenase (PyrD) enzymes
	    7. constrain fatty acid biosynthesis to use the physiologically preferred enzymes'''
        ijo1366_sbml = settings.workspace_data+"/models/iJO1366.xml"
        # Read in the sbml file and define the model conditions
        cobra_model = create_cobra_model_from_sbml_file(ijo1366_sbml, print_time=True)
        if update_ampms2:
            # Update AMPMS2
            coc = Metabolite('co_c','CO','carbon monoxide','c');
            cop = Metabolite('co_p','CO','carbon monoxide','p');
            coe = Metabolite('co_e','CO','carbon monoxide','e');
            cobra_model.add_metabolites([coc,cop,coe])
            ampms2_mets = {};
            ampms2_mets[cobra_model.metabolites.get_by_id('air_c')] = -1;
            ampms2_mets[cobra_model.metabolites.get_by_id('amet_c')] = -1;
            ampms2_mets[cobra_model.metabolites.get_by_id('dad_DASH_5_c')] = 1;
            ampms2_mets[cobra_model.metabolites.get_by_id('met_DASH_L_c')] = 1;
            ampms2_mets[cobra_model.metabolites.get_by_id('4ampm_c')] = 1;
            ampms2_mets[cobra_model.metabolites.get_by_id('h_c')] = 3;
            ampms2_mets[cobra_model.metabolites.get_by_id('for_c')] = 1;
            ampms2_mets[cobra_model.metabolites.get_by_id('co_c')] = 1;
            ampms2 = Reaction('AMPMS3');
            ampms2.add_metabolites(ampms2_mets);
            copp_mets = {};
            copp_mets[cobra_model.metabolites.get_by_id('co_c')] = -1;
            copp_mets[cobra_model.metabolites.get_by_id('co_p')] = 1;
            copp = Reaction('COtpp');
            copp.add_metabolites(copp_mets);
            coex_mets = {};
            coex_mets[cobra_model.metabolites.get_by_id('co_p')] = -1;
            coex_mets[cobra_model.metabolites.get_by_id('co_e')] = 1;
            coex = Reaction('COtex');
            coex.add_metabolites(coex_mets);
            cotrans_mets = {};
            cotrans_mets[cobra_model.metabolites.get_by_id('co_e')] = -1;
            cotrans = Reaction('EX_co_LPAREN_e_RPAREN_');
            cotrans.add_metabolites(cotrans_mets);
            cobra_model.add_reactions([ampms2,copp,coex,cotrans]);
            cobra_model.remove_reactions(['AMPMS2']);
        # Define the model conditions:
        system_boundaries = [x.id for x in cobra_model.reactions if x.boundary == 'system_boundary'];
        for b in system_boundaries:
                cobra_model.reactions.get_by_id(b).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(b).upper_bound = 0.0;
        # Reset demand reactions
        demand = ['DM_4CRSOL',
                'DM_5DRIB',
                'DM_AACALD',
                'DM_AMOB',
                'DM_MTHTHF',
                'DM_OXAM'];
        for d in demand:
                cobra_model.reactions.get_by_id(d).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(d).upper_bound = 1000.0;
        # Change the objective
        update_objective(cobra_model,{'Ec_biomass_iJO1366_WT_53p95M':1.0})
        # Assign KOs

        # Specify media composition (M9 glucose):
        cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN_').lower_bound = -10.0;
        cobra_model.reactions.get_by_id('EX_o2_LPAREN_e_RPAREN_').lower_bound = -18.0;
        #uptake = ['EX_cl_LPAREN_e_RPAREN_',
        #            'EX_so4_LPAREN_e_RPAREN_',
        #            'EX_ca2_LPAREN_e_RPAREN_',
        #            'EX_pi_LPAREN_e_RPAREN_',
        #            'EX_fe2_LPAREN_e_RPAREN_',
        #            'EX_cu2_LPAREN_e_RPAREN_',
        #            'EX_zn2_LPAREN_e_RPAREN_',
        #            'EX_cbl1_LPAREN_e_RPAREN_',
        #            'EX_mobd_LPAREN_e_RPAREN_',
        #            'EX_ni2_LPAREN_e_RPAREN_',
        #            'EX_mn2_LPAREN_e_RPAREN_',
        #            'EX_k_LPAREN_e_RPAREN_',
        #            'EX_nh4_LPAREN_e_RPAREN_',
        #            'EX_cobalt2_LPAREN_e_RPAREN_',
        #            'EX_mg2_LPAREN_e_RPAREN_'];
        uptake = ['EX_ca2_LPAREN_e_RPAREN_',
                    'EX_cbl1_LPAREN_e_RPAREN_',
                    'EX_cl_LPAREN_e_RPAREN_',
                    'EX_co2_LPAREN_e_RPAREN_',
                    'EX_cobalt2_LPAREN_e_RPAREN_',
                    'EX_cu2_LPAREN_e_RPAREN_',
                    'EX_fe2_LPAREN_e_RPAREN_',
                    'EX_fe3_LPAREN_e_RPAREN_',
                    'EX_h_LPAREN_e_RPAREN_',
                    'EX_h2o_LPAREN_e_RPAREN_',
                    'EX_k_LPAREN_e_RPAREN_',
                    'EX_mg2_LPAREN_e_RPAREN_',
                    'EX_mn2_LPAREN_e_RPAREN_',
                    'EX_mobd_LPAREN_e_RPAREN_',
                    'EX_na1_LPAREN_e_RPAREN_',
                    'EX_nh4_LPAREN_e_RPAREN_',
                    'EX_ni2_LPAREN_e_RPAREN_',
                    'EX_pi_LPAREN_e_RPAREN_',
                    'EX_sel_LPAREN_e_RPAREN_',
                    'EX_slnt_LPAREN_e_RPAREN_',
                    'EX_so4_LPAREN_e_RPAREN_',
                    'EX_tungs_LPAREN_e_RPAREN_',
                    'EX_zn2_LPAREN_e_RPAREN_'];
        for u in uptake:
            cobra_model.reactions.get_by_id(u).lower_bound = -1000.0;
        # Specify allowed secretion products
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
        # Constrain specific reactions
        noFlux = ['F6PA', 'DHAPT'];
        ammoniaExcess = ['GLUDy']; # PMCID: 196288
        # RNR control (DOI:10.1111/j.1365-2958.2006.05493.x)
        # Dihydroorotate dehydrogenase (PyrD) (DOI:10.1016/S0076-6879(78)51010-0, PMID: 199252, DOI:S0969212602008316 [pii])
        aerobic = ['RNDR1', 'RNDR2', 'RNDR3', 'RNDR4', 'DHORD2', 'ASPO6','LCARR','PFL','FRD2','FRD3']; # see DOI:10.1111/j.1365-2958.2011.07593.x; see DOI:10.1089/ars.2006.8.773 for a review
        anaerobic = ['RNTR1c2', 'RNTR2c2', 'RNTR3c2', 'RNTR4c2', 'DHORD5', 'ASPO5','PDH','SUCDi']; # see DOI:10.1074/jbc.274.44.31291, DOI:10.1128/JB.00440-07
        if anoxic:
            rxnList = noFlux + ammoniaExcess + anaerobic;
            for rxn in rxnList:
                cobra_model.reactions.get_by_id(rxn).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(rxn).upper_bound = 0.0;
        elif oxic:
            rxnList = noFlux + ammoniaExcess + aerobic;
            for rxn in rxnList:
                cobra_model.reactions.get_by_id(rxn).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(rxn).upper_bound = 0.0;
        else:
            rxnList = noFlux + ammoniaExcess;
            for rxn in rxnList:
                cobra_model.reactions.get_by_id(rxn).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(rxn).upper_bound = 0.0;
        # Set the direction for specific reactions
        # Fatty acid biosynthesis: DOI: 10.1016/j.ymben.2010.10.007, PMCID: 372925
        fattyAcidSynthesis = ['ACCOAC', 'ACOATA', 'HACD1', 'HACD2', 'HACD3', 'HACD4', 'HACD5', 'HACD6', 'HACD7', 'HACD8', 'KAS14', 'KAS15', 'MACPD', 'MCOATA', '3OAR100', '3OAR120', '3OAR121', '3OAR140', '3OAR141', '3OAR160', '3OAR161', '3OAR180', '3OAR181', '3OAR40', '3OAR60', '3OAR80']
        fattyAcidOxidation = ['ACACT1r', 'ACACT2r', 'ACACT3r', 'ACACT4r', 'ACACT5r', 'ACACT6r', 'ACACT7r', 'ACACT8r', 'ACOAD1f', 'ACOAD2f', 'ACOAD3f', 'ACOAD4f', 'ACOAD5f', 'ACOAD6f', 'ACOAD7f', 'ACOAD8f', 'CTECOAI6', 'CTECOAI7', 'CTECOAI8', 'ECOAH1', 'ECOAH2', 'ECOAH3', 'ECOAH4', 'ECOAH5', 'ECOAH6', 'ECOAH7', 'ECOAH8']
        ndpk = ['NDPK1','NDPK2','NDPK3','NDPK4','NDPK5','NDPK7','NDPK8'];
        rxnList = fattyAcidSynthesis + fattyAcidOxidation;
        for rxn in rxnList:
            cobra_model.reactions.get_by_id(rxn).lower_bound = 0.0;
            cobra_model.reactions.get_by_id(rxn).upper_bound = 1000.0;
        # convert to irreversible
        if convert2irreversible: convert_to_irreversible(cobra_model);

        return cobra_model;
    def reduce_model(self,cobra_model,cobra_model_outFileName=None):
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
        #with open("data/ijo1366_irrev_fva.json", 'w') as outfile:
        #    json.dump(data, outfile, indent=4);

        #fva_data = json.load(open("data/ijo1366_irrev_fva.json"));

        # Reduce model
        rxns_noflux = [];
        for k,v in fva_data.items():
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
            print('reduced model is inconsistent with the original model')
            print('original model solution: ' + str(sol_f))
            print('reduced model solution: ' + str(sol_reduced_f))
    def reduce_model_pfba(self,cobra_model,cobra_model_outFileName=None,fba_outFileName=None,subs=[]):
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
        for k,v in cobra_model.solution.x_dict.items():
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
                for k,v in cobra_model.solution.x_dict.items():
                    writer.writerow([k,v]);

        cobra_model.optimize()
        sol_reduced_f = cobra_model.solution.f

        # Check that the reduced model is consistent with the original model
        if not sol_f == sol_reduced_f:
            print('reduced model is inconsistent with the original model')
            print('original model solution: ' + str(sol_f))
            print('reduced model solution: ' + str(sol_reduced_f))
    def add_net_reaction(self,cobra_model_IO, rxn_dict_I,remove_reverse=False):
        '''add a net reaction to the model after removing
        the individual reactions'''
        # input: rxn_dict_I = dictionary of net reaction ids and
        #                       corresponding list of individual reaction ids
        # output: cobra_model_IO = individual reactions replaced with a
        #                           net reaction

        cobra_model_IO.optimize();
        sol_orig = cobra_model_IO.solution.f;
        print("original model solution", sol_orig)

        try:
            cobra_model_tmp = cobra_model_IO.copy2();
        except KeyError as e:
            print(e); 

        # make net reactions:
        rxn_dict_net = {};
        for k,v in rxn_dict_I.items():
            rxn_net = make_net_reaction(cobra_model_tmp, k, v['reactions'],v['stoichiometry']);
            if rxn_net:
                rxn_net.lower_bound = 0.0;
                rxn_net.upper_bound = 1000.0;
                rxn_net.objective_coefficient = 0.0;
            else:
                print('an error occured in add_net_reaction')
                exit(-1)

            #rxn_net.reversibility = False;
            rxn_dict_net[k] = (v['reactions'],rxn_net);

        # add replace individual reactions with net reaction
        for k,v in rxn_dict_net.items():
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
            print(k, sol_new)
    def make_net_reaction(self,cobra_model_I, rxn_id_I, rxn_list_I,stoich_list_I):
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
            print("error in " + rxn_id_I + ": there are " + str(len(rxn_list_I)) + " rxn ids and " + str(len(stoich_list_I)) + " coefficients");
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
    def get_solBySub(self,cobra_model_I,sol_I,sub_I):

        sol_O = {};
        for k,v in sol_I.items():
            try:
                if cobra_model_I.reactions.get_by_id(k).subsystem == sub_I:
                    sol_O[k] = v;
            except:
                print(k + ' reaction not found')

        return sol_O;
    def groupBySameFlux(self,cobra_model_I,sol_I):

        flux_list = [];
        for r,f in sol_I.items():
            if not f in flux_list and float(f)>0.0:
                flux_list.append(f)
            
        sameFlux_O = {};
        for f in flux_list:
            rxn_list = [];
            for r,v in sol_I.items():
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
    def add_net_reaction_subsystem(self,cobra_model_IO,sol_I,subs_I):
        '''make net reactions for specific subsystems grouped 
        by reactions that have the same flux from pfba'''
        #input: cobra_model
        #       sol_I = pfba solution
        #       sub_I = list of model subsystems
        #output: cobra_model
    
        # Make net reactions for pathways outside of the scope
        # of the isotopomer model
        for s in subs_I:
            sol = get_solBySub(cobra_model_IO,sol_I,s)
            sameFlux = groupBySameFlux(cobra_model_IO,sol)
            netRxns = {};
            for k,v in sameFlux.items():
                if len(v['reactions'])>1: 
                    netRxns[k] = v;
            add_net_reaction(cobra_model_IO,netRxns);
            # add subsystem information back in
            for k in sameFlux.keys():
                cobra_model_IO.reactions.get_by_id(k).subsystem = s
            remove_noflux_reactions(cobra_model_IO,sol_I,subs_I)
    def remove_noflux_reactions(self,cobra_model,sol=None,subs=[]):
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
                for k,v in sol.items():
                    try:
                        if (float(v) < 0.0 or float(v) == 0.0) and cobra_model.reactions.get_by_id(k).subsystem in subs:
                            cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
                            cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
                            cobra_model.remove_reactions(k)
                            rxns_noflux.append(k);
                    except:
                        print('reaction is not in model: ' + k)
            else:
                for k,v in sol.items():
                    try:
                        if (float(v) < 0.0 or float(v) == 0.0):
                            cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
                            cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
                            cobra_model.remove_reactions(k)
                            rxns_noflux.append(k);
                    except:
                        print('reaction is not in model: ' + k)
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
            print('reduced model is inconsistent with the original model')
            print('original model solution: ' + str(sol_f))
            print('reduced model solution: ' + str(sol_reduced_f))
    def get_reactionsInfo(self,cobra_model):
        '''return the number of reactions and the number of reactions 
        that cannot carry a flux (i.e. lb and ub of 0.0)'''
        nrxn_O = len(cobra_model.reactions);
        nrxn_noflux_O = 0;
        for r in cobra_model.reactions:
            if r.lower_bound == 0.0 and r.upper_bound == 0.0:
                nrxn_noflux_O += 1;
        return nrxn_O, nrxn_noflux_O