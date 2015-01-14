--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.1
-- Dumped by pg_dump version 9.3.1
-- Started on 2014-12-28 14:27:18

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

DROP DATABASE sbaas;

--
-- TOC entry 3137 (class 1262 OID 112808)
-- Name: metabolomics; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE sbaas WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';


ALTER DATABASE sbaas OWNER TO postgres;