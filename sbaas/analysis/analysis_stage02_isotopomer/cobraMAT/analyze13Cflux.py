# Dependencies
import json, csv
from math import fabs, sqrt, pow
# Dependencies from 3rd party
import scipy.io
import numpy
import h5py
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file, write_cobra_model_to_sbml_file
from cobra.io import load_matlab_model
# Dependencies that will break (analysis.analysis_base.base_exportData import base_exportData)
from analysis.analysis_base.base_exportData import base_exportData

def load_isotopomer_matlab(matlab_data,isotopomer_data=None):
    '''Load 13CFlux isotopomer simulation data from matlab file'''
    # load measured isotopomers from MATLAB file into numpy array
    # load names and calculated isotopomers from MATLAB file into numpy array
    names = scipy.io.loadmat(matlab_data)['output']['names'][0][0];
    calculated_ave = scipy.io.loadmat(matlab_data)['output']['ave'][0][0];
    calculated_stdev = scipy.io.loadmat(matlab_data)['output']['stdev'][0][0];
    # load residuals from MATLAB file into numpy array
    residuals = scipy.io.loadmat(matlab_data)['residuals'];
    if isotopomer_data:
        measured_dict = json.load(open(isotopomer_data,'r'));
        measured_names = [];
        measured_ave = [];
        measured_stdev = [];
        # extract data to lists
        for frag,data in measured_dict['fragments'].items():
            for name in data['data_names']:
                measured_names.append(name);
            for ave in data['data_ave']:
                measured_ave.append(ave);
            for stdev in data['data_stdev']:
                measured_stdev.append(stdev);
        # convert lists to dict
        measured_dict = {};
        for i,name in enumerate(measured_names):
            measured_dict[name]={'measured_ave':measured_ave[i],
                                   'measured_stdev':measured_stdev[i]};
        # match measured names to calculated names
        measured_ave = [];
        measured_stdev = [];
        residuals = [];
        for i,name in enumerate(names):
            if name[0][0] in measured_dict:
                measured_ave.append(measured_dict[name[0][0]]['measured_ave']);
                measured_stdev.append(measured_dict[name[0][0]]['measured_stdev']);
                residuals.append(measured_dict[name[0][0]]['measured_ave']-calculated_ave[i][0]);
            else:
                measured_ave.append(None);
                measured_stdev.append(None);
                residuals.append(None);
    else:
        measured_ave_tmp = scipy.io.loadmat(matlab_data)['toCompare'];
        measured_ave = [];
        for d in measured_ave_tmp:
            measured_ave.append(d[0]);
        measured_stdev = numpy.zeros(len(measured_ave));
    # combine into a dictionary
    isotopomer = {};
    for i in range(len(names)):
        isotopomer[names[i][0][0]] = {'measured_ave':measured_ave[i], #TODO: extract out by fragment names
                                'measured_stdev':measured_stdev[i],
                                'calculated_ave':calculated_ave[i][0],
                                'calculated_stdev':calculated_stdev[i][0],
                                'residuals':residuals[i]};

    return isotopomer;

def load_confidenceIntervals_matlab(matlab_data,cobra_model_matlab,cobra_model_name):
    '''Load confidence intervals from matlab file'''
    # load confidence intervals from MATLAB file into numpy array
    cimin_h5py = h5py.File(matlab_data)['ci']['minv'][0];
    cimax_h5py = h5py.File(matlab_data)['ci']['maxv'][0];
    cimin = numpy.array(cimin_h5py);
    cimax = numpy.array(cimax_h5py);
    # load cobramodel
    rxns = scipy.io.loadmat(cobra_model_matlab)[cobra_model_name]['rxns'][0][0]
    # combine cimin, cimax, and rxns into dictionary
    ci = {};
    for i in range(len(cimin)):
        ci[rxns[i][0][0]] = {'minv':cimin[i],'maxv':cimax[i]};

    return ci;

