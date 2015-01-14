from base_analysis import *
from scipy.stats import linregress
import scipy.stats
from scipy.sparse.linalg import svds

import matplotlib.pyplot as pp
from scipy import linspace, sin
from scipy.interpolate import splrep, splev
import numpy
import json

from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

import pandas as pd

from resources.cookb_signalsmooth import smooth
from resources.legendre_smooth import legendre_smooth
from Bio.Statistics import lowess

class base_calculate(base_analysis):
    def __init__(self):
        self.session = Session();

    # calculations
    # biomass normalization
    def calculate_gdw_CVSAndCVSUnitsAndODAndConversionAndConversionUnits(self,cvs_I,cvs_units_I,od600_I,conversion_I,conversion_units_I):
        # check units
        if (cvs_units_I == 'mL' and conversion_units_I == 'gDW*L-1*OD600-1'):
            gdw_O = cvs_I*1e-3*od600_I*conversion_I;
            gdw_units_O = 'gDW';
            return gdw_O, gdw_units_O;
        else:
            print('biomass conversion units do not match!')
            exit(-1);
    def calculate_cellVolume_CVSAndCVSUnitsAndODAndConversionAndConversionUnits(self,cvs_I,cvs_units_I,od600_I,conversion_I,conversion_units_I):
        # check units
        if (cvs_units_I == 'mL' and conversion_units_I == 'uL*mL-1*OD600-1'):
            cellVolume_O = cvs_I*od600_I*conversion_I*1e-6;
            cellVolume_units_O = 'L';
            return cellVolume_O, cellVolume_units_O;
        else:
            print('cell volume conversion units do not match!')
            exit(-1);
    def calculate_conc_concAndConcUnitsAndDilAndDilUnitsAndConversionAndConversionUnits(self,conc_I,conc_units_I,dil_I,dil_units_I,conversion_I,conversion_units_I):
        # check units
        if (conc_units_I == 'uM' and conversion_units_I == 'L' and dil_units_I == 'mL'):
            conc_O = (conc_I*1e-6)*(dil_I)*(1/conversion_I);
            conc_units_O = 'mM';
            return conc_O, conc_units_O;
        elif ((conc_units_I == 'height_ratio' or conc_units_I == 'area_ratio') and conversion_units_I == 'L' and dil_units_I == 'mL'):
            conc_O = (conc_I*1e-3)*(dil_I)*(1/conversion_I);
            conc_units_O = conc_units_I;
            return conc_O, conc_units_O;
        else:
            print('concentration normalization units do not match!')
            exit(-1);
    def calculate_cultureDensity_ODAndConversionAndConversionUnits(self,od600_I,conversion_I,conversion_units_I):
        cultureDensity_O = od600_I*conversion_I;
        cultureDensity_units_O = conversion_units_I.replace('*OD600-1','');
        return cultureDensity_O, cultureDensity_units_O;

    # calculate the geometric mean and variance:
    def calculate_ave_var_geometric(self,data_I):
        # calculate the geometric average and var of data
        # with 95% confidence intervals

        try:
            data_ave_O = 0.0
            # calculate the average of the sample
            for c in data_I:
                data_ave_O += log(c);
            data_ave_O = exp(data_ave_O/len(data_I));

            data_var_O = 0.0
            #calculate the variance of the sample
            for c in data_I:
                data_var_O += pow(log(c/data_ave_O),2);
            data_var_O = data_var_O/(len(data_I)-1); #note: we will need to take the exp()
                                                     # to get the final variance
                                                     # but leaving it this way makes the
                                                     # downstream calculations simpler

            #calculate the 95% confidence intervals
            data_se = sqrt(data_var_O/len(data_I));
            data_lb_O = exp(log(data_ave_O) - 1.96*data_se);
            data_ub_O = exp(log(data_ave_O) + 1.96*data_se);
            
            #correct the variance for use in reporting
            data_var_O = exp(data_var_O);

            return data_ave_O, data_var_O, data_lb_O, data_ub_O;
        except Exception as e:
            print(e);
            exit(-1);
    # calculate the mean and variance:
    def calculate_ave_var(self,data_I,confidence_I = 0.95):
        # calculate the average and var of data
        # with 95% confidence intervals

        try:
            data = numpy.array(data_I);

            data_ave_O = 0.0
            # calculate the average of the sample
            data_ave_O = numpy.mean(data);

            data_var_O = 0.0
            #calculate the variance of the sample
            data_var_O = numpy.var(data);

            #calculate the standard error of the sample
            se = scipy.stats.sem(data)

            #calculate the 95% confidence intervals
            n = len(data);
            h = se * scipy.stats.t._ppf((1+confidence_I)/2., n-1)
            data_lb_O = data_ave_O - h;
            data_ub_O = data_ave_O + h;

            return data_ave_O, data_var_O, data_lb_O, data_ub_O;
        except Exception as e:
            print(e);
            exit(-1);

    # linear regression
    def calculate_regressionParameters(self,concentrations_I,ratios_I,dilution_factors_I,fit_I,weighting_I,use_area_I):
        '''calculate regression parameters for a given component
        NOTE: intended to be used in a loop'''
        # input:
        #       concentrations_I
        #       ratios_I
        #       dilution_factors_I
        #       fit_I
        #       weighting_I
        #       use_area_I
        # ouput:
        #       slope
        #       intercept
        #       correlation
        #       lloq
        #       uloq
        #       points

        # note need to make complimentary method to query concentrations, ratios, and dilution factors
        # for each component prior to calling this function

        #TODO

        return
    def calculate_growthRate(self,time_I,biomass_I):
        '''calculate exponential growth'''

        x = numpy.array(time_I);
        y = numpy.log(biomass_I); #weight the biomass by the natural logarithmn

        slope, intercept, r_value, p_value, std_err = linregress(x,y);
        r2 = r_value**2; #coefficient of determination

        return slope, intercept, r2, p_value, std_err;
    def interpolate_biomass(self,time_I, slope, intercept):
        '''interpolate the biomass from an exponential fit of the growth rate'''

        biomass = [];
        for t in time_I:
            biomass.append(t*slope+intercept);
        return biomass;
    def calculate_uptakeAndSecretionRate(self,dcw_I,conc_I,gr_I):
        '''calculate uptake and secretion rates'''

        x = numpy.array(dcw_I);
        y = numpy.array(conc_I); 

        slope, intercept, r_value, p_value, std_err = linregress(x,y);
        r2 = r_value**2; #coefficient of determination

        rate = slope*gr_I;

        return slope, intercept, r2, p_value, std_err, rate;
    def interpolate_biomass(self,time_I, slope, intercept):
        '''interpolate the biomass from an exponential fit of the growth rate'''

        biomass = [];
        for t in time_I:
            biomass.append(t*slope+intercept);
        return biomass;

    # smoothing functions
    def fit_trajectories(self,x_I,y_I,fit_func_I='lowess',plot_textLabels_I=None,plot_fit_I=False):
        '''fit trajectory growth rate data to a smoothing function'''
        #Input:
        #   x_I = ale_time
        #   y_I = growth_rate
        #Output:
        #   x_O = ale_time_fitted
        #   y_O = growth_rate_fitted

        #cnt = 1;
        x = [];
        y = [];
        x = x_I;
        y = y_I;
        if fit_func_I=='spline':
            #spline
            tck = splrep(x,y,k=3,s=.025) #no smoothing factor
            #tck = splrep(x,y,k=3,task=-1,t=10) #no smoothing factor
            x2 = linspace(min(x),max(x),500)
            y2_spline= splev(x2,tck)
            y2 = numpy.zeros_like(y2_spline);
            for i,y2s in enumerate(y2_spline):
                if i==0:
                    y2[i] = y2s;
                elif i!=0 and y2s<y2[i-1]:
                    y2[i] = y2[i-1];
                else:
                    y2[i] = y2s;
        elif fit_func_I=='movingWindow':
            #moving window filter
            x2 = numpy.array(x);
            y2 = smooth(numpy.array(y),window_len=10, window='hanning');
        elif fit_func_I=='legendre':
            #legendre smoothing optimization
            smooth = legendre_smooth(len(x),1,1e-4,25)
            x2 = numpy.array(x);
            y2 = smooth.fit(numpy.array(y))
        elif fit_func_I=='lowess':
            #lowess
            x2 = numpy.array(x);
            y2_lowess = lowess.lowess(x2,numpy.array(y),f=0.1,iter=100)
            y2 = numpy.zeros_like(y2_lowess);
            for i,y2s in enumerate(y2_lowess):
                if i==0:
                    y2[i] = y2s;
                elif i!=0 and y2s<y2[i-1]:
                    y2[i] = y2[i-1];
                else:
                    y2[i] = y2s;
        else:
            print "fit function not recongnized";
        if plot_fit_I:
            ##QC plot using MatPlotLib
            # Create a Figure object.
            fig = pp.figure();
            # Create an Axes object.
            ax = fig.add_subplot(1,1,1) # one row, one column, first plot
            ## Add a title.
            #ax.set_title(k['sample_label'])
            # Set the axis
            pp.axis([0,max(x),0,max(y)+0.1]);
            # Add axis labels.
            ax.set_xlabel('Time [days]')
            ax.set_ylabel('GR [hr-1]')
            ## Label data points
            #tck = splrep(x,y,k=3,s=1.); #spline fit with very high smoothing factor
            #x_days = ALEsKOs_textLabels[k['sample_name_abbreviation']]['day']
            #y_days = splev(x_days,tck)
            #for i,txt in enumerate(ALEsKOs_textLabels[k['sample_name_abbreviation']]['dataType']):
            #    ax.annotate(txt, (x_days[i],y_days[i]-.15))
            # Create the plot
            #pp.plot(x_days,y_days,'rx',x,y,'b.',x2,y2,'g')
            pp.plot(x,y,'b.',x2,y2,'g')
            #display the plot
            pp.show()
        #record
        x_O = [];
        y_O = [];
        x_O = x2;
        y_O = y2;
        #cnt += 1;
        return x_O, y_O;
    
    # other
    def null(self, A, eps=1e-6):
        u, s, vh = numpy.linalg.svd(A,full_matrices=1,compute_uv=1)
        null_rows = [];
        rank = numpy.linalg.matrix_rank(A)
        for i in range(A.shape[1]):
            if i<rank:
                null_rows.append(False);
            else:
                null_rows.append(True);
        null_space = scipy.compress(null_rows, vh, axis=0)
        return null_space.T

    # heatmap
    def heatmap(self,data_I,row_labels_I,column_labels_I):
        '''Generate a heatmap using pandas and scipy'''
        mets_data = pd.DataFrame(data=data_I, index=row_labels_I, columns=column_labels_I)

        mets_data = mets_data.dropna(how='all').fillna(0.)
        #mets_data = mets_data.replace([np.inf], 10.)
        #mets_data = mets_data.replace([-np.inf], -10.)
        col_labels = list(mets_data.columns)
        row_labels = list(mets_data.index)

        heatmap_data = []
        for i,g in enumerate(mets_data.index):
            for j,c in enumerate(mets_data.columns):
                heatmap_data.append({"col": j+1, "row": i+1, "value": mets_data.ix[g][c]})


        dm = mets_data
        D1 = squareform(pdist(dm, metric='euclidean'))
        D2 = squareform(pdist(dm.T, metric='euclidean'))

        Y = linkage(D1, method='single')
        Z1 = dendrogram(Y, labels=dm.index)

        Y = linkage(D2, method='single')
        Z2 = dendrogram(Y, labels=dm.columns)

        hccol = Z2['leaves'] # no hclustering; same as heatmap_data['col']
        hcrow = Z1['leaves'] # no hclustering; same as heatmap_data['row']

        hccol = [x+1 for x in hccol]
        hcrow = [x+1 for x in hcrow]

        return {'hcrow': hcrow, 'hccol': hccol, 'row_labels':row_labels,
                                            'col_labels':col_labels,
                                            'heatmap_data':heatmap_data,
                                            'maxval' : max([x['value'] for x in heatmap_data]),
                                            'minval' : min([x['value'] for x in heatmap_data])}
