from analysis.analysis_base import *
from stage01_quantification_query import stage01_quantification_query
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

class stage01_quantification_io(base_analysis):
    def __init__(self):
        self.session = Session();
        self.stage01_quantification_query = stage01_quantification_query();
    
    def export_dataStage01Replicates_csv(self, experiment_id_I, filename):
        '''export dataStage01Replicates to csv file'''
        # query the data
        data = [];
        query = stage01_quantification_query();
        data = query.get_data_experimentID_dataStage01Replicates(experiment_id_I);
        # expand the data file:
        sns = []
        cgn = []
        for d in data:
             sns.append(d['sample_name_short']);
             cgn.append(d['component_group_name']);
        sns_sorted = sorted(set(sns))
        cgn_sorted = sorted(set(cgn))
        concentrations = []
        for c in cgn_sorted:
             row = ['NA' for r in range(len(sns_sorted))];
             cnt = 0;
             for s in sns_sorted:
                 for d in data:
                     if d['sample_name_short'] == s and d['component_group_name'] == c:
                         if d['calculated_concentration']:
                            row[cnt] = d['calculated_concentration'];
                            break;
                 cnt = cnt+1
             concentrations.append(row);
        # write concentrations to file
        export = base_exportData(concentrations);
        export.write_headerAndColumnsAndElements2csv(sns_sorted,cgn_sorted,filename);

    def export_dataStage01ReplicatesMI_csv(self, experiment_id_I, filename):
        '''export dataStage01ReplicatesMI to csv file'''
        # query the data
        data = [];
        query = stage01_quantification_query();
        data = query.get_data_experimentID_dataStage01ReplicatesMI(experiment_id_I);
        # expand the data file:
        sns = []
        cgn = []
        for d in data:
             sns.append(d['sample_name_short']);
             cgn.append(d['component_group_name']);
        sns_sorted = sorted(set(sns))
        cgn_sorted = sorted(set(cgn))
        concentrations = []
        for c in cgn_sorted:
             row = ['NA' for r in range(len(sns_sorted))];
             cnt = 0;
             for s in sns_sorted:
                 for d in data:
                     if d['sample_name_short'] == s and d['component_group_name'] == c:
                         if d['calculated_concentration']:
                            row[cnt] = d['calculated_concentration'];
                            break;
                 cnt = cnt+1
             concentrations.append(row);
        # write concentrations to file
        export = base_exportData(concentrations);
        export.write_headerAndColumnsAndElements2csv(sns_sorted,cgn_sorted,filename);

    def export_dataStage01AveragesMI_json(self, experiment_id_I, sample_name_abbreviation_I, time_point_I, filename_I):
        '''export dataStage01AveragesMI to json file'''
        # query the data
        data = {};
        query = stage01_quantification_query();
        data = query.get_concentrations_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage01AveragesMI(experiment_id_I, sample_name_abbreviation_I, time_point_I);
        # write json to file
        with open(filename_I, 'wb') as outfile:
                json.dump(data, outfile, indent=4);

    def export_dataStage01AveragesMIgeo_json(self, experiment_id_I, sample_name_abbreviation_I, time_point_I, filename_I):
        '''export dataStage01AveragesMI to json file'''
        # query the data
        data = {};
        query = stage01_quantification_query();
        data = query.get_concentrations_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage01AveragesMIgeo(experiment_id_I, sample_name_abbreviation_I, time_point_I);
        # write json to file
        with open(filename_I, 'wb') as outfile:
                json.dump(data, outfile, indent=4);

    def import_quantitationMethod_add(self,QMethod_id_I, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_quantitationMethod(QMethod_id_I, data.data);
        data.clear_data();

    def add_quantitationMethod(self, QMethod_id_I, data_I):
        '''add rows of quantitation_method'''
        if data_I:
            for d in data_I:
                if not d['IS'] or d['IS'] == 'False': # ignore internal standards
                    try:
                        data_add = quantitation_method(QMethod_id_I,
                                                    d['Q1 Mass - 1'],
                                                    d['Q3 Mass - 1'],
                                                    d['Group Name'],
                                                    d['Name'],
                                                    d['IS Name'],
                                                    d['Regression Type'],
                                                    d['Regression Weighting'],
                                                    None,
                                                    None,
                                                    None,
                                                    d['Use Area'],
                                                    None,
                                                    None,
                                                    None);
                        self.session.add(data_add);
                    except SQLAlchemyError as e:
                        print(e);
            self.session.commit();

    def import_dataStage01MQResultsTable_add(self,filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01MQResultsTable(data.data);
        data.clear_data();

    def add_dataStage01MQResultsTable(self,data_I):
        '''add rows of data_stage01_quantification_MQResultsTable'''
        if data_I:
            cnt = 0;
            for d in data_I:
                try:
                    data_add = data_stage01_quantification_MQResultsTable(d['Index'],
                            d['Sample Index'],
                            d['Original Filename'],
                            d['Sample Name'],
                            d['Sample ID'],
                            d['Sample Comment'],
                            d['Sample Type'],
                            d['Acquisition Date & Time'],
                            d['Rack Number'],
                            d['Plate Number'],
                            d['Vial Number'],
                            d['Dilution Factor'],
                            d['Injection Volume'],
                            d['Operator Name'],
                            d['Acq. Method Name'],
                            d['IS'],
                            d['Component Name'],
                            d['Component Index'],
                            d['Component Comment'],
                            d['IS Comment'],
                            d['Mass Info'],
                            d['IS Mass Info'],
                            d['IS Name'],
                            d['Component Group Name'],
                            d['Conc. Units'],
                            d['Failed Query'],
                            d['IS Failed Query'],
                            d['Peak Comment'],
                            d['IS Peak Comment'],
                            d['Actual Concentration'],
                            d['IS Actual Concentration'],
                            d['Concentration Ratio'],
                            d['Expected RT'],
                            d['IS Expected RT'],
                            d['Integration Type'],
                            d['IS Integration Type'],
                            d['Area'],
                            d['IS Area'],
                            d['Corrected Area'],
                            d['IS Corrected Area'],
                            d['Area Ratio'],
                            d['Height'],
                            d['IS Height'],
                            d['Corrected Height'],
                            d['IS Corrected Height'],
                            d['Height Ratio'],
                            d['Area / Height'],
                            d['IS Area / Height'],
                            d['Corrected Area/Height'],
                            d['IS Corrected Area/Height'],
                            d['Region Height'],
                            d['IS Region Height'],
                            d['Quality'],
                            d['IS Quality'],
                            d['Retention Time'],
                            d['IS Retention Time'],
                            d['Start Time'],
                            d['IS Start Time'],
                            d['End Time'],
                            d['IS End Time'],
                            d['Total Width'],
                            d['IS Total Width'],
                            d['Width at 50%'],
                            d['IS Width at 50%'],
                            d['Signal / Noise'],
                            d['IS Signal / Noise'],
                            d['Baseline Delta / Height'],
                            d['IS Baseline Delta / Height'],
                            d['Modified'],
                            d['Relative RT'],
                            d['Used'],
                            d['Calculated Concentration'],
                            d['Accuracy'],
                            d['Comment'],
                            d['Use_Calculated_Concentration']);
                    self.session.add(data_add);
                    cnt = cnt + 1;
                    if cnt > 1000: 
                        self.session.commit();
                        cnt = 0;
                except IntegrityError as e:
                    print(e);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    
    def import_dataStage01MQResultsTable_update(self,filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01MQResultsTable(data.data);
        data.clear_data();

    def update_dataStage01MQResultsTable(self,data_I):
        '''update rows of data_stage01_quantification_MQResultsTable'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage01_quantification_MQResultsTable).filter(
                            data_stage01_quantification_MQResultsTable.component_name.like(d['Component Name']),
                            data_stage01_quantification_MQResultsTable.sample_name.like(d['Sample Name']),
                            data_stage01_quantification_MQResultsTable.acquisition_date_and_time == d['Acquisition Date & Time']).update(
                            {'index_':d['Index'],
                            'sample_index':d['Sample Index'],
                            'original_filename':d['Original Filename'],
                            'sample_name':d['Sample Name'],
                            'sample_id':d['Sample ID'],
                            'sample_comment':d['Sample Comment'],
                            'sample_type':d['Sample Type'],
                            'acquisition_date_and_time':d['Acquisition Date & Time'],
                            'rack_number':d['Rack Number'],
                            'plate_number':d['Plate Number'],
                            'vial_number':d['Vial Number'],
                            'dilution_factor':d['Dilution Factor'],
                            'injection_volume':d['Injection Volume'],
                            'operator_name':d['Operator Name'],
                            'acq_method_name':d['Acq. Method Name'],
                            'is_':d['IS'],
                            'component_name':d['Component Name'],
                            'component_index':d['Component Index'],
                            'component_comment':d['Component Comment'],
                            'is_comment':d['IS Comment'],
                            'mass_info':d['Mass Info'],
                            'is_mass':d['IS Mass Info'],
                            'is_name':d['IS Name'],
                            'component_group_name':d['Component Group Name'],
                            'conc_units':d['Conc. Units'],
                            'failed_query':d['Failed Query'],
                            'is_failed_query':d['IS Failed Query'],
                            'peak_comment':d['Peak Comment'],
                            'is_peak_comment':d['IS Peak Comment'],
                            'actual_concentration':d['Actual Concentration'],
                            'is_actual_concentration':d['IS Actual Concentration'],
                            'concentration_ratio':d['Concentration Ratio'],
                            'expected_rt':d['Expected RT'],
                            'is_expected_rt':d['IS Expected RT'],
                            'integration_type':d['Integration Type'],
                            'is_integration_type':d['IS Integration Type'],
                            'area':d['Area'],
                            'is_area':d['IS Area'],
                            'corrected_area':d['Corrected Area'],
                            'is_corrected_area':d['IS Corrected Area'],
                            'area_ratio':d['Area Ratio'],
                            'height':d['Height'],
                            'is_height':d['IS Height'],
                            'corrected_height':d['Corrected Height'],
                            'is_corrected_height':d['IS Corrected Height'],
                            'height_ratio':d['Height Ratio'],
                            'area_2_height':d['Area / Height'],
                            'is_area_2_height':d['IS Area / Height'],
                            'corrected_area2height':d['Corrected Area/Height'],
                            'is_corrected_area2height':d['IS Corrected Area/Height'],
                            'region_height':d['Region Height'],
                            'is_region_height':d['IS Region Height'],
                            'quality':d['Quality'],
                            'is_quality':d['IS Quality'],
                            'retention_time':d['Retention Time'],
                            'is_retention_time':d['IS Retention Time'],
                            'start_time':d['Start Time'],
                            'is_start_time':d['IS Start Time'],
                            'end_time':d['End Time'],
                            'is_end_time':d['IS End Time'],
                            'total_width':d['Total Width'],
                            'is_total_width':d['IS Total Width'],
                            'width_at_50':d['Width at 50%'],
                            'is_width_at_50':d['IS Width at 50%'],
                            'signal_2_noise':d['Signal / Noise'],
                            'is_signal_2_noise':d['IS Signal / Noise'],
                            'baseline_delta_2_height':d['Baseline Delta / Height'],
                            'is_baseline_delta_2_height':d['IS Baseline Delta / Height'],
                            'modified_':d['Modified'],
                            'relative_rt':d['Relative RT'],
                            'used_':d['Used'],
                            'calculated_concentration':d['Calculated Concentration'],
                            'accuracy_':d['Accuracy'],
                            'comment_':d['Comment'],
                            'use_calculated_concentration':d['Use_Calculated_Concentration']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01Normalized_update(self,filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01Normalized(data.data);
        data.clear_data();

    def update_dataStage01Normalized(self,dataListUpdated_I):
        # update the data_stage01_quantification_normalized
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_quantification_normalized).filter(
                        #data_stage01_quantification_normalized.id == d['id'],
                        data_stage01_quantification_normalized.experiment_id.like(d['experiment_id']),
                        data_stage01_quantification_normalized.sample_name.like(d['sample_name']),
                        data_stage01_quantification_normalized.component_name.like(d['component_name'])).update(		
                        {
                        #'experiment_id':d['experiment_id'],
                        #'sample_name':d['sample_name'],
                        #'sample_id':d['sample_id'],
                        #'component_group_name':d['component_group_name'],
                        #'component_name':d['component_name'],
                        'calculated_concentration':d['calculated_concentration'],
                        'calculated_concentration_units':d['calculated_concentration_units'],
                        'used_':d['used_'],
                        'comment_':d['comment_']},
                        synchronize_session=False);
                if data_update == 0:
                    print 'row not found.'
                    print d
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def import_dataStage01ReplicatesMI_update(self,filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01ReplicatesMI(data.data);
        data.clear_data();

    def update_dataStage01ReplicatesMI(self,dataListUpdated_I):
        # update the data_stage01_quantification_normalized
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_quantification_replicatesMI).filter(
                        data_stage01_quantification_replicatesMI.experiment_id.like(d['experiment_id']),
                        data_stage01_quantification_replicatesMI.sample_name_short.like(d['sample_name_short']),
                        data_stage01_quantification_replicatesMI.time_point.like(d['time_point']),
                        data_stage01_quantification_replicatesMI.component_name.like(d['component_name'])).update(		
                        {
                        'calculated_concentration':d['calculated_concentration'],
                        'calculated_concentration_units':d['calculated_concentration_units'],
                        'used_':d['used_']},
                        synchronize_session=False);
                if data_update == 0:
                    print 'row not found.'
                    print d
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def import_dataStage01physiologicalRatiosReplicates_add(self,filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01physiologicalRatiosReplicates(data.data);
        data.clear_data();

    def add_dataStage01physiologicalRatiosReplicates(self,data_I):
        '''add rows of data_stage01_quantification_physiologicalRatio_replicates'''
        if data_I:
            cnt = 0;
            for d in data_I:
                try:
                    data_add = data_stage01_physiologicalRatios_replicates(d['experiment_id'],
                            d['sample_name_short'],
                            d['time_point'],
                            d['physiologicalratio_id'],
                            d['physiologicalratio_name'],
                            d['physiologicalratio_value'],
                            d['physiologicalratio_description'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                    cnt = cnt + 1;
                    if cnt > 1000: 
                        self.session.commit();
                        cnt = 0;
                except IntegrityError as e:
                    print(e);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    
    def import_dataStage01physiologicalRatiosReplicates_update(self,filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01physiologicalRatiosReplicates(data.data);
        data.clear_data();

    def update_dataStage01physiologicalRatiosReplicates(self,data_I):
        '''update rows of data_stage01_physiologicalRatios_replicates'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage01_physiologicalRatios_replicates).filter(
                            data_stage01_physiologicalRatios_replicates.id == d['id']).update(
                            {'experiment_id':d['experiment_id'],
                                    'sample_name_short':d['sample_name_short'],
                                    'time_point':d['time_point'],
                                    'physiologicalratio_id':d['physiologicalratio_id'],
                                    'physiologicalratio_name':d['physiologicalratio_name'],
                                    'physiologicalratio_value':d['physiologicalratio_value'],
                                    'physiologicalratio_description':d['physiologicalratio_description'],
                                    'used_':d['used_'],
                                    'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01physiologicalRatiosAverages_add(self,filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01physiologicalRatiosAverages(data.data);
        data.clear_data();

    def add_dataStage01physiologicalRatiosAverages(self,data_I):
        '''add rows of data_stage01_quantification_physiologicalRatio_averages'''
        if data_I:
            cnt = 0;
            for d in data_I:
                try:
                    data_add = data_stage01_physiologicalRatios_averages(d['experiment_id'],
                        d['sample_name_abbreviation'],
                        d['time_point'],
                        d['physiologicalratio_id'],
                        d['physiologicalratio_name'],
                        d['physiologicalratio_value_ave'],
                        d['physiologicalratio_value_cv'],
                        d['physiologicalratio_value_lb'],
                        d['physiologicalratio_value_ub'],
                        d['physiologicalratio_description'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                    cnt = cnt + 1;
                    if cnt > 1000: 
                        self.session.commit();
                        cnt = 0;
                except IntegrityError as e:
                    print(e);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    
    def import_dataStage01physiologicalRatiosAverages_update(self,filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01physiologicalRatiosAverages(data.data);
        data.clear_data();

    def update_dataStage01physiologicalRatiosAverages(self,data_I):
        '''update rows of data_stage01_physiologicalRatios_averages'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage01_physiologicalRatios_averages).filter(
                            data_stage01_physiologicalRatios_averages.id == d['id']).update(
                            {'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'physiologicalratio_id':d['physiologicalratio_id'],
                            'physiologicalratio_name':d['physiologicalratio_name'],
                            'physiologicalratio_value_ave':d['physiologicalratio_value_ave'],
                            'physiologicalratio_value_cv':d['physiologicalratio_value_cv'],
                            'physiologicalratio_value_lb':d['physiologicalratio_value_lb'],
                            'physiologicalratio_value_ub':d['physiologicalratio_value_ub'],
                            'physiologicalratio_description':d['physiologicalratio_description'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_dataStage01physiologicalRatios_d3(self, experiment_id,sample_name_abbreviations_I=[], time_points_I=[],ratios_I=[],
                                                 time_course_I=False,
                                                 json_var_name='data',
                                                 filename=[settings.visualization_data,'/quantification/boxandwhiskers/','ratios/']):
        '''Export data for viewing using d3'''
        #Input:
        #   experiment_id
        #Output:
        #   menu for sna, tp, ratio based on index menu
        
        print 'Exporting physiologicalRatios for d3 boxandwhiskers plot'
        data_all_O = [];
        filter_O = {};
        filter_O['time_point'] = [];
        filter_O['feature'] = [];
        if time_course_I:
            # get physiological ratio_ids
            ratios = {};
            ratios = self.stage01_quantification_query.get_ratioIDs_experimentID_dataStage01PhysiologicalRatiosReplicates(experiment_id);
            record_tp=True;
            for k,v in ratios.iteritems():
                print 'exporting physiologicalRatios from replicates for ratio ' + k;
                # get time points
                if time_points_I:
                    time_points = time_points_I;
                else:
                    time_points = [];
                    time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndRatioID_dataStage01PhysiologicalRatiosReplicates(experiment_id,k);
                data_O = [];
                labels_O = {};
                labels_O['labels']=[];
                condition_cnt = 0;
                for tp_cnt,tp in enumerate(time_points):
                    print 'exporting physiologicalRatios from replicates for time_point ' + tp;
                    # get sample_names
                    if sample_name_abbreviations_I:
                        sample_name_abbreviations = sample_name_abbreviations_I;
                    else:
                        sample_name_abbreviations = [];
                        sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndRatioID_dataStage01PhysiologicalRatiosAverages(experiment_id,tp,k);
                    for sna_cnt,sna in enumerate(sample_name_abbreviations):
                        print 'exporting physiologicalRatios from replicates for sample name abbreviation ' + sna;
                        # get sample names short
                        sample_names_short = [];
                        sample_names_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndRatioIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(experiment_id,sna,k,tp);
                        for sns_cnt,sns in enumerate(sample_names_short):
                            # get ratios
                            ratio = None;
                            ratio = self.stage01_quantification_query.get_ratio_experimentIDAndSampleNameShortAndTimePointAndRatioID_dataStage01PhysiologicalRatiosReplicates(experiment_id,sns,tp,k);
                            if not ratio: continue;
                            data_tmp = {};
                            data_tmp['condition'] = condition_cnt;
                            data_tmp['replicate'] = sns_cnt;
                            data_tmp['value'] = ratio;
                            data_O.append(data_tmp);
                        labels_O['labels'].append(sna);
                        condition_cnt+=1;
                if record_tp:
                    filter_tp_str = 'time_point/'+','.join(time_points);
                    filter_O['time_point'].append(filter_tp_str);
                    record_tp=False;
                filter_f_str = 'time_point/'+','.join(time_points)+'/feature/'+k;
                filter_O['feature'].append(filter_f_str);
                # initialize js variables
                json_O = {};
                options_O = {};
                options_O['x_axis_label'] = 'ratio';
                options_O['y_axis_label'] = 'sample';
                options_O['value_label'] = 'ratio';
                # assign data to the js variables
                json_O['data']=data_O;
                json_O.update(labels_O);
                json_O['options'] = options_O;
                # dump the data to a json file
                json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
                filename_str = filename[0] + '/' + experiment_id + filename[1] + filename[2] + ','.join(time_points) + '_' + k + '.js';
                with open(filename_str,'w') as file:
                    file.write(json_str);
            # dump the filter data to a json file
            json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
            filename_str = filename[0]  + '/' + experiment_id + filename[1] + filename[2] + 'filter.js'
            with open(filename_str,'w') as file:
                file.write(json_str);
        else:
            # get time points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage01_quantification_query.get_timePoint_experimentID_dataStage01PhysiologicalRatiosReplicates(experiment_id);
            for tp in time_points:
                print 'exporting physiologicalRatios from replicates for time_point ' + tp;
                filter_tp_str = 'time_point/'+tp;
                filter_O['time_point'].append(filter_tp_str);
                # get physiological ratio_ids
                ratios = {};
                ratios = self.stage01_quantification_query.get_ratioIDs_experimentIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(experiment_id,tp);
                for k,v in ratios.iteritems():
                    filter_f_str = 'time_point/'+tp+'/feature/'+k;
                    filter_O['feature'].append(filter_f_str);
                    data_O = [];
                    print 'exporting physiologicalRatios from replicates for ratio ' + k;
                    # get sample_names
                    if sample_name_abbreviations_I:
                        sample_name_abbreviations = sample_name_abbreviations_I;
                    else:
                        sample_name_abbreviations = [];
                        sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndRatioID_dataStage01PhysiologicalRatiosAverages(experiment_id,tp,k);
                    for sna_cnt,sna in enumerate(sample_name_abbreviations):
                        print 'exporting physiologicalRatios from replicates for sample name abbreviation ' + sna;
                        # get sample names short
                        sample_names_short = [];
                        sample_names_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndRatioIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(experiment_id,sna,k,tp);
                        for sns_cnt,sns in enumerate(sample_names_short):
                            # get ratios
                            ratio = None;
                            ratio = self.stage01_quantification_query.get_ratio_experimentIDAndSampleNameShortAndTimePointAndRatioID_dataStage01PhysiologicalRatiosReplicates(experiment_id,sns,tp,k);
                            if not ratio: continue;
                            data_tmp = {};
                            data_tmp['condition'] = sna_cnt;
                            data_tmp['replicate'] = sns_cnt;
                            data_tmp['value'] = ratio;
                            data_O.append(data_tmp)
                    # initialize js variables
                    json_O = {};
                    options_O = {};
                    options_O['x_axis_label'] = 'ratio';
                    options_O['y_axis_label'] = 'sample';
                    options_O['value_label'] = 'ratio';
                    labels_O = {};
                    labels_O['labels']=sample_name_abbreviations;
                    # assign data to the js variables
                    json_O['data']=data_O;
                    json_O.update(labels_O);
                    json_O['options'] = options_O;
                    # dump the data to a json file
                    json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
                    filename_str = filename[0] + '/' + experiment_id + filename[1] + filename[2] + tp + '_' + k + '.js';
                    with open(filename_str,'w') as file:
                        file.write(json_str);
            # dump the filter data to a json file
            json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
            filename_str = filename[0]  + '/' + experiment_id + filename[1] + filename[2] + 'filter.js'
            with open(filename_str,'w') as file:
                file.write(json_str);

    def export_dataStage01replicatesMI_d3(self, experiment_id,sample_name_abbreviations_I=[], time_points_I=[],component_names_I=[],
                                                 time_course_I=False,
                                                 json_var_name='data',
                                                 filename=[settings.visualization_data,'/quantification/boxandwhiskers/','concentrations/']):
        '''Export data for viewing using d3'''
        
        print 'Exporting replicatesMI for d3 boxandwhiskers plot'
        data_all_O = [];
        filter_O = {};
        filter_O['time_point'] = [];
        filter_O['feature'] = [];
        if time_course_I:
            # get component_names
            if component_names_I:
                component_names = component_names_I;
            else:
                component_names = [];
                component_names = self.stage01_quantification_query.get_componentNames_experimentID_dataStage01ReplicatesMI(experiment_id);
            record_tp=True;
            for cn in component_names:
                print 'exporting replicatesMI for component_name ' + cn;
                # get time points
                if time_points_I:
                    time_points = time_points_I;
                else:
                    time_points = [];
                    time_points = self.stage01_quantification_query.get_timePoint_experimentIDAndComponentName_dataStage01ReplicatesMI(experiment_id,cn);
                data_O = [];
                labels_O = {};
                labels_O['labels']=[];
                condition_cnt = 0;
                for tp in time_points:
                    print 'exporting replicatesMI for time_point ' + tp;
                    # get sample_names
                    if sample_name_abbreviations_I:
                        sample_name_abbreviations = sample_name_abbreviations_I;
                    else:
                        sample_name_abbreviations = [];
                        sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id,tp,cn);
                    for sna_cnt,sna in enumerate(sample_name_abbreviations):
                        print 'exporting replicatesMI  for sample name abbreviation ' + sna;
                        # get sample names short
                        sample_names_short = [];
                        sample_names_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndComponentNameAndTimePoint_dataStage01ReplicatesMI(experiment_id,sna,cn,tp);
                        concentrations = [];
                        for sns_cnt,sns in enumerate(sample_names_short):
                            # get concentrations
                            concentration, units = None, None;
                            concentration, units = self.stage01_quantification_query.get_concAndConcUnits_experimentIDAndSampleNameShortAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id,sns,tp,cn);
                            if not concentration: continue;
                            data_tmp = {};
                            data_tmp['condition'] = condition_cnt;
                            data_tmp['replicate'] = sns_cnt;
                            data_tmp['value'] = concentration;
                            concentrations.append(concentration);
                            data_O.append(data_tmp)
                        condition_cnt+=1;
                        labels_O['labels'].append(sna + ' ' + '[' + units + ']');
                if record_tp:
                    filter_tp_str = 'time_point/'+','.join(time_points);
                    filter_O['time_point'].append(filter_tp_str);
                    record_tp=False;
                filter_f_str = 'time_point/'+','.join(time_points)+'/feature/'+cn;
                filter_O['feature'].append(filter_f_str);
                # initialize js variables
                json_O = {};
                options_O = {};
                options_O['row_axis_label'] = 'concentration';
                options_O['col_axis_label'] = 'sample';
                options_O['value_label'] = units;
                # assign data to the js variables
                json_O['data']=data_O;
                json_O.update(labels_O);
                json_O['options'] = options_O;
                # dump the data to a json file
                json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
                filename_str = filename[0]  + '/' + experiment_id + filename[1] + filename[2]+ ','.join(time_points) + '_' + cn + '.js';
                with open(filename_str,'w') as file:
                    file.write(json_str);
            # dump the filter data to a json file
            json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
            filename_str = filename[0]  + '/' + experiment_id + filename[1] + filename[2] + 'filter.js'
            with open(filename_str,'w') as file:
                file.write(json_str);
        else:
            # get time points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage01_quantification_query.get_timePoint_experimentID_dataStage01ReplicatesMI(experiment_id);
            for tp in time_points:
                print 'exporting replicatesMI for time_point ' + tp;
                filter_tp_str = 'time_point/'+tp;
                filter_O['time_point'].append(filter_tp_str);
                # get component_names
                if component_names_I:
                    component_names = component_names_I;
                else:
                    component_names = [];
                    component_names = self.stage01_quantification_query.get_componentNames_experimentIDAndTimePoint_dataStage01ReplicatesMI(experiment_id,tp);
                for cn in component_names:
                    filter_f_str = 'time_point/'+tp+'/feature/'+cn;
                    filter_O['feature'].append(filter_f_str);
                    data_O = [];
                    print 'exporting replicatesMI for component_name ' + cn;
                    # get sample_names
                    if sample_name_abbreviations_I:
                        sample_name_abbreviations = sample_name_abbreviations_I;
                    else:
                        sample_name_abbreviations = [];
                        sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id,tp,cn);
                    for sna_cnt,sna in enumerate(sample_name_abbreviations):
                        print 'exporting replicatesMI  for sample name abbreviation ' + sna;
                        # get sample names short
                        sample_names_short = [];
                        sample_names_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndComponentNameAndTimePoint_dataStage01ReplicatesMI(experiment_id,sna,cn,tp);
                        concentrations = [];
                        for sns_cnt,sns in enumerate(sample_names_short):
                            # get concentrations
                            concentration, units = None, None;
                            concentration, units = self.stage01_quantification_query.get_concAndConcUnits_experimentIDAndSampleNameShortAndTimePointAndComponentName_dataStage01ReplicatesMI(experiment_id,sns,tp,cn);
                            if not concentration: continue;
                            data_tmp = {};
                            data_tmp['condition'] = sna_cnt;
                            data_tmp['replicate'] = sns_cnt;
                            data_tmp['value'] = concentration;
                            concentrations.append(concentration);
                            data_O.append(data_tmp)
                    # initialize js variables
                    json_O = {};
                    options_O = {};
                    options_O['row_axis_label'] = 'concentration';
                    options_O['col_axis_label'] = 'sample';
                    options_O['value_label'] = units;
                    labels_O = {};
                    #labels_tmp = [sna + '\n' + '[' + units + ']' for sna in sample_name_abbreviations];
                    labels_tmp = [sna + ' ' + '[' + units + ']' for sna in sample_name_abbreviations];
                    labels_O['labels']=labels_tmp;
                    # assiggn data to the js variables
                    json_O['data']=data_O;
                    json_O.update(labels_O);
                    json_O['options'] = options_O;
                    # dump the data to a json file
                    json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
                    filename_str = filename[0]  + '/' + experiment_id + filename[1] + filename[2]+ tp + '_' + cn + '.js';
                    with open(filename_str,'w') as file:
                        file.write(json_str);
            # dump the filter data to a json file
            json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
            filename_str = filename[0]  + '/' + experiment_id + filename[1] + filename[2] + 'filter.js'
            with open(filename_str,'w') as file:
                file.write(json_str);
            
    def export_dataStage01physiologicalRatios2_d3(self, experiment_id,sample_name_abbreviations_I=[], time_points_I=[],ratios_I=[],
                                                 json_var_name='data',
                                                 filename=['visualization/data/','/quantification/scatterplot/','ratios/']):
        '''Export data for viewing using d3'''
        #Input:
        #   experiment_id
        #Output:
        #   menu for sna, tp, ratio based on index menu
        
        print 'Exporting physiologicalRatios for d3 boxandwhiskers plot'
        # get time points
        time_points = [];
        time_points = self.stage01_quantification_query.get_timePoint_experimentID_dataStage01PhysiologicalRatiosReplicates(experiment_id);
        data_all_O = [];
        filter_O = {};
        filter_O['time_point'] = [];
        filter_O['feature'] = [];
        for tp in time_points:
            print 'exporting physiologicalRatios from replicates for time_point ' + tp;
            filter_tp_str = 'time_point/'+tp;
            filter_O['time_point'].append(filter_tp_str);
            # get physiological ratio_ids
            ratios = {};
            ratios = self.stage01_quantification_query.get_ratioIDs_experimentIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(experiment_id,tp);
            for k,v in ratios.iteritems():
                filter_f_str = 'time_point/'+tp+'/feature/'+k;
                filter_O['feature'].append(filter_f_str);
                data_O = [];
                print 'exporting physiologicalRatios from replicates for ratio ' + k;
                # get sample_names
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage01_quantification_query.get_sampleNameAbbreviations_experimentIDAndTimePointAndRatioID_dataStage01PhysiologicalRatiosAverages(experiment_id,tp,k);
                for sna_cnt,sna in enumerate(sample_name_abbreviations):
                    print 'exporting physiologicalRatios from replicates for sample name abbreviation ' + sna;
                    # get sample names short
                    sample_names_short = [];
                    sample_names_short = self.stage01_quantification_query.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndRatioIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(experiment_id,sna,k,tp);
                    ratios = [];
                    for sns_cnt,sns in enumerate(sample_names_short):
                        # get ratios
                        ratio = None;
                        ratio = self.stage01_quantification_query.get_ratio_experimentIDAndSampleNameShortAndTimePointAndRatioID_dataStage01PhysiologicalRatiosReplicates(experiment_id,sns,tp,k);
                        if not ratio: continue;
                        data_tmp = {};
                        data_tmp['condition'] = sna_cnt;
                        data_tmp['replicate'] = sns_cnt;
                        data_tmp['value'] = ratio;
                        ratios.append(ratio);
                        data_O.append(data_tmp)
                    #n_replicates = len(ratios);
                    #ratio_average = 0.0;
                    #ratio_var = 0.0;
                    #ratio_cv = 0.0;
                    #ratio_lb = 0.0;
                    #ratio_ub = 0.0;
                    ## calculate average and CV of ratios
                    #if (not(ratios)): 
                    #    continue
                    #elif n_replicates<2: 
                    #    continue
                    #else: 
                    #    ratio_average,ratio_var,ratio_lb,ratio_ub = self.calculate.calculate_ave_var(ratios);
                    #    if (ratio_average <= 0): ratio_cv = 0;
                    #    else: ratio_cv = sqrt(ratio_var)/ratio_average*100; 
                    #data_all_O.append({'sample_name_abbreviation':sna,
                    #                'time_point':tp,
                    #                'ratio_values':ratios,
                    #                'ratio_average':ratio_average,
                    #                'ratio_var':ratio_var,
                    #                'ratio_cv':ratio_cv,
                    #                'ratio_lb':ratio_lb,
                    #                'ratio_ub':ratio_ub
                    #                });
                # initialize js variables
                json_O = {};
                options_O = {};
                options_O['x_axis_label'] = 'ratio';
                options_O['y_axis_label'] = 'sample';
                options_O['value_label'] = 'ratio';
                labels_O = {};
                labels_O['labels']=sample_name_abbreviations;
                # assiggn data to the js variables
                json_O['data']=data_O;
                json_O.update(labels_O);
                json_O['options'] = options_O;
                # dump the data to a json file
                json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
                filename_str = filename[0] + experiment_id + filename[1] + filename[2] + tp + '_' + k + '.js';
                with open(filename_str,'w') as file:
                    file.write(json_str);
        # dump the filter data to a json file
        json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
        filename_str = filename[0] + experiment_id + filename[1] + filename[2] + 'filter.js'
        with open(filename_str,'w') as file:
            file.write(json_str);