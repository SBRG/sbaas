from analysis.analysis_base import *
from stage02_physiology_query import stage02_physiology_query
from resources.molmass import Formula
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file, write_cobra_model_to_sbml_file
from cobra.io import load_matlab_model
# Dependencies from escher
from escher import Builder

class stage02_physiology_io(base_analysis):

    def __init__(self):
        self.session = Session();
        self.stage02_physiology_query = stage02_physiology_query();
        self.calculate = base_calculate();

    def import_dataStage02PhysiologyModel_sbml(self, model_id_I, date_I, model_sbml):
        '''import isotopomer model from file'''
        dataStage02PhysiologyModelRxns_data = [];
        dataStage02PhysiologyModelMets_data = [];
        dataStage02PhysiologyModels_data,\
            dataStage02PhysiologyModelRxns_data,\
            dataStage02PhysiologyModelMets_data = self._parse_model_sbml(model_id_I, date_I, model_sbml)
        self.add_dataStage02PhysiologyModelMetabolites(dataStage02PhysiologyModelMets_data);
        self.add_dataStage02PhysiologyModelReactions(dataStage02PhysiologyModelRxns_data);
        self.add_dataStage02PhysiologyModels(dataStage02PhysiologyModels_data);

    def _parse_model_sbml(self,model_id_I,date_I,filename_I):
        # Read in the sbml file
        cobra_model = create_cobra_model_from_sbml_file(filename_I, print_time=True)
        model_data = [];
        model_data_tmp = {};
        # parse out model metadata
        model_data_tmp['model_id'] = model_id_I;
        model_data_tmp['model_name'] = None;
        model_data_tmp['date'] = date_I;
        model_data_tmp['model_description'] = cobra_model.description;
        with open(filename_I, 'r') as f:
            model_data_tmp['model_file'] = f.read();
        model_data_tmp['file_type'] = 'sbml'
        model_data.append(model_data_tmp)
        reaction_data = [];
        # parse out reaction data
        for r in cobra_model.reactions:
            reaction_data_dict = {};
            reaction_data_dict['model_id'] = model_id_I
            reaction_data_dict['rxn_id'] = r.id
            reaction_data_dict['rxn_name'] = r.name
            reaction_data_dict['equation'] = r.build_reaction_string()
            reaction_data_dict['subsystem'] = r.subsystem
            reaction_data_dict['gpr'] = r.gene_reaction_rule
            reaction_data_dict['genes'] = []
            genes = r.genes;
            for g in genes:
                reaction_data_dict['genes'].append(g.id);
            reaction_data_dict['reactants_stoichiometry'] = [];
            reaction_data_dict['reactants_ids'] = [];
            reactants = r.reactants;
            for react in reactants:
                reaction_data_dict['reactants_stoichiometry'].append(r.get_coefficient(react.id));
                reaction_data_dict['reactants_ids'].append(react.id);
            reaction_data_dict['products_stoichiometry'] = [];
            reaction_data_dict['products_ids'] = [];
            products = r.products;
            for prod in products:
                reaction_data_dict['products_stoichiometry'].append(r.get_coefficient(prod.id));
                reaction_data_dict['products_ids'].append(prod.id);
            reaction_data_dict['lower_bound'] = r.lower_bound
            reaction_data_dict['upper_bound'] = r.upper_bound
            reaction_data_dict['objective_coefficient'] = r.objective_coefficient
            reaction_data_dict['flux_units'] = 'mmol*gDW-1*hr-1'
            reaction_data_dict['reversibility'] = r.reversibility
            reaction_data_dict['used_'] = True
            reaction_data_dict['comment_'] = None;
            reaction_data.append(reaction_data_dict);
        metabolite_data = [];
        # parse out metabolite data
        for met in cobra_model.metabolites:
            metabolite_data_tmp = {};
            metabolite_data_tmp['model_id'] = model_id_I
            metabolite_data_tmp['met_name'] = met.name;
            metabolite_data_tmp['met_id'] = met.id;
            formula = {};
            for k,v in met.formula.elements.iteritems():
                formula[k] = {0:v};
            tmp = Formula()
            tmp._elements=formula
            metabolite_data_tmp['formula'] = tmp.formula;
            metabolite_data_tmp['charge'] = met.charge
            metabolite_data_tmp['compartment'] = met.compartment
            metabolite_data_tmp['bound'] = met._bound
            metabolite_data_tmp['constraint_sense'] = met._constraint_sense
            metabolite_data_tmp['used_'] = True
            metabolite_data_tmp['comment_'] = None;
            metabolite_data.append(metabolite_data_tmp);

        return model_data,reaction_data,metabolite_data

    def import_dataStage02PhysiologyModels_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologyModels(data.data);
        data.clear_data();

    def add_dataStage02PhysiologyModels(self, data_I):
        '''add rows of data_stage02_physiology_models'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_physiology_models(d['model_id'],
                        d['model_name'],
                        d['model_description'],
                            d['model_file'],
                            d['file_type'],
                        d['date']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02PhysiologyModels_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologyModels(data.data);
        data.clear_data();

    def update_dataStage02PhysiologyModels(self,data_I):
        #Not yet tested
        '''update rows of data_stage02_physiology_models'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_physiology_models).filter(
                            data_stage02_physiology_models.id.like(d['id'])).update(
                            {'model_id':d['model_id'],
                            'model_name':d['model_name'],
                            'model_description':d['model_description'],
                            'file':d['model_file'],
                            'file_type':d['file_type'],
                            'date':d['date']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02PhysiologyModelReactions_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologyModelReactions(data.data);
        data.clear_data();

    def add_dataStage02PhysiologyModelReactions(self, data_I):
        '''add rows of data_stage02_physiology_modelReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_physiology_modelReactions(d['model_id'],
                            d['rxn_id'],
                            d['rxn_name'],
                            d['equation'],
                            d['subsystem'],
                            d['gpr'],
                            d['genes'],
                            d['reactants_stoichiometry'],
                            d['products_stoichiometry'],
                            d['reactants_ids'],
                            d['products_ids'],
                            d['lower_bound'],
                            d['upper_bound'],
                            d['objective_coefficient'],
                            d['flux_units'],
                            d['reversibility'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02PhysiologyModelReactions_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologyModelReactions(data.data);
        data.clear_data();

    def update_dataStage02PhysiologyModelReactions(self,data_I):
        #Not yet tested
        '''update rows of data_stage02_physiology_modelReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_physiology_modelReactions).filter(
                            data_stage02_physiology_modelReactions.id.like(d['id'])).update(
                            {'model_id':d['model_id'],
                                'rxn_id':d['rxn_id'],
                                'rxn_name':d['rxn_name'],
                                'equation':d['equation'],
                                'subsystem':d['subsystem'],
                                'gpr':d['gpr'],
                                'genes':d['genes'],
                                'reactants_stoichiometry':d['reactants_stoichiometry'],
                                'products_stoichiometry':d['products_stoichiometry'],
                                'reactants_ids':d['reactants_ids'],
                                'products_ids':d['products_ids'],
                                'lower_bound':d['lower_bound'],
                                'upper_bound':d['upper_bound'],
                                'objective_coefficient':d['objective_coefficient'],
                                'flux_units':d['flux_units'],
                                'reversibility':d['reversibility'],
                                'used_':d['used_'],
                                'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02PhysiologyModelMetabolites_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologyModelMetabolites(data.data);
        data.clear_data();

    def add_dataStage02PhysiologyModelMetabolites(self, data_I):
        '''add rows of data_stage02_physiology_modelMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_physiology_modelMetabolites(d['model_id'],
                        d['met_name'],
                        d['met_id'],
                        d['formula'],
                        d['charge'],
                        d['compartment'],
                        d['bound'],
                        d['constraint_sense'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02PhysiologyModelMetabolites_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologyModelMetabolites(data.data);
        data.clear_data();

    def update_dataStage02PhysiologyModelMetabolites(self,data_I):
        '''update rows of data_stage02_physiology_modelMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_physiology_modelMetabolites).filter(
                            data_stage02_physiology_modelMetabolites.id.like(d['id'])).update(
                            {'model_id':d['model_id'],
                                'met_name':d['met_name'],
                                'met_id':d['met_id'],
                                'formula':d['formula'],
                                'charge':d['charge'],
                                'compartment':d['compartment'],
                                'bound':d['bound'],
                                'constraint_sense':d['constraint_sense'],
                                'used_':d['used_'],
                                'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02PhysiologySimulation_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02PhysiologySimulation(data.data);
        data.clear_data();

    def add_dataStage02PhysiologySimulation(self, data_I):
        '''add rows of data_stage02_physiology_simulation'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_physiology_simulation(d['experiment_id'],
                        d['model_id'],
                        d['sample_name_abbreviation'],
                        #d['time_point'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02PhysiologySimulation_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02PhysiologySimulation(data.data);
        data.clear_data();

    def update_dataStage02PhysiologySimulation(self,data_I):
        '''update rows of data_stage02_physiology_simulation'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_physiology_simulation).filter(
                            data_stage02_physiology_simulation.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            #'time_point':d['time_point'],
                            'compartment_id':d['compartment_id'],
                            'pH':d['pH'],
                            'temperature':d['temperature'],
                            'temperature_units':d['temperature_units'],
                            'ionic_strength':d['ionic_strength'],
                            'ionic_strength_units':d['ionic_strength_units'],
                            'used_':d['used_'],
                            'comment_I':d['comment_I']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_data_stage02PhysiologyMeasuredFluxes(self, data_I):
        '''add rows of data_stage02_physiology_measuredFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_physiology_measuredFluxes(d['experiment_id'],
                            d['model_id'],
                            d['sample_name_abbreviation'],
                            #d['time_point'],
                            d['rxn_id'],
                            d['flux_average'],
                            d['flux_stdev'],
                            d['flux_lb'],
                            d['flux_ub'],
                            d['flux_units'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_data_stage02PhysiologyMeasuredFluxes(self,data_I):
        #TODO:
        '''update rows of data_stage02_physiology_measuredFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_physiology_measuredFluxes).filter(
                            data_stage02_physiology_measuredFluxes.id==d['id']
                            ).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            #'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
                            'flux_average':d['flux_average'],
                            'flux_stdev':d['flux_stdev'],
                            'flux_lb':d['flux_lb'],
                            'flux_ub':d['flux_ub'],
                            'flux_units':d['flux_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_samplingAnalysis_escher(self,experiment_id_I,model_ids_I=[],
                     model_ids_dict_I={},
                     sample_name_abbreviations_I=[],
                     filename=['visualization/data/','/physiology/metabolicmap/','sampling/']):
        '''export sampling data for visualization'''
        
        # get the model ids:
        filter_O = {};
        filter_O['model_id'] = [];
        filter_O['sample'] = [];
        filter_O['map_id'] = [];
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_physiology_query.get_modelID_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for model_id in model_ids:
            filter_mi_str = 'model_id/'+ model_id;
            filter_O['model_id'].append(filter_mi_str);
            print 'exporting sampling analysis for model_id ' + model_id;
            # get the cobra model
            if model_ids_dict_I:
                cobra_model = model_ids_dict_I[model_id];
            else:
                cobra_model_sbml = None;
                cobra_model_sbml = self.stage02_physiology_query.get_row_modelID_dataStage02PhysiologyModels(model_id);
                # write the model to a temporary file
                with open('data/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                # Read in the sbml file and define the model conditions
                cobra_model = create_cobra_model_from_sbml_file('data/cobra_model_tmp.xml', print_time=True);
            # get sample_name_abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.stage02_physiology_query.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage02PhysiologySimulation(experiment_id_I,model_id);
            for sna in sample_name_abbreviations:
                filter_sna_str = 'model_id/'+ model_id +'/sample/'+sna;
                filter_O['sample'].append(filter_sna_str);
                print 'exporting sampling analysis for sample_name_abbreviation ' + sna;
                # get sampled data 
                sampling_ave = {}
                sampling_ave = self.stage02_physiology_query.get_rowsEscher_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(experiment_id_I,model_id,sna)
                for map_id in ['Alternate Carbon Metabolism',\
                    'Amino Acid Metabolism',\
                    'Central Metabolism',\
                    'Cofactor Biosynthesis',\
                    'Inorganic Ion Metabolism',\
                    'Nucleotide Metabolism']:
                    filter_map_str = 'model_id/'+ model_id +'/sample/'+sna+'/map_id/'+map_id;
                    filter_O['map_id'].append(filter_map_str);
                    print 'exporting sampling analysis for map_id ' + map_id;
                    # generate the map html using escher
                    map_json = json.load(open('data/escher_maps/' + map_id + '.json','rb'));
                    map = Builder(map_json=json.dumps(map_json), reaction_data=sampling_ave);
                    html_file = map._get_html(menu='all',enable_editing=True)
                    filename_str = filename[0] + experiment_id_I + filename[1] + filename[2] + model_id + '_' + sna + '_' + map_id + '.html';
                    with open(filename_str,'w') as file:
                        file.write(html_file);
        # dump the filter data to a json file
        json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
        filename_str = filename[0] + experiment_id_I + filename[1] + filename[2] + 'filter.js'
        with open(filename_str,'w') as file:
            file.write(json_str);

    def export_samplingAnalysisComparison_escher(self,experiment_id_I,sample_name_abbreviation_base,
                    model_ids_I=[],
                    model_ids_dict_I={},
                     sample_name_abbreviations_I=[],
                     filename=['visualization/data/','/physiology/metabolicmap/','sampling/']):
        '''export sampling data for visualization'''
        
        # get the model ids:
        filter_O = {};
        filter_O['model_id'] = [];
        filter_O['sample'] = [];
        filter_O['map_id'] = [];
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_physiology_query.get_modelID_experimentID_datastage02physiologyExperiment(experiment_id_I);
        for model_id in model_ids:
            filter_mi_str = 'model_id/'+ model_id;
            filter_O['model_id'].append(filter_mi_str);
            print 'exporting sampling analysis for model_id ' + model_id;
            # get the cobra model
            if model_ids_dict_I:
                cobra_model = model_ids_dict_I[model_id];
            else:
                cobra_model_sbml = None;
                cobra_model_sbml = self.stage02_physiology_query.get_row_modelID_datastage02physiologyModels(model_id);
                # write the model to a temporary file
                with open('data/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                # Read in the sbml file and define the model conditions
                cobra_model = create_cobra_model_from_sbml_file('data/cobra_model_tmp.xml', print_time=True);
            # get sample_name_abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.stage02_physiology_query.get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_datastage02physiologyExperiment(experiment_id_I,model_id,tp);
            sample_name_abbreviations = [sna for sna in sample_name_abbreviations if sna !=sample_name_abbreviation_base]
            # get information about the sample to be compared
            sampling_base = {}
            sampling_base = self.stage02_physiology_query.get_rowsEscher_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(experiment_id_I,model_id,sample_name_abbreviation_base)
            for sna in sample_name_abbreviations:
                filter_sna_str = 'model_id/'+ model_id +'/sample/'+sample_name_abbreviation_base+'_vs_'+sna;
                filter_O['sample'].append(filter_sna_str);
                print 'exporting sampling analysis for sample_name_abbreviation ' + sample_name_abbreviation_base+'_vs_'+sna;
                # get sampleddata
                sampling_ave = {}
                sampling_ave = self.stage02_physiology_query.get_rowsEscher_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(experiment_id_I,model_id,sna)
                # make the data structure
                sampling_diff = [sampling_base,sampling_ave];
                for map_id in ['Alternate Carbon Metabolism',\
                    'Amino Acid Metabolism',\
                    'Central Metabolism',\
                    'Cofactor Biosynthesis',\
                    'Inorganic Ion Metabolism',\
                    'Nucleotide Metabolism']:
                    filter_map_str = 'model_id/'+ model_id +'/sample/'+sample_name_abbreviation_base+'_vs_'+sna+'/map_id/'+map_id;
                    filter_O['map_id'].append(filter_map_str);
                    print 'exporting sampling analysis for map_id ' + map_id;
                    # generate the map html using escher
                    map_json = json.load(open('data/escher_maps/' + map_id + '.json','rb'));
                    map = Builder(map_json=json.dumps(map_json), reaction_data=sampling_diff);
                    #html_file = map._get_html(scroll_behavior='zoom')
                    html_file = map._get_html(menu='all',enable_editing=True)
                    filename_str = filename[0] + experiment_id_I + filename[1] + filename[2] + model_id + '_' + sample_name_abbreviation_base+'_vs_'+sna + '_' + map_id + '.html';
                    with open(filename_str,'w') as file:
                        file.write(html_file);
        # dump the filter data to a json file
        json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
        filename_str = filename[0] + experiment_id_I + filename[1] + filename[2] + 'filter.js'
        with open(filename_str,'w') as file:
            file.write(json_str);

    #TODO
    def export_samplingAnalysisComparison_csv(self,experiment_id_I,sample_name_abbreviation_base,
                    model_ids_I=[],
                    model_ids_dict_I={},
                     time_points_I=[],
                     sample_name_abbreviations_I=[],
                     filename=['data/_output/','sampling_comparison.csv']):
        '''export sampling data comparison'''
        
        # get the model ids:
        data_O = [];
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_physiology_query.get_modelID_experimentID_datastage02physiologyExperiment(experiment_id_I);
        for model_id in model_ids:
            print 'exporting sampling analysis for model_id ' + model_id;
            # get the cobra model
            if model_ids_dict_I:
                cobra_model = model_ids_dict_I[model_id];
            else:
                cobra_model_sbml = None;
                cobra_model_sbml = self.stage02_physiology_query.get_row_modelID_datastage02physiologyModels(model_id);
                # write the model to a temporary file
                with open('data/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                # Read in the sbml file and define the model conditions
                cobra_model = create_cobra_model_from_sbml_file('data/cobra_model_tmp.xml', print_time=True);
            # get the time-points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage02_physiology_query.get_timePoints_experimentIDAndModelID_datastage02physiologyExperiment(experiment_id_I,model_id);
            for tp in time_points:
                print 'exporting sampling analysis for time_point ' + tp;
                # get sample_name_abbreviations
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage02_physiology_query.get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_datastage02physiologyExperiment(experiment_id_I,model_id,tp);
                sample_name_abbreviations = [sna for sna in sample_name_abbreviations if sna !=sample_name_abbreviation_base]
                # get information about the sample to be compared
                concentrations_base = {};
                concentrations_base = self.stage02_physiology_query.get_rowsEscher_experimentIDAndTimePointAndSampleNameAbbreviations_datastage02physiologyMetabolomicsData(experiment_id_I,tp,sample_name_abbreviation_base);
                # get tcc
                tcc_base = [];
                tcc_base = self.stage02_physiology_query.get_rows_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_datastage02physiologyTCC(experiment_id_I,model_id,tp,sample_name_abbreviation_base,measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I);
                for sna in sample_name_abbreviations:
                    print 'exporting sampling analysis for sample_name_abbreviation ' + sample_name_abbreviation_base+'_vs_'+sna;
                    for tcc_b in tcc_base:
                        # get tcc
                        tcc = {};
                        tcc = self.stage02_physiology_query.get_row_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_datastage02physiologyTCC(experiment_id_I,model_id,tp,sna,tcc_b['rxn_id'],tcc_b['dG_r_lb'],tcc_b['dG_r_ub'],measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I);
                        # record data
                        if tcc:
                            data_O.append({'experiment_id':experiment_id_I,
                            'model_id':model_id,
                            'sample_name_abbreviation':sna,
                            'time_point':tp,
                            'rxn_id':tcc['rxn_id'],
                            'dG_r_units':tcc['dG_r_units'],
                            'dG_r_lb_base':tcc_b['dG_r_lb'],
                            'dG_r_lb':tcc['dG_r_lb'],
                            'dG_r_ub_base':tcc_b['dG_r_ub'],
                            'dG_r_ub':tcc['dG_r_ub'],
                            'displacement_lb_base':tcc_b['displacement_lb'],
                            'displacement_lb':tcc['displacement_lb'],
                            'displacement_ub_base':tcc_b['displacement_ub'],
                            'displacement_ub':tcc['displacement_ub'],
                            'feasible_base':tcc_b['feasible'],
                            'feasible':tcc['feasible']});
        # write data to csv
        headers = ['experiment_id',
                            'model_id',
                            'sample_name_abbreviation',
                            'time_point',
                            'rxn_id',
                            'dG_r_units',
                            'dG_r_lb_base',
                            'dG_r_lb',
                            'dG_r_ub_base',
                            'dG_r_ub',
                            'displacement_lb_base',
                            'displacement_lb',
                            'displacement_ub_base',
                            'displacement_ub',
                            'feasible_base',
                            'feasible']
        io = base_exportData(data_O);
        filename_str = filename[0] + experiment_id_I + filename[1];
        io.write_dict2csv(filename_str,headers);
    def _parse_model_json(self,model_id_I,date_I,filename_I):
        # Read in the sbml file and define the model conditions
        cobra_model = load_json_model(filename_I);
        model_data = [];
        model_data_tmp = {};
        # parse out model metadata
        model_data_tmp['model_id'] = model_id_I;
        model_data_tmp['model_name'] = None;
        model_data_tmp['date'] = date_I;
        model_data_tmp['model_description'] = cobra_model.description;
        with open(filename_I, 'r') as f:
            model_data_tmp['model_file'] = f.read();
        model_data_tmp['file_type'] = 'json'
        model_data.append(model_data_tmp)
        reaction_data = [];
        # parse out reaction data
        for r in cobra_model.reactions:
            reaction_data_dict = {};
            reaction_data_dict['model_id'] = model_id_I
            reaction_data_dict['rxn_id'] = r.id
            reaction_data_dict['rxn_name'] = r.name
            reaction_data_dict['equation'] = r.build_reaction_string()
            reaction_data_dict['subsystem'] = r.subsystem
            reaction_data_dict['gpr'] = r.gene_reaction_rule
            reaction_data_dict['genes'] = []
            genes = r.genes;
            for g in genes:
                reaction_data_dict['genes'].append(g.id);
            reaction_data_dict['reactants_stoichiometry'] = [];
            reaction_data_dict['reactants_ids'] = [];
            reactants = r.reactants;
            for react in reactants:
                reaction_data_dict['reactants_stoichiometry'].append(r.get_coefficient(react.id));
                reaction_data_dict['reactants_ids'].append(react.id);
            reaction_data_dict['products_stoichiometry'] = [];
            reaction_data_dict['products_ids'] = [];
            products = r.products;
            for prod in products:
                reaction_data_dict['products_stoichiometry'].append(r.get_coefficient(prod.id));
                reaction_data_dict['products_ids'].append(prod.id);
            reaction_data_dict['lower_bound'] = r.lower_bound
            reaction_data_dict['upper_bound'] = r.upper_bound
            reaction_data_dict['objective_coefficient'] = r.objective_coefficient
            reaction_data_dict['flux_units'] = 'mmol*gDW-1*hr-1'
            reaction_data_dict['reversibility'] = r.reversibility
            #reaction_data_dict['reactants_stoichiometry_tracked'] = None;
            #reaction_data_dict['products_stoichiometry_tracked'] = None;
            #reaction_data_dict['reactants_ids_tracked'] = None;
            #reaction_data_dict['products_ids_tracked'] = None;
            #reaction_data_dict['reactants_mapping'] = None;
            #reaction_data_dict['products_mapping'] = None;
            #reaction_data_dict['rxn_equation'] = None;
            reaction_data_dict['fixed'] = None;
            reaction_data_dict['free'] = None;
            reaction_data_dict['weight'] = None;
            reaction_data_dict['used_'] = True
            reaction_data_dict['comment_'] = None;
            reaction_data.append(reaction_data_dict);
        metabolite_data = [];
        # parse out metabolite data
        for met in cobra_model.metabolites:
            metabolite_data_tmp = {};
            metabolite_data_tmp['model_id'] = model_id_I
            metabolite_data_tmp['met_name'] = met.name;
            metabolite_data_tmp['met_id'] = met.id;
            formula = {};
            for k,v in met.formula.elements.iteritems():
                formula[k] = {0:v};
            tmp = Formula()
            tmp._elements=formula
            metabolite_data_tmp['formula'] = tmp.formula;
            metabolite_data_tmp['charge'] = met.charge
            metabolite_data_tmp['compartment'] = met.compartment
            metabolite_data_tmp['bound'] = met._bound
            metabolite_data_tmp['constraint_sense'] = met._constraint_sense
            #metabolite_data_tmp['met_elements'] = None;
            #metabolite_data_tmp['met_atompositions'] = None;
            #metabolite_data_tmp['balanced'] = None;
            #metabolite_data_tmp['met_symmetry'] = None;
            #metabolite_data_tmp['met_symmetry_atompositions'] = None;
            metabolite_data_tmp['used_'] = True
            metabolite_data_tmp['comment_'] = None;
            metabolite_data.append(metabolite_data_tmp);

        return model_data,reaction_data,metabolite_data