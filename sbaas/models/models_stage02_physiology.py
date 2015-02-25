# models_stage03_physiology
# i.e. thermodynamics

# ORMs
from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage02_physiology_simulatedData(Base):
    __tablename__ = 'data_stage02_physiology_simulatedData'
    id = Column(Integer, Sequence('data_stage02_physiology_simulatedData_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    rxn_id = Column(String(100))
    fba_flux = Column(Float);
    fva_minimum = Column(Float);
    fva_maximum = Column(Float);
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    sra_gr = Column(Float);
    sra_gr_ratio = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
                 #experiment_id_I,model_id_I,
                 #sample_name_abbreviation_I,
                 rxn_id_I,fba_flux_I,
                 fva_minimum_I,fva_maximum_I,flux_units_I,
                 sra_gr_I,sra_gr_ratio_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.rxn_id=rxn_id_I
        self.fba_flux=fba_flux_I
        self.fva_minimum=fva_minimum_I
        self.fva_maximum=fva_maximum_I
        self.flux_units=flux_units_I
        self.sra_gr=sra_gr_I
        self.sra_gr_ratio=sra_gr_ratio_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
            #    'experiment_id':self.experiment_id,
            #    'model_id':self.model_id,
            #'sample_name_abbreviation':self.sample_name_abbreviation,
                'rxn_id':self.rxn_id,
                'fba_flux':self.fba_flux,
                'fva_minimum':self.fva_minimum,
                'fva_maximum':self.fva_maximum,
                'flux_units':self.flux_units,
                'sra_gr':self.sra_gr,
                'sra_gr_ratio':self.sra_gr_ratio,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_simulation(Base):
    __tablename__ = 'data_stage02_physiology_simulation'
    id = Column(Integer, Sequence('data_stage02_physiology_simulation_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    experiment_id = Column(String(50))
    model_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    simulation_type = Column(String(50)); # sampling, fva, sra, fba, fba-loopless, pfba, etc.
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','model_id','sample_name_abbreviation','simulation_type'),
            #UniqueConstraint('experiment_id','model_id','sample_name_abbreviation','time_point','simulation_type'),
            UniqueConstraint('simulation_id'),
            )

    def __init__(self,simulation_id_I,
                 experiment_id_I,
            model_id_I,
            sample_name_abbreviation_I,
            #time_point_I,
            simulation_type_I,
            used__I,
            comment__I):
        self.simulation_id=simulation_id_I
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.simulation_type=simulation_type_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
            'experiment_id':self.experiment_id,
            'model_id':self.model_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
            'simulation_type':self.simulation_type,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage02_physiology_models(Base):
    __tablename__ = 'data_stage02_physiology_models'
    id = Column(Integer, Sequence('data_stage02_physiology_models_id_seq'), primary_key=True)
    model_id = Column(String(50))
    model_name = Column(String(100))
    model_description = Column(String(100))
    model_file = Column(Text)
    file_type = Column(String(50))
    date = Column(DateTime)

    __table_args__ = (
            UniqueConstraint('model_id'),
            )

    def __init__(self,model_id_I,
            model_name_I,
            model_description_I,
            model_file_I,
            file_type_I,
            date_I):
        self.model_id=model_id_I
        self.model_name=model_name_I
        self.model_description=model_description_I
        self.model_file=model_file_I
        self.file_type=file_type_I
        self.date=date_I

    def __repr__dict__(self):
        return {'model_id':self.model_id,
                'model_name':self.model_name,
                'model_description':self.model_description,
                'model_file':self.model_file,
                'file_type':self.file_type,
                'date':self.date}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_modelReactions(Base):
    __tablename__ = 'data_stage02_physiology_modelReactions'
    id = Column(Integer, Sequence('data_stage02_physiology_modelReactions_id_seq'), primary_key=True)
    model_id = Column(String(50))
    rxn_id = Column(String(50))
    rxn_name = Column(String(255))
    equation = Column(String(4000));
    subsystem = Column(String(255));
    gpr = Column(Text);
    genes = Column(postgresql.ARRAY(String(50)));
    reactants_stoichiometry = Column(postgresql.ARRAY(Float)) # stoichiometry of metabolites
    products_stoichiometry = Column(postgresql.ARRAY(Float)) 
    reactants_ids = Column(postgresql.ARRAY(String(50))) # list of met_ids that are in the reaction
    products_ids = Column(postgresql.ARRAY(String(50))) 
    lower_bound = Column(Float) #derived from experimentally measured values or estimations from simulations
    upper_bound = Column(Float) #derived from experimentally measured values or estimations from simulations
    objective_coefficient = Column(Float)
    flux_units = Column(String(50))
    reversibility = Column(Boolean)
    used_ = Column(Boolean)
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('model_id','rxn_id'),
            )

    def __init__(self,model_id_I,
            rxn_id_I,
            rxn_name_I,
            equation_I,
            subsystem_I,
            gpr_I,
            genes_I,
            reactants_stoichiometry_I,
            products_stoichiometry_I,
            reactants_ids_I,
            products_ids_I,
            lower_bound_I,
            upper_bound_I,
            objective_coefficient_I,
            flux_units_I,
            reversibility_I,
            used__I,
            comment__I):
        self.model_id=model_id_I
        self.rxn_id=rxn_id_I
        self.rxn_name=rxn_name_I
        self.equation=equation_I
        self.subsystem=subsystem_I
        self.gpr=gpr_I
        self.genes=genes_I
        self.reactants_stoichiometry=reactants_stoichiometry_I
        self.products_stoichiometry=products_stoichiometry_I
        self.reactants_ids=reactants_ids_I
        self.products_ids=products_ids_I
        self.lower_bound=lower_bound_I
        self.upper_bound=upper_bound_I
        self.objective_coefficient=objective_coefficient_I
        self.reversibility=reversibility_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'model_id':self.model_id,
            'rxn_id':self.rxn_id,
            'rxn_name':self.rxn_name,
            'equation':self.equation,
            'subsystem':self.subsystem,
            'gpr':self.gpr,
            'genes':self.genes,
            'reactants_stoichiometry':self.reactants_stoichiometry,
            'products_stoichiometry':self.products_stoichiometry,
            'reactants_ids':self.reactants_ids,
            'products_ids':self.products_ids,
            'lower_bound':self.lower_bound,
            'upper_bound':self.upper_bound,
            'objective_coefficient':self.objective_coefficient,
            'flux_units':self.flux_units,
            'reversibility':self.reversibility,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage02_physiology_modelMetabolites(Base):
    __tablename__ = 'data_stage02_physiology_modelMetabolites'
    id = Column(Integer, Sequence('data_stage02_physiology_modelMetabolites_id_seq'), primary_key=True)
    model_id = Column(String(50))
    met_name = Column(String(500))
    met_id = Column(String(50))
    formula = Column(String(100))
    charge = Column(Integer)
    compartment = Column(String(50))
    bound = Column(Float)
    constraint_sense = Column(String(5))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('model_id','met_id'),
            )

    def __init__(self,model_id_I,
            met_name_I,
            met_id_I,
            formula_I,
            charge_I,
            compartment_I,
            bound_I,
            constraint_sense_I,
            used__I,
            comment__I):
        self.model_id=model_id_I
        self.met_name=met_name_I
        self.met_id=met_id_I
        self.formula=formula_I
        self.charge=charge_I
        self.compartment=compartment_I
        self.bound=bound_I
        self.constraint_sense=constraint_sense_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'model_id':self.model_id,
                'met_name':self.met_name,
                'met_id':self.met_id,
                'formula':self.formula,
                'charge':self.charge,
                'bound':self.bound,
                'constraint_sense':self.constraint_sense,
                'compartment':self.compartment,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_measuredFluxes(Base):
    __tablename__ = 'data_stage02_physiology_measuredFluxes'
    id = Column(Integer, Sequence('data_stage02_physiology_measuredFluxes_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    model_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    rxn_id = Column(String(100))
    flux_average = Column(Float);
    flux_stdev = Column(Float);
    flux_lb = Column(Float); # based on 95% CI
    flux_ub = Column(Float);
    flux_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name_abbreviation','rxn_id','model_id'),
            )

    def __init__(self,experiment_id_I,
            model_id_I,
            sample_name_abbreviation_I,
            #time_point_I,
            rxn_id_I,
            flux_average_I,
            flux_stdev_I,
            flux_lb_I,
            flux_ub_I,
            flux_units_I,
            used__I,
            comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.rxn_id=rxn_id_I
        self.flux_average=flux_average_I
        self.flux_stdev=flux_stdev_I
        self.flux_lb=flux_lb_I
        self.flux_ub=flux_ub_I
        self.flux_units=flux_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                    'model_id':self.model_id,
                    'sample_name_abbreviation':self.sample_name_abbreviation,
                    #'time_point':self.time_point,
                    'rxn_id':self.rxn_id,
                    'flux_average':self.flux_average,
                    'flux_stdev':self.flux_stdev,
                    'flux_lb':self.flux_lb,
                    'flux_ub':self.flux_ub,
                    'flux_units':self.flux_units,
                    'used_':self.used_,
                    'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_sampledPoints(Base):
    __tablename__ = 'data_stage02_physiology_sampledPoints'
    id = Column(Integer, Sequence('data_stage02_physiology_sampledData_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    mixed_fraction = Column(Float);
    data_dir = Column(String(500)); #
    infeasible_loops = Column(postgresql.ARRAY(String));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','simulation_dateAndTime'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            mixed_fraction_I,data_dir_I,infeasible_loops_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.mixed_fraction=mixed_fraction_I
        self.data_dir=data_dir_I
        self.infeasible_loops=infeasible_loops_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'data_dir':self.data_dir,
                'infeasible_loops':self.infeasible_loops,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_sampledData(Base):
    __tablename__ = 'data_stage02_physiology_sampledData'
    id = Column(Integer, Sequence('data_stage02_physiology_sampledData_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    rxn_id = Column(String(100)) #TODO: change name to variable_id and add column for variable_type (e.g. met,rxn)
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1'); #TODO: change to variable_units
    sampling_points = Column(postgresql.ARRAY(Float)); #
    sampling_ave = Column(Float);
    sampling_var = Column(Float);
    sampling_lb = Column(Float);
    sampling_ub = Column(Float);
    #sampling_ci = Column(Float, default = 0.95);
    sampling_min = Column(Float);
    sampling_max = Column(Float);
    sampling_median = Column(Float);
    sampling_iq_1 = Column(Float);
    sampling_iq_3 = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            rxn_id_I,flux_units_I,sampling_points_I,
                 sampling_ave_I,sampling_var_I,sampling_lb_I,sampling_ub_I,
                 #sampling_ci_I,
                 sampling_min_I,sampling_max_I,sampling_median_I,
                 sampling_iq_1_I,sampling_iq_3_I,
                 used__I,comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.rxn_id=rxn_id_I
        self.flux_units=flux_units_I
        self.sampling_points=sampling_points_I
        self.sampling_ave=sampling_ave_I
        self.sampling_var=sampling_var_I
        self.sampling_lb=sampling_lb_I
        self.sampling_ub=sampling_ub_I
        #self.sampling_ci=sampling_ci_I
        self.sampling_min=sampling_min_I
        self.sampling_max=sampling_max_I
        self.sampling_median=sampling_median_I
        self.sampling_iq_1=sampling_iq_1_I
        self.sampling_iq_3=sampling_iq_3_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'rxn_id':self.rxn_id,
                'flux_units':self.flux_units,
                'sampling_points':self.sampling_points,
                'sampling_ave':self.sampling_ave,
                'sampling_var':self.sampling_var,
                'sampling_lb':self.sampling_lb,
                'sampling_ub':self.sampling_ub,
                #'sampling_ci':self.sampling_ci,
                'sampling_max':self.sampling_max,
                'sampling_min':self.sampling_min,
                'sampling_median':self.sampling_median,
                'sampling_iq_1':self.sampling_iq_1,
                'sampling_iq_3':self.sampling_iq_3,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_simulationParameters(Base):
    __tablename__ = 'data_stage02_physiology_simulationParameters'
    id = Column(Integer, Sequence('data_stage02_physiology_simulationParameters_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    #simulation_dateAndTime = Column(DateTime);
    solver_id = Column(String);
    n_points = Column(Integer); # sampling-specific
    n_steps = Column(Integer); # sampling-specific
    max_time = Column(Float); # sampling-specific
    sampler_id = Column(String); # sampling-specific; gpSampler (Matlab) opGpSampler (Python)
    #solve_time = Column(Float);
    #solve_time_units = Column(String);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id'),
            )

    def __init__(self,
                 simulation_id_I,
        #simulation_dateAndTime_I,
        solver_id_I,
        n_points_I,
        n_steps_I,
        max_time_I,
        sampler_id_I,
        #solve_time_I,
        #solve_time_units_I,
        used__I,comment__I):
        self.simulation_id=simulation_id_I
        #self.simulation_dateAndTime=simulation_dateAndTime_I
        self.solver_id=solver_id_I
        self.n_points=n_points_I
        self.n_steps=n_steps_I
        self.max_time=max_time_I
        self.sampler_id=sampler_id_I
        #self.solve_time=solve_time_I
        #self.solve_time_units=solve_time_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
            #'simulation_dateAndTime':self.simulation_dateAndTime,
            'solver_id':self.solver_id,
            'n_points':self.n_points,
            'n_steps':self.n_steps,
            'max_time':self.max_time,
            'sampler_id':self.sampler_id,
            #'solve_time':self.solve_time,
            #'solve_time_units':self.solve_time_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#TODO:
class data_stage02_physiology_pairWiseTest(Base):
    __tablename__ = 'data_stage02_physiology_pairWiseTest'
    id = Column(Integer, Sequence('data_stage02_physiology_pairWiseTest_id_seq'), primary_key=True)
    simulation_id_1 = Column(String(500))
    simulation_id_2 = Column(String(500))
    #simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    rxn_id = Column(String(100))
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    fold_change = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id_1','simulation_id_2','rxn_id'),
            )

    def __init__(self,simulation_id_1_I,simulation_id_2_I,
        #simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            rxn_id_I,flux_units_I,
                 mean_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 fold_change_I,
                 used__I,comment__I):
        self.simulation_id_1=simulation_id_1_I
        self.simulation_id_2=simulation_id_2_I
        #self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.rxn_id=rxn_id_I
        self.flux_units=flux_units_I
        self.mean=mean_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.fold_change=fold_change_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id_1':self.simulation_id_1,
                'simulation_id_2':self.simulation_id_2,
        #       'simulation_dateAndTime':self.simulation_dateAndTime,
        #       'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #       'sample_name_abbreviation':self.sample_name_abbreviation,
                'rxn_id':self.rxn_id,
                'flux_units':self.flux_units,
                'sampling_delta_ave':self.sampling_delta_ave,
                'sampling_delta_var':self.sampling_delta_var,
                'sampling_delta_lb':self.sampling_delta_lb,
                'sampling_delta_ub':self.sampling_delta_ub,
                'z_delta':self.z_delta,
                'pvalue_delta':self.pvalue_delta,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_pairWiseTestMetabolites(Base):
    __tablename__ = 'data_stage02_physiology_pairWiseTestMetabolites'
    id = Column(Integer, Sequence('data_stage02_physiology_pairWiseTestMetabolites_id_seq'), primary_key=True)
    simulation_id_1 = Column(String(500))
    simulation_id_2 = Column(String(500))
    #simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    met_id = Column(String(100))
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    fold_change = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id_1','simulation_id_2','met_id'),
            )

    def __init__(self,simulation_id_1_I,simulation_id_2_I,
        #simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            met_id_I,flux_units_I,
                 mean_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 fold_change_I,
                 used__I,comment__I):
        self.simulation_id_1=simulation_id_1_I
        self.simulation_id_2=simulation_id_2_I
        #self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.met_id=met_id_I
        self.flux_units=flux_units_I
        self.mean=mean_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.fold_change=fold_change_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id_1':self.simulation_id_1,
                'simulation_id_2':self.simulation_id_2,
        #'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'met_id':self.met_id,
                'flux_units':self.flux_units,
                'sampling_delta_ave':self.sampling_delta_ave,
                'sampling_delta_var':self.sampling_delta_var,
                'sampling_delta_lb':self.sampling_delta_lb,
                'sampling_delta_ub':self.sampling_delta_ub,
                'z_delta':self.z_delta,
                'pvalue_delta':self.pvalue_delta,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_pairWiseTestSubsystems(Base):
    __tablename__ = 'data_stage02_physiology_pairWiseTestSubsystems'
    id = Column(Integer, Sequence('data_stage02_physiology_pairWiseTestSubsystems_id_seq'), primary_key=True)
    simulation_id_1 = Column(String(500))
    simulation_id_2 = Column(String(500))
    #simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #sample_name_abbreviation = Column(String(100))
    subsystem_id = Column(String(100))
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    fold_change = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('simulation_id_1','simulation_id_2','subsystem_id'),
            )

    def __init__(self,simulation_id_1_I,simulation_id_2_I,
        #simulation_dateAndTime_I,
        #experiment_id_I,model_id_I,
        #    sample_name_abbreviation_I,
            subsystem_id_I,flux_units_I,
                 mean_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 fold_change_I,
                 used__I,comment__I):
        self.simulation_id_1=simulation_id_1_I
        self.simulation_id_2=simulation_id_2_I
        #self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        self.subsystem_id=subsystem_id_I
        self.flux_units=flux_units_I
        self.mean=mean_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.fold_change=fold_change_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id_1':self.simulation_id_1,
                'simulation_id_2':self.simulation_id_2,
        #'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #        'model_id':self.model_id,
        #    'sample_name_abbreviation':self.sample_name_abbreviation,
                'subsystem_id':self.subsystem_id,
                'flux_units':self.flux_units,
                'sampling_delta_ave':self.sampling_delta_ave,
                'sampling_delta_var':self.sampling_delta_var,
                'sampling_delta_lb':self.sampling_delta_lb,
                'sampling_delta_ub':self.sampling_delta_ub,
                'z_delta':self.z_delta,
                'pvalue_delta':self.pvalue_delta,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#TODO: data_stage02_physiology_sampledData_svd

class data_stage02_physiology_pca_scores(Base):
    __tablename__ = 'data_stage02_physiology_pca_scores'
    id = Column(Integer, Sequence('data_stage02_physiology_pca_scores_id_seq'), primary_key=True)
    simulation_group_id = Column(String(50))
    simulation_id = Column(String(500))
    score = Column(Float);
    axis = Column(Integer);
    var_proportion = Column(Float);
    var_cumulative = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, simulation_group_id_I,
                 simulation_id_I,
                 score_I, axis_I,
                 var_proportion_I, var_cumulative_I,
                 used_I, comment_I):
        self.simulation_group_id = simulation_group_id_I;
        self.simulation_id = simulation_id_I;
        self.score=score_I
        self.axis=axis_I
        self.var_proportion=var_proportion_I
        self.var_cumulative=var_cumulative_I
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self): # not complete!
        return {'simulation_id_I':self.experiment_id,
                #...
                'used_I':self.used_,
                'comments_I':self.comments_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_pca_loadings(Base):
    __tablename__ = 'data_stage02_physiology_pca_loadings'
    id = Column(Integer, Sequence('data_stage02_physiology_pca_loadings_id_seq'), primary_key=True)
    simulation_group_id = Column(String(50))
    rxn_id = Column(String(100))
    loadings = Column(Float);
    axis = Column(Integer)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, simulation_group_id_I,
                 simulation_id_I,
                 rxn_id_I,
                 loadings_I, axis_I,  
                 used_I, comment_I):
        self.simulation_group_id = simulation_group_id_I;
        self.simulation_id = simulation_id_I;
        self.rxn_id = rxn_id_I;
        self.loadings=loadings_I
        self.axis=axis_I
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self): # not complete!
        return {'simulation_id_I':self.simulation_id,
                #...
                'used_I':self.used_,
                'comments_I':self.comments_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

