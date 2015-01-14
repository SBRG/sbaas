--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.1
-- Dumped by pg_dump version 9.3.1
-- Started on 2015-01-14 09:07:51

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 6 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 3138 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 399 (class 3079 OID 11750)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 3140 (class 0 OID 0)
-- Dependencies: 399
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 170 (class 1259 OID 130603)
-- Name: acquisition_method; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE acquisition_method (
    id character varying(50) NOT NULL,
    ms_method_id character varying(50),
    autosampler_method_id character varying(50),
    lc_method_id character varying(50)
);


ALTER TABLE public.acquisition_method OWNER TO postgres;

--
-- TOC entry 171 (class 1259 OID 130606)
-- Name: autosampler_information; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE autosampler_information (
    manufacturer character varying(100) NOT NULL,
    id character varying(100) NOT NULL,
    serial_number character varying(100) NOT NULL
);


ALTER TABLE public.autosampler_information OWNER TO postgres;

--
-- TOC entry 172 (class 1259 OID 130609)
-- Name: autosampler_method; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE autosampler_method (
    id character varying(50) NOT NULL,
    autosampler_parameters_id character varying(50) NOT NULL,
    autosampler_information_id character varying(50) NOT NULL
);


ALTER TABLE public.autosampler_method OWNER TO postgres;

--
-- TOC entry 173 (class 1259 OID 130612)
-- Name: autosampler_parameters; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE autosampler_parameters (
    id character varying(50) NOT NULL,
    injvolume_ul double precision,
    washsolvent1 character varying(500),
    washsolvent2 character varying(500)
);


ALTER TABLE public.autosampler_parameters OWNER TO postgres;

--
-- TOC entry 174 (class 1259 OID 130618)
-- Name: biologicalmaterial_description; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE biologicalmaterial_description (
    biologicalmaterial_id character varying(100) NOT NULL,
    biologicalmaterial_strain character varying(100),
    biologicalmaterial_notes text,
    biologicalmaterial_description text
);


ALTER TABLE public.biologicalmaterial_description OWNER TO postgres;

--
-- TOC entry 175 (class 1259 OID 130624)
-- Name: biologicalmaterial_genereferences; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE biologicalmaterial_genereferences (
    id integer NOT NULL,
    biologicalmaterial_id character varying(100),
    ordered_locus_name character varying(20),
    ordered_locus_name2 character varying(100),
    swissprot_entry_name character varying(20),
    ac character varying(20),
    ecogene_accession_number character varying(20),
    gene_name character varying(20)
);


ALTER TABLE public.biologicalmaterial_genereferences OWNER TO postgres;

--
-- TOC entry 176 (class 1259 OID 130627)
-- Name: biologicalmaterial_genereferences_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE biologicalmaterial_genereferences_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.biologicalmaterial_genereferences_id_seq OWNER TO postgres;

--
-- TOC entry 177 (class 1259 OID 130629)
-- Name: biologicalmaterial_storage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE biologicalmaterial_storage (
    biologicalmaterial_id character varying(100) NOT NULL,
    biologicalmaterial_label character varying(100),
    biologicalmaterial_box integer,
    biologicalmaterial_posstart integer,
    biologicalmaterial_posend integer,
    biologicalmaterial_date timestamp without time zone
);


ALTER TABLE public.biologicalmaterial_storage OWNER TO postgres;

--
-- TOC entry 178 (class 1259 OID 130632)
-- Name: calibrator; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE calibrator (
    met_id character varying(50) NOT NULL,
    lloq double precision,
    uloq double precision,
    uloq_working double precision,
    concentration_units character varying(25),
    stockdate date
);


ALTER TABLE public.calibrator OWNER TO postgres;

--
-- TOC entry 179 (class 1259 OID 130635)
-- Name: calibrator2mix; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE calibrator2mix (
    calibrator_id integer NOT NULL,
    mix_id character varying(25) NOT NULL
);


ALTER TABLE public.calibrator2mix OWNER TO postgres;

--
-- TOC entry 180 (class 1259 OID 130638)
-- Name: calibrator_calculations; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE calibrator_calculations (
    met_id character varying(50) NOT NULL,
    calcstart_concentration double precision,
    start_concentration double precision
);


ALTER TABLE public.calibrator_calculations OWNER TO postgres;

--
-- TOC entry 181 (class 1259 OID 130641)
-- Name: calibrator_concentrations; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE calibrator_concentrations (
    met_id character varying(50) NOT NULL,
    calibrator_level integer NOT NULL,
    dilution_factor double precision,
    calibrator_concentration double precision,
    concentration_units character varying(25)
);


ALTER TABLE public.calibrator_concentrations OWNER TO postgres;

--
-- TOC entry 182 (class 1259 OID 130644)
-- Name: calibrator_levels; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE calibrator_levels (
    calibrator_level integer NOT NULL,
    dilution double precision NOT NULL,
    injectionvolume double precision,
    workingvolume double precision,
    dilution_factor_from_the_previous_level double precision,
    amount_from_previous_level double precision,
    balance_h2o double precision,
    dilution_concentration double precision
);


ALTER TABLE public.calibrator_levels OWNER TO postgres;

--
-- TOC entry 183 (class 1259 OID 130647)
-- Name: calibrator_met2mix_calculations; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE calibrator_met2mix_calculations (
    met_id character varying(50) NOT NULL,
    mix_id character varying(25) NOT NULL,
    working_concentration double precision,
    total_volume double precision,
    add_volume double precision
);


ALTER TABLE public.calibrator_met2mix_calculations OWNER TO postgres;

--
-- TOC entry 184 (class 1259 OID 130650)
-- Name: calibrator_met_parameters; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE calibrator_met_parameters (
    met_id character varying(50) NOT NULL,
    dilution integer NOT NULL
);


ALTER TABLE public.calibrator_met_parameters OWNER TO postgres;

--
-- TOC entry 185 (class 1259 OID 130653)
-- Name: data_stage01_QCs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_QCs_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_QCs_id_seq" OWNER TO postgres;

--
-- TOC entry 186 (class 1259 OID 130655)
-- Name: data_stage01_ale_jumps; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_ale_jumps (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100),
    jump_region_start double precision,
    jump_region_stop double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage01_ale_jumps OWNER TO postgres;

--
-- TOC entry 187 (class 1259 OID 130661)
-- Name: data_stage01_ale_jumps_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_ale_jumps_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_ale_jumps_id_seq OWNER TO postgres;

--
-- TOC entry 188 (class 1259 OID 130663)
-- Name: data_stage01_ale_trajectories; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_ale_trajectories (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100),
    ale_time double precision NOT NULL,
    ale_time_units character varying(50),
    rate double precision,
    rate_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage01_ale_trajectories OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 130669)
-- Name: data_stage01_ale_trajectories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_ale_trajectories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_ale_trajectories_id_seq OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 130671)
-- Name: data_stage01_averages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_averages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_averages_id_seq OWNER TO postgres;

--
-- TOC entry 191 (class 1259 OID 130673)
-- Name: data_stage01_checkCVAndExtracellular_averages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_checkCVAndExtracellular_averages_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_checkCVAndExtracellular_averages_id_seq" OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 130675)
-- Name: data_stage01_checkCV_dilutions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_checkCV_dilutions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_checkCV_dilutions_id_seq" OWNER TO postgres;

--
-- TOC entry 193 (class 1259 OID 130677)
-- Name: data_stage01_checkLLOQAndULOQ_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_checkLLOQAndULOQ_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_checkLLOQAndULOQ_id_seq" OWNER TO postgres;

--
-- TOC entry 194 (class 1259 OID 130679)
-- Name: data_stage01_dilutions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_dilutions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_dilutions_id_seq OWNER TO postgres;

--
-- TOC entry 195 (class 1259 OID 130681)
-- Name: data_stage01_isotopomer_averages; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_isotopomer_averages (
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    sample_type character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    met_id character varying(100) NOT NULL,
    fragment_formula character varying(500) NOT NULL,
    fragment_mass integer NOT NULL,
    n_replicates integer,
    intensity_normalized_average double precision,
    intensity_normalized_cv double precision,
    intensity_normalized_units character varying(20),
    intensity_theoretical double precision,
    "abs_devFromTheoretical" double precision,
    scan_type character varying(50) NOT NULL,
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage01_isotopomer_averages OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 130687)
-- Name: data_stage01_isotopomer_averagesNormSum; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_isotopomer_averagesNormSum" (
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    sample_type character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    met_id character varying(100) NOT NULL,
    fragment_formula character varying(500) NOT NULL,
    fragment_mass integer NOT NULL,
    n_replicates integer,
    intensity_normalized_average double precision,
    intensity_normalized_cv double precision,
    intensity_normalized_units character varying(20),
    intensity_theoretical double precision,
    "abs_devFromTheoretical" double precision,
    scan_type character varying(50) NOT NULL,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_isotopomer_averagesNormSum" OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 130693)
-- Name: data_stage01_isotopomer_averagesNormSum_fragment_mass_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_isotopomer_averagesNormSum_fragment_mass_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_isotopomer_averagesNormSum_fragment_mass_seq" OWNER TO postgres;

--
-- TOC entry 3141 (class 0 OID 0)
-- Dependencies: 197
-- Name: data_stage01_isotopomer_averagesNormSum_fragment_mass_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE "data_stage01_isotopomer_averagesNormSum_fragment_mass_seq" OWNED BY "data_stage01_isotopomer_averagesNormSum".fragment_mass;


--
-- TOC entry 198 (class 1259 OID 130695)
-- Name: data_stage01_isotopomer_averages_fragment_mass_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_isotopomer_averages_fragment_mass_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_isotopomer_averages_fragment_mass_seq OWNER TO postgres;

--
-- TOC entry 3142 (class 0 OID 0)
-- Dependencies: 198
-- Name: data_stage01_isotopomer_averages_fragment_mass_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE data_stage01_isotopomer_averages_fragment_mass_seq OWNED BY data_stage01_isotopomer_averages.fragment_mass;


--
-- TOC entry 199 (class 1259 OID 130697)
-- Name: data_stage01_isotopomer_mqresultstable; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_isotopomer_mqresultstable (
    index_ integer,
    sample_index integer,
    original_filename text,
    sample_name character varying(100) NOT NULL,
    sample_id character varying(500),
    sample_comment text,
    sample_type character varying(20),
    acquisition_date_and_time timestamp without time zone NOT NULL,
    rack_number integer,
    plate_number integer,
    vial_number integer,
    dilution_factor double precision,
    injection_volume double precision,
    operator_name character varying(100),
    acq_method_name character varying(100),
    is_ boolean,
    component_name character varying(500) NOT NULL,
    component_index integer,
    component_comment text,
    is_comment text,
    mass_info character varying(100),
    is_mass character varying(100),
    is_name character varying(500),
    component_group_name character varying(100),
    conc_units character varying(20),
    failed_query boolean,
    is_failed_query boolean,
    peak_comment text,
    is_peak_comment text,
    actual_concentration double precision,
    is_actual_concentration double precision,
    concentration_ratio double precision,
    expected_rt double precision,
    is_expected_rt double precision,
    integration_type character varying(100),
    is_integration_type character varying(100),
    area double precision,
    is_area double precision,
    corrected_area double precision,
    is_corrected_area double precision,
    area_ratio double precision,
    height double precision,
    is_height double precision,
    corrected_height double precision,
    is_corrected_height double precision,
    height_ratio double precision,
    area_2_height double precision,
    is_area_2_height double precision,
    corrected_area2height double precision,
    is_corrected_area2height double precision,
    region_height double precision,
    is_region_height double precision,
    quality double precision,
    is_quality double precision,
    retention_time double precision,
    is_retention_time double precision,
    start_time double precision,
    is_start_time double precision,
    end_time double precision,
    is_end_time double precision,
    total_width double precision,
    is_total_width double precision,
    width_at_50 double precision,
    is_width_at_50 double precision,
    signal_2_noise double precision,
    is_signal_2_noise double precision,
    baseline_delta_2_height double precision,
    is_baseline_delta_2_height double precision,
    modified_ boolean,
    relative_rt double precision,
    used_ boolean,
    calculated_concentration double precision,
    accuracy_ double precision,
    comment_ text,
    use_calculated_concentration boolean DEFAULT true
);


ALTER TABLE public.data_stage01_isotopomer_mqresultstable OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 130704)
-- Name: data_stage01_isotopomer_normalized; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_isotopomer_normalized (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name character varying(100),
    sample_name_abbreviation character varying(100),
    sample_type character varying(100),
    time_point character varying(10),
    dilution double precision,
    replicate_number integer,
    met_id character varying(100),
    fragment_formula character varying(500),
    fragment_mass integer,
    intensity double precision,
    intensity_units character varying(20),
    intensity_corrected double precision,
    intensity_corrected_units character varying(20),
    intensity_normalized double precision,
    intensity_normalized_units character varying(20),
    intensity_theoretical double precision,
    "abs_devFromTheoretical" double precision,
    scan_type character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage01_isotopomer_normalized OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 130710)
-- Name: data_stage01_isotopomer_normalized_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_isotopomer_normalized_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_isotopomer_normalized_id_seq OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 130712)
-- Name: data_stage01_isotopomer_peakData; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_isotopomer_peakData" (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name character varying(100),
    met_id character varying(500),
    precursor_formula character varying(500),
    mass double precision,
    mass_units character varying(20),
    intensity double precision,
    intensity_units character varying(20),
    scan_type character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_isotopomer_peakData" OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 130718)
-- Name: data_stage01_isotopomer_peakList; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_isotopomer_peakList" (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name character varying(100),
    met_id character varying(500),
    precursor_formula character varying(500),
    mass double precision,
    mass_units character varying(20),
    intensity double precision,
    intensity_units character varying(20),
    centroid_mass double precision,
    centroid_mass_units character varying(20),
    peak_start double precision,
    peak_start_units character varying(20),
    peak_stop double precision,
    peak_stop_units character varying(20),
    resolution double precision,
    scan_type character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_isotopomer_peakList" OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 130724)
-- Name: data_stage01_isotopomer_peakSpectrum; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_isotopomer_peakSpectrum" (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name character varying(100),
    sample_name_abbreviation character varying(100),
    sample_type character varying(100),
    time_point character varying(10),
    replicate_number integer,
    met_id character varying(100),
    precursor_formula character varying(500),
    precursor_mass integer,
    product_formula character varying(500),
    product_mass integer,
    intensity double precision,
    intensity_units character varying(20),
    intensity_corrected double precision,
    intensity_corrected_units character varying(20),
    intensity_normalized double precision,
    intensity_normalized_units character varying(20),
    intensity_theoretical double precision,
    "abs_devFromTheoretical" double precision,
    scan_type character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_isotopomer_peakSpectrum" OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 130730)
-- Name: data_stage01_isotopomer_peakSpectrum_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_isotopomer_peakSpectrum_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_isotopomer_peakSpectrum_id_seq" OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 130732)
-- Name: data_stage01_isotopomer_peakdata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_isotopomer_peakdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_isotopomer_peakdata_id_seq OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 130734)
-- Name: data_stage01_isotopomer_peaklist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_isotopomer_peaklist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_isotopomer_peaklist_id_seq OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 130736)
-- Name: data_stage01_isotopomer_spectrumAccuracy; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_isotopomer_spectrumAccuracy" (
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    sample_type character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    met_id character varying(100) NOT NULL,
    fragment_formula character varying(500) NOT NULL,
    spectrum_accuracy double precision,
    scan_type character varying(50) NOT NULL,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_isotopomer_spectrumAccuracy" OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 130742)
-- Name: data_stage01_isotopomer_spectrumAccuracyNormSum; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_isotopomer_spectrumAccuracyNormSum" (
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    sample_type character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    met_id character varying(100) NOT NULL,
    fragment_formula character varying(500) NOT NULL,
    spectrum_accuracy double precision,
    scan_type character varying(50) NOT NULL,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_isotopomer_spectrumAccuracyNormSum" OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 130748)
-- Name: data_stage01_physiology_data; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_physiology_data (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_id character varying(500) NOT NULL,
    met_id character varying(100) NOT NULL,
    data_raw double precision,
    data_corrected double precision,
    data_units character varying(100),
    data_reference character varying(500) NOT NULL,
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage01_physiology_data OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 130754)
-- Name: data_stage01_physiology_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_physiology_data_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_physiology_data_id_seq OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 130756)
-- Name: data_stage01_physiology_rates; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_physiology_rates (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_short character varying(100) NOT NULL,
    met_id character varying(100) NOT NULL,
    slope double precision,
    intercept double precision,
    r2 double precision,
    rate double precision,
    rate_units character varying(20),
    p_value double precision,
    std_err double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage01_physiology_rates OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 130762)
-- Name: data_stage01_physiology_ratesAverages; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_physiology_ratesAverages" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100),
    met_id character varying(100) NOT NULL,
    n integer,
    slope_average double precision,
    intercept_average double precision,
    rate_average double precision,
    rate_var double precision,
    rate_lb double precision,
    rate_ub double precision,
    rate_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_physiology_ratesAverages" OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 130768)
