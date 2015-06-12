from sys import exit
from math import log, sqrt, exp
import operator, json, csv
from analysis.analysis_base.base_calculate import base_calculate
from copy import copy
# Dependencies from 3rd party
import h5py
import scipy.io
import numpy
from numpy import histogram, mean, std, loadtxt, savetxt
import matplotlib as mpl
import matplotlib.pyplot as plt
from resources.molmass import Formula
# Dependencies from cobra
from cobra.io.mat import load_matlab_model,save_matlab_model
#from cobra.mlab import matlab_cobra_struct_to_python_cobra_object
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra.flux_analysis import flux_variability_analysis, single_deletion
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis.objective import update_objective

class cobra_sampling(base_calculate):

    def __init__(self,data_dir_I=None,model_I=None,loops_I=[]):#,sampler_I=None):
        if data_dir_I:self.data_dir =  data_dir_I;
        else: self.data_dir = None;
        if model_I: self.model = model_I;
        else: self.model = None;
        if loops_I: self.loops = loops_I;
        else: self.loops = [];
        #if sampler_I: self.sampler = sampler_I;
        #else: self.sampler = [];
        self.points = {};
        self.points_statistics = {};
        self.points_metabolite = {};
        self.points_subsystem = {};
        self.mixed_fraction = None;
        self.calculate = base_calculate();
    # import functions
    def get_points_numpy(self,numpy_data,model_sbml=None):
        '''load sampling points from numpy file'''

        # extract information about the file
        import os, time
        from datetime import datetime
        from stat import ST_SIZE, ST_MTIME
        try:
            st = os.stat(self.data_dir + '/' + numpy_data)
        except IOError:
            print("failed to get information about", self.data_dir + '/' + numpy_data)
            return;
        else:
            file_size = st[ST_SIZE]
            simulation_dateAndTime_struct = time.localtime(st[ST_MTIME])
            simulation_dateAndTime = datetime.fromtimestamp(time.mktime(simulation_dateAndTime_struct))

        # load points from numpy file
        points = loadtxt(numpy_data);

        # Read in the sbml file and define the model conditions
        if model_sbml: self.model = create_cobra_model_from_sbml_file(model_sbml, print_time=True)

        points_dict = {};
        for i,r in enumerate(cobra_model.reactions):
            # extract points
            points_dict[r_id_conv]=points[i,:];

        self.points = points_dict;
        #self.mixed_fraction = mixed_fraction;
        self.simulation_dateAndTime = simulation_dateAndTime;
    def get_points_matlab(self,matlab_data,sampler_model_name='sampler_out'):
        '''load sampling points from MATLAB'''

        # extract information about the file
        import os, time
        from datetime import datetime
        from stat import ST_SIZE, ST_MTIME
        try:
            st = os.stat(self.data_dir + '/' + matlab_data)
        except IOError:
            print("failed to get information about", self.data_dir + '/' + matlab_data)
            return;
        else:
            file_size = st[ST_SIZE]
            simulation_dateAndTime_struct = time.localtime(st[ST_MTIME])
            simulation_dateAndTime = datetime.fromtimestamp(time.mktime(simulation_dateAndTime_struct))

        # load model from MATLAB file
        try:
            model = load_matlab_model(self.data_dir + '/' + matlab_data,sampler_model_name);
        except NotImplementedError as e:
            print(e);
            model_tmp = h5py.File(self.data_dir + '/' + matlab_data,'r')['sampler_out'];
            #model = matlab_cobra_struct_to_python_cobra_object(matlab_struct)
            model = self.model;

        # load sample points from MATLAB file into numpy array
        try:
            points = scipy.io.loadmat(self.data_dir + '/' + matlab_data)[sampler_model_name]['points'][0][0];
            mixed_fraction=scipy.io.loadmat(self.data_dir + '/' + matlab_data)['mixedFrac'][0][0];
        except NotImplementedError as e:
            print(e);
            points = h5py.File(self.data_dir + '/' + matlab_data,'r')[sampler_model_name]['points'];
            points = numpy.array(points);
            mixed_fraction=h5py.File(self.data_dir + '/' + matlab_data,'r')['mixedFrac'][0][0];
        #mat = scipy.io.loadmat('data/EvoWt.mat')
        #points = mat['model_WT_sampler_out']['points'][0][0]

        points_dict = {};
        for i,r in enumerate(model.reactions):
            # convert names:
            r_id_conv = r.id.replace('-','_DASH_');
            r_id_conv = r_id_conv.replace('(','_LPAREN_');
            r_id_conv = r_id_conv.replace(')','_RPAREN_');
            # extract points
            points_dict[r_id_conv]=points[i,:];

        self.points = points_dict;
        self.model = model;
        self.mixed_fraction = mixed_fraction;
        self.simulation_dateAndTime = simulation_dateAndTime;
    # export functions
    def export_points_numpy(self,filename):
        '''export sampling points'''

        savetxt(filename,self.points);
    def export_sampling_matlab(self,cobra_model,fraction_optimal = None, filename_model='sample_model.mat',filename_script='sample_script.m', filename_points='points.mat',
                               solver_id_I='gurobi',n_points_I = None, n_steps_I = 20000, max_time_I = None):
        '''export model and script for sampling using matlab cobra_toolbox'''
        ## copy the model:
        #cobra_model_copy = cobra_model.copy();
        # convert numerical input to string
        n_points,n_steps,max_time = '[]','[]','[]';
        if n_points_I:
            n_points = n_points_I;
        if n_steps_I:
            n_steps = n_steps_I;
        if max_time_I:
            max_time = max_time_I;
        # confine the objective to a fraction of maximum optimal
        if fraction_optimal:
            # optimize
            cobra_model.optimize(solver_id_I);
            objective = [x.id for x in cobra_model.reactions if x.objective_coefficient == 1]
            cobra_model.reactions.get_by_id(objective[0]).upper_bound = fraction_optimal * cobra_model.solution.f;
        # write model to mat
        save_matlab_model(cobra_model,self.data_dir + '/' + filename_model);
        ## write model to xml
        #write_sbml_model(cobra_model,'data/sampling/sampler.xml');
        # write the sampling script to file
        #[sampleStructOut, mixedFraction] = gpSampler(sampleStruct, nPoints, bias, maxTime, maxSteps, threads, nPointsCheck)
        mat_script = "% initialize with Tomlab_CPLEX\n";
        mat_script +="load('" + self.data_dir + '/' + filename_model + "')\n";
        mat_script +="initCobraToolbox();\n";
        mat_script +="% sample\n";
        mat_script +="[sampler_out, mixedFrac] = gpSampler(" + cobra_model.description
        mat_script +=(", %s, [], %s, %s, [], true);\n" %(n_points,n_steps,max_time));
        mat_script +="[sampler_out, mixedFrac] = gpSampler(sampler_out";
        mat_script +=(", %s, [], %s, %s, [], true);\n" %(n_points,n_steps,max_time));
        mat_script +="save('"+ self.data_dir + '/' + filename_points + "','sampler_out', 'mixedFrac');";
        with open(self.data_dir + '/' + filename_script,'w') as f:
            f.write(mat_script);
    # plotting functions
    def plot_points_histogram(self,reaction_lst=[]):
        '''plot sampling points as a histogram'''
        if not reaction_lst:
            reaction_lst = ['ENO','FBA','FBP','G6PP','GAPD','GLBRAN2',
                        'GLCP','GLCP2','GLDBRAN2','HEX1','PDH','PFK',
                        'PGI','PGK','PGM','PPS','PYK','TPI','ENO_reverse',
                        'FBA_reverse','GAPD_reverse','PGI_reverse',
                        'PGK_reverse','PGM_reverse','TPI_reverse']
        for r in reaction_lst:
            # loop through each reaction in the list
            plt.figure()
            n, bins, patches = plt.hist(self.points[r],50,label = [r])
            plt.legend()
            plt.show()
    def plot_points_boxAndWhiskers(self,reaction_lst=[]):
        '''plot sampling points as box and whiskers plots'''
        if not reaction_lst:
            reaction_lst = ['ENO','FBA','FBP','G6PP','GAPD','GLBRAN2',
                        'GLCP','GLCP2','GLDBRAN2','HEX1','PDH','PFK',
                        'PGI','PGK','PGM','PPS','PYK','TPI','ENO_reverse',
                        'FBA_reverse','GAPD_reverse','PGI_reverse',
                        'PGK_reverse','PGM_reverse','TPI_reverse']
        for r in reaction_lst:
            # loop through each reaction in the list
            plt.figure()
            fig, ax = plt.subplots()
            bp = ax.boxplot(self.points[r], sym='k+',
                            notch=False, bootstrap=False,
                            usermedians=None,
                            conf_intervals=None)
            plt.show()
    # loop removal
    def check_loops(self,cobra_model_I=None):
        '''Check if the model contains loops'''

        # Change all uptake reactions to 0
        if cobra_model_I: cobra_model = cobra_model_I.copy();
        else: cobra_model = self.model.copy();
        system_boundaries = [x.id for x in cobra_model.reactions if x.boundary == 'system_boundary'];
        for rxn in cobra_model.reactions:
            if rxn.id in system_boundaries:
                cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(rxn.id).upper_bound = 0.0;
        # Set ATPM to 0
        cobra_model.reactions.get_by_id('ATPM').lower_bound = 0.0
        # set the objective function to a default value
        cobra_model.change_objective('Ec_biomass_iJO1366_WT_53p95M')
        cobra_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound=1e-6
        cobra_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound=1e6

        loops_bool = True;
        cobra_model.optimize(solver='gurobi');
        if not cobra_model.solution.f:
            loops_bool = False;

        return loops_bool;
    def simulate_loops(self,cobra_model_I=None,data_fva='loops_fva.json'):
        '''Simulate FVA after closing exchange reactions and setting ATPM to 0
        reactions with flux will be involved in loops'''
        
        if cobra_model_I: cobra_model = cobra_model_I.copy();
        else: cobra_model = self.model.copy();
        # Change all uptake reactions to 0
        system_boundaries = [x.id for x in cobra_model.reactions if x.boundary == 'system_boundary'];
        for rxn in cobra_model.reactions:
            if rxn.id in system_boundaries:
                cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(rxn.id).upper_bound = 0.0;
        # Set ATPM to 0
        cobra_model.reactions.get_by_id('ATPM').lower_bound = 0.0;
        # set the objective function to a default value
        cobra_model.change_objective('Ec_biomass_iJO1366_WT_53p95M')
        cobra_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound=0.0
        cobra_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound=1e6

        # calculate the reaction bounds using FVA
        reaction_bounds = flux_variability_analysis(cobra_model, fraction_of_optimum=1.0,
                                          the_reactions=None, solver='gurobi');

        # Update the data file
        with open(data_fva, 'wb') as outfile:
            json.dump(reaction_bounds, outfile, indent=4);
    def simulate_loops_sbml(self,ijo1366_sbml,data_fva):
        '''Simulate FVA after closing exchange reactions and setting ATPM to 0
        reactions with flux will be involved in loops'''

        # Read in the sbml file and define the model conditions
        cobra_model = create_cobra_model_from_sbml_file(ijo1366_sbml, print_time=True)
        # Change all uptake reactions to 0
        for rxn in cobra_model.reactions:
            if 'EX_' in rxn.id and '_LPAREN_e_RPAREN_' in rxn.id:
                rxn.lower_bound = 0.0;
        # Set ATPM to 0
        cobra_model.reactions.get_by_id('ATPM').lower_bound = 0.0

        # calculate the reaction bounds using FVA
        reaction_bounds = flux_variability_analysis(cobra_model, fraction_of_optimum=0.9,
                                          objective_sense='maximize', the_reactions=None,
                                          allow_loops=True, solver='gurobi',
                                          the_problem='return', tolerance_optimality=1e-6,
                                          tolerance_feasibility=1e-6, tolerance_barrier=1e-8,
                                          lp_method=1, lp_parallel=0, new_objective=None,
                                          relax_b=None, error_reporting=None,
                                          number_of_processes=1, copy_model=False);

        # Update the data file
        with open(data_fva, 'wb') as outfile:
            json.dump(reaction_bounds, outfile, indent=4);
    def find_loops(self,data_fva='loops_fva.json'):
        '''extract out loops from simulate_loops'''

        data_loops = json.load(open(data_fva))
        rxn_loops = [];
        for k,v in data_loops.items():
            if abs(v['minimum'])>1.0 or abs(v['maximum'])>1.0:
                rxn_loops.append(k);
        #return rxn_loops
        self.loops = rxn_loops;
    def remove_loopsFromPoints(self):
        '''remove reactions with loops from sampling points'''

        points_loopless = {};
        for k,v in self.points.items():
            if k in self.loops: continue
            else: 
                points_loopless[k] = v;

        #return points_loopless_mean;
        self.points = points_loopless;
    def remove_noFluxReactionsFromPoints(self):
        '''remove reactions that carry 0 flux'''

        points_flux = {};
        for k,v in self.points.items():
            # determine the max/min of the data
            max_point = max(v);
            min_point = min(v);
            if max_point == 0.0 and min_point == 0.0: continue;
            else: 
                points_flux[k] = v;

        self.points = points_flux;
        return
    # points QC
    def remove_points_notInSolutionSpace(self):
        '''remove points that are not in the solution space'''
        pruned_reactions = [];
        for rxn in self.model.reactions:
            points_copy = copy(self.points[rxn.id])
            self.points[rxn.id] = [p for p in self.points[rxn.id] if p >= rxn.lower_bound and p<= rxn.upper_bound] 
            if len(points_copy)!= len(self.points[rxn.id]):
                pruned_reactions.append(rxn.id)
        return pruned_reactions
    # analyses
    def descriptive_statistics(self):
        '''calculate the following:
        1. mean, variance, 95% CI
        2. median, mode, 1st quartile, 3rd quartile, range'''

        points_statistics = {};
        for k,v in self.points.items():
            # calculate the mean and variance
            m,var,lb,ub = self.calculate.calculate_ave_var(self.points[k]['points'],confidence_I = 0.95);
            # directly calculate the 95% CI
            lb,ub = self.calculate.calculate_ciFromPoints(self.points[k]['points'],alpha=0.05)
            #lb,ub = self.calculate.bootstrap(self.points[k]['points'], num_samples=100000, statistic=numpy.mean, alpha=0.05)
            # calculate the min, max, median, and interquartile ranges
            min,max,median,iq_1,iq_3=self.calculate.calculate_interquartiles(self.points[k]['points'],iq_range_I = [25,75])
            tmp = {};
            tmp = {
                'ave':m,
                'var':var,
                'lb':lb,
                'ub':ub,
                'median':median,
                'min':min,
                'max':max,
                'iq_1':iq_1,
                'iq_3':iq_3
                }
            points_statistics[k]=tmp;
        self.points_statistics = points_statistics;
    def svd(self):
        '''Singular value decomposition of the solution space'''
        return
    def convert_points2MetabolitePoints(self):
        '''convert the reaction flux to total flux through each metabolite for each sampling point'''
        metabolite_points = {};
        first_loop = True;
        for k,v in self.points.items():
            if first_loop:
                for met in self.model.metabolites:
                    metabolite_points[met.id]=numpy.zeros_like(v);
                first_loop = False;
            for i,flux in enumerate(v):
                for p in self.model.reactions.get_by_id(k).products:
                    metabolite_points[p.id][i]+=0.5*abs(flux*self.model.reactions.get_by_id(k).get_coefficient(p.id))
                for p in self.model.reactions.get_by_id(k).reactants:
                    metabolite_points[p.id][i]+=0.5*abs(flux*self.model.reactions.get_by_id(k).get_coefficient(p.id))
        self.points_metabolite=metabolite_points;
    def convert_points2SubsystemPoints(self):
        '''convert the reaction flux to total flux through each subsystem for each sampling point'''
        subsystem_points = {};
        subsystems_all = [];
        for r in self.model.reactions:
            subsystems_all.append(r.subsystem);
        subsystems = list(set(subsystems_all)); 
        first_loop = True;
        for k,v in self.points.items():
            if first_loop:       
                for sub in subsystems:
                    subsystem_points[sub]=numpy.zeros_like(v);
                first_loop = False;
            for i,flux in enumerate(v):
                subsystem_points[self.model.reactions.get_by_id(k).subsystem][i]+=abs(flux);
        self.points_subsystem=subsystem_points;
    def normalize_points2Total(self):
        '''normalize each reaction for a given point to the total
        flux through all reactions for that point'''
        points = self.points;
        points_normalized={};
        n_points = len(points[list(points.keys())[0]]);
        for i in range(n_points):
            total=0.0;
            for k,v in points.items():
                total+=numpy.abs(v[i]);
            for k,v in points.items():
                if i==0:
                    points_normalized[k]=numpy.zeros_like(v);
                points_normalized[k][i] = v[i]/total
        self.points = points_normalized;
    def normalize_points2CarbonInput(self):
        '''normalize each reaction for a given point to the total
        carbon input flux for that point'''
        points = self.points;
        system_boundaries = [x.id for x in self.model.reactions if x.boundary == 'system_boundary'];
        points_normalized={};
        n_points = len(points[list(points.keys())[0]]);
        for i in range(n_points):
            total=0.0;
            for k,v in points.items():
                if k in system_boundaries:
                    if self.model.reactions.get_by_id(k).reactants and v[i] < 0:
                        # e.g. glc-D -->
                        mets = self.model.reactions.get_by_id(k).reactants
                        for met in mets:
                            formula_str = met.formula.formula
                            n12C = 0
                            if 'C' not in Formula(formula_str)._elements and 0 in Formula(formula_str)._elements['C']:
                                n12C += Formula(formula_str)._elements['C'][0]; #get the # of Carbons
                            total+=numpy.abs(v[i])*n12C;
                    elif self.model.reactions.get_by_id(k).products and v[i] > 0:
                        # e.g. --> glc-D
                        mets = self.model.reactions.get_by_id(k).reactants
                        for met in mets:
                            formula_str = met.formula.formula
                            n12C = 0
                            if 'C' not in Formula(formula_str)._elements and 0 in Formula(formula_str)._elements['C']:
                                n12C += Formula(formula_str)._elements['C'][0]; #get the # of Carbons
                            total+=numpy.abs(v[i])*n12C;
            for k,v in points.items():
                if i==0:
                    points_normalized[k]=numpy.zeros_like(v);
                points_normalized[k][i] = v[i]/total
        self.points = points_normalized;
    def normalize_points2Input(self):
        '''normalize each reaction for a given point to the total
        input flux for that point'''
        points = self.points;
        system_boundaries = [x.id for x in self.model.reactions if x.boundary == 'system_boundary'];
        points_normalized={};
        n_points = len(points[list(points.keys())[0]]);
        for i in range(n_points):
            total=0.0;
            for k,v in points.items():
                if k in system_boundaries:
                    if self.model.reactions.get_by_id(k).reactants and v[i] < 0:
                        # e.g. glc-D -->
                        total+=numpy.abs(v[i]);
                    elif self.model.reactions.get_by_id(k).products and v[i] > 0:
                        # e.g. --> glc-D
                        total+=numpy.abs(v[i]);
            for k,v in points.items():
                if i==0:
                    points_normalized[k]=numpy.zeros_like(v);
                points_normalized[k][i] = v[i]/total
        self.points = points_normalized;
    # add data
    def add_data(self,data_dir_I=None,model_I=None,loops_I=[]):
        '''add new data'''
        if data_dir_I:self.data_dir =  data_dir_I;
        if model_I: self.model = model_I;
        if loops_I: self.loops = loops_I;
    # clear all data
    def remove_data(self):
        '''remove all data'''
        self.data_dir = None;
        self.model = None;
        self.points = {};
        self.mixed_fraction = None;
        self.loops = {};
        self.calculate = base_calculate();

