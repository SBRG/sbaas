SBaaS
============
Systems Biochemistry as a Service
============
Douglas McCloskey
-----------------

Getting started:
----------------
1.	Install python, postgresql, R, and other dependencies

2.	Build the sbaas database.  Login to the local server and run the commands listed below to create the database, load the table schemas, and load the initial data.  If running a windows machine, use the scripts located in the "ansi" folder.  For all other machines, use the scripts located in the "utf-8" folder.  Replace the filepaths with those specific to your file directory.  If you are attempting to access the database as another user other than "postgres", use the desired user name in the commands listed below.
	
	a.	C:\path_to_posgresql\PostgreSQL\9.3\bin\psql -h localhost -p 5432 -f C:\path_to_github\GitHub\sbaas\sbaas\data\postgresql\ansi\create_sbaas.sql postgres postgres
	
	b.	C:\path_to_posgresql\PostgreSQL\9.3\bin\psql -h localhost -p 5432 -f C:\path_to_github\GitHub\sbaas\sbaas\data\postgresql\ansi\initialize_sbaas.sql sbaas postgres
	
	c.	C:\path_to_posgresql\PostgreSQL\9.3\bin\psql -h localhost -p 5432 -f C:\path_to_github\GitHub\sbaas\sbaas\data\postgresql\ansi\initialize_data_stage00_sbaas.sql sbaas postgres

3.	Define the local user settings in the file data/sbaas_settings for use by the ORM

4.	Run one or multiple of the desired tests provided

Dependencies:
------------
Python 2.7+

R 2.12+

Postgresql 9.0+

Python-dependencies:
-------------------
cobrapy

escher

numpy

scipy

matplotlib

r2py

sqlalchemy

...