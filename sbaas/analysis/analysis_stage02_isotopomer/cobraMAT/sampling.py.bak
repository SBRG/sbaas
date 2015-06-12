# Dependencies
import operator, json, csv
# Dependencies from 3rd party
import scipy.io
from numpy import histogram, mean, std, loadtxt
import matplotlib as mpl
import matplotlib.pyplot as plt
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra.flux_analysis import flux_variability_analysis, single_deletion
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis.objective import update_objective

def get_points_matlab(matlab_data,sampler_model_name):
    '''load sampling points from MATLAB'''

    # load model from MATLAB file
    model = load_matlab_model(matlab_data,sampler_model_name);

    # load sample points from MATLAB file into numpy array
    points = scipy.io.loadmat(matlab_data)[sampler_model_name]['points'][0][0];
    #mat = scipy.io.loadmat('data\\EvoWt.mat')
    #points = mat['model_WT_sampler_out']['points'][0][0]

    points_dict = {};
    for i,r in enumerate(model.reactions):
        # convert names:
        r_id_conv = r.id.replace('-','_DASH_');
        r_id_conv = r_id_conv.replace('(','_LPAREN_');
        r_id_conv = r_id_conv.replace(')','_RPAREN_');
        # extract points
        points_dict[r_id_conv] = {'points':points[i,:],
                             'mean':mean(points[i,:]),
                             'std':std(points[i,:])}

    return points_dict;

def get_points_numpy(numpy_data,ijo1366_sbml):
    '''load sampling points from numpy file'''

    # load points from numpy file
    points = loadtxt(numpy_data);

    # Read in the sbml file and define the model conditions
    cobra_model = create_cobra_model_from_sbml_file(ijo1366_sbml, print_time=True)

    points_dict = {};
    for i,r in enumerate(cobra_model.reactions):
        # extract points
        points_dict[r.id] = {'points':points[i,:],
                             'mean':mean(points[i,:]),
                             'std':std(points[i,:])}

    return points_dict;

def plot_points(points_dict):
    '''plot sampling points from MATLAB'''
    reaction_lst = ['ENO','FBA','FBP','G6PP','GAPD','GLBRAN2',
                    'GLCP','GLCP2','GLDBRAN2','HEX1','PDH','PFK',
                    'PGI','PGK','PGM','PPS','PYK','TPI','ENO_reverse',
                    'FBA_reverse','GAPD_reverse','PGI_reverse',
                    'PGK_reverse','PGM_reverse','TPI_reverse']
    for r in reaction_lst:
        # loop through each reaction in the list
        plt.figure()
        n, bins, patches = plt.hist(points_dict[r]['points'],50,label = [r])
        plt.legend()
        plt.show()

def simulate_loops(ijo1366_sbml,data_fva):
    '''Simulate FVA after closing exchange reactions and setting ATPM to 0
    reactions with flux will be involved in loops'''

    # Read in the sbml file and define the model conditions
    cobra_model = create_cobra_model_from_sbml_file(ijo1366_sbml, print_time=True)
    # Change all uptake reactions to 0
    for rxn in cobra_model.reactions:
        if 'EX_' in rxn.id and '_LPAREN_e_RPAREN_' in rxn.id:
            rxn.lower_bound = 0.0;
    # Set ATPM to 0
    cobra_model.reactions.get_by_id('ATPM').lower_bound = 0.0

    # calculate the reaction bounds using FVA
    reaction_bounds = flux_variability_analysis(cobra_model, fraction_of_optimum=0.9,
                                      objective_sense='maximize', the_reactions=None,
                                      allow_loops=True, solver='gurobi',
                                      the_problem='return', tolerance_optimality=1e-6,
                                      tolerance_feasibility=1e-6, tolerance_barrier=1e-8,
                                      lp_method=1, lp_parallel=0, new_objective=None,
                                      relax_b=None, error_reporting=None,
                                      number_of_processes=1, copy_model=False);

    # Update the data file
    with open(data_fva, 'wb') as outfile:
        json.dump(reaction_bounds, outfile, indent=4);

def find_loops(data_fva):
    '''extract out loops from simulate_loops'''

    data_loops = json.load(open(data_fva))
    rxn_loops = [];
    for k,v in data_loops.iteritems():
        if abs(v['minimum'])>1.0 or abs(v['maximum'])>1.0:
            rxn_loops.append(k);
    return rxn_loops

def remove_loopsFromPoints(rxn_loops, points_dict):
    '''remove reactions with loops from sampling points'''

    points_loopless = {};
    points_loopless_mean = {};
    for k,v in points_dict.iteritems():
        if k in rxn_loops: continue
        else: 
            points_loopless[k] = v;
            points_loopless_mean[k] = {'mean':v['mean'],'std':v['std']};

    return points_loopless_mean;

