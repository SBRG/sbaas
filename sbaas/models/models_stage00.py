from models_base import *
from sqlalchemy.orm import relationship
import datetime

#Base models:
#Experimentor
#experimentor_id2name
class experimentor_id2name(Base):
    #__table__ = make_table('experimentor_id2name')
    __tablename__ = 'experimentor_id2name'
    experimentor_id = Column(String(50), nullable = False);
    experimentor_name = Column(String(100), nullable = False);
    experimentor_role = Column(String(500), nullable = False)

    __table_args__ = (ForeignKeyConstraint(['experimentor_id'],['experimentor_list.experimentor_id'], onupdate="CASCADE"),
                ForeignKeyConstraint(['experimentor_name'],['experimentor.experimentor_name']),
                PrimaryKeyConstraint('experimentor_id','experimentor_name','experimentor_role'),
            )

    def __repr__(self):
        return "experimentor_id2name: %s, %s, %s" % (self.experimentor_id,self.experimentor_name,self.experimentor_role)

    def __repr__dict__(self):
        return {"experimentor_id":self.experimentor_id,"experimentor_name":self.experimentor_name,"experimentor_role":self.experimentor_role}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#experimentor
class experimentor(Base):
    #__table__ = make_table('experimentor')
    __tablename__ = 'experimentor'
    experimentor_name = Column(String(100), nullable = False);
    contact_information = Column(String(100))
    __table_args__ = (PrimaryKeyConstraint('experimentor_name'),
            )

    #define relations
    experimentor_id2name = relationship(experimentor_id2name);

    def __repr__(self):
        return "experimentor: %s, %s" % (self.experimentor_name,self.contact_information)

    #TODO:
    #JSON representation
    def __repr__dict__(self):
        return {"experimentor_name":self.experimentor_name,"contact_information":self.contact_information}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#experimentor_list
class experimentor_list(Base):
    #__table__ = make_table('experimentor_list')
    __tablename__ = 'experimentor_list'
    experimentor_id = Column(String(50), nullable = False)

    __table_args__ = (PrimaryKeyConstraint('experimentor_id'),
            )
    #define relations
    experimentor_id2name = relationship(experimentor_id2name);

    def __repr__(self):
        return "experimentor_list: %s" % (self.experimentor_id)

    #TODO:
    #JSON representation
    def __repr__dict__(self):
        return {"experimentor_list":self.experimentor_id}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#Extraction Method
#extraction_method
class extraction_method(Base):
    #__table__ = make_table('extraction_method')
    __tablename__ = 'extraction_method'
    id = Column(String(500), nullable = False);
    extraction_method_reference = Column(String(100), nullable = False);
    notes = Column(Text)
    
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "extraction_method: %s" % (self.id)

    #JSON representation
    def __repr__dict__(self):
        return {"id":self.id,"extraction_method_reference":self.extraction_method_reference,"notes":self.notes}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#Standards
#standards
class standards(Base):
    #__table__ = make_table('standards')
    
    __tablename__ = 'standards'
    met_id = Column(String(50), nullable = False);
    met_name = Column(String(500), nullable = False);
    formula = Column(String(100));
    hmdb = Column(String(500));
    solubility = Column(Float);
    solubility_units = Column(String(10));
    mass = Column(Float);
    cas_number = Column(String(100));
    keggid = Column(String(100));
    structure_file = Column(Text);
    structure_file_extention = Column(String(10));
    exactmass = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('met_id'),
            )

    def __init__(self,met_id_I,met_name_I,formula_I,hmdb_I,
                solubility_I,solubility_units_I,mass_I,cas_number_I,
                keggid_I,structure_file_I,structure_file_extention_I,
                exactmass_I):
        self.met_id=met_id_I
        self.met_name=met_name_I
        self.formula=formula_I
        self.hmdb=hmdb_I
        self.solubility=solubility_I
        self.solubility_units=solubility_units_I
        self.mass=mass_I
        self.cas_number=cas_number_I
        self.keggid=keggid_I
        self.structure_file=structure_file_I
        self.structure_file_extention=structure_file_extention_I
        self.exactmass=exactmass_I

    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "standards: %s" % (self.met_id)

    #JSON representation
    def __repr__dict__(self):
        return {"met_id":self.met_id}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#standards_ordering
class standards_ordering(Base):
    #__table__ = make_table('standards_ordering')
    __tablename__ = 'standards_ordering'
    met_id = Column(String(50), nullable = False);
    met_name = Column(String(100), nullable = False);
    hillcrest = Column(Boolean);
    provider = Column(String(100), nullable = False);
    provider_reference = Column(String(100), nullable = False);
    price = Column(Float);
    amount = Column(Float);
    amount_units = Column(String(10));
    purity = Column(Float);
    mw = Column(Float);
    notes = Column(String(500));
    powderdate_received= Column(Date);
    powderdate_opened= Column(Date);
    order_standard = Column(Boolean);
    standards_storage = Column(Float);
    purchase = Column(Boolean)
    __table_args__ = (PrimaryKeyConstraint('met_id','provider','provider_reference'),
            )

    def __init__(self,met_id_I,met_name_I,hillcrest_I,
                 provider_I,provider_reference_I,price_I,
                 amount_I,amount_units_I,purity_I,mw_I,
                 notes_I,powderdate_received_I,
                 powderdate_opened_I,order_standard_I,
                 standards_storage_I,purchase_I):
        self.met_id=met_id_I
        self.met_name=met_name_I
        self.hillcrest=hillcrest_I
        self.provider=provider_I
        self.provider_reference=provider_reference_I
        self.price=price_I
        self.amount=amount_I
        self.amount_units=amount_units_I
        self.purity=purity_I
        self.mw=mw_I
        self.notes=notes_I
        self.powderdate_received=powderdate_received_I
        self.powderdate_opened=powderdate_opened_I
        self.order_standard=order_standard_I
        self.standards_storage=standards_storage_I
        self.purchase=purchase_I

    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "standards_ordering: %s" % (self.met_id)

    #JSON representation
    def __repr__dict__(self):
        return {"met_id":self.met_id}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#standards2material