-- Name: data_stage01_physiology_ratesAverages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_physiology_ratesAverages_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_physiology_ratesAverages_id_seq" OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 130770)
-- Name: data_stage01_physiology_rates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_physiology_rates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_physiology_rates_id_seq OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 130772)
-- Name: data_stage01_quantification_lloqanduloq_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_lloqanduloq_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_lloqanduloq_id_seq OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 130774)
-- Name: data_stage01_quantification_LLOQAndULOQ; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_LLOQAndULOQ" (
    experiment_id character varying(50) NOT NULL,
    sample_name character varying(100) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    calculated_concentration double precision,
    calculated_concentration_units character varying(20),
    correlation double precision,
    lloq double precision,
    uloq double precision,
    points double precision,
    used_ boolean,
    id integer DEFAULT nextval('data_stage01_quantification_lloqanduloq_id_seq'::regclass) NOT NULL
);


ALTER TABLE public."data_stage01_quantification_LLOQAndULOQ" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 130781)
-- Name: data_stage01_quantification_qcs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_qcs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_qcs_id_seq OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 130783)
-- Name: data_stage01_quantification_QCs; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_QCs" (
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    sample_dilution double precision NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    n_replicates integer,
    calculated_concentration_average double precision,
    "calculated_concentration_CV" double precision,
    calculated_concentration_units character varying(20),
    id integer DEFAULT nextval('data_stage01_quantification_qcs_id_seq'::regclass) NOT NULL
);


ALTER TABLE public."data_stage01_quantification_QCs" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 130790)
-- Name: data_stage01_quantification_averages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_averages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_averages_id_seq OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 130792)
-- Name: data_stage01_quantification_averages; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_quantification_averages (
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    n_replicates_broth integer,
    calculated_concentration_broth_average double precision,
    calculated_concentration_broth_cv double precision,
    n_replicates_filtrate integer,
    calculated_concentration_filtrate_average double precision,
    calculated_concentration_filtrate_cv double precision,
    n_replicates integer,
    calculated_concentration_average double precision,
    calculated_concentration_cv double precision,
    calculated_concentration_units character varying(20),
    extracellular_percent double precision,
    used_ boolean,
    id integer DEFAULT nextval('data_stage01_quantification_averages_id_seq'::regclass) NOT NULL
);


ALTER TABLE public.data_stage01_quantification_averages OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 130799)
-- Name: data_stage01_quantification_averagesmi_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_averagesmi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_averagesmi_id_seq OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 130801)
-- Name: data_stage01_quantification_averagesmi; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_quantification_averagesmi (
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    n_replicates integer,
    calculated_concentration_average double precision,
    calculated_concentration_cv double precision,
    calculated_concentration_units character varying(20),
    used_ boolean,
    id integer DEFAULT nextval('data_stage01_quantification_averagesmi_id_seq'::regclass) NOT NULL
);


ALTER TABLE public.data_stage01_quantification_averagesmi OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 130808)
-- Name: data_stage01_quantification_averagesmigeo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_averagesmigeo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_averagesmigeo_id_seq OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 130810)
-- Name: data_stage01_quantification_averagesmigeo; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_quantification_averagesmigeo (
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    n_replicates integer,
    calculated_concentration_average double precision,
    calculated_concentration_var double precision,
    calculated_concentration_lb double precision,
    calculated_concentration_ub double precision,
    calculated_concentration_units character varying(20),
    used_ boolean,
    id integer DEFAULT nextval('data_stage01_quantification_averagesmigeo_id_seq'::regclass) NOT NULL
);


ALTER TABLE public.data_stage01_quantification_averagesmigeo OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 130817)
-- Name: data_stage01_quantification_checkCVAndExtracellular_averages; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_checkCVAndExtracellular_averages" (
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    n_replicates_broth integer,
    calculated_concentration_broth_average double precision,
    calculated_concentration_broth_cv double precision,
    n_replicates_filtrate integer,
    calculated_concentration_filtrate_average double precision,
    calculated_concentration_filtrate_cv double precision,
    n_replicates integer,
    calculated_concentration_average double precision,
    calculated_concentration_cv double precision,
    calculated_concentration_units character varying(20),
    extracellular_percent double precision,
    used_ boolean
);


ALTER TABLE public."data_stage01_quantification_checkCVAndExtracellular_averages" OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 130823)
-- Name: data_stage01_quantification_checkCV_QCs; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_checkCV_QCs" (
    experiment_id character varying(50) NOT NULL,
    "sample_Name_Abbreviation" character varying(100) NOT NULL,
    sample_dilution double precision NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    n_replicates integer,
    calculated_concentration_average double precision,
    calculated_concentration_cv double precision,
    calculated_concentration_units character varying(20)
);


ALTER TABLE public."data_stage01_quantification_checkCV_QCs" OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 130829)
-- Name: data_stage01_quantification_checkCV_dilutions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_checkCV_dilutions" (
    experiment_id character varying(50) NOT NULL,
    sample_id character varying(100) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    n_replicates integer,
    calculated_concentration_average double precision,
    calculated_concentration_cv double precision,
    calculated_concentration_units character varying(20)
);


ALTER TABLE public."data_stage01_quantification_checkCV_dilutions" OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 130835)
-- Name: data_stage01_quantification_checkISMatch; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_checkISMatch" (
    experiment_id character varying(50) NOT NULL,
    sample_name character varying(100) NOT NULL,
    component_name character varying(500) NOT NULL,
    "IS_name_samples" character varying(500),
    "IS_name_calibrators" character varying(500)
);


ALTER TABLE public."data_stage01_quantification_checkISMatch" OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 130841)
-- Name: data_stage01_quantification_checkLLOQAndULOQ; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_checkLLOQAndULOQ" (
    experiment_id character varying(50) NOT NULL,
    sample_name character varying(100) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    calculated_concentration double precision,
    calculated_concentration_units character varying(20),
    correlation double precision,
    lloq double precision,
    uloq double precision,
    points double precision,
    used_ boolean
);


ALTER TABLE public."data_stage01_quantification_checkLLOQAndULOQ" OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 130847)
-- Name: data_stage01_quantification_dilutions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_dilutions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_dilutions_id_seq OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 130849)
-- Name: data_stage01_quantification_dilutions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_quantification_dilutions (
    experiment_id character varying(50) NOT NULL,
    sample_id character varying(100) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    n_replicates integer,
    calculated_concentration_average double precision,
    calculated_concentration_cv double precision,
    calculated_concentration_units character varying(20),
    id integer DEFAULT nextval('data_stage01_quantification_dilutions_id_seq'::regclass) NOT NULL
);


ALTER TABLE public.data_stage01_quantification_dilutions OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 130856)
-- Name: data_stage01_quantification_mqresultstable; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_quantification_mqresultstable (
    index_ integer,
    sample_index integer,
    original_filename text,
    sample_name character varying(100) NOT NULL,
    sample_id character varying(500),
    sample_comment text,
    sample_type character varying(20),
    acquisition_date_and_time timestamp without time zone NOT NULL,
    rack_number integer,
    plate_number integer,
    vial_number integer,
    dilution_factor double precision,
    injection_volume double precision,
    operator_name character varying(100),
    acq_method_name character varying(100),
    is_ boolean,
    component_name character varying(500) NOT NULL,
    component_index integer,
    component_comment text,
    is_comment text,
    mass_info character varying(100),
    is_mass character varying(100),
    is_name character varying(500),
    component_group_name character varying(100),
    conc_units character varying(20),
    failed_query boolean,
    is_failed_query boolean,
    peak_comment text,
    is_peak_comment text,
    actual_concentration double precision,
    is_actual_concentration double precision,
    concentration_ratio double precision,
    expected_rt double precision,
    is_expected_rt double precision,
    integration_type character varying(100),
    is_integration_type character varying(100),
    area double precision,
    is_area double precision,
    corrected_area double precision,
    is_corrected_area double precision,
    area_ratio double precision,
    height double precision,
    is_height double precision,
    corrected_height double precision,
    is_corrected_height double precision,
    height_ratio double precision,
    area_2_height double precision,
    is_area_2_height double precision,
    corrected_area2height double precision,
    is_corrected_area2height double precision,
    region_height double precision,
    is_region_height double precision,
    quality double precision,
    is_quality double precision,
    retention_time double precision,
    is_retention_time double precision,
    start_time double precision,
    is_start_time double precision,
    end_time double precision,
    is_end_time double precision,
    total_width double precision,
    is_total_width double precision,
    width_at_50 double precision,
    is_width_at_50 double precision,
    signal_2_noise double precision,
    is_signal_2_noise double precision,
    baseline_delta_2_height double precision,
    is_baseline_delta_2_height double precision,
    modified_ boolean,
    relative_rt double precision,
    used_ boolean,
    calculated_concentration double precision,
    accuracy_ double precision,
    comment_ text,
    use_calculated_concentration boolean DEFAULT true
);


ALTER TABLE public.data_stage01_quantification_mqresultstable OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 130863)
-- Name: data_stage01_quantification_normalized_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_normalized_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_normalized_id_seq OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 130865)
-- Name: data_stage01_quantification_normalized; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_quantification_normalized (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name character varying(100),
    sample_id character varying(100),
    component_group_name character varying(100),
    component_name character varying(500),
    calculated_concentration double precision,
    calculated_concentration_units character varying(20),
    used_ boolean,
    comment_ text,
    rid integer DEFAULT nextval('data_stage01_quantification_normalized_id_seq'::regclass) NOT NULL
);


ALTER TABLE public.data_stage01_quantification_normalized OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 130872)
-- Name: data_stage01_quantification_peakInformation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_peakInformation" (
    id integer NOT NULL,
    experiment_id character varying(50),
    component_group_name character varying(100),
    component_name character varying(500),
    "peakInfo_parameter" character varying(50),
    "peakInfo_ave" double precision,
    "peakInfo_cv" double precision,
    "peakInfo_lb" double precision,
    "peakInfo_ub" double precision,
    "peakInfo_units" character varying(50),
    sample_names character varying(100)[],
    sample_types character varying(100)[],
    acqusition_date_and_times timestamp without time zone[],
    "peakInfo_data" double precision[],
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_quantification_peakInformation" OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 130878)
-- Name: data_stage01_quantification_peakInformation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_quantification_peakInformation_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_quantification_peakInformation_id_seq" OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 130880)
-- Name: data_stage01_quantification_peakResolution; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_peakResolution" (
    id integer NOT NULL,
    experiment_id character varying(50),
    component_group_name_pair character varying(100)[],
    component_name_pair character varying(500)[],
    "peakInfo_parameter" character varying(50),
    "peakInfo_ave" double precision,
    "peakInfo_cv" double precision,
    "peakInfo_lb" double precision,
    "peakInfo_ub" double precision,
    "peakInfo_units" character varying(50),
    sample_names character varying(100)[],
    sample_types character varying(100)[],
    acqusition_date_and_times timestamp without time zone[],
    "peakInfo_data" double precision[],
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_quantification_peakResolution" OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 130886)
-- Name: data_stage01_quantification_peakResolution_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_quantification_peakResolution_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_quantification_peakResolution_id_seq" OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 130888)
-- Name: data_stage01_quantification_physiologicalRatios_averages; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_physiologicalRatios_averages" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    physiologicalratio_id character varying(50) NOT NULL,
    physiologicalratio_name character varying(100),
    physiologicalratio_value_ave double precision,
    physiologicalratio_value_cv double precision,
    physiologicalratio_value_lb double precision,
    physiologicalratio_value_ub double precision,
    physiologicalratio_description character varying(500),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_quantification_physiologicalRatios_averages" OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 130894)
-- Name: data_stage01_quantification_physiologicalRatios_averages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_quantification_physiologicalRatios_averages_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_quantification_physiologicalRatios_averages_id_seq" OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 130896)
-- Name: data_stage01_quantification_physiologicalRatios_replicates; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_quantification_physiologicalRatios_replicates" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_short character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    physiologicalratio_id character varying(50) NOT NULL,
    physiologicalratio_name character varying(100),
    physiologicalratio_value double precision,
    physiologicalratio_description character varying(500),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_quantification_physiologicalRatios_replicates" OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 130902)
-- Name: data_stage01_quantification_physiologicalRatios_replicates_id_s; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_quantification_physiologicalRatios_replicates_id_s"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_quantification_physiologicalRatios_replicates_id_s" OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 130904)
-- Name: data_stage01_quantification_physiologicalratios_averages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_physiologicalratios_averages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_physiologicalratios_averages_id_seq OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 130906)
-- Name: data_stage01_quantification_replicates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_replicates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_replicates_id_seq OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 130908)
-- Name: data_stage01_quantification_replicates; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_quantification_replicates (
    experiment_id character varying(50) NOT NULL,
    sample_name_short character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    calculated_concentration double precision,
    calculated_concentration_units character varying(20),
    used_ boolean,
    id integer DEFAULT nextval('data_stage01_quantification_replicates_id_seq'::regclass) NOT NULL
);


ALTER TABLE public.data_stage01_quantification_replicates OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 130915)
-- Name: data_stage01_quantification_replicatesmi_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_quantification_replicatesmi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_quantification_replicatesmi_id_seq OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 130917)
-- Name: data_stage01_quantification_replicatesmi; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_quantification_replicatesmi (
    experiment_id character varying(50) NOT NULL,
    sample_name_short character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    calculated_concentration double precision,
    calculated_concentration_units character varying(20),
    used_ boolean,
    id integer DEFAULT nextval('data_stage01_quantification_replicatesmi_id_seq'::regclass) NOT NULL
);


ALTER TABLE public.data_stage01_quantification_replicatesmi OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 130924)
-- Name: data_stage01_replicates_analytical_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_replicates_analytical_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_replicates_analytical_id_seq OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 130926)
-- Name: data_stage01_replicates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_replicates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_replicates_id_seq OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 130928)
-- Name: data_stage01_resequencing_endpoints; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_resequencing_endpoints (
    id integer NOT NULL,
    experiment_id character varying(50),
    endpoint_name character varying(100),
    sample_name character varying(100),
    mutation_frequency double precision,
    mutation_type character varying(3),
    mutation_position integer,
    mutation_data json,
    "isUnique" boolean,
    mutation_annotations character varying(500)[],
    mutation_genes character varying(25)[],
    mutation_locations character varying(100)[],
    mutation_links character varying(500)[],
    comment_ text
);


ALTER TABLE public.data_stage01_resequencing_endpoints OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 130934)
-- Name: data_stage01_resequencing_endpoints_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_resequencing_endpoints_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_resequencing_endpoints_id_seq OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 130936)
-- Name: data_stage01_resequencing_evidence; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_resequencing_evidence (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name character varying(100) NOT NULL,
    parent_id integer NOT NULL,
    evidence_data json
);


ALTER TABLE public.data_stage01_resequencing_evidence OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 130942)
-- Name: data_stage01_resequencing_evidence_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_resequencing_evidence_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_resequencing_evidence_id_seq OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 130944)
-- Name: data_stage01_resequencing_lineage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_resequencing_lineage (
    id integer NOT NULL,
    experiment_id character varying(50),
    lineage_name character varying(100),
    sample_name character varying(100),
    intermediate integer,
    mutation_frequency double precision,
    mutation_type character varying(3),
    mutation_position integer,
    mutation_data json,
    mutation_annotations character varying(500)[],
    mutation_genes character varying(25)[],
    mutation_locations character varying(100)[],
    mutation_links character varying(500)[],
    comment_ text
);


ALTER TABLE public.data_stage01_resequencing_lineage OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 130950)
-- Name: data_stage01_resequencing_lineage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_resequencing_lineage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_resequencing_lineage_id_seq OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 130952)
-- Name: data_stage01_resequencing_metadata; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_resequencing_metadata (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name character varying(100),
    genome_diff double precision,
    refseq character varying(500),
    readseq character varying(500)[],
    author character varying(100)
);


ALTER TABLE public.data_stage01_resequencing_metadata OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 130958)
-- Name: data_stage01_resequencing_metadata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_resequencing_metadata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_resequencing_metadata_id_seq OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 130960)
-- Name: data_stage01_resequencing_mutations; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_resequencing_mutations (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name character varying(100) NOT NULL,
    mutation_id integer NOT NULL,
    parent_ids integer[],
    mutation_data json
);


ALTER TABLE public.data_stage01_resequencing_mutations OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 130966)
-- Name: data_stage01_resequencing_mutationsAnnotated; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_resequencing_mutationsAnnotated" (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name character varying(100),
    mutation_frequency double precision,
    mutation_type character varying(3),
    mutation_position integer,
    mutation_data json,
    mutation_annotations character varying(500)[],
    mutation_genes character varying(25)[],
    mutation_locations character varying(100)[],
    mutation_links character varying(500)[],
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage01_resequencing_mutationsAnnotated" OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 130972)
-- Name: data_stage01_resequencing_mutationsAnnotated_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_resequencing_mutationsAnnotated_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_resequencing_mutationsAnnotated_id_seq" OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 130974)
-- Name: data_stage01_resequencing_mutationsFiltered; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage01_resequencing_mutationsFiltered" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name character varying(100) NOT NULL,
    mutation_id integer NOT NULL,
    parent_ids integer[],
    mutation_data json
);


