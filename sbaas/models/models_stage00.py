from models_base import *
from sqlalchemy.orm import relationship

#Base models:
#Experimentor
#experimentor_id2name
class experimentor_id2name(Base):
    __table__ = make_table('experimentor_id2name')

    def __repr__(self):
        return "experimentor_id2name: %s, %s, %s" % (self.experimentor_id,self.experimentor_name,self.experimentor_role)

    def __repr__dict__(self):
        return {"experimentor_id":self.experimentor_id,"experimentor_name":self.experimentor_name,"experimentor_role":self.experimentor_role}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#experimentor
class experimentor(Base):
    __table__ = make_table('experimentor')
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
    __table__ = make_table('experimentor_list')
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
    __table__ = make_table('extraction_method')
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
    __table__ = make_table('standards')

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
    __table__ = make_table('standards_ordering')

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
#standards_storage
 
#Calibrators and mixes
#mix_storage
#mix_description
#mix_parameters
#calibrator_met_parameters
#calibrator2mix
class calibrator2mix(Base):
    #__table__ = make_table('calibrator2mix')
    __tablename__ = 'calibrator2mix'
    calibrator_id = Column(Integer)
    mix_id = Column(String(25), primary_key=True)

    def __init__(self,calibrator_id_I,mix_id_I):
        self.calibrator_id=calibrator_id_I
        self.mix_id=mix_id_I
#mix2met_ID
class mix2met_id(Base):
    #__table__ = make_table('mix2met_id')
    __tablename__ = 'mix2met_id'
    mix_id = Column(String(25), primary_key=True)
    met_id = Column(String(50), primary_key=True)
    met_name = Column(String(500))

    def __init__(self,mix_id_I,met_id_I,met_name_I):
        self.mix_id=mix_id_I
        self.met_id=met_id_I
        self.met_name=met_name_I
#calibrator
#calibrator_concentrations
class calibrator_concentrations(Base):
    #__table__ = make_table('calibrator_concentrations')
    __tablename__ = 'calibrator_concentrations'
    met_id = Column(String(50), primary_key=True)
    calibrator_level = Column(Integer, primary_key=True)
    dilution_factor = Column(Float)
    calibrator_concentration = Column(Float)
    concentration_units = Column(String(25))

    def __init__(self,met_id_I,calibrator_level_I,dilution_factor_I,
                 calibrator_concentration_I,concentration_units_I):
        self.met_id=met_id_I
        self.calibrator_level=calibrator_level_I
        self.dilution_factor=dilution_factor_I
        self.calibrator_concentration=calibrator_concentration_I
        self.concentration_units=concentration_units_I

#calibrator_calculations
#calibrator_met2mix_calculations
#mix_calculations
#calibrator_levels

#Batch
#MS_components
class MS_components(Base):
    #__table__ = make_table('ms_components')
    __tablename__ = 'ms_components'
    id = Column(Integer, Sequence('ms_components_id_seq'))
    q1_mass = Column(Float, primary_key=True)
    q3_mass = Column(Float, primary_key=True)
    ms3_mass = Column(Float)
    met_name = Column(Text)
    dp = Column(Float)
    ep = Column(Float)
    ce = Column(Float)
    cxp = Column(Float)
    af = Column(Float)
    quantifier = Column(Integer)
    ms_mode = Column(String(1))
    ion_intensity_rank = Column(Integer)
    ion_abundance = Column(Float)
    precursor_formula = Column(Text)
    product_ion_reference = Column(Text)
    product_formula = Column(Text)
    production_ion_notes = Column(Text)
    met_id = Column(String(50), primary_key=True)
    external_reference = Column(Text)
    q1_mass_units = Column(String(20))
    q3_mass_units = Column(String(20))
    ms3_mass_units = Column(String(20))
    threshold_units = Column(String(20))
    dp_units = Column(String(20))
    ep_units = Column(String(20))
    ce_units = Column(String(20))
    cxp_units = Column(String(20))
    af_units = Column(String(20))
    ms_group = Column(String(100))
    threshold = Column(Float, default = 5000)
    dwell_weight = Column(Float, default = 1.0)
    component_name = Column(String(500),unique=True)
    ms_include = Column(Boolean, default = False)
    ms_is = Column(Boolean, default = False)
    precursor_fragment = Column(postgresql.ARRAY(Boolean))
    product_fragment = Column(postgresql.ARRAY(Boolean))
    precursor_exactmass = Column(Float)
    product_exactmass = Column(Float)
    ms_methodtype = Column(String(20))
    precursor_fragment_elements = Column(postgresql.ARRAY(String(3)))
    product_fragment_elements = Column(postgresql.ARRAY(String(3)))

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

    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "MS_analytes %s" % ()

    #TODO:
    #JSON representation