class standards2material(Base):
    __tablename__ = 'standards2material'
    met_id = Column(String(50), nullable = False);
    provider = Column(String(100), nullable = False);
    provider_reference = Column(String(100), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('met_id','provider','provider_reference'),
                      ForeignKeyConstraint(['met_id'],['standards.met_id']),
                      ForeignKeyConstraint(['met_id','provider','provider_reference'],['standards_ordering.met_id','standards_ordering.provider','standards_ordering.provider_reference']),
            )
#standards_storage
class standards_storage(Base):
    __tablename__ = 'standards_storage'
    met_id = Column(String(50), nullable = False);
    met_name = Column(String(500), nullable = False);
    provider = Column(String(100), nullable = False);
    provider_reference = Column(String(50), nullable = False);
    powderdate= Column(Date);
    stockdate= Column(Date, nullable = False);
    concentration = Column(Float);
    concentration_units = Column(String(10));
    aliquots = Column(Integer);
    solvent = Column(String(100));
    ph = Column(Float);
    box = Column(Integer);
    posstart = Column(Integer);
    posend = Column(Integer)
    __table_args__ = (UniqueConstraint('met_id','stockdate'),
            PrimaryKeyConstraint('met_id','provider','provider_reference','stockdate'),
            ForeignKeyConstraint(['met_id','provider','provider_reference'],['standards2material.met_id','standards2material.provider','standards2material.provider_reference']),
            )
 
#Calibrators and mixes
#mix_storage
class mix_storage(Base):
    __tablename__ = 'mix_storage'
    mix_id = Column(String(25), nullable = False);
    mixdate= Column(Date);
    box = Column(postgresql.ARRAY(Integer));
    posstart = Column(postgresql.ARRAY(Integer));
    posend = Column(postgresql.ARRAY(Integer))
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            )
#mix_description
class mix_description(Base):
    __tablename__ = 'mix_description'
    mix_id = Column(String(25), nullable = False);
    mix_description = Column(Text, nullable = False)
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            )
#mix_parameters
class mix_parameters(Base):
    __tablename__ = 'mix_parameters'
    mix_id = Column(String(25), nullable = False);
    number_of_aliquots = Column(Float, nullable = False);
    mix_volume = Column(Float, nullable = False);
    number_of_aliquiots = Column(Integer, nullable = False)
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            )
#calibrator_met_parameters
class calibrator_met_parameters(Base):
    __tablename__ = 'calibrator_met_parameters'
    met_id = Column(String(50), nullable = False);
    dilution = Column(Integer, nullable = False)
    __table_args__ = (PrimaryKeyConstraint('met_id'),
            )
#calibrator2mix
class calibrator2mix(Base):
    #__table__ = make_table('calibrator2mix')
    __tablename__ = 'calibrator2mix'
    calibrator_id = Column(Integer, nullable = False);
    mix_id = Column(String(25), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            )

    def __init__(self,calibrator_id_I,mix_id_I):
        self.calibrator_id=calibrator_id_I
        self.mix_id=mix_id_I
#mix2met_ID
class mix2met_id(Base):
    #__table__ = make_table('mix2met_id')
    __tablename__ = 'mix2met_id'
    mix_id = Column(String(25), nullable = False);
    met_id = Column(String(50), nullable = False);
    met_name = Column(String(500), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('met_id','mix_id'),
            ForeignKeyConstraint(['mix_id'],['mix_storage.mix_id']),
            ForeignKeyConstraint(['mix_id'],['calibrator2mix.mix_id']),
            ForeignKeyConstraint(['mix_id'],['mix_description.mix_id']),
            )
    
    def __init__(self,mix_id_I,met_id_I,met_name_I):
        self.mix_id=mix_id_I
        self.met_id=met_id_I
        self.met_name=met_name_I
#calibrator
class calibrator(Base):
    __tablename__ = 'calibrator'
    met_id = Column(String(50), nullable = False);
    lloq = Column(Float);
    uloq = Column(Float);
    uloq_working = Column(Float);
    concentration_units = Column(String(25));
    stockdate= Column(Date)
    __table_args__ = (UniqueConstraint('met_id','stockdate'),
            PrimaryKeyConstraint('met_id'),
            ForeignKeyConstraint(['met_id','stockdate'],['standards_storage.met_id','standards_storage.stockdate']),
            )
#calibrator_concentrations
class calibrator_concentrations(Base):
    #__table__ = make_table('calibrator_concentrations')
    __tablename__ = 'calibrator_concentrations'
    met_id = Column(String(50), nullable = False);
    calibrator_level = Column(Integer, nullable = False);
    dilution_factor = Column(Float);
    calibrator_concentration = Column(Float);
    concentration_units = Column(String(25))
    __table_args__ = (PrimaryKeyConstraint('met_id','calibrator_level'),
            )

    def __init__(self,met_id_I,calibrator_level_I,dilution_factor_I,
                 calibrator_concentration_I,concentration_units_I):
        self.met_id=met_id_I
        self.calibrator_level=calibrator_level_I
        self.dilution_factor=dilution_factor_I
        self.calibrator_concentration=calibrator_concentration_I
        self.concentration_units=concentration_units_I