ALTER TABLE public."data_stage01_resequencing_mutationsFiltered" OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 130980)
-- Name: data_stage01_resequencing_mutationsFiltered_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage01_resequencing_mutationsFiltered_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage01_resequencing_mutationsFiltered_id_seq" OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 130982)
-- Name: data_stage01_resequencing_mutations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_resequencing_mutations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_resequencing_mutations_id_seq OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 130984)
-- Name: data_stage01_resequencing_validation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage01_resequencing_validation (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name character varying(100) NOT NULL,
    validation_id integer NOT NULL,
    validation_data json
);


ALTER TABLE public.data_stage01_resequencing_validation OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 130990)
-- Name: data_stage01_resequencing_validation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage01_resequencing_validation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage01_resequencing_validation_id_seq OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 130992)
-- Name: data_stage02_isotopomer_atomMappingMetabolites; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_isotopomer_atomMappingMetabolites" (
    id integer NOT NULL,
    mapping_id character varying(100) NOT NULL,
    met_id character varying(50) NOT NULL,
    met_elements character varying(3)[],
    met_atompositions integer[],
    met_symmetry_elements character varying(3)[],
    met_symmetry_atompositions integer[],
    used_ boolean,
    comment_ text,
    met_mapping json,
    base_met_ids character varying(50)[],
    base_met_elements json,
    base_met_atompositions json,
    base_met_symmetry_elements json,
    base_met_symmetry_atompositions json,
    base_met_indices integer[]
);


ALTER TABLE public."data_stage02_isotopomer_atomMappingMetabolites" OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 130998)
-- Name: data_stage02_isotopomer_atomMappingMetabolites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_isotopomer_atomMappingMetabolites_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_isotopomer_atomMappingMetabolites_id_seq" OWNER TO postgres;

--
-- TOC entry 269 (class 1259 OID 131000)
-- Name: data_stage02_isotopomer_atomMappingReactions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_isotopomer_atomMappingReactions" (
    id integer NOT NULL,
    mapping_id character varying(100) NOT NULL,
    rxn_id character varying(50) NOT NULL,
    rxn_description character varying(500),
    reactants_stoichiometry_tracked double precision[],
    products_stoichiometry_tracked double precision[],
    reactants_ids_tracked character varying(50)[],
    products_ids_tracked character varying(50)[],
    reactants_mapping character varying(5000)[],
    products_mapping character varying(5000)[],
    rxn_equation character varying(4000),
    used_ boolean,
    comment_ text,
    reactants_elements_tracked json,
    products_elements_tracked json,
    reactants_positions_tracked json,
    products_positions_tracked json
);


ALTER TABLE public."data_stage02_isotopomer_atomMappingReactions" OWNER TO postgres;

--
-- TOC entry 270 (class 1259 OID 131006)
-- Name: data_stage02_isotopomer_atomMappingReactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_isotopomer_atomMappingReactions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_isotopomer_atomMappingReactions_id_seq" OWNER TO postgres;

--
-- TOC entry 271 (class 1259 OID 131008)
-- Name: data_stage02_isotopomer_calcFluxes; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_isotopomer_calcFluxes" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    mapping_id character varying(100) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    flux_average double precision,
    flux_stdev double precision,
    flux_lb double precision,
    flux_ub double precision,
    flux_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_isotopomer_calcFluxes" OWNER TO postgres;

--
-- TOC entry 272 (class 1259 OID 131014)
-- Name: data_stage02_isotopomer_calcFluxes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_isotopomer_calcFluxes_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_isotopomer_calcFluxes_id_seq" OWNER TO postgres;

--
-- TOC entry 273 (class 1259 OID 131016)
-- Name: data_stage02_isotopomer_calcFragments; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_isotopomer_calcFragments" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50),
    mapping_id character varying(100) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    met_id character varying(100),
    fragment_name character varying(100) NOT NULL,
    fragment_formula character varying(500),
    fragment_mass integer,
    idv_average double precision,
    idv_stdev double precision,
    idv_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_isotopomer_calcFragments" OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 131022)
-- Name: data_stage02_isotopomer_calcFragments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_isotopomer_calcFragments_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_isotopomer_calcFragments_id_seq" OWNER TO postgres;

--
-- TOC entry 275 (class 1259 OID 131024)
-- Name: data_stage02_isotopomer_measuredFluxes; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_isotopomer_measuredFluxes" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50),
    sample_name_abbreviation character varying(100) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    flux_average double precision,
    flux_stdev double precision,
    flux_lb double precision,
    flux_ub double precision,
    flux_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_isotopomer_measuredFluxes" OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 131030)
-- Name: data_stage02_isotopomer_measuredFluxes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_isotopomer_measuredFluxes_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_isotopomer_measuredFluxes_id_seq" OWNER TO postgres;

--
-- TOC entry 277 (class 1259 OID 131032)
-- Name: data_stage02_isotopomer_measuredFragments; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_isotopomer_measuredFragments" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    met_id character varying(100) NOT NULL,
    fragment_id character varying(100) NOT NULL,
    fragment_formula character varying(500) NOT NULL,
    intensity_normalized_average double precision[],
    intensity_normalized_cv double precision[],
    intensity_normalized_stdev double precision[],
    intensity_normalized_units character varying(20),
    scan_type character varying(50) NOT NULL,
    met_elements character varying(3)[],
    met_atompositions integer[],
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_isotopomer_measuredFragments" OWNER TO postgres;

--
-- TOC entry 278 (class 1259 OID 131038)
-- Name: data_stage02_isotopomer_measuredFragments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_isotopomer_measuredFragments_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_isotopomer_measuredFragments_id_seq" OWNER TO postgres;

--
-- TOC entry 279 (class 1259 OID 131040)
-- Name: data_stage02_isotopomer_measuredPools; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_isotopomer_measuredPools" (
    id integer NOT NULL,
    experiment_id character varying(50),
    model_id character varying(50),
    sample_name_abbreviation character varying(100),
    time_point character varying(10),
    met_id character varying(50),
    pool_size double precision,
    concentration_average double precision,
    concentration_var double precision,
    concentration_lb double precision,
    concentration_ub double precision,
    concentration_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_isotopomer_measuredPools" OWNER TO postgres;

--
-- TOC entry 280 (class 1259 OID 131046)
-- Name: data_stage02_isotopomer_measuredPools_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_isotopomer_measuredPools_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_isotopomer_measuredPools_id_seq" OWNER TO postgres;

--
-- TOC entry 281 (class 1259 OID 131048)
-- Name: data_stage02_isotopomer_modelMetabolites; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_isotopomer_modelMetabolites" (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    met_name character varying(500),
    met_id character varying(50) NOT NULL,
    formula character varying(100),
    charge integer,
    compartment character varying(50),
    bound double precision,
    constraint_sense character varying(5),
    used_ boolean,
    comment_ text,
    lower_bound double precision,
    upper_bound double precision,
    balanced boolean,
    fixed boolean
);


ALTER TABLE public."data_stage02_isotopomer_modelMetabolites" OWNER TO postgres;

--
-- TOC entry 282 (class 1259 OID 131054)
-- Name: data_stage02_isotopomer_modelMetabolites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_isotopomer_modelMetabolites_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_isotopomer_modelMetabolites_id_seq" OWNER TO postgres;

--
-- TOC entry 283 (class 1259 OID 131056)
-- Name: data_stage02_isotopomer_modelReactions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_isotopomer_modelReactions" (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    rxn_id character varying(50) NOT NULL,
    rxn_name character varying(100),
    equation character varying(4000),
    subsystem character varying(255),
    gpr text,
    genes character varying(50)[],
    reactants_stoichiometry double precision[],
    products_stoichiometry double precision[],
    reactants_ids character varying(50)[],
    products_ids character varying(50)[],
    lower_bound double precision,
    upper_bound double precision,
    objective_coefficient double precision,
    flux_units character varying(50),
    fixed boolean,
    free boolean,
    reversibility boolean,
    weight double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_isotopomer_modelReactions" OWNER TO postgres;

--
-- TOC entry 284 (class 1259 OID 131062)
-- Name: data_stage02_isotopomer_modelReactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_isotopomer_modelReactions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_isotopomer_modelReactions_id_seq" OWNER TO postgres;

--
-- TOC entry 285 (class 1259 OID 131064)
-- Name: data_stage02_isotopomer_models; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage02_isotopomer_models (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    model_name character varying(100),
    model_description character varying(100),
    model_file text,
    date timestamp without time zone,
    file_type character varying(50) DEFAULT 'sbml'::character varying
);


ALTER TABLE public.data_stage02_isotopomer_models OWNER TO postgres;

--
-- TOC entry 286 (class 1259 OID 131071)
-- Name: data_stage02_isotopomer_models_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_isotopomer_models_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_isotopomer_models_id_seq OWNER TO postgres;

--
-- TOC entry 287 (class 1259 OID 131073)
-- Name: data_stage02_isotopomer_simulation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage02_isotopomer_simulation (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    mapping_id character varying(100) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    used_ boolean,
    comment_ text,
    simulation_id character varying(500) NOT NULL
);


ALTER TABLE public.data_stage02_isotopomer_simulation OWNER TO postgres;

--
-- TOC entry 288 (class 1259 OID 131079)
-- Name: data_stage02_isotopomer_simulation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_isotopomer_simulation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_isotopomer_simulation_id_seq OWNER TO postgres;

--
-- TOC entry 289 (class 1259 OID 131081)
-- Name: data_stage02_isotopomer_substrates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_isotopomer_substrates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_isotopomer_substrates_id_seq OWNER TO postgres;

--
-- TOC entry 290 (class 1259 OID 131083)
-- Name: data_stage02_isotopomer_tracers; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage02_isotopomer_tracers (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    met_id character varying(50) NOT NULL,
    met_name character varying(100) NOT NULL,
    isotopomer_formula character varying(50)[],
    met_elements character varying(3)[],
    met_atompositions integer[],
    ratio double precision,
    supplier character varying(100),
    supplier_reference character varying(100),
    purity double precision,
    comment_ text
);


ALTER TABLE public.data_stage02_isotopomer_tracers OWNER TO postgres;

--
-- TOC entry 291 (class 1259 OID 131089)
-- Name: data_stage02_isotopomer_tracers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_isotopomer_tracers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_isotopomer_tracers_id_seq OWNER TO postgres;

--
-- TOC entry 292 (class 1259 OID 131091)
-- Name: data_stage02_physiology_measuredFluxes; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_physiology_measuredFluxes" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50),
    sample_name_abbreviation character varying(100) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    flux_average double precision,
    flux_stdev double precision,
    flux_lb double precision,
    flux_ub double precision,
    flux_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_physiology_measuredFluxes" OWNER TO postgres;

--
-- TOC entry 293 (class 1259 OID 131097)
-- Name: data_stage02_physiology_measuredFluxes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_physiology_measuredFluxes_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_physiology_measuredFluxes_id_seq" OWNER TO postgres;

--
-- TOC entry 294 (class 1259 OID 131099)
-- Name: data_stage02_physiology_modelMetabolites; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_physiology_modelMetabolites" (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    met_name character varying(500),
    met_id character varying(50) NOT NULL,
    formula character varying(100),
    charge integer,
    compartment character varying(50),
    bound double precision,
    constraint_sense character varying(5),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_physiology_modelMetabolites" OWNER TO postgres;

--
-- TOC entry 295 (class 1259 OID 131105)
-- Name: data_stage02_physiology_modelMetabolites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_physiology_modelMetabolites_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_physiology_modelMetabolites_id_seq" OWNER TO postgres;

--
-- TOC entry 296 (class 1259 OID 131107)
-- Name: data_stage02_physiology_modelReactions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_physiology_modelReactions" (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    rxn_id character varying(50) NOT NULL,
    rxn_name character varying(255),
    equation character varying(4000),
    subsystem character varying(255),
    gpr text,
    genes character varying(50)[],
    reactants_stoichiometry double precision[],
    products_stoichiometry double precision[],
    reactants_ids character varying(50)[],
    products_ids character varying(50)[],
    lower_bound double precision,
    upper_bound double precision,
    objective_coefficient double precision,
    flux_units character varying(50),
    reversibility boolean,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_physiology_modelReactions" OWNER TO postgres;

--
-- TOC entry 297 (class 1259 OID 131113)
-- Name: data_stage02_physiology_modelReactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_physiology_modelReactions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_physiology_modelReactions_id_seq" OWNER TO postgres;

--
-- TOC entry 298 (class 1259 OID 131115)
-- Name: data_stage02_physiology_models; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage02_physiology_models (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    model_name character varying(100),
    model_description character varying(100),
    model_file text,
    date timestamp without time zone,
    file_type character varying(50) DEFAULT 'sbml'::character varying
);


ALTER TABLE public.data_stage02_physiology_models OWNER TO postgres;

--
-- TOC entry 299 (class 1259 OID 131122)
-- Name: data_stage02_physiology_models_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_physiology_models_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_physiology_models_id_seq OWNER TO postgres;

--
-- TOC entry 300 (class 1259 OID 131124)
-- Name: data_stage02_physiology_sampledData; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_physiology_sampledData" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    flux_units character varying(50),
    sampling_ave double precision,
    sampling_var double precision,
    sampling_lb double precision,
    sampling_ub double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_physiology_sampledData" OWNER TO postgres;

--
-- TOC entry 301 (class 1259 OID 131130)
-- Name: data_stage02_physiology_sampledData_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_physiology_sampledData_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_physiology_sampledData_id_seq" OWNER TO postgres;

--
-- TOC entry 302 (class 1259 OID 131132)
-- Name: data_stage02_physiology_sampledPoints; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_physiology_sampledPoints" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    flux_units character varying(50),
    mixed_fraction double precision,
    sampling_points double precision[],
    data_dir character varying(500),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_physiology_sampledPoints" OWNER TO postgres;

--
-- TOC entry 303 (class 1259 OID 131138)
-- Name: data_stage02_physiology_sampledPoints_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_physiology_sampledPoints_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_physiology_sampledPoints_id_seq" OWNER TO postgres;

--
-- TOC entry 304 (class 1259 OID 131140)
-- Name: data_stage02_physiology_simulatedData; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_physiology_simulatedData" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    fba_flux double precision,
    fva_minimum double precision,
    fva_maximum double precision,
    flux_units character varying(50),
    sra_gr double precision,
    sra_gr_ratio double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_physiology_simulatedData" OWNER TO postgres;

--
-- TOC entry 305 (class 1259 OID 131146)
-- Name: data_stage02_physiology_simulatedData_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_physiology_simulatedData_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_physiology_simulatedData_id_seq" OWNER TO postgres;

