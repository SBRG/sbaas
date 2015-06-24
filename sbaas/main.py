# define search paths manually
import sys
from data import sbaas_settings as settings
#sys.path.append('C:\\Users\\dmccloskey-sbrg\\Documents\\GitHub\\sbaas\\sbaas')
sys.path.append(settings.sbaas)
sys.path.append('C:\\Users\\dmccloskey-sbrg\\Documents\\GitHub\\thermodynamics')
sys.path.append('C:\\Users\\dmccloskey-sbrg\\Documents\\GitHub\\component-contribution')

##Analysis tests:
#from tests import analysis_ale, analysis_physiology, analysis_resequencing
#analysis_ale.run_all_tests();
#analysis_physiology.run_all_tests();
#analysis_resequencing.run_all_tests();

##Visualization tests:
#from visualization.server import run
#run();
##run(port=8080,public=True);

#Debug mode:
from sbaas.analysis.analysis_stage01_isotopomer import *
from sbaas.analysis.analysis_base.base_importData import base_importData
from sbaas.models import *
session = Session();
io01 = stage01_isotopomer_io(session);
ex01 = stage01_isotopomer_execute(session);
ex01.execute_buildSpectrumFromPeakData('ALEsKOs01','isotopomer_13C',
    sample_name_abbreviations_I =[
    'OxicEvo04pgiEvo06EPEcoli13CGlc',
    #'OxicEvo04pgiEvo07EPEcoli13CGlc',
    ],
    #met_ids_I=['dhap','glyc3p','glyclt']
    );