#calibrator_calculations
class calibrator_calculations(Base):
    __tablename__ = 'calibrator_calculations'
    met_id = Column(String(50), nullable = False);
    calcstart_concentration = Column(Float);
    start_concentration = Column(Float)
    
    __table_args__ = (PrimaryKeyConstraint('met_id'),
            ForeignKeyConstraint(['met_id'],['calibrator.met_id']),
            )
#calibrator_met2mix_calculations
class calibrator_met2mix_calculations(Base):
    __tablename__ = 'calibrator_met2mix_calculations'
    met_id = Column(String(50), nullable = False);
    mix_id = Column(String(25), nullable = False);
    working_concentration = Column(Float);
    total_volume = Column(Float);
    add_volume = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('met_id'),
            ForeignKeyConstraint(['met_id'],['calibrator_met_parameters.met_id']),
            ForeignKeyConstraint(['met_id'],['calibrator_calculations.met_id']),
            ForeignKeyConstraint(['mix_id'],['mix_calculations.mix_id']),
            ForeignKeyConstraint(['mix_id'],['mix_parameters.mix_id']),
            )
#mix_calculations
class mix_calculations(Base):
    __tablename__ = 'mix_calculations'
    mix_id = Column(String(25), nullable = False);
    number_of_compounds = Column(Integer);
    total_volume_actual = Column(Float);
    aliquot_volume = Column(Float);
    add_to_make_aliquot_volume_even = Column(Float);
    corrected_aliquot_volume = Column(Float);
    volume_units = Column(String(25))
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            ForeignKeyConstraint(['mix_id'],['mix_parameters.mix_id']),
            )
#calibrator_levels
class calibrator_levels(Base):
    __tablename__ = 'calibrator_levels'
    calibrator_level = Column(Integer, nullable = False);
    dilution = Column(Float, nullable = False);
    injectionvolume = Column(Float);
    workingvolume = Column(Float);
    dilution_factor_from_the_previous_level = Column(Float);
    amount_from_previous_level = Column(Float);
    balance_h2o = Column(Float);
    dilution_concentration = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('calibrator_level'),
            )
#MS_components
class MS_components(Base):
    #__table__ = make_table('ms_components')
    __tablename__ = 'ms_components'
    id = Column(Integer, Sequence('ms_components_id_seq'))
    q1_mass = Column(Float, nullable = False);
    q3_mass = Column(Float, nullable = False);
    ms3_mass = Column(Float);
    met_name = Column(Text);
    dp = Column(Float);
    ep = Column(Float);
    ce = Column(Float);
    cxp = Column(Float);
    af = Column(Float);
    quantifier = Column(Integer);
    ms_mode = Column(String(1));
    ion_intensity_rank = Column(Integer);
    ion_abundance = Column(Float);
    precursor_formula = Column(Text);
    product_ion_reference = Column(Text);
    product_formula = Column(Text);
    production_ion_notes = Column(Text);
    met_id = Column(String(50), nullable = False);
    external_reference = Column(Text);
    q1_mass_units = Column(String(20));
    q3_mass_units = Column(String(20));
    ms3_mass_units = Column(String(20));
    threshold_units = Column(String(20));
    dp_units = Column(String(20));
    ep_units = Column(String(20));
    ce_units = Column(String(20));
    cxp_units = Column(String(20));
    af_units = Column(String(20));
    ms_group = Column(String(100));
    threshold = Column(Float, default = 5000)
    dwell_weight = Column(Float, default = 1)
    component_name = Column(String(500));
    ms_include = Column(Boolean, default = False);
    ms_is = Column(Boolean, default = False);
    precursor_fragment = Column(postgresql.ARRAY(Boolean))
    product_fragment = Column(postgresql.ARRAY(Boolean))
    precursor_exactmass = Column(Float);
    product_exactmass = Column(Float);
    ms_methodtype = Column(String(20), default = 'tuning')
    precursor_fragment_elements = Column(postgresql.ARRAY(String(3)))
    product_fragment_elements = Column(postgresql.ARRAY(String(3)))

    __table_args__ = (UniqueConstraint('component_name','ms_include'),
                      PrimaryKeyConstraint('met_id','q1_mass','q3_mass','ms_methodtype'),
            )
    def __init__(self,q1_mass_I,q3_mass_I,ms3_mass_I,
                 met_name_I,dp_I,ep_I,ce_I,cxp_I,af_I,
                 quantifier_I,ms_mode_I,ion_intensity_rank_I,
                 ion_abundance_I,precursor_formula_I,
                 product_ion_reference_I,product_formula_I,
                 production_ion_notes_I,met_id_I,external_reference_I,
                 q1_mass_units_I,q3_mass_units_I,ms3_mass_units_I,
                 threshold_units_I,dp_units_I,ep_units_I,ce_units_I,
                 cxp_units_I,af_units_I,ms_group_I,threshold_I,
                 dwell_weight_I,component_name_I,ms_include_I,
                 ms_is_I,precursor_fragment_I,product_fragment_I,
                 precursor_exactmass_I,product_exactmass_I,
                 ms_methodtype_I,
                 precursor_fragment_elements_I,
                 product_fragment_elements_I):
        self.q1_mass=q1_mass_I
        self.q3_mass=q3_mass_I
        self.ms3_mass=ms3_mass_I
        self.met_name=met_name_I
        self.dp=dp_I
        self.ep=ep_I
        self.ce=ce_I
        self.cxp=cxp_I
        self.af=af_I
        self.quantifier=quantifier_I
        self.ms_mode=ms_mode_I
        self.ion_intensity_rank=ion_intensity_rank_I
        self.ion_abundance=ion_abundance_I
        self.precursor_formula=precursor_formula_I
        self.product_ion_reference=product_ion_reference_I
        self.product_formula=product_formula_I
        self.production_ion_notes=production_ion_notes_I
        self.met_id=met_id_I
        self.external_reference=external_reference_I
        self.q1_mass_units=q1_mass_units_I
        self.q3_mass_units=q3_mass_units_I
        self.ms3_mass_units=ms3_mass_units_I
        self.threshold_units=threshold_units_I
        self.dp_units=dp_units_I
        self.ep_units=ep_units_I
        self.ce_units=ce_units_I
        self.cxp_units=cxp_units_I
        self.af_units=af_units_I
        self.ms_group=ms_group_I
        self.threshold=threshold_I
        self.dwell_weight=dwell_weight_I
        self.component_name=component_name_I
        self.ms_include=ms_include_I
        self.ms_is=ms_is_I
        self.precursor_fragment=precursor_fragment_I
        self.product_fragment=product_fragment_I
        self.precursor_exactmass = precursor_exactmass_I
        self.product_exactmass = product_exactmass_I
        self.ms_methodtype = ms_methodtype_I
        self.precursor_fragment_elements = precursor_fragment_elements_I
        self.product_fragment_elements = product_fragment_elements_I
