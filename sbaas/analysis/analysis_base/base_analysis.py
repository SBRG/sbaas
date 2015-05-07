'''Base class for metabolomics analysis'''

from math import log, sqrt, exp
import csv
from sys import exit
import numpy
import re
#ORM
from models import *
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
#settings
from data import sbaas_settings as settings

class base_analysis():
    def __init__(self,session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();

    def remove_jsRegularExpressions(self,string_I):
        '''Remove java script regular expressions that interfere with the string filtering
        Substitutions:
        * for x
        . for _
        '''
        p = re.compile('[*.]');
        #string_O = string_I.replace('*','x');
        string_O = p.sub('_',string_I);
        return string_O;

    