def export_points(ijo1366_sbml, points_loopless_mean, data_srd, data_pfba, data_points):
    '''export sampling analysis'''

    srd = json.load(open(data_srd));
    pfba = json.load(open(data_pfba));
    
    # Read in the sbml file and define the model conditions
    cobra_model = create_cobra_model_from_sbml_file(ijo1366_sbml, print_time=True)

    points = {};
    assay = ['glx_c', 'glyclt_c', 'pyr_c', 'ala_DASH_L_c', 'lac_DASH_L_c', 'oxa_c', 'acac_c',
             'ser_DASH_L_c', 'ura_c', 'fum_c', 'mmal_c', 'succ_c', 'thr_DASH_L_c', 'thym_c',
             '5oxpro_c', 'glutacon_c', 'orn_c', 'asn_DASH_L_c', 'oaa_c', 'asp_DASH_L_c',
             'mal_DASH_L_c', 'ade_c', 'hxan_c', 'actp_c', 'gln_DASH_L_c', 'akg_c', 'glu_DASH_L_c',
             'met_DASH_L_c', 'gua_c', 'xan_c', 'his_DASH_L_c', 'phpyr_c', 'phe_DASH_L_c', 'urate_c',
             'pep_c', 'dhap_c', 'g3p_c', 'glyc3p_c', 'arg_DASH_L_c', 'acon_DASH_C_c', 'citr_DASH_L_c',
             'tyr_DASH_L_c', '2pg_c', '3pg_c', 'cit_c', 'icit_c', 'trp_DASH_L_c', 'r5p_c',
             'ru5p_DASH_D_c', 'Lcystin_c', 'cytd_c', 'btn_c', 'uri_c', 'gam6p_c', 'g6p_c',
             'f6p_c', 'g1p_c', 'f1p_c', '23dpg_c', 'adn_c', 'ins_c', '6pgc_c', 'gsn_c',
             's7p_c', 'gthrd_c', 'dcmp_c', 'dump_c', 'dtmp_c', 'cmp_c', 'ump_c',
             'camp_c', 'damp_c', 'dimp_c', 'fdp_c', '35cgmp_c', 'amp_c', 'dgmp_c',
             'imp_c', 'gmp_c', 'ribflv_c', 'dcdp_c', 'prpp_c', 'udp_c', 'dadp_c',
             'adp_c', 'dgdp_c', 'fol_c', 'gdp_c', 'dctp_c', 'dutp_c', 'dttp_c',
             'ctp_c', 'utp_c', 'datp_c', 'ditp_c', 'atp_c', 'itp_c', 'gtp_c',
             'dtdpglu_c', 'adpglc_c', 'gthox_c', 'nad_c', 'nadh_c', 'nadp_c',
             'nadph_c', 'coa_c', 'fad_c', 'accoa_c', 'succoa_c'];
    # combine analyses into a final data structure
    for k,v in points_loopless_mean.iteritems():
        ngenes = len(cobra_model.reactions.get_by_id(k).genes)
        genes = ', '.join(i.id for i in cobra_model.reactions.get_by_id(k).genes);
        nmets_down = len([i.id for i in cobra_model.reactions.get_by_id(k).products if i.compartment == 'c' and i.id in assay]);
        mets_down = ', '.join(i.id for i in cobra_model.reactions.get_by_id(k).products if i.compartment == 'c' and i.id in assay);
        nmets_up = len([i.id for i in cobra_model.reactions.get_by_id(k).reactants if i.compartment == 'c' and i.id in assay]);
        mets_up = ', '.join(i.id for i in cobra_model.reactions.get_by_id(k).reactants if i.compartment == 'c' and i.id in assay);
        #points[k] = {'mean':v['mean'],'std':v['std'],'gr_ratio':srd[k]['gr_ratio'],'pfba':pfba[k]};
        points[k] = {'mean':v['mean'],'std':v['std'],'gr_ratio':srd[k]['gr_ratio'],
                     'ngenes':ngenes,'genes':genes,'nmets_up':nmets_up,'mets_up':mets_up,
                     'nmets_down':nmets_down,'mets_down':mets_down};

    # Update the data file
    with open(data_points, 'wb') as outfile:
        csvwriter = csv.writer(outfile);
        #csvwriter.writerow(['rxn_id','mean','mean_abs','std','gr_ratio','pfba']);
        csvwriter.writerow(['rxn_id','mean','mean_abs','std','gr_ratio','ngenes','genes','nmets_up','mets_up','nmets_down','mets_down']);
        for k,v in points.iteritems():
            csvwriter.writerow([k,v['mean'],abs(v['mean']),v['std'],v['gr_ratio'],
                                v['ngenes'],v['genes'],v['nmets_up'],v['mets_up'],
                                v['nmets_down'],v['mets_down']]);
            #csvwriter.writerow([k,v['mean'],abs(v['mean']),v['std'],v['gr_ratio'],v['pfba']]);
        #json.dump(reaction_bounds, outfile, indent=4);

def _main_():
    # data files:
    matlab_data = 'data\\EvoWt.mat'
    numpy_data = 'data\\samplertest.txt'
    ijo1366_sbml = "data\\ijo1366_netrxn_irreversible.xml"
    data_fva = 'data\\ijo1366_netrxn_irreversible_fva_loops.json';
    data_points = 'data\\ijo1366_netrxn_irreversible_sampling_loopless.csv';

    points_dict = get_points_numpy(numpy_data,ijo1366_sbml);
    plot_points(points_dict);
    simulate_loops(ijo1366_sbml,data_fva);
    rxn_loops = find_loops(data_fva);
    points_loopless_mean = remove_loopsFromPoints(rxn_loops, points_dict)
    #export_points(ijo1366_sbml, points_loopless_mean, data_srd, data_pfba, data_points);