#MS_sourceParameters
class MS_sourceParameters(Base):
    #__table__ = make_table('ms_sourceParameters')
    __tablename__ = 'ms_sourceparameters'
    id = Column(String(50), nullable = False);
    ms_cur = Column(Float, nullable = False);
    ms_cad = Column(String(10), nullable = False)
    ms_is = Column(Float, nullable = False);
    ms_tem = Column(Float, nullable = False);
    ms_gs1 = Column(Float, nullable = False);
    ms_gs2 = Column(Float, nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
#MS_information
class MS_information(Base):
    #__table__ = make_table('ms_information')
    __tablename__ = 'ms_information'
    manufacturer = Column(String(100), nullable = False);
    id = Column(String(100), nullable = False);
    serial_number = Column(String(100), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
#MS_method
class MS_method(Base):
    #__table__ = make_table('ms_method')
    __tablename__ = 'ms_method'
    id = Column(String(50), nullable = False);
    ms_sourceparameters_id = Column(String(50), nullable = False);
    ms_information_id = Column(String(50), nullable = False);
    ms_experiment_id = Column(String(50))
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['ms_information_id'],['ms_information.id'], onupdate="CASCADE", ondelete="CASCADE"),
            ForeignKeyConstraint(['ms_sourceparameters_id'],['ms_sourceparameters.id'], onupdate="CASCADE", ondelete="CASCADE"),
            )

    def __init__(self,id_I, ms_sourceparameters_id_I,ms_information_id_I,ms_experiment_id_I):
        self.id = id_I;
        self.ms_sourceparameters_id = ms_sourceparameters_id_I;
        self.ms_information_id = ms_information_id_I;
        self.ms_experiment_id = ms_experiment_id_I;
#MS_component_list
class MS_component_list(Base):
    #__table__ = make_table('ms_component_list')
    __tablename__ = 'ms_component_list'
    ms_method_id = Column(String(50), nullable = False);
    q1_mass = Column(Float);
    q3_mass = Column(Float);
    met_id = Column(String(50));
    component_name = Column(String(500), nullable = False);
    ms_methodtype = Column(String(20), default = 'quantification')
    __table_args__ = (PrimaryKeyConstraint('ms_method_id','component_name'),
            ForeignKeyConstraint(['ms_method_id'],['ms_method.id'], onupdate="CASCADE"),
            )
    
    def __init__(self,ms_method_id_I,q1_mass_I,q3_mass_I,
                 met_id_I,component_name_I,ms_methodtype_I):
        self.ms_method_id=ms_method_id_I
        self.q1_mass=q1_mass_I
        self.q3_mass=q3_mass_I
        self.met_id=met_id_I
        self.component_name=component_name_I
        self.ms_methodtype=ms_methodtype_I

#Autosampler_parameters
class autosampler_parameters(Base):
    __tablename__ = 'autosampler_parameters'
    id = Column(String(50), nullable = False);
    injvolume_ul = Column(Float);
    washsolvent1 = Column(String(500));
    washsolvent2 = Column(String(500))
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
#Autosampler_information
class autosampler_information(Base):
    __tablename__ = 'autosampler_information'
    manufacturer = Column(String(100), nullable = False);
    id = Column(String(100), nullable = False);
    serial_number = Column(String(100), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
#Autosampler_method
class autosampler_method(Base):
    __tablename__ = 'autosampler_method'
    id = Column(String(50), nullable = False);
    autosampler_parameters_id = Column(String(50), nullable = False);
    autosampler_information_id = Column(String(50), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['id'],['autosampler_method.id'], onupdate="CASCADE"),
            ForeignKeyConstraint(['autosampler_information_id'],['autosampler_information.id'], onupdate="CASCADE"),
            ForeignKeyConstraint(['autosampler_parameters_id'],['autosampler_parameters.id'], onupdate="CASCADE"),
            )

#LC_information
class lc_information(Base):
    __tablename__ = 'lc_information'
    manufacturer = Column(String(100), nullable = False);
    id = Column(String(100), nullable = False);
    serial_number = Column(String(100), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
#LC_gradient
class lc_gradient(Base):
    __tablename__ = 'lc_gradient'
    id = Column(String(50), nullable = False);
    lc_event = Column(postgresql.ARRAY(Integer), nullable = False);
    lc_time = Column(postgresql.ARRAY(Float), nullable = False);
    percent_b = Column(postgresql.ARRAY(Float), nullable = False);
    flow_rate = Column(postgresql.ARRAY(Float), nullable = False);
    lc_time_units = Column(String(25), nullable = False);
    flow_rate_units = Column(String(25), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['id'],['lc_gradient.id'], onupdate="CASCADE"),
            )
