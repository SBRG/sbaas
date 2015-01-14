from analysis.analysis_base import *
from stage01_isotopomer_query import stage01_isotopomer_query

class stage01_isotopomer_io(base_analysis):
    
    def export_dataStage01Replicates_csv(self, experiment_id_I, filename):
        '''export dataStage01Replicates to csv file'''
        # query the data
        data = [];
        query = stage01_isotopomer_query();
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
                         if d['intensity']:
                            row[cnt] = d['intensity'];
                            break;
                 cnt = cnt+1
             concentrations.append(row);
        # write concentrations to file
        export = base_exportData(concentrations);
        export.write_headerAndColumnsAndElements2csv(sns_sorted,cgn_sorted,filename);
    def export_compareAveragesSpectrumToTheoretical(self, experiment_id_I, filename, sample_name_abbreviations_I=None,scan_types_I=None,met_ids_I = None):
        '''export a comparison of calculated spectrum to theoretical spectrum'''
        # query the data
        data = [];
        query = stage01_isotopomer_query();
        # get time points
        time_points = query.get_timePoint_experimentID_dataStage01Averages(experiment_id_I);
        for tp in time_points:
            print 'Reporting average precursor and product spectrum from isotopomer normalized for time-point ' + str(tp);
            if sample_name_abbreviations_I:
                sample_abbreviations = sample_name_abbreviations_I;
                # query sample types from sample name abbreviations and time-point from _dataStage01Averages
            else:
                # get sample names and sample name abbreviations
                sample_abbreviations = [];
                sample_types = ['Unknown','QC'];
                sample_types_lst = [];
                for st in sample_types:
                    sample_abbreviations_tmp = [];
                    sample_abbreviations_tmp = query.get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePoint_dataStage01Averages(experiment_id_I,st,tp);
                    sample_abbreviations.extend(sample_abbreviations_tmp);
                    sample_types_lst.extend([st for i in range(len(sample_abbreviations_tmp))]);
            for sna_cnt,sna in enumerate(sample_abbreviations):
                print 'Reporting average precursor and product spectrum from isotopomer normalized for sample name abbreviation ' + sna;
                # get the scan_types
                if scan_types_I:
                    scan_types = [];
                    scan_types_tmp = [];
                    scan_types_tmp = query.get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01Averages(experiment_id_I,tp,sna,sample_types_lst[sna_cnt]);
                    scan_types = [st for st in scan_types_tmp if st in scan_types_I];
                else:
                    scan_types = [];
                    scan_types = query.get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01Averages(experiment_id_I,tp,sna,sample_types_lst[sna_cnt]);
                for scan_type in scan_types:
                    print 'Reporting average precursor and product spectrum for scan type ' + scan_type
                    # met_ids
                    if not met_ids_I:
                        met_ids = [];
                        met_ids = query.get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanType_dataStage01Averages( \
                                experiment_id_I,sna,tp,sample_types_lst[sna_cnt],scan_type);
                    else:
                        met_ids = met_ids_I;
                    if not(met_ids): continue #no component information was found
                    for met in met_ids:
                        print 'Reporting average precursor and product spectrum for metabolite ' + met;
                        data_tmp = [];
                        data_tmp = query.get_dataPrecursorFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01Averages(\
                                experiment_id_I,sna,tp,sample_types_lst[sna_cnt],scan_type,met);
                        data.extend(data_tmp);
                        data_tmp = [];
                        data_tmp = query.get_dataProductFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01Averages(\
                                experiment_id_I,sna,tp,sample_types_lst[sna_cnt],scan_type,met);
                        data.extend(data_tmp);
        # write the comparison to file
        headerL1 = ['sample_name_abbreviation','time_point','met_id','fragment_formula','C_pos','scan_type','theoretical'] + ['' for i in range(49)]\
            + ['measured'] + ['' for i in range(49)]\
            + ['measured_cv'] + ['' for i in range(49)]\
            + ['abs_difference'] + ['' for i in range(49)];
        headerL2 = ['' for i in range(6)] + ['a' + str(i) for i in range(50)]\
            + ['a' + str(i) for i in range(50)]\
            + ['a' + str(i) for i in range(50)]\
            + ['a' + str(i) for i in range(50)];
        header = [];
        header.append(headerL1);
        header.append(headerL2);
        export = base_exportData(data);
        export.write_headersAndElements2csv(header,filename);
    def export_compareAveragesNormSumSpectrumToTheoretical(self, experiment_id_I, filename, sample_name_abbreviations_I=None,scan_types_I=None,met_ids_I = None):
        '''export a comparison of calculated spectrum to theoretical spectrum'''
        # query the data
        data = [];
        query = stage01_isotopomer_query();
        # get time points
        time_points = query.get_timePoint_experimentID_dataStage01AveragesNormSum(experiment_id_I);
        for tp in time_points:
            print 'Reporting average precursor and product spectrum from isotopomer normalized for time-point ' + str(tp);
            if sample_name_abbreviations_I:
                sample_abbreviations = sample_name_abbreviations_I;
                # query sample types from sample name abbreviations and time-point from data_stage01_isotopomer_normalized
            else:
                # get sample names and sample name abbreviations
                sample_abbreviations = [];
                sample_types = ['Unknown','QC'];
                sample_types_lst = [];
                for st in sample_types:
                    sample_abbreviations_tmp = [];
                    sample_abbreviations_tmp = query.get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePoint_dataStage01AveragesNormSum(experiment_id_I,st,tp);
                    sample_abbreviations.extend(sample_abbreviations_tmp);
                    sample_types_lst.extend([st for i in range(len(sample_abbreviations_tmp))]);
            for sna_cnt,sna in enumerate(sample_abbreviations):
                print 'Reporting average precursor and product spectrum from isotopomer normalized for sample name abbreviation ' + sna;
                # get the scan_types
                if scan_types_I:
                    scan_types = [];
                    scan_types_tmp = [];
                    scan_types_tmp = query.get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01AveragesNormSum(experiment_id_I,tp,sna,sample_types_lst[sna_cnt]);
                    scan_types = [st for st in scan_types_tmp if st in scan_types_I];
                else:
                    scan_types = [];
                    scan_types = query.get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01AveragesNormSum(experiment_id_I,tp,sna,sample_types_lst[sna_cnt]);
                for scan_type in scan_types:
                    print 'Reporting average precursor and product spectrum for scan type ' + scan_type
                    # met_ids
                    if not met_ids_I:
                        met_ids = [];
                        met_ids = query.get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanType_dataStage01AveragesNormSum( \
                                experiment_id_I,sna,tp,sample_types_lst[sna_cnt],scan_type);
                    else:
                        met_ids = met_ids_I;
                    if not(met_ids): continue #no component information was found
                    for met in met_ids:
                        print 'Reporting average precursor and product spectrum for metabolite ' + met;
                        data_tmp = [];
                        data_tmp = query.get_dataPrecursorFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01AveragesNormSum(\
                                experiment_id_I,sna,tp,sample_types_lst[sna_cnt],scan_type,met);
                        data.extend(data_tmp);
                        data_tmp = [];
                        data_tmp = query.get_dataProductFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01AveragesNormSum(\
                                experiment_id_I,sna,tp,sample_types_lst[sna_cnt],scan_type,met);
                        data.extend(data_tmp);
        # write the comparison to file
        headerL1 = ['sample_name_abbreviation','time_point','met_id','fragment_formula','C_pos','scan_type','theoretical'] + ['' for i in range(49)]\
            + ['measured'] + ['' for i in range(49)]\
            + ['measured_cv'] + ['' for i in range(49)]\
            + ['abs_difference'] + ['' for i in range(49)]\
            + ['average_accuracy'];
        headerL2 = ['' for i in range(6)] + ['a' + str(i) for i in range(50)]\
            + ['a' + str(i) for i in range(50)]\
            + ['a' + str(i) for i in range(50)]\
            + ['a' + str(i) for i in range(50)]\
            + [''];
        header = [];
        header.append(headerL1);
        header.append(headerL2);
        export = base_exportData(data);
        export.write_headersAndElements2csv(header,filename);

    def import_sample_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_sample(data.data);
        data.clear_data();

    def add_sample(self, data_I):
        '''add rows of sample'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample(d['sample_name'],
                            d['sample_type'],
                            d['calibrator_id'],
                            d['calibrator_level'],
                            d['sample_id'],
                            d['sample_dilution']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_sample_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_sample(data.data);
        data.clear_data();

    def update_sample(self,data_I):
        '''update rows of sample'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample).filter(
                            sample.sample_name.like(d['sample_name'])).update(
                            {'sample_type':d['sample_type'],
                            'calibrator_id':d['calibrator_id'],
                            'calibrator_level':d['calibrator_level'],
                            'sample_id':d['sample_id'],
                            'sample_dilution':d['sample_dilution']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_sampleDescription_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_sampleDescription(data.data);
        data.clear_data();

    def add_sampleDescription(self, data_I):
        '''add rows of sample_description'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample_description(d['sample_id'],
                            d['sample_name_short'],
                            d['sample_name_abbreviation'],
                            d['sample_date'],
                            d['time_point'],
                            d['sample_condition'],
                            d['extraction_method_id'],
                            d['biological_material'],
                            d['sample_description'],
                            d['sample_replicate'],
                            d['is_added'],
                            d['is_added_units'],
                            d['reconstitution_volume'],
                            d['reconstitution_volume_units'],
                            d['sample_replicate_biological'],
                            d['istechnical']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_samplePhysiologicalParameters_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_samplePhysiologicalParameters(data.data);
        data.clear_data();

    def add_samplePhysiologicalParameters(self, data_I):
        '''add rows of sample_physiologicalparameters'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample_physiologicalParameters(d['sample_id'],
                            d['growth_condition_short'],
                            d['growth_condition_long'],
                            d['media_short'],
                            d['media_long'],
                            d['isoxic'],
                            d['temperature'],
                            d['supplementation'],
                            d['od600'],
                            d['vcd'],
                            d['culture_density'],
                            d['culture_volume_sampled'],
                            d['cells'],
                            d['dcw'],
                            d['wcw'],
                            d['vcd_units'],
                            d['culture_density_units'],
                            d['culture_volume_sampled_units'],
                            d['dcw_units'],
                            d['wcw_units']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_sampleStorage_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_sampleStorage(data.data);
        data.clear_data();

    def add_sampleStorage(self, data_I):
        '''add rows of sample_storage'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample_storage(d['sample_id'],
                            d['sample_label'],
                            d['ph'],
                            d['box'],
                            d['pos']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_experiment_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_experiment(data.data);
        data.clear_data();

    def add_experiment(self, data_I):
        '''add rows of experiment'''
        if data_I:
            for d in data_I:
                try:
                    data_add = experiment(d['exp_type_id'],
                        d['id'],
                        d['sample_name'],
                        d['experimentor_id'],
                        d['extraction_method_id'],
                        d['acquisition_method_id'],
                        d['quantitation_method_id'],
                        d['internal_standard_id']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

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
                if d['IS'] == 'FALSE': # ignore internal standards
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
        '''add rows of data_stage01_isotopomer_MQResultsTable'''
        if data_I:
            cnt = 0;
            for d in data_I:
                try:
                    data_add = data_stage01_isotopomer_MQResultsTable(d['Index'],
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
        '''update rows of data_stage01_isotopomer_MQResultsTable'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage01_isotopomer_MQResultsTable).filter(
                            data_stage01_isotopomer_MQResultsTable.component_name.like(d['Component Name']),
                            data_stage01_isotopomer_MQResultsTable.sample_name.like(d['Sample Name'])).update(
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
                    if data_update == 0:
                        print 'row not found.'
                        print d;
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_peakData_add(self, filename, experiment_id, samplename, precursor_formula, met_id,
                            mass_units_I='Da',intensity_units_I='cps', scan_type_I='EPI', header_I=True):
        '''table adds'''
        data = base_importData();
        data.read_tab_fieldnames(filename,['Mass/Charge','Intensity'],header_I);
        #data.read_tab_fieldnames(filename,['mass','intensity','intensity_percent'],header_I);
        data.format_data();
        self.add_peakData(data.data, experiment_id, samplename, precursor_formula, met_id,
                          mass_units_I,intensity_units_I, scan_type_I);
        data.clear_data();

    def add_peakData(self, data_I, experiment_id, samplename, precursor_formula, met_id,
                          mass_units_I,intensity_units_I, scan_type_I):
        '''add rows of data_stage01_isotopomer_peakData'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_isotopomer_peakData(experiment_id,
                            samplename,
                            met_id,
                            precursor_formula,
                            d['Mass/Charge'],
                            #d['mass'],
                            mass_units_I,
                            d['Intensity'],
                            #d['intensity'],
                            intensity_units_I,
                            scan_type_I,
                            True);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_peakList_add(self, filename, experiment_id, samplename, precursor_formula, met_id,
                            mass_units_I='Da',intensity_units_I='cps', 
                            centroid_mass_units_I='Da', peak_start_units_I='Da',
                            peak_stop_units_I='Da', resolution_I=None, scan_type_I='EPI'):
        '''table adds'''
        data = base_importData();
        data.read_tab_fieldnames(filename,['mass','centroid_mass','intensity','peak_start','peak_end','width','intensity_percent']);
        data.format_data();
        self.add_peakList(data.data, experiment_id, samplename, met_id,
                          mass_units_I,intensity_units_I, scan_type_I);
        data.clear_data();

    def add_peakList(self, data_I, experiment_id, samplename, precursor_formula, met_id,
                            mass_units_I='Da',intensity_units_I='cps',
                            centroid_mass_units_I='Da', peak_start_units_I='Da',
                            peak_stop_units_I='Da', resolution_I=None, scan_type_I='EPI'):
        '''add rows of data_stage01_isotopomer_peakList'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_isotopomer_peakList(experiment_id,
                            samplename,
                            met_id,
                            precursor_formula,
                            d['mass'],
                            mass_units_I,
                            d['intensity'],
                            intensity_units_I,
                            d['centroid_mass'],
                            centroid_mass_units_I,
                            d['peak_start'],
                            peak_start_units_I,
                            d['peak_stop'],
                            peak_stop_units_I,
                            resolution_I,
                            scan_type_I);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01PeakSpectrum_add(self,filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01PeakSpectrum(data.data);
        data.clear_data();

    def add_dataStage01PeakSpectrum(self,data_I):
        '''add rows of data_stage01_isotopomer_peakSpectrum'''
        if data_I:
            #cnt = 0;
            for d in data_I:
                try:
                    data_add = data_stage01_isotopomer_peakSpectrum(d['experiment_id'],
                                    d['sample_name'],
                                    d['sample_name_abbreviation'],
                                    d['sample_type'],
                                    d['time_point'],
                                    d['replicate_number'],
                                    d['met_id'],
                                    d['precursor_formula'],
                                    d['precursor_mass'],
                                    d['product_formula'],
                                    d['product_mass'],
                                    d['intensity'],
                                    d['intensity_units'],
                                    d['intensity_corrected'],
                                    d['intensity_corrected_units'],
                                    d['intensity_normalized'],
                                    d['intensity_normalized_units'],
                                    d['intensity_theoretical'],
                                    d['abs_devFromTheoretical'],
                                    d['scan_type'],
                                    d['used_'],
                                    d['comment_']);
                    self.session.add(data_add);
                    #cnt = cnt + 1;
                    #if cnt > 1000: 
                    #    self.session.commit();
                    #    cnt = 0;
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01PeakSpectrum_update(self,filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01PeakSpectrum(data.data);
        data.clear_data();

    def update_dataStage01PeakSpectrum(self,dataListUpdated_I):
        # update the data_stage01_isotopomer_peakSpectrum
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_isotopomer_peakSpectrum).filter(
                        data_stage01_isotopomer_peakSpectrum.id == d['id']).update(
                        #data_stage01_isotopomer_peakSpectrum.experiment_id.like(d['experiment_id']),
                        #data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                        #data_stage01_isotopomer_peakSpectrum.time_point.like(d['time_point']),
                        #data_stage01_isotopomer_peakSpectrum.sample_type.like(d['sample_type']),
                        #data_stage01_isotopomer_peakSpectrum.replicate_number == d['replicate_number'],
                        #data_stage01_isotopomer_peakSpectrum.met_id.like(d['met_id']),
                        #data_stage01_isotopomer_peakSpectrum.precursor_formula.like(d['precursor_formula']),
                        #data_stage01_isotopomer_peakSpectrum.precursor_mass == d['precursor_mass'],
                        #data_stage01_isotopomer_peakSpectrum.product_formula.like(d['product_formula']),
                        #data_stage01_isotopomer_peakSpectrum.product_mass == d['product_mass']).update(		
                        {'intensity':d['intensity'],
                        'intensity_units':d['intensity_units'],
                        'intensity_corrected':d['intensity_corrected'],
                        'intensity_corrected_units':d['intensity_corrected_units'],
                        'intensity_normalized':d['intensity_normalized'],
                        'intensity_normalized_units':d['intensity_normalized_units'],
                        'scan_type':d['scan_type'],
                        'used_':d['used_'],
                        'comment_':d['comment_']},
                        synchronize_session=False);
                if data_update == 0:
                    print 'row not found.'
                    print d
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def import_dataStage01Normalized_update(self,filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01Normalized(data.data);
        data.clear_data();

    def update_dataStage01Normalized(self,dataListUpdated_I):
        # update the data_stage01_isotopomer_normalized
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_isotopomer_normalized).filter(
                        data_stage01_isotopomer_normalized.id == d['id']).update(
                        #data_stage01_isotopomer_normalized.experiment_id.like(d['experiment_id']),
                        #data_stage01_isotopomer_normalized.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                        #data_stage01_isotopomer_normalized.time_point.like(d['time_point']),
                        #data_stage01_isotopomer_normalized.dilution == d['dilution'],
                        #data_stage01_isotopomer_normalized.sample_type.like(d['sample_type']),
                        #data_stage01_isotopomer_normalized.replicate_number == d['replicate_number'],
                        #data_stage01_isotopomer_normalized.met_id.like(d['met_id']),
                        #data_stage01_isotopomer_normalized.fragment_formula.like(d['fragment_formula']),
                        #data_stage01_isotopomer_normalized.fragment_mass == d['fragment_mass']).update(		
                        {
                        'experiment_id':d['experiment_id'],
                        'sample_name_abbreviation':d['sample_name_abbreviation'],
                        'time_point':d['time_point'],
                        'dilution':d['dilution'],
                        'sample_type':d['sample_type'],
                        'replicate_number':d['replicate_number'],
                        'met_id':d['met_id'],
                        'fragment_formula':d['fragment_formula'],
                        'fragment_mass':d['fragment_mass'],
                        'intensity':d['intensity'],
                        'intensity_units':d['intensity_units'],
                        'intensity_corrected':d['intensity_corrected'],
                        'intensity_corrected_units':d['intensity_corrected_units'],
                        'intensity_normalized':d['intensity_normalized'],
                        'intensity_normalized_units':d['intensity_normalized_units'],
                        'scan_type':d['scan_type'],
                        'used_':d['used_'],
                        'comment_':d['comment_']},
                        synchronize_session=False);
                if data_update == 0:
                    print 'row not found.'
                    print d
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def import_dataStage01Normalized_updateUsedAndComment(self,filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.updateUsedAndComment_dataStage01Normalized(data.data);
        data.clear_data();

    def updateUsedAndComment_dataStage01Normalized(self,dataListUpdated_I):
        # update the data_stage01_isotopomer_normalized
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_isotopomer_normalized).filter(
                        data_stage01_isotopomer_normalized.experiment_id.like(d['experiment_id']),
                        data_stage01_isotopomer_normalized.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                        data_stage01_isotopomer_normalized.time_point.like(d['time_point']),
                        data_stage01_isotopomer_normalized.dilution == d['dilution'],
                        data_stage01_isotopomer_normalized.sample_type.like(d['sample_type']),
                        data_stage01_isotopomer_normalized.replicate_number == d['replicate_number'],
                        data_stage01_isotopomer_normalized.met_id.like(d['met_id']),
                        data_stage01_isotopomer_normalized.fragment_formula.like(d['fragment_formula']),
                        data_stage01_isotopomer_normalized.fragment_mass == d['fragment_mass'],
                        data_stage01_isotopomer_normalized.scan_type.like(d['scan_type'])).update(		
                        {
                        'used_':d['used_'],
                        'comment_':d['comment_']},
                        synchronize_session=False);
                if data_update == 0:
                    print 'row not found.'
                    print d
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def import_dataStage01Normalized_add(self,filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01Normalized(data.data);
        data.clear_data();

    def add_dataStage01Normalized(self,dataListUpdated_I):
        # add to data_stage01_isotopomer_normalized
        for d in dataListUpdated_I:
            try:
                data_update = data_stage01_isotopomer_normalized(d['experiment_id'],
                        d['sample_name_abbreviation'],
                        d['time_point'],
                        d['dilution'],
                        d['sample_type'],
                        d['replicate_number'],
                        d['met_id'],
                        d['fragment_formula'],
                        d['fragment_mass'],
                        d['intensity'],
                        d['intensity_units'],
                        d['intensity_corrected'],
                        d['intensity_corrected_units'],
                        d['intensity_normalized'],
                        d['intensity_normalized_units'],
                        d['scan_type'],
                        d['used_'],
                        d['comment_']);
                self.session.add(data_add);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def import_dataStage01Averages_updateUsedAndComment(self,filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01Averages_usedAndComment(data.data);
        data.clear_data();

    def update_dataStage01Averages_usedAndComment(self,dataListUpdated_I):
        # update used and comment fields of the data_stage01_isotopomer_averages
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_isotopomer_averages).filter(
                        data_stage01_isotopomer_averages.experiment_id.like(d['experiment_id']),
                        data_stage01_isotopomer_averages.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                        data_stage01_isotopomer_averages.time_point.like(d['time_point']),
                        data_stage01_isotopomer_averages.sample_type.like(d['sample_type']),
                        data_stage01_isotopomer_averages.met_id.like(d['met_id']),
                        data_stage01_isotopomer_averages.fragment_formula.like(d['fragment_formula']),
                        data_stage01_isotopomer_averages.fragment_mass == int(d['fragment_mass']),
                        data_stage01_isotopomer_averages.scan_type.like(d['scan_type'])
                        ).update(		
                        {
                        'used_':d['used_'],
                        'comment_':d['comment_']},
                        synchronize_session=False);
                if data_update == 0:
                    print 'row not found.'
                    print d
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def import_dataStage01AveragesNormSum_updateUsedAndComment(self,filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01AveragesNormSum_usedAndComment(data.data);
        data.clear_data();

    def update_dataStage01AveragesNormSum_usedAndComment(self,dataListUpdated_I):
        # update used and comment fields of the data_stage01_isotopomer_averagesNormSum
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_isotopomer_averagesNormSum).filter(
                        data_stage01_isotopomer_averagesNormSum.experiment_id.like(d['experiment_id']),
                        data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                        data_stage01_isotopomer_averagesNormSum.time_point.like(d['time_point']),
                        data_stage01_isotopomer_averagesNormSum.sample_type.like(d['sample_type']),
                        data_stage01_isotopomer_averagesNormSum.met_id.like(d['met_id']),
                        data_stage01_isotopomer_averagesNormSum.fragment_formula.like(d['fragment_formula']),
                        data_stage01_isotopomer_averagesNormSum.fragment_mass == int(d['fragment_mass']),
                        data_stage01_isotopomer_averagesNormSum.scan_type.like(d['scan_type'])
                        ).update(		
                        {
                        'used_':d['used_'],
                        'comment_':d['comment_']},
                        synchronize_session=False);
                if data_update == 0:
                    print 'row not found.'
                    print d
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();