class matlab_sampling(cobra_sampling):

    def __init__(self,matlab_path_I):
        if matlab_path_I:self.matlab_path =  matlab_path_I;
        else: self.matlab_path = 'C:/Users/dmccloskey-sbrg/Documents/MATLAB/sampling';
        self.points = {};
        self.mixed_fraction = None;
        self.model = None;
        self.simulation_dateAndTime = None;
        self.loops = {};
        self.calculate = base_calculate();

    def get_points_matlab(self,matlab_data,sampler_model_name):
        '''load sampling points from MATLAB'''

        # extract information about the file
        import os, time
        from datetime import datetime
        from stat import ST_SIZE, ST_MTIME
        try:
            st = os.stat(self.matlab_path + '/' + matlab_data)
        except IOError:
            print("failed to get information about", filename)
            return;
        else:
            file_size = st[ST_SIZE]
            simulation_dateAndTime_struct = time.localtime(st[ST_MTIME])
            simulation_dateAndTime = datetime.fromtimestamp(time.mktime(simulation_dateAndTime_struct))

        # load model from MATLAB file
        model = load_matlab_model(self.matlab_path + '/' + matlab_data,sampler_model_name);

        # load sample points from MATLAB file into numpy array
        points = scipy.io.loadmat(self.matlab_path + '/' + matlab_data)[sampler_model_name]['points'][0][0];
        mixed_fraction=scipy.io.loadmat(self.matlab_path + '/' + matlab_data)['mixedFrac'][0][0];
        #mat = scipy.io.loadmat('data/EvoWt.mat')
        #points = mat['model_WT_sampler_out']['points'][0][0]

        points_dict = {};
        for i,r in enumerate(model.reactions):
            # convert names:
            r_id_conv = r.id.replace('-','_DASH_');
            r_id_conv = r_id_conv.replace('(','_LPAREN_');
            r_id_conv = r_id_conv.replace(')','_RPAREN_');
            # extract points
            #m,var,lb,ub = self.calculate.calculate_ave_var(points[i,:],confidence_I = 0.95)
            points_dict[r_id_conv] = {'points':points[i,:]
                                 ##'mean':mean(points[i,:]),
                                 #'ave':m,
                                 ##'std':std(points[i,:]),
                                 #'var':var,
                                 #'lb':lb,
                                 #'ub':ub
                                 }

        self.points = points_dict;
        self.model = model;
        self.mixed_fraction = mixed_fraction;
        self.simulation_dateAndTime = simulation_dateAndTime;

    def export_sampling_matlab(self,cobra_model,fraction_optimal = None, filename_model='sample_model.mat',filename_script='sample_script.m', filename_points='points.mat',
                               solver_id_I='gurobi',n_points_I = None, n_steps_I = 20000, max_time_I = None):
        '''export model and script for sampling using matlab cobra_toolbox'''
        ## copy the model:
        #cobra_model_copy = cobra_model.copy();
        # convert numerical input to string
        n_points,n_steps,max_time = '[]','[]','[]';
        if n_points_I:
            n_points = n_points_I;
        if n_steps_I:
            n_steps = n_steps_I;
        if max_time_I:
            max_time = max_time_I;
        # confine the objective to a fraction of maximum optimal
        if fraction_optimal:
            # optimize
            cobra_model.optimize(solver_id_I);
            objective = [x.id for x in cobra_model.reactions if x.objective_coefficient == 1]
            cobra_model.reactions.get_by_id(objective[0]).upper_bound = fraction_optimal * cobra_model.solution.f;
        # write model to mat
        save_matlab_model(cobra_model,self.matlab_path + '/' + filename_model);
        ## write model to xml
        #write_sbml_model(cobra_model,'data/sampling/sampler.xml');
        # write the sampling script to file
        #[sampleStructOut, mixedFraction] = gpSampler(sampleStruct, nPoints, bias, maxTime, maxSteps, threads, nPointsCheck)
        mat_script = "% initialize with Tomlab_CPLEX\n";
        mat_script +="load('" + self.matlab_path + '/' + filename_model + "')\n";
        mat_script +="initCobraToolbox();\n";
        mat_script +="% sample\n";
        mat_script +="[sampler_out, mixedFrac] = gpSampler(" + cobra_model.description
        mat_script +=(", %s, [], %s, %s, [], true);\n" %(n_points,n_steps,max_time));
        mat_script +="[sampler_out, mixedFrac] = gpSampler(sampler_out";
        mat_script +=(", %s, [], %s, %s, [], true);\n" %(n_points,n_steps,max_time));
        mat_script +="save('"+ self.matlab_path + '/' + filename_points + "','sampler_out', 'mixedFrac');";
        with open(self.matlab_path + '/' + filename_script,'w') as f:
            f.write(mat_script);