#LC_parameters
class lc_parameters(Base):
    __tablename__ = 'lc_parameters'
    id = Column(String(50), nullable = False);
    column_name = Column(String(100), nullable = False);
    dimensions_and_particle_size = Column(String(100), nullable = False);
    mobile_phase_a = Column(String(100), nullable = False);
    mobile_phase_b = Column(String(100), nullable = False);
    oven_temperature = Column(String(100), nullable = False);
    notes = Column(Text)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
#LC_method
class lc_method(Base):
    __tablename__ = 'lc_method'
    id = Column(String(50), nullable = False);
    lc_information_id = Column(String(100), nullable = False);
    lc_gradient_id = Column(String(50), nullable = False);
    lc_parameters_id = Column(String(50), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['lc_information_id'],['lc_information.id'], onupdate="CASCADE"),
            ForeignKeyConstraint(['lc_parameters_id'],['lc_parameters.id'], onupdate="CASCADE"),
            )
#LC_elution
class lc_elution(Base):
    __tablename__ = 'lc_elution'
    id=Column(String(length=50), nullable = False, primary_key=True)
    met_id=Column(String(length=50), nullable = False)
    rt=Column(Float, default = 0.0)
    ms_window=Column(Float, default = 60.0)
    rt_units=Column(String(length=20))
    window_units=Column(String(length=20))
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['id'],['lc_method.id'], onupdate="CASCADE"),
            )
    
#acquisition_method
class acquisition_method(Base):
    #__table__ = make_table('acquisition_method')
    __tablename__ = 'acquisition_method'
    id = Column(String(50), nullable = False);
    ms_method_id = Column(String(50));
    autosampler_method_id = Column(String(50));
    lc_method_id = Column(String(50))
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['lc_method_id'],['lc_method.id'], onupdate="CASCADE"),
            ForeignKeyConstraint(['ms_method_id'],['ms_method.id'], onupdate="CASCADE"),
            )

    def __init__(self,id_I, ms_method_id_I,autosampler_method_id_I,lc_method_id_I):
        self.id = id_I;
        self.ms_method_id = ms_method_id_I;
        self.autosampler_method_id = autosampler_method_id_I;
        self.lc_method_id = lc_method_id_I;

#quantitation_method
class quantitation_method(Base):
    #__table__ = make_table('quantitation_method')
    __tablename__ = 'quantitation_method'
    id = Column(String(50), nullable = False);
    q1_mass = Column(Float);
    q3_mass = Column(Float);
    met_id = Column(String(50));
    component_name = Column(String(100), nullable = False);
    is_name = Column(String(100))
    fit = Column(String(20));
    weighting = Column(String(20));
    intercept = Column(Float);
    slope = Column(Float);
    correlation = Column(Float);
    use_area = Column(Boolean, default = False)
    lloq = Column(Float);
    uloq = Column(Float);
    points = Column(Integer)
    __table_args__ = (PrimaryKeyConstraint('id','component_name'),
            ForeignKeyConstraint(['id'],['quantitation_method_list.quantitation_method_id'], ondelete="CASCADE"),
            )

    def __init__(self,id_I, q1_mass_I,q3_mass_I,met_id_I,component_name_I,is_name_I,fit_I,
                 weighting_I,intercept_I,slope_I,correlation_I,use_area_I,lloq_I,uloq_I,
                 points_I):
        self.id = id_I;
        self.q1_mass = q1_mass_I;
        self.q3_mass = q3_mass_I;
        self.met_id = met_id_I;
        self.component_name = component_name_I;
        self.is_name = is_name_I;
        self.fit = fit_I;
        self.weighting = weighting_I;
        self.intercept = intercept_I;
        self.slope = slope_I;
        self.correlation = correlation_I;
        self.use_area = use_area_I;
        self.lloq = lloq_I;
        self.uloq = uloq_I;
        self.points = points_I;
#quantitation_method_list
class quantitation_method_list(Base):
    #__table__ = make_table('quantitation_method_list')
    __tablename__ = 'quantitation_method_list'
    quantitation_method_id = Column(String(50), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('quantitation_method_id'),
            )

#Samples
#sample
class sample(Base):
    #__table__ = make_table('sample')
    __tablename__ = 'sample'
    sample_name = Column(String(500), nullable = False);
    sample_type = Column(String(100), nullable = False);
    calibrator_id = Column(Integer);
    calibrator_level = Column(Integer);
    sample_id = Column(String(500));
    sample_dilution = Column(Float, default = 1.0)
    
    __table_args__ = (PrimaryKeyConstraint('sample_name'),
            ForeignKeyConstraint(['sample_id'],['sample_storage.sample_id']),
            ForeignKeyConstraint(['sample_id'],['sample_physiologicalparameters.sample_id']),
            ForeignKeyConstraint(['sample_id'],['sample_description.sample_id']),
            )

    def __init__(self,sample_name_I,sample_type_I,calibrator_id_I,calibrator_level_I,sample_id_I,sample_dilution_I):
        self.sample_name=sample_name_I;
        self.sample_type=sample_type_I;
        self.calibrator_id=calibrator_id_I;
        self.calibrator_level=calibrator_level_I;
        self.sample_id=sample_id_I;
        self.sample_dilution=sample_dilution_I;
