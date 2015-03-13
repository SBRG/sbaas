# ORMs
from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage02_isotopomer_simulation(Base):
    __tablename__ = 'data_stage02_isotopomer_simulation'
    id = Column(Integer, Sequence('data_stage02_isotopomer_simulation_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    experiment_id = Column(String(50))
    model_id = Column(String(50))
    mapping_id = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,
            simulation_id_I,
            experiment_id_I,
            model_id_I,mapping_id_I,
            sample_name_abbreviation_I,
            time_point_I,
            used__I,
            comment__I):
        self.simulation_id=simulation_id_I
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.mapping_id=mapping_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {
            'simulation_id':self.simulation_id,
            'experiment_id':self.experiment_id,
            'model_id':self.model_id,
            'mapping_id':self.mapping_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_calcFragments(Base):
    __tablename__ = 'data_stage02_isotopomer_calcFragments'
    id = Column(Integer, Sequence('data_stage02_isotopomer_calcFragments_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50))
    mapping_id = Column(String(100), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    met_id = Column(String(100))
    fragment_name = Column(String(100), primary_key=True)
    fragment_formula = Column(String(500))
    fragment_mass = Column(Integer)
    idv_average = Column(Float);
    idv_stdev = Column(Float);
    idv_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I,
            model_id_I,mapping_id_I,
            sample_name_abbreviation_I,
            time_point_I,
            met_id_I,
            fragment_name_I,
            fragment_formula_I,
            fragment_mass_I,
            idv_average_I,
            idv_stdev_I,
            idv_units_I,
            used__I,
            comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.mapping_id=mapping_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.met_id=met_id_I
        self.fragment_name=fragment_name_I
        self.fragment_formula=fragment_formula_I
        self.fragment_mass=fragment_mass_I
        self.idv_average=idv_average_I
        self.idv_stdev=idv_stdev_I
        self.idv_units=idv_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'model_id':self.model_id,
                'mapping_id':self.mapping_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'met_id':self.met_id,
                'fragment_name':self.fragment_name,
                'fragment_formula':self.fragment_formula,
                'fragment_mass':self.fragment_mass,
                'idv_average':self.idv_average,
                'idv_stdev':self.idv_stdev,
                'idv_units':self.idv_units,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_calcFluxes(Base):
    __tablename__ = 'data_stage02_isotopomer_calcFluxes'
    id = Column(Integer, Sequence('data_stage02_isotopomer_calcFluxes_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    mapping_id = Column(String(100), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    rxn_id = Column(String(100), primary_key=True)
    flux_average = Column(Float);
    flux_stdev = Column(Float);
    flux_lb = Column(Float); # based on 95% CI
    flux_ub = Column(Float);
    flux_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,
            model_id_I,mapping_id_I,
            sample_name_abbreviation_I,
            time_point_I,
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
        self.mapping_id=mapping_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
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
            'mapping_id':self.mapping_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
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

class data_stage02_isotopomer_tracers(Base):
    __tablename__ = 'data_stage02_isotopomer_tracers'
    id = Column(Integer, Sequence('data_stage02_isotopomer_tracers_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    met_id = Column(String(50)) # e.g glc_DASH_D_e
    met_name = Column(String(100)) # e.g. 1-13C Glucose
    isotopomer_formula = Column(postgresql.ARRAY(String(50))) # e.g. ['[13C]HO','CH2O','CH2O','CH2O','CH2O','CH3O']
    met_elements = Column(postgresql.ARRAY(String(3))) # the elements that are labeled (e.g. C,C,C)
    met_atompositions = Column(postgresql.ARRAY(Integer)) #the atoms positions that are labeled (e.g. 1,2,3) 
    ratio = Column(Float)
    supplier = Column(String(100))
    supplier_reference = Column(String(100))
    purity = Column(Float)
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name_abbreviation','met_id','met_name'),
            )

    def __init__(self,experiment_id_I,
            sample_name_abbreviation_I,
            met_id_I,
            met_name_I,
            isotopomer_formula_I,
            met_elements_I,
            met_atompositions_I,
            ratio_I,
            supplier_I,
            supplier_reference_I,
            purity_I,
            comment__I):
        self.experiment_id=experiment_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.met_id=met_id_I
        self.met_name=met_name_I
        self.isotopomer_formula=isotopomer_formula_I
        self.met_elements=met_elements_I
        self.met_atompositions=met_atompositions_I
        self.ratio=ratio_I
        self.supplier=supplier_I
        self.supplier_reference=supplier_reference_I
        self.purity=purity_I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
                'met_id':self.met_id,
                'met_name':self.met_name,
                'isotopomer_formula':self.isotopomer_formula,
                'met_elements':self.met_elements,
                'met_atompositions':self.met_atompositions,
                'ratio':self.ratio,
                'supplier':self.supplier,
                'supplier_reference':self.supplier_reference,
                'purity':self.purity,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage02_isotopomer_models(Base):
    __tablename__ = 'data_stage02_isotopomer_models'
    id = Column(Integer, Sequence('data_stage02_isotopomer_models_id_seq'), primary_key=True)
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
                'file':self.file,
                'file_type':self.file_type,
                'date':self.date}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_modelReactions(Base):
    __tablename__ = 'data_stage02_isotopomer_modelReactions'
    id = Column(Integer, Sequence('data_stage02_isotopomer_modelReactions_id_seq'), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    rxn_id = Column(String(50), primary_key=True)
    rxn_name = Column(String(100))
    equation = Column(String(4000));
    subsystem = Column(String(255));
    gpr = Column(Text);
    genes = Column(postgresql.ARRAY(String(50)));
    reactants_stoichiometry = Column(postgresql.ARRAY(Float)) # stoichiometry of metabolites
    products_stoichiometry = Column(postgresql.ARRAY(Float)) 
    reactants_ids = Column(postgresql.ARRAY(String(100))) # list of met_ids that are in the reaction
    products_ids = Column(postgresql.ARRAY(String(100))) 
    lower_bound = Column(Float) #derived from experimentally measured values or estimations from simulations
    upper_bound = Column(Float) #derived from experimentally measured values or estimations from simulations
    objective_coefficient = Column(Float)
    flux_units = Column(String(50))
    fixed = Column(Boolean)
    free = Column(Boolean)
    reversibility = Column(Boolean)
    weight = Column(Float) #weighting given in the optimization problem
    used_ = Column(Boolean)
    comment_ = Column(Text);

    def __init__(self,model_id_I,
            rxn_id_I,
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
            fixed_I,
            free_I,
            reversibility_I,
            weight_I,
            used__I,
            comment__I):
        self.model_id=model_id_I
        self.rxn_id=rxn_id_I
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
        self.flux_units=flux_units_I
        self.fixed=fixed_I
        self.free=free_I
        self.reversibility=reversibility_I
        self.weight=weight_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'model_id':self.model_id,
            'rxn_id':self.rxn_id,
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
            'fixed':self.fixed,
            'free':self.free,
            'reversibility':self.reversibility,
            'weight':self.weight,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage02_isotopomer_modelMetabolites(Base):
    __tablename__ = 'data_stage02_isotopomer_modelMetabolites'
    id = Column(Integer, Sequence('data_stage02_isotopomer_modelMetabolites_id_seq'), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    met_name = Column(String(500))
    met_id = Column(String(100), primary_key=True)
    formula = Column(String(100))
    charge = Column(Integer)
    compartment = Column(String(50))
    bound = Column(Float)
    constraint_sense = Column(String(5))
    used_ = Column(Boolean)
    comment_ = Column(Text);
    lower_bound = Column(Float) #derived from experimentally measured values or estimations from simulations
    upper_bound = Column(Float) #derived from experimentally measured values or estimations from simulations
    balanced = Column(Boolean)
    fixed = Column(Boolean)

    def __init__(self,model_id_I,
            met_name_I,
            met_id_I,
            formula_I,
            charge_I,
            compartment_I,
            bound_I,
            constraint_sense_I,
            lower_bound_I,
            upper_bound_I,
            balanced_I,
            fixed_I,
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
        self.lower_bound=lower_bound_I
        self.upper_bound=upper_bound_I
        self.balanced=balanced_I
        self.fixed=fixed_I
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
                'lower_bound':self.lower_bound,
                'upper_bound':self.upper_bound,
                'balanced':self.balanced,
                'fixed':self.fixed,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_measuredFluxes(Base):
    __tablename__ = 'data_stage02_isotopomer_measuredFluxes'
    id = Column(Integer, Sequence('data_stage02_isotopomer_measuredFluxes_id_seq'), primary_key=True)
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
    
class data_stage02_isotopomer_measuredPools(Base):
    __tablename__ = 'data_stage02_isotopomer_measuredPools'
    id = Column(Integer, Sequence('data_stage02_isotopomer_measuredPools_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    model_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    met_id = Column(String(50))
    # Time-course simulations only:
    pool_size = Column(Float) # 0 if steady-state
    concentration_average = Column(Float) #derived from experimentally measured values or estimations from simulations
    concentration_var = Column(Float) #derived from experimentally measured values or estimations from simulations
    concentration_lb = Column(Float) #derived from experimentally measured values or estimations from simulations
    concentration_ub = Column(Float) #derived from experimentally measured values or estimations from simulations
    concentration_units = Column(String(50))
    used_ = Column(Boolean)
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,
            model_id_I,
            sample_name_abbreviation_I,
            time_point_I,
            met_id_I,
            pool_size_I,
            concentration_average_I,
            concentration_var_I,
            concentration_lb_I,
            concentration_ub_I,
            concentration_units_I,
            used__I,
            comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.met_id=met_id_I
        self.pool_size=pool_size_I
        self.concentration_average=concentration_average_I
        self.concentration_var=concentration_var_I
        self.concentration_lb=concentration_lb_I
        self.concentration_ub=concentration_ub_I
        self.concentration_units=concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                    'model_id':self.model_id,
                    'sample_name_abbreviation':self.sample_name_abbreviation,
                    'time_point':self.time_point,
                    'met_id':self.met_id,
                    'pool_size':self.pool_size,
                    'concentration_average':self.concentration_average,
                    'concentration_var':self.concentration_var,
                    'concentration_lb':self.concentration_lb,
                    'concentration_ub':self.concentration_ub,
                    'concentration_units':self.concentration_units,
                    'used_':self.used_,
                    'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_measuredFragments(Base):
    __tablename__ = 'data_stage02_isotopomer_measuredFragments'
    id = Column(Integer, Sequence('data_stage02_isotopomer_measuredFragments_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    met_id = Column(String(100))
    fragment_id = Column(String(100))
    fragment_formula = Column(String(500))
    #fragment_mass = Column(Integer)
    #n_replicates = Column(Integer)
    intensity_normalized_average = Column(postgresql.ARRAY(Float))
    intensity_normalized_cv = Column(postgresql.ARRAY(Float))
    intensity_normalized_stdev = Column(postgresql.ARRAY(Float))
    intensity_normalized_units = Column(String(20))
    scan_type = Column(String(50), primary_key=True);
    met_elements = Column(postgresql.ARRAY(String(3))) # the elements that are tracked (e.g. C,C,C)
    met_atompositions = Column(postgresql.ARRAY(Integer)) #the atoms positions that are tracked (e.g. 1,2,3) 
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_abbreviation_I, 
                 time_point_I, met_id_I,fragment_id_I,
                    fragment_formula_I,
                    #fragment_mass_I,
                    #n_replicates_I,
                    intensity_normalized_average_I, intensity_normalized_cv_I,
                    intensity_normalized_stdev_I,
                    intensity_normalized_units_I, scan_type_I,
                    met_elements_I,
                    met_atompositions_I,used__I,comment__I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.met_id = met_id_I;
        self.fragment_id = fragment_id_I;
        self.fragment_formula = fragment_formula_I;
        #self.fragment_mass = fragment_mass_I;
        #self.n_replicates = n_replicates_I;
        self.intensity_normalized_average = intensity_normalized_average_I;
        self.intensity_normalized_cv = intensity_normalized_cv_I;
        self.intensity_normalized_stdev = intensity_normalized_stdev_I;
        self.intensity_normalized_units = intensity_normalized_units_I;
        self.scan_type = scan_type_I;
        self.met_elements=met_elements_I;
        self.met_atompositions=met_atompositions_I;
        self.used_=used__I;
        self.comment_=comment__I;

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'met_id':self.met_id,
                'fragment_id':self.fragment_id,
                'fragment_formula':self.fragment_formula,
                'intensity_normalized_average':self.intensity_normalized_average,
                'intensity_normalized_cv':self.intensity_normalized_cv,
                'intensity_normalized_stdev':self.intensity_normalized_stdev,
                'intensity_normalized_units':self.intensity_normalized_units,
                'scan_type':self.scan_type,
                'met_elements':self.met_elements,
                'met_atompositions':self.met_atompositions,
                'used_':self.used_,
                'comment_':self.comment_};
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_atomMappingReactions(Base):
    __tablename__ = 'data_stage02_isotopomer_atomMappingReactions'
    id = Column(Integer, Sequence('data_stage02_isotopomer_atomMappingReactions_id_seq'), primary_key=True)
    mapping_id = Column(String(100), primary_key=True)
    rxn_id = Column(String(50), primary_key=True)
    rxn_description = Column(String(500))
    reactants_stoichiometry_tracked = Column(postgresql.ARRAY(Float)) # stoichiometry of metabolites (e.g. ['-1','-1'])
    products_stoichiometry_tracked = Column(postgresql.ARRAY(Float))  
    reactants_ids_tracked = Column(postgresql.ARRAY(String(100))) # list of met_ids that are tracked (e.g. ['pyr_c','accoa_c'])
    products_ids_tracked = Column(postgresql.ARRAY(String(100)))
    reactants_elements_tracked = Column(postgresql.JSON) # list of elements that are tracked (e.g. ['C','C'])
    products_elements_tracked = Column(postgresql.JSON)
    reactants_positions_tracked = Column(postgresql.JSON) # list of elements that are tracked (e.g. ['C','C'])
    products_positions_tracked = Column(postgresql.JSON)
    reactants_mapping = Column(postgresql.ARRAY(String(20000))) # mappings of each atom for each met_id that are tracked (e.g. ['abc','de'])
    products_mapping = Column(postgresql.ARRAY(String(20000)))
    rxn_equation = Column(String(5000)) #formatted version of rxn_formula and rxn_mapping depending on the fluxomics software
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,
            #id_I,
            mapping_id_I,
            rxn_id_I,
            rxn_description_I,
            reactants_stoichiometry_tracked_I,
            products_stoichiometry_tracked_I,
            reactants_ids_tracked_I,
            products_ids_tracked_I,
            reactants_elements_tracked_I,
            products_elements_tracked_I,
            reactants_positions_tracked_I,
            products_positions_tracked_I,
            reactants_mapping_I,
            products_mapping_I,
            rxn_equation_I,
            used__I,
            comment__I):
        #self.id=id_I
        self.mapping_id=mapping_id_I
        self.rxn_id=rxn_id_I
        self.rxn_description=rxn_description_I
        self.reactants_stoichiometry_tracked=reactants_stoichiometry_tracked_I
        self.products_stoichiometry_tracked=products_stoichiometry_tracked_I
        self.reactants_ids_tracked=reactants_ids_tracked_I
        self.products_ids_tracked=products_ids_tracked_I
        self.reactants_elements_tracked=reactants_elements_tracked_I
        self.products_elements_tracked=products_elements_tracked_I
        self.reactants_positions_tracked=reactants_positions_tracked_I
        self.products_positions_tracked=products_positions_tracked_I
        self.reactants_mapping=reactants_mapping_I
        self.products_mapping=products_mapping_I
        self.rxn_equation=rxn_equation_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'mapping_id':self.mapping_id,
                'rxn_id':self.rxn_id,
                'rxn_description':self.rxn_description,
                'reactants_stoichiometry_tracked':self.reactants_stoichiometry_tracked,
                'products_stoichiometry_tracked':self.products_stoichiometry_tracked,
                'reactants_ids_tracked':self.reactants_ids_tracked,
                'products_ids_tracked':self.products_ids_tracked,
                'reactants_elements_tracked':self.reactants_elements_tracked,
                'products_elements_tracked':self.products_elements_tracked,
                'reactants_positions_tracked':self.reactants_positions_tracked,
                'products_positions_tracked':self.products_positions_tracked,
                'reactants_mapping':self.reactants_mapping,
                'products_mapping':self.products_mapping,
                'rxn_equation':self.rxn_equation,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__());

class data_stage02_isotopomer_modelReactionsAtomMapping(Base):
    __tablename__ = 'data_stage02_isotopomer_modelReactionsAtomMapping'
    id = Column(Integer, Sequence('data_stage02_isotopomer_modelReactionsAtomMapping_id_seq'), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    mapping_id = Column(String(100), primary_key=True)
    rxn_id = Column(String(50), primary_key=True)
    rxn_name = Column(String(100))
    equation = Column(String(4000));
    subsystem = Column(String(255));
    gpr = Column(Text);
    genes = Column(postgresql.ARRAY(String(50)));
    reactants_stoichiometry = Column(postgresql.ARRAY(Float)) # stoichiometry of metabolites
    products_stoichiometry = Column(postgresql.ARRAY(Float)) 
    reactants_ids = Column(postgresql.ARRAY(String(50))) # list of met_ids that are in the reaction
    products_ids = Column(postgresql.ARRAY(String(50))) 
    reactants_stoichiometry_tracked = Column(postgresql.ARRAY(Float)) # stoichiometry of metabolites
    products_stoichiometry_tracked = Column(postgresql.ARRAY(Float))  
    reactants_ids_tracked = Column(postgresql.ARRAY(String(50))) # list of met_ids that are tracked
    products_ids_tracked = Column(postgresql.ARRAY(String(50)))
    reactants_elements_tracked = Column(postgresql.ARRAY(String(3))) # list of elements that are tracked (e.g. ['C','C'])
    products_elements_tracked = Column(postgresql.ARRAY(String(3)))
    reactants_mapping = Column(postgresql.ARRAY(String(50))) # mappings of each atom for each met_id that are tracked
    products_mapping = Column(postgresql.ARRAY(String(50)))
    rxn_equation = Column(String(1000)) #formatted version of rxn_formula and rxn_mapping depending on the fluxomics software
    lower_bound = Column(Float) #derived from experimentally measured values or estimations from simulations
    upper_bound = Column(Float) #derived from experimentally measured values or estimations from simulations
    objective_coefficient = Column(Float)
    flux_units = Column(String(50))
    fixed = Column(Boolean)
    free = Column(Boolean)
    reversibility = Column(Boolean)
    weight = Column(Float) #weighting given in the optimization problem
    used_ = Column(Boolean)
    comment_ = Column(Text);

    def __init__(self,model_id_I,
            mapping_id_I,
            rxn_id_I,
            equation_I,
            subsystem_I,
            gpr_I,
            genes_I,
            reactants_stoichiometry_I,
            products_stoichiometry_I,
            reactants_ids_I,
            products_ids_I,
            reactants_stoichiometry_tracked_I,
            products_stoichiometry_tracked_I,
            reactants_ids_tracked_I,
            products_ids_tracked_I,
            reactants_elements_tracked_I,
            products_elements_tracked_I,
            reactants_mapping_I,
            products_mapping_I,
            rxn_equation_I,
            lower_bound_I,
            upper_bound_I,
            objective_coefficient_I,
            flux_units_I,
            fixed_I,
            free_I,
            reversibility_I,
            weight_I,
            used__I,
            comment__I):
        self.model_id=model_id_I
        self.mapping_id=mapping_id_I
        self.rxn_id=rxn_id_I
        self.equation=equation_I
        self.subsystem=subsystem_I
        self.gpr=gpr_I
        self.genes=genes_I
        self.reactants_stoichiometry=reactants_stoichiometry_I
        self.products_stoichiometry=products_stoichiometry_I
        self.reactants_ids=reactants_ids_I
        self.products_ids=products_ids_I
        self.reactants_stoichiometry_tracked=reactants_stoichiometry_tracked_I
        self.products_stoichiometry_tracked=products_stoichiometry_tracked_I
        self.reactants_ids_tracked=reactants_ids_tracked_I
        self.products_ids_tracked=products_ids_tracked_I
        self.reactants_elements_tracked=reactants_elements_tracked_I
        self.products_elements_tracked=products_elements_tracked_I
        self.reactants_mapping=reactants_mapping_I
        self.products_mapping=products_mapping_I
        self.rxn_equation=rxn_equation_I
        self.lower_bound=lower_bound_I
        self.upper_bound=upper_bound_I
        self.objective_coefficient=objective_coefficient_I
        self.flux_units=flux_units_I
        self.fixed=fixed_I
        self.free=free_I
        self.reversibility=reversibility_I
        self.weight=weight_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'model_id':self.model_id,
            'rxn_id':self.rxn_id,
            'equation':self.equation,
            'subsystem':self.subsystem,
            'gpr':self.gpr,
            'genes':self.genes,
            'reactants_stoichiometry':self.reactants_stoichiometry,
            'products_stoichiometry':self.products_stoichiometry,
            'reactants_ids':self.reactants_ids,
            'products_ids':self.products_ids,
            'reactants_stoichiometry_tracked':self.reactants_stoichiometry_tracked,
            'products_stoichiometry_tracked':self.products_stoichiometry_tracked,
            'reactants_ids_tracked':self.reactants_ids_tracked,
            'products_ids_tracked':self.products_ids_tracked,
            'reactants_elements_tracked':self.reactants_elements_tracked,
            'products_elements_tracked':self.products_elements_tracked,
            'reactants_mapping':self.reactants_mapping,
            'products_mapping':self.products_mapping,
            'rxn_equation':self.rxn_equation,
            'lower_bound':self.lower_bound,
            'upper_bound':self.upper_bound,
            'objective_coefficient':self.objective_coefficient,
            'flux_units':self.flux_units,
            'fixed':self.fixed,
            'free':self.free,
            'reversibility':self.reversibility,
            'weight':self.weight,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_modelMetabolitesAtomMapping(Base):
    __tablename__ = 'data_stage02_isotopomer_modelMetabolitesAtomMapping'
    id = Column(Integer, Sequence('data_stage02_isotopomer_modelMetabolitesAtomMapping_id_seq'), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    mapping_id = Column(String(100), primary_key=True)
    met_name = Column(String(500))
    met_id = Column(String(50), primary_key=True)
    formula = Column(String(100))
    charge = Column(Integer)
    compartment = Column(String(50))
    bound = Column(Float)
    constraint_sense = Column(String(5))
    lower_bound = Column(Float)
    upper_bound = Column(Float)
    met_elements = Column(postgresql.JSON) # the elements that are tracked (e.g. C,C,C)
    met_atompositions = Column(postgresql.JSON) #the atoms positions that are tracked (e.g. 1,2,3) 
    balanced = Column(Boolean)
    met_symmetry_elements = Column(postgresql.JSON) #symmetric molecules can alternatively be indicated in the reaction mapping
    met_symmetry_atompositions = Column(postgresql.JSON) #maps the symmetric atom positions
    used_ = Column(Boolean)
    comment_ = Column(Text);

    def __init__(self,model_id_I,
            mapping_id_I,
            met_name_I,
            met_id_I,
            formula_I,
            charge_I,
            compartment_I,
            bound_I,
            constraint_sense_I,
            met_elements_I,
            met_atompositions_I,
            balanced_I,
            met_symmetry_elements_I,
            met_symmetry_atompositions_I,
            used__I,
            comment__I):
        self.model_id=model_id_I
        self.mapping_id=mapping_id_I
        self.met_name=met_name_I
        self.met_id=met_id_I
        self.formula=formula_I
        self.charge=charge_I
        self.bound=bound_I
        self.constraint_sense=constraint_sense_I
        self.met_elements=met_elements_I
        self.met_atompositions=met_atompositions_I
        self.compartment=compartment_I
        self.balanced=balanced_I
        self.met_symmetry_elements=met_symmetry_elements_I
        self.met_symmetry_atompositions=met_symmetry_atompositions_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'model_id':self.model_id,
                'met_name':self.met_name,
                'met_id':self.met_id,
                'formula':self.formula,
                'charge':self.charge,
                'compartment':self.compartment,
                'met_elements':self.met_elements,
                'met_atompositions':self.met_atompositions,
                'balanced':self.balanced,
                'met_symmetry_elements':self.met_symmetry_elements,
                'met_symmetry_atompositions':self.met_symmetry_atompositions,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_atomMappingMetabolites(Base):
    __tablename__ = 'data_stage02_isotopomer_atomMappingMetabolites'
    id = Column(Integer, Sequence('data_stage02_isotopomer_atomMappingMetabolites_id_seq'), primary_key=True)
    mapping_id = Column(String(100), primary_key=True)
    #met_name = Column(String(500))
    met_id = Column(String(100), primary_key=True)
    #formula = Column(String(100))
    met_elements = Column(postgresql.ARRAY(String(3))) # the elements that are tracked (e.g. C,C,C)
    met_atompositions = Column(postgresql.ARRAY(Integer)) #the atoms positions that are tracked (e.g. 1,2,3) 
    met_symmetry_elements = Column(postgresql.ARRAY(String(3))) #symmetric molecules can alternatively be indicated in the reaction mapping
    met_symmetry_atompositions = Column(postgresql.ARRAY(Integer)) #maps the symmetric atom positions
    used_ = Column(Boolean)
    comment_ = Column(Text);
    met_mapping=Column(postgresql.JSON())
    #met_mapping=Column(postgresql.ARRAY(String(5000)))
    base_met_ids=Column(postgresql.ARRAY(String(100)))
    base_met_elements=Column(postgresql.JSON())
    #base_met_elements=Column(postgresql.ARRAY(String(3)))
    base_met_atompositions=Column(postgresql.JSON())
    #base_met_atompositions=Column(postgresql.ARRAY(Integer))
    base_met_symmetry_elements=Column(postgresql.JSON())
    #base_met_symmetry_elements=Column(postgresql.ARRAY(String(3)))
    base_met_symmetry_atompositions=Column(postgresql.JSON())
    #base_met_symmetry_atompositions=Column(postgresql.ARRAY(Integer))
    base_met_indices=Column(postgresql.ARRAY(Integer))

    def __init__(self,
            mapping_id_I,
            #met_name_I,
            met_id_I,
            #formula_I,
            met_elements_I,
            met_atompositions_I,
            met_symmetry_elements_I,
            met_symmetry_atompositions_I,
            used__I,
            comment__I,
            met_mapping_I=None,
            base_met_ids_I=None,
            base_met_elements_I=None,
            base_met_atompositions_I=None,
            base_met_symmetry_elements_I=None,
            base_met_symmetry_atompositions_I=None,
            base_met_indices_I=None):
        self.mapping_id=mapping_id_I
        #self.met_name=met_name_I
        self.met_id=met_id_I
        #self.formula=formula_I
        self.met_elements=met_elements_I
        self.met_atompositions=met_atompositions_I
        self.met_symmetry_elements=met_symmetry_elements_I
        self.met_symmetry_atompositions=met_symmetry_atompositions_I
        self.used_=used__I
        self.comment_=comment__I
        self.met_mapping=met_mapping_I;
        self.base_met_ids=base_met_ids_I;
        self.base_met_elements=base_met_elements_I;
        self.base_met_atompositions=base_met_atompositions_I;
        self.base_met_symmetry_elements=base_met_symmetry_elements_I;
        self.base_met_symmetry_atompositions=base_met_symmetry_atompositions_I;
        self.base_met_indices = base_met_indices_I;

    def __repr__dict__(self):
        return {'mapping_id':self.mapping_id,
                #'met_name':self.met_name,
                'met_id':self.met_id,
                #'formula':self.formula,
                'met_elements':self.met_elements,
                'met_atompositions':self.met_atompositions,
                'met_symmetry_elements':self.met_symmetry_elements,
                'met_symmetry_atompositions':self.met_symmetry_atompositions,
                'used_':self.used_,
                'comment_':self.comment_,
                'met_mapping':self.met_mapping,
                'base_met_ids':self.base_met_ids,
                'base_met_elements':self.base_met_elements,
                'base_met_atompositions':self.base_met_atompositions,
                'base_met_symmetry_elements':self.base_met_symmetry_elements,
                'base_met_symmetry_atompositions':self.base_met_symmetry_atompositions,
                'base_met_indices':self.base_met_indices}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_fittedFluxes(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedFluxes'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedFluxes_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #mapping_id = Column(String(100))
    #sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    rxn_id = Column(String(100))
    flux = Column(Float);
    flux_stdev = Column(Float);
    flux_lb = Column(Float); # based on 95% CI
    flux_ub = Column(Float);
    flux_units = Column(String(50));
    fit_alf = Column(Float);
    fit_chi2s = Column(postgresql.ARRAY(Float));
    fit_cor = Column(postgresql.ARRAY(Float));
    fit_cov = Column(postgresql.ARRAY(Float));
    free = Column(Boolean);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,
        #model_id_I,
        #mapping_id_I,
        #sample_name_abbreviation_I,
        #time_point_I,
        rxn_id_I,
        flux_I,
        flux_stdev_I,
        flux_lb_I,
        flux_ub_I,
        flux_units_I,
        fit_alf_I,
        fit_chi2s_I,
        fit_cor_I,
        fit_cov_I,
        free_I,
        used__I,
        comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.rxn_id=rxn_id_I
        self.flux=flux_I
        self.flux_stdev=flux_stdev_I
        self.flux_lb=flux_lb_I
        self.flux_ub=flux_ub_I
        self.flux_units=flux_units_I
        self.fit_alf=fit_alf_I
        self.fit_chi2s=fit_chi2s_I
        self.fit_cor=fit_cor_I
        self.fit_cov=fit_cov_I
        self.free=free_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        #'sample_name_abbreviation':self.sample_name_abbreviation,
        #'time_point':self.time_point,
        'rxn_id':self.rxn_id,
        'flux':self.flux,
        'flux_stdev':self.flux_stdev,
        'flux_lb':self.flux_lb,
        'flux_ub':self.flux_ub,
        'flux_units':self.flux_units,
        'fit_alf':self.fit_alf,
        'fit_chi2s':self.fit_chi2s,
        'fit_cor':self.fit_cor,
        'fit_cov':self.fit_cov,
        'free':self.free,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_isotopomer_fittedFragments(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedFragments'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedFragments_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    experiment_id = Column(String(50));
    #model_id = Column(String(50));
    #mapping_id = Column(String(100));
    sample_name_abbreviation = Column(String(100));
    time_point = Column(String(10));
    fragment_id = Column(String(100));
    #fragment_formula = Column(String(500));
    fragment_mass = Column(Integer);
    fit_val = Column(Float);
    fit_stdev = Column(Float);
    fit_units = Column(String(50));
    fit_alf = Column(Float);
    fit_cor = Column(postgresql.ARRAY(Float));
    fit_cov = Column(postgresql.ARRAY(Float));
    free = Column(Boolean);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','time_point','fragment_id','fragment_mass','simulation_dateAndTime'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        experiment_id_I,
        #model_id_I,
        #mapping_id_I,
        sample_name_abbreviation_I,
        time_point_I,
        fragment_id_I,
        #fragment_formula_I,
        fragment_mass_I,
        fit_val_I,
        fit_stdev_I,
        fit_units_I,
        fit_alf_I,
        fit_cor_I,
        fit_cov_I,
        free_I,
        used__I,
        comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.fragment_id=fragment_id_I
        #self.fragment_formula=fragment_formula_I
        self.fragment_mass=fragment_mass_I
        self.fit_val=fit_val_I
        self.fit_stdev=fit_stdev_I
        self.fit_units=fit_units_I
        self.fit_alf=fit_alf_I
        self.fit_cor=fit_cor_I
        self.fit_cov=fit_cov_I
        self.free=free_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        'sample_name_abbreviation':self.sample_name_abbreviation,
        'time_point':self.time_point,
        'fragment_id':self.fragment_id,
        #'fragment_formula':self.fragment_formula,
        'fragment_mass':self.fragment_mass,
        'fit_val':self.fit_val,
        'fit_stdev':self.fit_stdev,
        'fit_units':self.fit_units,
        'fit_alf':self.fit_alf,
        'fit_chi2s':self.fit_chi2s,
        'fit_cor':self.fit_cor,
        'fit_cov':self.fit_cov,
        'free':self.free,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_isotopomer_fittedData(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedData'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedData_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #mapping_id = Column(String(100))
    #sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    fitted_echi2 = Column(postgresql.ARRAY(Float));
    fitted_alf = Column(Float);
    fitted_chi2 = Column(Float);
    fitted_dof = Column(Integer);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','simulation_dateAndTime'),
            )

    def __init__(self,
        simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,
        #model_id_I,
        #mapping_id_I,
        #sample_name_abbreviation_I,
        #time_point_I,
        fitted_echi2_I,
        fitted_alf_I,
        fitted_chi2_I,
        fitted_dof_I,
        used__I,
        comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.fitted_echi2=fitted_echi2_I
        self.fitted_alf=fitted_alf_I
        self.fitted_chi2=fitted_chi2_I
        self.fitted_dof=fitted_dof_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        #'sample_name_abbreviation':self.sample_name_abbreviation,
        #'time_point':self.time_point,
        'fitted_echi2':self.fitted_echi2,
        'fitted_alf':self.fitted_alf,
        'fitted_chi2':self.fitted_chi2,
        'fitted_dof':self.fitted_dof,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_isotopomer_fittedMeasuredFluxes(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedMeasuredFluxes'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedMeasuredFluxes_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #mapping_id = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    rxn_id = Column(String(100))
    fitted_sres = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime'),
            )

    def __init__(self,
        simulation_id_I,
        simulation_dateAndTime_I,
        experiment_id_I,
        #model_id_I,
        #mapping_id_I,
        sample_name_abbreviation_I,
        #time_point_I,
        rxn_id_I,
        fitted_sres_I,
        used__I,
        comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.rxn_id=rxn_id_I
        self.fitted_sres=fitted_sres_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        'sample_name_abbreviation':self.sample_name_abbreviation,
        #'time_point':self.time_point,
        'rxn_id':self.rxn_id,
        'fitted_sres':self.fitted_sres,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_isotopomer_fittedMeasuredFragments(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedMeasuredFragments'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedMeasuredFragments_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #mapping_id = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    #met_id = Column(String(100))
    fragment_id = Column(String(100))
    #fragment_formula = Column(String(500))
    fitted_sres = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','fragment_id','simulation_dateAndTime'),
            )

    def __init__(self,simulation_id_I,
    simulation_dateAndTime_I,
    experiment_id_I,
    #model_id_I,
    #mapping_id_I,
    sample_name_abbreviation_I,
    #time_point_I,
    #met_id_I,
    fragment_id_I,
    #fragment_formula_I,
    fitted_sres_I,
    used__I,
    comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        #self.met_id=met_id_I
        self.fragment_id=fragment_id_I
        #self.fragment_formula=fragment_formula_I
        self.fitted_sres=fitted_sres_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        'sample_name_abbreviation':self.sample_name_abbreviation,
        #'time_point':self.time_point,
        #'met_id':self.met_id,
        'fragment_id':self.fragment_id,
        #'fragment_formula':self.fragment_formula,
        'fitted_sres':self.fitted_sres,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_isotopomer_fittedMeasuredFluxResiduals(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedMeasuredFluxResiduals'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedMeasuredFluxResiduals_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #mapping_id = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    rxn_id = Column(String(100))
    res_data = Column(Float);
    res_esens = Column(Float);
    res_fit = Column(Float);
    res_msens = Column(Float);
    res_peak = Column(String(100));
    res_stdev = Column(Float);
    res_val = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','rxn_id','time_point','simulation_dateAndTime'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        experiment_id_I,
        #model_id_I,
        #mapping_id_I,
        sample_name_abbreviation_I,
        time_point_I,
        rxn_id_I,
        res_data_I,
        res_esens_I,
        res_fit_I,
        res_msens_I,
        res_peak_I,
        res_stdev_I,
        res_val_I,
        used__I,
        comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.rxn_id=rxn_id_I
        self.res_data=res_data_I
        self.res_esens=res_esens_I
        self.res_fit=res_fit_I
        self.res_msens=res_msens_I
        self.res_peak=res_peak_I
        self.res_stdev=res_stdev_I
        self.res_val=res_val_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        'sample_name_abbreviation':self.sample_name_abbreviation,
        'time_point':self.time_point,
        'rxn_id':self.rxn_id,
        'res_data':self.res_data,
        'res_esens':self.res_esens,
        'res_fit':self.res_fit,
        'res_msens':self.res_msens,
        'res_peak':self.res_peak,
        'res_stdev':self.res_stdev,
        'res_val':self.res_val,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_isotopomer_fittedMeasuredFragmentResiduals(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedMeasuredFragmentResiduals'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedMeasuredFragmentResiduals_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    experiment_id = Column(String(50));
    #model_id = Column(String(50));
    #mapping_id = Column(String(100));
    sample_name_abbreviation = Column(String(100));
    time_point = Column(String(10));
    fragment_id = Column(String(100));
    #fragment_formula = Column(String(500));
    fragment_mass = Column(Integer);
    res_data = Column(Float);
    res_esens = Column(Float);
    res_fit = Column(Float);
    res_msens = Column(Float);
    res_peak = Column(String(100));
    res_stdev = Column(Float);
    res_val = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','time_point','fragment_id','fragment_mass','simulation_dateAndTime'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        experiment_id_I,
        #model_id_I,
        #mapping_id_I,
        sample_name_abbreviation_I,
        time_point_I,
        fragment_id_I,
        #fragment_formula_I,
        fragment_mass_I,
        res_data_I,
        res_esens_I,
        res_fit_I,
        res_msens_I,
        res_peak_I,
        res_stdev_I,
        res_val_I,
        used__I,
        comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.fragment_id=fragment_id_I
        #self.fragment_formula=fragment_formula_I
        self.fragment_mass=fragment_mass_I
        self.res_data=res_data_I
        self.res_esens=res_esens_I
        self.res_fit=res_fit_I
        self.res_msens=res_msens_I
        self.res_peak=res_peak_I
        self.res_stdev=res_stdev_I
        self.res_val=res_val_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        'sample_name_abbreviation':self.sample_name_abbreviation,
        'time_point':self.time_point,
        'fragment_id':self.fragment_id,
        #'fragment_formula':self.fragment_formula,
        'fragment_mass':self.fragment_mass,
        'res_data':self.res_data,
        'res_esens':self.res_esens,
        'res_fit':self.res_fit,
        'res_msens':self.res_msens,
        'res_peak':self.res_peak,
        'res_stdev':self.res_stdev,
        'res_val':self.res_val,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_isotopomer_simulationParameters(Base):
    __tablename__ = 'data_stage02_isotopomer_simulationParameters'
    id = Column(Integer, Sequence('data_stage02_isotopomer_simulationParameters_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    cont_alpha = Column(Float);
    cont_reltol = Column(Float);
    cont_steps = Column(Float);
    fit_nudge = Column(Float);
    fit_reinit = Column(Boolean);
    fit_reltol = Column(Float);
    fit_starts = Column(Float);
    fit_tau = Column(Float);
    hpc_mcr = Column(String(50));
    hpc_on = Column(Boolean);
    hpc_serve = Column(String(50));
    int_maxstep = Column(Float);
    int_reltol = Column(Float);
    int_senstol = Column(Float);
    int_timeout = Column(Float);
    int_tspan = Column(Float);
    ms_correct = Column(Boolean);
    oed_crit = Column(String(50))
    oed_reinit = Column(Boolean);
    oed_tolf = Column(Float);
    oed_tolx = Column(Float);
    sim_more = Column(Boolean);
    sim_na = Column(Boolean);
    sim_sens = Column(Boolean);
    sim_ss = Column(Boolean);
    sim_tunit = Column(String(50));

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','simulation_dateAndTime'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        cont_alpha_I,
        cont_reltol_I,
        cont_steps_I,
        fit_nudge_I,
        fit_reinit_I,
        fit_reltol_I,
        fit_starts_I,
        fit_tau_I,
        hpc_mcr_I,
        hpc_on_I,
        hpc_serve_I,
        int_maxstep_I,
        int_reltol_I,
        int_senstol_I,
        int_timeout_I,
        int_tspan_I,
        ms_correct_I,
        oed_crit_I,
        oed_reinit_I,
        oed_tolf_I,
        oed_tolx_I,
        sim_more_I,
        sim_na_I,
        sim_sens_I,
        sim_ss_I,
        sim_tunit_I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        self.cont_alpha=cont_alpha_I
        self.cont_reltol=cont_reltol_I
        self.cont_steps=cont_steps_I
        self.fit_nudge=fit_nudge_I
        self.fit_reinit=fit_reinit_I
        self.fit_reltol=fit_reltol_I
        self.fit_starts=fit_starts_I
        self.fit_tau=fit_tau_I
        self.hpc_mcr=hpc_mcr_I
        self.hpc_on=hpc_on_I
        self.hpc_serve=hpc_serve_I
        self.int_maxstep=int_maxstep_I
        self.int_reltol=int_reltol_I
        self.int_senstol=int_senstol_I
        self.int_timeout=int_timeout_I
        self.int_tspan=int_tspan_I
        self.ms_correct=ms_correct_I
        self.oed_crit=oed_crit_I
        self.oed_reinit=oed_reinit_I
        self.oed_tolf=oed_tolf_I
        self.oed_tolx=oed_tolx_I
        self.sim_more=sim_more_I
        self.sim_na=sim_na_I
        self.sim_sens=sim_sens_I
        self.sim_ss=sim_ss_I
        self.sim_tunit=sim_tunit_I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
            'simulation_dateAndTime':self.simulation_dateAndTime,
            'cont_alpha':self.cont_alpha,
            'cont_reltol':self.cont_reltol,
            'cont_steps':self.cont_steps,
            'fit_nudge':self.fit_nudge,
            'fit_reinit':self.fit_reinit,
            'fit_reltol':self.fit_reltol,
            'fit_starts':self.fit_starts,
            'fit_tau':self.fit_tau,
            'hpc_mcr':self.hpc_mcr,
            'hpc_on':self.hpc_on,
            'hpc_serve':self.hpc_serve,
            'int_maxstep':self.int_maxstep,
            'int_reltol':self.int_reltol,
            'int_senstol':self.int_senstol,
            'int_timeout':self.int_timeout,
            'int_tspan':self.int_tspan,
            'ms_correct':self.ms_correct,
            'oed_crit':self.oed_crit,
            'oed_reinit':self.oed_reinit,
            'oed_tolf':self.oed_tolf,
            'oed_tolx':self.oed_tolx,
            'sim_more':self.sim_more,
            'sim_na':self.sim_na,
            'sim_sens':self.sim_sens,
            'sim_ss':self.sim_ss,
            'sim_tunit':self.sim_tunit}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_fittedNetFluxes(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedNetFluxes'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedNetFluxes_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #mapping_id = Column(String(100))
    #sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    rxn_id = Column(String(100))
    flux = Column(Float);
    flux_stdev = Column(Float);
    flux_lb = Column(Float); # based on 95% CI
    flux_ub = Column(Float);
    flux_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','rxn_id','simulation_dateAndTime','flux_units'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,
        #model_id_I,
        #mapping_id_I,
        #sample_name_abbreviation_I,
        #time_point_I,
        rxn_id_I,
        flux_I,
        flux_stdev_I,
        flux_lb_I,
        flux_ub_I,
        flux_units_I,
        used__I,
        comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.rxn_id=rxn_id_I
        self.flux=flux_I
        self.flux_stdev=flux_stdev_I
        self.flux_lb=flux_lb_I
        self.flux_ub=flux_ub_I
        self.flux_units=flux_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        #'sample_name_abbreviation':self.sample_name_abbreviation,
        #'time_point':self.time_point,
        'rxn_id':self.rxn_id,
        'flux':self.flux,
        'flux_stdev':self.flux_stdev,
        'flux_lb':self.flux_lb,
        'flux_ub':self.flux_ub,
        'flux_units':self.flux_units,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_fittedFluxRatios(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedFluxRatios'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedFluxRatios_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #mapping_id = Column(String(100))
    #sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    ratio_id = Column(String(100))
    ratio_rxn_ids = Column(postgresql.ARRAY(String(100)))
    ratio = Column(Float);
    ratio_stdev = Column(Float);
    ratio_lb = Column(Float); # based on 95% CI
    ratio_ub = Column(Float);
    ratio_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','ratio_id','simulation_dateAndTime','ratio_units'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,
        #model_id_I,
        #mapping_id_I,
        #sample_name_abbreviation_I,
        #time_point_I,
        ratio_id_I,
        ratio_rxn_ids_I,
        ratio_I,
        ratio_stdev_I,
        ratio_lb_I,
        ratio_ub_I,
        ratio_units_I,
        used__I,
        comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.ratio_id=ratio_id_I
        self.ratio_rxn_ids=ratio_rxn_ids_I
        self.ratio=ratio_I
        self.ratio_stdev=ratio_stdev_I
        self.ratio_lb=ratio_lb_I
        self.ratio_ub=ratio_ub_I
        self.ratio_units=ratio_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        #'sample_name_abbreviation':self.sample_name_abbreviation,
        #'time_point':self.time_point,
        'ratio_id':self.ratio_id,
        'ratio_rxn_ids':self.ratio_rxn_ids,
        'ratio':self.ratio,
        'ratio_stdev':self.ratio_stdev,
        'ratio_lb':self.ratio_lb,
        'ratio_ub':self.ratio_ub,
        'ratio_units':self.ratio_units,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_isotopomer_fittedFluxSplits(Base):
    __tablename__ = 'data_stage02_isotopomer_fittedFluxSplits'
    id = Column(Integer, Sequence('data_stage02_isotopomer_fittedFluxSplits_id_seq'), primary_key=True)
    simulation_id = Column(String(500))
    simulation_dateAndTime = Column(DateTime);
    #experiment_id = Column(String(50))
    #model_id = Column(String(50))
    #mapping_id = Column(String(100))
    #sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    split_id = Column(String(100))
    split_rxn_id = Column(String(100))
    split = Column(Float);
    split_stdev = Column(Float);
    split_lb = Column(Float); # based on 95% CI
    split_ub = Column(Float);
    split_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            #ForeignKeyConstraint(['simulation_id'], ['data_stage02_isotopomer_simulation.simulation_id']),
            UniqueConstraint('simulation_id','split_id','split_rxn_id','simulation_dateAndTime','split_units'),
            )

    def __init__(self,simulation_id_I,
        simulation_dateAndTime_I,
        #experiment_id_I,
        #model_id_I,
        #mapping_id_I,
        #sample_name_abbreviation_I,
        #time_point_I,
        split_id_I,
        split_rxn_id_I,
        split_I,
        split_stdev_I,
        split_lb_I,
        split_ub_I,
        split_units_I,
        used__I,
        comment__I):
        self.simulation_id=simulation_id_I
        self.simulation_dateAndTime=simulation_dateAndTime_I
        #self.experiment_id=experiment_id_I
        #self.model_id=model_id_I
        #self.mapping_id=mapping_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
        self.split_id=split_id_I
        self.split_rxn_id=split_rxn_id_I
        self.split=split_I
        self.split_stdev=split_stdev_I
        self.split_lb=split_lb_I
        self.split_ub=split_ub_I
        self.split_units=split_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'simulation_id':self.simulation_id,
        'simulation_dateAndTime':self.simulation_dateAndTime,
        #'experiment_id':self.experiment_id,
        #'model_id':self.model_id,
        #'mapping_id':self.mapping_id,
        #'sample_name_abbreviation':self.sample_name_abbreviation,
        #'time_point':self.time_point,
        'split_id':self.split_id,
        'split_rxn_id':self.split_rxn_id,
        'split':self.split,
        'split_stdev':self.split_stdev,
        'split_lb':self.split_lb,
        'split_ub':self.split_ub,
        'split_units':self.split_units,
        'used_':self.used_,
        'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())