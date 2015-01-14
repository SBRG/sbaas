# models_stage03_quantification
# i.e. thermodynamics

# ORMs
from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage02_physiology_simulatedData(Base):
    __tablename__ = 'data_stage02_physiology_simulatedData'
    id = Column(Integer, Sequence('data_stage02_physiology_simulatedData_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    rxn_id = Column(String(100), primary_key=True)
    fba_flux = Column(Float);
    fva_minimum = Column(Float);
    fva_maximum = Column(Float);
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    sra_gr = Column(Float);
    sra_gr_ratio = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,model_id_I,
            sample_name_abbreviation_I,rxn_id_I,fba_flux_I,
                 fva_minimum_I,fva_maximum_I,flux_units_I,
                 sra_gr_I,sra_gr_ratio_I,
                 used__I,comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
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
        return {'experiment_id':self.experiment_id,
                'model_id':self.model_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
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
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    #time_point = Column(String(10), primary_key=True)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,
            model_id_I,
            sample_name_abbreviation_I,
            #time_point_I,
            used__I,
            comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {
            'experiment_id':self.experiment_id,
            'model_id':self.model_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            #'time_point':self.time_point,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage02_physiology_models(Base):
    __tablename__ = 'data_stage02_physiology_models'
    id = Column(Integer, Sequence('data_stage02_physiology_models_id_seq'), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    model_name = Column(String(100))
    model_description = Column(String(100))
    model_file = Column(Text)
    file_type = Column(String(50))
    date = Column(DateTime)

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
    model_id = Column(String(50), primary_key=True)
    rxn_id = Column(String(50), primary_key=True)
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
    model_id = Column(String(50), primary_key=True)
    met_name = Column(String(500))
    met_id = Column(String(50), primary_key=True)
    formula = Column(String(100))
    charge = Column(Integer)
    compartment = Column(String(50))
    bound = Column(Float)
    constraint_sense = Column(String(5))
    used_ = Column(Boolean);
    comment_ = Column(Text);

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
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50))
    sample_name_abbreviation = Column(String(100), primary_key=True)
    #time_point = Column(String(10), primary_key=True)
    rxn_id = Column(String(100), primary_key=True)
    flux_average = Column(Float);
    flux_stdev = Column(Float);
    flux_lb = Column(Float); # based on 95% CI
    flux_ub = Column(Float);
    flux_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

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
    id = Column(Integer, Sequence('data_stage02_physiology_sampledPoints_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    rxn_id = Column(String(100), primary_key=True)
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    mixed_fraction = Column(Float); #
    sampling_points = Column(postgresql.ARRAY(Float)); #
    data_dir = Column(String(500)); #
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,model_id_I,
            sample_name_abbreviation_I,rxn_id_I,flux_units_I,
            mixed_fraction_I,sampling_points_I,data_dir_I,
                 used__I,comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.rxn_id=rxn_id_I
        self.flux_units=flux_units_I
        self.mixed_fraction=mixed_fraction_I
        self.sampling_points=sampling_points_I
        self.data_dir=data_dir_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'model_id':self.model_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
                'rxn_id':self.rxn_id,
                'flux_units':self.flux_units,
                'sampling_points':self.sampling_points,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_physiology_sampledData(Base):
    __tablename__ = 'data_stage02_physiology_sampledData'
    id = Column(Integer, Sequence('data_stage02_physiology_sampledData_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    rxn_id = Column(String(100), primary_key=True)
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    sampling_ave = Column(Float);
    sampling_var = Column(Float);
    sampling_lb = Column(Float);
    sampling_ub = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,model_id_I,
            sample_name_abbreviation_I,rxn_id_I,flux_units_I,
                 sampling_ave_I,sampling_var_I,sampling_lb_I,sampling_ub_I,
                 used__I,comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.rxn_id=rxn_id_I
        self.flux_units=flux_units_I
        self.sampling_ave=sampling_ave_I
        self.sampling_var=sampling_var_I
        self.sampling_lb=sampling_lb_I
        self.sampling_ub=sampling_ub_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'model_id':self.model_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
                'rxn_id':self.rxn_id,
                'flux_units':self.flux_units,
                'sampling_ave':self.sampling_ave,
                'sampling_var':self.sampling_var,
                'sampling_lb':self.sampling_lb,
                'sampling_ub':self.sampling_ub,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())