def compare_isotopomers_calculated(isotopomer_1, isotopomer_2):
    '''compare two calculated isotopomer distributions'''
    # extract into lists
    absDif_list = [];
    ssr_1_list = [];
    ssr_2_list = [];
    bestFit_list = [];
    frag_list = [];
    ssr_1 = 0.0; # sum of squared residuals (threshold of 10e1, Antoniewicz poster, co-culture, Met Eng X)
    ssr_2 = 0.0;
    measured_1_list = [];
    measured_2_list = [];
    calculatedAve_1_list = [];
    calculatedAve_2_list = [];
    measuredStdev_1_list = [];
    measuredStdev_2_list = [];
    for frag,data in isotopomer_1.items():
        absDif = 0.0;
        sr_1 = 0.0;
        sr_2 = 0.0;
        bestFit = None;
        absDif = fabs(isotopomer_1[frag]['calculated_ave'] - isotopomer_2[frag]['calculated_ave']);
        sr_1 = pow(isotopomer_1[frag]['calculated_ave']-isotopomer_1[frag]['measured_ave'],2);
        sr_2 = pow(isotopomer_2[frag]['calculated_ave']-isotopomer_2[frag]['measured_ave'],2);
        if sr_1>sr_2: bestFit = '2';
        elif sr_1<sr_2: bestFit = '1';
        elif sr_1==sr_2: bestFit = None;
        absDif_list.append(absDif);
        ssr_1_list.append(sr_1);
        ssr_2_list.append(sr_2);
        bestFit_list.append(bestFit);
        frag_list.append(frag);
        ssr_1 += sr_1;
        ssr_2 += sr_2;
        measured_1_list.append(isotopomer_1[frag]['measured_ave'])
        measured_2_list.append(isotopomer_2[frag]['measured_ave'])
        calculatedAve_1_list.append(isotopomer_1[frag]['calculated_ave']);
        calculatedAve_2_list.append(isotopomer_2[frag]['calculated_ave']);
        measuredStdev_1_list.append(isotopomer_1[frag]['measured_stdev']);
        measuredStdev_2_list.append(isotopomer_2[frag]['measured_stdev']);

    # calculate the correlation coefficient
    # 1. between measured vs. calculated (1 and 2)
    # 2. between calculated 1 vs. calculated 2
    r_measuredVsCalculated_1 = None;
    r_measuredVsCalculated_2 = None;
    r_measured1VsMeasured2 = None;
    p_measuredVsCalculated_1 = None;
    p_measuredVsCalculated_2 = None;
    p_measured1VsMeasured2 = None;

    r_measuredVsCalculated_1, p_measuredVsCalculated_1 = scipy.stats.pearsonr(measured_1_list,calculatedAve_1_list);
    r_measuredVsCalculated_2, p_measuredVsCalculated_2 = scipy.stats.pearsonr(measured_2_list,calculatedAve_2_list);
    r_measured1VsMeasured2, p_measured1VsMeasured2 = scipy.stats.pearsonr(calculatedAve_1_list,calculatedAve_2_list);

    # wrap stats into a dictionary
    isotopomer_comparison_stats = {};
    isotopomer_comparison_stats = dict(list(zip(('r_measuredVsCalculated_1', 'p_measuredVsCalculated_1',
        'r_measuredVsCalculated_2', 'p_measuredVsCalculated_2',
        'r_measured1VsMeasured2', 'p_measured1VsMeasured2',
        'ssr_1,ssr_2'),
                                           (r_measuredVsCalculated_1, p_measuredVsCalculated_1,
        r_measuredVsCalculated_2, p_measuredVsCalculated_2,
        r_measured1VsMeasured2, p_measured1VsMeasured2,
        ssr_1,ssr_2))));

    ## zip, sort, unzip # does not appear to sort correctly!
    #zipped = zip(absDif_list,ssr_1_list,ssr_2_list,bestFit_list,frag_list,
    #             measured_1_list,measured_2_list,calculatedAve_1_list,calculatedAve_2_list,
    #             measuredStdev_1_list,measuredStdev_2_list);
    #zipped.sort();
    #zipped.reverse();
    #absDif_list,ssr_1_list,sst_2_list,bestFit_list,frag_list,\
    #             measured_1_list,measured_2_list,calculatedAve_1_list,calculatedAve_2_list,\
    #             measuredStdev_1_list,measuredStdev_2_list = zip(*zipped);
    # restructure into a list of dictionaries for easy parsing or data base viewing
    isotopomer_comparison = [];
    for i in range(len(absDif_list)):
        isotopomer_comparison.append({'isotopomer_absDif':absDif_list[i],
                                       'isotopomer_1_sr':ssr_1_list[i],
                                       'isotopomer_2_sr':ssr_2_list[i],
                                       'bestFit':bestFit_list[i],
                                       'frag':frag_list[i],
                                       'measured_1_ave':measured_1_list[i],
                                       'measured_2_ave':measured_2_list[i],
                                       'measured_1_stdev':measuredStdev_1_list[i],
                                       'measured_2_stdev':measuredStdev_2_list[i],
                                       'calculated_1_ave':calculatedAve_1_list[i],
                                       'calculated_2_ave':calculatedAve_2_list[i]});

    return isotopomer_comparison,isotopomer_comparison_stats;

