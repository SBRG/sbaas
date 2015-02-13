from sys import exit
from math import log, sqrt, exp
import operator, json, csv
from analysis.analysis_base.base_calculate import base_calculate
# Dependencies from 3rd party
import scipy.io
import numpy
import scipy.io
from numpy import histogram, mean, std, loadtxt, savetxt
import matplotlib as mpl
import matplotlib.pyplot as plt
# Dependencies from cobra
from cobra.io.mat import load_matlab_model,save_matlab_model
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra.flux_analysis import flux_variability_analysis, single_deletion
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis.objective import update_objective

class cobra_sampling(base_calculate):

    def __init__(self,data_dir_I):
        if data_dir_I:self.data_dir =  data_dir_I;
        else: self.data_dir = 'C:/Users/dmccloskey-sbrg/Documents/MATLAB/sampling';
        self.points = {};
        self.mixed_fraction = None;
        self.model = None;
        self.loops = {};
        self.calculate = base_calculate();

    def get_points_numpy(self,numpy_data,ijo1366_sbml):
        '''load sampling points from numpy file'''

        # load points from numpy file
        points = loadtxt(numpy_data);

        # Read in the sbml file and define the model conditions
        cobra_model = create_cobra_model_from_sbml_file(ijo1366_sbml, print_time=True)

        points_dict = {};
        for i,r in enumerate(cobra_model.reactions):
            # extract points
            m,var,lb,ub = self.calculate.calculate_ave_var(points[i,:],confidence_I = 0.95)
            points_dict[r.id] = {'points':points[i,:],
                                 #'mean':mean(points[i,:]),
                                 'ave':m,
                                 #'std':std(points[i,:]),
                                 'var':var,
                                 'lb':lb,
                                 'ub':ub}

        self.points = points_dict;
        self.model = cobra_model;

    def plot_points(self,reaction_lst=None):
        '''plot sampling points from MATLAB'''
        if not reaction_lst:
            reaction_lst = ['ENO','FBA','FBP','G6PP','GAPD','GLBRAN2',
                        'GLCP','GLCP2','GLDBRAN2','HEX1','PDH','PFK',
                        'PGI','PGK','PGM','PPS','PYK','TPI','ENO_reverse',
                        'FBA_reverse','GAPD_reverse','PGI_reverse',
                        'PGK_reverse','PGM_reverse','TPI_reverse']
        for r in reaction_lst:
            # loop through each reaction in the list
            plt.figure()
            n, bins, patches = plt.hist(self.points[r]['points'],50,label = [r])
            plt.legend()
            plt.show()

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
        for k,v in data_loops.iteritems():
            if abs(v['minimum'])>1.0 or abs(v['maximum'])>1.0:
                rxn_loops.append(k);
        #return rxn_loops
        self.loops = rxn_loops;

    def remove_loopsFromPoints(self):
        '''remove reactions with loops from sampling points'''

        points_loopless = {};
        for k,v in self.points.iteritems():
            if k in self.loops: continue
            else: 
                points_loopless[k] = {'points':v['points'],
                                 'ave':v['ave'],
                                 'var':v['var'],
                                 'lb':v['lb'],
                                 'ub':v['ub']}

        #return points_loopless_mean;
        self.points = points_loopless;

    def export_points_numpy(self,filename):
        '''export sampling points'''

        savetxt(filename,self.points);

