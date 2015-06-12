# ORMs
from .models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage01_isotopomer_normalized(Base):
    __tablename__ = 'data_stage01_isotopomer_normalized'
    id = Column(Integer, Sequence('data_stage01_isotopomer_normalized_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    sample_type = Column(String(100))
    time_point = Column(String(10))
    dilution = Column(Float)
    replicate_number = Column(Integer)
    met_id = Column(String(100))
    fragment_formula = Column(String(500))
    fragment_mass = Column(Integer)
    intensity = Column(Float)
    intensity_units = Column(String(20))
    intensity_corrected = Column(Float)
    intensity_corrected_units = Column(String(20))
    intensity_normalized = Column(Float)
    intensity_normalized_units = Column(String(20))
    intensity_theoretical = Column(Float)
    abs_devFromTheoretical = Column(Float)
    scan_type = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('experiment_id','sample_name','sample_type','met_id','time_point','fragment_formula','fragment_mass','scan_type'),
            )

    def __init__(self, experiment_id_I, sample_name_I, sample_name_abbreviation_I, sample_type_I,
                 time_point_I, dilution_I, replicate_number_I, met_id_I,
                 fragment_formula_I, fragment_mass_I, intensity_I, intensity_units_I,
                 intensity_corrected_I, intensity_corrected_units_I, intensity_normalized_I, intensity_normalized_units_I,
                 intensity_theoretical_I, abs_devFromTheoretical_I, scan_type_I, used_I,comment_I):
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.sample_type = sample_type_I;
        self.time_point = time_point_I;
        self.dilution = dilution_I;
        self.replicate_number = replicate_number_I;
        self.met_id = met_id_I;
        self.fragment_formula = fragment_formula_I;
        self.fragment_mass = fragment_mass_I;
        self.intensity = intensity_I;
        self.intensity_units = intensity_units_I;
        self.intensity_corrected = intensity_corrected_I;
        self.intensity_corrected_units = intensity_corrected_units_I;
        self.intensity_normalized = intensity_normalized_I;
        self.intensity_normalized_units = intensity_normalized_units_I;
        self.intensity_theoretical = intensity_theoretical_I;
        self.abs_devFromTheoretical = abs_devFromTheoretical_I;
        self.scan_type = scan_type_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            'experiment_id':self.experiment_id,
                'sample_name':self.sample_name,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'sample_type':self.sample_type,
                'time_point':self.time_point,
                'dilution':self.dilution,
                'replicate_number':self.replicate_number,
                'met_id':self.met_id,
                'fragment_formula':self.fragment_formula,
                'fragment_mass':self.fragment_mass,
                'intensity':self.intensity,
                'intensity_units':self.intensity_units,
                'intensity_corrected':self.intensity_corrected,
                'intensity_corrected_units':self.intensity_corrected_units,
                'intensity_normalized':self.intensity_normalized,
                'intensity_normalized_units':self.intensity_normalized_units,
                'intensity_theoretical':self.intensity_theoretical,
                'abs_devFromTheoretical':self.abs_devFromTheoretical,
                'scan_type':self.scan_type,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_isotopomer_averages(Base):
    __tablename__ = 'data_stage01_isotopomer_averages'
    #id = Column(Integer, Sequence('data_stage01_isotopomer_averages_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    sample_type = Column(String(100))
    time_point = Column(String(10))
    met_id = Column(String(100))
    fragment_formula = Column(String(500))
    fragment_mass = Column(Integer)
    n_replicates = Column(Integer)
    intensity_normalized_average = Column(Float)
    intensity_normalized_cv = Column(Float)
    intensity_normalized_units = Column(String(20))
    intensity_theoretical = Column(Float)
    abs_devFromTheoretical = Column(Float)
    scan_type = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (PrimaryKeyConstraint('experiment_id','sample_name_abbreviation','sample_type','met_id','time_point','fragment_formula','fragment_mass','scan_type'),
                      #UniqueConstraint('experiment_id','sample_name_abbreviation','sample_type','met_id','time_point','fragment_formula','fragment_mass','scan_type'),
            )

    def __init__(self, experiment_id_I, sample_name_abbreviation_I,  sample_type_I, time_point_I, met_id_I,fragment_formula_I, fragment_mass_I,
                    n_replicates_I, intensity_normalized_average_I, intensity_normalized_cv_I,
                    intensity_normalized_units_I, intensity_theoretical_I, abs_devFromTheoretical_I, scan_type_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.sample_type = sample_type_I;
        self.time_point = time_point_I;
        self.met_id = met_id_I;
        self.fragment_formula = fragment_formula_I;
        self.fragment_mass = fragment_mass_I;
        self.n_replicates = n_replicates_I;
        self.intensity_normalized_average = intensity_normalized_average_I;
        self.intensity_normalized_cv = intensity_normalized_cv_I;
        self.intensity_normalized_units = intensity_normalized_units_I;
        self.intensity_theoretical = intensity_theoretical_I;
        self.abs_devFromTheoretical = abs_devFromTheoretical_I;
        self.used_ = used_I;
        self.scan_type = scan_type_I;

class data_stage01_isotopomer_averagesNormSum(Base):
    __tablename__ = 'data_stage01_isotopomer_averagesNormSum'
    #id = Column(Integer, Sequence('data_stage01_isotopomer_averagesNormSum_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    sample_type = Column(String(100))
    time_point = Column(String(10))
    met_id = Column(String(100))
    fragment_formula = Column(String(500))
    fragment_mass = Column(Integer)
    n_replicates = Column(Integer)
    intensity_normalized_average = Column(Float)
    intensity_normalized_cv = Column(Float)
    intensity_normalized_units = Column(String(20))
    intensity_theoretical = Column(Float)
    abs_devFromTheoretical = Column(Float)
    scan_type = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (PrimaryKeyConstraint('experiment_id','sample_name_abbreviation','sample_type','met_id','time_point','fragment_formula','fragment_mass','scan_type'),
                      #UniqueConstraint('experiment_id','sample_name_abbreviation','sample_type','met_id','time_point','fragment_formula','fragment_mass','scan_type'),
            )

    def __init__(self, experiment_id_I, sample_name_abbreviation_I,  sample_type_I, time_point_I, met_id_I,fragment_formula_I, fragment_mass_I,
                    n_replicates_I, intensity_normalized_average_I, intensity_normalized_cv_I,
                    intensity_normalized_units_I, intensity_theoretical_I, abs_devFromTheoretical_I, scan_type_I, used_I, comment_I=None):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.sample_type = sample_type_I;
        self.time_point = time_point_I;
        self.met_id = met_id_I;
        self.fragment_formula = fragment_formula_I;
        self.fragment_mass = fragment_mass_I;
        self.n_replicates = n_replicates_I;
        self.intensity_normalized_average = intensity_normalized_average_I;
        self.intensity_normalized_cv = intensity_normalized_cv_I;
        self.intensity_normalized_units = intensity_normalized_units_I;
        self.intensity_theoretical = intensity_theoretical_I;
        self.abs_devFromTheoretical = abs_devFromTheoretical_I;
        self.used_ = used_I;
        self.scan_type = scan_type_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
                'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'sample_type':self.sample_type,
                'time_point':self.time_point,
                'met_id':self.met_id,
                'fragment_formula':self.fragment_formula,
                'fragment_mass':self.fragment_mass,
                'intensity_normalized_average':self.intensity_normalized_average,
                'intensity_normalized_cv':self.intensity_normalized_cv,
                'intensity_normalized_units':self.intensity_normalized_units,
                'intensity_theoretical':self.intensity_theoretical,
                'abs_devFromTheoretical':self.abs_devFromTheoretical,
                'scan_type':self.scan_type,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_isotopomer_peakData(Base):
    __tablename__ = 'data_stage01_isotopomer_peakData'
    id = Column(Integer, Sequence('data_stage01_isotopomer_peakdata_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    met_id = Column(String(500))
    precursor_formula = Column(String(500))
    mass = Column(Float)
    mass_units = Column(String(20), default='Da')
    intensity = Column(Float)
    intensity_units = Column(String(20), default='cps')
    scan_type = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_I, met_id_I, precursor_formula_I, mass_I, mass_units_I,
                    intensity_I, intensity_units_I, scan_type_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.met_id = met_id_I;
        self.precursor_formula = precursor_formula_I;
        self.mass = mass_I;
        self.mass_units = mass_units_I;
        self.intensity = intensity_I;
        self.intensity_units = intensity_units_I;
        self.scan_type = scan_type_I;
        self.used_ = used_I;

class data_stage01_isotopomer_peakList(Base):
    __tablename__ = 'data_stage01_isotopomer_peakList'
    id = Column(Integer, Sequence('data_stage01_isotopomer_peaklist_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    met_id = Column(String(500))
    precursor_formula = Column(String(500))
    mass = Column(Float)
    mass_units = Column(String(20), default='Da')
    intensity = Column(Float)
    intensity_units = Column(String(20), default='cps')
    centroid_mass = Column(Float)
    centroid_mass_units = Column(String(20), default='Da')
    peak_start = Column(Float)
    peak_start_units = Column(String(20), default='Da')
    peak_stop = Column(Float);
    peak_stop_units = Column(String(20), default='Da')
    resolution = Column(Float);
    scan_type = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_I, met_id_I, precursor_formula_I, mass_I, mass_units_I,
                    intensity_I, intensity_units_I, centroid_mass_I, centroid_mass_units_I,
                    peak_start_I, peak_start_units_I, peak_stop_I, peak_stop_units_I,
                    resolution_I, scan_type_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.met_id = met_id_I;
        self.precursor_formula = precursor_formula_I;
        self.mass = mass_I;
        self.mass_units = mass_units_I;
        self.intensity = intensity_I;
        self.intensity_units = intensity_units_I;
        self.centroid_mass = centroid_mass_I;
        self.centroid_mass_units = centroid_mass_units_I;
        self.peak_start = peak_start_I;
        self.peak_start_units = peak_start_units_I;
        self.peak_stop = peak_stop_I;
        self.peak_stop_units = peak_stop_units_I;
        self.resolution = resolution_I;
        self.scan_type = scan_type_I;
        self.used_ = used_I;
        
class data_stage01_isotopomer_peakSpectrum(Base):
    __tablename__ = 'data_stage01_isotopomer_peakSpectrum'
    id = Column(Integer, Sequence('data_stage01_isotopomer_peakSpectrum_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    sample_type = Column(String(100))
    time_point = Column(String(10))
    replicate_number = Column(Integer)
    met_id = Column(String(100))
    precursor_formula = Column(String(500))
    precursor_mass = Column(Integer)#Column(Float)
    product_formula = Column(String(500))
    product_mass = Column(Integer)#Column(Float)
    intensity = Column(Float)
    intensity_units = Column(String(20))
    intensity_corrected = Column(Float)
    intensity_corrected_units = Column(String(20))
    intensity_normalized = Column(Float)
    intensity_normalized_units = Column(String(20))
    intensity_theoretical = Column(Float)
    abs_devFromTheoretical = Column(Float)
    scan_type = Column(String(50));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_I, sample_name_abbreviation_I, sample_type_I, time_point_I, replicate_number_I, met_id_I,
                 precursor_formula_I, precursor_mass_I, product_formula_I, product_mass_I, intensity_I, intensity_units_I,
                 intensity_corrected_I, intensity_corrected_units_I, intensity_normalized_I, intensity_normalized_units_I,
                 intensity_theoretical_I, abs_devFromTheoretical_I, scan_type_I, used_I, comment_I):
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.sample_type = sample_type_I;
        self.time_point = time_point_I;
        self.replicate_number = replicate_number_I;
        self.met_id = met_id_I;
        self.precursor_formula = precursor_formula_I;
        self.precursor_mass = precursor_mass_I;
        self.product_formula = product_formula_I;
        self.product_mass = product_mass_I;
        self.intensity = intensity_I;
        self.intensity_units = intensity_units_I;
        self.intensity_corrected = intensity_corrected_I;
        self.intensity_corrected_units = intensity_corrected_units_I;
        self.intensity_normalized = intensity_normalized_I;
        self.intensity_normalized_units = intensity_normalized_units_I;
        self.intensity_theoretical = intensity_theoretical_I;
        self.abs_devFromTheoretical = abs_devFromTheoretical_I;
        self.scan_type = scan_type_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

# views:
class data_stage01_isotopomer_spectrumAccuracy(Base):
    __tablename__ = 'data_stage01_isotopomer_spectrumAccuracy'
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    sample_type = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    met_id = Column(String(100), primary_key=True)
    fragment_formula = Column(String(500), primary_key=True)
    spectrum_accuracy = Column(Float)
    scan_type = Column(String(50), primary_key=True);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_abbreviation_I,  sample_type_I, time_point_I, met_id_I,fragment_formula_I,
                    spectrum_accuracy_I, scan_type_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.sample_type = sample_type_I;
        self.time_point = time_point_I;
        self.met_id = met_id_I;
        self.fragment_formula = fragment_formula_I;
        self.spectrum_accuracy = spectrum_accuracy_I;
        self.used_ = used_I;
        self.scan_type = scan_type_I;
class data_stage01_isotopomer_spectrumAccuracyNormSum(Base):
    __tablename__ = 'data_stage01_isotopomer_spectrumAccuracyNormSum'
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    sample_type = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    met_id = Column(String(100), primary_key=True)
    fragment_formula = Column(String(500), primary_key=True)
    spectrum_accuracy = Column(Float)
    scan_type = Column(String(50), primary_key=True);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_abbreviation_I,  sample_type_I, time_point_I, met_id_I,fragment_formula_I,
                    spectrum_accuracy_I, scan_type_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.sample_type = sample_type_I;
        self.time_point = time_point_I;
        self.met_id = met_id_I;
        self.fragment_formula = fragment_formula_I;
        self.spectrum_accuracy = spectrum_accuracy_I;
        self.used_ = used_I;
        self.scan_type = scan_type_I;

class data_stage01_isotopomer_MQResultsTable(Base):
    #__table__ = make_table('data_stage01_isotopomer_mqresultstable')
    __tablename__ = 'data_stage01_isotopomer_mqresultstable'
    index_=Column(Integer);
    sample_index=Column(Integer);
    original_filename=Column(Text);
    sample_name=Column(String(100),nullable=False, primary_key=True);
    sample_id=Column(String(500));
    sample_comment=Column(Text);
    sample_type=Column(String(20));
    acquisition_date_and_time=Column(DateTime,nullable=False, primary_key=True);
    rack_number=Column(Integer);
    plate_number=Column(Integer);
    vial_number=Column(Integer);
    dilution_factor=Column(Float);
    injection_volume=Column(Float);
    operator_name=Column(String(100));
    acq_method_name=Column(String(100));
    is_=Column(Boolean);
    component_name=Column(String(500),nullable=False, primary_key=True);
    component_index=Column(Integer);
    component_comment=Column(Text);
    is_comment=Column(Text);
    mass_info=Column(String(100));
    is_mass=Column(String(100));
    is_name=Column(String(500));
    component_group_name=Column(String(100));
    conc_units=Column(String(20));
    failed_query=Column(Boolean);
    is_failed_query=Column(Boolean);
    peak_comment=Column(Text);
    is_peak_comment=Column(Text);
    actual_concentration=Column(Float);
    is_actual_concentration=Column(Float);
    concentration_ratio=Column(Float);
    expected_rt=Column(Float);
    is_expected_rt=Column(Float);
    integration_type=Column(String(100));
    is_integration_type=Column(String(100));
    area=Column(Float);
    is_area=Column(Float);
    corrected_area=Column(Float);
    is_corrected_area=Column(Float);
    area_ratio=Column(Float);
    height=Column(Float);
    is_height=Column(Float);
    corrected_height=Column(Float);
    is_corrected_height=Column(Float);
    height_ratio=Column(Float);
    area_2_height=Column(Float);
    is_area_2_height=Column(Float);
    corrected_area2height=Column(Float);
    is_corrected_area2height=Column(Float);
    region_height=Column(Float);
    is_region_height=Column(Float);
    quality=Column(Float);
    is_quality=Column(Float);
    retention_time=Column(Float);
    is_retention_time=Column(Float);
    start_time=Column(Float);
    is_start_time=Column(Float);
    end_time=Column(Float);
    is_end_time=Column(Float);
    total_width=Column(Float);
    is_total_width=Column(Float);
    width_at_50=Column(Float);
    is_width_at_50=Column(Float);
    signal_2_noise=Column(Float);
    is_signal_2_noise=Column(Float);
    baseline_delta_2_height=Column(Float);
    is_baseline_delta_2_height=Column(Float);
    modified_=Column(Boolean);
    relative_rt=Column(Float);
    used_=Column(Boolean);
    calculated_concentration=Column(Float);
    accuracy_=Column(Float);
    comment_=Column(Text);
    use_calculated_concentration=Column(Boolean,default=True);

    def __init__(self,index__I,sample_index_I,original_filename_I,
                 sample_name_I,sample_id_I,sample_comment_I,sample_type_I,
                 acquisition_date_and_time_I,rack_number_I,plate_number_I,
                 vial_number_I,dilution_factor_I,injection_volume_I,
                 operator_name_I,acq_method_name_I,is__I,component_name_I,
                 component_index_I,component_comment_I,is_comment_I,
                 mass_info_I,is_mass_I,is_name_I,component_group_name_I,
                 conc_units_I,failed_query_I,is_failed_query_I,peak_comment_I,
                 is_peak_comment_I,actual_concentration_I,is_actual_concentration_I,
                 concentration_ratio_I,expected_rt_I,is_expected_rt_I,
                 integration_type_I,is_integration_type_I,area_I,is_area_I,
                 corrected_area_I,is_corrected_area_I,area_ratio_I,height_I,
                 is_height_I,corrected_height_I,is_corrected_height_I,
                 height_ratio_I,area_2_height_I,is_area_2_height_I,
                 corrected_area2height_I,is_corrected_area2height_I,
                 region_height_I,is_region_height_I,quality_I,is_quality_I,
                 retention_time_I,is_retention_time_I,start_time_I,
                 is_start_time_I,end_time_I,is_end_time_I,total_width_I,
                 is_total_width_I,width_at_50_I,is_width_at_50_I,
                 signal_2_noise_I,is_signal_2_noise_I,baseline_delta_2_height_I,
                 is_baseline_delta_2_height_I,modified__I,relative_rt_I,used__I,
                 calculated_concentration_I,accuracy__I,comment__I,use_calculated_concentration_I):
        self.index_=index__I;
        self.sample_index=sample_index_I;
        self.original_filename=original_filename_I;
        self.sample_name=sample_name_I;
        self.sample_id=sample_id_I;
        self.sample_comment=sample_comment_I;
        self.sample_type=sample_type_I;
        self.acquisition_date_and_time=acquisition_date_and_time_I;
        self.rack_number=rack_number_I;
        self.plate_number=plate_number_I;
        self.vial_number=vial_number_I;
        self.dilution_factor=dilution_factor_I;
        self.injection_volume=injection_volume_I;
        self.operator_name=operator_name_I;
        self.acq_method_name=acq_method_name_I;
        self.is_=is__I;
        self.component_name=component_name_I;
        self.component_index=component_index_I;
        self.component_comment=component_comment_I;
        self.is_comment=is_comment_I;
        self.mass_info=mass_info_I;
        self.is_mass=is_mass_I;
        self.is_name=is_name_I;
        self.component_group_name=component_group_name_I;
        self.conc_units=conc_units_I;
        self.failed_query=failed_query_I;
        self.is_failed_query=is_failed_query_I;
        self.peak_comment=peak_comment_I;
        self.is_peak_comment=is_peak_comment_I;
        self.actual_concentration=actual_concentration_I;
        self.is_actual_concentration=is_actual_concentration_I;
        self.concentration_ratio=concentration_ratio_I;
        self.expected_rt=expected_rt_I;
        self.is_expected_rt=is_expected_rt_I;
        self.integration_type=integration_type_I;
        self.is_integration_type=is_integration_type_I;
        self.area=area_I;
        self.is_area=is_area_I;
        self.corrected_area=corrected_area_I;
        self.is_corrected_area=is_corrected_area_I;
        self.area_ratio=area_ratio_I;
        self.height=height_I;
        self.is_height=is_height_I;
        self.corrected_height=corrected_height_I;
        self.is_corrected_height=is_corrected_height_I;
        self.height_ratio=height_ratio_I;
        self.area_2_height=area_2_height_I;
        self.is_area_2_height=is_area_2_height_I;
        self.corrected_area2height=corrected_area2height_I;
        self.is_corrected_area2height=is_corrected_area2height_I;
        self.region_height=region_height_I;
        self.is_region_height=is_region_height_I;
        self.quality=quality_I;
        self.is_quality=is_quality_I;
        self.retention_time=retention_time_I;
        self.is_retention_time=is_retention_time_I;
        self.start_time=start_time_I;
        self.is_start_time=is_start_time_I;
        self.end_time=end_time_I;
        self.is_end_time=is_end_time_I;
        self.total_width=total_width_I;
        self.is_total_width=is_total_width_I;
        self.width_at_50=width_at_50_I;
        self.is_width_at_50=is_width_at_50_I;
        self.signal_2_noise=signal_2_noise_I;
        self.is_signal_2_noise=is_signal_2_noise_I;
        self.baseline_delta_2_height=baseline_delta_2_height_I;
        self.is_baseline_delta_2_height=is_baseline_delta_2_height_I;
        self.modified_=modified__I;
        self.relative_rt=relative_rt_I;
        self.used_=used__I;
        self.calculated_concentration=calculated_concentration_I;
        self.accuracy_=accuracy__I;
        self.comment_=comment__I;
        self.use_calculated_concentration=use_calculated_concentration_I;

    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "data_stage01_isotopomer_MQResultsTable %s" % (self.acquisition_date_and_time, self.sample_name,self.component_name)