def compare_ci_calculated(ci_1,ci_2):
    '''compare 2 calculated confidence intervals'''
    # extract into lists
    rxns_1_list = [];
    rxns_2_list = [];
    ciminv_1_list = [];
    ciminv_2_list = [];
    cimaxv_1_list = [];
    cimaxv_2_list = [];
    cirange_1_list = [];
    cirange_2_list = [];
    cirange_1_sum = 0.0;
    cirange_2_sum = 0.0;
    # ci_1:
    for k,v in ci_1.items():
        rxns_1_list.append(k);
        ciminv_1_list.append(v['minv']);
        cimaxv_1_list.append(v['maxv']);
        cirange_1_list.append(v['maxv']-v['minv']);
        cirange_1_sum += v['maxv']-v['minv'];
    ## zip, sort, unzip
    #zipped1 = zip(rxns_1_list,ciminv_1_list,cimaxv_1_list,cirange_1_list);
    #zipped1.sort();
    #rxns_1_list,ciminv_1_list,cimaxv_1_list,cirange_1_list = zip(*zipped1);
    # ci_2:
    for k,v in ci_2.items():
        rxns_2_list.append(k);
        ciminv_2_list.append(v['minv']);
        cimaxv_2_list.append(v['maxv']);
        cirange_2_list.append(v['maxv']-v['minv']);
        cirange_2_sum += v['maxv']-v['minv'];
    ## zip, sort, unzip
    #zipped2 = zip(rxns_2_list,ciminv_2_list,cimaxv_2_list,cirange_2_list);
    #zipped2.sort();
    #rxns_2_list,ciminv_2_list,cimaxv_2_list,cirange_2_list = zip(*zipped2);
    # compare by rxn_id
    cirange_absDev_list = [];
    rxns_combined_list = [];
    ciminv_1_combined_list = [];
    ciminv_2_combined_list = [];
    cimaxv_1_combined_list = [];
    cimaxv_2_combined_list = [];
    cirange_1_combined_list = [];
    cirange_2_combined_list = [];
    cirange_1_combined_sum = 0.0;
    cirange_2_combined_sum = 0.0;
    for i in range(len(rxns_1_list)):
        for j in range(len(rxns_2_list)):
            if rxns_1_list[i] == rxns_2_list[j]:
                rxns_combined_list.append(rxns_1_list[i]);
                cirange_absDev_list.append(fabs(cirange_1_list[i]-cirange_2_list[j]));
                ciminv_1_combined_list.append(ciminv_1_list[i]);
                ciminv_2_combined_list.append(ciminv_2_list[j]);
                cimaxv_1_combined_list.append(cimaxv_1_list[i]);
                cimaxv_2_combined_list.append(cimaxv_2_list[j]);
                cirange_1_combined_list.append(cirange_1_list[i]);
                cirange_2_combined_list.append(cirange_2_list[j]);
                cirange_1_combined_sum += cirange_1_list[i]
                cirange_2_combined_sum += cirange_2_list[j]
    ## zip, sort, unzip
    #zippedCombined = zip(cirange_absDev_list,rxns_combined_list,ciminv_1_combined_list,ciminv_2_combined_list,cimaxv_1_combined_list,cimaxv_2_combined_list,cirange_1_combined_list,cirange_2_combined_list);
    #zippedCombined.sort();
    #zippedCombined.reverse();
    #cirange_absDev_list,rxns_combined_list,ciminv_1_combined_list,ciminv_2_combined_list,cimaxv_1_combined_list,cimaxv_2_combined_list,cirange_1_combined_list,cirange_2_combined_list = zip(*zippedCombined);
    # restructure into a list of dictionaries for easy parsing or data base viewing
    ci_comparison = [];
    for i in range(len(cirange_absDev_list)):
        ci_comparison.append({'cirange_absDev_list':cirange_absDev_list[i],
                              'rxns_combined_list':rxns_combined_list[i],
                              'ciminv_1_combined_list':ciminv_1_combined_list[i],
                              'ciminv_2_combined_list':ciminv_2_combined_list[i],
                              'cimaxv_1_combined_list':cimaxv_1_combined_list[i],
                              'cimaxv_2_combined_list':cimaxv_2_combined_list[i],
                              'cirange_1_combined_list':cirange_1_combined_list[i],
                              'cirange_2_combined_list':cirange_2_combined_list[i]});

    return ci_comparison,cirange_1_sum,cirange_2_sum,cirange_1_combined_sum,cirange_2_combined_sum;

