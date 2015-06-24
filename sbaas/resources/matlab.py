from sys import exit
from math import log, sqrt, exp
import operator, json, csv
from sbaas.analysis.analysis_base.base_calculate import base_calculate
# Dependencies from 3rd party
import scipy.io
import numpy

class matlab_calculate(base_calculate):
    def __init__(self,matlab_path_I):
        if matlab_path_I:self.matlab_path =  matlab_path_I;
        else: self.matlab_path = 'C:/Users/dmccloskey-sbrg/Documents/MATLAB/ALEsKOs'

    def SMLtools(self,x_I,y_I,filename_I=None,filename_O=None,degree_I=3,knots_I=10,interiorknots_I='free',plot_I='off',increasing_I='on'):
        '''Compute a spline fit of the data using matlab's SMLtools'''

        if not filename_I:
            filename_I = matlab_path + "/SMLtool_in.m";
        if not filename_O:
            filename_O = matlab_path + "/SMLtool_out.m";

        mat_cmd = '';
        #export data
        mat_cmd += 'x=[...\n'
        for x in x_I:
            mat_cmd += str(x) + ',\n';
        mat_cmd += '];\n';
        mat_cmd += 'y=[...\n'
        for y in y_I:
            mat_cmd += str(y) + ',\n';
        mat_cmd += '];\n';
        #spline command
        mat_cmd += ("slm=slmengine(x,y,'degree',%s,'plot',%s,'interiorknots',%s,'knots',%f,'increasing',%s);\n" % (degree_I,plot_I,interiorknots_I,knots_I,increasing_I))
        mat_cmd += "xx{i}=(slm.x(1):slm.x(end)/1000:slm.x(end));\n"
        mat_cmd += "yy{i}=slmeval(xx{i},slm);\n"
        mat_cmd += "curves{i} = slm;\n"
        mat_cmd += ("save(%s);\n" %filename_O);
        #write to file
        with open(filename_I,'wb') as file:
            file.write(mat_cmd);
        #wait for user to execute matlab script
        print("Press any key to continue once script has been executed")
        a=input();
        #read in the data from file:
        xx = scipy.io.loadmat(filename_O)['xx'][0][0];
        yy = scipy.io.loadmat(filename_O)['yy'][0][0];
        curves = scipy.io.loadmat(filename_O)['curves'][0][0];
        return xx,yy,curves;