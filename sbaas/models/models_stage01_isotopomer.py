# ORMs
from models_base import *
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

    def __init__(self, experiment_id_I, sample_name_I, sample_name_abbreviation_I, sample_type_I,
                 time_point_I, dilution_I, replicate_number_I, met_id_I,
                 fragment_formula_I, fragment_mass_I, intensity_I, intensity_units_I,
                 intensity_corrected_I, intensity_corrected_units_I, intensity_normalized_I, intensity_normalized_units_I,
                 intensity_theoretical_I, abs_devFromTheoretical_I, scan_type_I, used_I):
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

    def __repr__dict__(self):
        return {'experiment_id_I':self.experiment_id,
                'sample_name_I':self.sample_name,
                'sample_name_abbreviation_I':self.sample_name_abbreviation,
                'sample_type_I':self.sample_type,
                'time_point_I':self.time_point,
                'dilution_I':self.dilution,
                'replicate_number_I':self.replicate_number,
                'met_id_I':self.met_id,
                'fragment_formula_I':self.fragment_formula,
                'fragment_mass_I':self.fragment_mass,
                'intensity_I':self.intensity,
                'intensity_units_I':self.intensity_units,
                'intensity_corrected_I':self.intensity_corrected,
                'intensity_corrected_units_I':self.intensity_corrected_units,
                'intensity_normalized_I':self.intensity_normalized,
                'intensity_normalized_units_I':self.intensity_normalized_units,
                'intensity_theoretical_I':self.intensity_theoretical,
                'abs_devFromTheoretical_I':self.abs_devFromTheoretical,
                'scan_type_I':self.scan_type,
                'used_I':self.used_,
                'comments_I':self.comments_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_isotopomer_averages(Base):
    __tablename__ = 'data_stage01_isotopomer_averages'
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    sample_type = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    met_id = Column(String(100), primary_key=True)
    fragment_formula = Column(String(500), primary_key=True)
    fragment_mass = Column(Integer, primary_key=True)
    n_replicates = Column(Integer)
    intensity_normalized_average = Column(Float)
    intensity_normalized_cv = Column(Float)
    intensity_normalized_units = Column(String(20))
    intensity_theoretical = Column(Float)
    abs_devFromTheoretical = Column(Float)
    scan_type = Column(String(50), primary_key=True);
    used_ = Column(Boolean);
    comment_ = Column(Text);

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
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    sample_type = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    met_id = Column(String(100), primary_key=True)
    fragment_formula = Column(String(500), primary_key=True)
    fragment_mass = Column(Integer, primary_key=True)
    n_replicates = Column(Integer)
    intensity_normalized_average = Column(Float)
    intensity_normalized_cv = Column(Float)
    intensity_normalized_units = Column(String(20))
    intensity_theoretical = Column(Float)
    abs_devFromTheoretical = Column(Float)
    scan_type = Column(String(50), primary_key=True);
    used_ = Column(Boolean);
    comment_ = Column(Text);

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