#sample_storage
class sample_storage(Base):
    #__table__ = make_table('sample_storage')
    __tablename__ = 'sample_storage'
    sample_id=Column(String(500),nullable=False, primary_key=True)
    sample_label=Column(String(50), nullable = False)
    #sample_dateAndTime=Column(DateTime)
    ph=Column(Float)
    box=Column(Integer)
    pos=Column(Integer)

    def __init__(self,sample_id_I,
                 #sample_dateAndTime_I,
                 sample_label_I,ph_I,box_I,pos_I):
        self.sample_id = sample_id_I
        self.sample_label = sample_label_I
        #self.sample_dateAndTime = sample_dateAndTime_I
        self.ph = ph_I
        self.box = box_I
        self.pos = pos_I
#sample_physiologicalParameters
class sample_physiologicalParameters(Base):
    #__table__ = make_table('sample_physiologicalparameters')
    __tablename__ = 'sample_physiologicalparameters'
    sample_id=Column(String(500),nullable=False, primary_key=True)
    growth_condition_short=Column(Text)
    growth_condition_long=Column(Text)
    media_short=Column(Text)
    media_long=Column(Text)
    isoxic=Column(Boolean)
    temperature=Column(Float)
    supplementation=Column(String(100))
    od600=Column(Float)
    vcd=Column(Float)
    culture_density=Column(Float)
    culture_volume_sampled=Column(Float)
    cells=Column(Float)
    dcw=Column(Float)
    wcw=Column(Float)
    vcd_units=Column(String(10))
    culture_density_units=Column(String(10))
    culture_volume_sampled_units=Column(String(10))
    dcw_units=Column(String(10))
    wcw_units=Column(String(10))

    def __init__(self,sample_id_I,growth_condition_short_I,growth_condition_long_I,
                media_short_I,media_long_I,isoxic_I,temperature_I,supplementation_I,od600_I,
                vcd_I,culture_density_I,culture_volume_sampled_I,cells_I,dcw_I,wcw_I,vcd_units_I,
                culture_density_units_I,culture_volume_sampled_units_I,dcw_units_I,wcw_units_I):
        self.sample_id = sample_id_I
        self.growth_condition_short = growth_condition_short_I
        self.growth_condition_long = growth_condition_long_I
        self.media_short = media_short_I
        self.media_long = media_long_I
        self.isoxic = isoxic_I
        self.temperature = temperature_I
        self.supplementation = supplementation_I
        self.od600 = od600_I
        self.vcd = vcd_I
        self.culture_density = culture_density_I
        self.culture_volume_sampled = culture_volume_sampled_I
        self.cells = cells_I
        self.dcw = dcw_I
        self.wcw = wcw_I
        self.vcd_units = vcd_units_I
        self.culture_density_units = culture_density_units_I
        self.culture_volume_sampled_units = culture_volume_sampled_units_I
        self.dcw_units = dcw_units_I
        self.wcw_units = wcw_units_I
#sample_description
class sample_description(Base):
    #__table__ = make_table('sample_description')
    __tablename__ ='sample_description'
    sample_id=Column(String(500),nullable=False, primary_key=True);
    sample_name_short=Column(String(100));
    sample_name_abbreviation=Column(String(50));
    sample_date=Column(Date,nullable=False);
    time_point=Column(String(50),nullable=False);
    sample_condition=Column(String(100),nullable=False);
    extraction_method_id=Column(String(500));
    biological_material=Column(String(100),nullable=False);
    sample_description=Column(String(100),nullable=False);
    sample_replicate=Column(Integer);
    is_added=Column(Float);
    is_added_units=Column(String(10));
    reconstitution_volume=Column(Float);
    reconstitution_volume_units=Column(String(10));
    istechnical=Column(Boolean);
    sample_replicate_biological=Column(Integer);
    notes=Column(Text);

    def __init__(self,sample_id_I,sample_name_short_I,sample_name_abbreviation_I,
                 sample_date_I,time_point_I,sample_condition_I,extraction_method_id_I,
                 biological_material_I,sample_description_I,sample_replicate_I,
                 is_added_I,is_added_units_I,reconstitution_volume_I,reconstitution_volume_units_I,
                 sample_replicate_biological_I,istechnical_I,notes_I):
        self.sample_id=sample_id_I
        self.sample_name_short=sample_name_short_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.sample_date=sample_date_I
        self.time_point=time_point_I
        self.sample_condition=sample_condition_I
        self.extraction_method_id=extraction_method_id_I
        self.biological_material=biological_material_I
        self.sample_description=sample_description_I
        self.sample_replicate=sample_replicate_I
        self.is_added=is_added_I
        self.is_added_units=is_added_units_I
        self.reconstitution_volume=reconstitution_volume_I
        self.reconstitution_volume_units=reconstitution_volume_units_I
        self.sample_replicate_biological=sample_replicate_biological_I
        self.istechnical=istechnical_I
        self.notes=notes_I
#sample_massVolumeConversion
class sample_massVolumeConversion(Base):
    #__table__ = make_table('sample_massvolumeconversion')
    __tablename__ = 'sample_massvolumeconversion'
    biological_material=Column(String(100),nullable=False, primary_key=True);
    conversion_name=Column(String(50),nullable=False, primary_key=True);
    conversion_factor=Column(Float);
    conversion_units=Column(String(50),nullable=False);
    conversion_reference=Column(String(500),nullable=False);