#MS_sourceParameters
#MS_information
#MS_method
class MS_method(Base):
    __table__ = make_table('ms_method')

    def __init__(self,id_I, ms_sourceparameters_id_I,ms_information_id_I,ms_experiment_id_I):
        self.id = id_I;
        self.ms_sourceparameters_id = ms_sourceparameters_id_I;
        self.ms_information_id = ms_information_id_I;
        self.ms_experiment_id = ms_experiment_id_I;

    #TODO:
    #define representation
    #def __repr__(self):
        #return "MS_method %s" % ()

    #TODO:
    #JSON representation
#MS_component_list
class MS_component_list(Base):
    __table__ = make_table('ms_component_list')

    def __init__(self,ms_method_id_I,q1_mass_I,q3_mass_I,
                 met_id_I,component_name_I,ms_methodtype_I):
        self.ms_method_id=ms_method_id_I
        self.q1_mass=q1_mass_I
        self.q3_mass=q3_mass_I
        self.met_id=met_id_I
        self.component_name=component_name_I
        self.ms_methodtype=ms_methodtype_I
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "MS_component_list %s" % ()

    #TODO:
    #JSON representation
#Autosampler_parameters
#Autosampler_information
#Autosampler_method
#LC_information
#LC_gradient
#LC_parameters
#LC_method
#LC_elution
class lc_elution(Base):
    __tablename__ = 'lc_elution'

    lc_method_id=Column(String(length=50), nullable = False, primary_key=True)
    met_id=Column(String(length=50), nullable = False)
    rt=Column(Float, default = 0.0)
    ms_window=Column(Float, default = 60.0)
    rt_units=Column(String(length=20))
    window_units=Column(String(length=20))

    #TODO:
    #def __init__(self,lc_method_id_I):
    #    self.lc_method_id=lc_method_id_I;

    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "sample %s" % ()

    #TODO:
    #JSON representation


#acquisition_method
class acquisition_method(Base):
    __table__ = make_table('acquisition_method')

    def __init__(self,id_I, ms_method_id_I,autosampler_method_id_I,lc_method_id_I):
        self.id = id_I;
        self.ms_method_id = ms_method_id_I;
        self.autosampler_method_id = autosampler_method_id_I;
        self.lc_method_id = lc_method_id_I;

    #TODO:
    #define representation
    #def __repr__(self):
        #return "acquisition_method %s" % ()

    #TODO:
    #JSON representation

#quantitation_method
class quantitation_method(Base):
    __table__ = make_table('quantitation_method')

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

    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "quantitation_method %s" % ()

    #TODO:
    #JSON representation
#quantitation_method_list
class quantitation_method_list(Base):
    __table__ = make_table('quantitation_method_list')

    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "quantitation_method_list %s" % ()

    #TODO:
    #JSON representation

#Samples
#sample
class sample(Base):
    #__table__ = make_table('sample')
    __tablename__ = 'sample'

    sample_name=Column(String(length=500), nullable = False, primary_key=True)
    sample_type=Column(String(length=100), nullable = False)
    calibrator_id=Column(Integer)
    calibrator_level=Column(Integer)
    sample_id=Column(String(length=500))
    sample_dilution=Column(Float, default = 1.0)


    def __init__(self,sample_name_I,sample_type_I,calibrator_id_I,calibrator_level_I,sample_id_I,sample_dilution_I):
        self.sample_name=sample_name_I;
        self.sample_type=sample_type_I;
        self.calibrator_id=calibrator_id_I;
        self.calibrator_level=calibrator_level_I;
        self.sample_id=sample_id_I;
        self.sample_dilution=sample_dilution_I;

    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "sample %s" % ()

    #TODO:
    #JSON representation
#sample_storage
class sample_storage(Base):
    #__table__ = make_table('sample_storage')
    __tablename__ = 'sample_storage'
    sample_id=Column(String(500),nullable=False, primary_key=True)
    sample_label=Column(String(50))
    ph=Column(Float)
    box=Column(Integer)
    pos=Column(Integer)

    def __init__(self,sample_id_I,sample_label_I,ph_I,box_I,pos_I):
        self.sample_id = sample_id_I
        self.sample_label = sample_label_I
        self.ph = ph_I
        self.box = box_I
        self.pos = pos_I
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "sample_storage %s" % ()

    #TODO:
    #JSON representation
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
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "sample_physiologicalParameters %s" % ()

    #TODO:
    #JSON representation
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
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "sample_storage %s" % ()

    #TODO:
    #JSON representation
