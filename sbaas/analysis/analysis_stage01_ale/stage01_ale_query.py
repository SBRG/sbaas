from analysis.analysis_base import *

class stage01_ale_query(base_analysis):        
    # query sample name abbreviations from data_stage01_ale_trajectories
    def get_sampleNameAbbreviations_experimentID_dataStage01AleTrajectories(self,experiment_id_I):
        '''Querry sample name abbreviations that are used from the experiment'''
        try:
            sample_names = self.session.query(data_stage01_ale_trajectories.sample_name_abbreviation).filter(
                    data_stage01_ale_trajectories.experiment_id.like(experiment_id_I),
                    data_stage01_ale_trajectories.used_.is_(True)).group_by(
                    data_stage01_ale_trajectories.sample_name_abbreviation).order_by(
                    data_stage01_ale_trajectories.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query rows from data_stage01_ale_rates
    def get_rows_experimentIDAndSampleNameAbbreviation_dataStage01AleTrajectories(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rows for sample_name_abbreviations that are used from the experiment'''
        try:
            data = self.session.query(data_stage01_ale_trajectories).filter(
                    data_stage01_ale_trajectories.experiment_id.like(experiment_id_I),
                    data_stage01_ale_trajectories.used_.is_(True),
                    data_stage01_ale_trajectories.sample_name_abbreviation.like(sample_name_abbreviation_I)).order_by(
                    data_stage01_ale_trajectories.ale_time.asc()).all();
            data_O = [];
            if data:
                for d in data:
                    data_tmp = {'experiment_id':d.experiment_id,
                                'sample_name_abbreviation':d.sample_name_abbreviation,
                                'ale_time':d.ale_time,
                                'ale_time_units':d.ale_time_units,
                                'rate':d.rate,
                                'rate_units':d.rate_units,
                                'used_':d.used_,
                                'comment_':d.comment_};
                    data_O.append(data_tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);