--
-- TOC entry 306 (class 1259 OID 131148)
-- Name: data_stage02_physiology_simulation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage02_physiology_simulation (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage02_physiology_simulation OWNER TO postgres;

--
-- TOC entry 307 (class 1259 OID 131154)
-- Name: data_stage02_physiology_simulation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_physiology_simulation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_physiology_simulation_id_seq OWNER TO postgres;

--
-- TOC entry 308 (class 1259 OID 131156)
-- Name: data_stage02_quantification_anova; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage02_quantification_anova (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name_abbreviation character varying(100)[],
    time_point character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    test_stat double precision,
    test_description character varying(50),
    pvalue double precision,
    pvalue_corrected double precision,
    pvalue_corrected_description character varying(500),
    calculated_concentration_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage02_quantification_anova OWNER TO postgres;

--
-- TOC entry 309 (class 1259 OID 131162)
-- Name: data_stage02_quantification_anova_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_quantification_anova_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_quantification_anova_id_seq OWNER TO postgres;

--
-- TOC entry 310 (class 1259 OID 131164)
-- Name: data_stage02_quantification_descriptiveStats; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_quantification_descriptiveStats" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    test_stat double precision,
    test_description character varying(50),
    pvalue double precision,
    pvalue_corrected double precision,
    pvalue_corrected_description character varying(500),
    mean double precision,
    var double precision,
    cv double precision,
    n double precision,
    ci_lb double precision,
    ci_ub double precision,
    ci_level double precision,
    calculated_concentration_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_quantification_descriptiveStats" OWNER TO postgres;

--
-- TOC entry 311 (class 1259 OID 131170)
-- Name: data_stage02_quantification_descriptiveStats_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_quantification_descriptiveStats_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_quantification_descriptiveStats_id_seq" OWNER TO postgres;

--
-- TOC entry 312 (class 1259 OID 131172)
-- Name: data_stage02_quantification_glogNormalized; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_quantification_glogNormalized" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_short character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    calculated_concentration double precision,
    calculated_concentration_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_quantification_glogNormalized" OWNER TO postgres;

--
-- TOC entry 313 (class 1259 OID 131178)
-- Name: data_stage02_quantification_glogNormalized_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_quantification_glogNormalized_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_quantification_glogNormalized_id_seq" OWNER TO postgres;

--
-- TOC entry 314 (class 1259 OID 131180)
-- Name: data_stage02_quantification_pairWiseTest; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_quantification_pairWiseTest" (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name_abbreviation_1 character varying(100),
    sample_name_abbreviation_2 character varying(100),
    time_point_1 character varying(10) NOT NULL,
    time_point_2 character varying(10) NOT NULL,
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    test_stat double precision,
    test_description character varying(50),
    pvalue double precision,
    pvalue_corrected double precision,
    pvalue_corrected_description character varying(500),
    mean double precision,
    ci_lb double precision,
    ci_ub double precision,
    ci_level double precision,
    fold_change double precision,
    calculated_concentration_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_quantification_pairWiseTest" OWNER TO postgres;

--
-- TOC entry 315 (class 1259 OID 131186)
-- Name: data_stage02_quantification_pairWiseTest_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_quantification_pairWiseTest_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_quantification_pairWiseTest_id_seq" OWNER TO postgres;

--
-- TOC entry 316 (class 1259 OID 131188)
-- Name: data_stage02_quantification_pca_loadings; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage02_quantification_pca_loadings (
    id integer NOT NULL,
    experiment_id character varying(50),
    time_point character varying(10),
    component_group_name character varying(100),
    component_name character varying(500) NOT NULL,
    loadings double precision,
    axis integer,
    calculated_concentration_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage02_quantification_pca_loadings OWNER TO postgres;

--
-- TOC entry 317 (class 1259 OID 131194)
-- Name: data_stage02_quantification_pca_loadings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_quantification_pca_loadings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_quantification_pca_loadings_id_seq OWNER TO postgres;

--
-- TOC entry 318 (class 1259 OID 131196)
-- Name: data_stage02_quantification_pca_scores; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage02_quantification_pca_scores (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name_short character varying(100),
    time_point character varying(10),
    score double precision,
    axis integer,
    var_proportion double precision,
    var_cumulative double precision,
    calculated_concentration_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage02_quantification_pca_scores OWNER TO postgres;

--
-- TOC entry 319 (class 1259 OID 131202)
-- Name: data_stage02_quantification_pca_scores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_quantification_pca_scores_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_quantification_pca_scores_id_seq OWNER TO postgres;

--
-- TOC entry 320 (class 1259 OID 131204)
-- Name: data_stage02_quantification_volcano_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage02_quantification_volcano_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage02_quantification_volcano_id_seq OWNER TO postgres;

--
-- TOC entry 321 (class 1259 OID 131206)
-- Name: data_stage02_resequencing_mapResequencingPhysiology; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_resequencing_mapResequencingPhysiology" (
    id integer NOT NULL,
    experiment_id character varying(50),
    sample_name character varying(100),
    mutation_frequency double precision,
    mutation_type character varying(3),
    mutation_position integer,
    mutation_data json,
    mutation_annotations character varying(500)[],
    mutation_genes character varying(25)[],
    mutation_locations character varying(100)[],
    mutation_links character varying(500)[],
    sample_name_abbreviation character varying(100),
    met_id character varying(100),
    rate_average double precision,
    rate_var double precision,
    rate_lb double precision,
    rate_ub double precision,
    rate_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_resequencing_mapResequencingPhysiology" OWNER TO postgres;

--
-- TOC entry 322 (class 1259 OID 131212)
-- Name: data_stage02_resequencing_mapResequencingPhysiology_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_resequencing_mapResequencingPhysiology_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_resequencing_mapResequencingPhysiology_id_seq" OWNER TO postgres;

--
-- TOC entry 323 (class 1259 OID 131214)
-- Name: data_stage02_resequencing_reduceResequencingPhysiology; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage02_resequencing_reduceResequencingPhysiology" (
    id integer NOT NULL,
    experiment_id character varying(50),
    group_name character varying(100),
    sample_names character varying(100)[],
    sample_name_abbreviations character varying(100)[],
    resequencing_reduce_id character varying,
    physiology_reduce_id character varying,
    reduce_count integer,
    mutation_frequencies double precision[],
    mutation_types character varying(3)[],
    mutation_positions integer[],
    met_ids character varying(100)[],
    rate_averages double precision[],
    rate_vars double precision[],
    rate_lbs double precision[],
    rate_ubs double precision[],
    rate_units character varying(50)[],
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage02_resequencing_reduceResequencingPhysiology" OWNER TO postgres;

--
-- TOC entry 324 (class 1259 OID 131220)
-- Name: data_stage02_resequencing_reduceResequencingPhysiology_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage02_resequencing_reduceResequencingPhysiology_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage02_resequencing_reduceResequencingPhysiology_id_seq" OWNER TO postgres;

--
-- TOC entry 325 (class 1259 OID 131222)
-- Name: data_stage03_quantification_dG0_f; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_dG0_f" (
    id integer NOT NULL,
    reference_id character varying(100) NOT NULL,
    met_name character varying(500),
    met_id character varying(100),
    "KEGG_id" character varying(20) NOT NULL,
    priority integer NOT NULL,
    "dG0_f" double precision,
    "dG0_f_var" double precision,
    "dG0_f_units" character varying(50),
    temperature double precision,
    temperature_units character varying(50),
    ionic_strength double precision,
    ionic_strength_units character varying(50),
    "pH" double precision,
    "pH_units" character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_dG0_f" OWNER TO postgres;

--
-- TOC entry 326 (class 1259 OID 131228)
-- Name: data_stage03_quantification_dG0_f_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_dG0_f_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_dG0_f_id_seq" OWNER TO postgres;

--
-- TOC entry 327 (class 1259 OID 131230)
-- Name: data_stage03_quantification_dG0_p; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_dG0_p" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    pathway_id character varying(100) NOT NULL,
    "dG0_p" double precision,
    "dG0_p_var" double precision,
    "dG0_p_units" character varying(50),
    "dG0_p_lb" double precision,
    "dG0_p_ub" double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_dG0_p" OWNER TO postgres;

--
-- TOC entry 328 (class 1259 OID 131236)
-- Name: data_stage03_quantification_dG0_p_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_dG0_p_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_dG0_p_id_seq" OWNER TO postgres;

--
-- TOC entry 329 (class 1259 OID 131238)
-- Name: data_stage03_quantification_dG0_r; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_dG0_r" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    "Keq_lb" double precision,
    "Keq_ub" double precision,
    "dG0_r" double precision,
    "dG0_r_var" double precision,
    "dG0_r_units" character varying(50),
    "dG0_r_lb" double precision,
    "dG0_r_ub" double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_dG0_r" OWNER TO postgres;

--
-- TOC entry 330 (class 1259 OID 131244)
-- Name: data_stage03_quantification_dG0_r_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_dG0_r_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_dG0_r_id_seq" OWNER TO postgres;

--
-- TOC entry 331 (class 1259 OID 131246)
-- Name: data_stage03_quantification_dG_f; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_dG_f" (
    id integer NOT NULL,
    experiment_id character varying(100) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    met_name character varying(500),
    met_id character varying(100) NOT NULL,
    "dG_f" double precision,
    "dG_f_var" double precision,
    "dG_f_units" character varying(50),
    "dG_f_lb" double precision,
    "dG_f_ub" double precision,
    temperature double precision,
    temperature_units character varying(50),
    ionic_strength double precision,
    ionic_strength_units character varying(50),
    "pH" double precision,
    "pH_units" character varying(50),
    measured boolean,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_dG_f" OWNER TO postgres;

--
-- TOC entry 332 (class 1259 OID 131252)
-- Name: data_stage03_quantification_dG_f_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_dG_f_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_dG_f_id_seq" OWNER TO postgres;

--
-- TOC entry 333 (class 1259 OID 131254)
-- Name: data_stage03_quantification_dG_p; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_dG_p" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    pathway_id character varying(100) NOT NULL,
    "dG_p" double precision,
    "dG_p_var" double precision,
    "dG_p_units" character varying(50),
    "dG_p_lb" double precision,
    "dG_p_ub" double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_dG_p" OWNER TO postgres;

--
-- TOC entry 334 (class 1259 OID 131260)
-- Name: data_stage03_quantification_dG_p_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_dG_p_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_dG_p_id_seq" OWNER TO postgres;

--
-- TOC entry 335 (class 1259 OID 131262)
-- Name: data_stage03_quantification_dG_r; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_dG_r" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    "Keq_lb" double precision,
    "Keq_ub" double precision,
    "dG_r" double precision,
    "dG_r_var" double precision,
    "dG_r_units" character varying(50),
    "dG_r_lb" double precision,
    "dG_r_ub" double precision,
    displacement_lb double precision,
    displacement_ub double precision,
    "Q_lb" double precision,
    "Q_ub" double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_dG_r" OWNER TO postgres;

--
-- TOC entry 336 (class 1259 OID 131268)
-- Name: data_stage03_quantification_dG_r_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_dG_r_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_dG_r_id_seq" OWNER TO postgres;

--
-- TOC entry 337 (class 1259 OID 131270)
-- Name: data_stage03_quantification_metabolomicsData; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_metabolomicsData" (
    id integer NOT NULL,
    experiment_id character varying(100) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    met_id character varying(100) NOT NULL,
    concentration double precision,
    concentration_var double precision,
    concentration_units character varying(50),
    concentration_lb double precision,
    concentration_ub double precision,
    measured boolean,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_metabolomicsData" OWNER TO postgres;

--
-- TOC entry 338 (class 1259 OID 131276)
-- Name: data_stage03_quantification_metabolomicsData_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_metabolomicsData_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_metabolomicsData_id_seq" OWNER TO postgres;

--
-- TOC entry 339 (class 1259 OID 131278)
-- Name: data_stage03_quantification_metid2keggid; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage03_quantification_metid2keggid (
    id integer NOT NULL,
    met_id character varying(100),
    "KEGG_id" character varying(20) NOT NULL,
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage03_quantification_metid2keggid OWNER TO postgres;

--
-- TOC entry 340 (class 1259 OID 131284)
-- Name: data_stage03_quantification_metid2keggid_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage03_quantification_metid2keggid_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage03_quantification_metid2keggid_id_seq OWNER TO postgres;

--
-- TOC entry 341 (class 1259 OID 131286)
-- Name: data_stage03_quantification_modelMetabolites; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_modelMetabolites" (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    met_name character varying(500),
    met_id character varying(50) NOT NULL,
    formula character varying(100),
    charge integer,
    compartment character varying(50),
    bound double precision,
    constraint_sense character varying(5),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_modelMetabolites" OWNER TO postgres;

--
-- TOC entry 342 (class 1259 OID 131292)
-- Name: data_stage03_quantification_modelMetabolites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_modelMetabolites_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_modelMetabolites_id_seq" OWNER TO postgres;

--
-- TOC entry 343 (class 1259 OID 131294)
-- Name: data_stage03_quantification_modelPathways; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_modelPathways" (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    pathway_id character varying(100) NOT NULL,
    reactions character varying(100)[],
    stoichiometry double precision[],
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_modelPathways" OWNER TO postgres;

--
-- TOC entry 344 (class 1259 OID 131300)
-- Name: data_stage03_quantification_modelPathways_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_modelPathways_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_modelPathways_id_seq" OWNER TO postgres;

--
-- TOC entry 345 (class 1259 OID 131302)
-- Name: data_stage03_quantification_modelReactions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_modelReactions" (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    rxn_id character varying(50) NOT NULL,
    rxn_name character varying(255),
    equation character varying(4000),
    subsystem character varying(255),
    gpr text,
    genes character varying(50)[],
    reactants_stoichiometry double precision[],
    products_stoichiometry double precision[],
    reactants_ids character varying(50)[],
    products_ids character varying(50)[],
    lower_bound double precision,
    upper_bound double precision,
    objective_coefficient double precision,
    flux_units character varying(50),
    reversibility boolean,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_modelReactions" OWNER TO postgres;

--
-- TOC entry 346 (class 1259 OID 131308)
-- Name: data_stage03_quantification_modelReactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_modelReactions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_modelReactions_id_seq" OWNER TO postgres;

--
-- TOC entry 347 (class 1259 OID 131310)
-- Name: data_stage03_quantification_models; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage03_quantification_models (
    id integer NOT NULL,
    model_id character varying(50) NOT NULL,
    model_name character varying(100),
    model_description character varying(100),
    sbml_file text,
    date timestamp without time zone
);


ALTER TABLE public.data_stage03_quantification_models OWNER TO postgres;

--
-- TOC entry 348 (class 1259 OID 131316)
-- Name: data_stage03_quantification_models_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage03_quantification_models_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage03_quantification_models_id_seq OWNER TO postgres;

--
-- TOC entry 349 (class 1259 OID 131318)
-- Name: data_stage03_quantification_otherData; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_otherData" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    compartment_id character varying(25) NOT NULL,
    "pH" double precision,
    temperature double precision,
    temperature_units character varying(50),
    ionic_strength double precision,
    ionic_strength_units character varying(50),
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_otherData" OWNER TO postgres;

--
-- TOC entry 350 (class 1259 OID 131324)
-- Name: data_stage03_quantification_otherData_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_otherData_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_otherData_id_seq" OWNER TO postgres;

--
-- TOC entry 351 (class 1259 OID 131326)
-- Name: data_stage03_quantification_simulatedData; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "data_stage03_quantification_simulatedData" (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    fba_flux double precision,
    fva_minimum double precision,
    fva_maximum double precision,
    flux_units character varying(50),
    sra_gr double precision,
    sra_gr_ratio double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public."data_stage03_quantification_simulatedData" OWNER TO postgres;

--
-- TOC entry 352 (class 1259 OID 131332)
-- Name: data_stage03_quantification_simulatedData_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "data_stage03_quantification_simulatedData_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."data_stage03_quantification_simulatedData_id_seq" OWNER TO postgres;

--
-- TOC entry 353 (class 1259 OID 131334)
-- Name: data_stage03_quantification_simulation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage03_quantification_simulation (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage03_quantification_simulation OWNER TO postgres;

--
-- TOC entry 354 (class 1259 OID 131340)
-- Name: data_stage03_quantification_simulation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage03_quantification_simulation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage03_quantification_simulation_id_seq OWNER TO postgres;

--
-- TOC entry 355 (class 1259 OID 131342)
-- Name: data_stage03_quantification_tcc; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_stage03_quantification_tcc (
    id integer NOT NULL,
    experiment_id character varying(50) NOT NULL,
    model_id character varying(50) NOT NULL,
    sample_name_abbreviation character varying(100) NOT NULL,
    time_point character varying(10) NOT NULL,
    rxn_id character varying(100) NOT NULL,
    feasible boolean,
    measured_concentration_coverage_criteria double precision,
    "measured_dG_f_coverage_criteria" double precision,
    measured_concentration_coverage double precision,
    "measured_dG_f_coverage" double precision,
    used_ boolean,
    comment_ text
);


ALTER TABLE public.data_stage03_quantification_tcc OWNER TO postgres;

--
-- TOC entry 356 (class 1259 OID 131348)
-- Name: data_stage03_quantification_tcc_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE data_stage03_quantification_tcc_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_stage03_quantification_tcc_id_seq OWNER TO postgres;

--
-- TOC entry 357 (class 1259 OID 131350)
-- Name: data_versions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE data_versions (
    experiment_id character varying(50) NOT NULL,
    sample_name character varying(500) NOT NULL,
    component_name character varying(500) NOT NULL,
    acquisition_date_and_time timestamp without time zone NOT NULL,
    concentration_before double precision,
    concentration_after double precision,
    concentration_units_before character varying(20),
    concentration_units_after character varying(20),
    used_before boolean,
    used_after boolean,
    data_stage_before integer,
    data_stage_after integer,
    data_stage_modtime timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.data_versions OWNER TO postgres;

--
-- TOC entry 358 (class 1259 OID 131357)
-- Name: wids; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE wids
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wids OWNER TO postgres;

--
-- TOC entry 359 (class 1259 OID 131359)
-- Name: experiment; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE experiment (
    wid integer DEFAULT nextval('wids'::regclass) NOT NULL,
    exp_type_id integer NOT NULL,
    id character varying(50) NOT NULL,
    sample_name character varying(500) NOT NULL,
    experimentor_id character varying(50),
    extraction_method_id character varying(50),
    acquisition_method_id character varying(50),
    quantitation_method_id character varying(50),
    internal_standard_id integer
);


ALTER TABLE public.experiment OWNER TO postgres;

--
-- TOC entry 360 (class 1259 OID 131366)
-- Name: experiment_types; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE experiment_types (
    id integer NOT NULL,
    experiment_name character varying(100)
);


ALTER TABLE public.experiment_types OWNER TO postgres;

--
-- TOC entry 361 (class 1259 OID 131369)
-- Name: experimentor; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE experimentor (
    experimentor_name character varying(100) NOT NULL,
    contact_information character varying(100)
);


ALTER TABLE public.experimentor OWNER TO postgres;

--
-- TOC entry 362 (class 1259 OID 131372)
-- Name: experimentor_id2name; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE experimentor_id2name (
    experimentor_id character varying(50) NOT NULL,
    experimentor_name character varying(100) NOT NULL,
    experimentor_role character varying(500) NOT NULL
);


ALTER TABLE public.experimentor_id2name OWNER TO postgres;

--
-- TOC entry 363 (class 1259 OID 131378)
-- Name: experimentor_list; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE experimentor_list (
    experimentor_id character varying(50) NOT NULL
);


ALTER TABLE public.experimentor_list OWNER TO postgres;

--
-- TOC entry 364 (class 1259 OID 131381)
-- Name: extraction_method; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE extraction_method (
    id character varying(500) NOT NULL,
    extraction_method_reference character varying(100) NOT NULL,
    notes text NOT NULL
);


ALTER TABLE public.extraction_method OWNER TO postgres;

--
-- TOC entry 365 (class 1259 OID 131387)
-- Name: internal_standard; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE internal_standard (
    is_id integer NOT NULL,
    is_date timestamp without time zone NOT NULL,
    experimentor_id character varying(50) NOT NULL,
    extraction_method_id character varying(50)
);


ALTER TABLE public.internal_standard OWNER TO postgres;

--
-- TOC entry 366 (class 1259 OID 131390)
-- Name: internal_standard_storage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE internal_standard_storage (
    is_id integer NOT NULL,
    concentration double precision,
    concentration_units character varying(10),
    aliquots integer,
    aliquot_volume double precision,
    aliquot_volume_units character varying(10),
    solvent character varying(100),
    ph double precision,
    box integer,
    posstart integer,
    posend integer
);


ALTER TABLE public.internal_standard_storage OWNER TO postgres;

--
-- TOC entry 367 (class 1259 OID 131393)
-- Name: lc_elution; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE lc_elution (
    lc_method_id character varying(50) NOT NULL,
    met_id character varying(50) NOT NULL,
    rt double precision DEFAULT 0,
    ms_window double precision DEFAULT 60,
    rt_units character varying(20),
    window_units character varying(20)
);


ALTER TABLE public.lc_elution OWNER TO postgres;

--
-- TOC entry 368 (class 1259 OID 131398)
-- Name: lc_gradient; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE lc_gradient (
    id character varying(50) NOT NULL,
    lc_event integer[] NOT NULL,
    lc_time double precision[] NOT NULL,
    percent_b double precision[] NOT NULL,
    flow_rate double precision[] NOT NULL,
    lc_time_units character varying(25) NOT NULL,
    flow_rate_units character varying(25) NOT NULL
);


ALTER TABLE public.lc_gradient OWNER TO postgres;

--
-- TOC entry 369 (class 1259 OID 131404)
-- Name: lc_information; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE lc_information (
    manufacturer character varying(100) NOT NULL,
    id character varying(100) NOT NULL,
    serial_number character varying(100) NOT NULL
);


ALTER TABLE public.lc_information OWNER TO postgres;

--
-- TOC entry 370 (class 1259 OID 131407)
-- Name: lc_method; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE lc_method (
    id character varying(50) NOT NULL,
    lc_information_id character varying(100) NOT NULL,
    lc_gradient_id character varying(50) NOT NULL,
    lc_parameters_id character varying(50) NOT NULL
);


ALTER TABLE public.lc_method OWNER TO postgres;

--
-- TOC entry 371 (class 1259 OID 131410)
-- Name: lc_parameters; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE lc_parameters (
    id character varying(50) NOT NULL,
    column_name character varying(100) NOT NULL,
    dimensions_and_particle_size character varying(100) NOT NULL,
    mobile_phase_a character varying(100) NOT NULL,
    mobile_phase_b character varying(100) NOT NULL,
    oven_temperature character varying(100) NOT NULL,
    notes text
);


ALTER TABLE public.lc_parameters OWNER TO postgres;

--
-- TOC entry 372 (class 1259 OID 131416)
-- Name: metabolomics_physiologicalratio2met; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE metabolomics_physiologicalratio2met (
    physiologicalratio_id character varying(50) NOT NULL,
    met_id character varying(50) NOT NULL
);


ALTER TABLE public.metabolomics_physiologicalratio2met OWNER TO postgres;

--
-- TOC entry 373 (class 1259 OID 131419)
-- Name: metabolomics_physiologicalratios; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE metabolomics_physiologicalratios (
    physiologicalratio_id character varying(50) NOT NULL,
    physiologicalratio_name character varying(100),
    physiologicalratio_description character varying(100),
    formula character varying(500),
    literature_value_lower double precision[],
    literature_value_upper double precision[],
    literature_references character varying(500)[]
);


ALTER TABLE public.metabolomics_physiologicalratios OWNER TO postgres;

--
-- TOC entry 374 (class 1259 OID 131425)
-- Name: mix2met_id; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE mix2met_id (
    mix_id character varying(25) NOT NULL,
    met_id character varying(50) NOT NULL,
    met_name character varying(500) NOT NULL
);


ALTER TABLE public.mix2met_id OWNER TO postgres;

--
-- TOC entry 375 (class 1259 OID 131431)
-- Name: mix_calculations; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE mix_calculations (
    mix_id character varying(25) NOT NULL,
    number_of_compounds integer,
    total_volume_actual double precision,
    aliquot_volume double precision,
    add_to_make_aliquot_volume_even double precision,
    corrected_aliquot_volume double precision,
    volume_units character varying(25)
);


ALTER TABLE public.mix_calculations OWNER TO postgres;

--
-- TOC entry 376 (class 1259 OID 131434)
-- Name: mix_description; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE mix_description (
    mix_id character varying(25) NOT NULL,
    mix_description text NOT NULL
);


ALTER TABLE public.mix_description OWNER TO postgres;

--
-- TOC entry 377 (class 1259 OID 131440)
-- Name: mix_parameters; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE mix_parameters (
    mix_id character varying(25) NOT NULL,
    number_of_aliquots double precision NOT NULL,
    mix_volume double precision NOT NULL,
    number_of_aliquiots integer NOT NULL
);


ALTER TABLE public.mix_parameters OWNER TO postgres;

--
-- TOC entry 378 (class 1259 OID 131443)
-- Name: mix_storage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE mix_storage (
    mix_id character varying(25) NOT NULL,
    mixdate date,
    box integer[],
    posstart integer[],
    posend integer[]
);


ALTER TABLE public.mix_storage OWNER TO postgres;

--
-- TOC entry 379 (class 1259 OID 131449)
-- Name: ms_component_list; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE ms_component_list (
    ms_method_id character varying(50) NOT NULL,
    q1_mass double precision,
    q3_mass double precision,
    met_id character varying(50),
    component_name character varying(500) NOT NULL,
    ms_methodtype character varying(20) DEFAULT 'quantification'::character varying
);


ALTER TABLE public.ms_component_list OWNER TO postgres;

--
-- TOC entry 380 (class 1259 OID 131456)
-- Name: ms_components_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ms_components_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ms_components_id_seq OWNER TO postgres;

--
-- TOC entry 381 (class 1259 OID 131458)
-- Name: ms_components; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE ms_components (
    q1_mass double precision NOT NULL,
    q3_mass double precision NOT NULL,
    ms3_mass double precision,
    met_name text,
    dp double precision,
    ep double precision,
    ce double precision,
    cxp double precision,
    af double precision,
    quantifier integer,
    ms_mode character(1),
    ion_intensity_rank integer,
    ion_abundance double precision,
    precursor_formula text,
    product_ion_reference text,
    product_formula text,
    production_ion_notes text,
    met_id character varying(50) NOT NULL,
    external_reference text,
    q1_mass_units character varying(20),
    q3_mass_units character varying(20),
    ms3_mass_units character varying(20),
    threshold_units character varying(20),
    dp_units character varying(20),
    ep_units character varying(20),
    ce_units character varying(20),
    cxp_units character varying(20),
    af_units character varying(20),
    ms_group character varying(100),
    threshold double precision DEFAULT 5000,
    dwell_weight double precision DEFAULT 1,
    component_name character varying(500),
    ms_include boolean DEFAULT false,
    ms_is boolean DEFAULT false,
    precursor_fragment boolean[],
    product_fragment boolean[],
    precursor_exactmass double precision,
    product_exactmass double precision,
    ms_methodtype character varying(20) DEFAULT 'tuning'::character varying NOT NULL,
    id integer DEFAULT nextval('ms_components_id_seq'::regclass),
    precursor_fragment_elements character varying(3)[] DEFAULT NULL::character varying[],
    product_fragment_elements character varying(3)[] DEFAULT NULL::character varying[]
);


ALTER TABLE public.ms_components OWNER TO postgres;

--
-- TOC entry 382 (class 1259 OID 131472)
-- Name: mrm_acquisitionmethod; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW mrm_acquisitionmethod AS
 SELECT ms_component_list.component_name AS ms_component_name, 
    ms_components.met_id, 
    ms_components.met_name, 
    ms_components.q1_mass, 
    ms_components.q3_mass, 
    ms_components.dp, 
    ms_components.ep, 
    ms_components.ce, 
    ms_components.cxp, 
    ms_components.precursor_formula, 
    ms_components.product_formula, 
    ms_components.quantifier, 
    ms_components.ms_group, 
    ms_components.threshold, 
    ms_components.dwell_weight, 
    ms_components.component_name, 
    ms_components.dp_units, 
    ms_components.ep_units, 
    ms_components.ce_units, 
    ms_components.cxp_units, 
    lc_elution.rt, 
    lc_elution.ms_window, 
    lc_elution.rt_units, 
    lc_elution.window_units
   FROM lc_elution, 
    ms_components, 
    ms_component_list
  WHERE (((((ms_component_list.ms_method_id)::text ~~ '%_McCloskey2013'::text) AND ((ms_component_list.component_name)::text ~~ (ms_components.component_name)::text)) AND ((lc_elution.lc_method_id)::text ~~ 'McCloskey2013'::text)) AND ((ms_components.met_id)::text ~~ (lc_elution.met_id)::text));


ALTER TABLE public.mrm_acquisitionmethod OWNER TO postgres;

--
-- TOC entry 383 (class 1259 OID 131477)
-- Name: ms_information; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE ms_information (
    manufacturer character varying(100) NOT NULL,
    id character varying(100) NOT NULL,
    serial_number character varying(100) NOT NULL
);


ALTER TABLE public.ms_information OWNER TO postgres;

--
-- TOC entry 384 (class 1259 OID 131480)
-- Name: ms_method; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE ms_method (
    id character varying(50) NOT NULL,
    ms_sourceparameters_id character varying(50) NOT NULL,
    ms_information_id character varying(50) NOT NULL,
    ms_experiment_id character varying(50)
);


ALTER TABLE public.ms_method OWNER TO postgres;

--
-- TOC entry 385 (class 1259 OID 131483)
-- Name: ms_sourceparameters; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE ms_sourceparameters (
    id character varying(50) NOT NULL,
    ms_cur double precision NOT NULL,
    ms_cad character varying(10) NOT NULL,
    ms_is double precision NOT NULL,
    ms_tem double precision NOT NULL,
    ms_gs1 double precision NOT NULL,
    ms_gs2 double precision NOT NULL
);


ALTER TABLE public.ms_sourceparameters OWNER TO postgres;

--
-- TOC entry 386 (class 1259 OID 131486)
-- Name: oligos_description; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE oligos_description (
    oligos_id character varying(100) NOT NULL,
    oligos_sequence text,
    oligos_purification character varying(100),
    oligos_description text,
    oligos_notes text
);


ALTER TABLE public.oligos_description OWNER TO postgres;

--
-- TOC entry 387 (class 1259 OID 131492)
-- Name: oligos_storage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE oligos_storage (
    oligos_id character varying(100) NOT NULL,
    oligos_label character varying(100),
    oligos_box integer,
    oligos_posstart integer,
    oligos_posend integer,
    oligos_date timestamp without time zone,
    oligos_storagebuffer character varying(100),
    oligos_concentration double precision,
    oligos_concentration_units character varying(20)
);


ALTER TABLE public.oligos_storage OWNER TO postgres;

--
-- TOC entry 388 (class 1259 OID 131495)
-- Name: quantitation_method; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE quantitation_method (
    id character varying(50) NOT NULL,
    q1_mass double precision,
    q3_mass double precision,
    met_id character varying(50),
    component_name character varying(100) NOT NULL,
    is_name character varying(100) DEFAULT NULL::character varying,
    fit character varying(20),
    weighting character varying(20),
    intercept double precision,
    slope double precision,
    correlation double precision,
    use_area boolean DEFAULT false,
    lloq double precision,
    uloq double precision,
    points integer
);


ALTER TABLE public.quantitation_method OWNER TO postgres;

--
-- TOC entry 389 (class 1259 OID 131500)
-- Name: quantitation_method_list; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE quantitation_method_list (
    quantitation_method_id character varying(50) NOT NULL
);


ALTER TABLE public.quantitation_method_list OWNER TO postgres;

--
-- TOC entry 390 (class 1259 OID 131503)
-- Name: sample; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sample (
    sample_name character varying(500) NOT NULL,
    sample_type character varying(100) NOT NULL,
    calibrator_id integer,
    calibrator_level integer,
    sample_id character varying(500),
    sample_dilution double precision DEFAULT 1
);


ALTER TABLE public.sample OWNER TO postgres;

--
-- TOC entry 391 (class 1259 OID 131510)
-- Name: sample_description; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sample_description (
    sample_id character varying(500) NOT NULL,
    sample_name_short character varying(100),
    sample_name_abbreviation character varying(50),
    sample_date timestamp without time zone NOT NULL,
    time_point character varying(50) NOT NULL,
    sample_condition character varying(100) NOT NULL,
    extraction_method_id character varying(500),
    biological_material character varying(100),
    sample_description character varying(100) NOT NULL,
    sample_replicate integer,
    is_added double precision,
    is_added_units character varying(10),
    reconstitution_volume double precision,
    reconstitution_volume_units character varying(10),
    istechnical boolean,
    sample_replicate_biological integer,
    notes text
);


ALTER TABLE public.sample_description OWNER TO postgres;

--
-- TOC entry 392 (class 1259 OID 131516)
-- Name: sample_massvolumeconversion; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sample_massvolumeconversion (
    biological_material character varying(100) NOT NULL,
    conversion_name character varying(50) NOT NULL,
    conversion_factor double precision,
    conversion_units character varying(50) NOT NULL,
    conversion_reference character varying(500) NOT NULL
);


ALTER TABLE public.sample_massvolumeconversion OWNER TO postgres;

--
-- TOC entry 393 (class 1259 OID 131522)
-- Name: sample_physiologicalparameters; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sample_physiologicalparameters (
    sample_id character varying(500) NOT NULL,
    growth_condition_short text,
    growth_condition_long text,
    media_short text,
    media_long text,
    isoxic boolean,
    temperature double precision,
    supplementation character varying(100),
    od600 double precision,
    vcd double precision,
    culture_density double precision,
    culture_volume_sampled double precision,
    cells double precision,
    dcw double precision,
    wcw double precision,
    vcd_units character varying(10),
    culture_density_units character varying(10),
    culture_volume_sampled_units character varying(10),
    dcw_units character varying(10),
    wcw_units character varying(10)
);


ALTER TABLE public.sample_physiologicalparameters OWNER TO postgres;

--
-- TOC entry 394 (class 1259 OID 131528)
-- Name: sample_storage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sample_storage (
    sample_id character varying(500) NOT NULL,
    sample_label character varying(50) NOT NULL,
    ph double precision,
    box integer,
    pos integer
);


ALTER TABLE public.sample_storage OWNER TO postgres;

--
-- TOC entry 395 (class 1259 OID 131534)
-- Name: standards; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE standards (
    met_id character varying(50) NOT NULL,
    met_name character varying(500) NOT NULL,
    formula character varying(100),
    hmdb character varying(500),
    solubility double precision,
    solubility_units character varying(10),
    mass double precision,
    cas_number character varying(100),
    keggid character varying(100),
    structure_file text,
    structure_file_extention character varying(10),
    exactmass double precision
);


ALTER TABLE public.standards OWNER TO postgres;

--
-- TOC entry 396 (class 1259 OID 131540)
-- Name: standards2material; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE standards2material (
    met_id character varying(50) NOT NULL,
    provider character varying(100) NOT NULL,
    provider_reference character varying(100) NOT NULL
);


ALTER TABLE public.standards2material OWNER TO postgres;

--
-- TOC entry 397 (class 1259 OID 131543)
-- Name: standards_ordering; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE standards_ordering (
    met_id character varying(50) NOT NULL,
    met_name character varying(100) NOT NULL,
    hillcrest boolean,
    provider character varying(100) NOT NULL,
    provider_reference character varying(100) NOT NULL,
    price double precision,
    amount double precision,
    amount_units character varying(10),
    purity double precision,
    mw double precision,
    notes character varying(500),
    powderdate_received date,
    powderdate_opened date,
    order_standard boolean,
    standards_storage double precision,
    purchase boolean
);


ALTER TABLE public.standards_ordering OWNER TO postgres;

--
-- TOC entry 398 (class 1259 OID 131549)
-- Name: standards_storage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE standards_storage (
    met_id character varying(50) NOT NULL,
    met_name character varying(500) NOT NULL,
    provider character varying(100) NOT NULL,
    provider_reference character varying(50) NOT NULL,
    powderdate date,
    stockdate date NOT NULL,
    concentration double precision,
    concentration_units character varying(10),
    aliquots integer,
    solvent character varying(100),
    ph double precision,
    box integer,
    posstart integer,
    posend integer
);


ALTER TABLE public.standards_storage OWNER TO postgres;

--
-- TOC entry 2661 (class 2604 OID 131555)
-- Name: fragment_mass; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY data_stage01_isotopomer_averages ALTER COLUMN fragment_mass SET DEFAULT nextval('data_stage01_isotopomer_averages_fragment_mass_seq'::regclass);


--
-- TOC entry 2662 (class 2604 OID 131556)
-- Name: fragment_mass; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "data_stage01_isotopomer_averagesNormSum" ALTER COLUMN fragment_mass SET DEFAULT nextval('"data_stage01_isotopomer_averagesNormSum_fragment_mass_seq"'::regclass);


--
-- TOC entry 2693 (class 2606 OID 131584)
-- Name: acquisition_method_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acquisition_method
    ADD CONSTRAINT acquisition_method_pkey PRIMARY KEY (id);


--
-- TOC entry 2695 (class 2606 OID 131586)
-- Name: autosampler_information_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY autosampler_information
    ADD CONSTRAINT autosampler_information_pkey PRIMARY KEY (id);


--
-- TOC entry 2697 (class 2606 OID 131588)
-- Name: autosampler_method_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY autosampler_method
    ADD CONSTRAINT autosampler_method_pkey PRIMARY KEY (id);


--
-- TOC entry 2699 (class 2606 OID 131590)
-- Name: autosampler_parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY autosampler_parameters
    ADD CONSTRAINT autosampler_parameters_pkey PRIMARY KEY (id);


--
-- TOC entry 2701 (class 2606 OID 131592)
-- Name: biologicalmaterial_description_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY biologicalmaterial_description
    ADD CONSTRAINT biologicalmaterial_description_pkey PRIMARY KEY (biologicalmaterial_id);


--
-- TOC entry 2703 (class 2606 OID 131594)
-- Name: biologicalmaterial_genereferences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY biologicalmaterial_genereferences
    ADD CONSTRAINT biologicalmaterial_genereferences_pkey PRIMARY KEY (id);


--
-- TOC entry 2705 (class 2606 OID 131596)
-- Name: biologicalmaterial_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY biologicalmaterial_storage
    ADD CONSTRAINT biologicalmaterial_storage_pkey PRIMARY KEY (biologicalmaterial_id);


--
-- TOC entry 2711 (class 2606 OID 131598)
-- Name: calibrator2mix_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY calibrator2mix
    ADD CONSTRAINT calibrator2mix_pkey PRIMARY KEY (mix_id);


--
-- TOC entry 2713 (class 2606 OID 131600)
-- Name: calibrator_calculations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY calibrator_calculations
    ADD CONSTRAINT calibrator_calculations_pkey PRIMARY KEY (met_id);


--
-- TOC entry 2715 (class 2606 OID 131602)
-- Name: calibrator_concentrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY calibrator_concentrations
    ADD CONSTRAINT calibrator_concentrations_pkey PRIMARY KEY (met_id, calibrator_level);


--
-- TOC entry 2717 (class 2606 OID 131604)
-- Name: calibrator_levels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY calibrator_levels
    ADD CONSTRAINT calibrator_levels_pkey PRIMARY KEY (calibrator_level);


--
-- TOC entry 2719 (class 2606 OID 131606)
-- Name: calibrator_met2mix_calculations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY calibrator_met2mix_calculations
    ADD CONSTRAINT calibrator_met2mix_calculations_pkey PRIMARY KEY (met_id);


--
-- TOC entry 2707 (class 2606 OID 131608)
-- Name: calibrator_met_id_stockdate_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY calibrator
    ADD CONSTRAINT calibrator_met_id_stockdate_key UNIQUE (met_id, stockdate);


--
-- TOC entry 2721 (class 2606 OID 131610)
-- Name: calibrator_met_parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY calibrator_met_parameters
    ADD CONSTRAINT calibrator_met_parameters_pkey PRIMARY KEY (met_id);


--
-- TOC entry 2709 (class 2606 OID 131612)
-- Name: calibrator_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY calibrator
    ADD CONSTRAINT calibrator_pkey PRIMARY KEY (met_id);


--
-- TOC entry 2751 (class 2606 OID 131614)
-- Name: data_stage01_LLOQAndULOQ_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_LLOQAndULOQ"
    ADD CONSTRAINT "data_stage01_LLOQAndULOQ_pkey" PRIMARY KEY (experiment_id, sample_name, component_name);


--
-- TOC entry 2753 (class 2606 OID 131616)
-- Name: data_stage01_QCs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_QCs"
    ADD CONSTRAINT "data_stage01_QCs_pkey" PRIMARY KEY (experiment_id, sample_name_abbreviation, sample_dilution, component_name);


--
-- TOC entry 2723 (class 2606 OID 131618)
-- Name: data_stage01_ale_jumps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_ale_jumps
    ADD CONSTRAINT data_stage01_ale_jumps_pkey PRIMARY KEY (id, experiment_id);


--
-- TOC entry 2725 (class 2606 OID 131620)
-- Name: data_stage01_ale_trajectories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_ale_trajectories
    ADD CONSTRAINT data_stage01_ale_trajectories_pkey PRIMARY KEY (id, experiment_id);


--
-- TOC entry 2755 (class 2606 OID 131622)
-- Name: data_stage01_averages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_quantification_averages
    ADD CONSTRAINT data_stage01_averages_pkey PRIMARY KEY (experiment_id, sample_name_abbreviation, time_point, component_name);


--
-- TOC entry 2757 (class 2606 OID 131624)
-- Name: data_stage01_averagesmi_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_quantification_averagesmi
    ADD CONSTRAINT data_stage01_averagesmi_pkey PRIMARY KEY (experiment_id, sample_name_abbreviation, time_point, component_name);


--
-- TOC entry 2759 (class 2606 OID 131626)
-- Name: data_stage01_averagesmigeo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_quantification_averagesmigeo
    ADD CONSTRAINT data_stage01_averagesmigeo_pkey PRIMARY KEY (experiment_id, sample_name_abbreviation, time_point, component_name);


--
-- TOC entry 2761 (class 2606 OID 131628)
-- Name: data_stage01_checkCVAndExtracellular_averages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_checkCVAndExtracellular_averages"
    ADD CONSTRAINT "data_stage01_checkCVAndExtracellular_averages_pkey" PRIMARY KEY (experiment_id, sample_name_abbreviation, time_point, component_name);


--
-- TOC entry 2763 (class 2606 OID 131630)
-- Name: data_stage01_checkCV_QCs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_checkCV_QCs"
    ADD CONSTRAINT "data_stage01_checkCV_QCs_pkey" PRIMARY KEY (experiment_id, "sample_Name_Abbreviation", sample_dilution, component_name);


--
-- TOC entry 2765 (class 2606 OID 131632)
-- Name: data_stage01_checkCV_dilutions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_checkCV_dilutions"
    ADD CONSTRAINT "data_stage01_checkCV_dilutions_pkey" PRIMARY KEY (experiment_id, sample_id, component_name);


--
-- TOC entry 2767 (class 2606 OID 131634)
-- Name: data_stage01_checkISMatch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_checkISMatch"
    ADD CONSTRAINT "data_stage01_checkISMatch_pkey" PRIMARY KEY (experiment_id, sample_name, component_name);


--
-- TOC entry 2769 (class 2606 OID 131636)
-- Name: data_stage01_checkLLOQAndULOQ_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_checkLLOQAndULOQ"
    ADD CONSTRAINT "data_stage01_checkLLOQAndULOQ_pkey" PRIMARY KEY (experiment_id, sample_name, component_name);


--
-- TOC entry 2771 (class 2606 OID 131638)
-- Name: data_stage01_dilutions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_quantification_dilutions
    ADD CONSTRAINT data_stage01_dilutions_pkey PRIMARY KEY (experiment_id, sample_id, component_name);


--
-- TOC entry 2729 (class 2606 OID 131640)
-- Name: data_stage01_isotopomer_averagesNormSum_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_isotopomer_averagesNormSum"
    ADD CONSTRAINT "data_stage01_isotopomer_averagesNormSum_pkey" PRIMARY KEY (experiment_id, sample_name_abbreviation, sample_type, time_point, met_id, fragment_formula, fragment_mass, scan_type);


--
-- TOC entry 2727 (class 2606 OID 131642)
-- Name: data_stage01_isotopomer_averages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_isotopomer_averages
    ADD CONSTRAINT data_stage01_isotopomer_averages_pkey PRIMARY KEY (experiment_id, sample_name_abbreviation, sample_type, time_point, met_id, fragment_formula, fragment_mass, scan_type);


--
-- TOC entry 2731 (class 2606 OID 131644)
-- Name: data_stage01_isotopomer_mqresultstable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_isotopomer_mqresultstable
    ADD CONSTRAINT data_stage01_isotopomer_mqresultstable_pkey PRIMARY KEY (sample_name, component_name, acquisition_date_and_time);


--
-- TOC entry 2733 (class 2606 OID 131646)
-- Name: data_stage01_isotopomer_normalized_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_isotopomer_normalized
    ADD CONSTRAINT data_stage01_isotopomer_normalized_pkey PRIMARY KEY (id);


--
-- TOC entry 2735 (class 2606 OID 131648)
-- Name: data_stage01_isotopomer_peakData_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_isotopomer_peakData"
    ADD CONSTRAINT "data_stage01_isotopomer_peakData_pkey" PRIMARY KEY (id);


--
-- TOC entry 2737 (class 2606 OID 131650)
-- Name: data_stage01_isotopomer_peakList_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_isotopomer_peakList"
    ADD CONSTRAINT "data_stage01_isotopomer_peakList_pkey" PRIMARY KEY (id);


--
-- TOC entry 2739 (class 2606 OID 131652)
-- Name: data_stage01_isotopomer_peakSpectrum_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_isotopomer_peakSpectrum"
    ADD CONSTRAINT "data_stage01_isotopomer_peakSpectrum_pkey" PRIMARY KEY (id);


--
-- TOC entry 2743 (class 2606 OID 131654)
-- Name: data_stage01_isotopomer_spectrumAccuracyNormSum_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_isotopomer_spectrumAccuracyNormSum"
    ADD CONSTRAINT "data_stage01_isotopomer_spectrumAccuracyNormSum_pkey" PRIMARY KEY (experiment_id, sample_name_abbreviation, sample_type, time_point, met_id, fragment_formula, scan_type);


--
-- TOC entry 2741 (class 2606 OID 131656)
-- Name: data_stage01_isotopomer_spectrumAccuracy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_isotopomer_spectrumAccuracy"
    ADD CONSTRAINT "data_stage01_isotopomer_spectrumAccuracy_pkey" PRIMARY KEY (experiment_id, sample_name_abbreviation, sample_type, time_point, met_id, fragment_formula, scan_type);


--
-- TOC entry 2773 (class 2606 OID 131658)
-- Name: data_stage01_mqresultstable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_quantification_mqresultstable
    ADD CONSTRAINT data_stage01_mqresultstable_pkey PRIMARY KEY (sample_name, component_name, acquisition_date_and_time);


--
-- TOC entry 2775 (class 2606 OID 131725)
-- Name: data_stage01_normalized_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_quantification_normalized
    ADD CONSTRAINT data_stage01_normalized_pkey PRIMARY KEY (id);


--
-- TOC entry 2745 (class 2606 OID 131727)
-- Name: data_stage01_physiology_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_physiology_data
    ADD CONSTRAINT data_stage01_physiology_data_pkey PRIMARY KEY (id, experiment_id, sample_id, met_id, data_reference);


--
-- TOC entry 2749 (class 2606 OID 131729)
-- Name: data_stage01_physiology_ratesAverages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_physiology_ratesAverages"
    ADD CONSTRAINT "data_stage01_physiology_ratesAverages_pkey" PRIMARY KEY (id, experiment_id, met_id);


--
-- TOC entry 2747 (class 2606 OID 131731)
-- Name: data_stage01_physiology_rates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_physiology_rates
    ADD CONSTRAINT data_stage01_physiology_rates_pkey PRIMARY KEY (id, experiment_id, sample_name_short, met_id);


--
-- TOC entry 2777 (class 2606 OID 131733)
-- Name: data_stage01_quantification_peakInformation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_peakInformation"
    ADD CONSTRAINT "data_stage01_quantification_peakInformation_pkey" PRIMARY KEY (id);


--
-- TOC entry 2779 (class 2606 OID 131735)
-- Name: data_stage01_quantification_peakResolution_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_peakResolution"
    ADD CONSTRAINT "data_stage01_quantification_peakResolution_pkey" PRIMARY KEY (id);


--
-- TOC entry 2781 (class 2606 OID 131737)
-- Name: data_stage01_quantification_physiologicalRatios_averages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_physiologicalRatios_averages"
    ADD CONSTRAINT "data_stage01_quantification_physiologicalRatios_averages_pkey" PRIMARY KEY (id, experiment_id, sample_name_abbreviation, time_point, physiologicalratio_id);


--
-- TOC entry 2783 (class 2606 OID 131740)
-- Name: data_stage01_quantification_physiologicalRatios_replicates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_quantification_physiologicalRatios_replicates"
    ADD CONSTRAINT "data_stage01_quantification_physiologicalRatios_replicates_pkey" PRIMARY KEY (id, experiment_id, sample_name_short, time_point, physiologicalratio_id);


--
-- TOC entry 2785 (class 2606 OID 131745)
-- Name: data_stage01_replicates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_quantification_replicates
    ADD CONSTRAINT data_stage01_replicates_pkey PRIMARY KEY (experiment_id, sample_name_short, time_point, component_name);


--
-- TOC entry 2787 (class 2606 OID 131753)
-- Name: data_stage01_replicatesmi_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_quantification_replicatesmi
    ADD CONSTRAINT data_stage01_replicatesmi_pkey PRIMARY KEY (experiment_id, sample_name_short, time_point, component_name);


--
-- TOC entry 2789 (class 2606 OID 131755)
-- Name: data_stage01_resequencing_endpoints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_resequencing_endpoints
    ADD CONSTRAINT data_stage01_resequencing_endpoints_pkey PRIMARY KEY (id);


--
-- TOC entry 2791 (class 2606 OID 131757)
-- Name: data_stage01_resequencing_evidence_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_resequencing_evidence
    ADD CONSTRAINT data_stage01_resequencing_evidence_pkey PRIMARY KEY (id, experiment_id, sample_name, parent_id);


--
-- TOC entry 2793 (class 2606 OID 131759)
-- Name: data_stage01_resequencing_lineage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_resequencing_lineage
    ADD CONSTRAINT data_stage01_resequencing_lineage_pkey PRIMARY KEY (id);


--
-- TOC entry 2795 (class 2606 OID 131761)
-- Name: data_stage01_resequencing_metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_resequencing_metadata
    ADD CONSTRAINT data_stage01_resequencing_metadata_pkey PRIMARY KEY (id);


--
-- TOC entry 2797 (class 2606 OID 131763)
-- Name: data_stage01_resequencing_metadata_sample_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_resequencing_metadata
    ADD CONSTRAINT data_stage01_resequencing_metadata_sample_name_key UNIQUE (sample_name);


--
-- TOC entry 2801 (class 2606 OID 131765)
-- Name: data_stage01_resequencing_mutationsAnnotated_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_resequencing_mutationsAnnotated"
    ADD CONSTRAINT "data_stage01_resequencing_mutationsAnnotated_pkey" PRIMARY KEY (id);


--
-- TOC entry 2803 (class 2606 OID 131767)
-- Name: data_stage01_resequencing_mutationsFiltered_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage01_resequencing_mutationsFiltered"
    ADD CONSTRAINT "data_stage01_resequencing_mutationsFiltered_pkey" PRIMARY KEY (id, experiment_id, sample_name, mutation_id);


--
-- TOC entry 2799 (class 2606 OID 131769)
-- Name: data_stage01_resequencing_mutations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_resequencing_mutations
    ADD CONSTRAINT data_stage01_resequencing_mutations_pkey PRIMARY KEY (id, experiment_id, sample_name, mutation_id);


--
-- TOC entry 2805 (class 2606 OID 131771)
-- Name: data_stage01_resequencing_validation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage01_resequencing_validation
    ADD CONSTRAINT data_stage01_resequencing_validation_pkey PRIMARY KEY (id, experiment_id, sample_name, validation_id);


--
-- TOC entry 2807 (class 2606 OID 131773)
-- Name: data_stage02_isotopomer_atomMappingMetabolites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_atomMappingMetabolites"
    ADD CONSTRAINT "data_stage02_isotopomer_atomMappingMetabolites_pkey" PRIMARY KEY (id);


--
-- TOC entry 2809 (class 2606 OID 131775)
-- Name: data_stage02_isotopomer_atomMapping_pkey1; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_atomMappingReactions"
    ADD CONSTRAINT "data_stage02_isotopomer_atomMapping_pkey1" PRIMARY KEY (id);


--
-- TOC entry 2811 (class 2606 OID 131777)
-- Name: data_stage02_isotopomer_calcFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_calcFluxes"
    ADD CONSTRAINT "data_stage02_isotopomer_calcFluxes_pkey" PRIMARY KEY (id);


--
-- TOC entry 2813 (class 2606 OID 131779)
-- Name: data_stage02_isotopomer_calcFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_calcFragments"
    ADD CONSTRAINT "data_stage02_isotopomer_calcFragments_pkey" PRIMARY KEY (id);


--
-- TOC entry 2815 (class 2606 OID 131781)
-- Name: data_stage02_isotopomer_experimentalFluxes_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_measuredFluxes"
    ADD CONSTRAINT "data_stage02_isotopomer_experimentalFluxes_key" UNIQUE (experiment_id, model_id, sample_name_abbreviation, rxn_id);


--
-- TOC entry 2817 (class 2606 OID 131783)
-- Name: data_stage02_isotopomer_measuredFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_measuredFluxes"
    ADD CONSTRAINT "data_stage02_isotopomer_measuredFluxes_pkey" PRIMARY KEY (id);


--
-- TOC entry 2819 (class 2606 OID 131785)
-- Name: data_stage02_isotopomer_measuredFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_measuredFragments"
    ADD CONSTRAINT "data_stage02_isotopomer_measuredFragments_pkey" PRIMARY KEY (id);


--
-- TOC entry 2821 (class 2606 OID 131787)
-- Name: data_stage02_isotopomer_measuredPools_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_measuredPools"
    ADD CONSTRAINT "data_stage02_isotopomer_measuredPools_pkey" PRIMARY KEY (id);


--
-- TOC entry 2823 (class 2606 OID 131789)
-- Name: data_stage02_isotopomer_modelMetabolites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_modelMetabolites"
    ADD CONSTRAINT "data_stage02_isotopomer_modelMetabolites_pkey" PRIMARY KEY (id);


--
-- TOC entry 2825 (class 2606 OID 131791)
-- Name: data_stage02_isotopomer_modelReactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_isotopomer_modelReactions"
    ADD CONSTRAINT "data_stage02_isotopomer_modelReactions_pkey" PRIMARY KEY (id);


--
-- TOC entry 2827 (class 2606 OID 131793)
-- Name: data_stage02_isotopomer_models_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage02_isotopomer_models
    ADD CONSTRAINT data_stage02_isotopomer_models_key UNIQUE (model_id);


--
-- TOC entry 2829 (class 2606 OID 131795)
-- Name: data_stage02_isotopomer_models_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage02_isotopomer_models
    ADD CONSTRAINT data_stage02_isotopomer_models_pkey PRIMARY KEY (id);


--
-- TOC entry 2831 (class 2606 OID 131797)
-- Name: data_stage02_isotopomer_simulation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage02_isotopomer_simulation
    ADD CONSTRAINT data_stage02_isotopomer_simulation_pkey PRIMARY KEY (id);


--
-- TOC entry 2833 (class 2606 OID 131799)
-- Name: data_stage02_isotopomer_tracers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage02_isotopomer_tracers
    ADD CONSTRAINT data_stage02_isotopomer_tracers_pkey PRIMARY KEY (id);


--
-- TOC entry 2835 (class 2606 OID 131801)
-- Name: data_stage02_physiology_experimentalFluxes_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_physiology_measuredFluxes"
    ADD CONSTRAINT "data_stage02_physiology_experimentalFluxes_key" UNIQUE (experiment_id, sample_name_abbreviation, rxn_id);


--
-- TOC entry 2837 (class 2606 OID 131803)
-- Name: data_stage02_physiology_measuredFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_physiology_measuredFluxes"
    ADD CONSTRAINT "data_stage02_physiology_measuredFluxes_pkey" PRIMARY KEY (id);


--
-- TOC entry 2839 (class 2606 OID 131805)
-- Name: data_stage02_physiology_modelMetabolites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_physiology_modelMetabolites"
    ADD CONSTRAINT "data_stage02_physiology_modelMetabolites_pkey" PRIMARY KEY (id, model_id, met_id);


--
-- TOC entry 2841 (class 2606 OID 131807)
-- Name: data_stage02_physiology_modelReactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_physiology_modelReactions"
    ADD CONSTRAINT "data_stage02_physiology_modelReactions_pkey" PRIMARY KEY (id, model_id, rxn_id);


--
-- TOC entry 2843 (class 2606 OID 131809)
-- Name: data_stage02_physiology_models_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage02_physiology_models
    ADD CONSTRAINT data_stage02_physiology_models_pkey PRIMARY KEY (id, model_id);


--
-- TOC entry 2845 (class 2606 OID 131811)
-- Name: data_stage02_physiology_sampledData_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_physiology_sampledData"
    ADD CONSTRAINT "data_stage02_physiology_sampledData_pkey" PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, rxn_id);


--
-- TOC entry 2847 (class 2606 OID 131813)
-- Name: data_stage02_physiology_sampledPoints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_physiology_sampledPoints"
    ADD CONSTRAINT "data_stage02_physiology_sampledPoints_pkey" PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, rxn_id);


--
-- TOC entry 2849 (class 2606 OID 131815)
-- Name: data_stage02_physiology_simulatedData_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_physiology_simulatedData"
    ADD CONSTRAINT "data_stage02_physiology_simulatedData_pkey" PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, rxn_id);


--
-- TOC entry 2851 (class 2606 OID 131817)
-- Name: data_stage02_physiology_simulation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage02_physiology_simulation
    ADD CONSTRAINT data_stage02_physiology_simulation_pkey PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation);


--
-- TOC entry 2853 (class 2606 OID 131819)
-- Name: data_stage02_quantification_anova_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage02_quantification_anova
    ADD CONSTRAINT data_stage02_quantification_anova_pkey PRIMARY KEY (id, time_point, component_name);


--
-- TOC entry 2855 (class 2606 OID 131821)
-- Name: data_stage02_quantification_descriptiveStats_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_quantification_descriptiveStats"
    ADD CONSTRAINT "data_stage02_quantification_descriptiveStats_pkey" PRIMARY KEY (id, experiment_id, sample_name_abbreviation, time_point, component_name);


--
-- TOC entry 2857 (class 2606 OID 131823)
-- Name: data_stage02_quantification_glogNormalized_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_quantification_glogNormalized"
    ADD CONSTRAINT "data_stage02_quantification_glogNormalized_pkey" PRIMARY KEY (id, experiment_id, sample_name_short, time_point, component_name);


--
-- TOC entry 2859 (class 2606 OID 131825)
-- Name: data_stage02_quantification_pairWiseTest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_quantification_pairWiseTest"
    ADD CONSTRAINT "data_stage02_quantification_pairWiseTest_pkey" PRIMARY KEY (id, time_point_1, time_point_2, component_name);


--
-- TOC entry 2861 (class 2606 OID 131827)
-- Name: data_stage02_quantification_pca_loadings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage02_quantification_pca_loadings
    ADD CONSTRAINT data_stage02_quantification_pca_loadings_pkey PRIMARY KEY (id, component_name);


--
-- TOC entry 2863 (class 2606 OID 131829)
-- Name: data_stage02_quantification_pca_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage02_quantification_pca_scores
    ADD CONSTRAINT data_stage02_quantification_pca_scores_pkey PRIMARY KEY (id);


--
-- TOC entry 2865 (class 2606 OID 131831)
-- Name: data_stage02_resequencing_mapResequencingPhysiology_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_resequencing_mapResequencingPhysiology"
    ADD CONSTRAINT "data_stage02_resequencing_mapResequencingPhysiology_pkey" PRIMARY KEY (id);


--
-- TOC entry 2867 (class 2606 OID 131833)
-- Name: data_stage02_resequencing_reduceResequencingPhysiology_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage02_resequencing_reduceResequencingPhysiology"
    ADD CONSTRAINT "data_stage02_resequencing_reduceResequencingPhysiology_pkey" PRIMARY KEY (id);


--
-- TOC entry 2869 (class 2606 OID 131835)
-- Name: data_stage03_quantification_dG0_f_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_dG0_f"
    ADD CONSTRAINT "data_stage03_quantification_dG0_f_pkey" PRIMARY KEY (id, reference_id, "KEGG_id", priority);


--
-- TOC entry 2871 (class 2606 OID 131837)
-- Name: data_stage03_quantification_dG0_p_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_dG0_p"
    ADD CONSTRAINT "data_stage03_quantification_dG0_p_pkey" PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, time_point, pathway_id);


--
-- TOC entry 2873 (class 2606 OID 131839)
-- Name: data_stage03_quantification_dG0_r_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_dG0_r"
    ADD CONSTRAINT "data_stage03_quantification_dG0_r_pkey" PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, time_point, rxn_id);


--
-- TOC entry 2875 (class 2606 OID 131841)
-- Name: data_stage03_quantification_dG_f_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_dG_f"
    ADD CONSTRAINT "data_stage03_quantification_dG_f_pkey" PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, time_point, met_id);


--
-- TOC entry 2877 (class 2606 OID 131843)
-- Name: data_stage03_quantification_dG_p_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_dG_p"
    ADD CONSTRAINT "data_stage03_quantification_dG_p_pkey" PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, time_point, pathway_id);


