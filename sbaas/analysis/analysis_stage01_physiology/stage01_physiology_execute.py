from analysis.analysis_base import *
from .stage01_physiology_query import *
from .stage01_physiology_io import *
import datetime
from math import exp

class stage01_physiology_execute():
    '''class for physiological analysis analysis'''
    def __init__(self,session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.stage01_physiology_query = stage01_physiology_query(self.session);
        self.calculate = base_calculate();

    #analyses:
    def execute_calculateGrowthRates(self,experiment_id_I,sample_name_short_I=[]):
        '''Calculate growth rates (hr-1) based on the sample time and measured OD600'''

        #query sample names
        print('executing calculating growth rates...')
        if sample_name_short_I:
            sample_name_short = sample_name_short_I;
        else:
            sample_name_short = [];
            sample_name_short = self.stage01_physiology_query.get_sampleNameShort_experimentID(experiment_id_I,6)
        for sns in sample_name_short:
            print('calculating growth rates for sample_name_short ' + sns);
            #query met_ids
            met_ids = [];
            met_ids = self.stage01_physiology_query.get_metIDs_experimentIDAndSampleNameShort(experiment_id_I,6,sns);
            for met in met_ids:
                print('calculating growth rates for met_id ' + met);
                if met != 'biomass': continue;
                #query time and OD600 values
                time, OD600 = [], [];
                time, OD600 = self.stage01_physiology_query.get_sampleDateAndDataCorrected_experimentIDAndSampleNameShortAndMetIDAndDataUnits(experiment_id_I,6,sns,met,'OD600');
                if not OD600 or not time: continue;
                #convert time to hrs
                time_hrs = [];
                for t in time:
                    time_hrs.append(t.year*8765.81277 + t.month*730.484  + t.day*365.242 + t.hour + t.minute / 60. + t.second / 3600.); #convert using datetime object
                #calculate growth rate and r2
                slope, intercept, r2, p_value, std_err = self.calculate.calculate_growthRate(time_hrs,OD600)
                #add rows to the data base
                row = [];
                row = data_stage01_physiology_rates(experiment_id_I, sns, met,
                     slope, intercept, r2, slope, 'hr-1',
                     p_value, std_err,
                     True, None);
                self.session.add(row);
        self.session.commit();
    def execute_interpolateBiomassFromReplicates(self,experiment_id_I, sample_ids_I=[]):
        '''Interpolate the OD600 based on the Calculated growth rates (hr-1) of the respective replicate and time the sample was taken
        for samples in the experiment that do not have a measured OD600 value
        Use cases:
        1. Broth samples (Filtrate samples should be calculated off of the average)'''

        data = [];
        #query sample_ids for the experiment that do not have an OD600 but have a time
        print('execute interpolate biomass from replicates...')
        if sample_ids_I:
            sample_ids = [];
            sample_ids = sample_ids_I;
        else:
            sample_ids = [];
            sample_ids = self.stage01_physiology_query.get_sampleIDs_experimentIDAndSampleDescriptionNoOD600_samplePhysiologicalParameters(experiment_id_I,'Broth')
        for si in sample_ids:
            print('interpolating biomass from replicates for sample_id ' + si)
            #query rate parameters for the sample_id
            slope, intercept, r2, rate, rate_units, p_value, std_err = None,None,None,None,None,None,None;
            slope, intercept, r2, rate, rate_units, p_value, std_err = self.stage01_physiology_query.get_rateData_experimentIDAndSampleIDAndMetID_dataStage01PhysiologyRates(experiment_id_I,si,'biomass');
            #query physiological parameters for the sample_id
            pp = {};
            pp = self.stage01_physiology_query.get_physiologicalParameters_experimentIDAndSampleID_samplePhysiologicalParameters(experiment_id_I,si)
            #query sample_date
            sample_date = None;
            sample_date = self.stage01_physiology_query.get_sampleDate_experimentIDAndSampleID_sampleDescription(experiment_id_I,si);
            #interpolate based off of the regression parameters
            time = sample_date.year*8765.81277 + sample_date.month*730.484  + sample_date.day*365.242 + sample_date.hour + sample_date.minute / 60. + sample_date.second / 3600.;
            biomass = exp(time*slope+intercept);
            if biomass < 1e-1:
                print('check biomass')
            #update sample_physiologicalParameters
            pp['od600'] = biomass;
            data.append(pp);  
        self.stage01_physiology_query.update_data_samplePhysiologicalParameters(data)
    def execute_calculateRatesAverages(self,experiment_id_I,sample_name_abbreviations_I=[]):
        '''Calculate the average rates based on the rates of the replicates'''

        #query sample_name abbreviations
        print('execute calcute rates averages...')
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage01_physiology_query.get_sampleNameAbbreviations_experimentID_dataStage01PhysiologyRates(experiment_id_I,6);
        for sna in sample_name_abbreviations:
            print('calculating rates averages for sample_name_abbreviation ' + sna);
            #query met_ids
            met_ids = [];
            met_ids = self.stage01_physiology_query.get_metIDs_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologyRates(experiment_id_I,6,sna)
            for met in met_ids:
                print('calculating rates averages for met_id ' +met);
                #query sample names
                sample_name_short = [];
                sample_name_short = self.stage01_physiology_query.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRates(experiment_id_I,6,sna,met)
                slopes, intercepts, rates, rates_units, std_errs = [],[],[],[],[];
                for sns in sample_name_short:
                    #query slope, intercept, and rate
                    slope, intercept, r2, rate, rate_units, p_value, std_err = None,None,None,None,None,None,None;
                    slope, intercept, r2, rate, rate_units, p_value, std_err = self.stage01_physiology_query.get_rateData_experimentIDAndSampleNameShortAndMetID_dataStage01PhysiologyRates(experiment_id_I,sns,met);
                    slopes.append(slope);
                    intercepts.append(intercept);
                    rates.append(rate);
                    rates_units.append(rate_units);
                    std_errs.append(std_err);
                #calculate the average, variance, and 95% confidence intervals
                n = len(rates);
                slopes_ave, slopes_var, slopes_lb, slopes_ub = self.calculate.calculate_ave_var(slopes);
                intercepts_ave, intercepts_var, intercepts_lb, intercepts_ub = self.calculate.calculate_ave_var(intercepts);
                rates_ave, rates_var, rates_lb, rates_ub = self.calculate.calculate_ave_var(rates);
                #add rows to the data base
                row = [];
                row = data_stage01_physiology_ratesAverages(experiment_id_I, sna,
                     met, n, slopes_ave, intercepts_ave, rates_ave, rates_var,
                     rates_lb, rates_ub, rates_units[0], True, None);
                self.session.add(row);
        self.session.commit();
    def execute_interpolateBiomassFromAverages(self,experiment_id_I, sample_ids_I=[]):
        '''Interpolate the OD600 based on the Calculated growth rates (hr-1) of the average and time the sample was taken
        for samples in the experiment that do not have a measured OD600 value
        Use cases:
        1. a replicate is bad'''

        data = [];
        #query sample_ids for the experiment that do not have an OD600 but have a time
        print('execute interoplate biomass from averages...')
        if sample_ids_I:
            sample_ids = [];
            sample_ids = sample_ids_I;
        else:
            sample_ids = [];
            sample_ids = self.stage01_physiology_query.get_sampleIDs_experimentIDNoOD600_samplePhysiologicalParameters(experiment_id_I)
        for si in sample_ids:
            print('interpolating biomass from averages for sample_id' + si);
            #query rate parameters for the sample_id
            slope_average, intercept_average, rate_average, rate_units, rate_var = None,None,None,None,None;
            slope_average, intercept_average, rate_average, rate_units, rate_var = self.stage01_physiology_query.get_rateData_experimentIDAndSampleIDAndMetID_dataStage01PhysiologyRatesAverages(experiment_id_I,si,'biomass');
            #query physiological parameters for the sample_id
            pp = {};
            pp = self.stage01_physiology_query.get_physiologicalParameters_experimentIDAndSampleID_samplePhysiologicalParameters(experiment_id_I,si)
            #query sample_date
            sample_date = None;
            sample_date = self.stage01_physiology_query.get_sampleDate_experimentIDAndSampleID_sampleDescription(experiment_id_I,si);
            #interpolate based off of the regression parameters
            time = sample_date.year*8765.81277 + sample_date.month*730.484  + sample_date.day*365.242 + sample_date.hour + sample_date.minute / 60. + sample_date.second / 3600.;
            biomass = exp(time*slope_average+intercept_average);
            #update sample_physiologicalParameters
            pp['od600'] = biomass;
            data.append(pp);  
        self.stage01_physiology_query.update_data_samplePhysiologicalParameters(data)
    def execute_calculateBiomassFromBrothAverage(self,experiment_id_I, sample_ids_I=[]):
        '''Calculate the OD600 based on the average OD600 of the broth samples
        for samples in the experiment that do not have a measured OD600 value
        Use cases:
        1. the sample Filtrate'''

        data = [];
        #query sample_ids for the experiment that do not have an OD600
        print('execute calculate biomass from broth averages...')
        if sample_ids_I:
            sample_ids = [];
            sample_ids = sample_ids_I;
        else:
            sample_ids = [];
            sample_ids = self.stage01_physiology_query.get_sampleIDs_experimentIDAndSampleDescriptionNoOD600_samplePhysiologicalParameters(experiment_id_I,'Filtrate')
        for si in sample_ids:
            print('calculating biomass from broth averages for sample_id ' + si);
            #query physiological parameters for the sample_id
            pp = {};
            pp = self.stage01_physiology_query.get_physiologicalParameters_experimentIDAndSampleID_samplePhysiologicalParameters(experiment_id_I,si)
            #query sample_date
            sample_date = None;
            sample_date = self.stage01_physiology_query.get_sampleDate_experimentIDAndSampleID_sampleDescription(experiment_id_I,si);
            #query od600 values from biological broth replicates
            broth_od600 = [];
            broth_od600 = self.stage01_physiology_query.get_OD600s_experimentIDAndSampleID_samplePhysiologicalParameters(experiment_id_I,si);
            #update sample_physiologicalParameters
            pp['od600'] = numpy.mean(broth_od600);
            data.append(pp);  
        self.stage01_physiology_query.update_data_samplePhysiologicalParameters(data)
    def execute_updatePhysiologicalParametersFromOD600(self, experiment_id_I, sample_ids_I=[]):
        '''Calculate physiological parameters from the OD600 and volume sample'''
        data = [];
        #query sample_ids for the experiment that have an OD600, but do not have culture_density
        print('execute update physiological parameters from OD600...')
        if sample_ids_I:
            sample_ids = [];
            sample_ids = sample_ids_I;
        else:
            sample_ids = [];
            sample_ids = self.stage01_physiology_query.get_sampleIDs_experimentIDWithOD600NoCultureDensity_samplePhysiologicalParameters(experiment_id_I)
        for si in sample_ids:
            print('updating physiological parameters from OD600 for sample_id ' + si);
            #Query sample_description
            desc = {};
            desc = self.stage01_physiology_query.get_description_experimentIDAndSampleID_sampleDescription(experiment_id_I,si)
            if not desc['biological_material']: continue;
            #query physiological parameters for the sample_id
            pp = {};
            pp = self.stage01_physiology_query.get_physiologicalParameters_experimentIDAndSampleID_samplePhysiologicalParameters(experiment_id_I,si)
            #Query conversions (conversion_name: gDW2OD_lab and ODspecificCellConcentration_lab)
            conversion_gDW2OD = None;
            conversion_gDW2OD_units = None;
            conversion_gDW2OD, conversion_gDW2OD_units = self.stage01_physiology_query.get_conversionAndConversionUnits_biologicalMaterialAndConversionName(desc['biological_material'],'gDW2OD_lab');
            conversion_ODspecificCellConcentration = None;
            conversion_ODspecificCellConcentration_units = None;
            conversion_ODspecificCellConcentration, conversion_ODspecificCellConcentration_units = self.stage01_physiology_query.get_conversionAndConversionUnits_biologicalMaterialAndConversionName(desc['biological_material'],'ODspecificCellConcentration_lab');
            #Calculate the vcd, culture_density from the OD600 and conversions
            culture_density,culture_density_units = None,None;
            culture_density,culture_density_units = self.calculate.calculate_cultureDensity_ODAndConversionAndConversionUnits(pp['od600'],conversion_gDW2OD, conversion_gDW2OD_units);
            vcd,vcd_units = None,None;
            vcd,vcd_units = self.calculate.calculate_cultureDensity_ODAndConversionAndConversionUnits(pp['od600'],conversion_ODspecificCellConcentration, conversion_ODspecificCellConcentration_units);
            #Calculate the cells, dcw, wcw from the OD600, culture_volume_sampled and conversions

            #Update sample_physiologicalparameters
            pp['culture_density'],pp['culture_density_units'] = culture_density,culture_density_units;
            pp['vcd'],pp['vcd_units'] = vcd,vcd_units;
            data.append(pp);
        self.stage01_physiology_query.update_data_samplePhysiologicalParameters(data);
    def execute_calculateUptakeAndSecretionRates(self,experiment_id_I,sample_name_short_I=[],QC_filename_O=None):
        '''Calculate uptake and secretion rates (mmol*gDCW-1*hr-1) based on the sample time,
        measured gDCW (calculated from the OD600),
        and calculated growth rate (hr-1)'''

        data_O = [];
        #query sample names
        print('execute calculate uptake and secretion rates...')
        if sample_name_short_I:
            sample_name_short = sample_name_short_I;
        else:
            sample_name_short = [];
            sample_name_short = self.stage01_physiology_query.get_sampleNameShort_experimentID(experiment_id_I,7)
        for sns in sample_name_short:
            print('calculating uptake and secretion rates for sample_name_short ' +sns);
            #query met_ids
            met_ids = [];
            met_ids = self.stage01_physiology_query.get_metIDs_experimentIDAndSampleNameShort(experiment_id_I,7,sns);
            for met in met_ids:
                print('calculating uptake and secretion rates for met_id ' + met);
                if met == 'biomass': continue; #ignore biomass (calculated previously)
                #query time,conc (mM), and sample_ids
                time, conc, sample_ids = [], [], []; #sorted by sample_date
                time, conc, sample_ids = self.stage01_physiology_query.get_sampleDateAndDataCorrectedAndSampleIDs_experimentIDAndSampleNameShortAndMetIDAndDataUnits(experiment_id_I,7,sns,met,'mM');
                if not conc or not time: continue;
                #query slope, intercept, and rate for the growth rate
                slope, intercept, r2, gr_rate, rate_units, p_value, std_err = None,None,None,None,None,None,None;
                slope, intercept, r2, gr_rate, rate_units, p_value, std_err = self.stage01_physiology_query.get_rateData_experimentIDAndSampleNameShortAndMetID_dataStage01PhysiologyRates(experiment_id_I,sns,'biomass');
                #query OD600 and DCW from sample_physiologicalparameters
                OD600, culture_density = [],[]; #sorted by sample_date
                for si in sample_ids:
                    OD600_tmp, culture_density_tmp = None,None;
                    OD600_tmp, culture_density_tmp = self.stage01_physiology_query.get_OD600AndCultureDensity_experimentIDAndSampleID_samplePhysiologicalParameters(experiment_id_I,7,si);
                    OD600.append(OD600_tmp);
                    culture_density.append(culture_density_tmp);
                #check that the length of DCW and conc match
                if len(conc)!=len(culture_density):
                    print('The length of measured concentrations and measured dcw do not match!')
                #convert time to hrs
                time_hrs = [];
                for t in time:
                    time_hrs.append(t.year*8765.81277 + t.month*730.484  + t.day*365.242 + t.hour + t.minute / 60. + t.second / 3600.); #convert using datetime object
                #calculate growth rate and r2
                slope, intercept, r2, rate, rate_units, p_value, std_err = None,None,None,None,None,None,None;
                slope, intercept, r2, p_value, std_err, rate = self.calculate.calculate_uptakeAndSecretionRate(culture_density,conc,gr_rate)
                #record time, conc, and culture density for QC
                for si_cnt,si in enumerate(sample_ids):
                    tmp={};
                    tmp['sample_name_short']=sns;
                    tmp['met_id']=met;
                    tmp['sample_id']=si;
                    tmp['time [hr]']=time_hrs[si_cnt];
                    tmp['OD600']=OD600[si_cnt];
                    tmp['culture_density [gDW*L-1]']=culture_density[si_cnt];
                    tmp['concentration [mM]']=conc[si_cnt];
                    tmp['growth_rate [hr-1]']=gr_rate;
                    data_O.append(tmp);
                #add rows to the data base
                row = [];
                row = data_stage01_physiology_rates(experiment_id_I, sns, met,
                     slope, intercept, r2, rate, 'mmol*gDCW-1*hr-1',
                     p_value, std_err,
                     True, None);
                self.session.add(row);
        self.session.commit();
        if QC_filename_O:
            io = base_exportData(data_O);
            io.write_dict2csv(QC_filename_O,['sample_name_short','met_id','sample_id',
                                             'time [hr]','OD600','culture_density [gDW*L-1]',
                                             'concentration [mM]','growth_rate [hr-1]']);
    #table initializations:
    def drop_dataStage01(self):
        try:
            data_stage01_physiology_data.__table__.drop(engine,True);
            data_stage01_physiology_rates.__table__.drop(engine,True);
            data_stage01_physiology_ratesAverages.__table__.drop(engine,True);
            data_stage01_physiology_analysis.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage01(self,experiment_id_I = None,analysis_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage01_physiology_data).filter(data_stage01_physiology_data.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_physiology_ratesAverages).filter(data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_physiology_rates).filter(data_stage01_physiology_rates.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            elif analysis_id_I:
                reset = self.session.query(data_stage01_physiology_analysis).filter(data_stage01_physiology_analysis.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage01_physiology_data).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_physiology_ratesAverages).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_physiology_rates).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_physiology_analysis).analysis_id.like(analysis_id_I).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage01_physiology_rates(self,experiment_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage01_physiology_ratesAverages).filter(data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_physiology_rates).filter(data_stage01_physiology_rates.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage01_physiology_ratesAverages).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_physiology_rates).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage01(self):
        try:
            data_stage01_physiology_data.__table__.create(engine,True);
            data_stage01_physiology_ratesAverages.__table__.create(engine,True);
            data_stage01_physiology_rates.__table__.create(engine,True);
            data_stage01_physiology_analysis.__table__.create(engine,True);
        except SQLAlchemyError as e:
            print(e);
