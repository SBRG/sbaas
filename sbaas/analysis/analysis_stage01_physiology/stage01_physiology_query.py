from analysis.analysis_base import *

class stage01_physiology_query(base_analysis):
    # query conversion and conversion units from sample_masstovolumeconversion
    def get_conversionAndConversionUnits_biologicalMaterialAndConversionName(self,biological_material_I,conversion_name_I):
        '''Querry conversion and conversion units from
        biological material and conversion name
        NOTE: intended to be used within a for loop'''
        try:
            physiologicalParameters = self.session.query(sample_massVolumeConversion.conversion_factor,
                    sample_massVolumeConversion.conversion_units).filter(
                    sample_massVolumeConversion.biological_material.like(biological_material_I),
                    sample_massVolumeConversion.conversion_name.like(conversion_name_I)).all();
            conversion_O = physiologicalParameters[0][0];
            conversion_units_O = physiologicalParameters[0][1];
            return conversion_O, conversion_units_O;
        except SQLAlchemyError as e:
            print(e);

    # query sample names from data_stage01_physiology_data
    def get_sampleNameShort_experimentID(self,experiment_id_I,exp_type_I):
        '''Querry sample name short (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample_description.sample_name_short).filter(
                    data_stage01_physiology_data.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_data.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_physiology_data.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_short).order_by(
                    sample_description.sample_name_short.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_short);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample IDs from data_stage01_physiology_data
    def get_sampleIDs_experimentID(self,experiment_id_I,exp_type_I):
        '''Querry sample ids (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_physiology_data.sample_id).filter(
                    data_stage01_physiology_data.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_data.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_physiology_data.sample_id)).group_by(
                    data_stage01_physiology_data.sample_id).order_by(
                    data_stage01_physiology_data.sample_id.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_short);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query met_ids from data_stage01_physiology_data
    def get_metIDs_experimentIDAndSampleNameShort(self,experiment_id_I,exp_type_I,sample_name_short_I):
        '''Querry met_ids by sample name short that are used from
        the experiment'''
        try:
            met_ids = self.session.query(data_stage01_physiology_data.met_id).filter(
                    data_stage01_physiology_data.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_data.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_physiology_data.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(sample_name_short_I)).group_by(
                    data_stage01_physiology_data.met_id).order_by(
                    data_stage01_physiology_data.met_id.asc()).all();
            met_ids_O = [];
            for met in met_ids: met_ids_O.append(met.met_id);
            return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample_date and data_corrected from data_stage01_physiology_data
    def get_sampleDateAndDataCorrected_experimentIDAndSampleNameShortAndMetIDAndDataUnits(self,experiment_id_I,exp_type_I,sample_name_short_I,met_id_I,data_units_I):
        '''Querry time and data_corrected by sample name short that are used from
        the experiment sorted by time'''
        try:
            data = self.session.query(sample_description.sample_date,
                    data_stage01_physiology_data.data_corrected).filter(
                    data_stage01_physiology_data.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_data.met_id.like(met_id_I),
                    data_stage01_physiology_data.data_units.like(data_units_I),
                    data_stage01_physiology_data.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_physiology_data.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(sample_name_short_I)).order_by(
                    sample_description.sample_date.asc()).all();
            sample_date_O = [];
            data_corrected_O = [];
            for d in data: 
                sample_date_O.append(d.sample_date);
                data_corrected_O.append(d.data_corrected);
            return sample_date_O,data_corrected_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample_date, data_corrected, and sample_ids from data_stage01_physiology_data
    def get_sampleDateAndDataCorrectedAndSampleIDs_experimentIDAndSampleNameShortAndMetIDAndDataUnits(self,experiment_id_I,exp_type_I,sample_name_short_I,met_id_I,data_units_I):
        '''Querry time and data_corrected by sample name short that are used from
        the experiment sorted by time'''
        try:
            data = self.session.query(sample_description.sample_date,
                    data_stage01_physiology_data.data_corrected,
                    data_stage01_physiology_data.sample_id).filter(
                    data_stage01_physiology_data.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_data.met_id.like(met_id_I),
                    data_stage01_physiology_data.data_units.like(data_units_I),
                    data_stage01_physiology_data.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_physiology_data.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(sample_name_short_I)).order_by(
                    sample_description.sample_date.asc()).all();
            sample_date_O = [];
            data_corrected_O = [];
            sample_id_O = [];
            for d in data: 
                sample_date_O.append(d.sample_date);
                data_corrected_O.append(d.data_corrected);
                sample_id_O.append(d.sample_id);
            return sample_date_O,data_corrected_O,sample_id_O;
        except SQLAlchemyError as e:
            print(e);
            
    # query sample ids from sample_physiologicalParameters
    def get_sampleIDs_experimentIDNoOD600_samplePhysiologicalParameters(self,experiment_id_I):
        '''Querry sample ids (i.e. unknowns) that are used from
        the experiment for all experiment types
        that do not have an OD600 but do have a time'''
        try:
            sample_names = self.session.query(sample_physiologicalParameters.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id),
                    #sample.sample_id.like(sample_description.sample_id),
                    sample_physiologicalParameters.od600 == None).group_by(
                    sample_physiologicalParameters.sample_id).order_by(
                    sample_physiologicalParameters.sample_id.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_id);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleIDs_experimentIDAndSampleDescriptionNoOD600_samplePhysiologicalParameters(self,experiment_id_I,sample_description_I):
        '''Querry sample ids (i.e. unknowns) that are used from
        the experiment for all experiment types
        that do not have an OD600 but do have a time'''
        try:
            sample_names = self.session.query(sample_physiologicalParameters.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_description.like(sample_description_I),
                    sample_physiologicalParameters.od600 == None).group_by(
                    sample_physiologicalParameters.sample_id).order_by(
                    sample_physiologicalParameters.sample_id.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_id);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleIDs_experimentIDWithOD600NoCultureDensity_samplePhysiologicalParameters(self,experiment_id_I):
        '''Querry sample ids (i.e. unknowns) that are used from
        the experiment for all experiment types
        that do have an OD600 but do not have a culture density'''
        try:
            sample_names = self.session.query(sample_physiologicalParameters.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id),
                    sample_physiologicalParameters.od600 != None,
                    sample_physiologicalParameters.culture_density == None).group_by(
                    sample_physiologicalParameters.sample_id).order_by(
                    sample_physiologicalParameters.sample_id.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_id);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query physiologicalParameters from sample_physiologicalParameters
    def get_physiologicalParameters_experimentIDAndSampleID_samplePhysiologicalParameters(self,experiment_id_I,sample_id_I):
        '''Query physiologicalParameters by sample id from sample_physiologicalparameters'''
        try:
            data = self.session.query(sample_physiologicalParameters).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id)).first();
            pp = {};
            if data: 
                pp['sample_id']=data.sample_id;
                pp['growth_condition_short']=data.growth_condition_short;
                pp['growth_condition_long']=data.growth_condition_long;
                pp['media_short']=data.media_short;
                pp['media_long']=data.media_long;
                pp['isoxic']=data.isoxic;
                pp['temperature']=data.temperature;
                pp['supplementation']=data.supplementation;
                pp['od600']=data.od600;
                pp['vcd']=data.vcd;
                pp['culture_density']=data.culture_density;
                pp['culture_volume_sampled']=data.culture_volume_sampled;
                pp['cells']=data.cells;
                pp['dcw']=data.dcw;
                pp['wcw']=data.wcw;
                pp['vcd_units']=data.vcd_units;
                pp['culture_density_units']=data.culture_density_units;
                pp['culture_volume_sampled_units']=data.culture_volume_sampled_units;
                pp['dcw_units']=data.dcw_units;
                pp['wcw_units']=data.wcw_units;
            return pp;
        except SQLAlchemyError as e:
            print(e);
    # query OD600 values from sample_physiologicalParameters
    def get_OD600s_experimentIDAndSampleID_samplePhysiologicalParameters(self,experiment_id_I,sample_id_I):
        '''query OD600 values from biological broth replicates'''
        #1 query sample_name_abbreviation and exp_typ_id by experiment_id and sample_id
        try:
            sample_names = self.session.query(sample_description.sample_name_abbreviation,
                    experiment.exp_type_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample.sample_id.like(sample_id_I)).first();
            sample_name_abbreviation_O = None;
            exp_type_id_O = None;
            if sample_names:
                sample_name_abbreviation_O = sample_names.sample_name_abbreviation;
                exp_type_id_O = sample_names.exp_type_id
        except SQLAlchemyError as e:
            print(e);
        #2 query OD600 by sample_name_abbreviation, exp_type_id, sample_description, istechnical
        try:
            od600 = self.session.query(sample_physiologicalParameters.od600).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_O),
                    sample_description.sample_description.like('Broth'),
                    sample_description.istechnical.is_(False),
                    sample_physiologicalParameters.od600 != None,
                    sample.sample_id.like(sample_description.sample_id),
                    sample_physiologicalParameters.sample_id.like(sample_description.sample_id),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.exp_type_id == exp_type_id_O).group_by(
                    sample_physiologicalParameters.od600).all();
            od600_O = [];
            if od600: 
                for od in od600:
                    od600_O.append(od.od600);
            return od600_O;
        except SQLAlchemyError as e:
            print(e);
    # query OD600 and DCW values from sample_physiologicalParameters
    def get_OD600AndCultureDensity_experimentIDAndSampleNameShort_samplePhysiologicalParameters(self,experiment_id_I,exp_type_id_I,sample_name_short_I):
        '''query OD600 and culture density values sorted by time'''
        try:
            od600 = self.session.query(sample_physiologicalParameters.od600,
                    sample_physiologicalParameters.culture_density,
                    sample_description.sample_date).filter(
                    experiment.id.like(experiment_id_I),
                    sample_description.sample_name_short.like(sample_name_short_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_physiologicalParameters.sample_id.like(sample.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.exp_type_id == exp_type_id_I).group_by(
                    sample_physiologicalParameters.od600,
                    sample_physiologicalParameters.culture_density,
                    sample_description.sample_date).order_by(
                    sample_description.sample_date.asc()).all();
            od600_O = [];
            culture_density_O = [];
            if od600: 
                for od in od600:
                    od600_O.append(od.od600);
                    culture_density_O.append(od.culture_density);
            return od600_O,culture_density_O;
        except SQLAlchemyError as e:
            print(e);
    # query OD600 and DCW values from sample_physiologicalParameters
    def get_OD600AndCultureDensity_experimentIDAndSampleID_samplePhysiologicalParameters(self,experiment_id_I,exp_type_id_I,sample_id_I):
        '''query OD600 and culture density values sorted by time'''
        try:
            od600 = self.session.query(sample_physiologicalParameters.od600,
                    sample_physiologicalParameters.culture_density,
                    sample_description.sample_date).filter(
                    experiment.id.like(experiment_id_I),
                    sample_description.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_id_I),
                    sample_physiologicalParameters.sample_id.like(sample_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.exp_type_id == exp_type_id_I).first();
            od600_O = None;
            culture_density_O = None;
            if od600: 
                od600_O=od600.od600;
                culture_density_O=od600.culture_density;
            return od600_O,culture_density_O;
        except SQLAlchemyError as e:
            print(e);

    # query description from sample_description
    def get_description_experimentIDAndSampleID_sampleDescription(self,experiment_id_I,sample_id_I):
        '''Query description by sample id from sample_description'''
        try:
            data = self.session.query(sample_description).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id)).first();
            desc = {};
            if data: 
                desc['sample_id']=data.sample_id;
                desc['sample_name_short']=data.sample_name_short;
                desc['sample_name_abbreviation']=data.sample_name_abbreviation;
                desc['sample_date']=data.sample_date;
                desc['time_point']=data.time_point;
                desc['sample_condition']=data.sample_condition;
                desc['extraction_method_id']=data.extraction_method_id;
                desc['biological_material']=data.biological_material;
                desc['sample_description']=data.sample_description;
                desc['sample_replicate']=data.sample_replicate;
                desc['is_added']=data.is_added;
                desc['is_added_units']=data.is_added_units;
                desc['reconstitution_volume']=data.reconstitution_volume;
                desc['reconstitution_volume_units']=data.reconstitution_volume_units;
                desc['istechnical']=data.istechnical;
                desc['sample_replicate_biological']=data.sample_replicate_biological;
                desc['notes']=data.notes;
            return desc;
        except SQLAlchemyError as e:
            print(e);

    # update physiologicalParameters 
    def update_data_samplePhysiologicalParameters(self,dataListUpdated_I):
        # update the sample_physiologicalParameters table
        updates = [];
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(sample_physiologicalParameters).filter(
                        sample_physiologicalParameters.sample_id.like(d['sample_id'])).update(		
                        {'growth_condition_short':d['growth_condition_short'],
                        'growth_condition_long':d['growth_condition_long'],
                        'media_short':d['media_short'],
                        'media_long':d['media_long'],
                        'isoxic':d['isoxic'],
                        'temperature':d['temperature'],
                        'supplementation':d['supplementation'],
                        'od600':d['od600'],
                        'vcd':d['vcd'],
                        'culture_density':d['culture_density'],
                        'culture_volume_sampled':d['culture_volume_sampled'],
                        'cells':d['cells'],
                        'dcw':d['dcw'],
                        'wcw':d['wcw'],
                        'vcd_units':d['vcd_units'],
                        'culture_density_units':d['culture_density_units'],
                        'culture_volume_sampled_units':d['culture_volume_sampled_units'],
                        'dcw_units':d['dcw_units'],
                        'wcw_units':d['wcw_units']},
                        synchronize_session=False);
                if data_update == 0:
                    print 'row not found.'
                    print d;
                updates.append(data_update);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    # query sample_date from sample_description
    def get_sampleDate_experimentIDAndSampleID_sampleDescription(self,experiment_id_I,sample_id_I):
        '''Query sample_date by sample id'''
        try:
            data = self.session.query(sample_description.sample_date).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id)).first();
            sample_date_O = None;
            if data: 
                sample_date_O=data.sample_date;
            return sample_date_O;
        except SQLAlchemyError as e:
            print(e);
        
    # query sample names from data_stage01_physiology_rates
    def get_sampleNameAbbreviations_experimentID_dataStage01PhysiologyRates(self,experiment_id_I,exp_type_I):
        '''Querry sample name abbreviations (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage01_physiology_rates.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_rates.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_physiology_data.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(data_stage01_physiology_rates.sample_name_short)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRates(self,experiment_id_I,exp_type_I,sample_name_abbreviation_I,met_id_I):
        '''Querry sample name short that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample_description.sample_name_short).filter(
                    data_stage01_physiology_rates.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_rates.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_physiology_data.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(data_stage01_physiology_rates.sample_name_short),
                    data_stage01_physiology_rates.met_id.like(met_id_I),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I)).group_by(
                    sample_description.sample_name_short).order_by(
                    sample_description.sample_name_short.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_short);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query metIDs from data_stage01_physiology_rates
    def get_metIDs_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologyRates(self,experiment_id_I,exp_type_I,sample_name_abbreviation_I):
        '''Querry met_ids that are used from
        the experiment'''
        try:
            met_ids = self.session.query(data_stage01_physiology_rates.met_id).filter(
                    data_stage01_physiology_rates.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_rates.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_physiology_data.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.sample_name_short.like(data_stage01_physiology_rates.sample_name_short)).group_by(
                    data_stage01_physiology_rates.met_id).order_by(
                    data_stage01_physiology_rates.met_id.asc()).all();
            met_ids_O = [];
            for met in met_ids: met_ids_O.append(met.met_id);
            return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query rate from data_stage01_physiology_rates
    def get_rateData_experimentIDAndSampleIDAndMetID_dataStage01PhysiologyRates(self,experiment_id_I,sample_id_I,met_id_I):
        '''Querry rate data by sample id and met id that are used from
        the experiment'''
        #1 check if the sample is a technical replicate
        try:
           tech = self.session.query(sample_description.istechnical,
                                     sample_description.sample_replicate_biological,
                                     sample_description.sample_date,
                                     sample_description.sample_name_abbreviation,
                                     sample_description.sample_description,
                                     sample_description.time_point,
                                     experiment.exp_type_id).filter(
                    sample_description.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name)).first();
           technical_O = False;
           sample_replicate_biological_O = None;
           sample_name_abbreviation_O = None;
           sample_description_O = None;
           sample_date_O = None;
           time_point_O = None;
           exp_type_id_O = None;
           if tech:
               technical_O = tech.istechnical;
               sample_replicate_biological_O = tech.sample_replicate_biological;
               sample_date_O = tech.sample_date;
               sample_name_abbreviation_O = tech.sample_name_abbreviation;
               sample_description_O = tech.sample_description
               time_point_O = tech.time_point;
               exp_type_id_O = tech.exp_type_id;
        except SQLAlchemyError as e:
           print(e);
        #2 if the sample is a technical replicate, get the biological replicate
        if technical_O:
            try:
               sample_id = self.session.query(sample_description.sample_id).filter(
                        sample_description.sample_name_abbreviation.like(sample_name_abbreviation_O),
                        sample_description.sample_description.like(sample_description_O),
                        sample_description.time_point.like(time_point_O),
                        sample_description.istechnical.is_(False),
                        sample_description.sample_replicate_biological == sample_replicate_biological_O,
                        sample_description.sample_date == sample_date_O,
                        sample_description.sample_replicate == sample_replicate_biological_O,
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.exp_type_id == exp_type_id_O).first();
               sample_id_I = None;
               if sample_id: sample_id_I = sample_id.sample_id
            except SQLAlchemyError as e:
                print(e);
        #3 query the data
        try:
            data = self.session.query(data_stage01_physiology_rates.slope,
                    data_stage01_physiology_rates.intercept,
                    data_stage01_physiology_rates.r2,
                    data_stage01_physiology_rates.rate,
                    data_stage01_physiology_rates.rate_units,
                    data_stage01_physiology_rates.p_value,
                    data_stage01_physiology_rates.std_err).filter(
                    data_stage01_physiology_rates.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_rates.met_id.like(met_id_I),
                    data_stage01_physiology_rates.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_physiology_rates.sample_name_short.like(sample_description.sample_name_short)).first();
            slope, intercept, r2, rate, rate_units, p_value, std_err = None,None,None,None,None,None,None;
            if data: 
                slope, intercept, r2, rate, rate_units, p_value, std_err = data.slope, data.intercept, data.r2, data.rate, data.rate_units, data.p_value, data.std_err;
            return slope, intercept, r2, rate, rate_units, p_value, std_err;
        except SQLAlchemyError as e:
            print(e);
    def get_rateData_experimentIDAndSampleNameShortAndMetID_dataStage01PhysiologyRates(self,experiment_id_I,sample_name_short_I,met_id_I):
        '''Querry rate data by sample name short and met id that are used from
        the experiment'''
        try:
            data = self.session.query(data_stage01_physiology_rates.slope,
                    data_stage01_physiology_rates.intercept,
                    data_stage01_physiology_rates.r2,
                    data_stage01_physiology_rates.rate,
                    data_stage01_physiology_rates.rate_units,
                    data_stage01_physiology_rates.p_value,
                    data_stage01_physiology_rates.std_err).filter(
                    data_stage01_physiology_rates.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_rates.met_id.like(met_id_I),
                    data_stage01_physiology_rates.used_.is_(True),
                    data_stage01_physiology_rates.sample_name_short.like(sample_name_short_I)).first();
            slope, intercept, r2, rate, rate_units, p_value, std_err = None,None,None,None,None,None,None;
            if data: 
                slope, intercept, r2, rate, rate_units, p_value, std_err = data.slope, data.intercept, data.r2, data.rate, data.rate_units, data.p_value, data.std_err;
            return slope, intercept, r2, rate, rate_units, p_value, std_err;
        except SQLAlchemyError as e:
            print(e);
    
    # query sample names from data_stage01_physiology_rates
    def get_sampleNameAbbreviations_experimentID_dataStage01PhysiologyRatesAverages(self,experiment_id_I):
        '''Querry sample name abbreviations (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_physiology_ratesAverages.sample_name_abbreviation).filter(
                    data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_ratesAverages.used_.is_(True)).group_by(
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation).order_by(
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e)
    # query met_ids from data_stage01_physiology_rates
    def get_metIDs_experimentID_dataStage01PhysiologyRatesAverages(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry sample name abbreviations (i.e. unknowns) that are used from
        the experiment'''
        try:
            met_id = self.session.query(data_stage01_physiology_ratesAverages.met_id).filter(
                    data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_ratesAverages.used_.is_(True),
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation.like(sample_name_abbreviation_I)).group_by(
                    data_stage01_physiology_ratesAverages.met_id).order_by(
                    data_stage01_physiology_ratesAverages.met_id.asc()).all();
            met_id_O = [];
            for sn in met_id: met_id_O.append(sn.met_id);
            return met_id_O;
        except SQLAlchemyError as e:
            print(e)
            
    # query rate from data_stage01_physiology_ratesAverages
    def get_rateData_experimentIDAndSampleIDAndMetID_dataStage01PhysiologyRatesAverages(self,experiment_id_I,sample_id_I,met_id_I):
        '''Querry rate data by sample id and met id that are used from
        the experiment'''
        try:
            data = self.session.query(data_stage01_physiology_ratesAverages.slope_average,
                    data_stage01_physiology_ratesAverages.intercept_average,
                    data_stage01_physiology_ratesAverages.rate_average,
                    data_stage01_physiology_ratesAverages.rate_units,
                    data_stage01_physiology_ratesAverages.rate_var).filter(
                    data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_ratesAverages.met_id.like(met_id_I),
                    data_stage01_physiology_ratesAverages.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation.like(sample_description.sample_name_abbreviation)).first();
            slope_average, intercept_average, rate_average, rate_units, rate_var = None,None,None,None,None;
            if data: 
                slope_average, intercept_average, rate_average, rate_units, rate_var = data.slope_average, data.intercept_average, data.rate_average, data.rate_units, data.rate_var;
            return slope_average, intercept_average, rate_average, rate_units, rate_var;
        except SQLAlchemyError as e:
            print(e);
    def get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(self,experiment_id_I,sample_name_abbreviation_I,met_id_I):
        '''Querry rate data by sample id and met id that are used from
        the experiment'''
        try:
            data = self.session.query(data_stage01_physiology_ratesAverages.slope_average,
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