#sample_massVolumeConversion
class sample_massVolumeConversion(Base):
    #__table__ = make_table('sample_massvolumeconversion')
    __tablename__ = 'sample_massvolumeconversion'
    biological_material=Column(String(100),nullable=False, primary_key=True);
    conversion_name=Column(String(50),nullable=False, primary_key=True);
    conversion_factor=Column(Float);
    conversion_units=Column(String(50),nullable=False);
    conversion_reference=Column(String(500),nullable=False);
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "sample_storage %s" % ()

    #TODO:
    #JSON representation

#IS
#internal_standard
#internal_standard_storage

#experiments
#experiment_types
#experiment
class experiment(Base):
    #__table__ = make_table('experiment')
    __tablename__ = 'experiment'
    wid = Column(Integer, Sequence('wids'), primary_key=True,nullable=False,)
    exp_type_id=Column(Integer);
    id=Column(String(50),nullable=False, primary_key=True);
    sample_name=Column(String(500),nullable=False, primary_key=True);
    experimentor_id=Column(String(50));
    extraction_method_id=Column(String(50));
    acquisition_method_id=Column(String(50),nullable=False);
    quantitation_method_id=Column(String(50));
    internal_standard_id=Column(Integer);

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
    __table__ = make_table('data_versions')
    #TODO:
    #define relations

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
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "biologicalmaterial_storage %s" % ()

    #TODO:
    #JSON representation
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

    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "biologicalmaterial_description %s" % ()

    #TODO:
    #JSON representation
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

    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "oligos_description %s" % ()

    #TODO:
    #JSON representation
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
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "oligos_storage %s" % ()

    #TODO:
    #JSON representation

# Models
# metabolomics_models
class metabolomics_models(Base):
    __tablename__ = 'metabolomics_models'
    model_id = Column(String(100), primary_key=True)
    model_date = Column(DateTime)
    model_file = Column(Text)
    model_file_extension = Column(String(10), default = '.xml')

    def __init__(self,model_id_I, model_date_I, model_file_I, model_file_extension_I):
        self.model_id = model_id_I
        self.model_date = model_date_I
        self.model_file = model_file_I
        self.model_file_extension = model_file_exntension_I
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "oligos_storage %s" % ()

    #TODO:
    #JSON representation

# models_atomMapping
class models_atomMapping(Base):
    __tablename__ = 'models_atomMapping'
    mapping_id = Column(String(100), primary_key=True)
    mapping_date = Column(DateTime)
    mapping_description = Column(String(100), default = '13CFlux')
    rxn_id_old = Column(String(100))
    rxn_id = Column(String(100))
    ctrack = Column(String(500))
    mapping = Column(String(500))
    notes = Column(String(500))

    def __init__(self,mapping_id_I,mapping_date_I,mapping_description_I,rxn_id_old_I,rxn_id_I,ctrack_I,mapping_I,notes_I):
        self.mapping_id=mapping_id_I
        self.mapping_date=mapping_date_I
        self.mapping_description=mapping_description_I
        self.rxn_id_old=rxn_id_old_I
        self.rxn_id=rxn_id_I
        self.ctrack=ctrack_I
        self.mapping=mapping_I
        self.notes=notes_I

    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "oligos_storage %s" % ()

    #TODO:
    #JSON representation

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

    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "oligos_storage %s" % ()

    #TODO:
    #JSON representation

# Characterization
# metabolomics_characterization
class metabolomics_characterization(Base):
    __tablename__ = 'metabolomics_characterization'
    experiment_id = Column(String(50), primary_key=True)
    experiment_type=Column(Integer, primary_key=True);
    sample_name_short = Column(String(100), primary_key=True)
    sample_label = Column(String(50))
    time_point = Column(String(10))
    date_and_time = Column(DateTime, primary_key=True)
    data_raw = Column(Float)
    data_corrected = Column(Float)
    data_type = Column(String(100), primary_key=True)
    data_type_units = Column(String(100))
    data_type_reference = Column(String(500), primary_key=True)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I,experiment_type_I,sample_name_short_I,
                 sample_label_I,time_point_I,date_and_time_I,data_raw_I,data_corrected_I,
                 data_type_I,data_type_units_I,data_type_reference_I,used__I,comment__I,):
        self.experiment_id=experiment_id_I
        self.experiment_type=experiment_type_I
        self.sample_name_short=sample_name_short_I
        self.sample_label=sample_label_I
        self.time_point=time_point_I
        self.date_and_time=date_and_time_I
        self.data_raw=data_raw_I
        self.data_corrected=data_corrected_I
        self.data_type=data_type_I
        self.data_type_units=data_type_units_I
        self.data_type_reference=data_type_reference_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'experiment_type':self.experiment_type,
                'sample_name_short':self.sample_name_short,
                'sample_label':self.sample_label,
                'time_point':self.time_point,
                'time':self.time,
                'data_raw':self.data_raw,
                'data_corrected':self.data_corrected,
                'data_type_name':self.data_type_name,
                'data_type_reference':self.data_type_reference,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