--
-- TOC entry 2879 (class 2606 OID 131845)
-- Name: data_stage03_quantification_dG_r_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_dG_r"
    ADD CONSTRAINT "data_stage03_quantification_dG_r_pkey" PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, time_point, rxn_id);


--
-- TOC entry 2881 (class 2606 OID 131847)
-- Name: data_stage03_quantification_metabolomicsData_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_metabolomicsData"
    ADD CONSTRAINT "data_stage03_quantification_metabolomicsData_pkey" PRIMARY KEY (id, experiment_id, sample_name_abbreviation, time_point, met_id);


--
-- TOC entry 2883 (class 2606 OID 131850)
-- Name: data_stage03_quantification_metid2keggid_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage03_quantification_metid2keggid
    ADD CONSTRAINT data_stage03_quantification_metid2keggid_pkey PRIMARY KEY (id, "KEGG_id");


--
-- TOC entry 2885 (class 2606 OID 131854)
-- Name: data_stage03_quantification_modelMetabolites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_modelMetabolites"
    ADD CONSTRAINT "data_stage03_quantification_modelMetabolites_pkey" PRIMARY KEY (id, model_id, met_id);


--
-- TOC entry 2887 (class 2606 OID 131856)
-- Name: data_stage03_quantification_modelPathways_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_modelPathways"
    ADD CONSTRAINT "data_stage03_quantification_modelPathways_pkey" PRIMARY KEY (id, model_id, pathway_id);