#IS
#internal_standard
class internal_standard(Base):
    #__table__ = make_table('internal_standard')
    __tablename__ = 'internal_standard'
    is_id = Column(Integer, nullable = False);
    is_date = Column(DateTime, nullable = False);
    experimentor_id = Column(String(50), nullable = False);
    extraction_method_id = Column(String(50))
    __table_args__ = (PrimaryKeyConstraint('is_id'),
            ForeignKeyConstraint(['is_id'],['internal_standard_storage.is_id']),
            )
#internal_standard_storage
class internal_standard_storage(Base):
    #__table__ = make_table('internal_standard_storage')
    __tablename__ = 'internal_standard_storage'
    is_id = Column(Integer, nullable = False);
    concentration = Column(Float);
    concentration_units = Column(String(10));
    aliquots = Column(Integer);
    aliquot_volume = Column(Float);
    aliquot_volume_units = Column(String(10));
    solvent = Column(String(100));
    ph = Column(Float);
    box = Column(Integer);
    posstart = Column(Integer);
    posend = Column(Integer)
    __table_args__ = (PrimaryKeyConstraint('is_id'),
            )

#experiments
#experiment_types
class experiment_types(Base):
    #__table__ = make_table('experiment_types')
    __tablename__ = 'experiment_types'
    id = Column(Integer, nullable = False);
    experiment_name = Column(String(100))
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
#experiment
class experiment(Base):
    #__table__ = make_table('experiment')
    __tablename__ = 'experiment'
    wid = Column(Integer, Sequence('wids'),nullable=False,)
    exp_type_id=Column(Integer);
    id=Column(String(50),nullable=False);
    sample_name=Column(String(500),nullable=False);
    experimentor_id=Column(String(50));
    extraction_method_id=Column(String(50));
    acquisition_method_id=Column(String(50),nullable=False);
    quantitation_method_id=Column(String(50));
    internal_standard_id=Column(Integer);
    
    __table_args__ = (
            PrimaryKeyConstraint('id','sample_name'),
            ForeignKeyConstraint(['acquisition_method_id'], ['acquisition_method.id'], onupdate="CASCADE"),
            ForeignKeyConstraint(['exp_type_id'], ['experiment_types.id'], ondelete="CASCADE"),
            ForeignKeyConstraint(['experimentor_id'], ['experimentor_list.experimentor_id']),
            ForeignKeyConstraint(['extraction_method_id'], ['extraction_method.id']),
            ForeignKeyConstraint(['internal_standard_id'], ['internal_standard.is_id']),
            ForeignKeyConstraint(['quantitation_method_id'], ['quantitation_method_list.quantitation_method_id']),
            ForeignKeyConstraint(['sample_name'], ['sample.sample_name']),
            UniqueConstraint('wid'),
            )

    def __init__(self,exp_type_id_I,id_I,sample_name_I,
                 experimentor_id_I,extraction_method_id_I,
                 acquisition_method_id_I,quantitation_method_id_I,
                 internal_standard_id_I):
        self.exp_type_id=exp_type_id_I;
        self.id=id_I;
        self.sample_name=sample_name_I;
        self.experimentor_id=experimentor_id_I;
        self.extraction_method_id=extraction_method_id_I;
        self.acquisition_method_id=acquisition_method_id_I;
        self.quantitation_method_id=quantitation_method_id_I;
        self.internal_standard_id=internal_standard_id_I;
    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "experiment: %s" % (self.id)

    #JSON representation
    def __repr__dict__(self):
        return {"id":self.id,
                "sample_name":self.sample_name,
                "experimentor_id":self.experimentor_id,
                "extraction_method_ide":self.extraction_method_id,
                "acquisition_method_id":self.acquisition_method_id,
                "quantitation_method_id":self.quantitation_method_id,
                "internal_standard_id":self.internal_standard_id}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#data_versions
class data_versions(Base):
    __tablename__ = 'data_versions'
    experiment_id = Column(String(50), nullable = False);
    sample_name = Column(String(500), nullable = False);
    component_name = Column(String(500), nullable = False);
    acquisition_date_and_time = Column(DateTime, nullable = False);
    concentration_before = Column(Float);
    concentration_after = Column(Float);
    concentration_units_before = Column(String(20));
    concentration_units_after = Column(String(20));
    used_before = Column(Boolean);
    used_after = Column(Boolean);
    data_stage_before = Column(Integer);
    data_stage_after = Column(Integer);
    data_stage_modtime = Column(DateTime, default=datetime.datetime.utcnow, nullable = False);
    __table_args__ = (PrimaryKeyConstraint('experiment_id','sample_name','component_name','data_stage_modtime'),
            ForeignKeyConstraint(['experiment_id','sample_name'],['experiment.id','experiment.sample_name']),
            ForeignKeyConstraint(['sample_name','component_name','acquisition_date_and_time'],['data_stage01_quantification_mqresultstable.sample_name','data_stage01_quantification_mqresultstable.component_name','data_stage01_quantification_mqresultstable.acquisition_date_and_time']),
            )
    #define representation
    def __repr__(self):
        return "data_versions %s" % (self.experiment_id, self.sample_name,self.component_name, self.acquisition_date_and_time)

#Biological material 
#biologicalmaterial_storage
class biologicalMaterial_storage(Base):
    __tablename__ = 'biologicalmaterial_storage'
    biologicalmaterial_id = Column(String(100), primary_key=True)
    biologicalmaterial_label = Column(String(100))
    biologicalmaterial_box = Column(Integer)
    biologicalmaterial_posstart = Column(Integer)
    biologicalmaterial_posend = Column(Integer)
    biologicalmaterial_date = Column(DateTime)

    def __init__(self,biologicalmaterial_id_I,biologicalmaterial_label_I,biologicalmaterial_box_I,
                 biologicalmaterial_posstart_I,biologicalmaterial_posend_I,biologicalmaterial_date_I):
        self.biologicalmaterial_id = biologicalmaterial_id_I
        self.biologicalmaterial_label = biologicalmaterial_label_I
        self.biologicalmaterial_box = biologicalmaterial_box_I
        self.biologicalmaterial_posstart = biologicalmaterial_posstart_I
        self.biologicalmaterial_posend = biologicalmaterial_posend_I
        self.biologicalmaterial_date = biologicalmaterial_date_I