'''
class standards(Base):
    __table__ = make_table('standards')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "standards %s" % ()

    #TODO:
    #JSON representation
class standards_ordering(Base):
    __table__ = make_table('standards_ordering')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "standards_ordering %s" % ()

    #TODO:
    #JSON representation
class standards2material(Base):
    __table__ = make_table('standards2material')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "standards2material %s" % ()

    #TODO:
    #JSON representation
class standards_storage(Base):
    __table__ = make_table('standards_storage')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "standards_storage %s" % ()

    #TODO:
    #JSON representation
class mix_storage(Base):
    __table__ = make_table('mix_storage')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "mix_storage %s" % ()

    #TODO:
    #JSON representation
class mix_description(Base):
    __table__ = make_table('mix_description')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "mix_description %s" % ()

    #TODO:
    #JSON representation
class mix_parameters(Base):
    __table__ = make_table('mix_parameters')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "mix_parameters %s" % ()

    #TODO:
    #JSON representation
class calibrator_met_parameters(Base):
    __table__ = make_table('calibrator_met_parameters')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "calibrator_met_parameters %s" % ()

    #TODO:
    #JSON representation
class calibrator2mix(Base):
    __table__ = make_table('calibrator2mix')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "calibrator2mix %s" % ()

    #TODO:
    #JSON representation
class mix2met_ID(Base):
    __table__ = make_table('mix2met_ID')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "mix2met_ID %s" % ()

    #TODO:
    #JSON representation
class calibrator(Base):
    __table__ = make_table('calibrator')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "calibrator %s" % ()

    #TODO:
    #JSON representation
class calibrator_calculations(Base):
    __table__ = make_table('calibrator_calculations')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "calibrator_calculations %s" % ()

    #TODO:
    #JSON representation
class calibrator_met2mix_calculations(Base):
    __table__ = make_table('calibrator_met2mix_calculations')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "calibrator_met2mix_calculations %s" % ()

    #TODO:
    #JSON representation
class mix_calculations(Base):
    __table__ = make_table('mix_calculations')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "mix_calculations %s" % ()

    #TODO:
    #JSON representation
class calibrator_levels(Base):
    __table__ = make_table('calibrator_levels')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "calibrator_levels %s" % ()

    #TODO:
    #JSON representation

class MS_sourceParameters(Base):
    __table__ = make_table('MS_sourceParameters')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "MS_sourceParameters %s" % ()

    #TODO:
    #JSON representation
class MS_information(Base):
    __table__ = make_table('MS_information')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "MS_information %s" % ()

    #TODO:
    #JSON representation

class Autosampler_parameters(Base):
    __table__ = make_table('Autosampler_parameters')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "Autosampler_parameters %s" % ()

    #TODO:
    #JSON representation
class Autosampler_information(Base):
    __table__ = make_table('Autosampler_information')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "Autosampler_information %s" % ()

    #TODO:
    #JSON representation
class Autosampler_method(Base):
    __table__ = make_table('Autosampler_method')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "Autosampler_method %s" % ()

    #TODO:
    #JSON representation
class LC_information(Base):
    __table__ = make_table('LC_information')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "LC_information %s" % ()

    #TODO:
    #JSON representation
class LC_gradient(Base):
    __table__ = make_table('LC_gradient')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "LC_gradient %s" % ()

    #TODO:
    #JSON representation
class LC_parameters(Base):
    __table__ = make_table('LC_parameters')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "LC_parameters %s" % ()

    #TODO:
    #JSON representation
class LC_method(Base):
    __table__ = make_table('LC_method')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "LC_method %s" % ()

    #TODO:
    #JSON representation

class batch_information(Base):
    __table__ = make_table('batch_information')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "batch_information %s" % ()

    #TODO:
    #JSON representation

class experiments(Base):
    __table__ = make_table('experiments')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "experiments %s" % ()

    #TODO:
    #JSON representation
class experiment_types(Base):
    __table__ = make_table('experiment_types')
    #TODO:
    #define relations

    #TODO:
    #define representation
    #def __repr__(self):
        #return "experiment_types %s" % ()

    #TODO:
    #JSON representation
'''