--
-- TOC entry 2889 (class 2606 OID 131869)
-- Name: data_stage03_quantification_modelReactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_modelReactions"
    ADD CONSTRAINT "data_stage03_quantification_modelReactions_pkey" PRIMARY KEY (id, model_id, rxn_id);


--
-- TOC entry 2891 (class 2606 OID 131871)
-- Name: data_stage03_quantification_models_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage03_quantification_models
    ADD CONSTRAINT data_stage03_quantification_models_pkey PRIMARY KEY (id, model_id);


--
-- TOC entry 2893 (class 2606 OID 131873)
-- Name: data_stage03_quantification_simulatedData_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "data_stage03_quantification_simulatedData"
    ADD CONSTRAINT "data_stage03_quantification_simulatedData_pkey" PRIMARY KEY (id, experiment_id, model_id, rxn_id);


--
-- TOC entry 2895 (class 2606 OID 131875)
-- Name: data_stage03_quantification_simulation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage03_quantification_simulation
    ADD CONSTRAINT data_stage03_quantification_simulation_pkey PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, time_point);


--
-- TOC entry 2897 (class 2606 OID 131877)
-- Name: data_stage03_quantification_tcc_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_stage03_quantification_tcc
    ADD CONSTRAINT data_stage03_quantification_tcc_pkey PRIMARY KEY (id, experiment_id, model_id, sample_name_abbreviation, time_point, rxn_id);


