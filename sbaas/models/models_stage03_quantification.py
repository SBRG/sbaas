# models_stage03_quantification
# i.e. thermodynamics

# ORMs
from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage03_quantification_simulatedData(Base):
    __tablename__ = 'data_stage03_quantification_simulatedData'
    id = Column(Integer, Sequence('data_stage03_quantification_simulatedData_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    #sample_name_abbreviation = Column(String(100), primary_key=True)
    #time_point = Column(String(10), primary_key=True)
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
                 #sample_name_abbreviation_I,
                 #time_point_I,
                 rxn_id_I,fba_flux_I,
                 fva_minimum_I,fva_maximum_I,flux_units_I,
                 sra_gr_I,sra_gr_ratio_I,used__I,comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        #self.sample_name_abbreviation=sample_name_abbreviation_I
        #self.time_point=time_point_I
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
                #'sample_name_abbreviation':self.sample_name_abbreviation,
                #'time_point':self.time_point,
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

class data_stage03_quantification_otherData(Base):
    __tablename__ = 'data_stage03_quantification_otherData'
    id = Column(Integer, Sequence('data_stage03_quantification_otherData_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    compartment_id = Column(String(25), primary_key=True)
    pH = Column(Float);
    temperature = Column(Float);
    temperature_units = Column(String(50));
    ionic_strength = Column(Float);
    ionic_strength_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,sample_name_abbreviation_I,
                 time_point_I,compartment_id_I,pH_I,
                 temperature_I,temperature_units_I,ionic_strength_I,
                 ionic_strength_units_I,used__I,comment__I):
        self.experiment_id=experiment_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.compartment_id=compartment_id_I
        self.pH=pH_I
        self.temperature=temperature_I
        self.temperature_units=temperature_units_I
        self.ionic_strength=ionic_strength_I
        self.ionic_strength_units=ionic_strength_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'compartment_id':self.compartment_id,
                'pH':self.pH,
                'temperature':self.temperature,
                'temperature_units':self.temperature_units,
                'ionic_strength':self.ionic_strength,
                'ionic_strength_units':self.ionic_strength_units,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_dG0_r(Base):
    __tablename__ = 'data_stage03_quantification_dG0_r'
    id = Column(Integer, Sequence('data_stage03_quantification_dG0_r_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    rxn_id = Column(String(100), primary_key=True)
    Keq_lb = Column(Float)
    Keq_ub = Column(Float)
    dG0_r = Column(Float);
    dG0_r_var = Column(Float);
    dG0_r_units = Column(String(50));
    dG0_r_lb = Column(Float);
    dG0_r_ub = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,model_id_I,sample_name_abbreviation_I,
                 time_point_I,rxn_id_I,Keq_lb_I,Keq_ub_I,
                 dG0_r_I,dG0_r_var_I,dG0_r_units_I,dG0_r_lb_I,
                 dG0_r_ub_I,used_I,comment_I):
        self.experiment_id = experiment_id_I;
        self.model_id = model_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.rxn_id = rxn_id_I;
        self.Keq_lb = Keq_lb_I;
        self.Keq_ub = Keq_ub_I;
        self.dG0_r = dG0_r_I;
        self.dG0_r_var = dG0_r_var_I;
        self.dG0_r_units = dG0_r_units_I;
        self.dG0_r_lb = dG0_r_lb_I;
        self.dG0_r_ub = dG0_r_ub_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'model_id':self.model_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'sample_type':self.sample_type,
                'time_point':self.time_point,
                'rxn_id':self.rxn_id,
                'Keq_lb':self.Keq_lb,
                'Keq_ub':self.Keq_ub,
                'dG0_r':self.dG0_r,
                'dG0_r_var':self.dG0_r_var,
                'dG0_r_units':self.dG0_r_units,
                'dG0_r_lb':self.dG0_r_lb,
                'dG0_r_ub':self.dG0_r_ub,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_dG_r(Base):
    __tablename__ = 'data_stage03_quantification_dG_r'
    id = Column(Integer, Sequence('data_stage03_quantification_dG_r_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    rxn_id = Column(String(100), primary_key=True)
    Keq_lb = Column(Float)
    Keq_ub = Column(Float)
    dG_r = Column(Float);
    dG_r_var = Column(Float);
    dG_r_units = Column(String(50));
    dG_r_lb = Column(Float);
    dG_r_ub = Column(Float);
    displacement_lb = Column(Float);
    displacement_ub = Column(Float);
    Q_lb = Column(Float);
    Q_ub = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,
                    model_id_I,
                    sample_name_abbreviation_I,
                    time_point_I,
                    rxn_id_I,
                    Keq_lb_I,
                    Keq_ub_I,
                    dG_r_I,
                    dG_r_var_I,
                    dG_r_units_I,
                    dG_r_lb_I,
                    dG_r_ub_I,
                    displacement_lb_I,
                    displacement_ub_I,
                    Q_lb_I,
                    Q_ub_I,
                    used__I,
                    comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.rxn_id=rxn_id_I
        self.Keq_lb = Keq_lb_I;
        self.Keq_ub = Keq_ub_I;
        self.dG_r=dG_r_I
        self.dG_r_var=dG_r_var_I
        self.dG_r_units=dG_r_units_I
        self.dG_r_lb=dG_r_lb_I
        self.dG_r_ub=dG_r_ub_I
        self.displacement_lb=displacement_lb_I
        self.displacement_ub=displacement_ub_I
        self.Q_lb=Q_lb_I
        self.Q_ub=Q_ub_I
        self.used_=used__I
        self.comment_=comment__I;

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'model_id':self.model_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'rxn_id':self.rxn_id,
                'Keq_lb':self.Keq_lb,
                'Keq_ub':self.Keq_ub,
                'dG_r':self.dG_r,
                'dG_r_var':self.dG_r_var,
                'dG_r_units':self.dG_r_units,
                'dG_r_lb':self.dG_r_lb,
                'dG_r_ub':self.dG_r_ub,
                'displacement_lb':self.displacement_lb,
                'displacement_ub':self.displacement_ub,
                'Q_lb':self.Q_lb,
                'Q_ub':self.Q_ub,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_dG0_f(Base):
    __tablename__ = 'data_stage03_quantification_dG0_f'
    id = Column(Integer, Sequence('data_stage03_quantification_dG0_f_id_seq'), primary_key=True)
    reference_id = Column(String(100), primary_key=True)
    met_name = Column(String(500))
    met_id = Column(String(100))
    KEGG_id = Column(String(20), primary_key=True)
    priority = Column(Integer, primary_key=True);
    dG0_f = Column(Float);
    dG0_f_var = Column(Float);
    dG0_f_units = Column(String(50));
    temperature = Column(Float, default=298.15);
    temperature_units = Column(String(50), default='K');
    ionic_strength = Column(Float, default=0.0);
    ionic_strength_units = Column(String(50),default='M');
    pH = Column(Float, default=0.0);
    pH_units = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, reference_id_I, met_name_I, met_id_I, KEGG_id_I, priority_I,
                 dG0_f_I, dG0_f_var_I, dG0_f_units_I, temperature_I, temperature_units_I, ionic_strength_I, ionic_strength_units_I,
                 pH_I, pH_units_I, used_I, comment_I):
        self.reference_id = reference_id_I;
        self.met_name = met_name_I;
        self.met_id = met_id_I;
        self.KEGG_id = KEGG_id_I;
        self.priority = priority_I;
        self.dG0_f = dG0_f_I;
        self.dG0_f_var = dG0_f_var_I;
        self.dG0_f_units = dG0_f_units_I;
        self.temperature = temperature_I;
        self.temperature_units = temperature_units_I;
        self.ionic_strength = ionic_strength_I;
        self.ionic_strength_units = ionic_strength_units_I;
        self.pH = pH_I;
        self.pH_units = pH_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'reference_id':self.reference_id,
                'met_name':self.met_name,
                'met_id':self.met_id,
                'KEGG_ID':self.KEGG_id,
                'priority':self.priority,
                'dG0_f':self.dG0_f,
                'dG0_f_var':self.dG0_f_var,
                'dG0_f_units':self.dG0_f_units,
                'temperature':self.temperature,
                'temperature_units':self.temperature_units,
                'ionic_strength':self.ionic_strength,
                'ionic_strength_units':self.ionic_strength_units,
                'pH':self.pH,
                'pH_units':self.pH_units,
                'used_':self.used_,
                'comments_':self.comments_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_dG_f(Base):
    __tablename__ = 'data_stage03_quantification_dG_f'
    id = Column(Integer, Sequence('data_stage03_quantification_dG_f_id_seq'), primary_key=True)
    experiment_id = Column(String(100), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    met_name = Column(String(500))
    met_id = Column(String(100), primary_key=True)
    dG_f = Column(Float);
    dG_f_var = Column(Float);
    dG_f_units = Column(String(50));
    dG_f_lb = Column(Float);
    dG_f_ub = Column(Float);
    temperature = Column(Float);
    temperature_units = Column(String(50));
    ionic_strength = Column(Float);
    ionic_strength_units = Column(String(50));
    pH = Column(Float);
    pH_units = Column(String(50));
    measured = Column(Boolean);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I,model_id_I,sample_name_abbreviation_I,
                 time_point_I, met_name_I, met_id_I,
                 dG_f_I, dG_f_var_I, dG_f_units_I, 
                 dG_f_lb_I, dG_f_ub_I, temperature_I, temperature_units_I,
                 ionic_strength_I, ionic_strength_units_I,
                 pH_I, pH_units_I, measured_I, used_I, comment_I):
        self.experiment_id = experiment_id_I;
        self.model_id = model_id_I;
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.met_name = met_name_I;
        self.met_id = met_id_I;
        self.dG_f = dG_f_I;
        self.dG_f_var = dG_f_var_I;
        self.dG_f_units = dG_f_units_I;
        self.dG_f_lb = dG_f_lb_I;
        self.dG_f_ub = dG_f_ub_I;
        self.temperature = temperature_I;
        self.temperature_units = temperature_units_I;
        self.ionic_strength = ionic_strength_I;
        self.ionic_strength_units = ionic_strength_units_I;
        self.pH = pH_I;
        self.pH_units = pH_units_I;
        self.measured = measured_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self): 
        return {'experiment_id':self.experiment_id,
                'model_id':self.model_id,
                    'sample_name_abbreviation':self.sample_name_abbreviation,
                    'time_point':self.time_point,
                    'met_name':self.met_name,
                    'met_id':self.met_id,
                    'dG_f':self.dG_f,
                    'dG_f_var':self.dG_f_var,
                    'dG_f_units':self.dG_f_units,
                    'dG_f_lb':self.dG_f_lb,
                    'dG_f_ub':self.dG_f_ub,
                    'temperature':self.temperature,
                    'temperature_units':self.temperature_units,
                    'ionic_strength':self.ionic_strength,
                    'ionic_strength_units':self.ionic_strength_units,
                    'pH':self.pH,
                    'pH_units':self.pH_units,
                    'measured':self.measured,
                    'used_':self.used_,
                    'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_metabolomicsData(Base):
    __tablename__ = 'data_stage03_quantification_metabolomicsData'
    id = Column(Integer, Sequence('data_stage03_quantification_metabolomicsData_id_seq'), primary_key=True)
    experiment_id = Column(String(100), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    met_id = Column(String(100), primary_key=True)
    concentration = Column(Float);
    concentration_var = Column(Float);
    concentration_units = Column(String(50));
    concentration_lb = Column(Float);
    concentration_ub = Column(Float);
    measured = Column(Boolean);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_abbreviation_I,
                 time_point_I, met_id_I,
                 concentration_I, concentration_var_I, concentration_units_I, concentration_lb_I,
                 concentration_ub_I,
                 measured_I, used__I, comment__I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.met_id = met_id_I;
        self.concentration = concentration_I;
        self.concentration_var = concentration_var_I;
        self.concentration_units = concentration_units_I;
        self.concentration_lb = concentration_lb_I;
        self.concentration_ub = concentration_ub_I;
        self.measured = measured_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self): # not complete!
        return {'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'met_id':self.met_id,
                'concentration':self.concentration,
                'concentration_var':self.concentration_var,
                'concentration_units':self.concentration_units,
                'concentration_lb':self.concentration_lb,
                'concentration_ub':self.concentration_ub,
                'measured':self.measured,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_tcc(Base):
    __tablename__ = 'data_stage03_quantification_tcc'
    id = Column(Integer, Sequence('data_stage03_quantification_tcc_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    rxn_id = Column(String(100), primary_key=True)
    feasible = Column(Boolean);
    measured_concentration_coverage_criteria = Column(Float, default = 0.5);
    measured_dG_f_coverage_criteria = Column(Float, default = 0.99);
    measured_concentration_coverage = Column(Float);
    measured_dG_f_coverage = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I, model_id_I,sample_name_abbreviation_I,
                time_point_I,rxn_id_I,feasible_I,
                measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I,
                measured_concentration_coverage_I,measured_dG_f_coverage_I,
                used__I,comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.rxn_id=rxn_id_I
        self.feasible=feasible_I
        self.measured_concentration_coverage_criteria=measured_concentration_coverage_criteria_I
        self.measured_dG_f_coverage_criteria=measured_dG_f_coverage_criteria_I
        self.measured_concentration_coverage=measured_concentration_coverage_I
        self.measured_dG_f_coverage=measured_dG_f_coverage_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
            'model_id':self.model_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
            'rxn_id':self.rxn_id,
            'feasible':self.feasible,
            'measured_concentration_coverage_criteria':self.measured_concentration_coverage_criteria,
            'measured_dG_f_coverage_criteria':self.measured_dG_f_coverage_criteria,
            'measured_concentration_coverage':self.measured_concentration_coverage,
            'measured_dG_f_coverage':self.measured_dG_f_coverage,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_dG_p(Base):
    __tablename__ = 'data_stage03_quantification_dG_p'
    id = Column(Integer, Sequence('data_stage03_quantification_dG_p_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    pathway_id = Column(String(100), primary_key=True)
    dG_p = Column(Float);
    dG_p_var = Column(Float);
    dG_p_units = Column(String(50));
    dG_p_lb = Column(Float);
    dG_p_ub = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,model_id_I,sample_name_abbreviation_I,
                 time_point_I,pathway_id_I,
                 dG_p_I,dG_p_var_I,dG_p_units_I,dG_p_lb_I,
                 dG_p_ub_I,used_I,comment_I,):
        self.experiment_id = experiment_id_I;
        self.model_id = model_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.pathway_id = pathway_id_I;
        self.dG_p = dG_p_I;
        self.dG_p_var = dG_p_var_I;
        self.dG_p_units = dG_p_units_I;
        self.dG_p_lb = dG_p_lb_I;
        self.dG_p_ub = dG_p_ub_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'model_id':self.model_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'pathway_id':self.pathway_id,
                'dG_p':self.dG_p,
                'dG_p_var':self.dG_p_var,
                'dG_p_units':self.dG_p_units,
                'dG_p_lb':self.dG_p_lb,
                'dG_p_ub':self.dG_p_ub,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_dG0_p(Base):
    __tablename__ = 'data_stage03_quantification_dG0_p'
    id = Column(Integer, Sequence('data_stage03_quantification_dG0_p_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    pathway_id = Column(String(100), primary_key=True)
    dG0_p = Column(Float);
    dG0_p_var = Column(Float);
    dG0_p_units = Column(String(50));
    dG0_p_lb = Column(Float);
    dG0_p_ub = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,model_id_I,sample_name_abbreviation_I,
                 time_point_I,pathway_id_I,
                 dG0_p_I,dG0_p_var_I,dG0_p_units_I,dG0_p_lb_I,
                 dG0_p_ub_I,used_I,comment_I,):
        self.experiment_id = experiment_id_I;
        self.model_id = model_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.pathway_id = pathway_id_I;
        self.dG0_p = dG0_p_I;
        self.dG0_p_var = dG0_p_var_I;
        self.dG0_p_units = dG0_p_units_I;
        self.dG0_p_lb = dG0_p_lb_I;
        self.dG0_p_ub = dG0_p_ub_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'model_id':self.model_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'pathway_id':self.pathway_id,
                'dG0_p':self.dG0_p,
                'dG0_p_var':self.dG0_p_var,
                'dG0_p_units':self.dG0_p_units,
                'dG0_p_lb':self.dG0_p_lb,
                'dG0_p_ub':self.dG0_p_ub,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage03_quantification_metid2keggid(Base):
    __tablename__ = 'data_stage03_quantification_metid2keggid'
    id = Column(Integer, Sequence('data_stage03_quantification_metid2keggid_id_seq'), primary_key=True)
    met_id = Column(String(100))
    KEGG_id = Column(String(20), primary_key=True)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, met_id_I, KEGG_id_I, used_I, comment_I):
        self.met_id = met_id_I;
        self.KEGG_id = KEGG_id_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self): # not complete!
        return {
                'met_id':self.met_id,
                'KEGG_ID':self.KEGG_id,
                'used_':self.used_,
                'comments_':self.comments_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_simulation(Base):
    __tablename__ = 'data_stage03_quantification_simulation'
    id = Column(Integer, Sequence('data_stage03_quantification_simulation_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,
            model_id_I,
            sample_name_abbreviation_I,
            time_point_I,
            used__I,
            comment__I):
        self.experiment_id=experiment_id_I
        self.model_id=model_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {
            'experiment_id':self.experiment_id,
            'model_id':self.model_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage03_quantification_models(Base):
    __tablename__ = 'data_stage03_quantification_models'
    id = Column(Integer, Sequence('data_stage03_quantification_models_id_seq'), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    model_name = Column(String(100))
    model_description = Column(String(100))
    sbml_file = Column(Text)
    date = Column(DateTime)

    def __init__(self,model_id_I,
            model_name_I,
            model_description_I,
            sbml_file_I,
            date_I):
        self.model_id=model_id_I
        self.model_name=model_name_I
        self.model_description=model_description_I
        self.sbml_file=sbml_file_I
        self.date=date_I

    def __repr__dict__(self):
        return {'model_id':self.model_id,
                'model_name':self.model_name,
                'model_description':self.model_description,
                'sbml_file':self.sbml_file,
                'date':self.date}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_modelReactions(Base):
    __tablename__ = 'data_stage03_quantification_modelReactions'
    id = Column(Integer, Sequence('data_stage03_quantification_modelReactions_id_seq'), primary_key=True)
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
    
class data_stage03_quantification_modelMetabolites(Base):
    __tablename__ = 'data_stage03_quantification_modelMetabolites'
    id = Column(Integer, Sequence('data_stage03_quantification_modelMetabolites_id_seq'), primary_key=True)
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

class data_stage03_quantification_modelPathways(Base):
    __tablename__ = 'data_stage03_quantification_modelPathways'
    id = Column(Integer, Sequence('data_stage03_quantification_modelPathways_id_seq'), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    pathway_id = Column(String(100), primary_key=True)
    reactions = Column(postgresql.ARRAY(String(100)))
    stoichiometry = Column(postgresql.ARRAY(Float))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,model_id_I,pathway_id_I,
                 reactions_I,stoichiometry_I,used_I,comment_I,):
        self.model_id = model_id_I;
        self.pathway_id = pathway_id_I;
        self.reactions = reactions_I;
        self.stoichiometry = stoichiometry_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
                'model_id':self.model_id,
                'pathway_id':self.pathway_id,
                'reactions':self.reactions,
                'stoichiometry':self.stoichiometry,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#TODO:
class data_stage03_quantification_tfbaReactions(Base):
    __tablename__ = 'data_stage03_quantification_tfbaReactions'
    id = Column(Integer, Sequence('data_stage03_quantification_tfbaReactions_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    model_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    rxn_id = Column(String(100), primary_key=True)
    flux_units = Column(String(50), default = 'mmol*gDW-1*hr-1');
    tfba_flux = Column(Float);
    tfva_flux_minimum = Column(Float);
    tfva_flux_maximum = Column(Float);
    tsampling_flux_average = Column(Float);
    tsampling_flux_var = Column(Float);
    dG_r_units = Column(Float);
    tfba_dG_r = Column(Float);
    tfva_dG_r_lb = Column(Float);
    tfva_dG_r_ub = Column(Float);
    tsampling_dG_r_average = Column(Float);
    tsampling_dG_r_var = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I):
        self.experiment_id=experiment_id_I

    def __repr__dict__(self):
        return {}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage03_quantification_tfbaMetabolites(Base):
    __tablename__ = 'data_stage03_quantification_tfbaMetabolites'
    id = Column(Integer, Sequence('data_stage03_quantification_tfbaMetabolites_id_seq'), primary_key=True)
    experiment_id = Column(String(100), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    met_id = Column(String(100), primary_key=True)
    concentration_units = Column(String(50));
    tfba_concentration_lb = Column(Float);
    tfva_concentration_lb = Column(Float);
    tfva_concentration_ub = Column(Float);
    tsampling_concentration_average = Column(Float);
    tsampling_concentration_var = Column(Float);
    dG_f_units = Column(Float);
    tfba_dG_f = Column(Float);
    tfva_dG_f_lb = Column(Float);
    tfva_dG_f_ub = Column(Float);
    tsampling_dG_f_average = Column(Float);
    tsampling_dG_f_var = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I):
        self.experiment_id = experiment_id_I;

    def __repr__dict__(self): 
        return {}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())