import itertools, os, csv
import io
from subprocess import Popen, PIPE
    
cxcalc_bin = 'C:/Program Files (x86)/ChemAxon/MarvinBeans/bin/cxcalc'

class ChemAxonError(Exception):
    pass

def RunCxcalc(cxcalc_bin, cmd, args):
    '''command line calculator plugin utility provided by chemaxon'''
    # input:
    #       cxcal_bin = location of cxcalc.bin
    #       cmd = command to execute (e.g. 'formula' or 'exactmass')
    #       args = list of arguments
    try:
        p1 = Popen([cxcalc_bin] + [cmd] + args, #stdin=p1.stdout,
                   stdout=PIPE, stderr=PIPE, shell=True) # shell = True required for windows
                                                         #executable = CXCALC_BIN illegal for windows
        res = p1.communicate()[0]
        if p1.returncode != 0:
            raise ChemAxonError(debug_args)
        return res
    except OSError:
        raise Exception("Marvin (by ChemAxon) is not installed.")