--
-- TOC entry 2899 (class 2606 OID 131879)
-- Name: data_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY data_versions
    ADD CONSTRAINT data_versions_pkey PRIMARY KEY (experiment_id, sample_name, component_name, data_stage_modtime);


--
-- TOC entry 2901 (class 2606 OID 131881)
-- Name: experiment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_pkey PRIMARY KEY (id, sample_name);


--
-- TOC entry 2903 (class 2606 OID 131883)
-- Name: experiment_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY experiment_types
    ADD CONSTRAINT experiment_types_pkey PRIMARY KEY (id);


--
-- TOC entry 2907 (class 2606 OID 131885)
-- Name: experimentor_id2name_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY experimentor_id2name
    ADD CONSTRAINT experimentor_id2name_pkey PRIMARY KEY (experimentor_id, experimentor_name, experimentor_role);


--
-- TOC entry 2909 (class 2606 OID 131887)
-- Name: experimentor_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY experimentor_list
    ADD CONSTRAINT experimentor_list_pkey PRIMARY KEY (experimentor_id);


--
-- TOC entry 2905 (class 2606 OID 131889)
-- Name: experimentor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY experimentor
    ADD CONSTRAINT experimentor_pkey PRIMARY KEY (experimentor_name);


--
-- TOC entry 2911 (class 2606 OID 131892)
-- Name: extraction_method_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY extraction_method
    ADD CONSTRAINT extraction_method_pkey PRIMARY KEY (id);


--
-- TOC entry 2915 (class 2606 OID 131894)
-- Name: internal_standard_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY internal_standard_storage
    ADD CONSTRAINT internal_standard_storage_pkey PRIMARY KEY (is_id);


--
-- TOC entry 2913 (class 2606 OID 131896)
-- Name: is_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY internal_standard
    ADD CONSTRAINT is_id_pkey PRIMARY KEY (is_id);


--
-- TOC entry 2917 (class 2606 OID 131898)
-- Name: lc_elution_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY lc_elution
    ADD CONSTRAINT lc_elution_pkey PRIMARY KEY (lc_method_id, met_id);


--
-- TOC entry 2919 (class 2606 OID 131900)
-- Name: lc_gradient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY lc_gradient
    ADD CONSTRAINT lc_gradient_pkey PRIMARY KEY (id);


--
-- TOC entry 2921 (class 2606 OID 131902)
-- Name: lc_information_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY lc_information
    ADD CONSTRAINT lc_information_pkey PRIMARY KEY (id);


--
-- TOC entry 2923 (class 2606 OID 131904)
-- Name: lc_method_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY lc_method
    ADD CONSTRAINT lc_method_pkey PRIMARY KEY (id);


--
-- TOC entry 2925 (class 2606 OID 131906)
-- Name: lc_parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY lc_parameters
    ADD CONSTRAINT lc_parameters_pkey PRIMARY KEY (id);


--
-- TOC entry 2929 (class 2606 OID 131908)
-- Name: metabolomics_physiologicalratios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY metabolomics_physiologicalratios
    ADD CONSTRAINT metabolomics_physiologicalratios_pkey PRIMARY KEY (physiologicalratio_id);


--
-- TOC entry 2931 (class 2606 OID 131910)
-- Name: mix2met_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY mix2met_id
    ADD CONSTRAINT mix2met_id_pkey PRIMARY KEY (met_id, mix_id);


--
-- TOC entry 2933 (class 2606 OID 131912)
-- Name: mix_calculations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY mix_calculations
    ADD CONSTRAINT mix_calculations_pkey PRIMARY KEY (mix_id);


--
-- TOC entry 2935 (class 2606 OID 131914)
-- Name: mix_description_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY mix_description
    ADD CONSTRAINT mix_description_pkey PRIMARY KEY (mix_id);


--
-- TOC entry 2937 (class 2606 OID 131917)
-- Name: mix_parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY mix_parameters
    ADD CONSTRAINT mix_parameters_pkey PRIMARY KEY (mix_id);


--
-- TOC entry 2939 (class 2606 OID 131919)
-- Name: mix_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY mix_storage
    ADD CONSTRAINT mix_storage_pkey PRIMARY KEY (mix_id);


--
-- TOC entry 2941 (class 2606 OID 131921)
-- Name: ms_component_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY ms_component_list
    ADD CONSTRAINT ms_component_list_pkey PRIMARY KEY (ms_method_id, component_name);


--
-- TOC entry 2943 (class 2606 OID 131923)
-- Name: ms_components_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY ms_components
    ADD CONSTRAINT ms_components_key UNIQUE (component_name, ms_include);


