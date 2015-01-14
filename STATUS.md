SBaaS
============
Systems Biochemistry as a Service
============
Douglas McCloskey
-----------------

Analysis pipelines currently supported:
---------------------------------------
LIMS:

	a.	Documentation of wet-lab experiments
	
	b.	Sample extraction methods
	
	c.	Instrument acquisition methods and system suitability tests
	
	d.	Sample information and storage
	
	c.	Standards, calibrators, and internal standards information and storage
	
	e.	Biological material information and storage

Quantification (i.e., Metabolomics)

	1.	Batch QC/QA, quantification of analytes, biomass normalization, calculation of physiological ratios, and missing value imputation
	
	2.	Statistical and correlation analysis (e.g. PCA, ANOVA, etc.)
	
	3.	Thermodynamic analysis
	
	4.	Kinetic analysis

Isotopomer (i.e., Fluxomics)

	1.	Isotopomer deconvolution and isotopomer distribution calculations
	
	2.	Fluxomics

Physiology (i.e., Phenomics)

	1.	Calculation of growth rate and substrate uptake/secretion rates
	
	2.	Sampling and analysis of the solution space using constraint-based modeling

adaptive laboratory evolution (ALE) (i.e., ALE experiment growth rate trajectories)

	1.	Growth rate trajectory curve fitting and jump finding

Resequencing (i.e., DNA population resequencing)

	1.	parsing of breseq data, clonal and population mutation filtering, analysis of ALE population mutation lineages and end-point mutation frequencies
	
	2.	correlation analysis of mutations and physiological data

Project organization:
---------------------
analysis/: analysis pipelines code

data/: escher maps, cobra and fluxomics models, compound .mol files, postgresql initialization scripts, etc.

models/: data models of the database written in the ORM (i.e., sqlalchemy)

resources/: open-source and 3rd party dependencies and classes utilized in various analyses

tests/: tests of the different analysis pipelines

visualization/: webserver files used for data visualization

Analysis Pipeline software needs:
---------------------------------
1.	Fluxomics package written as a module for cobrapy that includes support for stationary and non-stationary tracer experiments for any element type.  (expansion of data_stage02_isotopomer)

	a.	atom mapping method

	b.	cobra2emu
	
	c.	tracer simulation and identifiability analysis
	
	d.	flux estimate, parameter continuation, and monte-carlo sampling
	
2.	Peak viewing and peak integration software written outside of the vendor-specific/proprietary domain.  (expansion of data_stage01_quantification
and data_stage01_isotopomer)

3.	Direct integration with breseq

4.	Web-UI for data analysis beyond only data visualization