#biologicalmaterial_description
class biologicalMaterial_description(Base):
    __tablename__ = 'biologicalmaterial_description'
    biologicalmaterial_id = Column(String(100), primary_key=True)
    biologicalmaterial_strain = Column(String(100))
    biologicalmaterial_description = Column(Text)
    biologicalmaterial_notes = Column(Text)

    def __init__(self,biologicalmaterial_id_I,biologicalmaterial_strain_I,biologicalmaterial_description_I,
                biologicalmaterial_notes_I):
        self.biologicalmaterial_id = biologicalmaterial_id_I
        self.biologicalmaterial_strain = biologicalmaterial_strain_I
        self.biologicalmaterial_description = biologicalmaterial_description_I
        self.biologicalmaterial_notes = biologicalmaterial_notes_I
#biologicalmaterial_description
class biologicalMaterial_geneReferences(Base):
    __tablename__ = 'biologicalmaterial_genereferences'
    id = Column(Integer, Sequence('biologicalmaterial_genereferences_id_seq'), primary_key=True)
    biologicalmaterial_id = Column(String(100))
    ordered_locus_name = Column(String(20))
    ordered_locus_name2 = Column(String(100))
    swissprot_entry_name = Column(String(20))
    ac = Column(String(20))
    ecogene_accession_number = Column(String(20))
    gene_name = Column(String(20))

    def __init__(self,biologicalmaterial_id_I,
                ordered_locus_name_I,
                ordered_locus_name2_I,
                swissprot_entry_name_I,
                ac_I,
                ecogene_accession_number_I,
                gene_name_I):
        self.biologicalmaterial_id=biologicalmaterial_id_I
        self.ordered_locus_name=ordered_locus_name_I
        self.ordered_locus_name2=ordered_locus_name2_I
        self.swissprot_entry_name=swissprot_entry_name_I
        self.ac=ac_I
        self.ecogene_accession_number=ecogene_accession_number_I
        self.gene_name=gene_name_I

    #TODO:
    #define relations

    def __repr__dict__(self):
        return {'biologicalmaterial_id':self.biologicalmaterial_id,
                'ordered_locus_name':self.ordered_locus_name,
                'ordered_locus_name2':self.ordered_locus_name2,
                'swissprot_entry_name':self.swissprot_entry_name,
                'ac':self.ac,
                'ecogene_accession_number':self.ecogene_accession_number,
                'gene_name':self.gene_name}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#Oligos
#oligos_description
class oligos_description(Base):
    __tablename__ = 'oligos_description'
    oligos_id = Column(String(100), primary_key=True)
    oligos_sequence = Column(Text)
    oligos_purification = Column(String(100))
    oligos_description = Column(Text)
    oligos_notes = Column(Text)

    def __init__(self,oligos_id_I,oligos_sequence_I,
                 oligos_purification_I,oligos_description_I,
                 oligos_notes_I):
        self.oligos_id = oligos_id_I
        self.oligos_sequence = oligos_sequence_I
        self.oligos_purification = oligos_purification_I
        self.oligos_description = oligos_description_I
        self.oligos_notes = oligos_notes_I
#oligos_storage
class oligos_storage(Base):
    __tablename__ = 'oligos_storage'
    oligos_id = Column(String(100), primary_key=True)
    oligos_label = Column(String(100))
    oligos_box = Column(Integer)
    oligos_posstart = Column(Integer)
    oligos_posend = Column(Integer)
    oligos_date = Column(DateTime)
    oligos_storagebuffer = Column(String(100))
    oligos_concentration = Column(Float)
    oligos_concentration_units = Column(String(20))

    def __init__(self,oligos_id_I,oligos_label_I,oligos_box_I,
                 oligos_posstart_I,oligos_posend_I,oligos_date_I,
                 oligos_storagebuffer_I,oligos_concentration_I,
                 oligos_concentration_units_I):
        self.oligos_id = oligos_id_I
        self.oligos_label = oligos_label_I
        self.oligos_box = oligos_box_I
        self.oligos_posstart = oligos_posstart_I
        self.oligos_posend = oligos_posend_I
        self.oligos_date = oligos_date_I
        self.oligos_storagebuffer = oligos_storagebuffer_I
        self.oligos_concentration = oligos_concentration_I
        self.oligos_concentration_units = oligos_concentration_units_I

# Models
# models_lumpedRxns
class models_lumpedRxns(Base):
    __tablename__ = 'lumpedRxns'
    lumped_id = Column(String(100), primary_key=True)
    lumped_date = Column(DateTime)
    lumped_description = Column(String(500))
    rxn_id = Column(String(100))
    reactions = Column(postgresql.ARRAY(String(100))) # rxn_id
    stoichiometry = Column(postgresql.ARRAY(Float))

    def __init__(self,lumped_id_I,lumped_date_I,lumped_description_I,rxn_id_I,reactions_I,stoichiometry_I):
        self.lumped_id=lumped_id_I
        self.lumped_date=lumped_date_I
        self.lumped_description=lumped_description_I
        self.rxn_id=rxn_id_I
        self.reactions=reactions_I
        self.stoichiometry=stoichiometry_I