class matlab_calculate(base_calculate):
    def __init__(self,matlab_path_I):
        if matlab_path_I:self.matlab_path =  matlab_path_I;
        else: self.matlab_path = 'C:/Users/dmccloskey-sbrg/Documents/MATLAB/ALEsKOs'

    def SMLtools(self,x_I,y_I,filename_I=None,filename_O=None,degree_I=3,knots_I=10,interiorknots_I='free',plot_I='off',increasing_I='on'):
        '''Compute a spline fit of the data using matlab's SMLtools'''

        if not filename_I:
            filename_I = matlab_path + "/SMLtool_in.m";
        if not filename_O:
            filename_O = matlab_path + "/SMLtool_out.m";

        mat_cmd = '';
        #export data
        mat_cmd += 'x=[...\n'
        for x in x_I:
            mat_cmd += str(x) + ',\n';
        mat_cmd += '];\n';
        mat_cmd += 'y=[...\n'
        for y in y_I:
            mat_cmd += str(y) + ',\n';
        mat_cmd += '];\n';
        #spline command
        mat_cmd += ("slm=slmengine(x,y,'degree',%s,'plot',%s,'interiorknots',%s,'knots',%f,'increasing',%s);\n" % (degree_I,plot_I,interiorknots_I,knots_I,increasing_I))
        mat_cmd += "xx{i}=(slm.x(1):slm.x(end)/1000:slm.x(end));\n"
        mat_cmd += "yy{i}=slmeval(xx{i},slm);\n"
        mat_cmd += "curves{i} = slm;\n"
        mat_cmd += ("save(%s);\n" %filename_O);
        #write to file
        with open(filename_I,'wb') as file:
            file.write(mat_cmd);
        #wait for user to execute matlab script
        print "Press any key to continue once script has been executed"
        a=raw_input();
        #read in the data from file:
        xx = scipy.io.loadmat(filename_O)['xx'][0][0];
        yy = scipy.io.loadmat(filename_O)['yy'][0][0];
        curves = scipy.io.loadmat(filename_O)['curves'][0][0];
        return xx,yy,curves;

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
            print "failed to get information about", filename
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
            m,var,lb,ub = self.calculate.calculate_ave_var(points[i,:],confidence_I = 0.95)
            points_dict[r_id_conv] = {'points':points[i,:],
                                 #'mean':mean(points[i,:]),
                                 'ave':m,
                                 #'std':std(points[i,:]),
                                 'var':var,
                                 'lb':lb,
                                 'ub':ub}

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

class cobra_sampling_difference(base_calculate):

    def __init__(self,sampled_ave_1_I,sampled_ave_2_I,sampled_var_1_I,sampled_var_2_I,ci_level_I=0.95):
        if sampled_ave_1_I: self.sampled_ave_1 = sampled_ave_1_I;
        else: self.sampled_ave_1 = None;
        if sampled_ave_2_I: self.sampled_ave_2 = sampled_ave_2_I;
        else: self.sampled_ave_2 = None;
        if sampled_var_1_I: self.sampled_var_1 = sampled_var_1_I;
        else: self.sampled_var_1 = None;
        if sampled_var_2_I: self.sampled_var_2 = sampled_var_2_I;
        else: self.sampled_var_2 = None;
        if ci_level_I: self.ci_level = ci_level_I;
        else: ci_level_I=None;
        self.sampled_delta_ave = None;
        self.sampled_delta_var = None;
        self.sampled_delta_lb = None;
        self.sampled_delta_ub = None;
        self.sampled_fold_change = None;
        self.z_delta = None;
        self.pvalue_delta = None;
        self.sampled_delta_ave_metabolites = None;
        self.sampled_delta_var_metabolites = None;
        self.sampled_delta_lb_metabolites = None;
        self.sampled_delta_ub_metabolites = None;
        self.sampled_fold_change_metabolites = None;
        self.z_delta_metabolites = None;
        self.pvalue_delta_metabolites = None;
        self.sampled_delta_ave_subsystems = None;
        self.sampled_delta_var_subsystems = None;
        self.sampled_delta_lb_subsystems = None;
        self.sampled_delta_ub_subsystems = None;
        self.sampled_fold_change_subsystems = None;
        self.z_delta_subsystems = None;
        self.pvalue_delta_subsystems = None;

    def calculate_sampledZScore(self):
        return
    def calculate_reporterMetabolites(self):
        return
    def calculate_reporterSubsystems(self):
        return
