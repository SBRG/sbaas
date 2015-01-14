'''Base class for metabolomics analysis'''

from math import log, sqrt, exp
import csv
from sys import exit
import numpy
#ORM
from models import *
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
#settings
from data import sbaas_settings as settings

class base_analysis():
    def __init__(self):
        self.session = Session();

    