def plot_compare_isotopomers_calculated(isotopomer_comparison,isotopomer_comparison_stats):
    '''Plot 1: isotopomer fitting comparison
    Plot 2: isotopomer residual comparison'''
    io = base_exportData(isotopomer_comparison);
    # Plot 1 and Plot 2:
    io.write_dict2tsv('data//data.tsv');

def plot_ci_calculated(ci):
    '''plot confidence intervals from fluxomics experiment using escher'''
    data = [];
    flux1 = {};
    flux2 = {};
    for k,v in ci.items():
        flux1[k] = v['minv'];
        flux2[k] = v['maxv'];
    data.append(flux1);
    data.append(flux2);
    io = base_exportData(data);
    io.write_dict2json('visualization\\escher\\ci.json');

def export_modelWithFlux(cobra_model_xml_I,ci_list_I,cobra_model_xml_O):
    '''update model lower_bound/upper_bound with calculated flux confidence intervals'''

    cobra_model = create_cobra_model_from_sbml_file(cobra_model_xml_I);

    rxns_add = [];
    rxns_omitted = [];
    rxns_break = [];

    system_boundaries = [x.id for x in cobra_model.reactions if x.boundary == 'system_boundary'];
    objectives = [x.id for x in cobra_model.reactions if x.objective_coefficient == 1];

    for i,ci_I in enumerate(ci_list_I):
        print('add flux from ci ' + str(i));
        for rxn in cobra_model.reactions:
            if rxn.id in list(ci_I.keys()) and not(rxn.id in system_boundaries)\
                and not(rxn.id in objectives):
                cobra_model_copy = cobra_model.copy();
                # check for reactions that break the model:
                if ci_I[rxn.id]['minv'] > 0:
                    cobra_model_copy.reactions.get_by_id(rxn.id).lower_bound = ci_I[rxn.id]['minv'];
                if ci_I[rxn.id]['maxv'] > 0 and ci_I[rxn.id]['maxv'] > ci_I[rxn.id]['minv']:
                    cobra_model_copy.reactions.get_by_id(rxn.id).upper_bound = ci_I[rxn.id]['maxv'];
                cobra_model_copy.optimize(solver='gurobi');
                if not cobra_model_copy.solution.f:
                    print(rxn.id + ' broke the model!')
                    rxns_break.append(rxn.id);
                else: 
                    if ci_I[rxn.id]['minv'] > 0:
                        cobra_model.reactions.get_by_id(rxn.id).lower_bound = ci_I[rxn.id]['minv'];
                    if ci_I[rxn.id]['maxv'] > 0 and ci_I[rxn.id]['maxv'] > ci_I[rxn.id]['minv']:
                        cobra_model.reactions.get_by_id(rxn.id).upper_bound = ci_I[rxn.id]['maxv'];
                    rxns_add.append(rxn.id);
            else:
                rxns_omitted.append(rxn.id);

    write_cobra_model_to_sbml_file(cobra_model,cobra_model_xml_O)

