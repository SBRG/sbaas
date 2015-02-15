from analysis.analysis_base import *
from stage00_query import *
from stage00_io import *
from resources.molmass import Formula
import re
import io,os
from resources.chemaxon import cxcalc_bin, RunCxcalc
from resources.molmass import Formula
from copy import copy

class stage00_execute():
    '''class for quantitative metabolomics analysis'''

    def __init__(self):
        self.session = Session();
        self.stage00_query = stage00_query();
        self.calculate = base_calculate();

    def execute_correctMassesFromFormula(self):
        '''Replace the q1_mass, q3_mass, and ms3_mass with the monoisotopic mass from formula'''
        return
    def execute_13CFluxMRM(self,met_ids_I):
        '''generate the MRMs for each compound for m + 0 to m + # carbons in the precursor
        and product formula'''
        # input: 
        #       met_ids_I = [{'met_id': , 'precursor_formula':, 'product_formula':},]
        # ouptput:
        #       dictionary of 13CFlux MRMs

        phosphates = ["O3P-","H2O4P-","HO6P2-"]

        mrms_O = [];
        stage_io = stage00_io();
        # loop over each met_id
        for met in met_ids_I:
            # make mass ensemble for precursor
            precursor_Formula_str = re.sub('[+-]', '', met['precursor_formula']);
            precursor_Formula = Formula(precursor_Formula_str);
            precursor_ensemble = self.make_13CEnsemble(met['precursor_formula']);
            if 'C' in precursor_Formula._elements:
                nCpre = precursor_Formula._elements['C'][0]; # count the number of carbon;
            else: nCpre = 0;
            # make mass ensemble for product
            product_Formula_str = re.sub('[+-]', '', met['product_formula']);
            product_Formula = Formula(product_Formula_str);
            product_ensemble = self.make_13CEnsemble(met['product_formula']);
            if 'C' in product_Formula._elements:
                nCpro = product_Formula._elements['C'][0]; # count the number of carbon;
            else: nCpro = 0;

            # query transition from the tuning method
            trans = self.stage00_query.get_row_MSComponents_metIDAndFormula(met['met_id'],met['precursor_formula'],met['product_formula'],'tuning');

            # make component_name, group_name
            trans['ms_methodtype'] = 'isotopomer_13C';
            
            # match precursor to product and add to new mrms list
            for pre_m,pre_Formula in precursor_ensemble.iteritems(): # loop over each precursor
                if nCpre-pre_m < nCpro: nUnlabeled = nCpre-pre_m;
                else: nUnlabeled = nCpro;
                if pre_m < nCpro: nLabeled = pre_m;
                else: nLabeled = nCpro;
                if nUnlabeled > 0 and nUnlabeled < nCpro: pro_m_start = nCpro - nUnlabeled;
                elif nUnlabeled > 0: pro_m_start = 0;
                else: pro_m_start = nCpro;
                for i in range(pro_m_start,nLabeled+1): # loop over each product        
                    trans13C = trans.copy();
                    # make 13C component_name, group_name,...
                    trans13C['component_name'] = trans13C['met_id'] + '.' + trans13C['met_id'] + '_m' + str(pre_m) + '-' + str(i);
                    trans13C['ms_group'] = trans['met_id'] + '.' + trans13C['met_id'] + '_m' + str(pre_m) + '-' + str(i);
                    trans13C['quantifier'] = 1;
                    trans13C['precursor_formula'] = pre_Formula._formula + trans13C['ms_mode'];
                    trans13C['precursor_exactmass'] = pre_Formula.isotope.mass;
                    trans13C['product_formula'] = product_ensemble[i]._formula + trans13C['ms_mode'];
                    trans13C['product_exactmass'] = product_ensemble[i].isotope.mass;
                    trans13C['met_name'] = trans['met_name'] + '-' + pre_Formula._formula + '_' + product_ensemble[i]._formula;
                    trans13C['q1_mass'] = pre_Formula.isotope.mass;
                    trans13C['q3_mass'] = product_ensemble[i].isotope.mass;
                    trans13C['ms3_mass'] = None;
                    trans13C['quantifier'] = None;
                    trans13C['ion_intensity_rank'] = None;
                    trans13C['ion_abundance'] = None;
                    trans13C['ms_include'] = True;

                    mrms_O.append(trans13C);
        
        stage_io.add_MSComponents(mrms_O);       
    def execute_scheduledMRMPro_quant(self,met_ids_I):
        '''generate the MRMs for each compound for the scheduled MRM pro acquisition method'''
        # input: 
        #       met_ids_I = [{'met_id': , 'precursor_formula':, 'product_formula':},]
        # ouptput:
        #       dictionary of MRMs
        
        mrms_O = [];
        stage_io = stage00_io();
        # loop over each met_id
        for met in met_ids_I:
            # query transition from the tuning method
            trans = self.stage00_query.get_row_MSComponents_metIDAndFormula(met['met_id'],met['precursor_formula'],met['product_formula'],'tuning');
            transUC13 = trans.copy();
            # make component_name, group_name
            trans['component_name'] = met['met_id'] + '.' + met['met_id'] + '_' + str(trans['quantifier']) + '.Light';
            trans['ms_group'] = met['met_id'];
            trans['ms_methodtype'] = 'quantification';

            # make UC13 component_name, group_name
            transUC13['component_name'] = met['met_id'] + '.' + met['met_id'] + '_' + str(trans['quantifier']) + '.Heavy';
            transUC13['met_ID'] = met['met_id'] + '-UC13';
            transUC13['met_name'] = transUC13['met_name'] + '-UC13';
            transUC13['ms_group'] = met['met_id'] + '-UC13';
            transUC13['ms_methodtype'] = 'quantification';
                
            # make UC13 equivalent: q1/q3_mass, precursor/product_formula, precursor/product_exactmass
            if trans['precursor_formula']:
                trans_precursor_formula = Formula(re.sub('[+-]', '', trans['precursor_formula'])) # remove '-' or '+'
                trans['precursor_formula'] = trans_precursor_formula.formula + trans['ms_mode'];
                trans['precursor_exactmass'] = trans_precursor_formula.isotope.mass;
                if 'C' in trans_precursor_formula._elements.keys():
                    nC = trans_precursor_formula._elements['C'][0];
                    tmp = Formula(trans_precursor_formula.formula);
                    tmp._elements['C'] = {13:nC};
                    transUC13_precursor_formula = Formula(tmp.formula);
                else:
                    transUC13_precursor_formula = trans_precursor_formula;
                transUC13['precursor_formula'] = transUC13_precursor_formula.formula + trans['ms_mode'];
                transUC13['precursor_exactmass'] = transUC13_precursor_formula.isotope.mass;
                # substitute for algorithm that checks for unique q1_masses
                # therefore, must ensure that each q1_mass/q3_mass is unique for a given mode in ms_components
                transUC13['q1_mass'] = trans['q1_mass'] + transUC13_precursor_formula.isotope.mass - trans_precursor_formula.isotope.mass;

            if trans['product_formula']:
                trans_product_formula = Formula(re.sub('[+-]', '', trans['product_formula'])) # remove '-' or '+'
                trans['product_formula'] = trans_product_formula.formula + trans['ms_mode'];
                trans['product_exactmass'] = trans_product_formula.isotope.mass;
                if 'C' in trans_product_formula._elements.keys():
                    nC = trans_product_formula._elements['C'][0];
                    tmp = Formula(trans_product_formula.formula);
                    tmp._elements['C'] = {13:nC};
                    transUC13_product_formula = Formula(tmp.formula);
                else:
                    transUC13_product_formula = trans_product_formula;
                transUC13['product_formula'] = transUC13_product_formula.formula + trans['ms_mode'];
                transUC13['product_exactmass'] = transUC13_product_formula.isotope.mass;
                # substitute for algorithm that checks for unique q1_masses
                # therefore, must ensure that each q1_mass/q3_mass is unique for a given mode in ms_components
                transUC13['q3_mass'] = trans['q3_mass'] + transUC13_product_formula.isotope.mass - trans_product_formula.isotope.mass;
            # set defaults: window = 120 sec, dwell = 1, priority, ms_include = False
            mrms_O.append(trans);
            mrms_O.append(transUC13);
        
        stage_io.add_MSComponents(mrms_O);
    def execute_importStructureFile(self,data_I):
        '''import structure files for a list of metabolites and
        update metabolomics standards table
        
        NOTE: '''
        # input:
        #       data_I = [{met_id = list of metabolite ids,
        #                  file_directory = file directory for structure files
        #                       e.g. data/Compound Structure Files/
        #                  file_ext = extension of the file (e.g. .mol)}]
        # output:
        #       update to standards table
        
        data_O = [];
        for data in data_I:
            # generate the fileName
            fileName = data['file_directory'] + data['met_id'] + data['file_ext'];
            structureFile = '';
            # read in the structure file
            with open (fileName, "r") as myfile:
                structureFile=myfile.read()
            # update the standards table with the structure file
            data_O.append({'met_id':data['met_id'],
                           'structure_file':structureFile,
                           'structure_file_extention':data['file_ext']});
        # update standards table
        io = stage00_io();
        io.update_standards_structureFile(data_O);
    def execute_updateFormulaAndMassFromStructure(self, met_ids_I):
        '''update the molecular formula and exact mass of
        standards from imported structure file'''

        data_O = [];
        for met in met_ids_I:
            # query the structure file and extension
            struct_file, struct_file_ext = self.stage00_query.get_structureFile_standards(met);
            # write the structure file to a temporary directory
            struct_file_name = 'data/struct'+struct_file_ext
            with open(struct_file_name, 'w') as outfile:
                outfile.write(struct_file);
            # calculate the formula and exact mass using chemAxon cxcalc
            molfile = os.getcwd() + '/' + struct_file_name
            args = [molfile];
            cmd = 'exactmass';
            res = RunCxcalc(cxcalc_bin,cmd,args)
            res = res.split('\n')[1].split('\t')[1].split('\r')[0]
            exactmass_O = res;
            cmd = 'mass';
            res = RunCxcalc(cxcalc_bin,cmd,args)
            res = res.split('\n')[1].split('\t')[1].split('\r')[0]
            mass_O = res;
            cmd = 'formula';
            res = RunCxcalc(cxcalc_bin,cmd,args)
            res = res.split('\n')[1].split('\t')[1].split('\r')[0]
            formula_O = res;
            # update standards with the formula and exact mass
            data_O.append({'met_id':met,'exactmass':exactmass_O,'mass':mass_O,'formula':formula_O});
        # update standards table
        io = stage00_io();
        io.update_standards_formulaAndMass(data_O);
    def execute_updatePrecursorFormulaAndMass(self, met_ids_I):
        '''update the precusor formula and exact mass of
        ms_components from imported structure file'''
        
        io = stage00_io();
        # get the mass and exact mass for hydrogen
        # NOTE: mass is in aggrement with chemaxon
        exactmass_h = Formula('H').isotope.mass
        mass_h = Formula('H').mass
        data_O = [];
        for met in met_ids_I:
            # query exact mass and formula from standards
            exactMass_O, formula_O = self.stage00_query.get_exactMassAndFormula_standards(met);
            ## calculate the formula and exact mass using chemAxon cxcalc
            ## query the structure file and extension
            #struct_file, struct_file_ext = self.stage00_query.get_structureFile_standards(met);
            ## write the structure file to a temporary directory
            #struct_file_name = 'data/struct'+struct_file_ext
            #with open(struct_file_name, 'w') as outfile:
            #    outfile.write(struct_file);
            ## calculate the formula and exact mass using chemAxon cxcalc
            ## alternatively, one could query standards for the formula
            #molfile = os.getcwd() + '/' + struct_file_name
            #args = [molfile];
            #cmd = 'formula';
            #res = RunCxcalc(cxcalc_bin,cmd,args)
            #res = res.split('\n')[1].split('\t')[1].split('\r')[0]
            #formula_O = res;
            # query ms_components
            mscomponents = [];
            mscomponents = self.stage00_query.get_Q1AndQ3MassAndMode_MSComponents(met);
            if len(mscomponents)==0:
                print ('no component found for ' + met + ' in ms_components')
                continue;
            # calculate the formula, exact mass, and average mass for the ms_mode
            data_tmp = {};
            for msc in mscomponents:
                if msc['ms_mode'] == '-':
                    if met == 'nad' or met == 'nadp': # correct for nad and nadp
                        precursor = Formula(formula_O) - Formula('H2')
                    else:
                        precursor = Formula(formula_O) - Formula('H')
                    data_O.append({'met_id':met,
                                   'q1_mass':msc['q1_mass'],
                                   'q3_mass':msc['q3_mass'],
                                   'precursor_exactmass':precursor.isotope.mass,
                                   'precursor_formula':precursor.formula + '-'});
                elif msc['ms_mode'] == '+':
                    precursor = Formula(formula_O) + Formula('H')
                    data_O.append({'met_id':met,
                                   'q1_mass':msc['q1_mass'],
                                   'q3_mass':msc['q3_mass'],
                                   'precursor_exactmass':precursor.isotope.mass,
                                   'precursor_formula':precursor.formula + '+'});
                else:
                    print ('no ms_mode specified for ' + met)
                    exit(-1);
        # update ms_components table
        io.update_MSComponents_precursorFormulaAndMass(data_O);

        return
    def update_componentNames(self):
        '''update component names for quant and isotopomer methods'''
        return
    def execute_checkPrecursorFormulaAndMass(self, met_ids_I):
        '''check that the formula, q1_mass and precursor_exactmass are consistent'''
        return
    def execute_makeBatchFileCalibrators(self, experiment_id_I, DateAcquisition_I, batch_fileName_I):
        '''Generate the acqusition batch file for the calibrators'''
        return;
    def execute_makeExperimentFromSampleFile(self, sample_fileName_I, nTechReps_I, dil_levels_I):
        '''Populate experiment, samples, sample_physiologicalparameters, sample_description, and sample_storage tables
        NOTE: the sample_file should only contain samples for 1 experiment_id and 1 exp_type if multiple technical replicates
              and/or dilutions are to be made'''

        # Input:
        #   sample_fileName_I = name of the .csv file with sample information
        #   nTechReps_I = the number of technical replicates per biological replicate that should be created
        #   dil_levels_I = additional dilution levels per sample

        io = stage00_io();
        #import sample file and split into respective tables
        sampleDescription_data,samplePhysiologicalParameters_data,\
            sampleStorage_data,sample_data,\
            experiment_data = io.import_sampleFile_add(sample_fileName_I);
        #make technical replicates and dilutions
        if nTechReps_I>0 or len(dil_levels_I)>0:
            # check that there is only 1 experiment_id and 1 exp_type
            experiment_ids = [v['id'] for v in experiment_data];
            experiment_ids_unique = list(set(experiment_ids));
            exp_types = [v['exp_type_id'] for v in experiment_data];
            exp_types_unique = list(set(exp_types));
            if len(experiment_ids_unique)!=1 or len(exp_types_unique)!=1:
                print 'More than 1 experiment_id and/or more than 1 exp_type found';
                print 'This should be changed in future iterations';
                print 'Technical replicates and dilutions will not be made';
                return;
            # make the technical replicates and dilutions
            sampleDescription_data,samplePhysiologicalParameters_data,\
                sampleStorage_data,sample_data,\
                experiment_data = self.make_techRepsAndDils(nTechReps_I, dil_levels_I,
                                                                        sampleDescription_data,samplePhysiologicalParameters_data,
                                                                        sampleStorage_data,
                                                                        sample_data,experiment_data);
            # add the data in order
            io.add_sampleDescription(sampleDescription_data);
            io.add_samplePhysiologicalParameters(samplePhysiologicalParameters_data);
            io.add_sampleStorage(sampleStorage_data);
            io.add_sample(sample_data);
            io.add_experiment(experiment_data);
    def execute_makeBatchFile(self, experiment_id_I, DateAcquisition_I, batch_fileName_I, experiment_type_I=4):
        '''generate the acqusition batch file for the experiment'''

        # Input:
        #   batch_fileName_I = name of the .txt batch file that will be created
        # Output:
        #   batch_fileName_I.txt

        io = stage00_io();
        #query sample and experiment data
        #ordered dilutions.asc(), sample_replicate.asc();
        data_unknown = self.stage00_query.get_batchFileInfo_experimentIDAndExpType(experiment_id_I,'Unknown',exp_type_I=experiment_type_I);
        data_qc = self.stage00_query.get_batchFileInfo_experimentIDAndExpType(experiment_id_I,'QC',exp_type_I=experiment_type_I);
        #generate the batch file
        batchFile_data = []
        batchFile_header = [];
        batchFile_data,batchFile_header = self.make_batchFile(DateAcquisition_I,data_unknown,data_qc);
        io.export_batchFile(batchFile_data, batchFile_header, batch_fileName_I); #analyst cannot read in csv files for some reason, only txt files
    def execute_deleteSamplesFromExperiment(self,experiment_id_I, sample_ids_I):
        '''remove specific samples from an experiment by their sample ID'''

        # NOTES: DELETE statement appears to be broken

        # remove samples from
        # 1. experiment
        # 2. sample
        # 3. sample_description, sample_storage, sample_physiologicalparameters

        dataListDelete = [];
        for si in sample_ids_I:
            dataListDelete.append({'experiment_id':experiment_id_I,
                                   'sample_id':si});
        # remove samples in order
        self.stage00_query.delete_sample_experimentIDAndSampleID_experiment(dataListDelete);
        self.stage00_query.delete_sample_experimentIDAndSampleID_sample(dataListDelete);
        self.stage00_query.delete_sample_experimentIDAndSampleID_sampleDescription(dataListDelete);
        self.stage00_query.delete_sample_experimentIDAndSampleID_sampleStorage(dataListDelete);
        self.stage00_query.delete_sample_experimentIDAndSampleID_samplePhysiologicalParameters(dataListDelete);
    def execute_makeExperimentFromCalibrationFile(self, calibration_fileName_I):
        '''Populate experiment and samples'''

        # Input:
        #   calibration_fileName_I = name of the .csv file with calibrator information

        io = stage00_io();
        #import sample file and split into respective tables
        io.import_calibrationFile_add(calibration_fileName_I);
    def execute_exportCalibrationConcentrations(self, sampleAndComponent_fileName_I, concentrations_fileName_O):
        '''export calibrator concentrations for "cut&paste" into Actual Concentration column in MultiQuant
        when filtering Analytes only'''

        #Input:
        #   sampleAndComponent_fileName_I = .csv file specifying sample_name, sample_type, and component_group_name
        #Output:
        #   concentrations_fileName_O = .csv file specifying sample_name, sample_type, component_group_name, and actual_concentration
        
        io = stage00_io();
        concentrations_O = [];
        met_id_conv_dict = {'Hexose_Pool_fru_glc-D':'glc-D',
                            'Pool_2pg_3pg':'3pg'};
        #import sampleAndComponents
        samplesComponents = [];
        samplesComponents = io.import_calibration_sampleAndComponents(sampleAndComponent_fileName_I);
        for sc in samplesComponents:
            # if met_id is a pool of metabolites, convert to the metabolite
            # that is logged in calibrator tables and standards tables
            if sc['met_id'] in met_id_conv_dict.keys():
                met_id_conv = met_id_conv_dict[sc['met_id']];
            else:
                met_id_conv = sc['met_id'];
            #query calibrator_id and calibrator_level from sample
            calibrator_id,calibrator_level = None,None;
            calibrator_id,calibrator_level = self.stage00_query.get_calibratorIDAndLevel_sampleNameAndSampleType_sample(sc['sample_name'],sc['sample_type']);
            #query calibrator_concentration from calibrator_concentrations
            calibrator_concentration, concentration_units = 'N/A', None;
            if calibrator_id and calibrator_level:
                calibrator_concentration, concentration_units = self.stage00_query.get_calibratorConcentrationAndUnit_metIDAndCalibratorIDAndLevel_calibratorConcentrations(met_id_conv,calibrator_id,calibrator_level);
            concentrations_O.append({'sample_name':sc['sample_name'], 'sample_type':sc['sample_type'],'component_group_name':sc['met_id'], 'actual_concentration':calibrator_concentration});
        io.export_calibrationConcentrations(concentrations_O, concentrations_fileName_O)
    def execute_exportAcqusitionMethod(self,lc_method_I,ms_mode_I,ms_methodtype_I,filename_I):
        '''export the current acqusition method'''
        io = stage00_io();
        # get the data
        amethod = [];
        amethod = self.stage00_query.get_acqusitionMethod(lc_method_I,ms_mode_I,ms_methodtype_I);
        # export the data to csv
        io.export_acquisitionMethod(amethod, filename_I);
    def execute_deleteExperiments(self,experiment_ids_I):
        '''remove an experiment'''

        # NOTES: DELETE statement appears to be broken

        # remove samples from
        # 1. experiment
        # 2. sample
        # 3. sample_description, sample_storage, sample_physiologicalparameters

        dataListDelete = [];
        for experiment_id_I in experiment_ids_I:
            #query the sample IDs in the experiment
            sample_ids = self.stage00_query.get_sampleIDs_experimentID_experiment(experiment_id_I);
            for si in sample_ids:
                dataListDelete.append({'experiment_id':experiment_id_I,
                                   'sample_id':si});
        # remove samples in order
        self.stage00_query.delete_sample_experimentIDAndSampleID_experiment(dataListDelete);
        self.stage00_query.delete_sample_experimentIDAndSampleID_sample(dataListDelete);
        self.stage00_query.delete_sample_experimentIDAndSampleID_sampleDescription(dataListDelete);
        self.stage00_query.delete_sample_experimentIDAndSampleID_sampleStorage(dataListDelete);
        self.stage00_query.delete_sample_experimentIDAndSampleID_samplePhysiologicalParameters(dataListDelete);
    #internal functions
    def make_batchFile(self,DateAcquisition_I,data_unknown_I,data_qc_I):
        '''make an acquisition batch file from sample_description'''
        batchFile_data_O = [];
        batchFile_header_O = [['% header=SampleName','SampleID',
                            'Comments','AcqMethod','ProcMethod',
                            'RackCode','PlateCode','VialPos',
                            'SmplInjVol','DilutFact','WghtToVol',
                            'Type','RackPos','PlatePos','SetName',
                            'OutputFile']];
        n_racks_max = 6; 
        n_pos_max = 51; # pos 52, 53, and 54 are reserved for a water blank;
        cnt_rack = 3;
        cnt_pos = 1;
        injection_order = [];
        cnt_sample = 0;
        cnt_qc = 0;
        cnt_blank = 0;
        cnt_blank_inj = 0;
        n_blank_max_inj = 20;
        vialPos_blank = 54;
        
        # injection order:
        # QC01
        # Blank
        # 9 samples in increasing dilution
        # QCx
        # Blank
        # ...
        if data_qc_I:
            vialPos = cnt_pos;
            rackPos = cnt_rack;
            platePos = 1;
            rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
            setName = DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
            outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
            row = [];
            row.append(data_qc_I[cnt_qc]['sample_name']);
            row.append('');
            row.append('');
            row.append(data_qc_I[cnt_qc]['acquisition_method_id']);
            row.append('none');
            row.append(rackCode);
            row.append('VT54')
            row.append(vialPos);
            row.append(10);
            row.append(1);
            row.append(0);
            row.append(data_qc_I[cnt_qc]['sample_type']);
            row.append(rackPos);
            row.append(platePos);
            row.append(setName);
            row.append(outputFile);
            batchFile_data_O.append(row);
            cnt_pos+=1;
            cnt_qc+=1;
        vialPos = cnt_pos;
        rackPos = cnt_rack;
        platePos = 1;
        rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
        setName = DateAcquisition_I + '_' + data_unknown_I[cnt_sample]['id'];
        outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_unknown_I[cnt_sample]['id'];
        row = [];
        row.append(DateAcquisition_I + '_Blank' + str(cnt_blank));
        row.append('');
        row.append('');
        row.append(data_unknown_I[cnt_sample]['acquisition_method_id']);
        row.append('none');
        row.append(rackCode);
        row.append('VT54')
        row.append(vialPos_blank);
        row.append(10);
        row.append(1);
        row.append(0);
        row.append('Solvent');
        row.append(rackPos);
        row.append(platePos);
        row.append(setName);
        row.append(outputFile);
        batchFile_data_O.append(row);
        cnt_blank+=1;
        cnt_blank_inj+=1;
        for d in data_unknown_I:
            vialPos = cnt_pos;
            rackPos = cnt_rack;
            platePos = 1;
            #rackCode = CStk1-01;
            rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #CStk1-01
            setName = DateAcquisition_I + '_' + d['id'];
            outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + d['id'];
            row = [];
            row.append(d['sample_name']);
            row.append('');
            row.append('');
            row.append(d['acquisition_method_id']);
            row.append('none');
            row.append(rackCode);
            row.append('VT54')
            row.append(vialPos);
            row.append(10);
            row.append(1);
            row.append(0);
            row.append(d['sample_type']);
            row.append(rackPos);
            row.append(platePos);
            row.append(setName);
            row.append(outputFile);
            batchFile_data_O.append(row);

            #row['% header=SampleName']=
            #row['SampleID']=
            #row['Comments']=
            #row['AcqMethod']=
            #row['ProcMethod']=
            #row['RackCode']=
            #row['PlateCode']=
            #row['VialPos']=
            #row['SmplInjVol']=
            #row['DilutFact']=
            #row['WghtToVol']=
            #row['Type']=
            #row['RackPos']=
            #row['PlatePos']=
            #row['SetName']=
            #row['OutputFile']=

            #increment rack and vial positions
            cnt_pos+=1;
            if cnt_pos > n_pos_max:
                cnt_pos = 1;
                cnt_rack+=1;

            cnt_sample +=1;
            if cnt_sample >= 8:
                # add QC and blank
                if data_qc_I:
                    vialPos = cnt_pos;
                    rackPos = cnt_rack;
                    platePos = 1;
                    rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
                    setName = DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
                    outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
                    row = [];
                    row.append(data_qc_I[cnt_qc]['sample_name']);
                    row.append('');
                    row.append('');
                    row.append(data_qc_I[cnt_qc]['acquisition_method_id']);
                    row.append('none');
                    row.append(rackCode);
                    row.append('VT54')
                    row.append(vialPos);
                    row.append(10);
                    row.append(1);
                    row.append(0);
                    row.append(data_qc_I[cnt_qc]['sample_type']);
                    row.append(rackPos);
                    row.append(platePos);
                    row.append(setName);
                    row.append(outputFile);
                    batchFile_data_O.append(row);
                    cnt_pos+=1;
                    cnt_qc+=1;
                    if cnt_pos > n_pos_max:
                        cnt_pos = 1;
                        cnt_rack+=1;

                vialPos = cnt_pos;
                rackPos = cnt_rack;
                platePos = 1;
                rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
                setName = DateAcquisition_I + '_' + d['id'];
                outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + d['id'];
                row = [];
                row.append(DateAcquisition_I + '_Blank' + str(cnt_blank));
                row.append('');
                row.append('');
                row.append(d['acquisition_method_id']);
                row.append('none');
                row.append(rackCode);
                row.append('VT54')
                row.append(vialPos_blank);
                row.append(10);
                row.append(1);
                row.append(0);
                row.append('Solvent');
                row.append(rackPos);
                row.append(platePos);
                row.append(setName);
                row.append(outputFile);
                batchFile_data_O.append(row);
                cnt_blank+=1;
                cnt_blank_inj+=1;
                if cnt_blank_inj > n_blank_max_inj:
                    vialPos_blank-=1;
                cnt_sample = 0;

        # add final QC and Blank
        if data_qc_I:
            vialPos = cnt_pos;
            rackPos = cnt_rack;
            platePos = 1;
            rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
            setName = DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
            outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
            row = [];
            row.append(data_qc_I[cnt_qc]['sample_name']);
            row.append('');
            row.append('');
            row.append(data_qc_I[cnt_qc]['acquisition_method_id']);
            row.append('none');
            row.append(rackCode);
            row.append('VT54')
            row.append(vialPos);
            row.append(10);
            row.append(1);
            row.append(0);
            row.append(data_qc_I[cnt_qc]['sample_type']);
            row.append(rackPos);
            row.append(platePos);
            row.append(setName);
            row.append(outputFile);
            batchFile_data_O.append(row);
            cnt_pos+=1;
            cnt_qc+=1;
        vialPos = cnt_pos;
        rackPos = cnt_rack;
        platePos = 1;
        rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
        setName = DateAcquisition_I + '_' + data_unknown_I[cnt_sample]['id'];
        outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_unknown_I[cnt_sample]['id'];
        row = [];
        row.append(DateAcquisition_I + '_Blank' + str(cnt_blank));
        row.append('');
        row.append('');
        row.append(data_unknown_I[0]['acquisition_method_id']);
        row.append('none');
        row.append(rackCode);
        row.append('VT54')
        row.append(vialPos_blank);
        row.append(10);
        row.append(1);
        row.append(0);
        row.append('Solvent');
        row.append(rackPos);
        row.append(platePos);
        row.append(setName);
        row.append(outputFile);
        batchFile_data_O.append(row);
        cnt_blank+=1;
        cnt_blank_inj+=1;

        return batchFile_data_O, batchFile_header_O;
    def make_techRepsAndDils(self,nTechReps_I, dil_levels_I,
                             sampleDescription_data_I, samplePhysiologicalParameters_data_I, sampleStorage_data_I,
                             sample_data_I,experiment_data_I):
        '''expand experiment and sample tables
        to include technical replicates and dilutions'''

        sampleDescription_data_O = [];
        samplePhysiologicalParameters_data_O = [];
        sampleStorage_data_O = [];
        sample_data_O = [];
        experiment_data_O = [];

        # get the different metabolomics experiment ids:
        experiment_ids = [v['id'] for v in experiment_data_I];
        experiment_ids_unique = list(set(experiment_ids));
        exp_types = [v['exp_type_id'] for v in experiment_data_I];
        exp_types_unique = list(set(exp_types));
        for experiment_id in experiment_ids_unique:
            for exp_type in exp_types_unique:
                # get the bioRep sample names for the experiment
                sample_names = [v['sample_name'] for v in experiment_data_I];
                ## query the maximum number of technical reps based on the experiment id
                #nMaxBioReps = self.stage00_query.get_nMaxBioReps_sampleDescription(experiment_id); # breaks when the number of bio reps is not the same for all samples in an experiment
                for row in sampleDescription_data_I:
                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.stage00_query.get_sampleNameAbbreviation_experimentIDAndSampleID(experiment_id,row['sample_id']);
                    #nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    for rep in range(1,nTechReps_I+1):
                        # add techReps to sample Description
                        # copy sample description fields to techReps
                        sample_id_new = '';
                        sample_id_list = row['sample_id'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_id_list[len(sample_id_list)-1]): 
                            sample_dil = sample_id_list[len(sample_id_list)-1]
                            sample_id_list = sample_id_list[:-1]
                        for l in range(len(sample_id_list)-1):  sample_id_new += sample_id_list[l] + '-';
                        replicate_number = int(sample_id_list[len(sample_id_list)-1]);
                        sample_id_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_id_new += '-' + sample_dil;
                        sample_name_short_new = '';
                        sample_name_short_list = row['sample_name_short'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_name_short_list[len(sample_name_short_list)-1]): 
                            sample_dil = sample_name_short_list[len(sample_name_short_list)-1]
                            sample_name_short_list = sample_name_short_list[:-1]
                        for l in range(len(sample_name_short_list)-1):  sample_name_short_new += sample_name_short_list[l] + '-';
                        sample_name_short_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_name_short_new += '-' + sample_dil;
                        sampleDescription_data_O.append({'sample_id':sample_id_new, #change sample_id
                                                'sample_name_short':sample_name_short_new, #change sample_name_short
                                                'sample_name_abbreviation':row['sample_name_abbreviation'],
                                                'sample_date':row['sample_date'],
                                                'time_point':row['time_point'],
                                                'sample_condition':row['sample_condition'],
                                                'extraction_method_id':row['extraction_method_id'],
                                                'biological_material':row['biological_material'],
                                                'sample_description':row['sample_description'],
                                                'sample_replicate':nMaxBioReps*rep + replicate_number,# modify sample_replicate_biological
                                                'is_added':row['is_added'],
                                                'is_added_units':row['is_added_units'],
                                                'reconstitution_volume':row['reconstitution_volume'],
                                                'reconstitution_volume_units':row['reconstitution_volume_units'],
                                                'sample_replicate_biological':row['sample_replicate_biological'],
                                                'istechnical':True,
                                                'notes':row['notes']});# modify istech (True)
                for row in samplePhysiologicalParameters_data_I:
                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.stage00_query.get_sampleNameAbbreviation_experimentIDAndSampleID(experiment_id,row['sample_id']);
                    #nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    for rep in range(1,nTechReps_I+1):
                        # add techReps to physiological parameters
                        # copy physiological parameters fields to techReps
                        sample_id_new = '';
                        sample_id_list = row['sample_id'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_id_list[len(sample_id_list)-1]): 
                            sample_dil = sample_id_list[len(sample_id_list)-1]
                            sample_id_list = sample_id_list[:-1]
                        for l in range(len(sample_id_list)-1):  sample_id_new += sample_id_list[l] + '-';
                        replicate_number = int(sample_id_list[len(sample_id_list)-1]);
                        sample_id_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_id_new += '-' + sample_dil;
                        samplePhysiologicalParameters_data_O.append({'sample_id':sample_id_new,
                                            'growth_condition_short':row['growth_condition_short'],
                                            'growth_condition_long':row['growth_condition_long'],
                                            'media_short':row['media_short'],
                                            'media_long':row['media_long'],
                                            'isoxic':row['isoxic'],
                                            'temperature':row['temperature'],
                                            'supplementation':row['supplementation'],
                                            'od600':row['od600'],
                                            'vcd':row['vcd'],
                                            'culture_density':row['culture_density'],
                                            'culture_volume_sampled':row['culture_volume_sampled'],
                                            'cells':row['cells'],
                                            'dcw':row['dcw'],
                                            'wcw':row['wcw'],
                                            'vcd_units':row['vcd_units'],
                                            'culture_density_units':row['culture_density_units'],
                                            'culture_volume_sampled_units':row['culture_volume_sampled_units'],
                                            'dcw_units':row['dcw_units'],
                                            'wcw_units':row['wcw_units']});
                for row in sampleStorage_data_I:
                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.stage00_query.get_sampleNameAbbreviation_experimentIDAndSampleID(experiment_id,row['sample_id']);
                    #nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    for rep in range(1,nTechReps_I+1):
                        # add techReps to storage
                        # copy storage parameter fields to techReps
                        # modify box/pos (point back to the biological replicate)
                        sample_id_new = '';
                        sample_id_list = row['sample_id'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_id_list[len(sample_id_list)-1]): 
                            sample_dil = sample_id_list[len(sample_id_list)-1]
                            sample_id_list = sample_id_list[:-1]
                        for l in range(len(sample_id_list)-1):  sample_id_new += sample_id_list[l] + '-';
                        replicate_number = int(sample_id_list[len(sample_id_list)-1]);
                        sample_id_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_id_new += '-' + sample_dil;
                        sampleStorage_data_O.append({'sample_id':sample_id_new,
                                            'sample_label':row['sample_label'],
                                            'ph':row['ph'],
                                            'box':row['box'],
                                            'pos':row['pos']});
                for row in sample_data_I:
                    # add techReps to sample
                    # copy sample fields to techReps
                    # add dilutions to sample
                    # copy sample fields for bio/techReps to dilutions
                    # modify sample_dilution field to reflect the dilution factor

                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.stage00_query.get_sampleNameAbbreviation_experimentIDAndSampleName(experiment_id,row['sample_name']);
                    #nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    for dil in dil_levels_I:
                        sample_name_new_dil = copy(row['sample_name']);
                        sample_name_new_dil += '-' + str(dil) + 'x';
                        sample_data_O.append({'sample_name':sample_name_new_dil,
                                        'sample_type':row['sample_type'],
                                        'calibrator_id':None,
                                        'calibrator_level':None,
                                        'sample_id':row['sample_id'],
                                        'sample_dilution':dil});
                    for rep in range(1,nTechReps_I+1):
                        sample_id_new = '';
                        sample_id_list = row['sample_id'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_id_list[len(sample_id_list)-1]): 
                            sample_dil = sample_id_list[len(sample_id_list)-1]
                            sample_id_list = sample_id_list[:-1]
                        for l in range(len(sample_id_list)-1):  sample_id_new += sample_id_list[l] + '-';
                        replicate_number = int(sample_id_list[len(sample_id_list)-1]);
                        sample_id_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_id_new += '-' + sample_dil;
                        sample_name_new = '';
                        sample_name_list = row['sample_name'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_name_list[len(sample_name_list)-1]): 
                            sample_dil = sample_name_list[len(sample_name_list)-1]
                            sample_name_list = sample_name_list[:-1]
                        for l in range(len(sample_name_list)-1):  sample_name_new += sample_name_list[l] + '-';
                        sample_name_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_name_new += '-' + sample_dil;
                        sample_data_O.append({'sample_name':sample_name_new,
                                            'sample_type':row['sample_type'],
                                            'calibrator_id':None,
                                            'calibrator_level':None,
                                            'sample_id':sample_id_new,
                                            'sample_dilution':row['sample_dilution']});
                        for dil in dil_levels_I:
                            sample_name_new_dil = copy(sample_name_new);
                            sample_name_new_dil += '-' + str(dil) + 'x';
                            sample_data_O.append({'sample_name':sample_name_new_dil,
                                            'sample_type':row['sample_type'],
                                            'calibrator_id':None,
                                            'calibrator_level':None,
                                            'sample_id':sample_id_new,
                                            'sample_dilution':dil});
                        
                for row in experiment_data_I:
                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.stage00_query.get_sampleNameAbbreviation_experimentIDAndSampleName(experiment_id,row['sample_name']);
                    #nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.stage00_query.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    # add techReps and dilutions to experiment
                    # copy experiment fields to techReps and dilutions
                    for dil in dil_levels_I:
                        sample_name_new_dil = copy(row['sample_name']);
                        sample_name_new_dil += '-' + str(dil) + 'x';
                        experiment_data_O.append({'exp_type_id':row['exp_type_id'],
                                            'id':row['id'],
                                            'sample_name':sample_name_new_dil,
                                            'experimentor_id':row['experimentor_id'],
                                            'extraction_method_id':row['extraction_method_id'],
                                            'acquisition_method_id':row['acquisition_method_id'],
                                            'quantitation_method_id':row['quantitation_method_id'],
                                            'internal_standard_id':row['internal_standard_id']});

                    for rep in range(1,nTechReps_I+1):
                        sample_name_new = '';
                        sample_name_list = row['sample_name'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_name_list[len(sample_name_list)-1]): 
                            sample_dil = sample_name_list[len(sample_name_list)-1]
                            sample_name_list = sample_name_list[:-1]
                        for l in range(len(sample_name_list)-1):  sample_name_new += sample_name_list[l] + '-';
                        replicate_number = int(sample_name_list[len(sample_name_list)-1]);
                        sample_name_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_name_new += '-' + sample_dil;
                        experiment_data_O.append({'exp_type_id':row['exp_type_id'],
                                            'id':row['id'],
                                            'sample_name':sample_name_new,
                                            'experimentor_id':row['experimentor_id'],
                                            'extraction_method_id':row['extraction_method_id'],
                                            'acquisition_method_id':row['acquisition_method_id'],
                                            'quantitation_method_id':row['quantitation_method_id'],
                                            'internal_standard_id':row['internal_standard_id']});

                        for dil in dil_levels_I:
                            sample_name_new_dil = copy(sample_name_new);
                            sample_name_new_dil += '-' + str(dil) + 'x';
                            experiment_data_O.append({'exp_type_id':row['exp_type_id'],
                                            'id':row['id'],
                                            'sample_name':sample_name_new_dil,
                                            'experimentor_id':row['experimentor_id'],
                                            'extraction_method_id':row['extraction_method_id'],
                                            'acquisition_method_id':row['acquisition_method_id'],
                                            'quantitation_method_id':row['quantitation_method_id'],
                                            'internal_standard_id':row['internal_standard_id']});

        return sampleDescription_data_O, samplePhysiologicalParameters_data_O, sampleStorage_data_O, sample_data_O,experiment_data_O;
    def make_13CEnsemble(self,formula_str_I):
        '''Make formula for m + 0 to m + # carbons'''
        # input:
        #       formula_str_I = string of formula
        # output:
        #       mass_ensemble_O = ensemble of distributions
        formula_str = re.sub('[+-]', '', formula_str_I) # remove '-' or '+' 

        formula = Formula(formula_str);
        mass_ensemble_O = {};
        if 'C' in formula._elements:
            nC = formula._elements['C'][0]; # count the number of carbon;
            for c in range(nC+1):
                tmp = Formula(formula_str);
                if c==0:tmp._elements['C'] = {0:nC-c};
                elif nC-c==0:tmp._elements['C'] = {13:c};
                else:tmp._elements['C'] = {0:nC-c, 13:c};
                mass_ensemble_O[c] = Formula(tmp.formula);
            return mass_ensemble_O;
        else: 
            nC = 0;
            mass_ensemble_O = {0:formula};
            return mass_ensemble_O

    #TODO:
    def execute_MSComponents_consistencyCheck(self):
        '''
        All method types:
        check that q1 mass matches precursor formula
        check that q3 mas matches product formula
        check that precursor_exactmass matches precursor formula
        check that product_exactmass matches product formula
        Quantification:
        check that the component_name matches the priority
        check that no components have the same q1_mass
        '''

    #table initializations:
    def drop_dataStage01(self):
        try:
            experimentor_id2name.__table__.drop(engine,True);
            experimentor.__table__.drop(engine,True);
            experimentor_list.__table__.drop(engine,True);
            extraction_method.__table__.drop(engine,True);
            standards.__table__.drop(engine,True);
            standards_ordering.__table__.drop(engine,True);
            standards2material.__table__.drop(engine,True);
            standards_storage.__table__.drop(engine,True);
            mix_storage.__table__.drop(engine,True);
            mix_description.__table__.drop(engine,True);
            mix_parameters.__table__.drop(engine,True);
            calibrator_met_parameters.__table__.drop(engine,True);
            calibrator2mix.__table__.drop(engine,True);
            mix2met_id.__table__.drop(engine,True);
            calibrator.__table__.drop(engine,True);
            calibrator_concentrations.__table__.drop(engine,True);
            calibrator_calculations.__table__.drop(engine,True);
            calibrator_met2mix_calculations.__table__.drop(engine,True);
            mix_calculations.__table__.drop(engine,True);
            calibrator_levels.__table__.drop(engine,True);
            MS_components.__table__.drop(engine,True);
            MS_sourceParameters.__table__.drop(engine,True);
            MS_information.__table__.drop(engine,True);
            MS_method.__table__.drop(engine,True);
            MS_component_list.__table__.drop(engine,True);
            autosampler_parameters.__table__.drop(engine,True);
            autosampler_information.__table__.drop(engine,True);
            autosampler_method.__table__.drop(engine,True);
            lc_information.__table__.drop(engine,True);
            lc_gradient.__table__.drop(engine,True);
            lc_parameters.__table__.drop(engine,True);
            lc_method.__table__.drop(engine,True);
            lc_elution.__table__.drop(engine,True);
            acquisition_method.__table__.drop(engine,True);
            quantitation_method.__table__.drop(engine,True);
            quantitation_method_list.__table__.drop(engine,True);
            sample.__table__.drop(engine,True);
            sample_storage.__table__.drop(engine,True);
            sample_physiologicalParameters.__table__.drop(engine,True);
            sample_description.__table__.drop(engine,True);
            sample_massVolumeConversion.__table__.drop(engine,True);
            internal_standard.__table__.drop(engine,True);
            internal_standard_storage.__table__.drop(engine,True);
            experiment_types.__table__.drop(engine,True);
            experiment.__table__.drop(engine,True);
            data_versions.__table__.drop(engine,True);
            biologicalMaterial_storage.__table__.drop(engine,True);
            biologicalMaterial_description.__table__.drop(engine,True);
            biologicalMaterial_geneReferences.__table__.drop(engine,True);
            oligos_description.__table__.drop(engine,True);
            oligos_storage.__table__.drop(engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage01(self,experiment_id_I = None):
        try:
            reset = self.session.query(experimentor_id2name).delete(synchronize_session=False);
            reset = self.session.query(experimentor).delete(synchronize_session=False);
            reset = self.session.query(experimentor_list).delete(synchronize_session=False);
            reset = self.session.query(extraction_method).delete(synchronize_session=False);
            reset = self.session.query(standards).delete(synchronize_session=False);
            reset = self.session.query(standards_ordering).delete(synchronize_session=False);
            reset = self.session.query(standards2material).delete(synchronize_session=False);
            reset = self.session.query(standards_storage).delete(synchronize_session=False);
            reset = self.session.query(mix_storage).delete(synchronize_session=False);
            reset = self.session.query(mix_description).delete(synchronize_session=False);
            reset = self.session.query(mix_parameters).delete(synchronize_session=False);
            reset = self.session.query(calibrator_met_parameters).delete(synchronize_session=False);
            reset = self.session.query(calibrator2mix).delete(synchronize_session=False);
            reset = self.session.query(mix2met_id).delete(synchronize_session=False);
            reset = self.session.query(calibrator).delete(synchronize_session=False);
            reset = self.session.query(calibrator_concentrations).delete(synchronize_session=False);
            reset = self.session.query(calibrator_calculations).delete(synchronize_session=False);
            reset = self.session.query(calibrator_met2mix_calculations).delete(synchronize_session=False);
            reset = self.session.query(mix_calculations).delete(synchronize_session=False);
            reset = self.session.query(calibrator_levels).delete(synchronize_session=False);
            reset = self.session.query(MS_components).delete(synchronize_session=False);
            reset = self.session.query(MS_sourceParameters).delete(synchronize_session=False);
            reset = self.session.query(MS_information).delete(synchronize_session=False);
            reset = self.session.query(MS_method).delete(synchronize_session=False);
            reset = self.session.query(MS_component_list).delete(synchronize_session=False);
            reset = self.session.query(autosampler_parameters).delete(synchronize_session=False);
            reset = self.session.query(autosampler_information).delete(synchronize_session=False);
            reset = self.session.query(autosampler_method).delete(synchronize_session=False);
            reset = self.session.query(lc_information).delete(synchronize_session=False);
            reset = self.session.query(lc_gradient).delete(synchronize_session=False);
            reset = self.session.query(lc_parameters).delete(synchronize_session=False);
            reset = self.session.query(lc_method).delete(synchronize_session=False);
            reset = self.session.query(lc_elution).delete(synchronize_session=False);
            reset = self.session.query(acquisition_method).delete(synchronize_session=False);
            reset = self.session.query(quantitation_method).delete(synchronize_session=False);
            reset = self.session.query(quantitation_method_list).delete(synchronize_session=False);
            reset = self.session.query(sample).delete(synchronize_session=False);
            reset = self.session.query(sample_storage).delete(synchronize_session=False);
            reset = self.session.query(sample_physiologicalParameters).delete(synchronize_session=False);
            reset = self.session.query(sample_description).delete(synchronize_session=False);
            reset = self.session.query(sample_massVolumeConversion).delete(synchronize_session=False);
            reset = self.session.query(internal_standard).delete(synchronize_session=False);
            reset = self.session.query(internal_standard_storage).delete(synchronize_session=False);
            reset = self.session.query(experiment_types).delete(synchronize_session=False);
            reset = self.session.query(experiment).delete(synchronize_session=False);
            reset = self.session.query(data_versions).delete(synchronize_session=False);
            reset = self.session.query(biologicalMaterial_storage).delete(synchronize_session=False);
            reset = self.session.query(biologicalMaterial_description).delete(synchronize_session=False);
            reset = self.session.query(biologicalMaterial_geneReferences).delete(synchronize_session=False);
            reset = self.session.query(oligos_description).delete(synchronize_session=False);
            reset = self.session.query(oligos_storage).delete(synchronize_session=False);

            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage01(self):
        try:
            experimentor_id2name.__table__.create(engine,True);
            experimentor.__table__.create(engine,True);
            experimentor_list.__table__.create(engine,True);
            extraction_method.__table__.create(engine,True);
            standards.__table__.create(engine,True);
            standards_ordering.__table__.create(engine,True);
            standards2material.__table__.create(engine,True);
            standards_storage.__table__.create(engine,True);
            mix_storage.__table__.create(engine,True);
            mix_description.__table__.create(engine,True);
            mix_parameters.__table__.create(engine,True);
            calibrator_met_parameters.__table__.create(engine,True);
            calibrator2mix.__table__.create(engine,True);
            mix2met_id.__table__.create(engine,True);
            calibrator.__table__.create(engine,True);
            calibrator_concentrations.__table__.create(engine,True);
            calibrator_calculations.__table__.create(engine,True);
            calibrator_met2mix_calculations.__table__.create(engine,True);
            mix_calculations.__table__.create(engine,True);
            calibrator_levels.__table__.create(engine,True);
            MS_components.__table__.create(engine,True);
            MS_sourceParameters.__table__.create(engine,True);
            MS_information.__table__.create(engine,True);
            MS_method.__table__.create(engine,True);
            MS_component_list.__table__.create(engine,True);
            autosampler_parameters.__table__.create(engine,True);
            autosampler_information.__table__.create(engine,True);
            autosampler_method.__table__.create(engine,True);
            lc_information.__table__.create(engine,True);
            lc_gradient.__table__.create(engine,True);
            lc_parameters.__table__.create(engine,True);
            lc_method.__table__.create(engine,True);
            lc_elution.__table__.create(engine,True);
            acquisition_method.__table__.create(engine,True);
            quantitation_method.__table__.create(engine,True);
            quantitation_method_list.__table__.create(engine,True);
            sample.__table__.create(engine,True);
            sample_storage.__table__.create(engine,True);
            sample_physiologicalParameters.__table__.create(engine,True);
            sample_description.__table__.create(engine,True);
            sample_massVolumeConversion.__table__.create(engine,True);
            internal_standard.__table__.create(engine,True);
            internal_standard_storage.__table__.create(engine,True);
            experiment_types.__table__.create(engine,True);
            experiment.__table__.create(engine,True);
            data_versions.__table__.create(engine,True);
            material.__table__.create(engine,True);
            biologicalMaterial_storage.__table__.create(engine,True);
            biologicalMaterial_description.__table__.create(engine,True);
            biologicalMaterial_geneReferences.__table__.create(engine,True);
            oligos_description.__table__.create(engine,True);
            oligos_storage.__table__.create(engine,True);

        except SQLAlchemyError as e:
            print(e);