class cobra_sampling_n(base_calculate):

    def __init__(self,data_dir_I=None,model_I=None,loops_I=[],sample_ids_I=[],samplers_I=None,control_I=False):
        #   control_I = True: sample_ids_I[0]=control,sample_ids_I[1:]=perturbation
        #               False: pairwise test is performed on all
        #               controls how the pairwisetests are performed
        if data_dir_I:self.data_dir =  data_dir_I;
        else: self.data_dir = None;
        if model_I: self.model = model_I;
        else: self.model = None;
        if loops_I: self.loops = loops_I;
        else: self.loops = [];
        if sample_ids_I: self.sample_ids = sample_ids_I;
        else: self.sample_ids = []
        if samplers_I: self.samplers = samplers_I;
        else: self.samplers = [];
        if control_I: self.control = control_I;
        else: self.control=control_I;
        self.points = [];
        self.points_metabolites = [];
        self.points_subsystems = [];
        self.calculate = base_calculate();
        self.data = [];

    def calculate_pairWiseTest(self):
        '''Calculate the difference of the mean and median, fold change, and p-value
         between pairwise sampling distribution'''

        data_O = [];

        test_stat = None
        test_description = 'permutation'

        for i,data_1 in enumerate(self.points):
            sample_id_1 = self.sample_ids[i];
            if self.control and i>0:
                break;
            for j,data_2 in enumerate(self.points):
                sample_id_2 = self.sample_ids[j];
                if i==j: continue;
                for r in self.model.reactions:
                    rxn_id = r.id
                    mean_difference = None
                    median_difference = None
                    pvalue = None
                    fold_change = None;
                    # check point length
                    n_data_1 = len(data_1);
                    n_data_2 = len(data_2);
                    if n_data_1 != n_data_2:
                        print('number of sampled points are not consistent')
                    n_points = n_data_1;
                    if rxn_id in list(data_1.keys()):
                        cond1 = data_1[rxn_id];
                    else:
                        cond1 = np.zeros(n_points);
                    if rxn_id in list(data_2.keys()):
                        cond2 = data_2[rxn_id];
                    else:
                        cond2 = np.zeros(n_points);
                    mean_difference = cond2.mean()-cond1.mean();
                    median_difference = numpy.median(cond2) - numpy.median(cond1) 
                    #pvalue = self.calculate.permutation_resampling(cond1,cond2);
                    pvalue = self.calculate.calculate_pvalue_permutation(cond1,cond2);
                    fold_change = cond2.mean()/cond1.mean();
                    tmp = {};
                    tmp = {'sample_id_1':sample_id_1,
                           'sample_id_2':sample_id_2,
                           'rxn_id':rxn_id,
                           'pvalue':pvalue,
                           'mean_difference':mean_difference,
                           'median_difference':median_difference,
                           'fold_change':fold_change,
                           'test_stat':test_stat,
                           'test_description':test_description};
                    data_O.append(tmp);
        self.data = data_O;

    def calculate_pairWiseTest_metabolites(self):
        '''Calculate the difference of the mean and median, fold change, and p-value
         between pairwise sampling distribution for metabolites'''

        data_O = [];

        test_stat = None
        test_description = 'permutation'

        for i,data_1 in enumerate(self.points_metabolites):
            sample_id_1 = self.sample_ids[i];
            if self.control and i>0:
                break;
            for j,data_2 in enumerate(self.points_metabolites):
                sample_id_2 = self.sample_ids[j];
                if i==j: continue;
                for m in self.model.metabolites:
                    met_id = m.id
                    mean_difference = None
                    median_difference = None
                    pvalue = None
                    fold_change = None;
                    # check point length
                    n_data_1 = len(data_1);
                    n_data_2 = len(data_2);
                    if n_data_1 != n_data_2:
                        print('number of sampled points are not consistent')
                    n_points = n_data_1;
                    if met_id in list(data_1.keys()):
                        cond1 = data_1[met_id];
                    else:
                        cond1 = np.zeros(n_points);
                    if met_id in list(data_2.keys()):
                        cond2 = data_2[met_id];
                    else:
                        cond2 = np.zeros(n_points);
                    mean_difference = cond1.mean() - cond2.mean()
                    median_difference = cond1.median() - cond2.median() 
                    #pvalue = self.calculate.permutation_resampling(cond1,cond2);
                    pvalue = self.calculate.calculate_pvalue_permutation(cond1,cond2);
                    fold_change = cond2.mean()/cond1.mean();
                    tmp = {};
                    tmp = {'sample_id_1':sample_id_1,
                           'sample_id_2':sample_id_2,
                           'met_id':met_id,
                           'pvalue':pvalue,
                           'mean_difference':mean_difference,
                           'median_difference':median_difference,
                           'fold_change':fold_change,
                           'test_stat':test_stat,
                           'test_description':test_description};
                    data_O.append(tmp);
        self.data = data_O;

    def calculate_pairWiseTest_subsystems(self):
        '''Calculate the difference of the mean and median, fold change, and p-value
         between pairwise sampling distribution for metabolites'''

        data_O = [];

        test_stat = None
        test_description = 'permutation'

        for i,data_1 in enumerate(self.points_subsystems):
            sample_id_1 = self.sample_ids[i];
            if self.control and i>0:
                break;
            for j,data_2 in enumerate(self.points_subsystems):
                sample_id_2 = self.sample_ids[j];
                if i==j: continue;
                for sub_id in list(self.points_subsystems.keys()):
                    mean_difference = None
                    median_difference = None
                    pvalue = None
                    fold_change = None;
                    # check point length
                    n_data_1 = len(data_1);
                    n_data_2 = len(data_2);
                    if n_data_1 != n_data_2:
                        print('number of sampled points are not consistent')
                    n_points = n_data_1;
                    if sub_id in list(data_1.keys()):
                        cond1 = data_1[sub_id];
                    else:
                        cond1 = np.zeros(n_points);
                    if sub_id in list(data_2.keys()):
                        cond2 = data_2[sub_id];
                    else:
                        cond2 = np.zeros(n_points);
                    mean_difference = cond1.mean() - cond2.mean()
                    median_difference = cond1.median() - cond2.median() 
                    #pvalue = self.calculate.permutation_resampling(cond1,cond2);
                    pvalue = self.calculate.calculate_pvalue_permutation(cond1,cond2);
                    fold_change = cond2.mean()/cond1.mean();
                    tmp = {};
                    tmp = {'sample_id_1':sample_id_1,
                           'sample_id_2':sample_id_2,
                           'subsystem_id':sub_id,
                           'pvalue':pvalue,
                           'mean_difference':mean_difference,
                           'median_difference':median_difference,
                           'fold_change':fold_change,
                           'test_stat':test_stat,
                           'test_description':test_description};
                    data_O.append(tmp);
        self.data = data_O;

    def calculate_anova(self):
        return

    def calculate_pca(self):
        return

    def get_points(self,data_points_I=[],remove_loops_I=True,remove_no_flux_I=True,normalize_I=True):
        '''Get multiple points from sampling'''
        sampling = cobra_sampling();
        for i,sample_id in enumerate(self.sample_ids):
            sampling.add_data(data_dir_I=self.data_dir,model_I=self.model,loops_I=self.loops);
            if self.samplers[i]=='gpSampler':
                sampling.get_points_matlab(data_points_I[i]);
            elif self.samplers[i]=='optGpSampler':
                sampling.get_points_numpy(data_points_I[i])
            if remove_loops_I: sampling.remove_loopsFromPoints();
            if remove_no_flux_I: sampling.remove_noFluxReactionsFromPoints();
            if normalize_I: sampling.normalize_points2Total();
            #sampling.convert_points2MetabolitePoints();
            #sampling.convert_points2SubsystemPoints()
            self.points.append(sampling.points);
            self.points_metabolites.append(sampling.points_metabolite)
            self.points_subsystems.append(sampling.points_subsystem)
            sampling.remove_data();