--
-- TOC entry 2945 (class 2606 OID 131925)
-- Name: ms_components_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY ms_components
    ADD CONSTRAINT ms_components_pkey PRIMARY KEY (met_id, q1_mass, q3_mass, ms_methodtype);


--
-- TOC entry 2947 (class 2606 OID 131927)
-- Name: ms_information_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY ms_information
    ADD CONSTRAINT ms_information_pkey PRIMARY KEY (id);


--
-- TOC entry 2949 (class 2606 OID 131929)
-- Name: ms_method_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY ms_method
    ADD CONSTRAINT ms_method_pkey PRIMARY KEY (id);


--
-- TOC entry 2951 (class 2606 OID 131931)
-- Name: ms_sourceparameters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY ms_sourceparameters
    ADD CONSTRAINT ms_sourceparameters_pkey PRIMARY KEY (id);


--
-- TOC entry 2953 (class 2606 OID 131933)
-- Name: oligos_description_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY oligos_description
    ADD CONSTRAINT oligos_description_pkey PRIMARY KEY (oligos_id);


--
-- TOC entry 2955 (class 2606 OID 131935)
-- Name: oligos_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY oligos_storage
    ADD CONSTRAINT oligos_storage_pkey PRIMARY KEY (oligos_id);


--
-- TOC entry 2927 (class 2606 OID 131937)
-- Name: physiologicalratio2met_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY metabolomics_physiologicalratio2met
    ADD CONSTRAINT physiologicalratio2met_pkey PRIMARY KEY (physiologicalratio_id, met_id);


--
-- TOC entry 2959 (class 2606 OID 131939)
-- Name: quantitation_method_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY quantitation_method_list
    ADD CONSTRAINT quantitation_method_list_pkey PRIMARY KEY (quantitation_method_id);


--
-- TOC entry 2957 (class 2606 OID 131941)
-- Name: quantitation_method_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY quantitation_method
    ADD CONSTRAINT quantitation_method_pkey PRIMARY KEY (id, component_name);


--
-- TOC entry 2963 (class 2606 OID 131943)
-- Name: sample_description_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sample_description
    ADD CONSTRAINT sample_description_pkey PRIMARY KEY (sample_id);


--
-- TOC entry 2965 (class 2606 OID 131945)
-- Name: sample_massvolumeconversion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sample_massvolumeconversion
    ADD CONSTRAINT sample_massvolumeconversion_pkey PRIMARY KEY (biological_material, conversion_name);


--
-- TOC entry 2967 (class 2606 OID 131947)
-- Name: sample_physiologicalparameters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sample_physiologicalparameters
    ADD CONSTRAINT sample_physiologicalparameters_pkey PRIMARY KEY (sample_id);


--
-- TOC entry 2961 (class 2606 OID 131950)
-- Name: sample_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sample
    ADD CONSTRAINT sample_pkey PRIMARY KEY (sample_name);


--
-- TOC entry 2969 (class 2606 OID 131952)
-- Name: sample_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sample_storage
    ADD CONSTRAINT sample_storage_pkey PRIMARY KEY (sample_id);


--
-- TOC entry 2973 (class 2606 OID 131954)
-- Name: standards2material_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY standards2material
    ADD CONSTRAINT standards2material_pkey PRIMARY KEY (met_id, provider, provider_reference);


--
-- TOC entry 2975 (class 2606 OID 131956)
-- Name: standards_ordering_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY standards_ordering
    ADD CONSTRAINT standards_ordering_pkey PRIMARY KEY (met_id, provider, provider_reference);


--
-- TOC entry 2971 (class 2606 OID 131958)
-- Name: standards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY standards
    ADD CONSTRAINT standards_pkey PRIMARY KEY (met_id);


--
-- TOC entry 2977 (class 2606 OID 131960)
-- Name: standards_storage_met_id_stockdate_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY standards_storage
    ADD CONSTRAINT standards_storage_met_id_stockdate_key UNIQUE (met_id, stockdate);


--
-- TOC entry 2979 (class 2606 OID 131962)
-- Name: standards_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY standards_storage
    ADD CONSTRAINT standards_storage_pkey PRIMARY KEY (met_id, provider, provider_reference, stockdate);


--
-- TOC entry 2980 (class 2606 OID 131963)
-- Name: acquisition_method_autosampler_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acquisition_method
    ADD CONSTRAINT acquisition_method_autosampler_method_id_fkey FOREIGN KEY (autosampler_method_id) REFERENCES autosampler_method(id) ON UPDATE CASCADE;


--
-- TOC entry 2981 (class 2606 OID 131968)
-- Name: acquisition_method_lc_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acquisition_method
    ADD CONSTRAINT acquisition_method_lc_method_id_fkey FOREIGN KEY (lc_method_id) REFERENCES lc_method(id) ON UPDATE CASCADE;


--
-- TOC entry 2982 (class 2606 OID 131973)
-- Name: acquisition_method_ms_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY acquisition_method
    ADD CONSTRAINT acquisition_method_ms_method_id_fkey FOREIGN KEY (ms_method_id) REFERENCES ms_method(id) ON UPDATE CASCADE;


--
-- TOC entry 2983 (class 2606 OID 131978)
-- Name: autosampler_method_autosampler_information_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY autosampler_method
    ADD CONSTRAINT autosampler_method_autosampler_information_id_fkey FOREIGN KEY (autosampler_information_id) REFERENCES autosampler_information(id) ON UPDATE CASCADE;


--
-- TOC entry 2984 (class 2606 OID 131983)
-- Name: autosampler_method_autosampler_parameters_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY autosampler_method
    ADD CONSTRAINT autosampler_method_autosampler_parameters_id_fkey FOREIGN KEY (autosampler_parameters_id) REFERENCES autosampler_parameters(id) ON UPDATE CASCADE;


--
-- TOC entry 2986 (class 2606 OID 131988)
-- Name: calibrator_calculations_met_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY calibrator_calculations
    ADD CONSTRAINT calibrator_calculations_met_id_fkey FOREIGN KEY (met_id) REFERENCES calibrator(met_id);


--
-- TOC entry 2987 (class 2606 OID 131993)
-- Name: calibrator_met2mix_calculations_met_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY calibrator_met2mix_calculations
    ADD CONSTRAINT calibrator_met2mix_calculations_met_id_fkey FOREIGN KEY (met_id) REFERENCES calibrator_met_parameters(met_id);


--
-- TOC entry 2988 (class 2606 OID 131998)
-- Name: calibrator_met2mix_calculations_met_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY calibrator_met2mix_calculations
    ADD CONSTRAINT calibrator_met2mix_calculations_met_id_fkey1 FOREIGN KEY (met_id) REFERENCES calibrator_calculations(met_id);


--
-- TOC entry 2989 (class 2606 OID 132003)
-- Name: calibrator_met2mix_calculations_mix_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY calibrator_met2mix_calculations
    ADD CONSTRAINT calibrator_met2mix_calculations_mix_id_fkey FOREIGN KEY (mix_id) REFERENCES mix_calculations(mix_id);


--
-- TOC entry 2990 (class 2606 OID 132008)
-- Name: calibrator_met2mix_calculations_mix_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY calibrator_met2mix_calculations
    ADD CONSTRAINT calibrator_met2mix_calculations_mix_id_fkey1 FOREIGN KEY (mix_id) REFERENCES mix_parameters(mix_id);


--
-- TOC entry 2985 (class 2606 OID 132013)
-- Name: calibrator_met_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY calibrator
    ADD CONSTRAINT calibrator_met_id_fkey FOREIGN KEY (met_id, stockdate) REFERENCES standards_storage(met_id, stockdate);


--
-- TOC entry 2991 (class 2606 OID 132018)
-- Name: data_stage01_isotopomer_mqresultstable_sample_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY data_stage01_isotopomer_mqresultstable
    ADD CONSTRAINT data_stage01_isotopomer_mqresultstable_sample_name_fkey FOREIGN KEY (sample_name) REFERENCES sample(sample_name);


--
-- TOC entry 2992 (class 2606 OID 132023)
-- Name: data_stage01_mqresultstable_sample_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY data_stage01_quantification_mqresultstable
    ADD CONSTRAINT data_stage01_mqresultstable_sample_name_fkey FOREIGN KEY (sample_name) REFERENCES sample(sample_name);


--
-- TOC entry 2993 (class 2606 OID 132028)
-- Name: data_versions_experiment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY data_versions
    ADD CONSTRAINT data_versions_experiment_id_fkey FOREIGN KEY (experiment_id, sample_name) REFERENCES experiment(id, sample_name);


--
-- TOC entry 2994 (class 2606 OID 132033)
-- Name: data_versions_sample_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY data_versions
    ADD CONSTRAINT data_versions_sample_name_fkey FOREIGN KEY (sample_name, component_name, acquisition_date_and_time) REFERENCES data_stage01_quantification_mqresultstable(sample_name, component_name, acquisition_date_and_time);


--
-- TOC entry 2995 (class 2606 OID 132038)
-- Name: experiment_acquisition_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_acquisition_method_id_fkey FOREIGN KEY (acquisition_method_id) REFERENCES acquisition_method(id) ON UPDATE CASCADE;


--
-- TOC entry 2996 (class 2606 OID 132043)
-- Name: experiment_exp_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_exp_type_id_fkey FOREIGN KEY (exp_type_id) REFERENCES experiment_types(id) ON DELETE CASCADE;


--
-- TOC entry 2997 (class 2606 OID 132048)
-- Name: experiment_experimentor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_experimentor_id_fkey FOREIGN KEY (experimentor_id) REFERENCES experimentor_list(experimentor_id);


--
-- TOC entry 2998 (class 2606 OID 132053)
-- Name: experiment_extraction_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_extraction_method_id_fkey FOREIGN KEY (extraction_method_id) REFERENCES extraction_method(id);


--
-- TOC entry 2999 (class 2606 OID 132058)
-- Name: experiment_internal_standard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_internal_standard_id_fkey FOREIGN KEY (internal_standard_id) REFERENCES internal_standard(is_id);


--
-- TOC entry 3000 (class 2606 OID 132063)
-- Name: experiment_quantitation_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_quantitation_method_id_fkey FOREIGN KEY (quantitation_method_id) REFERENCES quantitation_method_list(quantitation_method_id);


--
-- TOC entry 3001 (class 2606 OID 132068)
-- Name: experiment_sample_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY experiment
    ADD CONSTRAINT experiment_sample_name_fkey FOREIGN KEY (sample_name) REFERENCES sample(sample_name);


--
-- TOC entry 3002 (class 2606 OID 132073)
-- Name: experimentor_id2name_experimentor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY experimentor_id2name
    ADD CONSTRAINT experimentor_id2name_experimentor_id_fkey FOREIGN KEY (experimentor_id) REFERENCES experimentor_list(experimentor_id) ON UPDATE CASCADE;


--
-- TOC entry 3003 (class 2606 OID 132078)
-- Name: experimentor_id2name_experimentor_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY experimentor_id2name
    ADD CONSTRAINT experimentor_id2name_experimentor_name_fkey FOREIGN KEY (experimentor_name) REFERENCES experimentor(experimentor_name);


--
-- TOC entry 3004 (class 2606 OID 132083)
-- Name: internal_standard_experimentor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY internal_standard
    ADD CONSTRAINT internal_standard_experimentor_id_fkey FOREIGN KEY (experimentor_id) REFERENCES experimentor_list(experimentor_id);


--
-- TOC entry 3005 (class 2606 OID 132088)
-- Name: internal_standard_is_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY internal_standard
    ADD CONSTRAINT internal_standard_is_id_fkey FOREIGN KEY (is_id) REFERENCES internal_standard_storage(is_id);


--
-- TOC entry 3006 (class 2606 OID 132093)
-- Name: lc_elution_lc_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY lc_elution
    ADD CONSTRAINT lc_elution_lc_method_id_fkey FOREIGN KEY (lc_method_id) REFERENCES lc_method(id) ON UPDATE CASCADE;


--
-- TOC entry 3007 (class 2606 OID 132098)
-- Name: lc_method_lc_gradient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY lc_method
    ADD CONSTRAINT lc_method_lc_gradient_id_fkey FOREIGN KEY (lc_gradient_id) REFERENCES lc_gradient(id) ON UPDATE CASCADE;


--
-- TOC entry 3008 (class 2606 OID 132103)
-- Name: lc_method_lc_information_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY lc_method
    ADD CONSTRAINT lc_method_lc_information_id_fkey FOREIGN KEY (lc_information_id) REFERENCES lc_information(id) ON UPDATE CASCADE;


--
-- TOC entry 3009 (class 2606 OID 132108)
-- Name: lc_method_lc_parameters_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY lc_method
    ADD CONSTRAINT lc_method_lc_parameters_id_fkey FOREIGN KEY (lc_parameters_id) REFERENCES lc_parameters(id) ON UPDATE CASCADE;


--
-- TOC entry 3011 (class 2606 OID 132113)
-- Name: mix2met_id_mix_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mix2met_id
    ADD CONSTRAINT mix2met_id_mix_id_fkey FOREIGN KEY (mix_id) REFERENCES mix_description(mix_id);


--
-- TOC entry 3012 (class 2606 OID 132118)
-- Name: mix2met_id_mix_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mix2met_id
    ADD CONSTRAINT mix2met_id_mix_id_fkey1 FOREIGN KEY (mix_id) REFERENCES mix_storage(mix_id);


--
-- TOC entry 3013 (class 2606 OID 132123)
-- Name: mix2met_id_mix_id_fkey2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mix2met_id
    ADD CONSTRAINT mix2met_id_mix_id_fkey2 FOREIGN KEY (mix_id) REFERENCES calibrator2mix(mix_id);


--
-- TOC entry 3014 (class 2606 OID 132128)
-- Name: mix_calculations_mix_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mix_calculations
    ADD CONSTRAINT mix_calculations_mix_id_fkey FOREIGN KEY (mix_id) REFERENCES mix_parameters(mix_id);


--
-- TOC entry 3015 (class 2606 OID 132133)
-- Name: ms_component_list_ms_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ms_component_list
    ADD CONSTRAINT ms_component_list_ms_method_id_fkey FOREIGN KEY (ms_method_id) REFERENCES ms_method(id) ON UPDATE CASCADE;


--
-- TOC entry 3016 (class 2606 OID 132138)
-- Name: ms_method_ms_information_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ms_method
    ADD CONSTRAINT ms_method_ms_information_id_fkey FOREIGN KEY (ms_information_id) REFERENCES ms_information(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3017 (class 2606 OID 132143)
-- Name: ms_method_ms_sourceparameters_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ms_method
    ADD CONSTRAINT ms_method_ms_sourceparameters_id_fkey FOREIGN KEY (ms_sourceparameters_id) REFERENCES ms_sourceparameters(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3010 (class 2606 OID 132148)
-- Name: physiologicalratio2met_physiologicalratio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY metabolomics_physiologicalratio2met
    ADD CONSTRAINT physiologicalratio2met_physiologicalratio_id_fkey FOREIGN KEY (physiologicalratio_id) REFERENCES metabolomics_physiologicalratios(physiologicalratio_id);


--
-- TOC entry 3018 (class 2606 OID 132153)
-- Name: quantitation_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY quantitation_method
    ADD CONSTRAINT quantitation_method_id_fkey FOREIGN KEY (id) REFERENCES quantitation_method_list(quantitation_method_id) ON DELETE CASCADE;


--
-- TOC entry 3019 (class 2606 OID 132158)
-- Name: sample_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sample
    ADD CONSTRAINT sample_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES sample_storage(sample_id);


--
-- TOC entry 3020 (class 2606 OID 132163)
-- Name: sample_sample_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sample
    ADD CONSTRAINT sample_sample_id_fkey1 FOREIGN KEY (sample_id) REFERENCES sample_physiologicalparameters(sample_id);


--
-- TOC entry 3021 (class 2606 OID 132168)
-- Name: sample_sample_id_fkey2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sample
    ADD CONSTRAINT sample_sample_id_fkey2 FOREIGN KEY (sample_id) REFERENCES sample_description(sample_id);


--
-- TOC entry 3022 (class 2606 OID 132173)
-- Name: standards2material_met_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY standards2material
    ADD CONSTRAINT standards2material_met_id_fkey FOREIGN KEY (met_id) REFERENCES standards(met_id);


--
-- TOC entry 3023 (class 2606 OID 132178)
-- Name: standards2material_met_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY standards2material
    ADD CONSTRAINT standards2material_met_id_fkey1 FOREIGN KEY (met_id, provider, provider_reference) REFERENCES standards_ordering(met_id, provider, provider_reference);


--
-- TOC entry 3024 (class 2606 OID 132183)
-- Name: standards_storage_met_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY standards_storage
    ADD CONSTRAINT standards_storage_met_id_fkey FOREIGN KEY (met_id, provider, provider_reference) REFERENCES standards2material(met_id, provider, provider_reference);


--
-- TOC entry 3139 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-01-14 09:07:52

--
-- PostgreSQL database dump complete
--

