'''quantitative metabolomics analysis class'''

from analysis.analysis_base import *
from stage01_quantification_query import *
from stage01_quantification_io import *
from resources.matplot import matplot

from time import mktime,strptime
from datetime import datetime

class stage01_quantification_execute():
    '''class for quantitative metabolomics analysis'''
    def __init__(self,session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.stage01_quantification_query = stage01_quantification_query(self.session);
        self.calculate = base_calculate();
        self.matplot = matplot();
        # variables:
        self.ratios = {'accoa_ratio':{'component_group_name':["accoa","coa"],'name':'Ac(CoA) Ratio','description':'accoa/(coa+accoa)'},
                    'ec':{'component_group_name':["adp","amp","atp"],'name':'Adenylate charge','description':'(0.5*adp+atp)/(adp+amp+atp)'},
                    'p_ratio01':{'component_group_name':["adp","atp"],'name':'Adenylate ratio01','description':'atp/adp'},
                    'p_ratio02':{'component_group_name':["amp","atp"],'name':'Adenylate ratio02','description':'atp/amp'},
                    'redox_ratio':{'component_group_name':["gthox","gthrd"],'name':'Redox ratio','description':'gthrd/(gthox+gthrd)'},
                    'gth_ratio01':{'component_group_name':["gthox","gthrd"],'name':'Glutathione ratio01','description':'gthrd/gthox'},
                    'mar_ak':{'component_group_name':["adp","amp","atp"],'name':'Mass action ratio of the adenylate kinase reaction','description':'(amp*atp)/(adp*adp)'},
                    'mar_fum':{'component_group_name':["fum","mal-L"],'name':'Mass action of the fumarase reaction','description':'fum/mal-L'},
                    'mar_pgi':{'component_group_name':["f6p","g6p"],'name':'Mass action ratio of the PGI reaction','description':'f6p/g6p'},
                    'mar_pgm_eno':{'component_group_name':["Pool_2pg_3pg","pep"],'name':'Mass action ratio of the PGM and ENO reactions','description':'pep/Pool_2pg_3pg'},
                    #'n2_ratio01':{'component_group_name':["gln-L","glu-L"],'name':'Nitrogen ratio01','description':'gln-L/(gln-L+glu-L)'},
                    'n2_ratio01':{'component_group_name':["gln-L","glu-L"],'name':'Nitrogen ratio01','description':'gln-L/glu-L'},
                    #'n2_ratio02':{'component_group_name':["akg","glu-L"],'name':'Nitrogen ratio02','description':'glu-L/(akg+glu-L)'},
                    'n2_ratio02':{'component_group_name':["akg","glu-L"],'name':'Nitrogen ratio02','description':'glu-L/akg'},
                    'n2_ratio03':{'component_group_name':["akg","gln-L"],'name':'Nitrogen ratio03','description':'gln-L/akg'},
                    'nc':{'component_group_name':["akg","gln-L","glu-L"],'name':'Nitrogen charge','description':'(0.5*glu-L+gln-L)/(akg+glu-L+gln-L)'},
                    'nad_ratio':{'component_group_name':["nad","nadh"],'name':'NAD(H) ratio','description':'nadh/(nad+nadh)'},
                    'nadp_ratio':{'component_group_name':["nadp","nadph"],'name':'NADP(H) ratio','description':'nadph/(nadp+nadph)'},
                    'nad(p)_ratio':{'component_group_name':["nadp","nadph","nad","nadh"],'name':'NAD(P)(H) ratio','description':'(nadph+nadh)/(nadp+nadph+nad+nadh)'}};
    # analyses:
    def execute_LLOQAndULOQ(self,experiment_id_I):
        '''check the lloq and uloq from the calibrators
        against the calculated concentration
        NOTE: a table is used to store the view'''

        print 'execute_LLOQAndULOQ...'
        # query data for the view
        check = [];
        check = self.stage01_quantification_query.get_LLOQAndULOQ(experiment_id_I);
        # create and populate the view
        for n in range(len(check)):
            if check[n]:
                row = data_stage01_quantification_LLOQAndULOQ(experiment_id_I,
                                                      check[n]['sample_name'],
                                                      check[n]['component_group_name'],
                                                      check[n]['component_name'],
                                                      check[n]['calculated_concentration'],
                                                      check[n]['conc_units'],
                                                      check[n]['correlation'],
                                                      check[n]['lloq'],
                                                      check[n]['uloq'],
                                                      check[n]['points'],
                                                      check[n]['used']);
                self.session.add(row);
        self.session.commit();
    def execute_checkLLOQAndULOQ(self,experiment_id_I):
        '''check the lloq and uloq from the calibrators
        against the calculated concentration
        NOTE: a table is used to store the view'''
        
        print 'execute_checkLLOQAndULOQ...'
        # query data for the view
        check = [];
        check = self.stage01_quantification_query.get_checkLLOQAndULOQ(experiment_id_I);
        # create and populate the view
        for n in range(len(check)):
            if check[n]:
                row = data_stage01_quantification_checkLLOQAndULOQ(experiment_id_I,
                                                      check[n]['sample_name'],
                                                      check[n]['component_group_name'],
                                                      check[n]['component_name'],
                                                      check[n]['calculated_concentration'],
                                                      check[n]['conc_units'],
                                                      check[n]['correlation'],
                                                      check[n]['lloq'],
                                                      check[n]['uloq'],
                                                      check[n]['points'],
                                                      check[n]['used']);
                self.session.add(row);
        self.session.commit();
    def execute_checkISMatch(self,experiment_id_I):
        '''check that the internal standard used in the data file
        matches that of the calibration method'''

        '''SELECT 
          experiment.id,
          data_stage01_quantification_mqresultstable.sample_name, 
          data_stage01_quantification_mqresultstable.component_name, 
          data_stage01_quantification_mqresultstable.is_name,
          quantitation_method.is_name
        FROM 
          public.data_stage01_quantification_mqresultstable, 
          public.experiment, 
          public.quantitation_method
        WHERE 
          experiment.id LIKE 'ibop_rbc02' AND 
          experiment.sample_name LIKE data_stage01_quantification_mqresultstable.sample_name AND 
          (data_stage01_quantification_mqresultstable.sample_type LIKE 'Unknown' OR
          data_stage01_quantification_mqresultstable.sample_type LIKE 'Quality Control') AND 
          experiment.quantitation_method_id LIKE quantitation_method.id AND 
          quantitation_method.component_name LIKE data_stage01_quantification_mqresultstable.component_name AND 
          data_stage01_quantification_mqresultstable.used_ AND
          NOT data_stage01_quantification_mqresultstable.is_ AND
          data_stage01_quantification_mqresultstable.is_name NOT LIKE quantitation_method.is_name;'''

        print 'execute_checkISMatch...'
        # query data for the view
        check = [];
        check = self.stage01_quantification_query.get_checkISMatch(experiment_id_I);
        # create and populate the view
        for n in range(len(check)):
            if check[n]:
                row = data_stage01_quantification_checkISMatch(experiment_id_I,
                                                      check[n]['sample_name'],
                                                      check[n]['component_name'],
                                                      check[n]['IS_name_samples'],
                                                      check[n]['IS_name_calibrators']);
                self.session.add(row);
        self.session.commit();
    def execute_analyzeQCs(self,experiment_id_I):
        '''calculate the average and coefficient of variation for QCs
        NOTE: analytical replicates are those samples with the same 
        sample_id (but different sample_name)'''
        # Input:
        #   experiment_id
        # Output:
        #   sample_name
        #   component_group_name
        #   component_name
        #   n_replicates
        #   conc_average
        #   conc_CV
        #   conc_units
        
        print 'execute_analyzeQCs...'
        # get sample name abbreviations
        sample_name_abbreviations = [];
        sample_types = ['QC'];
        for st in sample_types:
            sample_name_abbreviations_tmp = [];
            sample_name_abbreviations_tmp = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndSampleType(experiment_id_I,st);
            sample_name_abbreviations.extend(sample_name_abbreviations_tmp);
        # create database table
        for sna in sample_name_abbreviations:
            # get dilutions
            sample_dilutions = [];
            sample_dilutions = self.stage01_quantification_query.get_sampleDilution_experimentIDAndSampleNameAbbreviation(experiment_id_I,sna);
            # get component names
            component_names = [];
            component_names = self.stage01_quantification_query.get_componentsNames_experimentIDAndSampleNameAbbreviation(experiment_id_I,sna);
            for cn in component_names:
                component_group_name = self.stage01_quantification_query.get_componentGroupName_experimentIDAndComponentName(experiment_id_I,cn);
                for sd in sample_dilutions:
                    # get sample names
                    sample_names = [];
                    sample_names = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDilution(experiment_id_I,sna,sd);
                    if(sample_names<2): continue;
                    concs = [];
                    conc_units = None;
                    for sn in sample_names:
                        # concentrations and units
                        conc = None;
                        conc_unit = None;
                        conc, conc_unit = self.stage01_quantification_query.get_concAndConcUnits_sampleNameAndComponentName(sn,cn);
                        if not(conc): continue
                        if (conc_unit): conc_units = conc_unit;
                        concs.append(conc);
                    n_replicates = len(concs);
                    # calculate average and CV of concentrations
                    if (not(concs) or n_replicates<2): continue
                    #conc_average, conc_CV = self.calculate.calculate_ave_CV_R(concs);
                    conc_average = numpy.mean(numpy.array(concs));
                    conc_CV = numpy.std(numpy.array(concs))/conc_average*100;
                    # add data to the session
                    row = data_stage01_quantification_QCs(experiment_id_I,sna,sd,component_group_name,cn,n_replicates,
                                                                conc_average, conc_CV, conc_units);
                    self.session.add(row);
        self.session.commit();
    def execute_checkCV_QCs(self,experiment_id_I):
        print 'execute_checkCV_QCs...'
        return;
    def execute_analyzeDilutions(self,experiment_id_I):
        '''calculate the average and coefficient of variation for analytical
        replicates
        NOTE: analytical replicates are those samples with the same 
        sample_id (but different sample_name)'''
        # Input:
        #   experiment_id
        # Output:
        #   sample_name
        #   component_group_name
        #   component_name
        #   n_replicates
        #   conc_average
        #   conc_CV
        #   conc_units
        
        print 'execute_analyzeDilutions...'
        # get sample names
        sample_ids = [];
        sample_types = ['Unknown','QC'];
        for st in sample_types:
            sample_ids_tmp = [];
            sample_ids_tmp = self.stage01_quantification_query.get_sampleIDs_experimentIDAndSampleType(experiment_id_I,st);
            sample_ids.extend(sample_ids_tmp);
        # create database table
        for si in sample_ids:
            print 'analyzing dilutions for sample id ' + si;
            # get sample names
            sample_names = [];
            sample_names = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleID(experiment_id_I,si);
            if(sample_names<2): continue;
            # get component names
            component_names = [];
            component_names = self.stage01_quantification_query.get_componentsNames_experimentIDAndSampleID(experiment_id_I,si);
            for cn in component_names:
                print 'analyzing dilutions for component_name ' + cn;
                concs = [];
                conc_units = None;
                component_group_name = self.stage01_quantification_query.get_componentGroupName_experimentIDAndComponentName(experiment_id_I,cn);
                for sn in sample_names:
                    print 'analyzing dilutions for sample_name ' + sn;
                    # concentrations and units
                    conc = None;
                    conc_unit = None;
                    conc, conc_unit = self.stage01_quantification_query.get_concAndConcUnits_sampleNameAndComponentName(sn,cn);
                    if not(conc): continue
                    if (conc_unit): conc_units = conc_unit;
                    concs.append(conc);
                n_replicates = len(concs);
                # calculate average and CV of concentrations
                if (not(concs) or n_replicates<2): continue
                #conc_average, conc_CV = self.calculate.calculate_ave_CV_R(concs);
                conc_average = numpy.mean(numpy.array(concs));
                conc_CV = numpy.std(numpy.array(concs))/conc_average*100;
                # add data to the session
                row = data_stage01_quantification_dilutions(experiment_id_I, si,component_group_name,cn,n_replicates,
                                                            conc_average, conc_CV, conc_units);
                self.session.add(row);
        self.session.commit();
    def execute_checkCV_dilutions(self,experiment_id_I):
        '''check the CV of the dilutions table
        NOTE: a table is used to store the view'''
        
        print 'execute_checkCV_dilutions...'
        # query data for the view
        check = [];
        check = self.stage01_quantification_query.get_checkCV_dilutions(experiment_id_I);
        # create and populate the view
        for n in range(len(check)):
            if check[n]:
                row = data_stage01_quantification_checkCV_dilutions(check[n]['experiment_id'],
                                                      check[n]['sample_id'],
                                                      check[n]['component_group_name'],
                                                      check[n]['component_name'],
                                                      check[n]['n_replicates'],
                                                      check[n]['calculated_concentration_average'],
                                                      check[n]['calculated_concentration_cv'],
                                                      check[n]['calculated_concentration_units']);
                self.session.add(row);
        self.session.commit();
    def execute_removeDuplicateDilutions(self,experiment_id_I,component_names_dil_I = []):
        '''remove duplicate dilutions from data_stage01_quantification_normalized
        NOTE: rows are not removed, but the used value is changed to false
        NOTE: priority is given to the 1x dilution (i.e. 10x dilutions are removed
              if a 1x and 10x are both used'''
        # Input:
        #   experiment_id_I = experiment
        #   component_names_dil_I = component names for which the dilution will be prioritized
        
        print 'execute_removeDuplicateDilutions...'
        # get sample names
        sample_ids = [];
        sample_ids = self.stage01_quantification_query.get_sampleIDs_experimentID_dataStage01Normalized(experiment_id_I);
        for si in sample_ids:
            # get component names
            component_names = [];
            component_names = self.stage01_quantification_query.get_componentsNames_experimentIDAndSampleID_dataStage01Normalized(experiment_id_I,si);
            for cn in component_names:
                # get dilutions
                sample_dilutions = [];
                sample_dilutions = self.stage01_quantification_query.get_sampleDilutions_experimentIDAndSampleIDAndComponentName_dataStage01Normalized(experiment_id_I,si,cn);
                if len(sample_dilutions)<2: continue;
                # find the minimum and maximum dilution
                min_sample_dilution = min(sample_dilutions);
                max_sample_dilution = max(sample_dilutions);
                for sd in sample_dilutions:
                    # prioritize undiluted samples if not in the dilution list
                    # i.e. diluted samples used_ are set to FALSE
                    if not(cn in component_names_dil_I) and not(sd == min_sample_dilution):
                        # get the sample name
                        sample_name = self.stage01_quantification_query.get_sampleName_experimentIDAndSampleIDAndSampleDilution_dataStage01Normalized(experiment_id_I,si,sd);
                        try:
                            data_update = self.session.query(data_stage01_quantification_normalized).filter(
                                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                                    data_stage01_quantification_normalized.sample_name.like(sample_name),
                                    data_stage01_quantification_normalized.component_name.like(cn)).update(
                                    {'used_': False},synchronize_session=False);
                        except SQLAlchemyError as e:
                            print(e);
                    # prioritize diluted samples if in the dilution list
                    # i.e. undiluted samples used_ are set to FALSE
                    if (cn in component_names_dil_I) and not(sd == max_sample_dilution):
                        # get the sample name
                        sample_name = self.stage01_quantification_query.get_sampleName_experimentIDAndSampleIDAndSampleDilution_dataStage01Normalized(experiment_id_I,si,sd);
                        try:
                            data_update = self.session.query(data_stage01_quantification_normalized).filter(
                                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                                    data_stage01_quantification_normalized.sample_name.like(sample_name),
                                    data_stage01_quantification_normalized.component_name.like(cn)).update(
                                    {'used_': False},synchronize_session=False);
                        except SQLAlchemyError as e:
                            print(e);
        self.session.commit();
    def execute_removeDuplicateComponents(self,experiment_id_I):
        '''remove duplicate components from data_stage01_quantification_normalized
        NOTE: rows are not removed, but the used value is changed to false
        NOTE: priority is given to the primary transition'''
        return
    def execute_normalizeSamples2Biomass(self,experiment_id_I,biological_material_I=None,conversion_name_I=None,sample_names_I=[],component_names_I=[],use_height_I=False):
        '''Normalize calculated concentrations to measured biomass'''
        # Input:
        #   experiment_id_I
        #   biological_material_I =  biological material (if None, no normalization is done)
        #   conversion_name_I = biomass conversion name (if None, no normalization is done)
        #   use_height_I = if True, use the ion count for peak height instead of the calculated_concentration or height/area ratio
        # Output:
        #   sample_name
        #   sample_id
        #   component_group_name
        #   component_name
        #   calculated_concentration
        #   calculated_concentration_units
        #   used_
        
        print 'execute_normalizeSamples2Biomass...'
        # get sample names
        if sample_names_I:
            sample_names = sample_names_I;
        else:
            sample_names = [];
            sample_types = ['Unknown'];
            for st in sample_types:
                sample_names_tmp = [];
                sample_names_tmp = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleType(experiment_id_I,st);
                sample_names.extend(sample_names_tmp);
        # create database table
        for sn in sample_names:
            print 'normalizing samples2Biomass for sample_name ' + sn;
            # get component names
            if component_names_I:
                component_names = component_names_I;
            else:
                component_names = [];
                component_names = self.stage01_quantification_query.get_componentsNames_experimentIDAndSampleName(experiment_id_I,sn);
            # get sample id
            sample_id = self.stage01_quantification_query.get_sampleID_experimentIDAndSampleName(experiment_id_I,sn);
            if (biological_material_I and conversion_name_I):
                # get physiological parameters
                cvs = None;
                cvs_units = None;
                od600 = None;
                dil = None;
                dil_units = None;
                conversion = None;
                conversion_units = None;
                cvs, cvs_units, od600, dil,dil_units = self.stage01_quantification_query.get_CVSAndCVSUnitsAndODAndDilAndDilUnits_sampleName(sn);
                conversion, conversion_units = self.stage01_quantification_query.get_conversionAndConversionUnits_biologicalMaterialAndConversionName(biological_material_I,conversion_name_I);
                if not(cvs and cvs_units and od600 and dil and dil_units):
                    print('cvs, cvs_units, or od600 are missing from physiological parameters');
                    print('or dil and dil_units are missing from sample descripton');
                    exit(-1);
                elif not(conversion and conversion_units):
                    print('biological_material or conversion name is incorrect');
                    exit(-1);  
                else:
                    #calculate the cell volume or biomass depending on the conversion units
                    #cell_volume, cell_volume_units = self.calculate.calculate_cellVolume_CVSAndCVSUnitsAndODAndConversionAndConversionUnits(cvs,cvs_units,od600,conversion,conversion_units);
                    cell_volume, cell_volume_units = self.calculate.calculate_biomass_CVSAndCVSUnitsAndODAndConversionAndConversionUnits(cvs,cvs_units,od600,conversion,conversion_units);
                for cn in component_names:
                    print 'normalizing samples2Biomass for component_name ' + cn;
                    # get component group name
                    #component_group_name = self.stage01_quantification_query.get_componentGroupName_experimentIDAndComponentName(experiment_id_I,cn);
                    component_group_name = self.stage01_quantification_query.get_msGroup_componentName_MSComponents(cn);
                    # get the calculated concentration
                    calc_conc = None;
                    calc_conc_units = None;
                    if use_height_I: 
                        calc_conc, calc_conc_units = self.stage01_quantification_query.get_peakHeight_sampleNameAndComponentName(sn,cn);
                    else:
                        calc_conc, calc_conc_units = self.stage01_quantification_query.get_concAndConcUnits_sampleNameAndComponentName(sn,cn);
                    # calculate the normalized concentration
                    norm_conc = None;
                    norm_conc_units = None;
                    if calc_conc: 
                        norm_conc, norm_conc_units = self.calculate.calculate_conc_concAndConcUnitsAndDilAndDilUnitsAndConversionAndConversionUnits(calc_conc,calc_conc_units,dil,dil_units,cell_volume, cell_volume_units);
                    # update data_stage01_quantification_normalized
                    if norm_conc:
                        row = data_stage01_quantification_normalized(experiment_id_I, sn,sample_id,component_group_name,cn,norm_conc,norm_conc_units,True);
                        self.session.add(row);
            else:
                for cn in component_names:
                    print 'normalizing samples2Biomass for component_name ' + cn;
                    # get component group name
                    #component_group_name = self.stage01_quantification_query.get_componentGroupName_experimentIDAndComponentName(experiment_id_I,cn);
                    component_group_name = self.stage01_quantification_query.get_msGroup_componentName_MSComponents(cn);
                    # get the calculated concentration
                    calc_conc = None;
                    calc_conc_units = None;
                    if use_height_I: 
                        calc_conc, calc_conc_units = self.stage01_quantification_query.get_peakHeight_sampleNameAndComponentName(sn,cn);
                    else:
                        calc_conc, calc_conc_units = self.stage01_quantification_query.get_concAndConcUnits_sampleNameAndComponentName(sn,cn);
                    row = data_stage01_quantification_normalized(experiment_id_I, sn,sample_id,component_group_name,cn,calc_conc,calc_conc_units,True);
                    self.session.add(row);
            self.session.commit();
    def execute_analyzeReplicates(self,experiment_id_I,sample_name_abbreviations_I=[],sample_names_I=[],component_names_I=[]):
        '''calculate the replicates by subtracting out the filtrate
        NOTE: data_stage01_quantification_normalized must be populated'''
        # Input:
        #   experiment_id
        # Output:
        #   sample_name_short
        #   component_group_name
        #   component_name
        #   concentration
        #   concentration units
        
        print 'execute_analyzeReplicates...'
        # get sample_name_abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentID_dataStage01Normalized(experiment_id_I);
        # create database table
        for sna in sample_name_abbreviations:
            print 'analyzing replicates for sample_name_abbreviation ' + sna;
            # get component names
            if component_names_I:
                component_names = component_names_I
            else:
                component_names = [];
                component_names = self.stage01_quantification_query.get_componentsNames_experimentIDAndSampleNameAbbreviation_dataStage01Normalized(experiment_id_I,sna);
            for cn in component_names:
                print 'analyzing replicates for component_name ' + cn;
                component_group_name = self.stage01_quantification_query.get_componentGroupName_experimentIDAndComponentName_dataStage01Normalized(experiment_id_I,cn);
                # get time points
                time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01Normalized(experiment_id_I,sna);
                for tp in time_points:
                    print 'analyzing replicates for time_point ' + tp;
                    # get filtrate sample names
                    sample_names = [];
                    sample_description = 'Filtrate';
                    sample_names = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDescriptionAndComponentNameAndTimePoint_dataStage01Normalized(experiment_id_I,sna,sample_description,cn,tp);
                    if sample_names_I: # screen out sample names that are not in the input
                        sample_names = [x for x in sample_names if x in sample_names_I];
                    concs = [];
                    conc_units = None;
                    for sn in sample_names:
                        # concentrations and units
                        conc = None;
                        conc_unit = None;
                        conc, conc_unit = self.stage01_quantification_query.get_concAndConcUnits_sampleNameAndComponentName_dataStage01Normalized(sn,cn);
                        if not(conc): continue
                        if (conc_unit): conc_units = conc_unit;
                        concs.append(conc);
                    n_replicates = len(concs);
                    conc_average_filtrate = 0.0;
                    conc_var_filtrate = 0.0;
                    # calculate average and CV of concentrations
                    if (not(concs)): conc_average_filtrate = 0;
                    elif n_replicates<2: conc_average_filtrate = concs[0];
                    else: 
                        #conc_average_filtrate, conc_var_filtrate = self.calculate.calculate_ave_var_R(concs);
                        conc_average_filtrate = numpy.mean(numpy.array(concs));
                        conc_var_filtrate = numpy.var(numpy.array(concs));
                    # get filtrate sample names
                    sample_names = [];
                    sample_description = 'Broth';
                    sample_names = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDescriptionAndComponentNameAndTimePoint_dataStage01Normalized(experiment_id_I,sna,sample_description,cn,tp);
                    if sample_names_I: # screen out sample names that are not in the input
                        sample_names = [x for x in sample_names if x in sample_names_I];
                    for sn in sample_names:
                        print 'analyzing replicates for sample_name ' + sn;
                        # query concentrations and units
                        conc = None;
                        conc_unit = None;
                        conc, conc_unit = self.stage01_quantification_query.get_concAndConcUnits_sampleNameAndComponentName_dataStage01Normalized(sn,cn);
                        if (not(conc) or conc==0): continue # record all replicate broth samples whether they were measured or not 
                                                             # needed for MI2 later on
                        if (conc_unit): conc_units = conc_unit;
                        # subract out filtrate average from each broth
                        conc_broth = 0.0;
                        if conc:
                            conc_broth = conc-conc_average_filtrate;
                            if (conc_broth < 0 ): conc_broth = None;
                        else: conc_broth = None;
                        # get sample name short
                        sample_name_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleName_dataStage01Normalized(experiment_id_I, sn);
                        # add data to the session 
                        row = data_stage01_quantification_replicates(experiment_id_I, sample_name_short, tp, component_group_name, cn,
                                                                conc_broth, conc_units, True);
                        self.session.add(row);
            self.session.commit();
    def execute_analyzeAverages(self,experiment_id_I,sample_name_abbreviations_I=[],sample_names_I=[],component_names_I=[]):
        '''calculate the averages
        NOTE: data_stage01_quantification_normalized must be populated'''
        # Input:
        #   experiment_id
        # Output:
        #   sample_name_abbreviation
        #   component_group_name
        #   component_name
        #   concentration average
        #   concentration CV
        #   concentration units
        #   % extracellular
        
        print 'execute_analyzeAverages...'
        # get sample_name_abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentID_dataStage01Normalized(experiment_id_I);
        for sna in sample_name_abbreviations:
            print 'analyzing averages for sample_name_abbreviation ' + sna;
            # get component names
            if component_names_I:
                component_names = component_names_I
            else:
                component_names = [];
                component_names = self.stage01_quantification_query.get_componentsNames_experimentIDAndSampleNameAbbreviation_dataStage01Normalized(experiment_id_I,sna);
            for cn in component_names:
                print 'analyzing averages for component_name ' + cn;
                component_group_name = self.stage01_quantification_query.get_componentGroupName_experimentIDAndComponentName_dataStage01Normalized(experiment_id_I,cn);
                # get time points
                time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01Normalized(experiment_id_I,sna);
                for tp in time_points:
                    print 'analyzing averages for time_point ' + tp;
                    # get filtrate sample names
                    sample_names = [];
                    sample_description = 'Filtrate';
                    sample_names = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDescriptionAndComponentNameAndTimePoint_dataStage01Normalized(experiment_id_I,sna,sample_description,cn,tp);
                    if sample_names_I: # screen out sample names that are not in the input
                        sample_names = [x for x in sample_names if x in sample_names_I];
                    concs = [];
                    conc_units = None;
                    for sn in sample_names:
                        # concentrations and units
                        conc = None;
                        conc_unit = None;
                        conc, conc_unit = self.stage01_quantification_query.get_concAndConcUnits_sampleNameAndComponentName_dataStage01Normalized(sn,cn);
                        if (not(conc) or conc==0): continue
                        if (conc_unit): conc_units = conc_unit;
                        concs.append(conc);
                    n_replicates_filtrate = len(concs);
                    conc_average_filtrate = 0.0;
                    conc_var_filtrate = 0.0;
                    conc_cv_filtrate = 0.0;
                    # calculate average and CV of concentrations
                    if (not(concs)): 
                        conc_average_filtrate = 0;
                        conc_var_filtrate = 0;
                    elif n_replicates_filtrate<2: 
                        conc_average_filtrate = concs[0];
                        conc_var_filtrate = 0;
                    else: 
                        #conc_average_filtrate, conc_var_filtrate = self.calculate.calculate_ave_var_R(concs);
                        conc_average_filtrate = numpy.mean(numpy.array(concs));
                        conc_var_filtrate = numpy.var(numpy.array(concs));
                        if (conc_average_filtrate <= 0): conc_cv_filtrate = 0;
                        else: conc_cv_filtrate = sqrt(conc_var_filtrate)/conc_average_filtrate*100; 
                    # get broth sample names
                    sample_names = [];
                    sample_description = 'Broth';
                    sample_names = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDescriptionAndComponentNameAndTimePoint_dataStage01Normalized(experiment_id_I,sna,sample_description,cn,tp);
                    if sample_names_I: # screen out sample names that are not in the input
                        sample_names = [x for x in sample_names if x in sample_names_I];
                    concs = [];
                    conc_units = None;
                    for sn in sample_names:
                        print 'analyzing averages for sample_name ' + sn;
                        # query concentrations and units
                        conc = None;
                        conc_unit = None;
                        conc, conc_unit = self.stage01_quantification_query.get_concAndConcUnits_sampleNameAndComponentName_dataStage01Normalized(sn,cn);
                        if (not(conc) or conc==0): continue
                        if (conc_unit): conc_units = conc_unit;
                        concs.append(conc);
                    n_replicates = len(concs);
                    conc_average_broth = 0.0;
                    conc_var_broth = 0.0;
                    conc_cv_broth = 0.0;
                    # calculate average and CV of concentrations
                    if (not(concs)): 
                        continue
                    elif n_replicates<2: 
                        continue
                    else: 
                        #conc_average_broth, conc_var_broth = self.calculate.calculate_ave_var_R(concs);
                        conc_average_broth = numpy.mean(numpy.array(concs));
                        conc_var_broth = numpy.var(numpy.array(concs));
                        if (conc_average_broth <= 0): conc_cv_broth = 0;
                        else: conc_cv_broth = sqrt(conc_var_broth)/conc_average_broth*100; 
                    # calculate average and CV
                    conc_average = 0.0;
                    conc_var = 0.0;
                    conc_cv = 0.0;
                    conc_average = conc_average_broth-conc_average_filtrate;
                    if (conc_average < 0): conc_average = 0;
                    conc_var = conc_var_broth + conc_var_filtrate;
                    if (conc_average <= 0): conc_cv = 0;
                    else: conc_cv = sqrt(conc_var)/conc_average*100;
                    # calculate the % extracellular
                    extracellular_percent = conc_average_filtrate/conc_average_broth*100;
                    # add data to the session
                    row = data_stage01_quantification_averages(experiment_id_I, sna, tp, component_group_name, cn,
                                                   n_replicates, conc_average_broth, conc_cv_broth,
                                                   n_replicates_filtrate, conc_average_filtrate, conc_cv_filtrate,
                                                   n_replicates, conc_average, conc_cv, conc_units, extracellular_percent, True);   
                    self.session.add(row);
        self.session.commit(); 
    def execute_checkCVAndExtracelluar_averages(self,experiment_id_I):
        '''check the CV and % Extracellular of the averages table
        NOTE: a table is used to store the view'''
        
        print 'execute_checkCVAndExtracelluar_averages...'
        # query data for the view
        check = [];
        check = self.stage01_quantification_query.get_checkCVAndExtracellular_averages(experiment_id_I);
        # create and populate the view
        for n in range(len(check)):
            if check[n]:
                row = data_stage01_quantification_checkCVAndExtracellular_averages(check[n]['experiment_id'],
                                                      check[n]['sample_name_abbreviation'],
                                                      check[n]['component_group_name'],
                                                      check[n]['time_point'],
                                                      check[n]['component_name'],
                                                      check[n]['n_replicates_broth'],
                                                      check[n]['calculated_concentration_broth_average'],
                                                      check[n]['calculated_concentration_broth_cv'],
                                                      check[n]['n_replicates_filtrate'],
                                                      check[n]['calculated_concentration_filtrate_average'],
                                                      check[n]['calculated_concentration_filtrate_cv'],
                                                      check[n]['n_replicates'],
                                                      check[n]['calculated_concentration_average'],
                                                      check[n]['calculated_concentration_cv'],
                                                      check[n]['calculated_concentration_units'],
                                                      check[n]['extracellular_percent'],
                                                      check[n]['used']);
                self.session.add(row);
        self.session.commit();
    def execute_calculateMissingValues_replicates(self,experiment_id_I,sample_name_abbreviations_I=[]):
        '''calculate estimates for missing replicates values using AmeliaII from R'''

        from resources.r import r_calculate
        
        r_calc = r_calculate();

        print 'execute_calculateMissingValues_replicates...'
        # get sample name abbreviations
        if sample_name_abbreviations_I:
            sample_names_abbreviation = sample_name_abbreviations_I;
        else:
            sample_names_abbreviation = [];
            sample_names_abbreviation = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentID_dataStage01Replicates(experiment_id_I);
        # for each sample name abbreviation
        for sna in sample_names_abbreviation:
            print 'calculating missing values for sample_name_abbreviation ' + sna;
            # get time points
            time_points = [];
            time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01Replicates(experiment_id_I,sna);
            for tp in time_points:
                print 'calculating missing values for time_point ' + tp;
                # get sample names short
                sample_names_short = []
                sample_names_short = self.stage01_quantification_query.get_SampleNameShort_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage01Replicates(experiment_id_I,sna,tp);
                data = [];
                for sns in sample_names_short:
                    print 'calculating missing values for sample_name_abbreviation ' + sns;
                    # get sample names short, component names, and concentrations
                    data_tmp = [];
                    data_tmp = self.stage01_quantification_query.get_data_experimentIDAndSampleNameShortAndTimePoint_dataStage01Replicates(experiment_id_I,sns,tp);
                    data.extend(data_tmp);
                # compute missing values
                dataListUpdated = [];
                sns_NA = [];
                cn_NA = [];
                cc_NA = [];
                sns_NA, cn_NA, cc_NA = r_calc.calculate_missingValues(data);
                for n in range(len(sns_NA)):
                    component_group_name = None;
                    calculated_concentration_units = None;
                    component_group_name, calculated_concentration_units = self.stage01_quantification_query.get_componentGroupNameAndConcUnits_experimentIDAndComponentNameAndSampleNameAbbreviationAndTimePoint_dataStage01Replicates(experiment_id_I,cn_NA[n],sna,tp);
                    # update data_stage01_quantification_replicatesMI
                    row = data_stage01_quantification_replicatesMI(experiment_id_I,sns_NA[n],tp,component_group_name,cn_NA[n],cc_NA[n],calculated_concentration_units,True);
                    self.session.add(row);
            self.session.commit(); 
    def execute_calculateMissingComponents_replicates(self,experiment_id_I,biological_material_I=None,conversion_name_I=None,sample_names_short_I=[]):
        '''calculate estimates for samples in which a component was not found for any of the replicates'''
        
        io = stage01_quantification_io();

        print 'execute_calculateMissingComponents_replicates...'
        # get all sample names short
        if sample_names_short_I:
            sample_names_short = sample_names_short_I;
        else:
            sample_names_short = [];
            sample_names_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleDescription_dataStage01Normalized(experiment_id_I,'Broth');
        # get component names
        component_names = []
        component_names = self.stage01_quantification_query.get_componentNames_experimentID_dataStage01ReplicatesMI(experiment_id_I);
        # get time points
        time_points = [];
        time_points = self.stage01_quantification_query.get_timePoint_experimentID_dataStage01ReplicatesMI(experiment_id_I);
        for tp in time_points:
            print 'calculating missing components for time_point ' + tp;
            for cn in component_names:
                print 'calculating missing components for component_name ' + cn;
                component_group_name = None;
                calculated_concentration_units = None;
                component_group_name, calculated_concentration_units = self.stage01_quantification_query.get_componentGroupNameAndConcUnits_experimentIDAndComponentName_dataStage01Replicates(experiment_id_I,cn);
                for sns in sample_names_short:
                    print 'calculating missing components for sample_name_short ' + sns;
                    # get calculated concentration
                    calculated_concentration = None;
                    calculated_concentration = self.stage01_quantification_query.get_calculatedConcentration_experimentIDAndSampleNameShortAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id_I,sns,tp,cn);
                    if calculated_concentration: continue
                    # get the lloq
                    lloq = None;
                    conc_units = None;
                    lloq, conc_units = self.stage01_quantification_query.get_lloq_ExperimentIDAndComponentName_dataStage01LLOQAndULOQ(experiment_id_I,cn);
                    if not lloq: continue
                    # normalize the lloq
                    if (biological_material_I and conversion_name_I):
                        # get physiological parameters
                        cvs = None;
                        cvs_units = None;
                        od600 = None;
                        dil = None;
                        dil_units = None;
                        conversion = None;
                        conversion_units = None;
                        cvs, cvs_units, od600, dil,dil_units = self.stage01_quantification_query.get_CVSAndCVSUnitsAndODAndDilAndDilUnits_sampleNameShort(experiment_id_I,sns);
                        conversion, conversion_units = self.stage01_quantification_query.get_conversionAndConversionUnits_biologicalMaterialAndConversionName(biological_material_I,conversion_name_I);
                        if not(cvs and cvs_units and od600 and dil and dil_units):
                            print('cvs, cvs_units, or od600 are missing from physiological parameters');
                            print('or dil and dil_units are missing from sample descripton');
                            exit(-1);
                        elif not(conversion and conversion_units):
                            print('biological_material or conversion name is incorrect');
                            exit(-1);  
                        else:
                            #calculate the cell volume
                            cell_volume, cell_volume_units = self.calculate.calculate_cellVolume_CVSAndCVSUnitsAndODAndConversionAndConversionUnits(cvs,cvs_units,od600,conversion,conversion_units);
                            # calculate the normalized concentration
                            norm_conc = None;
                            norm_conc_units = None;
                            norm_conc, norm_conc_units = self.calculate.calculate_conc_concAndConcUnitsAndDilAndDilUnitsAndConversionAndConversionUnits(lloq,conc_units,dil,dil_units,cell_volume, cell_volume_units);
                            if norm_conc:
                                norm_conc = norm_conc/2;
                                # update data_stage01_quantification_normalized
                            #    dataListUpdated_I.append({'experiment_id':experiment_id_I,
                            #        'sample_name_short':sns,
                            #        'time_point':tp,
                            #        'component_group_name':component_group_name,
                            #        'component_name':cn,
                            #        'calculated_concentration':norm_conc,
                            #        'calculated_concentration_units':norm_conc_units,
                            #        'used_':True,
                            #        'comment_':None});
                                # populate data_stage01_quantification_replicatesMI
                                row = data_stage01_quantification_replicatesMI(experiment_id_I,sns,tp,component_group_name,cn,norm_conc,norm_conc_units,True);
                                self.session.add(row);
                    else:
                        for cn in component_names:
                            # get the calculated concentration
                            calc_conc = lloq/2;
                            # populate data_stage01_quantification_replicatesMI
                            #dataListUpdated_I.append({'experiment_id':experiment_id_I,
                            #        'sample_name_short':sns,
                            #        'time_point':tp,
                            #        'component_group_name':component_group_name,
                            #        'component_name':cn,
                            #        'calculated_concentration':calc_conc,
                            #        'calculated_concentration_units':conc_units,
                            #        'used_':True,
                            #        'comment_':None});
                            row = data_stage01_quantification_replicatesMI(experiment_id_I,sns,tp,component_group_name,cn,calc_conc,conc_units,True);
                            self.session.add(row);
        #io.update_dataStage01ReplicatesMI(dataListUpdated_I);
        self.session.commit();
    def execute_calculateAverages_replicates(self,experiment_id_I,sample_name_abbreviations_I=[]):
        '''Calculate the averages from replicates MI'''
        
        print 'execute_calculateAverages_replicates...'
        # get sample_name_abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentID_dataStage01ReplicatesMI(experiment_id_I);
        for sna in sample_name_abbreviations:
            print 'calculating averages from replicates for sample_name_abbreviation ' + sna;
            # get component names
            component_names = [];
            component_names = self.stage01_quantification_query.get_componentNames_experimentIDAndSampleNameAbbreviation_dataStage01ReplicatesMI(experiment_id_I,sna);
            for cn in component_names:
                print 'calculating averages from replicates for component_name ' + cn;
                component_group_name = self.stage01_quantification_query.get_componentGroupName_experimentIDAndComponentName_dataStage01Normalized(experiment_id_I,cn);
                # get time points
                time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01ReplicatesMI(experiment_id_I,sna);
                for tp in time_points:
                    print 'calculating averages from replicates for time_point ' + tp;
                    # get sample names short
                    sample_names_short = [];
                    sample_names_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndComponentNameAndTimePoint_dataStage01ReplicatesMI(experiment_id_I,sna,cn,tp);
                    concs = [];
                    conc_units = None;
                    for sns in sample_names_short:
                        # concentrations and units
                        conc = None;
                        conc_unit = None;
                        conc, conc_unit = self.stage01_quantification_query.get_concAndConcUnits_experimentIDAndSampleNameShortAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id_I,sns,tp,cn);
                        if (not(conc) or conc==0): continue
                        if (conc_unit): conc_units = conc_unit;
                        concs.append(conc);
                    n_replicates = len(concs);
                    conc_average = 0.0;
                    conc_var = 0.0;
                    conc_cv = 0.0;
                    # calculate average and CV of concentrations
                    if (not(concs)): 
                        continue
                    elif n_replicates<2: 
                        continue
                    else: 
                        #conc_average, conc_var = self.calculate.calculate_ave_var_R(concs);
                        conc_average = numpy.mean(numpy.array(concs));
                        conc_var = numpy.var(numpy.array(concs));
                        if (conc_average <= 0): conc_cv = 0;
                        else: conc_cv = sqrt(conc_var)/conc_average*100; 

                    # add data to the session
                    row = data_stage01_quantification_averagesMI(experiment_id_I, sna, tp, component_group_name, cn,
                                                   n_replicates, conc_average, conc_cv, conc_units, True);   
                    self.session.add(row);
            self.session.commit(); 
    def execute_calculateGeoAverages_replicates(self,experiment_id_I,sample_name_abbreviations_I=[]):
        '''Calculate the averages from replicates MI in ln space'''

        print ' execute_calculateGeoAverages_replicates...'
        # get sample_name_abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentID_dataStage01ReplicatesMI(experiment_id_I);
        for sna in sample_name_abbreviations:
            print 'calculating the geometric average from replicates for sample_name_abbreviation ' + sna;
            # get component names
            component_names = [];
            component_names = self.stage01_quantification_query.get_componentNames_experimentIDAndSampleNameAbbreviation_dataStage01ReplicatesMI(experiment_id_I,sna);
            for cn in component_names:
                print 'calculating the geometric average from replicates for component_names ' + cn;
                component_group_name = self.stage01_quantification_query.get_componentGroupName_experimentIDAndComponentName_dataStage01Normalized(experiment_id_I,cn);
                # get time points
                time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01ReplicatesMI(experiment_id_I,sna);
                for tp in time_points:
                    print 'calculating the geometric average from replicates for time_points ' + tp;
                    # get sample names short
                    sample_names_short = [];
                    sample_names_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndComponentNameAndTimePoint_dataStage01ReplicatesMI(experiment_id_I,sna,cn,tp);
                    concs = [];
                    conc_units = None;
                    for sns in sample_names_short:
                        # concentrations and units
                        conc = None;
                        conc_unit = None;
                        conc, conc_unit = self.stage01_quantification_query.get_concAndConcUnits_experimentIDAndSampleNameShortAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id_I,sns,tp,cn);
                        if (not(conc) or conc==0): continue
                        # calculate the ln of the concentration
                        # and convert to M from mM or uM
                        if (conc_unit == 'mM'): 
                            conc_units = 'M'; 
                            conc = conc*1e-3;
                        elif (conc_unit == 'uM'):
                            conc_units = 'M'; 
                            conc = conc*1e-6;
                        elif (conc_unit == 'uM'):
                            conc_units = 'M'; 
                            conc = conc*1e-6;
                        elif (conc_unit == 'uM*gDW-1'):
                            conc_units = 'M*gDW-1';
                            conc = conc*1e-6;
                        elif (conc_unit == 'height_ratio' or conc_unit == 'area_ratio'):
                            continue;
                        else:
                            print 'units of ' + str(conc_unit) + ' are not supported'
                            exit(-1);
                        concs.append(conc);
                    n_replicates = len(concs);
                    conc_average = 0.0;
                    conc_var = 0.0;
                    conc_lb = 0.0;
                    conc_ub = 0.0;
                    # calculate average and CV of concentrations
                    if (not(concs)): 
                        continue
                    elif n_replicates<2: 
                        continue
                    else: 
                        conc_average, conc_var, conc_lb, conc_ub = self.calculate.calculate_ave_var_geometric(concs);

                    # add data to the session
                    row = data_stage01_quantification_averagesMIgeo(experiment_id_I, sna, tp, component_group_name, cn,
                                                   n_replicates, conc_average, conc_var, conc_lb, conc_ub, conc_units, True);   
                    self.session.add(row);
            self.session.commit(); 
    def execute_physiologicalRatios_replicates(self,experiment_id_I):
        '''Calculate physiologicalRatios from replicates MI'''
        
        print 'calculate_physiologicalRatios_replicates...'
        # get sample names short
        sample_names_short = [];
        sample_names_short = self.stage01_quantification_query.get_SampleNameShort_experimentID_dataStage01ReplicatesMI(experiment_id_I);
        ratios_calc_O = [];
        for sns in sample_names_short:
            print 'calculating physiologicalRatios from replicates for sample_names_short ' + sns;
            # get time points
            time_points = [];
            time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndSampleNameShort_dataStage01ReplicatesMI(experiment_id_I,sns);
            for tp in time_points:
                print 'calculating physiologicalRatios from replicates for time_point ' + tp;
                for k,v in self.ratios.iteritems():
                    print 'calculating physiologicalRatios from replicates for ratio ' + k;
                    ratios_data={};
                    calcratios=True;
                    for cgn in v['component_group_name']:
                        ratios_data[cgn] = None;
                        # concentrations and units
                        conc = None;
                        conc_unit = None;
                        conc, conc_unit = self.stage01_quantification_query.get_concAndConcUnits_experimentIDAndSampleNameShortAndTimePointAndComponentGroupName_dataStage01ReplicatesMI(experiment_id_I,sns,tp,cgn);
                        if not(conc): 
                            calcratios=False;
                            break;
                        ratios_data[cgn]=conc;
                    # calculate the physiologicalratios
                    if not calcratios: continue
                    ratio_calc,num_calc,den_calc = self.calculate_physiologicalRatios(k,ratios_data);
                    # add data to the session
                    row = data_stage01_quantification_physiologicalRatios_replicates(experiment_id_I,
                                                                                    sns,
                                                                                    tp,
                                                                                    k,
                                                                                    v['name'],
                                                                                    ratio_calc,
                                                                                    v['description'],
                                                                                    True,
                                                                                    None);   
                    self.session.add(row);
                    row = data_stage01_quantification_physiologicalRatios_replicates(experiment_id_I,
                                                                                    sns,
                                                                                    tp,
                                                                                    k+'_numerator',
                                                                                    v['name']+'_numerator',
                                                                                    num_calc,
                                                                                    v['description'].split('/')[0],
                                                                                    True,
                                                                                    None);   
                    self.session.add(row);
                    row = data_stage01_quantification_physiologicalRatios_replicates(experiment_id_I,
                                                                                    sns,
                                                                                    tp,
                                                                                    k+'_denominator',
                                                                                    v['name']+'_denominator',
                                                                                    den_calc,
                                                                                    v['description'].split('/')[1],
                                                                                    True,
                                                                                    None);   
                    self.session.add(row);
        self.session.commit(); 
    def execute_physiologicalRatios_averages(self,experiment_id_I):
        '''Calculate physiologicalRatios_averages from physiologicalRatios_replicates'''
        
        print 'calculate_physiologicalRatios_averages...'
        # get sample_name_abbreviations
        sample_name_abbreviations = [];
        sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentID_dataStage01PhysiologicalRatiosReplicates(experiment_id_I);
        for sna in sample_name_abbreviations:
            print 'calculating physiologicalRatios from replicates for sample_name_abbreviation ' + sna;
            # get time points
            time_points = [];
            time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologicalRatiosReplicates(experiment_id_I,sna);
            for tp in time_points:
                print 'calculating physiologicalRatios from replicates for time_point ' + tp;
                # get ratio information
                ratio_info = {};
                ratio_info = self.stage01_quantification_query.get_ratioIDs_experimentIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(experiment_id_I,tp)
                #for k,v in self.ratios.iteritems():
                for k,v in ratio_info.iteritems():
                    print 'calculating physiologicalRatios from replicates for ratio ' + k;
                    # get sample names short
                    sample_names_short = [];
                    sample_names_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndRatioIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(experiment_id_I,sna,k,tp);
                    ratios = [];
                    for sns in sample_names_short:
                        # get ratios
                        ratio = None;
                        ratio = self.stage01_quantification_query.get_ratio_experimentIDAndSampleNameShortAndTimePointAndRatioID_dataStage01PhysiologicalRatiosReplicates(experiment_id_I,sns,tp,k);
                        if not ratio: continue;
                        ratios.append(ratio);
                    n_replicates = len(ratios);
                    ratio_average = 0.0;
                    ratio_var = 0.0;
                    ratio_cv = 0.0;
                    ratio_lb = 0.0;
                    ratio_ub = 0.0;
                    # calculate average and CV of ratios
                    if (not(ratios)): 
                        continue
                    elif n_replicates<2: 
                        continue
                    else: 
                        ratio_average,ratio_var,ratio_lb,ratio_ub = self.calculate.calculate_ave_var(ratios);
                        if (ratio_average <= 0): ratio_cv = 0;
                        else: ratio_cv = sqrt(ratio_var)/ratio_average*100; 
                    # add data to the session
                    row = data_stage01_quantification_physiologicalRatios_averages(experiment_id_I, 
                                                                               sna,
                                                                               tp,
                                                                               k,
                                                                               v['name'],
                                                                               ratio_average,
                                                                               ratio_cv,
                                                                               ratio_lb,
                                                                               ratio_ub,
                                                                               v['description'],
                                                                               True,
                                                                               None);   
                    self.session.add(row);
        self.session.commit(); 
    def execute_analyzePeakInformation(self,experiment_id_I,sample_names_I=[],
                            sample_types_I=['Standard'],
                            component_names_I=[],
                            peakInfo_I = ['height','retention_time','width_at_50','signal_2_noise'],
                            acquisition_date_and_time_I=[None,None]):
        '''Analyze retention-time, height, s/n, and assymetry'''

        #INPUT:
        #   experiment_id_I
        #   sample_names_I
        #   sample_types_I
        #   component_names_I
        #   peakInfo_I
        #   acquisition_date_and_time_I = ['%m/%d/%Y %H:%M','%m/%d/%Y %H:%M']

        print 'execute_peakInformation...'
        
        #convert string date time to datetime
        # e.g. time.strptime('4/15/2014 15:51','%m/%d/%Y %H:%M')
        acquisition_date_and_time = [];
        if acquisition_date_and_time_I[0] and acquisition_date_and_time_I[1]:
            for dateandtime in acquisition_date_and_time_I:
                time_struct = strptime(dateandtime,'%m/%d/%Y %H:%M')
                dt = datetime.fromtimestamp(mktime(time_struct))
                acquisition_date_and_time.append(dt);
        else: acquisition_date_and_time=[None,None]
        data_O = [];
        component_names_all = [];
        # get sample names
        if sample_names_I and sample_types_I and len(sample_types_I)==1:
            sample_names = sample_names_I;
            sample_types = [sample_types_I[0] for sn in sample_names];
        else:
            sample_names = [];
            sample_types = [];
            for st in sample_types_I:
                sample_names_tmp = [];
                sample_names_tmp = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleType(experiment_id_I,st);
                sample_names.extend(sample_names_tmp);
                sample_types_tmp = [];
                sample_types_tmp = [st for sn in sample_names_tmp];
                sample_types.extend(sample_types_tmp);
        print str(len(sample_names)) + ' total samples';
        for sn in sample_names:
            print 'analyzing peakInformation for sample_name ' + sn;
            # get sample description
            desc = {};
            desc = self.stage01_quantification_query.get_description_experimentIDAndSampleID_sampleDescription(experiment_id_I,sn);
            # get component names
            if component_names_I:
                component_names = component_names_I;
            else:
                component_names = [];
                component_names = self.stage01_quantification_query.get_componentsNames_experimentIDAndSampleName(experiment_id_I,sn);
            component_names_all.extend(component_names);
            for cn in component_names:
                # get rt, height, s/n
                sst_data = {};
                sst_data = self.stage01_quantification_query.get_peakInfo_sampleNameAndComponentName(sn,cn,acquisition_date_and_time);
                if sst_data:
                    tmp = {};
                    tmp.update(sst_data);
                    tmp.update(desc);
                    tmp.update({'sample_name':sn});
                    data_O.append(tmp);
        # calculate statistics for specific parameters
        component_names_unique = list(set(component_names_all));
        component_names_unique.sort();
        for cn in component_names_unique:
            data_parameters = {};
            data_parameters_stats = {};
            for parameter in peakInfo_I:
                data_parameters[parameter] = [];
                data_parameters_stats[parameter] = {'ave':None,'var':None,'cv':None,'lb':None,'ub':None};
                acquisition_date_and_times = [];
                sample_names_parameter = [];
                sample_types_parameter = [];
                component_group_name = None;
                for sn_cnt,sn in enumerate(sample_names):
                    for d in data_O:
                        if d['sample_name'] == sn and d['component_name'] == cn and d[parameter]:
                            data_parameters[parameter].append(d[parameter]);
                            acquisition_date_and_times.append(d['acquisition_date_and_time'])
                            sample_names_parameter.append(sn);
                            sample_types_parameter.append(sample_types[sn_cnt])
                            component_group_name = d['component_group_name'];
                ave,var,lb,ub = None,None,None,None;
                if len(data_parameters[parameter])>1:ave,var,lb,ub = self.calculate.calculate_ave_var(data_parameters[parameter]);
                if ave:
                    cv = sqrt(var)/ave*100;
                    data_parameters_stats[parameter] = {'ave':ave,'var':var,'cv':cv,'lb':lb,'ub':ub};
                    # add data to the database:
                    row = None;
                    row = data_stage01_quantification_peakInformation(experiment_id_I,
                                            component_group_name,
                                            cn,
                                            parameter,
                                            data_parameters_stats[parameter]['ave'],
                                            data_parameters_stats[parameter]['cv'],
                                            data_parameters_stats[parameter]['lb'],
                                            data_parameters_stats[parameter]['ub'],
                                            None,
                                            sample_names_parameter,
                                            sample_types_parameter,
                                            acquisition_date_and_times,
                                            data_parameters[parameter],
                                            True,
                                            None);
                    self.session.add(row);
        self.session.commit();
    def execute_analyzePeakResolution(self,experiment_id_I,sample_names_I=[],sample_types_I=['Standard'],component_name_pairs_I=[],
                            acquisition_date_and_time_I=[None,None]):
        '''Analyze resolution for critical pairs'''
        #Input:
        #   experiment_id_I
        #   sample_names_I
        #   sample_types_I
        #   component_name_pairs_I = [[component_name_1,component_name_2],...]
        #   acquisition_date_and_time_I = ['%m/%d/%Y %H:%M','%m/%d/%Y %H:%M']

        print 'execute_peakInformation_resolution...'
        #convert string date time to datetime
        # e.g. time.strptime('4/15/2014 15:51','%m/%d/%Y %H:%M')
        acquisition_date_and_time = [];
        if acquisition_date_and_time_I[0] and acquisition_date_and_time_I[1]:
            for dateandtime in acquisition_date_and_time_I:
                time_struct = strptime(dateandtime,'%m/%d/%Y %H:%M')
                dt = datetime.fromtimestamp(mktime(time_struct))
                acquisition_date_and_time.append(dt);
        else: acquisition_date_and_time=[None,None]
        data_O = [];
        component_names_pairs_all = [];
        # get sample names
        if sample_names_I and sample_types_I and len(sample_types_I)==1:
            sample_names = sample_names_I;
            sample_types = [sample_types_I[0] for sn in sample_names];
        else:
            sample_names = [];
            sample_types = [];
            for st in sample_types_I:
                sample_names_tmp = [];
                sample_names_tmp = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleType(experiment_id_I,st);
                sample_names.extend(sample_names_tmp);
                sample_types_tmp = [];
                sample_types_tmp = [st for sn in sample_names_tmp];
                sample_types.extend(sample_types_tmp);
        for sn in sample_names:
            print 'analyzing peakInformation for sample_name ' + sn;
            for component_name_pair in component_name_pairs_I:
                # get critical pair data
                cpd1 = {};
                cpd2 = {};
                cpd1 = self.stage01_quantification_query.get_peakInfo_sampleNameAndComponentName(sn,component_name_pair[0],acquisition_date_and_time);
                cpd2 = self.stage01_quantification_query.get_peakInfo_sampleNameAndComponentName(sn,component_name_pair[1],acquisition_date_and_time);
                if cpd1 and cpd2 and cpd1['retention_time'] and cpd2['retention_time']:
                    # calculate the RT difference and resolution
                    rt_dif = 0.0;
                    rt_dif = abs(cpd1['retention_time']-cpd2['retention_time'])
                    resolution = 0.0;
                    resolution = rt_dif/(0.5*(cpd1['width_at_50']+cpd2['width_at_50']));
                    # record data
                    data_O.append({'component_name_pair':component_name_pair,
                                   'rt_dif':rt_dif,
                                   'resolution':resolution,
                                   'component_group_name_pair':[cpd1['component_group_name'],cpd2['component_group_name']],
                                   'sample_name':sn,
                                   'acquisition_date_and_time':cpd1['acquisition_date_and_time']});
        # calculate statistics for specific parameters
        for cnp in component_name_pairs_I:
            data_parameters = {};
            data_parameters_stats = {};
            for parameter in ['rt_dif','resolution']:
                data_parameters[parameter] = [];
                data_parameters_stats[parameter] = {'ave':None,'var':None,'cv':None,'lb':None,'ub':None};
                acquisition_date_and_times = [];
                sample_names_parameter = [];
                sample_types_parameter = [];
                component_group_name_pair = None;
                for sn_cnt,sn in enumerate(sample_names):
                    for d in data_O:
                        if d['sample_name'] == sn and d['component_name_pair'] == cnp and d[parameter]:
                            data_parameters[parameter].append(d[parameter]);
                            acquisition_date_and_times.append(d['acquisition_date_and_time'])
                            sample_names_parameter.append(sn);
                            sample_types_parameter.append(sample_types[sn_cnt])
                            component_group_name_pair = d['component_group_name_pair'];
                ave,var,lb,ub = None,None,None,None;
                if len(data_parameters[parameter])>1:ave,var,lb,ub = self.calculate.calculate_ave_var(data_parameters[parameter]);
                if ave:
                    cv = sqrt(var)/ave*100;
                    data_parameters_stats[parameter] = {'ave':ave,'var':var,'cv':cv,'lb':lb,'ub':ub};
                    # add data to the database:
                    row = None;
                    row = data_stage01_quantification_peakResolution(experiment_id_I,
                                            component_group_name_pair,
                                            cnp,
                                            parameter,
                                            data_parameters_stats[parameter]['ave'],
                                            data_parameters_stats[parameter]['cv'],
                                            data_parameters_stats[parameter]['lb'],
                                            data_parameters_stats[parameter]['ub'],
                                            None,
                                            sample_names_parameter,
                                            sample_types_parameter,
                                            acquisition_date_and_times,
                                            data_parameters[parameter],
                                            True,
                                            None);
                    self.session.add(row);
        self.session.commit();
    # updates from QCs
    def update_dataStage01Normalized_replicates(self,experiment_id_I):
        return
    def update_dataStage01Normalized_averages(self,experiment_id_I):
        '''--upadate to used_ from data_stage01_quantification_mqresultstable based on averages
        UPDATE data_stage01_quantification_mqresultstable
           SET used_= FALSE
        --SELECT 
          --data_stage01_quantification_mqresultstable.sample_name, 
          --data_stage01_quantification_mqresultstable.component_name, 
          --data_stage01_quantification_mqresultstable.used_, 
          --data_stage01_quantification_mqresultstable.calculated_concentration
        FROM 
          public.experiment, 
          public.sample, 
          public.sample_description--, 
          --public.data_stage01_quantification_mqresultstable
        WHERE 
          experiment.id LIKE 'nitrate01' AND 
          experiment.sample_name LIKE data_stage01_quantification_mqresultstable.sample_name AND 
          experiment.sample_name LIKE sample.sample_name AND 
          sample.sample_id LIKE sample_description.sample_id AND 
          sample_description.sample_name_abbreviation LIKE 'AnoxicWTNitrate' AND 
          sample_description.time_point LIKE '0' AND 
          sample_description.sample_description LIKE 'Filtrate' AND 
          data_stage01_quantification_mqresultstable.component_name LIKE 'uri.uri_1.Light' AND 
          (sample.sample_dilution = 1 OR
          sample.sample_dilution = 10);'''

        return
    def update_dataStage01Averages_checkCVAndExtracellular(self,experiment_id_I):
        return
    # data_stage01_quantification initializations
    def drop_dataStage01_quantification(self):
        try:
            #data_stage01_quantification_MQResultsTable.__table__.drop(engine,True);
            data_stage01_quantification_LLOQAndULOQ.__table__.drop(engine,True);
            data_stage01_quantification_checkLLOQAndULOQ.__table__.drop(engine,True);
            data_stage01_quantification_checkISMatch.__table__.drop(engine,True);
            data_stage01_quantification_QCs.__table__.drop(engine,True);
            data_stage01_quantification_checkCV_QCs.__table__.drop(engine,True);
            data_stage01_quantification_dilutions.__table__.drop(engine,True);
            data_stage01_quantification_checkCV_dilutions.__table__.drop(engine,True);
            data_stage01_quantification_normalized.__table__.drop(engine,True);
            data_stage01_quantification_replicates.__table__.drop(engine,True);
            data_stage01_quantification_averages.__table__.drop(engine,True);
            data_stage01_quantification_checkCVAndExtracellular_averages.__table__.drop(engine,True);
            data_stage01_quantification_replicatesMI.__table__.drop(engine,TRUE);
            data_stage01_quantification_averagesMI.__table__.drop(engine,TRUE);
            data_stage01_quantification_averagesMIgeo.__table__.drop(engine,TRUE);
            data_stage01_quantification_physiologicalRatios_replicates.__table__.drop(engine,TRUE);
            data_stage01_quantification_physiologicalRatios_averages.__table__.drop(engine,TRUE);
            data_stage01_quantification_peakInformation.__table__.drop(engine,TRUE);
            data_stage01_quantification_peakResolution.__table__.drop(engine,TRUE);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage01_quantification(self,experiment_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage01_quantification_LLOQAndULOQ).filter(data_stage01_quantification_LLOQAndULOQ.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkLLOQAndULOQ).filter(data_stage01_quantification_checkLLOQAndULOQ.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkISMatch).filter(data_stage01_quantification_checkISMatch.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkCV_QCs).filter(data_stage01_quantification_checkCV_QCs.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_dilutions).filter(data_stage01_quantification_dilutions.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkCV_dilutions).filter(data_stage01_quantification_checkCV_dilutions.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkCVAndExtracellular_averages).filter(data_stage01_quantification_checkCVAndExtracellular_averages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_QCs).filter(data_stage01_quantification_QCs.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_normalized).filter(data_stage01_quantification_normalized.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_replicates).filter(data_stage01_quantification_replicates.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averages).filter(data_stage01_quantification_averages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_replicatesMI).filter(data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averagesMI).filter(data_stage01_quantification_averagesMI.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averagesMIgeo).filter(data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_replicates).filter(data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_averages).filter(data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_peakInformation).filter(data_stage01_quantification_peakInformation.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_peakResolution).filter(data_stage01_quantification_peakResolution.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage01_quantification_LLOQAndULOQ).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkLLOQAndULOQ).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkISMatch).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkCV_QCs).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkCV_dilutions).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_dilutions).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_checkCVAndExtracellular_averages).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averages).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_replicatesMI).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averagesMI).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averagesMIgeo).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_replicates).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_averages).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_peakInformation).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_peakResolution).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_datastage01_quantification_replicatesAndAverages(self,experiment_id_I):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage01_quantification_checkCVAndExtracellular_averages).filter(data_stage01_quantification_checkCVAndExtracellular_averages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_replicates).filter(data_stage01_quantification_replicates.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averages).filter(data_stage01_quantification_averages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_replicatesMI).filter(data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averagesMI).filter(data_stage01_quantification_averagesMI.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averagesMIgeo).filter(data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_replicates).filter(data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_averages).filter(data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_datastage01_quantification_replicatesAndAveragesMI(self,experiment_id_I):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage01_quantification_replicatesMI).filter(data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averagesMI).filter(data_stage01_quantification_averagesMI.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averagesMIgeo).filter(data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_replicates).filter(data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_averages).filter(data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_datastage01_quantification_averagesMI(self,experiment_id_I):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage01_quantification_averagesMI).filter(data_stage01_quantification_averagesMI.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_averagesMIgeo).filter(data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_replicates).filter(data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_quantification_physiologicalRatios_averages).filter(data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage01_quantification(self):
        try:
            data_stage01_quantification_MQResultsTable.__table__.create(engine,True);
            data_stage01_quantification_LLOQAndULOQ.__table__.create(engine,True);
            data_stage01_quantification_checkLLOQAndULOQ.__table__.create(engine,True);
            data_stage01_quantification_checkISMatch.__table__.create(engine,True);
            data_stage01_quantification_QCs.__table__.create(engine,True);
            data_stage01_quantification_checkCV_QCs.__table__.create(engine,True);
            data_stage01_quantification_dilutions.__table__.create(engine,True);
            data_stage01_quantification_checkCV_dilutions.__table__.create(engine,True);
            data_stage01_quantification_normalized.__table__.create(engine,True);
            data_stage01_quantification_replicates.__table__.create(engine,True);
            data_stage01_quantification_averages.__table__.create(engine,True);
            data_stage01_quantification_checkCVAndExtracellular_averages.__table__.create(engine,True);
            data_stage01_quantification_replicatesMI.__table__.create(engine,True);
            data_stage01_quantification_averagesMI.__table__.create(engine,True);
            data_stage01_quantification_averagesMIgeo.__table__.create(engine,True);
            data_stage01_quantification_physiologicalRatios_replicates.__table__.create(engine,True);
            data_stage01_quantification_physiologicalRatios_averages.__table__.create(engine,True);
            data_stage01_quantification_peakInformation.__table__.create(engine,True);
            data_stage01_quantification_peakResolution.__table__.create(engine,True);
        except SQLAlchemyError as e:
            print(e);
    # data_stage01_quantification deletes
    def execute_deleteExperimentFromMQResultsTable(self,experiment_id_I,sample_types_I = ['Quality Control','Unknown'],sample_names_I = []):
        '''delete rows in data_stage01_MQResultsTable by sample name and sample type 
        (default = Quality Control and Unknown) from the experiment'''
        
        print 'deleting rows in data_stage01_MQResultsTable by sample_name and sample_type...';
        dataDeletes = [];
        # get sample_names
        if sample_names_I:
            sample_names = sample_names_I;
        else:
            sample_names = [];
            for st in sample_types_I:
                sample_names_tmp = [];
                sample_names_tmp = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleType(experiment_id_I,st);
                sample_names.extend(sample_names_tmp);
        for sn in sample_names:
            # format into a dictionary list
            print 'deleting sample_name ' + sn;
            dataDeletes.append({'sample_name':sn});
        # delete rows based on sample_names
        self.stage01_quantification_query.delete_row_sampleName(dataDeletes);
    #   internal methods
    def calculate_physiologicalRatios(self,ratio_id_I,ratio_mets_I):
        '''Calculate physiological ratios'''
        #Input:
        # ratio_id_I = string
        # ratio_mets_I = {component_group_name:float}
        #Output:
        # 'ratio_O':float
        # 'num_O':float
        # 'den_O':float
        
        ratio_O = None;
        num_O = None;
        den_O = None
        if ratio_id_I == 'accoa_ratio':
            num_O = ratio_mets_I["accoa"]
            den_O = ratio_mets_I["coa"]+ratio_mets_I["accoa"]
            ratio_O = ratio_mets_I["accoa"]/(ratio_mets_I["coa"]+ratio_mets_I["accoa"])
        elif ratio_id_I == 'ec':
            num_O = 0.5*ratio_mets_I["adp"]+ratio_mets_I["atp"]
            den_O = ratio_mets_I["adp"]+ratio_mets_I["amp"]+ratio_mets_I["atp"]
            ratio_O = (0.5*ratio_mets_I["adp"]+ratio_mets_I["atp"])/(ratio_mets_I["adp"]+ratio_mets_I["amp"]+ratio_mets_I["atp"])
        elif ratio_id_I == 'p_ratio01':
            num_O = ratio_mets_I["atp"]
            den_O = ratio_mets_I["adp"]
            ratio_O = ratio_mets_I["atp"]/ratio_mets_I["adp"]
        elif ratio_id_I == 'p_ratio02':
            num_O = ratio_mets_I["atp"]
            den_O = ratio_mets_I["amp"]
            ratio_O = ratio_mets_I["atp"]/ratio_mets_I["amp"]
        elif ratio_id_I == 'redox_ratio':
            num_O = ratio_mets_I["gthrd"]
            den_O = ratio_mets_I["gthox"]+ratio_mets_I["gthrd"]
            ratio_O = ratio_mets_I["gthrd"]/(ratio_mets_I["gthox"]+ratio_mets_I["gthrd"])
        elif ratio_id_I == 'gth_ratio01':
            num_O = ratio_mets_I["gthrd"]
            den_O = ratio_mets_I["gthox"]
            ratio_O = ratio_mets_I["gthrd"]/ratio_mets_I["gthox"]
        elif ratio_id_I == 'mar_ak':
            num_O = ratio_mets_I["amp"]*ratio_mets_I["atp"]
            den_O = ratio_mets_I["adp"]*ratio_mets_I["adp"]
            ratio_O = (ratio_mets_I["amp"]*ratio_mets_I["atp"])/(ratio_mets_I["adp"]*ratio_mets_I["adp"])
        elif ratio_id_I == 'mar_fum':
            num_O = ratio_mets_I["fum"]
            den_O = ratio_mets_I["mal-L"]
            ratio_O = ratio_mets_I["fum"]/ratio_mets_I["mal-L"]
        elif ratio_id_I == 'mar_pgi':
            num_O = ratio_mets_I["f6p"]/ratio_mets_I["g6p"]
            den_O = ratio_mets_I["f6p"]/ratio_mets_I["g6p"]
            ratio_O = ratio_mets_I["f6p"]/ratio_mets_I["g6p"]
        elif ratio_id_I == 'mar_pgm_eno':
            num_O = ratio_mets_I["pep"]
            den_O = ratio_mets_I["Pool_2pg_3pg"]
            ratio_O = ratio_mets_I["pep"]/ratio_mets_I["Pool_2pg_3pg"]
        #elif ratio_id_I == 'n2_ratio01':
        #    ratio_O = ratio_mets_I["gln-L"]/(ratio_mets_I["gln-L"]+ratio_mets_I["glu-L"])
        #elif ratio_id_I == 'n2_ratio02':
        #    ratio_O = ratio_mets_I["glu-L"]/(ratio_mets_I["akg"]+ratio_mets_I["glu-L"])
        elif ratio_id_I == 'n2_ratio01':
            num_O = ratio_mets_I["gln-L"]
            den_O = ratio_mets_I["glu-L"]
            ratio_O = ratio_mets_I["gln-L"]/ratio_mets_I["glu-L"]
        elif ratio_id_I == 'n2_ratio02':
            num_O = ratio_mets_I["glu-L"]
            den_O = ratio_mets_I["akg"]
            ratio_O = ratio_mets_I["glu-L"]/ratio_mets_I["akg"]
        elif ratio_id_I == 'n2_ratio03':
            num_O = ratio_mets_I["gln-L"]
            den_O = ratio_mets_I["akg"]
            ratio_O = ratio_mets_I["gln-L"]/ratio_mets_I["akg"]
        elif ratio_id_I == 'nc':
            num_O = 0.5*ratio_mets_I["glu-L"]+ratio_mets_I["gln-L"]
            den_O = ratio_mets_I["akg"]+ratio_mets_I["glu-L"]+ratio_mets_I["gln-L"]
            ratio_O = (0.5*ratio_mets_I["glu-L"]+ratio_mets_I["gln-L"])/(ratio_mets_I["akg"]+ratio_mets_I["glu-L"]+ratio_mets_I["gln-L"])
        elif ratio_id_I == 'nad_ratio':
            num_O = ratio_mets_I["nadh"]
            den_O = ratio_mets_I["nad"]+ratio_mets_I["nadh"]
            ratio_O = ratio_mets_I["nadh"]/(ratio_mets_I["nad"]+ratio_mets_I["nadh"])
        elif ratio_id_I == 'nadp_ratio':
            num_O = ratio_mets_I["nadph"]
            den_O = ratio_mets_I["nadp"]+ratio_mets_I["nadph"]
            ratio_O = ratio_mets_I["nadph"]/(ratio_mets_I["nadp"]+ratio_mets_I["nadph"])
        elif ratio_id_I == 'nad(p)_ratio':
            num_O = ratio_mets_I["nadph"]+ratio_mets_I["nadh"]
            den_O = ratio_mets_I["nadp"]+ratio_mets_I["nadph"]+ratio_mets_I["nad"]+ratio_mets_I["nadh"]
            ratio_O = (ratio_mets_I["nadph"]+ratio_mets_I["nadh"])/(ratio_mets_I["nadp"]+ratio_mets_I["nadph"]+ratio_mets_I["nad"]+ratio_mets_I["nadh"])
        else:
            print 'ratio_id not recognized'
        return ratio_O,num_O,den_O;
    #  visualizations
    def execute_boxAndWhiskersPlot_physiologicalRatios(self,experiment_id_I,sample_name_abbreviations_I=[],ratio_ids_I=[]):
        '''generate a boxAndWhiskers plot from physiological ratios table'''

        print 'execute_boxAndWhiskersPlot...'
        # get time points
        time_points = [];
        time_points = self.stage01_quantification_query.get_timePoint_experimentID_dataStage01PhysiologicalRatiosAverages(experiment_id_I);
        for tp in time_points:
            print 'generating boxAndWhiskersPlot for time_point ' + tp;
            if ratio_ids_I:
                ratio_ids = ratio_ids_I;
            else:
                ratio_ids = self.ratios.keys();
            for k in ratio_ids:
            #for k,v in self.ratios.iteritems():
                print 'generating boxAndWhiskersPlot for ratio ' + k; # get sample_name_abbreviations
                data_plot_mean = [];
                data_plot_var = [];
                data_plot_ci = [];
                data_plot_sna = [];
                data_plot_ratio_ids = [];
                data_plot_data = [];
                data_plot_ratio_units = [];
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndRatioID_dataStage01PhysiologicalRatiosAverages(experiment_id_I,tp,k);
                for sna in sample_name_abbreviations:
                    print 'generating boxAndWhiskersPlot for sample_name_abbreviation ' + sna;
                    # get the data 
                    data = {};
                    data = self.stage01_quantification_query.get_data_experimentIDAndTimePointAndRatioIDAndSampleNameAbbreviation_dataStage01PhysiologicalRatiosAverages(experiment_id_I,tp,k,sna)
                    ratio_values = [];
                    ratio_values = self.stage01_quantification_query.get_ratios_experimentIDAndSampleNameAbbreviationAndTimePointAndRatioID_dataStage01PhysiologicalRatiosReplicates(experiment_id_I,sna,tp,k)
                    # record data for plotting
                    data_plot_mean.append(data['physiologicalratio_value_ave']);
                    data_plot_var.append(data['physiologicalratio_value_cv']);
                    data_plot_ci.append([data['physiologicalratio_value_lb'],data['physiologicalratio_value_ub']]);
                    data_plot_data.append(ratio_values);
                    data_plot_sna.append(sna);
                    data_plot_ratio_ids.append(k);
                    data_plot_ratio_units.append('');
                # visualize the stats:
                #self.matplot.barPlot(data_plot_ratio_ids[0],data_plot_sna,data_plot_sna[0],'samples',data_plot_mean,data_plot_var);
                self.matplot.boxAndWhiskersPlot(data_plot_ratio_ids[0],data_plot_sna,data_plot_ratio_units[0],'samples',data_plot_data,data_plot_mean,data_plot_ci);
    def execute_boxAndWhiskersPlot_averages(self,experiment_id_I,sample_name_abbreviations_I=[],component_names_I=[],time_points_I=[],time_course_I=False,show_95_ci_I=False,filename_I=None):
        '''generate a boxAndWhiskers plot from averagesMIGeo table'''

        print 'execute_boxAndWhiskersPlot...'
        if time_course_I:
            if component_names_I:
                component_names = component_names_I;
            else:
                component_names = [];
                component_names = self.stage01_quantification_query.get_componentNames_experimentID_dataStage01AveragesMIgeo(experiment_id_I);
            for cn in component_names:
                print 'generating boxAndWhiskersPlot for component_name ' + cn; 
                # get time points
                if time_points_I:
                    time_points = time_points_I;
                else:
                    time_points = [];
                    time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndComponentName_dataStage01AveragesMIgeo(experiment_id_I,cn);
                data_plot_mean = [];
                data_plot_var = [];
                data_plot_ci = [];
                data_plot_sna = [];
                data_plot_component_names = [];
                data_plot_data = [];
                data_plot_calculated_concentration_units = [];
                for tp in time_points:
                    print 'generating boxAndWhiskersPlot for time_point ' + tp;
                    # get sample_name_abbreviations
                    if sample_name_abbreviations_I:
                        sample_name_abbreviations = sample_name_abbreviations_I;
                    else:
                        sample_name_abbreviations = [];
                        sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndComponentName_dataStage01AveragesMIgeo(experiment_id_I,tp,cn);
                    for sna in sample_name_abbreviations:
                        print 'generating boxAndWhiskersPlot for sample_name_abbreviation ' + sna;
                        # get the data 
                        data = {};
                        data = self.stage01_quantification_query.get_data_experimentIDAndSampleNameAbbreviationAndTimePointAndComponentName_dataStage01AveragesMIgeo(experiment_id_I,sna,tp,cn)
                        if not data: continue;
                        calculated_concentrations = [];
                        calculated_concentrations = self.stage01_quantification_query.get_calculatedConcentrations_experimentIDAndSampleNameAbbreviationAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id_I,sna,tp,cn)
                        if not calculated_concentrations: continue;
                        # record data for plotting
                        data_plot_mean.append(data['calculated_concentration_average']);
                        data_plot_var.append(data['calculated_concentration_var']);
                        data_plot_ci.append([data['calculated_concentration_lb'],data['calculated_concentration_ub']]);
                        data_plot_data.append(numpy.array(calculated_concentrations)*1e-3);
                        data_plot_sna.append(sna);
                        data_plot_component_names.append(cn);
                        data_plot_calculated_concentration_units.append(data['calculated_concentration_units']);
                # visualize the stats:
                if filename_I: filename = filename_I + cn.split('.')[0];
                if show_95_ci_I:
                    data_95 = []
                    for i,d in enumerate(data_plot_mean):
                        data_95.append([data_plot_ci[i][0],data_plot_ci[i][1],d])
                    try:
                        if filename_I:
                            self.matplot.boxAndWhiskersPlot(data_plot_component_names[0],data_plot_sna,data_plot_calculated_concentration_units[0],'samples',data_95,data_plot_mean,data_plot_ci,filename_I=filename,show_plot_I=False);
                        else:
                            self.matplot.boxAndWhiskersPlot(data_plot_component_names[0],data_plot_sna,data_plot_calculated_concentration_units[0],'samples',data_95,data_plot_mean,data_plot_ci);
                    except IndexError as e:
                        print e;
                else:
                    data_plot_se = [(x[1]-x[0])/2 for x in data_plot_ci]
                    #self.matplot.barPlot(data_plot_component_names[0],data_plot_sna,data_plot_sna[0],'samples',data_plot_mean,se_I=data_plot_se,add_labels_I=False);
                    self.matplot.boxAndWhiskersPlot(data_plot_component_names[0],data_plot_sna,data_plot_calculated_concentration_units[0],'samples',data_plot_data,data_plot_mean,data_plot_ci);
        else:
            # get time points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage01_quantification_query.get_timePoint_experimentID_dataStage01AveragesMIgeo(experiment_id_I);
            for tp in time_points:
                print 'generating boxAndWhiskersPlot for time_point ' + tp;
                if component_names_I:
                    component_names = component_names_I;
                else:
                    component_names = [];
                    component_names = self.stage01_quantification_query.get_componentNames_experimentIDAndTimePoint_dataStage01AveragesMIgeo(experiment_id_I,tp);
                for cn in component_names:
                    print 'generating boxAndWhiskersPlot for component_name ' + cn; 
                    data_plot_mean = [];
                    data_plot_var = [];
                    data_plot_ci = [];
                    data_plot_sna = [];
                    data_plot_component_names = [];
                    data_plot_data = [];
                    data_plot_calculated_concentration_units = [];
                    # get sample_name_abbreviations
                    if sample_name_abbreviations_I:
                        sample_name_abbreviations = sample_name_abbreviations_I;
                    else:
                        sample_name_abbreviations = [];
                        sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndComponentName_dataStage01AveragesMIgeo(experiment_id_I,tp,cn);
                    for sna in sample_name_abbreviations:
                        print 'generating boxAndWhiskersPlot for sample_name_abbreviation ' + sna;
                        # get the data 
                        data = {};
                        data = self.stage01_quantification_query.get_data_experimentIDAndSampleNameAbbreviationAndTimePointAndComponentName_dataStage01AveragesMIgeo(experiment_id_I,sna,tp,cn)
                        if not data: continue;
                        calculated_concentrations = [];
                        calculated_concentrations = self.stage01_quantification_query.get_calculatedConcentrations_experimentIDAndSampleNameAbbreviationAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id_I,sna,tp,cn)
                        # record data for plotting
                        data_plot_mean.append(data['calculated_concentration_average']);
                        data_plot_var.append(data['calculated_concentration_var']);
                        data_plot_ci.append([data['calculated_concentration_lb'],data['calculated_concentration_ub']]);
                        data_plot_data.append(numpy.array(calculated_concentrations)*1e-3);
                        data_plot_sna.append(sna);
                        data_plot_component_names.append(cn);
                        data_plot_calculated_concentration_units.append(data['calculated_concentration_units']);
                    # visualize the stats:
                    if show_95_ci_I:
                        data_95 = []
                        for i,d in enumerate(data_plot_mean):
                            data_95.append([data_plot_ci[i][0],data_plot_ci[i][1],d])
                        self.matplot.boxAndWhiskersPlot(data_plot_component_names[0],data_plot_sna,data_plot_calculated_concentration_units[0],'samples',data_95,data_plot_mean,data_plot_ci);
                    else:
                        data_plot_se = [(x[1]-x[0])/2 for x in data_plot_ci]
                        #self.matplot.barPlot(data_plot_component_names[0],data_plot_sna,data_plot_sna[0],'samples',data_plot_mean,se_I=data_plot_se,add_labels_I=False);
                        self.matplot.boxAndWhiskersPlot(data_plot_component_names[0],data_plot_sna,data_plot_calculated_concentration_units[0],'samples',data_plot_data,data_plot_mean,data_plot_ci);
    def execute_barPlot_averages(self,experiment_id_I,sample_name_abbreviations_I=[],component_names_I=[]):
        '''generate a bar plot from averagesMIGeo table'''

        print 'execute_barPlot...'
        # get time points
        time_points = [];
        time_points = self.stage01_quantification_query.get_timePoint_experimentID_dataStage01AveragesMIgeo(experiment_id_I);
        for tp in time_points:
            print 'generating barPlot for time_point ' + tp;
            if component_names_I:
                component_names = component_names_I;
            else:
                component_names = [];
                component_names = self.stage01_quantification_query.get_componentNames_experimentIDAndTimePoint_dataStage01AveragesMIgeo(experiment_id_I,tp);
            for cn in component_names:
                print 'generating barPlot for component_name ' + cn; 
                data_plot_mean = [];
                data_plot_var = [];
                data_plot_ci = [];
                data_plot_sna = [];
                data_plot_component_names = [];
                data_plot_data = [];
                data_plot_calculated_concentration_units = [];
                # get sample_name_abbreviations
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndComponentName_dataStage01AveragesMIgeo(experiment_id_I,tp,cn);
                for sna in sample_name_abbreviations:
                    print 'generating barPlot for sample_name_abbreviation ' + sna;
                    # get the data 
                    data = {};
                    data = self.stage01_quantification_query.get_data_experimentIDAndSampleNameAbbreviationAndTimePointAndComponentName_dataStage01AveragesMIgeo(experiment_id_I,sna,tp,cn)
                    calculated_concentrations = [];
                    calculated_concentrations = self.stage01_quantification_query.get_calculatedConcentrations_experimentIDAndSampleNameAbbreviationAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id_I,sna,tp,cn)
                    # record data for plotting
                    data_plot_mean.append(data['calculated_concentration_average']);
                    data_plot_var.append(data['calculated_concentration_var']);
                    data_plot_ci.append([data['calculated_concentration_lb'],data['calculated_concentration_ub']]);
                    data_plot_data.append(numpy.array(calculated_concentrations)*1e-3);
                    data_plot_sna.append(sna);
                    data_plot_component_names.append(cn);
                    data_plot_calculated_concentration_units.append(data['calculated_concentration_units']);
                # visualize the stats:
                data_plot_se = [(x[1]-x[0])/2 for x in data_plot_ci]
                self.matplot.barPlot(data_plot_component_names[0],data_plot_sna,data_plot_calculated_concentration_units[0],'samples',data_plot_mean,se_I=data_plot_se,add_labels_I=False);
                #self.matplot.boxAndWhiskersPlot(data_plot_component_names[0],data_plot_sna,data_plot_calculated_concentration_units[0],'samples',data_plot_data,data_plot_mean,data_plot_ci);
    def execute_scatterLinePlot_physiologicalRatios(self,experiment_id_I,sample_name_abbreviations_I=[],ratio_ids_I=[]):
        '''Generate a scatter line plot for physiological ratios averages'''


        print 'Generating scatterLinePlot for physiologicalRatios'
        # get time points
        time_points = [];
        time_points = self.stage01_quantification_query.get_timePoint_experimentID_dataStage01PhysiologicalRatiosReplicates(experiment_id_I);
        for tp in time_points:
            print 'Generating scatterLinePlot for physiologicalRatios for time_point ' + tp;
            # get physiological ratio_ids
            ratios = {};
            ratios = self.stage01_quantification_query.get_ratioIDs_experimentIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(experiment_id_I,tp);
            for k,v in ratios.iteritems():
                if ratio_ids_I: 
                    if not k in ratio_ids_I:
                        continue;
                print 'Generating scatterLinePlot for physiologicalRatios for ratio ' + k;
                # get sample_names
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndRatioID_dataStage01PhysiologicalRatiosAverages(experiment_id_I,tp,k);
                ratios_num = [];
                ratios_den = [];
                for sna_cnt,sna in enumerate(sample_name_abbreviations):
                    print 'Generating scatterLinePlot for physiologicalRatios for sample name abbreviation ' + sna;
                    # get ratios_numerator
                    ratio_num = None;
                    ratio_num = self.stage01_quantification_query.get_ratio_experimentIDAndTimePointAndRatioIDAndSampleNameAbbreviation_dataStage01PhysiologicalRatiosAverages(experiment_id_I,tp,k+'_numerator',sna)
                    if not ratio_num: continue;
                    ratios_num.append(ratio_num);
                    # get ratios_denominator
                    ratio_den = None;
                    ratio_den = self.stage01_quantification_query.get_ratio_experimentIDAndTimePointAndRatioIDAndSampleNameAbbreviation_dataStage01PhysiologicalRatiosAverages(experiment_id_I,tp,k+'_denominator',sna)
                    if not ratio_den: continue;
                    ratios_den.append(ratio_den);
                # plot the data
                self.matplot.scatterLinePlot(k,k+'_denominator',k+'_numerator',ratios_den,ratios_num,sample_name_abbreviations);

    #TODO:
    def execute_scatterLinePlot_peakInformation(self,experiment_id_I,sample_names_I=[],
                            sample_types_I=['Standard'],
                            component_names_I=[],
                            peakInfo_I = ['retention_time'],
                            acquisition_date_and_time_I=[None,None],
                            x_title_I='Time [hrs]',y_title_I='Retention Time [min]',y_data_type_I='acquisition_date_and_time',
                            plot_type_I='single'):
        '''Analyze retention-time, height, s/n, and assymetry'''

        #INPUT:
        #   experiment_id_I
        #   sample_names_I
        #   sample_types_I
        #   component_names_I
        #   peakInfo_I
        #   acquisition_date_and_time_I = ['%m/%d/%Y %H:%M','%m/%d/%Y %H:%M']
        #   y_data_type_I = 'acquisition_date_and_time' or 'count'
        #   plot_type_I = 'single', 'multiple', or 'sub'

        print 'execute_peakInformation...'
        
        #convert string date time to datetime
        # e.g. time.strptime('4/15/2014 15:51','%m/%d/%Y %H:%M')
        acquisition_date_and_time = [];
        if acquisition_date_and_time_I[0] and acquisition_date_and_time_I[1]:
            for dateandtime in acquisition_date_and_time_I:
                time_struct = strptime(dateandtime,'%m/%d/%Y %H:%M')
                dt = datetime.fromtimestamp(mktime(time_struct))
                acquisition_date_and_time.append(dt);
        else: acquisition_date_and_time=[None,None]
        data_O = [];
        component_names_all = [];
        # get sample names
        if sample_names_I and sample_types_I and len(sample_types_I)==1:
            sample_names = sample_names_I;
            sample_types = [sample_types_I[0] for sn in sample_names];
        else:
            sample_names = [];
            sample_types = [];
            for st in sample_types_I:
                sample_names_tmp = [];
                sample_names_tmp = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleType(experiment_id_I,st);
                sample_names.extend(sample_names_tmp);
                sample_types_tmp = [];
                sample_types_tmp = [st for sn in sample_names_tmp];
                sample_types.extend(sample_types_tmp);
        for sn in sample_names:
            print 'analyzing peakInformation for sample_name ' + sn;
            # get sample description
            desc = {};
            desc = self.stage01_quantification_query.get_description_experimentIDAndSampleID_sampleDescription(experiment_id_I,sn);
            # get component names
            if component_names_I:
                component_names = component_names_I;
            else:
                component_names = [];
                component_names = self.stage01_quantification_query.get_componentsNames_experimentIDAndSampleName(experiment_id_I,sn);
            component_names_all.extend(component_names);
            for cn in component_names:
                # get rt, height, s/n
                sst_data = {};
                sst_data = self.stage01_quantification_query.get_peakInfo_sampleNameAndComponentName(sn,cn,acquisition_date_and_time);
                if sst_data:
                    tmp = {};
                    tmp.update(sst_data);
                    tmp.update(desc);
                    tmp.update({'sample_name':sn});
                    data_O.append(tmp);
        # Plot data over time
        if component_names_I:
            # use input order
            component_names_unique = component_names_I;
        else:
            # use alphabetical order
            component_names_unique = list(set(component_names_all));
            component_names_unique.sort();
        if plot_type_I == 'single':
            for cn in component_names_unique:
                data_parameters = {};
                data_parameters_stats = {};
                for parameter in peakInfo_I:
                    data_parameters[parameter] = [];
                    acquisition_date_and_times = [];
                    acquisition_date_and_times_hrs = [];
                    sample_names_parameter = [];
                    sample_types_parameter = [];
                    component_group_name = None;
                    for sn_cnt,sn in enumerate(sample_names):
                        for d in data_O:
                            if d['sample_name'] == sn and d['component_name'] == cn and d[parameter]:
                                data_parameters[parameter].append(d[parameter]);
                                acquisition_date_and_times.append(d['acquisition_date_and_time'])
                                acquisition_date_and_times_hrs.append(d['acquisition_date_and_time'].year*8765.81277 + d['acquisition_date_and_time'].month*730.484  + d['acquisition_date_and_time'].day*365.242 + d['acquisition_date_and_time'].hour + d['acquisition_date_and_time'].minute / 60. + d['acquisition_date_and_time'].second / 3600.); #convert using datetime object
                                sample_names_parameter.append(sn);
                                sample_types_parameter.append(sample_types[sn_cnt])
                                component_group_name = d['component_group_name'];
                    # normalize time
                    acquisition_date_and_times_hrs.sort();
                    t_start = min(acquisition_date_and_times_hrs);
                    for t_cnt,t in enumerate(acquisition_date_and_times_hrs):
                        if y_data_type_I == 'acquisition_date_and_time':acquisition_date_and_times_hrs[t_cnt] = t - t_start;
                        elif y_data_type_I == 'count':acquisition_date_and_times_hrs[t_cnt] = t_cnt;
                    title = cn + '\n' + parameter;
                    filename = 'data/_output/' + experiment_id_I + '_' + cn + '_' + parameter + '.png'
                    self.matplot.scatterLinePlot(title,x_title_I,y_title_I,acquisition_date_and_times_hrs,data_parameters[parameter],fit_func_I='lowess',show_eqn_I=False,show_r2_I=False,filename_I=filename,show_plot_I=False);
        if plot_type_I == 'multiple':
             for parameter in peakInfo_I:
                data_parameters = [];
                acquisition_date_and_times = [];
                acquisition_date_and_times_hrs = [];
                sample_names_parameter = [];
                sample_types_parameter = [];
                component_group_names = [];
                component_names = [];
                for cn_cnt,cn in enumerate(component_names_unique):
                    data = [];
                    acquisition_date_and_time = [];
                    acquisition_date_and_time_hrs = [];
                    sample_name_parameter = [];
                    sample_type_parameter = [];
                    for sn_cnt,sn in enumerate(sample_names):
                        for d in data_O:
                            if d['sample_name'] == sn and d['component_name'] == cn and d[parameter]:
                                data.append(d[parameter])
                                acquisition_date_and_time.append(d['acquisition_date_and_time'])
                                acquisition_date_and_time_hrs.append(d['acquisition_date_and_time'].year*8765.81277 + d['acquisition_date_and_time'].month*730.484  + d['acquisition_date_and_time'].day*365.242 + d['acquisition_date_and_time'].hour + d['acquisition_date_and_time'].minute / 60. + d['acquisition_date_and_time'].second / 3600.); #convert using datetime object
                                sample_name_parameter.append(sn);
                                sample_type_parameter.append(sample_types[sn_cnt])
                                if sn_cnt == 0:
                                    component_group_names.append(d['component_group_name']);
                                    component_names.append(d['component_name']);
                    # normalize time
                    acquisition_date_and_time_hrs.sort();
                    t_start = min(acquisition_date_and_time_hrs);
                    for t_cnt,t in enumerate(acquisition_date_and_time_hrs):
                        if y_data_type_I == 'acquisition_date_and_time':acquisition_date_and_time_hrs[t_cnt] = t - t_start;
                        elif y_data_type_I == 'count':acquisition_date_and_time_hrs[t_cnt] = t_cnt;
                    data_parameters.append(data);
                    acquisition_date_and_times.append(acquisition_date_and_time)
                    acquisition_date_and_times_hrs.append(acquisition_date_and_time_hrs);
                    sample_names_parameter.append(sample_name_parameter);
                    sample_types_parameter.append(sample_type_parameter)
                title = parameter;
                filename = 'data/_output/' + experiment_id_I + '_' + parameter + '.eps'
                self.matplot.multiScatterLinePlot(title,x_title_I,y_title_I,acquisition_date_and_times_hrs,data_parameters,data_labels_I=component_group_names,fit_func_I=None,show_eqn_I=False,show_r2_I=False,filename_I=filename,show_plot_I=False);
    def execute_scatterLinePlot_peakResolution(self,experiment_id_I,sample_names_I=[],sample_types_I=['Standard'],component_name_pairs_I=[],
                            peakInfo_I = ['rt_dif','resolution'],
                            acquisition_date_and_time_I=[None,None],
                            x_title_I='Time [hrs]',y_title_I='Retention Time [min]',y_data_type_I='acquisition_date_and_time',
                            plot_type_I='single'):
        '''Analyze resolution for critical pairs'''
        #Input:
        #   experiment_id_I
        #   sample_names_I
        #   sample_types_I
        #   component_name_pairs_I = [[component_name_1,component_name_2],...]
        #   acquisition_date_and_time_I = ['%m/%d/%Y %H:%M','%m/%d/%Y %H:%M']

        print 'execute_peakInformation_resolution...'
        #convert string date time to datetime
        # e.g. time.strptime('4/15/2014 15:51','%m/%d/%Y %H:%M')
        acquisition_date_and_time = [];
        if acquisition_date_and_time_I[0] and acquisition_date_and_time_I[1]:
            for dateandtime in acquisition_date_and_time_I:
                time_struct = strptime(dateandtime,'%m/%d/%Y %H:%M')
                dt = datetime.fromtimestamp(mktime(time_struct))
                acquisition_date_and_time.append(dt);
        else: acquisition_date_and_time=[None,None]
        data_O = [];
        component_names_pairs_all = [];
        # get sample names
        if sample_names_I and sample_types_I and len(sample_types_I)==1:
            sample_names = sample_names_I;
            sample_types = [sample_types_I[0] for sn in sample_names];
        else:
            sample_names = [];
            sample_types = [];
            for st in sample_types_I:
                sample_names_tmp = [];
                sample_names_tmp = self.stage01_quantification_query.get_sampleNames_experimentIDAndSampleType(experiment_id_I,st);
                sample_names.extend(sample_names_tmp);
                sample_types_tmp = [];
                sample_types_tmp = [st for sn in sample_names_tmp];
                sample_types.extend(sample_types_tmp);
        for sn in sample_names:
            print 'analyzing peakInformation for sample_name ' + sn;
            for component_name_pair in component_name_pairs_I:
                # get critical pair data
                cpd1 = {};
                cpd2 = {};
                cpd1 = self.stage01_quantification_query.get_peakInfo_sampleNameAndComponentName(sn,component_name_pair[0],acquisition_date_and_time);
                cpd2 = self.stage01_quantification_query.get_peakInfo_sampleNameAndComponentName(sn,component_name_pair[1],acquisition_date_and_time);
                # calculate the RT difference and resolution
                rt_dif = 0.0;
                rt_dif = abs(cpd1['retention_time']-cpd2['retention_time'])
                resolution = 0.0;
                resolution = rt_dif/(0.5*(cpd1['width_at_50']+cpd2['width_at_50']));
                # record data
                data_O.append({'component_name_pair':component_name_pair,
                               'rt_dif':rt_dif,
                               'resolution':resolution,
                               'component_group_name_pair':[cpd1['component_group_name'],cpd2['component_group_name']],
                               'sample_name':sn,
                               'acquisition_date_and_time':cpd1['acquisition_date_and_time']});
        if plot_type_I == 'single':
            for cnp in component_name_pairs_I:
                data_parameters = {};
                data_parameters_stats = {};
                for parameter in peakInfo_I:
                    data_parameters[parameter] = [];
                    acquisition_date_and_times = [];
                    acquisition_date_and_times_hrs = [];
                    sample_names_parameter = [];
                    sample_types_parameter = [];
                    component_group_name_pair = None;
                    for sn_cnt,sn in enumerate(sample_names):
                        for d in data_O:
                            if d['sample_name'] == sn and d['component_name_pair'] == cnp and d[parameter]:
                                data_parameters[parameter].append(d[parameter]);
                                acquisition_date_and_times.append(d['acquisition_date_and_time'])
                                acquisition_date_and_times_hrs.append(d['acquisition_date_and_time'].year*8765.81277 + d['acquisition_date_and_time'].month*730.484  + d['acquisition_date_and_time'].day*365.242 + d['acquisition_date_and_time'].hour + d['acquisition_date_and_time'].minute / 60. + d['acquisition_date_and_time'].second / 3600.); #convert using datetime object
                                sample_names_parameter.append(sn);
                                sample_types_parameter.append(sample_types[sn_cnt])
                                component_group_name_pair = d['component_group_name_pair'];
                    # normalize time
                    acquisition_date_and_times_hrs.sort();
                    t_start = min(acquisition_date_and_times_hrs);
                    for t_cnt,t in enumerate(acquisition_date_and_times_hrs):
                        if y_data_type_I == 'acquisition_date_and_time':acquisition_date_and_times_hrs[t_cnt] = t - t_start;
                        elif y_data_type_I == 'count':acquisition_date_and_times_hrs[t_cnt] = t_cnt;
                    title = cn + '\n' + parameter;
                    filename = 'data/_output/' + experiment_id_I + '_' + cn + '_' + parameter + '.png'
                    self.matplot.scatterLinePlot(title,x_title_I,y_title_I,acquisition_date_and_times_hrs,data_parameters[parameter],fit_func_I='lowess',show_eqn_I=False,show_r2_I=False,filename_I=filename,show_plot_I=False);
        if plot_type_I == 'multiple':
             for parameter in peakInfo_I:
                data_parameters = [];
                acquisition_date_and_times = [];
                acquisition_date_and_times_hrs = [];
                sample_names_parameter = [];
                sample_types_parameter = [];
                component_group_names_pair = [];
                component_names_pair = [];
                for cnp_cnt,cnp in enumerate(component_name_pairs_I):
                    data = [];
                    acquisition_date_and_time = [];
                    acquisition_date_and_time_hrs = [];
                    sample_name_parameter = [];
                    sample_type_parameter = [];
                    for sn_cnt,sn in enumerate(sample_names):
                        for d in data_O:
                            if d['sample_name'] == sn and d['component_name_pair'] == cnp and d[parameter]:
                                data.append(d[parameter])
                                acquisition_date_and_time.append(d['acquisition_date_and_time'])
                                acquisition_date_and_time_hrs.append(d['acquisition_date_and_time'].year*8765.81277 + d['acquisition_date_and_time'].month*730.484  + d['acquisition_date_and_time'].day*365.242 + d['acquisition_date_and_time'].hour + d['acquisition_date_and_time'].minute / 60. + d['acquisition_date_and_time'].second / 3600.); #convert using datetime object
                                sample_name_parameter.append(sn);
                                sample_type_parameter.append(sample_types[sn_cnt])
                                if sn_cnt == 0:
                                    component_group_names_pair.append(d['component_group_name_pair']);
                                    component_names_pair.append(d['component_name_pair']);
                    # normalize time
                    acquisition_date_and_time_hrs.sort();
                    t_start = min(acquisition_date_and_time_hrs);
                    for t_cnt,t in enumerate(acquisition_date_and_time_hrs):
                        if y_data_type_I == 'acquisition_date_and_time':acquisition_date_and_time_hrs[t_cnt] = t - t_start;
                        elif y_data_type_I == 'count':acquisition_date_and_time_hrs[t_cnt] = t_cnt;
                    data_parameters.append(data);
                    acquisition_date_and_times.append(acquisition_date_and_time)
                    acquisition_date_and_times_hrs.append(acquisition_date_and_time_hrs);
                    sample_names_parameter.append(sample_name_parameter);
                    sample_types_parameter.append(sample_type_parameter)
                # create data labels
                data_labels = [];
                for component_group_names in component_group_names_pair:
                    data_labels.append(component_group_names[0] + '/' + component_group_names[1]);
                title = parameter;
                filename = 'data/_output/' + experiment_id_I + '_' + parameter + '.eps'
                self.matplot.multiScatterLinePlot(title,x_title_I,y_title_I,acquisition_date_and_times_hrs,data_parameters,data_labels_I=data_labels,fit_func_I=None,show_eqn_I=False,show_r2_I=False,filename_I=filename,show_plot_I=False);
    
    def execute_boxAndWhiskersPlot_peakInformation(self,experiment_id_I,
                                                   peakInfo_parameter_I = ['height','retention_time','width_at_50','signal_2_noise'],
                                                   component_names_I=[]):
        '''generate a boxAndWhiskers plot from peakInformation table'''

        print 'execute_boxAndWhiskersPlot...'
        if peakInfo_parameter_I:
            peakInfo_parameter = peakInfo_parameter_I;
        else:
            peakInfo_parameter = [];
            peakInfo_parameter = self.stage01_quantification_query.get_peakInfoParameter_experimentID_dataStage01PeakInformation(experiment_id_I);
        for parameter in peakInfo_parameter:
            data_plot_mean = [];
            data_plot_cv = [];
            data_plot_ci = [];
            data_plot_parameters = [];
            data_plot_component_names = [];
            data_plot_data = [];
            data_plot_units = [];
            if component_names_I:
                component_names = component_names_I;
            else:
                component_names = [];
                component_names = self.stage01_quantification_query.get_componentNames_experimentIDAndPeakInfoParameter_dataStage01PeakInformation(experiment_id_I,parameter);
            for cn in component_names:
                print 'generating boxAndWhiskersPlot for component_name ' + cn; 
                # get the data 
                data = {};
                data = self.stage01_quantification_query.get_row_experimentIDAndPeakInfoParameterComponentName_dataStage01PeakInformation(experiment_id_I,parameter,cn)
                if data and data['peakInfo_ave']:
                    # record data for plotting
                    data_plot_mean.append(data['peakInfo_ave']);
                    data_plot_cv.append(data['peakInfo_cv']);
                    data_plot_ci.append([data['peakInfo_lb'],data['peakInfo_ub']]);
                    data_plot_data.append(data['peakInfo_data']);
                    data_plot_parameters.append(parameter);
                    data_plot_component_names.append(data['component_group_name']);
                    data_plot_units.append('Retention_time [min]');
            # visualize the stats:
            data_plot_se = [(x[1]-x[0])/2 for x in data_plot_ci]
            filename = 'data/_output/' + experiment_id_I + '_' + parameter + '.eps';
            self.matplot.boxAndWhiskersPlot(data_plot_parameters[0],data_plot_component_names,data_plot_units[0],'samples',data_plot_data,data_plot_mean,data_plot_ci,filename_I=filename,show_plot_I=False);
    def execute_boxAndWhiskersPlot_peakResolution(self,experiment_id_I,component_name_pairs_I=[],
                            peakInfo_parameter_I = ['rt_dif','resolution']):
        '''generate a boxAndWhiskers plot from peakResolution table'''

        print 'execute_boxAndWhiskersPlot...'
        if peakInfo_parameter_I:
            peakInfo_parameter = peakInfo_parameter_I;
        else:
            peakInfo_parameter = [];
            peakInfo_parameter = self.stage01_quantification_query.get_peakInfoParameter_experimentID_dataStage01PeakResolution(experiment_id_I);
        for parameter in peakInfo_parameter:
            data_plot_mean = [];
            data_plot_cv = [];
            data_plot_ci = [];
            data_plot_parameters = [];
            data_plot_component_names = [];
            data_plot_data = [];
            data_plot_units = [];
            if component_name_pairs_I:
                component_name_pairs = component_name_pairs_I;
            else:
                component_name_pairs = [];
                component_name_pairs = self.stage01_quantification_query.get_componentNamePairs_experimentIDAndPeakInfoParameter_dataStage01PeakResolution(experiment_id_I,parameter);
            for cn in component_name_pairs:
                # get the data 
                data = {};
                data = self.stage01_quantification_query.get_row_experimentIDAndPeakInfoParameterComponentName_dataStage01PeakResolution(experiment_id_I,parameter,cn)
                if data and data['peakInfo_ave']:
                    # record data for plotting
                    data_plot_mean.append(data['peakInfo_ave']);
                    data_plot_cv.append(data['peakInfo_cv']);
                    data_plot_ci.append([data['peakInfo_lb'],data['peakInfo_ub']]);
                    data_plot_data.append(data['peakInfo_data']);
                    data_plot_parameters.append(parameter);
                    data_plot_component_names.append(data['component_group_name_pair'][0]+'/'+data['component_group_name_pair'][0]);
                    data_plot_units.append('Retention_time [min]');
            # visualize the stats:
            data_plot_se = [(x[1]-x[0])/2 for x in data_plot_ci]
            filename = 'data/_output/' + experiment_id_I + '_' + parameter + '.eps';
            self.matplot.boxAndWhiskersPlot(data_plot_parameters[0],data_plot_component_names,data_plot_units[0],'samples',data_plot_data,data_plot_mean,data_plot_ci,filename_I=filename,show_plot_I=False);