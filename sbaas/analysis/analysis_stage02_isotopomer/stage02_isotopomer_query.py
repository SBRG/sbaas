from analysis.analysis_base import *

# intialize the session
query_session = Session();

class stage02_isotopomer_query(base_analysis):
    # Query data from ms_components
    def get_precursorFormulaAndProductFormulaAndCMapsAndPositions_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry precursor formulas for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = query_session.query(MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment,
                    MS_components.precursor_fragment_elements,
                    MS_components.product_fragment_elements).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment,
                    MS_components.precursor_fragment_elements,
                    MS_components.product_fragment_elements).all();
            data_O = {};
            if not component_names: exit('bad query result: get_precursorFormulaAndProductFormulaAndCMaps_metID');
            for cn in component_names:
                data_O[cn.product_formula] = {'fragment':cn.product_fragment,
                                              'fragment_elements':cn.product_fragment_elements};
                data_O[cn.precursor_formula] = {'fragment':cn.precursor_fragment,
                                              'fragment_elements':cn.precursor_fragment_elements};
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage01_isotopomer_averagesNormSum:
    # query time points from data_stage01_isotopomer_averagesNormSum:
    def get_timePoint_experimentID_dataStage01AveragesNormSum(self,experiment_id_I):
        '''Querry time points that are used from the experiment'''
        try:
            time_points = query_session.query(data_stage01_isotopomer_averagesNormSum.time_point).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.time_point).order_by(
                    data_stage01_isotopomer_averagesNormSum.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry time points that are used from the experiment and sample name abbreviation'''
        try:
            time_points = query_session.query(data_stage01_isotopomer_averagesNormSum.time_point).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.time_point).order_by(
                    data_stage01_isotopomer_averagesNormSum.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name abbreviations from data_stage01_isotopomer_averagesNormSum:
    def get_sampleNameAbbreviations_experimentIDAndSampleType_dataStage01AveragesNormSum(self,experiment_id_I,sample_type_I):
        '''Querry sample name abbreviations that are used from
        the experiment'''
        try:
            sample_name_abbreviations = query_session.query(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I)).group_by(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePoint_dataStage01AveragesNormSum(self,experiment_id_I,sample_type_I,time_point_I):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points'''
        try:
            sample_name_abbreviations = query_session.query(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I)).group_by(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    # query scan types from data_stage01_isotopomer_averagesNormSum
    def get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01AveragesNormSum(self,experiment_id_I,time_point_I,sample_name_abbreviations_I,sample_type_I):
        '''Querry scan types that are used from the experiment for specific time-points and sample name abbreviations'''
        try:
            scan_types = query_session.query(
                    data_stage01_isotopomer_averagesNormSum.scan_type).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviations_I)).group_by(
                    data_stage01_isotopomer_averagesNormSum.scan_type).order_by(
                    data_stage01_isotopomer_averagesNormSum.scan_type).all();
            scan_types_O = [];
            for st in scan_types:
                scan_types_O.append(st[0]);
            return scan_types_O;
        except SQLAlchemyError as e:
            print(e);
    # query met_ids  from data_stage01_isotopomer_averagesNormSum
    def get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanType_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I):
        '''Querry met ids that are used for the experiment, sample abbreviation, time point, scan type'''
        try:
            met_ids = query_session.query(data_stage01_isotopomer_averagesNormSum.met_id).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.met_id).order_by(
                    data_stage01_isotopomer_averagesNormSum.met_id.asc()).all();
            met_ids_O = [];
            if not(met_ids):
                print "no results found"
                print "experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I";
                print experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I;
            else:
                for cn in met_ids:
                    met_ids_O.append(cn[0]);
                return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query fragment formulas  from data_stage01_isotopomer_averagesNormSum
    def get_fragmentFormula_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanTypeAndMetID_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I,met_id_I):
        '''Querry fragments that are used for the experiment, sample abbreviation, time point, scan type, met id'''
        try:
            fragments = query_session.query(data_stage01_isotopomer_averagesNormSum.fragment_formula).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula).order_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.asc()).all();
            fragments_O = [];
            if not(fragments):
                print "no results found"
                print "experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I met_id_I";
                print experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I;
            else:
                for cn in fragments:
                    fragments_O.append(cn[0]);
                return fragments_O;
        except SQLAlchemyError as e:
            print(e);
    # query spectrum  from data_stage01_isotopomer_averagesNormSum
    def get_spectrum_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanTypeAndMetIDAndFragmentFormula_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I,met_id_I,fragment_formula_I):
        '''Querry fragments that are used for the experiment, sample abbreviation, time point, scan type, met id'''
        try:
            fragments = query_session.query(data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.n_replicates).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.like(fragment_formula_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.n_replicates).order_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_mass.asc()).all();
            fragment_mass_O = [];
            intensity_normalized_average_O = [];
            intensity_normalized_cv_O = [];
            intensity_normalized_n_O = [];
            if not(fragments):
                print "no results found"
                print "experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I met_id_I    fragment_forula_I";
                print experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I,fragment_forula_I;
            else:
                for cn in fragments:
                    fragment_mass_O.append(cn[0]);
                    intensity_normalized_average_O.append(cn[1]);
                    intensity_normalized_cv_O.append(cn[2]);
                    intensity_normalized_n_O.append(cn[3]);
                return intensity_normalized_average_O,intensity_normalized_cv_O,intensity_normalized_n_O;
        except SQLAlchemyError as e:
            print(e);
    # query normalized intensity from data_stage01_isotopomer_averagesNormSum
    def get_dataProductFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I, met_id_I):
        '''Querry peak data for a specific experiment_id, sample_name_abbreviation'''
        try:
            data = query_session.query(data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    MS_components.product_fragment,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.spectrum_accuracy,
                    data_stage01_isotopomer_averagesNormSum.scan_type).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.like(MS_components.product_formula),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(MS_components.met_id),
                    MS_components.ms_methodtype.like('tuning'),
                    data_stage01_isotopomer_averagesNormSum.used_,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.used_.is_(True),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.fragment_formula.like(MS_components.product_formula),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.met_id.like(MS_components.met_id)).group_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    MS_components.product_fragment,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.spectrum_accuracy,
                    data_stage01_isotopomer_averagesNormSum.scan_type).order_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.desc(),
                    data_stage01_isotopomer_averagesNormSum.fragment_mass.asc()).all();
            data_O = [];
            if not data:
                print('No normalized intensities found for the following:')
                print 'sample_name_abbreviation: ' + sample_name_abbreviation_I;
                return data_O;
            else:
                # algorithm will break there is no data for a0 mass and there are jumps in the a values (i.e. a0 to a2);
                fragment_formula = '';
                fragment_formula_old = '';
                data_cnt = len(data)-1;
                i = 0;
                while i <= data_cnt:
                    fragment_formula_old = data[i].fragment_formula;
                    row_key = [];
                    row_theoretical = [];
                    row_measured = [];
                    row_measured_cv = [];
                    row_measured_dif = [];
                    row_spectrum_accuracy = [];
                    row = [];
                    for a in range(50):
                        if i <= data_cnt:
                            fragment_formula = data[i].fragment_formula;
                            if fragment_formula == fragment_formula_old:
                                if a == 0:
                                    # add key columns
                                    row_key.append(sample_name_abbreviation_I);
                                    row_key.append(time_point_I);
                                    row_key.append(met_id_I);
                                    row_key.append(data[i].fragment_formula);
                                    row_key.append(str(data[i].product_fragment));
                                    row_key.append(data[i].scan_type);
                                    row_spectrum_accuracy.append(data[i].spectrum_accuracy);
                                    mass0 = data[i].fragment_mass
                                massi = data[i].fragment_mass;
                                massDif = massi-mass0;
                                # add a+0... information
                                if data[i].intensity_theoretical: theoretical = numpy.round(data[i].intensity_theoretical,3);
                                else: theoretical = data[i].intensity_theoretical;
                                row_theoretical.append(theoretical)
                                if data[i].intensity_normalized_average: measured = numpy.round(data[i].intensity_normalized_average,3);
                                else: measured = data[i].intensity_normalized_average;
                                row_measured.append(measured)
                                if data[i].intensity_normalized_cv: cv = numpy.round(data[i].intensity_normalized_cv,3);
                                else: cv = data[i].intensity_normalized_cv;
                                row_measured_cv.append(cv);
                                if data[i].abs_devFromTheoretical: dif = numpy.round(data[i].abs_devFromTheoretical,3)
                                else: dif = data[i].abs_devFromTheoretical;
                                row_measured_dif.append(dif)
                                i += 1;
                            else:
                                row_theoretical.append(None);
                                row_measured.append(None);
                                row_measured_cv.append(None);
                                row_measured_dif.append(None);
                        else:
                            row_theoretical.append(None);
                            row_measured.append(None);
                            row_measured_cv.append(None);
                            row_measured_dif.append(None);
                    row.extend(row_key);
                    row.extend(row_theoretical);
                    row.extend(row_measured);
                    row.extend(row_measured_cv);
                    row.extend(row_measured_dif);
                    row.extend(row_spectrum_accuracy);
                    data_O.append(row);
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_dataPrecursorFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I, met_id_I):
        '''Querry peak data for a specific experiment_id, sample_name_abbreviation'''
        try:
            data = query_session.query(data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    MS_components.precursor_fragment,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.spectrum_accuracy,
                    data_stage01_isotopomer_averagesNormSum.scan_type).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.like(MS_components.precursor_formula),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(MS_components.met_id),
                    MS_components.ms_methodtype.like('tuning'),
                    data_stage01_isotopomer_averagesNormSum.used_,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.used_.is_(True),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.fragment_formula.like(MS_components.precursor_formula),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.met_id.like(MS_components.met_id)).group_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    MS_components.precursor_fragment,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.spectrum_accuracy,
                    data_stage01_isotopomer_averagesNormSum.scan_type).order_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.desc(),
                    data_stage01_isotopomer_averagesNormSum.fragment_mass.asc()).all();
            data_O = [];
            if not data:
                print('No normalized intensities found for the following:')
                print 'sample_name_abbreviation: ' + sample_name_abbreviation_I;
                return data_O;
            else:
                # algorithm will break there is no data for a0 mass and there are jumps in the a values (i.e. a0 to a2);
                fragment_formula = '';
                fragment_formula_old = '';
                data_cnt = len(data)-1;
                i = 0;
                while i <= data_cnt:
                    fragment_formula_old = data[i].fragment_formula;
                    row_key = [];
                    row_theoretical = [];
                    row_measured = [];
                    row_measured_cv = [];
                    row_measured_dif = [];
                    row_spectrum_accuracy = [];
                    row = [];
                    for a in range(50):
                        if i <= data_cnt:
                            fragment_formula = data[i].fragment_formula;
                            if fragment_formula == fragment_formula_old:
                                if a == 0:
                                    # add key columns
                                    row_key.append(sample_name_abbreviation_I);
                                    row_key.append(time_point_I);
                                    row_key.append(met_id_I);
                                    row_key.append(data[i].fragment_formula);
                                    row_key.append(str(data[i].precursor_fragment));
                                    row_key.append(data[i].scan_type);
                                    row_spectrum_accuracy.append(data[i].spectrum_accuracy);
                                    mass0 = data[i].fragment_mass
                                massi = data[i].fragment_mass;
                                massDif = massi-mass0;
                                # add a+0... information
                                if data[i].intensity_theoretical: theoretical = numpy.round(data[i].intensity_theoretical,3);
                                else: theoretical = data[i].intensity_theoretical;
                                row_theoretical.append(theoretical)
                                if data[i].intensity_normalized_average: measured = numpy.round(data[i].intensity_normalized_average,3);
                                else: measured = data[i].intensity_normalized_average;
                                row_measured.append(measured)
                                if data[i].intensity_normalized_cv: cv = numpy.round(data[i].intensity_normalized_cv,3);
                                else: cv = data[i].intensity_normalized_cv;
                                row_measured_cv.append(cv);
                                if data[i].abs_devFromTheoretical: dif = numpy.round(data[i].abs_devFromTheoretical,3)
                                else: dif = data[i].abs_devFromTheoretical;
                                row_measured_dif.append(dif)
                                i += 1;
                            else:
                                row_theoretical.append(None);
                                row_measured.append(None);
                                row_measured_cv.append(None);
                                row_measured_dif.append(None);
                        else:
                            row_theoretical.append(None);
                            row_measured.append(None);
                            row_measured_cv.append(None);
                            row_measured_dif.append(None);
                    row.extend(row_key);
                    row.extend(row_theoretical);
                    row.extend(row_measured);
                    row.extend(row_measured_cv);
                    row.extend(row_measured_dif);
                    row.extend(row_spectrum_accuracy);
                    data_O.append(row);
                return data_O;
        except SQLAlchemyError as e:
            print(e);
            
    ## Query from data_stage01_physiology_ratesAverages:
    # query met_ids from data_stage01_physiology_ratesAverages
    def get_metID_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologyRatesAverages(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rate data by sample id and met id that are used from
        the experiment'''
        try:
            data = query_session.query(data_stage01_physiology_ratesAverages.sample_name_abbreviation,
                    data_stage01_physiology_ratesAverages.met_id).filter(
                    data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_ratesAverages.used_.is_(True),
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation.like(sample_name_abbreviation_I)).group_by(
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation,
                    data_stage01_physiology_ratesAverages.met_id).order_by(
                    data_stage01_physiology_ratesAverages.met_id.asc()).all();
            met_id_O = [];
            if data: 
                for d in data:
                    met_id_O.append(d.met_id);
            return met_id_O;
        except SQLAlchemyError as e:
            print(e);
    # query rate from data_stage01_physiology_ratesAverages
    def get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(self,experiment_id_I,sample_name_abbreviation_I,met_id_I):
        '''Querry rate data by sample id and met id that are used from
        the experiment'''
        try:
            data = query_session.query(data_stage01_physiology_ratesAverages.slope_average,
                    data_stage01_physiology_ratesAverages.intercept_average,
                    data_stage01_physiology_ratesAverages.rate_average,
                    data_stage01_physiology_ratesAverages.rate_lb,
                    data_stage01_physiology_ratesAverages.rate_ub,
                    data_stage01_physiology_ratesAverages.rate_units,
                    data_stage01_physiology_ratesAverages.rate_var).filter(
                    data_stage01_physiology_ratesAverages.met_id.like(met_id_I),
                    data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_ratesAverages.used_.is_(True),
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation.like(sample_name_abbreviation_I)).first();
            slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = None,None,None,None,None,None,None;
            if data: 
                slope_average, intercept_average,\
                    rate_average, rate_lb, rate_ub, rate_units, rate_var = data.slope_average, data.intercept_average,\
                    data.rate_average, data.rate_lb, data.rate_ub, data.rate_units, data.rate_var;
            return slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_isotopomer_simulation
    # query simulation_id
    def get_simulationID_experimentIDAndSampleNameAbbreviationsAndModelIDAndMappingID_dataStage02IsotopomerSimulation(self,experiment_id_I,sample_name_abbreviation_I,model_id_I,mapping_id_I):
        '''Querry model_ids for the sample_name_abbreviation that are used from the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_simulation.simulation_id).filter(
                    data_stage02_isotopomer_simulation.model_id.like(model_id_I),
                    data_stage02_isotopomer_simulation.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_simulation.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_simulation.used_.is_(True)).group_by(
                    data_stage02_isotopomer_simulation.simulation_id).order_by(
                    data_stage02_isotopomer_simulation.simulation_id.asc()).all();
            simulation_ids_O = [];
            if data: 
                for d in data:
                    simulation_ids_O.append(d.simulation_id);
            return simulation_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample_name_abbreviations from data_stage02_isotopomer_simulation
    def get_sampleNameAbbreviations_experimentID_dataStage02IsotopomerSimulation(self,experiment_id_I):
        '''Querry sample_name_abbreviations that are used from the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_simulation.sample_name_abbreviation).filter(
                    data_stage02_isotopomer_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_simulation.used_.is_(True)).group_by(
                    data_stage02_isotopomer_simulation.sample_name_abbreviation).order_by(
                    data_stage02_isotopomer_simulation.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndModelIDAndMappingID_dataStage02IsotopomerSimulation(self,experiment_id_I,model_id_I,mapping_id_I):
        '''Querry sample_name_abbreviations for the model_id and mapping that are used from the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_simulation.sample_name_abbreviation).filter(
                    data_stage02_isotopomer_simulation.model_id.like(model_id_I),
                    data_stage02_isotopomer_simulation.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_simulation.used_.is_(True)).group_by(
                    data_stage02_isotopomer_simulation.sample_name_abbreviation).order_by(
                    data_stage02_isotopomer_simulation.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    # query model_ids from data_stage02_isotopomer_simulation
    def get_modelID_experimentIDAndSampleNameAbbreviations_dataStage02IsotopomerSimulation(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry model_ids for the sample_name_abbreviation that are used from the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_simulation.model_id).filter(
                    data_stage02_isotopomer_simulation.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_simulation.used_.is_(True)).group_by(
                    data_stage02_isotopomer_simulation.model_id).order_by(
                    data_stage02_isotopomer_simulation.model_id.asc()).all();
            model_ids_O = [];
            if data: 
                for d in data:
                    model_ids_O.append(d.model_id);
            return model_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_modelID_experimentID_dataStage02IsotopomerSimulation(self,experiment_id_I):
        '''Querry model_ids that are used from the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_simulation.model_id).filter(
                    data_stage02_isotopomer_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_simulation.used_.is_(True)).group_by(
                    data_stage02_isotopomer_simulation.model_id).order_by(
                    data_stage02_isotopomer_simulation.model_id.asc()).all();
            model_ids_O = [];
            if data: 
                for d in data:
                    model_ids_O.append(d.model_id);
            return model_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query mapping_ids from data_stage02_isotopomer_simulation
    def get_mappingID_experimentIDAndSampleNameAbbreviationsAndModelID_dataStage02IsotopomerSimulation(self,experiment_id_I,sample_name_abbreviation_I,model_id_I):
        '''Querry model_ids for the sample_name_abbreviation that are used from the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_simulation.mapping_id).filter(
                    data_stage02_isotopomer_simulation.model_id.like(model_id_I),
                    data_stage02_isotopomer_simulation.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_simulation.used_.is_(True)).group_by(
                    data_stage02_isotopomer_simulation.mapping_id).order_by(
                    data_stage02_isotopomer_simulation.mapping_id.asc()).all();
            mapping_ids_O = [];
            if data: 
                for d in data:
                    mapping_ids_O.append(d.mapping_id);
            return mapping_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_mappingID_experimentIDAndModelID_dataStage02IsotopomerSimulation(self,experiment_id_I,model_id_I):
        '''Querry mapping_ids for the model_id that are used from the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_simulation.mapping_id).filter(
                    data_stage02_isotopomer_simulation.model_id.like(model_id_I),
                    data_stage02_isotopomer_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_simulation.used_.is_(True)).group_by(
                    data_stage02_isotopomer_simulation.mapping_id).order_by(
                    data_stage02_isotopomer_simulation.mapping_id.asc()).all();
            mapping_ids_O = [];
            if data: 
                for d in data:
                    mapping_ids_O.append(d.mapping_id);
            return mapping_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query rows from data_stage02_isotopomer_simulation
    def get_rows_simulationID_dataStage02IsotopomerSimulation(self,simulation_id_I):
        '''Querry rows that are used from the simulation'''
        try:
            data = query_session.query(data_stage02_isotopomer_simulation).filter(
                    data_stage02_isotopomer_simulation.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_simulation.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append({
                            'simulation_id':d.simulation_id,
                            'experiment_id':d.experiment_id,
                            'model_id':d.model_id,
                            'mapping_id':d.mapping_id,
                            'sample_name_abbreviation':d.sample_name_abbreviation,
                            'time_point':d.time_point,
                            'used_':d.used_,
                            'comment_':d.comment_});
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_simulation_simulationID_dataStage02IsotopomerSimulation(self,simulation_id_I):
        '''Querry rows that are used from the simulation'''
        try:
            data = query_session.query(data_stage02_isotopomer_simulation).filter(
                    data_stage02_isotopomer_simulation.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_simulation.used_.is_(True)).all();
            simulation_id_O = []
            experiment_id_O = []
            model_id_O = []
            mapping_id_O = []
            sample_name_abbreviation_O = []
            time_point_O = []
            simulation_O = {};
            if data: 
                for d in data:
                    simulation_id_O.append(d.simulation_id);
                    experiment_id_O.append(d.experiment_id);
                    model_id_O.append(d.model_id);
                    mapping_id_O.append(d.mapping_id);
                    sample_name_abbreviation_O.append(d.sample_name_abbreviation);
                    time_point_O.append(d.time_point);
                simulation_id_O = list(set(simulation_id_O))
                experiment_id_O = list(set(experiment_id_O))
                model_id_O = list(set(model_id_O))
                mapping_id_O = list(set(mapping_id_O))
                sample_name_abbreviation_O = list(set(sample_name_abbreviation_O))
                time_point_O = list(set(time_point_O))
                simulation_O={
                        'simulation_id':simulation_id_O,
                        'experiment_id':experiment_id_O,
                        'model_id':model_id_O,
                        'mapping_id':mapping_id_O,
                        'sample_name_abbreviation':sample_name_abbreviation_O,
                        'time_point':time_point_O};
                
            return simulation_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_isotopomer_measuredFragments
    # query sample_name_abbreviations from data_stage02_isotopomer_measuredFragments
    def get_sampleNameAbbreviations_experimentID_dataStage02IsotopomerMeasuredFragments(self,experiment_id_I):
        '''Querry sample_name_abbreviations that are used from
        the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_measuredFragments.sample_name_abbreviation).filter(
                    data_stage02_isotopomer_measuredFragments.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_measuredFragments.used_.is_(True)).group_by(
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation).order_by(
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    # query timePoint from data_stage02_isotopomer_measuredFragments
    def get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFragments(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rows for the sample_name_abbreviation that are used from the experiment'''
        try:
            data = query_session.query(
                    data_stage02_isotopomer_measuredFragments.time_point).filter(
                    data_stage02_isotopomer_measuredFragments.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_measuredFragments.used_.is_(True)).group_by(
                    data_stage02_isotopomer_measuredFragments.time_point).order_by(
                    data_stage02_isotopomer_measuredFragments.time_point.asc()).all();
            time_points_O = [];
            if data: 
                for d in data:
                    time_points_O.append(d.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query row from data_stage02_isotopomer_measuredFragments
    def get_row_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFragments(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rows for the sample_name_abbreviation that are used from the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_measuredFragments.experiment_id,
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation,
                    data_stage02_isotopomer_measuredFragments.time_point,
                    data_stage02_isotopomer_measuredFragments.met_id,
                    data_stage02_isotopomer_measuredFragments.fragment_id,
                    data_stage02_isotopomer_measuredFragments.fragment_formula,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_average,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_cv,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_stdev,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_units,
                    data_stage02_isotopomer_measuredFragments.scan_type,
                    data_stage02_isotopomer_measuredFragments.met_elements,
                    data_stage02_isotopomer_measuredFragments.met_atompositions).filter(
                    data_stage02_isotopomer_measuredFragments.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_measuredFragments.used_.is_(True)).group_by(
                    data_stage02_isotopomer_measuredFragments.experiment_id,
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation,
                    data_stage02_isotopomer_measuredFragments.time_point,
                    data_stage02_isotopomer_measuredFragments.met_id,
                    data_stage02_isotopomer_measuredFragments.fragment_id,
                    data_stage02_isotopomer_measuredFragments.fragment_formula,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_average,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_cv,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_stdev,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_units,
                    data_stage02_isotopomer_measuredFragments.scan_type,
                    data_stage02_isotopomer_measuredFragments.met_elements,
                    data_stage02_isotopomer_measuredFragments.met_atompositions).order_by(
                    data_stage02_isotopomer_measuredFragments.experiment_id.asc(),
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation.asc(),
                    data_stage02_isotopomer_measuredFragments.met_id.asc(),
                    data_stage02_isotopomer_measuredFragments.fragment_formula.desc(),
                    data_stage02_isotopomer_measuredFragments.time_point.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                            'sample_name_abbreviation':d.sample_name_abbreviation,
                            'time_point':d.time_point,
                            'met_id':d.met_id,
                            'fragment_id':d.fragment_id,
                            'fragment_formula':d.fragment_formula,
                            'intensity_normalized_average':d.intensity_normalized_average,
                            'intensity_normalized_cv':d.intensity_normalized_cv,
                            'intensity_normalized_stdev':d.intensity_normalized_stdev,
                            'intensity_normalized_units':d.intensity_normalized_units,
                            'scan_type':d.scan_type,
                            'met_elements':d.met_elements,
                            'met_atompositions':d.met_atompositions};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query row from data_stage02_isotopomer_measuredFragments
    def get_row_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage02IsotopomerMeasuredFragments(self,experiment_id_I,sample_name_abbreviation_I,time_point_I):
        '''Querry rows for the sample_name_abbreviation that are used from the experiment'''
        try:
            data = query_session.query(data_stage02_isotopomer_measuredFragments.experiment_id,
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation,
                    data_stage02_isotopomer_measuredFragments.time_point,
                    data_stage02_isotopomer_measuredFragments.met_id,
                    data_stage02_isotopomer_measuredFragments.fragment_id,
                    data_stage02_isotopomer_measuredFragments.fragment_formula,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_average,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_cv,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_stdev,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_units,
                    data_stage02_isotopomer_measuredFragments.scan_type,
                    data_stage02_isotopomer_measuredFragments.met_elements,
                    data_stage02_isotopomer_measuredFragments.met_atompositions).filter(
                    data_stage02_isotopomer_measuredFragments.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_measuredFragments.time_point.like(time_point_I),
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_measuredFragments.used_.is_(True)).group_by(
                    data_stage02_isotopomer_measuredFragments.experiment_id,
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation,
                    data_stage02_isotopomer_measuredFragments.time_point,
                    data_stage02_isotopomer_measuredFragments.met_id,
                    data_stage02_isotopomer_measuredFragments.fragment_id,
                    data_stage02_isotopomer_measuredFragments.fragment_formula,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_average,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_cv,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_stdev,
                    data_stage02_isotopomer_measuredFragments.intensity_normalized_units,
                    data_stage02_isotopomer_measuredFragments.scan_type,
                    data_stage02_isotopomer_measuredFragments.met_elements,
                    data_stage02_isotopomer_measuredFragments.met_atompositions).order_by(
                    data_stage02_isotopomer_measuredFragments.experiment_id.asc(),
                    data_stage02_isotopomer_measuredFragments.sample_name_abbreviation.asc(),
                    data_stage02_isotopomer_measuredFragments.met_id.asc(),
                    data_stage02_isotopomer_measuredFragments.fragment_formula.desc(),
                    data_stage02_isotopomer_measuredFragments.time_point.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                            'sample_name_abbreviation':d.sample_name_abbreviation,
                            'time_point':d.time_point,
                            'met_id':d.met_id,
                            'fragment_id':d.fragment_id,
                            'fragment_formula':d.fragment_formula,
                            'intensity_normalized_average':d.intensity_normalized_average,
                            'intensity_normalized_cv':d.intensity_normalized_cv,
                            'intensity_normalized_stdev':d.intensity_normalized_stdev,
                            'intensity_normalized_units':d.intensity_normalized_units,
                            'scan_type':d.scan_type,
                            'met_elements':d.met_elements,
                            'met_atompositions':d.met_atompositions};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_isotopomer_modelReactions
    # query rows from data_stage02_isotopomer_modelReactions
    def get_rows_modelID_dataStage02IsotopomerModelReactions(self,model_id_I):
        '''Querry rows by model_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_modelReactions).filter(
                    data_stage02_isotopomer_modelReactions.model_id.like(model_id_I),
                    data_stage02_isotopomer_modelReactions.used_.is_(True)).order_by(
                    data_stage02_isotopomer_modelReactions.model_id.asc(),
                    data_stage02_isotopomer_modelReactions.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'model_id':d.model_id,
                            'rxn_id':d.rxn_id,
                            'equation':d.equation,
                            'subsystem':d.subsystem,
                            'gpr':d.gpr,
                            'genes':d.genes,
                            'reactants_stoichiometry':d.reactants_stoichiometry,
                            'products_stoichiometry':d.products_stoichiometry,
                            'reactants_ids':d.reactants_ids,
                            'products_ids':d.products_ids,
                            'lower_bound':d.lower_bound,
                            'upper_bound':d.upper_bound,
                            'objective_coefficient':d.objective_coefficient,
                            'flux_units':d.flux_units,
                            'fixed':d.fixed,
                            'free':d.free,
                            'reversibility':d.reversibility,
                            'weight':d.weight,
                            'used_':d.used_,
                            'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query metabolites from data_stage02_isotopomer_modelReactions
    def get_metIDs_modelID_dataStage02IsotopomerModelReactions(self,model_id_I):
        '''Querry metabolites by model_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_modelReactions.reactants_ids,
                    data_stage02_isotopomer_modelReactions.products_ids).filter(
                    data_stage02_isotopomer_modelReactions.model_id.like(model_id_I),
                    data_stage02_isotopomer_modelReactions.used_.is_(True)).all();
            mets_all = [];
            mets_unique_O = [];
            if data: 
                for d in data:
                    mets_all.extend(d.reactants_ids);
                    mets_all.extend(d.products_ids);
                mets_unique_O = list(set(mets_all));
            return mets_unique_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_isotopomer_atomMappingReactions
    # query rxn_ids from data_stage02_isotopomer_atomMappingReactions
    def get_rxnIDs_mappingID_dataStage02IsotopomerAtomMappingReactions(self,mapping_id_I):
        '''Querry rows by mapping_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_atomMappingReactions.rxn_id).filter(
                    data_stage02_isotopomer_atomMappingReactions.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_atomMappingReactions.used_.is_(True)).order_by(
                    data_stage02_isotopomer_atomMappingReactions.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.rxn_id);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query rows from data_stage02_isotopomer_atomMappingReactions
    def get_rows_mappingID_dataStage02IsotopomerAtomMappingReactions(self,mapping_id_I):
        '''Querry rows by mapping_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_atomMappingReactions).filter(
                    data_stage02_isotopomer_atomMappingReactions.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_atomMappingReactions.used_.is_(True)).order_by(
                    data_stage02_isotopomer_atomMappingReactions.mapping_id.asc(),
                    data_stage02_isotopomer_atomMappingReactions.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'mapping_id':d.mapping_id,
                            'rxn_id':d.rxn_id,
                            'rxn_description':d.rxn_description,
                            'reactants_stoichiometry_tracked':d.reactants_stoichiometry_tracked,
                            'products_stoichiometry_tracked':d.products_stoichiometry_tracked,
                            'reactants_ids_tracked':d.reactants_ids_tracked,
                            'products_ids_tracked':d.products_ids_tracked,
                            'reactants_elements_tracked':d.reactants_elements_tracked,
                            'products_elements_tracked':d.products_elements_tracked,
                            'reactants_positions_tracked':d.reactants_positions_tracked,
                            'products_positions_tracked':d.products_positions_tracked,
                            'reactants_mapping':d.reactants_mapping,
                            'products_mapping':d.products_mapping,
                            'rxn_equation':d.rxn_equation,
                            'used_':d.used_,
                            'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_row_mappingIDAndRxnID_dataStage02IsotopomerAtomMappingReactions(self,mapping_id_I,rxn_id_I):
        '''Querry rows by mapping_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_atomMappingReactions).filter(
                    data_stage02_isotopomer_atomMappingReactions.rxn_id.like(rxn_id_I),
                    data_stage02_isotopomer_atomMappingReactions.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_atomMappingReactions.used_.is_(True)).order_by(
                    data_stage02_isotopomer_atomMappingReactions.mapping_id.asc(),
                    data_stage02_isotopomer_atomMappingReactions.rxn_id.asc()).all();
            row_O = {};
            if data: 
                for d in data:
                    row_tmp = {'mapping_id':d.mapping_id,
                            'rxn_id':d.rxn_id,
                            'rxn_description':d.rxn_description,
                            'reactants_stoichiometry_tracked':d.reactants_stoichiometry_tracked,
                            'products_stoichiometry_tracked':d.products_stoichiometry_tracked,
                            'reactants_ids_tracked':d.reactants_ids_tracked,
                            'products_ids_tracked':d.products_ids_tracked,
                            'reactants_elements_tracked':d.reactants_elements_tracked,
                            'products_elements_tracked':d.products_elements_tracked,
                            'reactants_positions_tracked':d.reactants_positions_tracked,
                            'products_positions_tracked':d.products_positions_tracked,
                            'reactants_mapping':d.reactants_mapping,
                            'products_mapping':d.products_mapping,
                            'rxn_equation':d.rxn_equation,
                            'used_':d.used_,
                            'comment_':d.comment_};
                    row_O.update(row_tmp);
            return row_O;
        except SQLAlchemyError as e:
            print(e);
    def get_atomMappingMetabolites_mappingID_dataStage02IsotopomerAtomMappingReactions(self,mapping_id_I):
        '''Querry rows by mapping_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_atomMappingReactions).filter(
                data_stage02_isotopomer_atomMappingReactions.mapping_id.like(mapping_id_I),
                data_stage02_isotopomer_atomMappingReactions.used_.is_(True)).all();
            data_O = []
            if data:
                for i,d in enumerate(data):
                    if d.reactants_ids_tracked:
                        for reactant_cnt,reactant in enumerate(d.reactants_ids_tracked):
                            print d.mapping_id,d.rxn_id,reactant
                            if len(d.reactants_elements_tracked)!=len(d.reactants_ids_tracked):
                                print 'reactants tracked do not match the elements tracked'
                                raw_input("Press enter to continue")
                            if len(d.reactants_positions_tracked)!=len(d.reactants_ids_tracked):
                                print 'reactants tracked do not match the positions tracked'
                                raw_input("Press enter to continue")
                            if len(d.reactants_stoichiometry_tracked)!=len(d.reactants_ids_tracked):
                                print 'reactants tracked do not match the stoichiometry tracked'
                                raw_input("Press enter to continue")
                            data_O.append({
                                    'mapping_id':d.mapping_id,
                                    #'met_name':self.met_name,
                                    'met_id':reactant,
                                    #'formula':self.formula,
                                    'met_elements':d.reactants_elements_tracked[reactant_cnt],
                                    'met_atompositions':d.reactants_positions_tracked[reactant_cnt],
                                    'met_symmetry_elements':None,
                                    'met_symmetry_atompositions':None,
                                    'used_':True,
                                    'comment_':None,
                                    'met_mapping':None,
                                    'base_met_ids':None,
                                    'base_met_elements':None,
                                    'base_met_atompositions':None,
                                    'base_met_symmetry_elements':None,
                                    'base_met_symmetry_atompositions':None,
                                    'base_met_indices':None})
                    if d.products_ids_tracked:
                        for product_cnt,product in enumerate(d.products_ids_tracked):
                            print d.mapping_id,d.rxn_id,product
                            if len(d.products_elements_tracked)!=len(d.products_ids_tracked):
                                print 'products tracked do not match the elements tracked'
                                raw_input("Press enter to continue")
                            if len(d.products_positions_tracked)!=len(d.products_ids_tracked):
                                print 'products tracked do not match the positions tracked'
                                raw_input("Press enter to continue")
                            if len(d.products_stoichiometry_tracked)!=len(d.products_ids_tracked):
                                print 'products tracked do not match the stoichiometry tracked'
                                raw_input("Press enter to continue")
                            data_O.append({
                                    'mapping_id':d.mapping_id,
                                    #'met_name':self.met_name,
                                    'met_id':product,
                                    #'formula':self.formula,
                                    'met_elements':d.products_elements_tracked[product_cnt],
                                    'met_atompositions':d.products_positions_tracked[product_cnt],
                                    'met_symmetry_elements':None,
                                    'met_symmetry_atompositions':None,
                                    'used_':True,
                                    'comment_':None,
                                    'met_mapping':None,
                                    'base_met_ids':None,
                                    'base_met_elements':None,
                                    'base_met_atompositions':None,
                                    'base_met_symmetry_elements':None,
                                    'base_met_symmetry_atompositions':None,
                                    'base_met_indices':None})
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_atomMappingMetabolites_mappingID_dataStage02IsotopomerAtomMappingReactionsAndAtomMappingMetabolites(self,mapping_id_rxns_I,mapping_id_mets_I):
        '''Querry rows by mapping_id that are used;
        NOTE: the mapping id matches the reaction mapping id'''
        try:
            data_O = [];
            #1. get the atom mapping metabolites already in the database
            data=None;
            data = query_session.query(data_stage02_isotopomer_atomMappingMetabolites).filter(
                data_stage02_isotopomer_atomMappingMetabolites.mapping_id.like(mapping_id_mets_I),
                data_stage02_isotopomer_atomMappingMetabolites.used_.is_(True)).all();
            if data:
                for d in data:
                    data_O.append({
                            'mapping_id':mapping_id_rxns_I, #d.mapping_id,
                            #'met_name':self.met_name,
                            'met_id':d.met_id,
                            #'formula':self.formula,
                            'met_elements':d.met_elements,
                            'met_atompositions':d.met_atompositions,
                            'met_symmetry_elements':d.met_symmetry_elements,
                            'met_symmetry_atompositions':d.met_symmetry_atompositions,
                            'used_':True,
                            'comment_':None,
                            'met_mapping':d.met_mapping,
                            'base_met_ids':d.base_met_ids,
                            'base_met_elements':d.base_met_elements,
                            'base_met_atompositions':d.base_met_atompositions,
                            'base_met_symmetry_elements':d.base_met_symmetry_elements,
                            'base_met_symmetry_atompositions':d.base_met_symmetry_atompositions,
                            'base_met_indices':d.base_met_indices})

            #2. get the atom mapping metabolites from the reactions
            data=None;
            data = query_session.query(data_stage02_isotopomer_atomMappingReactions).filter(
                data_stage02_isotopomer_atomMappingReactions.mapping_id.like(mapping_id_rxns_I),
                data_stage02_isotopomer_atomMappingReactions.used_.is_(True)).all();
            if data:
                for i,d in enumerate(data):
                    if d.reactants_ids_tracked:
                        for reactant_cnt,reactant in enumerate(d.reactants_ids_tracked):
                            print d.mapping_id,d.rxn_id,reactant
                            if len(d.reactants_elements_tracked)!=len(d.reactants_ids_tracked):
                                print 'reactants tracked do not match the elements tracked'
                                raw_input("Press enter to continue")
                            if len(d.reactants_positions_tracked)!=len(d.reactants_ids_tracked):
                                print 'reactants tracked do not match the positions tracked'
                                raw_input("Press enter to continue")
                            if len(d.reactants_stoichiometry_tracked)!=len(d.reactants_ids_tracked):
                                print 'reactants tracked do not match the stoichiometry tracked'
                                raw_input("Press enter to continue")
                            data_O.append({
                                    'mapping_id':d.mapping_id,
                                    #'met_name':self.met_name,
                                    'met_id':reactant,
                                    #'formula':self.formula,
                                    'met_elements':d.reactants_elements_tracked[reactant_cnt],
                                    'met_atompositions':d.reactants_positions_tracked[reactant_cnt],
                                    'met_symmetry_elements':None,
                                    'met_symmetry_atompositions':None,
                                    'used_':True,
                                    'comment_':None,
                                    'met_mapping':None,
                                    'base_met_ids':None,
                                    'base_met_elements':None,
                                    'base_met_atompositions':None,
                                    'base_met_symmetry_elements':None,
                                    'base_met_symmetry_atompositions':None,
                                    'base_met_indices':None})
                    if d.products_ids_tracked:
                        for product_cnt,product in enumerate(d.products_ids_tracked):
                            print d.mapping_id,d.rxn_id,product
                            if len(d.products_elements_tracked)!=len(d.products_ids_tracked):
                                print 'products tracked do not match the elements tracked'
                                raw_input("Press enter to continue")
                            if len(d.products_positions_tracked)!=len(d.products_ids_tracked):
                                print 'products tracked do not match the positions tracked'
                                raw_input("Press enter to continue")
                            if len(d.products_stoichiometry_tracked)!=len(d.products_ids_tracked):
                                print 'products tracked do not match the stoichiometry tracked'
                                raw_input("Press enter to continue")
                            data_O.append({
                                    'mapping_id':d.mapping_id,
                                    #'met_name':self.met_name,
                                    'met_id':product,
                                    #'formula':self.formula,
                                    'met_elements':d.products_elements_tracked[product_cnt],
                                    'met_atompositions':d.products_positions_tracked[product_cnt],
                                    'met_symmetry_elements':None,
                                    'met_symmetry_atompositions':None,
                                    'used_':True,
                                    'comment_':None,
                                    'met_mapping':None,
                                    'base_met_ids':None,
                                    'base_met_elements':None,
                                    'base_met_atompositions':None,
                                    'base_met_symmetry_elements':None,
                                    'base_met_symmetry_atompositions':None,
                                    'base_met_indices':None})
            return data_O; #may contain duplicates
        except SQLAlchemyError as e:
            print(e);
    # update rows from data_stage02_isotopomer_modelReactions and data_stage02_isotopomer_atomMappingReactions
    def update_rows_dataStage02IsotopomerAtomMappingReactions(self,data_I):
        '''update rows of data_stage02_isotopomer_atomMappingReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_update = query_session.query(data_stage02_isotopomer_atomMappingReactions).filter(
                            data_stage02_isotopomer_atomMappingReactions.mapping_id.like(d['mapping_id']),
                            data_stage02_isotopomer_atomMappingReactions.rxn_id.like(d['rxn_id'])
                            ).update(
                            {
                            'rxn_description':d['rxn_description'],
                            'reactants_stoichiometry_tracked':d['reactants_stoichiometry_tracked'],
                            'products_stoichiometry_tracked':d['products_stoichiometry_tracked'],
                            'reactants_ids_tracked':d['reactants_ids_tracked'],
                            'products_ids_tracked':d['products_ids_tracked'],
                            'reactants_elements_tracked':d['reactants_elements_tracked'],
                            'products_elements_tracked':d['products_elements_tracked'],
                            'reactants_positions_tracked':d['reactants_positions_tracked'],
                            'products_positions_tracked':d['products_positions_tracked'],
                            'reactants_mapping':d['reactants_mapping'],
                            'products_mapping':d['products_mapping'],
                            'rxn_equation':d['rxn_equation'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            query_session.commit();
    # delete rows from data_stage02_isotopomer_atomMappingReactions
    def delete_rows_mappingID_dataStage02IsotopomerAtomMappingReactions(self,mapping_id_I):
        '''Delete rows by mapping_id that are not used'''
        try:
            data = query_session.query(data_stage02_isotopomer_atomMappingReactions).filter(
                    data_stage02_isotopomer_atomMappingReactions.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_atomMappingReactions.used_.is_(False)).delete(synchronize_session=False);
            if data:
                query_session.commit();
        except SQLAlchemyError as e:
            print(e);
    # add rows to data_stage02_isotopomer_atomMappingReactions
    def add_data_dataStage02IsotopomerAtomMappingReactions(self, data_I):
        '''add rows of data_stage02_isotopomer_atomMappingReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_atomMappingReactions(
                                d['mapping_id'],
                                d['rxn_id'],
                                d['rxn_description'],
                                d['reactants_stoichiometry_tracked'],
                                d['products_stoichiometry_tracked'],
                                d['reactants_ids_tracked'],
                                d['products_ids_tracked'],
                                d['reactants_elements_tracked'],
                                d['products_elements_tracked'],
                                d['reactants_positions_tracked'],
                                d['products_positions_tracked'],
                                d['reactants_mapping'],
                                d['products_mapping'],
                                d['rxn_equation'],
                                d['used_'],
                                d['comment_']);
                    query_session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            query_session.commit();

    ## Query from data_stage02_isotopomer_modelReactions and data_stage02_isotopomer_atomMappingReactions
    # query rows from data_stage02_isotopomer_modelReactions and data_stage02_isotopomer_atomMappingReactions
    def get_join_modelIDAndMappingID_dataStage02IsotopomerModelReactionsAndAtomMapping(self,model_id_I,mapping_id_I):
        '''Querry join by model_id and mapping_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_modelReactions.model_id,
                    data_stage02_isotopomer_modelReactions.rxn_id,
                    data_stage02_isotopomer_modelReactions.equation,
                    data_stage02_isotopomer_modelReactions.subsystem,
                    data_stage02_isotopomer_modelReactions.gpr,
                    data_stage02_isotopomer_modelReactions.genes,
                    data_stage02_isotopomer_modelReactions.reactants_stoichiometry,
                    data_stage02_isotopomer_modelReactions.products_stoichiometry,
                    data_stage02_isotopomer_modelReactions.reactants_ids,
                    data_stage02_isotopomer_modelReactions.products_ids,
                    data_stage02_isotopomer_modelReactions.lower_bound,
                    data_stage02_isotopomer_modelReactions.upper_bound,
                    data_stage02_isotopomer_modelReactions.objective_coefficient,
                    data_stage02_isotopomer_modelReactions.flux_units,
                    data_stage02_isotopomer_modelReactions.fixed,
                    data_stage02_isotopomer_modelReactions.free,
                    data_stage02_isotopomer_modelReactions.reversibility,
                    data_stage02_isotopomer_modelReactions.weight,
                    data_stage02_isotopomer_atomMappingReactions.mapping_id,
                    data_stage02_isotopomer_atomMappingReactions.rxn_description,
                    data_stage02_isotopomer_atomMappingReactions.reactants_stoichiometry_tracked,
                    data_stage02_isotopomer_atomMappingReactions.products_stoichiometry_tracked,
                    data_stage02_isotopomer_atomMappingReactions.reactants_ids_tracked,
                    data_stage02_isotopomer_atomMappingReactions.products_ids_tracked,
                    data_stage02_isotopomer_atomMappingReactions.reactants_elements_tracked,
                    data_stage02_isotopomer_atomMappingReactions.products_elements_tracked,
                    data_stage02_isotopomer_atomMappingReactions.reactants_positions_tracked,
                    data_stage02_isotopomer_atomMappingReactions.products_positions_tracked,
                    data_stage02_isotopomer_atomMappingReactions.reactants_mapping,
                    data_stage02_isotopomer_atomMappingReactions.products_mapping,
                    data_stage02_isotopomer_atomMappingReactions.rxn_equation).filter(
                    data_stage02_isotopomer_modelReactions.model_id.like(model_id_I),
                    data_stage02_isotopomer_modelReactions.used_.is_(True),
                    data_stage02_isotopomer_atomMappingReactions.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_atomMappingReactions.used_.is_(True),
                    data_stage02_isotopomer_modelReactions.rxn_id.like(data_stage02_isotopomer_atomMappingReactions.rxn_id)).group_by(
                    data_stage02_isotopomer_modelReactions.model_id,
                    data_stage02_isotopomer_modelReactions.rxn_id,
                    data_stage02_isotopomer_modelReactions.equation,
                    data_stage02_isotopomer_modelReactions.subsystem,
                    data_stage02_isotopomer_modelReactions.gpr,
                    data_stage02_isotopomer_modelReactions.genes,
                    data_stage02_isotopomer_modelReactions.reactants_stoichiometry,
                    data_stage02_isotopomer_modelReactions.products_stoichiometry,
                    data_stage02_isotopomer_modelReactions.reactants_ids,
                    data_stage02_isotopomer_modelReactions.products_ids,
                    data_stage02_isotopomer_modelReactions.lower_bound,
                    data_stage02_isotopomer_modelReactions.upper_bound,
                    data_stage02_isotopomer_modelReactions.objective_coefficient,
                    data_stage02_isotopomer_modelReactions.flux_units,
                    data_stage02_isotopomer_modelReactions.fixed,
                    data_stage02_isotopomer_modelReactions.free,
                    data_stage02_isotopomer_modelReactions.reversibility,
                    data_stage02_isotopomer_modelReactions.weight,
                    data_stage02_isotopomer_atomMappingReactions.mapping_id,
                    data_stage02_isotopomer_atomMappingReactions.rxn_description,
                    data_stage02_isotopomer_atomMappingReactions.reactants_stoichiometry_tracked,
                    data_stage02_isotopomer_atomMappingReactions.products_stoichiometry_tracked,
                    data_stage02_isotopomer_atomMappingReactions.reactants_ids_tracked,
                    data_stage02_isotopomer_atomMappingReactions.products_ids_tracked,
                    data_stage02_isotopomer_atomMappingReactions.reactants_elements_tracked,
                    data_stage02_isotopomer_atomMappingReactions.products_elements_tracked,
                    data_stage02_isotopomer_atomMappingReactions.reactants_mapping,
                    data_stage02_isotopomer_atomMappingReactions.products_mapping,
                    data_stage02_isotopomer_atomMappingReactions.rxn_equation).order_by(
                    data_stage02_isotopomer_modelReactions.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'model_id':d.model_id,
                            'rxn_id':d.rxn_id,
                            'equation':d.equation,
                            'subsystem':d.subsystem,
                            'gpr':d.gpr,
                            'genes':d.genes,
                            'reactants_stoichiometry':d.reactants_stoichiometry,
                            'products_stoichiometry':d.products_stoichiometry,
                            'reactants_ids':d.reactants_ids,
                            'products_ids':d.products_ids,
                            'lower_bound':d.lower_bound,
                            'upper_bound':d.upper_bound,
                            'objective_coefficient':d.objective_coefficient,
                            'flux_units':d.flux_units,
                            'fixed':d.fixed,
                            'free':d.free,
                            'reversibility':d.reversibility,
                            'weight':d.weight,
                            'mapping_id':d.mapping_id,
                            'rxn_description':d.rxn_description,
                            'reactants_stoichiometry_tracked':d.reactants_stoichiometry_tracked,
                            'products_stoichiometry_tracked':d.products_stoichiometry_tracked,
                            'reactants_ids_tracked':d.reactants_ids_tracked,
                            'products_ids_tracked':d.products_ids_tracked,
                            'reactants_elements_tracked':d.reactants_elements_tracked,
                            'products_elements_tracked':d.products_elements_tracked,
                            'reactants_positions_tracked':d.reactants_positions_tracked,
                            'products_positions_tracked':d.products_positions_tracked,
                            'reactants_mapping':d.reactants_mapping,
                            'products_mapping':d.products_mapping,
                            'rxn_equation':d.rxn_equation};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    
    ## Query from data_stage02_isotopomer_tracers
    # query rows from data_stage02_isotopomer_tracers
    def get_rows_experimentID_dataStage02IsotopomerTracers(self,experiment_id_I):
        '''Querry rows by experiment_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_tracers).filter(
                    data_stage02_isotopomer_tracers.experiment_id.like(experiment_id_I)).order_by(
                    data_stage02_isotopomer_tracers.met_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                                'sample_name_abbreviation':d.sample_name_abbreviation,
                                'met_id':d.met_id,
                                'met_name':d.met_name,
                                'isotopomer_formula':d.isotopomer_formula,
                                'met_elements':d.met_elements,
                                'met_atompositions':d.met_atompositions,
                                'ratio':d.ratio,
                                'supplier':d.supplier,
                                'supplier_reference':d.supplier_reference,
                                'purity':d.purity,
                                'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerTracers(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rows by experiment_id and sample_name_abbreviation that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_tracers).filter(
                    data_stage02_isotopomer_tracers.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_tracers.sample_name_abbreviation.like(sample_name_abbreviation_I)).order_by(
                    data_stage02_isotopomer_tracers.met_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                                'sample_name_abbreviation':d.sample_name_abbreviation,
                                'met_id':d.met_id,
                                'met_name':d.met_name,
                                'isotopomer_formula':d.isotopomer_formula,
                                'met_elements':d.met_elements,
                                'met_atompositions':d.met_atompositions,
                                'ratio':d.ratio,
                                'supplier':d.supplier,
                                'supplier_reference':d.supplier_reference,
                                'purity':d.purity,
                                'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
            
    ## Query from data_stage02_isotopomer_measuredFluxes
    # query rows from data_stage02_isotopomer_measuredFluxes
    def get_rows_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFluxes(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_measuredFluxes).filter(
                    data_stage02_isotopomer_measuredFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_measuredFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_measuredFluxes.used_.is_(True)).order_by(
                    data_stage02_isotopomer_measuredFluxes.model_id.asc(),
                    data_stage02_isotopomer_measuredFluxes.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                    'model_id':d.model_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    #'time_point':d.time_point,
                    'rxn_id':d.rxn_id,
                    'flux_average':d.flux_average,
                    'flux_stdev':d.flux_stdev,
                    'flux_lb':d.flux_lb,
                    'flux_ub':d.flux_ub,
                    'flux_units':d.flux_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFluxes(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_measuredFluxes).filter(
                    data_stage02_isotopomer_measuredFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_measuredFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_measuredFluxes.model_id.like(model_id_I),
                    data_stage02_isotopomer_measuredFluxes.used_.is_(True)).order_by(
                    data_stage02_isotopomer_measuredFluxes.model_id.asc(),
                    data_stage02_isotopomer_measuredFluxes.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                    'model_id':d.model_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    #'time_point':d.time_point,
                    'rxn_id':d.rxn_id,
                    'flux_average':d.flux_average,
                    'flux_stdev':d.flux_stdev,
                    'flux_lb':d.flux_lb,
                    'flux_ub':d.flux_ub,
                    'flux_units':d.flux_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_isotopomer_atomMappingMetabolites
    # query rows from data_stage02_isotopomer_atomMappingMetabolites
    def get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(self,mapping_id_I,met_id_I):
        '''Querry rows by mapping_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_atomMappingMetabolites).filter(
                    data_stage02_isotopomer_atomMappingMetabolites.met_id.like(met_id_I),
                    data_stage02_isotopomer_atomMappingMetabolites.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_atomMappingMetabolites.used_.is_(True)).order_by(
                    data_stage02_isotopomer_atomMappingMetabolites.mapping_id.asc(),
                    data_stage02_isotopomer_atomMappingMetabolites.met_id.asc()).all();
            row_O = {};
            if data: 
                for d in data:
                    row_tmp = {'mapping_id':d.mapping_id,
                            'met_id':d.met_id,
                            'met_elements':d.met_elements,
                            'met_atompositions':d.met_atompositions,
                            'met_symmetry_elements':d.met_symmetry_elements,
                            'met_symmetry_atompositions':d.met_symmetry_atompositions,
                            'used_':d.used_,
                            'comment_':d.comment_,
                            'met_mapping':d.met_mapping,
                            'base_met_ids':d.base_met_ids,
                            'base_met_elements':d.base_met_elements,
                            'base_met_atompositions':d.base_met_atompositions,
                            'base_met_symmetry_elements':d.base_met_symmetry_elements,
                            'base_met_symmetry_atompositions':d.base_met_symmetry_atompositions,
                            'base_met_indices':d.base_met_indices};
                    row_O.update(row_tmp);
            return row_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_mappingID_dataStage02IsotopomerAtomMappingMetabolites(self,mapping_id_I):
        '''Querry rows by mapping_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_atomMappingMetabolites).filter(
                    data_stage02_isotopomer_atomMappingMetabolites.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_atomMappingMetabolites.used_.is_(True)).order_by(
                    data_stage02_isotopomer_atomMappingMetabolites.mapping_id.asc(),
                    data_stage02_isotopomer_atomMappingMetabolites.met_id.asc()).all();
            row_O = [];
            if data: 
                for d in data:
                    row_tmp = {'mapping_id':d.mapping_id,
                            'met_id':d.met_id,
                            'met_elements':d.met_elements,
                            'met_atompositions':d.met_atompositions,
                            'met_symmetry_elements':d.met_symmetry_elements,
                            'met_symmetry_atompositions':d.met_symmetry_atompositions,
                            'used_':d.used_,
                            'comment_':d.comment_,
                            'met_mapping':d.met_mapping,
                            'base_met_ids':d.base_met_ids,
                            'base_met_elements':d.base_met_elements,
                            'base_met_atompositions':d.base_met_atompositions,
                            'base_met_symmetry_elements':d.base_met_symmetry_elements,
                            'base_met_symmetry_atompositions':d.base_met_symmetry_atompositions,
                            'base_met_indices':d.base_met_indices};
                    row_O.append(row_tmp);
            return row_O;
        except SQLAlchemyError as e:
            print(e);
    # update rows from data_stage02_isotopomer_atomMappingMetabolites
    def update_rows_dataStage02IsotopomerAtomMappingMetabolites(self,data_I):
        '''update rows of data_stage02_isotopomer_atomMappingMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_update = query_session.query(data_stage02_isotopomer_atomMappingMetabolites).filter(
                            data_stage02_isotopomer_atomMappingMetabolites.mapping_id.like(d['mapping_id']),
                            data_stage02_isotopomer_atomMappingMetabolites.met_id.like(d['met_id'])
                            ).update(
                            {'met_elements':d['met_elements'],
                            'met_atompositions':d['met_atompositions'],
                            'met_symmetry_elements':d['met_symmetry_elements'],
                            'met_symmetry_atompositions':d['met_symmetry_atompositions'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],
                            'met_mapping':d['met_mapping'],
                            'base_met_ids':d['base_met_ids'],
                            'base_met_elements':d['base_met_elements'],
                            'base_met_atompositions':d['base_met_atompositions'],
                            'base_met_symmetry_elements':d['base_met_symmetry_elements'],
                            'base_met_symmetry_atompositions':d['base_met_symmetry_atompositions'],
                            'base_met_indices':d['base_met_indices']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            query_session.commit();
    # add rows to data_stage02_isotopomer_atomMappingMetabolites
    def add_data_dataStage02IsotopomerAtomMappingMetabolites(self, data_I):
        '''add rows of data_stage02_isotopomer_atomMappingMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_atomMappingMetabolites(
                                d['mapping_id'],
                                d['met_id'],
                                d['met_elements'],
                                d['met_atompositions'],
                                d['met_symmetry_elements'],
                                d['met_symmetry_atompositions'],
                                d['used_'],
                                d['comment_'],
                                d['met_mapping'],
                                d['base_met_ids'],
                                d['base_met_elements'],
                                d['base_met_atompositions'],
                                d['base_met_symmetry_elements'],
                                d['base_met_symmetry_atompositions'],
                                d['base_met_indices']);
                    query_session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            query_session.commit();
            
    ## Query from data_stage02_isotopomer_modelMetabolites
    # query formula from data_stage02_isotopomer_modelMetabolites
    def get_formula_modelIDAndMetID_dataStage02IsotopomerModelMetabolites(self,model_id_I, met_id_I):
        '''Query formula by model_id and met_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_modelMetabolites.formula).filter(
                    data_stage02_isotopomer_modelMetabolites.model_id.like(model_id_I),
                    data_stage02_isotopomer_modelMetabolites.met_id.like(met_id_I),
                    data_stage02_isotopomer_modelMetabolites.used_.is_(True)).order_by(
                    data_stage02_isotopomer_modelMetabolites.model_id.asc(),
                    data_stage02_isotopomer_modelMetabolites.met_id.asc()).all();
            formula_O = None;
            if data: 
                for d in data:
                    formula_O=d.formula
            else:
                print "formula not found"
            return formula_O;
        except SQLAlchemyError as e:
            print(e);
    # query rows from data_stage02_isotopomer_modelMetabolites
    def get_rows_modelID_dataStage02IsotopomerModelMetabolites(self,model_id_I):
        '''Querry rows by model_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_modelMetabolites).filter(
                    data_stage02_isotopomer_modelMetabolites.model_id.like(model_id_I),
                    data_stage02_isotopomer_modelMetabolites.used_.is_(True)).order_by(
                    data_stage02_isotopomer_modelMetabolites.model_id.asc(),
                    data_stage02_isotopomer_modelMetabolites.met_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'model_id':d.model_id,
                            'met_name':d.met_name,
                            'met_id':d.met_id,
                            'formula':d.formula,
                            'charge':d.charge,
                            'bound':d.bound,
                            'constraint_sense':d.constraint_sense,
                            'compartment':d.compartment,
                            'lower_bound':d.lower_bound,
                            'upper_bound':d.upper_bound,
                            'balanced':d.balanced,
                            'fixed':d.fixed,
                            'used_':d.used_,
                            'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites(self,model_id_I,met_id_I):
        '''Query row by model_id and met_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_modelMetabolites).filter(
                    data_stage02_isotopomer_modelMetabolites.model_id.like(model_id_I),
                    data_stage02_isotopomer_modelMetabolites.met_id.like(met_id_I),
                    data_stage02_isotopomer_modelMetabolites.used_.is_(True)).order_by(
                    data_stage02_isotopomer_modelMetabolites.model_id.asc(),
                    data_stage02_isotopomer_modelMetabolites.met_id.asc()).all();
            rows_O = {};
            if len(data)>1:
                print 'more than 1 model_id/met_id found!'
            if data: 
                for d in data:
                    rows_O = {'model_id':d.model_id,
                            'met_name':d.met_name,
                            'met_id':d.met_id,
                            'formula':d.formula,
                            'charge':d.charge,
                            'bound':d.bound,
                            'constraint_sense':d.constraint_sense,
                            'compartment':d.compartment,
                            'lower_bound':d.lower_bound,
                            'upper_bound':d.upper_bound,
                            'balanced':d.balanced,
                            'fixed':d.fixed,
                            'used_':d.used_,
                            'comment_':d.comment_};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query metabolites from data_stage02_isotopomer_modelMetabolites
    def get_metIDs_modelID_dataStage02IsotopomerModelMetabolites(self,model_id_I):
        '''Querry rows by model_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_modelMetabolites.met_id).filter(
                    data_stage02_isotopomer_modelMetabolites.model_id.like(model_id_I),
                    data_stage02_isotopomer_modelMetabolites.used_.is_(True)).order_by(
                    data_stage02_isotopomer_modelMetabolites.met_id.asc()).all();
            mets_O = [];
            if data: 
                for d in data:
                    mets_O.append(d.met_id);
            return mets_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_physiology_modelMetabolites
    # query rows from data_stage02_physiology_modelMetabolites
    def get_row_modelIDAndMetID_dataStage02PhysiologyModelMetabolites(self,model_id_I,met_id_I):
        '''Query row by model_id and met_id that are used'''
        try:
            data = query_session.query(data_stage02_physiology_modelMetabolites).filter(
                    data_stage02_physiology_modelMetabolites.model_id.like(model_id_I),
                    data_stage02_physiology_modelMetabolites.met_id.like(met_id_I),
                    data_stage02_physiology_modelMetabolites.used_.is_(True)).order_by(
                    data_stage02_physiology_modelMetabolites.model_id.asc(),
                    data_stage02_physiology_modelMetabolites.met_id.asc()).all();
            rows_O = {};
            if len(data)>1:
                print 'more than 1 model_id/met_id found!'
            if data: 
                for d in data:
                    rows_O = {'model_id':d.model_id,
                            'met_name':d.met_name,
                            'met_id':d.met_id,
                            'formula':d.formula,
                            'charge':d.charge,
                            'bound':d.bound,
                            'constraint_sense':d.constraint_sense,
                            'compartment':d.compartment};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);      

    ## Query from data_stage02_isotopomer_models
    # query row from data_stage02_isotopomer_models
    def get_row_modelID_dataStage02IsotopomerModels(self,model_id_I):
        '''Querry rows by model_id that are used'''
        try:
            data = query_session.query(data_stage02_isotopomer_models).filter(
                    data_stage02_isotopomer_models.model_id.like(model_id_I)).order_by(
                    data_stage02_isotopomer_models.model_id.asc()).all();
            rows_O = {};
            if data: 
                for d in data:
                    row_tmp = {'model_id':d.model_id,
                                'model_name':d.model_name,
                                'model_description':d.model_description,
                                'model_file':d.model_file,
                                'file_type':d.file_type,
                                'date':d.date};
                    rows_O.update(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_isotopomer_calcFluxes
    # query rows from data_stage02_isotopomer_calcFluxes   
    def get_rows_experimentIDAndModelIDAndMappingIDAndSampleNameAbbreviations_dataStage02IsotopomerCalcFluxes(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           mapping_id_I,
                                                                                                           sample_name_abbreviation_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_calcFluxes).filter(
                    data_stage02_isotopomer_calcFluxes.model_id.like(model_id_I),
                    data_stage02_isotopomer_calcFluxes.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_calcFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_calcFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_calcFluxes.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.experiment_id,
                        'model_id':d.model_id,
                        'sample_name_abbreviation':d.sample_name_abbreviation,
                        'mapping_id':d.mapping_id,
                        'rxn_id':d.rxn_id,
                        'flux_average':d.flux_average,
                        'flux_stdev':d.flux_stdev,
                        'flux_units':d.flux_units,
                        'flux_lb':d.flux_lb,
                        'flux_ub':d.flux_ub,
                        'used_':d.used_,
                        'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_experimentIDAndModelIDAndMappingIDAndSampleNameAbbreviations_dataStage02IsotopomerCalcFluxes(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           mapping_id_I,
                                                                                                           sample_name_abbreviation_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_calcFluxes).filter(
                    data_stage02_isotopomer_calcFluxes.model_id.like(model_id_I),
                    data_stage02_isotopomer_calcFluxes.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_calcFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_calcFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_calcFluxes.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if rows_O.has_key(d.rxn_id):
                        print 'duplicate rxn_id found!';
                    else:
                        rows_O[d.rxn_id]={
                        'flux':d.flux,
                        'flux_stdev':d.flux_stdev,
                        'flux_units':d.flux_units,
                        'flux_lb':d.flux_lb,
                        'flux_ub':d.flux_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherFluxLbUb_experimentIDAndModelIDAndMappingIDAndSampleNameAbbreviations_dataStage02IsotopomerCalcFluxes(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           mapping_id_I,
                                                                                                           sample_name_abbreviation_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_calcFluxes).filter(
                    data_stage02_isotopomer_calcFluxes.model_id.like(model_id_I),
                    data_stage02_isotopomer_calcFluxes.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_calcFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_calcFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_calcFluxes.used_.is_(True)).all();
            rows_O = [None,None];
            rows_O[0] = {};
            rows_O[1] = {}
            if data: 
                for d in data:
                    rows_O[0][d.rxn_id]=d.flux_lb;
                    rows_O[1][d.rxn_id]=d.flux_ub;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherFlux_experimentIDAndModelIDAndMappingIDAndSampleNameAbbreviations_dataStage02IsotopomerCalcFluxes(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           mapping_id_I,
                                                                                                           sample_name_abbreviation_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_calcFluxes).filter(
                    data_stage02_isotopomer_calcFluxes.model_id.like(model_id_I),
                    data_stage02_isotopomer_calcFluxes.mapping_id.like(mapping_id_I),
                    data_stage02_isotopomer_calcFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_isotopomer_calcFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_isotopomer_calcFluxes.used_.is_(True)).all();
            rows_O = {}
            if data: 
                for d in data:
                    rows_O[d.rxn_id]=d.flux_average;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_isotopomer_fittedFluxes
    # query simulation_dateAndTimes from data_stage02_isotopomer_fittedFluxes   
    def get_simulationDateAndTimes_simulationID_dataStage02IsotopomerfittedFluxes(self,simulation_id_I):
        '''Query reaction ids that are used from the fitted fluxes'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedFluxes.simulation_dateAndTime).filter(
                    data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedFluxes.used_.is_(True)).group_by(
                    data_stage02_isotopomer_fittedFluxes.simulation_dateAndTime).order_by(
                    data_stage02_isotopomer_fittedFluxes.simulation_dateAndTime.asc()).all();
            simulation_dateAndTimes_O = [];
            if data: 
                for d in data:
                    simulation_dateAndTimes_O.append(d.simulation_dateAndTime);
            return simulation_dateAndTimes_O;
        except SQLAlchemyError as e:
            print(e); 
    # query rxn_ids from data_stage02_isotopomer_fittedFluxes   
    def get_rxnIDs_simulationIDAndSimulationDateAndTime_dataStage02IsotopomerfittedFluxes(self,simulation_id_I,simulation_dateAndTime_I):
        '''Query reaction ids that are used from the fitted fluxes'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedFluxes.rxn_id).filter(
                    data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedFluxes.simulation_dateAndTime==simulation_dateAndTime_I,
                    data_stage02_isotopomer_fittedFluxes.used_.is_(True)).group_by(
                    data_stage02_isotopomer_fittedFluxes.rxn_id).order_by(
                    data_stage02_isotopomer_fittedFluxes.rxn_id.asc()).all();
            rxn_ids_O = [];
            if data: 
                for d in data:
                    rxn_ids_O.append(d.rxn_id);
            return rxn_ids_O;
        except SQLAlchemyError as e:
            print(e);   
    # query flux_average, flux_stdev, flux_lb, and flux_ub from data_stage02_isotopomer_fittedFluxes   
    def get_flux_simulationIDAndRxnID_dataStage02IsotopomerfittedFluxes(self,simulation_id_I,rxn_id_I):
        '''query flux_average, flux_stdev, flux_lb, and flux_ub from data_stage02_isotopomer_fittedFluxes'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedFluxes).filter(
                    data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedFluxes.rxn_id.like(rxn_id_I),
                    data_stage02_isotopomer_fittedFluxes.used_.is_(True)).all();
            flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O=0.0,0.0,0.0,0.0,'';
            if len(data)>1:
                print 'more than 1 row found'
                return;
            if data: 
                for d in data:
                    flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O = d.flux,d.flux_stdev,d.flux_lb,d.flux_ub,d.flux_units;
            return flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O;
        except SQLAlchemyError as e:
            print(e);    
    def get_flux_simulationIDAndSimulationDateAndTimeAndRxnID_dataStage02IsotopomerfittedFluxes(self,simulation_id_I,simulation_dateAndTime_I,rxn_id_I):
        '''query flux_average, flux_stdev, flux_lb, and flux_ub from data_stage02_isotopomer_fittedFluxes'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedFluxes).filter(
                    data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedFluxes.simulation_dateAndTime==simulation_dateAndTime_I,
                    data_stage02_isotopomer_fittedFluxes.rxn_id.like(rxn_id_I),
                    data_stage02_isotopomer_fittedFluxes.used_.is_(True)).all();
            flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O=0.0,0.0,0.0,0.0,'';
            if len(data)>1:
                print 'more than 1 row found'
                return;
            if data: 
                for d in data:
                    flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O = d.flux,d.flux_stdev,d.flux_lb,d.flux_ub,d.flux_units;
            return flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O;
        except SQLAlchemyError as e:
            print(e);   
    # query rows from data_stage02_isotopomer_fittedFluxes   
    def get_rows_simulationID_dataStage02IsotopomerfittedFluxes(self,simulation_id_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedFluxes).filter(
                    data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedFluxes.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'simulation_id':d.simulation_id,
                        'simulation_dateAndTime':d.simulation_dateAndTime,
                        'rxn_id':d.rxn_id,
                        'flux':d.flux,
                        'flux_stdev':d.flux_stdev,
                        'flux_units':d.flux_units,
                        'flux_lb':d.flux_lb,
                        'flux_ub':d.flux_ub,
                        'flux_alf':d.flux_alf,
                        'flux_chi2s':d.flux_chi2s,
                        'flux_cor':d.flux_cor,
                        'flux_cov':d.flux_cov,
                        'free':d.free,
                        'used_':d.used_,
                        'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_simulationID_dataStage02IsotopomerfittedFluxes(self,simulation_id_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedFluxes).filter(
                    data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedFluxes.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if rows_O.has_key(d.rxn_id):
                        print 'duplicate rxn_id found!';
                    else:
                        rows_O[d.rxn_id]={
                        'flux':d.flux,
                        'flux_stdev':d.flux_stdev,
                        'flux_units':d.flux_units,
                        'flux_lb':d.flux_lb,
                        'flux_ub':d.flux_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherFluxLbUb_simulationID_dataStage02IsotopomerfittedFluxes(self,simulation_id_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedFluxes).filter(
                    data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedFluxes.used_.is_(True)).all();
            rows_O = [None,None];
            rows_O[0] = {};
            rows_O[1] = {}
            if data: 
                for d in data:
                    rows_O[0][d.rxn_id]=d.flux_lb;
                    rows_O[1][d.rxn_id]=d.flux_ub;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherFlux_simulationID_dataStage02IsotopomerfittedFluxes(self,simulation_id_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedFluxes).filter(
                    data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedFluxes.used_.is_(True)).all();
            rows_O = {}
            if data: 
                for d in data:
                    rows_O[d.rxn_id]=d.flux;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    ## Query from data_stage02_isotopomer_fittedNetFluxes
    # query simulation_dateAndTimes from data_stage02_isotopomer_fittedNetFluxes   
    def get_simulationDateAndTimes_simulationID_dataStage02IsotopomerfittedNetFluxes(self,simulation_id_I):
        '''Query reaction ids that are used from the fitted fluxes'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedNetFluxes.simulation_dateAndTime).filter(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.used_.is_(True)).group_by(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_dateAndTime).order_by(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_dateAndTime.asc()).all();
            simulation_dateAndTimes_O = [];
            if data: 
                for d in data:
                    simulation_dateAndTimes_O.append(d.simulation_dateAndTime);
            return simulation_dateAndTimes_O;
        except SQLAlchemyError as e:
            print(e); 
    # query rxn_ids from data_stage02_isotopomer_fittedNetFluxes   
    def get_rxnIDs_simulationIDAndSimulationDateAndTime_dataStage02IsotopomerfittedNetFluxes(self,simulation_id_I,simulation_dateAndTime_I):
        '''Query reaction ids that are used from the fitted fluxes'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedNetFluxes.rxn_id).filter(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.simulation_dateAndTime==simulation_dateAndTime_I,
                    data_stage02_isotopomer_fittedNetFluxes.used_.is_(True)).group_by(
                    data_stage02_isotopomer_fittedNetFluxes.rxn_id).order_by(
                    data_stage02_isotopomer_fittedNetFluxes.rxn_id.asc()).all();
            rxn_ids_O = [];
            if data: 
                for d in data:
                    rxn_ids_O.append(d.rxn_id);
            return rxn_ids_O;
        except SQLAlchemyError as e:
            print(e);   
    # query flux_average, flux_stdev, flux_lb, and flux_ub from data_stage02_isotopomer_fittedNetFluxes   
    def get_flux_simulationIDAndRxnID_dataStage02IsotopomerfittedNetFluxes(self,simulation_id_I,rxn_id_I):
        '''query flux_average, flux_stdev, flux_lb, and flux_ub from data_stage02_isotopomer_fittedNetFluxes'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedNetFluxes).filter(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.rxn_id.like(rxn_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.used_.is_(True)).all();
            flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O=0.0,0.0,0.0,0.0,'';
            if len(data)>1:
                print 'more than 1 row found'
                return;
            if data: 
                for d in data:
                    flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O = d.flux,d.flux_stdev,d.flux_lb,d.flux_ub,d.flux_units;
            return flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O;
        except SQLAlchemyError as e:
            print(e);    
    def get_flux_simulationIDAndSimulationDateAndTimeAndRxnID_dataStage02IsotopomerfittedNetFluxes(self,simulation_id_I,simulation_dateAndTime_I,rxn_id_I):
        '''query flux_average, flux_stdev, flux_lb, and flux_ub from data_stage02_isotopomer_fittedNetFluxes'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedNetFluxes).filter(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.simulation_dateAndTime==simulation_dateAndTime_I,
                    data_stage02_isotopomer_fittedNetFluxes.rxn_id.like(rxn_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.used_.is_(True)).all();
            flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O=0.0,0.0,0.0,0.0,'';
            if len(data)>1:
                print 'more than 1 row found'
                return;
            if data: 
                for d in data:
                    flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O = d.flux,d.flux_stdev,d.flux_lb,d.flux_ub,d.flux_units;
            return flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O;
        except SQLAlchemyError as e:
            print(e);   
    # query rows from data_stage02_isotopomer_fittedNetFluxes   
    def get_rows_simulationID_dataStage02IsotopomerfittedNetFluxes(self,simulation_id_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedNetFluxes).filter(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'simulation_id':d.simulation_id,
                        'simulation_dateAndTime':d.simulation_dateAndTime,
                        'rxn_id':d.rxn_id,
                        'flux':d.flux,
                        'flux_stdev':d.flux_stdev,
                        'flux_units':d.flux_units,
                        'flux_lb':d.flux_lb,
                        'flux_ub':d.flux_ub,
                        'used_':d.used_,
                        'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_simulationID_dataStage02IsotopomerfittedNetFluxes(self,simulation_id_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedNetFluxes).filter(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if rows_O.has_key(d.rxn_id):
                        print 'duplicate rxn_id found!';
                    else:
                        rows_O[d.rxn_id]={
                        'flux':d.flux,
                        'flux_stdev':d.flux_stdev,
                        'flux_units':d.flux_units,
                        'flux_lb':d.flux_lb,
                        'flux_ub':d.flux_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherFluxLbUb_simulationID_dataStage02IsotopomerfittedNetFluxes(self,simulation_id_I):
        '''Query rows that are used from the flux_average'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedNetFluxes).filter(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.used_.is_(True)).all();
            rows_O = [None,None];
            rows_O[0] = {};
            rows_O[1] = {}
            if data: 
                for d in data:
                    rows_O[0][d.rxn_id]=d.flux_lb;
                    rows_O[1][d.rxn_id]=d.flux_ub;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherFlux_simulationID_dataStage02IsotopomerfittedNetFluxes(self,simulation_id_I):
        '''Query rows that are used from the flux_average
        output: dict, rxn_id:flux'''
        try:
            data = self.session.query(data_stage02_isotopomer_fittedNetFluxes).filter(
                    data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I),
                    data_stage02_isotopomer_fittedNetFluxes.used_.is_(True)).all();
            rows_O = {}
            if data: 
                for d in data:
                    rows_O[d.rxn_id]=d.flux;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);