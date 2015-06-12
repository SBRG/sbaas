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
Python 3.4+

R 2.12+

Postgresql 9.0+

Python-dependencies:
-------------------
windows: 
install winpython (http://winpython.github.io/)
download individual installations for cobrapy, escher, openbabel, xlwings and libsbml and use the winpython package manager to install
OR
install packages individually from pip from vc10++ command line

linux: requires pip installation

macox: requires pip installation

python-libsbml (http://www.lfd.uci.edu/~gohlke/pythonlibs/)

cobrapy (https://pypi.python.org/pypi/cobra/)

escher (https://github.com/zakandrewking/escher/)

numpy (pip)

pywin32 (pip;windows)


scipy (pip)

matplotlib (pip)

pandas (pip)

rpy2 (pip)

sqlalchemy (pip)

h5py (http://www.lfd.uci.edu/~gohlke/pythonlibs/)

jinja2 (pip)

tornado (pip)

pywin32 (http://www.lfd.uci.edu/~gohlke/pythonlibs/)
requires running the following script: python C:\Python34\Scripts\pywin32_postinstall.py -install

PyQt (http://www.lfd.uci.edu/~gohlke/pythonlibs/)

pyzmq (pip)

pytz (pip)

ipython (pip)

openbabel (http://www.lfd.uci.edu/~gohlke/pythonlibs/)

oct2py (pip)

biopython (pip)

gurobipy (not found for current version)

beautifulsoup (bs4) (not found for current version)

psycopg2 (http://www.lfd.uci.edu/~gohlke/pythonlibs/)

xlwings (pip)

thermodynamics (https://github.com/dmccloskey/thermodynamics.git)