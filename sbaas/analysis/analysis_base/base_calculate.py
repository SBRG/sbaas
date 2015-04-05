from base_analysis import *
from scipy.stats import linregress
import scipy.stats
from scipy.sparse.linalg import svds
from math import ceil

import matplotlib.pyplot as pp
from scipy import linspace, sin
from scipy.interpolate import splrep, splev
import numpy
import numpy.random as npr
import json

from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

import pandas as pd

from resources.cookb_signalsmooth import smooth
from resources.legendre_smooth import legendre_smooth
from Bio.Statistics import lowess

class base_calculate(base_analysis):
    def __init__(self):
        self.data=[];

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

    # statistical analysis
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
    # calculate the confidence intervals
    def calculate_ciFromPoints(self,data_I, alpha=0.05):
        """Calculate the confidence intervals from sampled points"""
        data_sorted = numpy.sort(data_I)
        n = len(data_sorted)
        lb = data_sorted[int((alpha/2.0)*n)]
        ub = data_sorted[int((1-alpha/2.0)*n)]
        return lb,ub
    def bootstrap(self,data, num_samples=100000, statistic=numpy.mean, alpha=0.05):
        """Returns bootstrap estimate of 100.0*(1-alpha) CI for statistic."""
        n = len(data)
        idx = npr.randint(0, n, (num_samples, n))
        samples = data[idx]
        stat = numpy.sort(statistic(samples, 1))
        return (stat[int((alpha/2.0)*num_samples)],
                stat[int((1-alpha/2.0)*num_samples)])
    # calculate the p-value difference
    def permutation_resampling(self,case, control, num_samples=50, statistic=numpy.mean):
        '''calculate the pvalue of two data sets using a resampling approach'''

        observed_diff = abs(statistic(case) - statistic(control))
        num_case = len(case)

        combined = numpy.concatenate([case, control])
        diffs = []
        for i in range(num_samples):
            xs = npr.permutation(combined)
            diff = numpy.mean(xs[:num_case]) - numpy.mean(xs[num_case:])
            diffs.append(diff)

        pval = (numpy.sum(diffs > observed_diff) +
                numpy.sum(diffs < -observed_diff))/float(num_samples)
        return pval, observed_diff, diffs
    def calculate_pvalue_permutation(self,data_1_I,data_2_I,n_permutations_I=10,n_resamples_I=10):    
        '''calculate the pvalue of two data by determining
        the lack of overlap between sample points using a permutation test.
        If the sample points of the data sets is not equal,
        a subset of samples of matching length is resampled from the larger data set'''
        
        data_1 = None; #sample set with fewer points
        data_2 = None; #sample set with more points
        n_resamples = 0;

        # check the length of data_1 and data_2
        if len(data_1_I)>len(data_2_I):
            data_1=numpy.array(data_2_I);
            data_2=numpy.array(data_1_I);
            n_resamples=n_resamples_I;
        elif len(data_1_I)<len(data_2_I):
            data_1=numpy.array(data_1_I);
            data_2=numpy.array(data_2_I);
            n_resamples=n_resamples_I;
        else:
            data_1=numpy.array(data_1_I);
            data_2=numpy.array(data_2_I);

        n_samples_min = len(data_1);

        vals = []
        for i in range(0,n_permutations_I):
            if n_resamples==0:
                cond1 = numpy.random.permutation(data_1)
                cond2 = numpy.random.permutation(data_2)
                z = cond1 - cond2
                x = len(z[z>0]) + 1
                y = len(z[z<0]) + 1
                k = min(x,y)
                vals.append(k)
            else:
                cond1 = numpy.random.permutation(data_1)
                cond2 = numpy.random.permutation(data_2)
                for resample in range(n_resamples):
                    cond2_int = numpy.random.randint(0,n_samples_min);
                    z = cond1 - cond2[cond2_int]
                    x = len(z[z>0]) + 1
                    y = len(z[z<0]) + 1
                    k = min(x,y)
                    vals.append(k)
        p = numpy.mean(vals)/len(data_1)*2
        return p;
    # calculate the interquartiles
    def calculate_interquartiles(self,data_I,iq_range_I = [25,75]):
        '''compute the interquartiles and return the min, max, median, iq1 and iq3'''

        min_O = numpy.min(data_I);
        max_O = numpy.max(data_I);
        iq_1_O, iq_2_O = numpy.percentile(data_I, iq_range_I)
        median_O = numpy.median(data_I);

        return min_O, max_O, median_O, iq_1_O, iq_2_O;

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
    def heatmap(self,data_I,row_labels_I,column_labels_I,
                row_pdist_metric_I='euclidean',row_linkage_method_I='ward',
                col_pdist_metric_I='euclidean',col_linkage_method_I='ward'):
        '''Generate a heatmap using pandas and scipy'''

        """dendrogram documentation:
        linkage Methods:
        single(y)	Performs single/min/nearest linkage on the condensed distance matrix y
        complete(y)	Performs complete/max/farthest point linkage on a condensed distance matrix
        average(y)	Performs average/UPGMA linkage on a condensed distance matrix
        weighted(y)	Performs weighted/WPGMA linkage on the condensed distance matrix.
        centroid(y)	Performs centroid/UPGMC linkage.
        median(y)	Performs median/WPGMC linkage.
        ward(y)	Performs Ward's linkage on a condensed or redundant distance matrix.
        Output:
        'color_list': A list of color names. The k?th element represents the color of the k?th link.
        'icoord' and 'dcoord':  Each of them is a list of lists. Let icoord = [I1, I2, ..., Ip] where Ik = [xk1, xk2, xk3, xk4] and dcoord = [D1, D2, ..., Dp] where Dk = [yk1, yk2, yk3, yk4], then the k?th link painted is (xk1, yk1) - (xk2, yk2) - (xk3, yk3) - (xk4, yk4).
        'ivl':  A list of labels corresponding to the leaf nodes.
        'leaves': For each i, H[i] == j, cluster node j appears in position i in the left-to-right traversal of the leaves, where \(j < 2n-1\) and \(i < n\). If j is less than n, the i-th leaf node corresponds to an original observation. Otherwise, it corresponds to a non-singleton cluster."""

        #parse input into col_labels and row_labels
        #TODO: pandas is not needed for this.
        mets_data = pd.DataFrame(data=data_I, index=row_labels_I, columns=column_labels_I)

        mets_data = mets_data.dropna(how='all').fillna(0.)
        #mets_data = mets_data.replace([np.inf], 10.)
        #mets_data = mets_data.replace([-np.inf], -10.)
        col_labels = list(mets_data.columns)
        row_labels = list(mets_data.index)

        #heatmap data matrix
        heatmap_data = []
        for i,g in enumerate(mets_data.index):
            for j,c in enumerate(mets_data.columns):
                #heatmap_data.append({"col": j+1, "row": i+1, "value": mets_data.ix[g][c]})
                heatmap_data.append({"col": j, "row": i, "value": mets_data.ix[g][c]})

        #perform the custering on the both the rows and columns
        dm = mets_data
        D1 = squareform(pdist(dm, metric=row_pdist_metric_I))
        D2 = squareform(pdist(dm.T, metric=col_pdist_metric_I))

        Y = linkage(D1, method=row_linkage_method_I)
        Z1 = dendrogram(Y, labels=dm.index)

        Y = linkage(D2, method=col_linkage_method_I)
        Z2 = dendrogram(Y, labels=dm.columns)

        #parse the output
        col_leaves = Z2['leaves'] # no hclustering; same as heatmap_data['col']
        row_leaves = Z1['leaves'] # no hclustering; same as heatmap_data['row']
        col_icoord = Z2['icoord'] # no hclustering; same as heatmap_data['col']
        row_icoord = Z1['icoord'] # no hclustering; same as heatmap_data['row']
        col_dcoord = Z2['dcoord'] # no hclustering; same as heatmap_data['col']
        row_dcoord = Z1['dcoord'] # no hclustering; same as heatmap_data['row']
        col_ivl = Z2['ivl'] # no hclustering; same as heatmap_data['col']
        row_ivl = Z1['ivl'] # no hclustering; same as heatmap_data['row']
        
        #hccol = [x+1 for x in hccol]; # hccol index should match heatmap_data index
        #hcrow = [x+1 for x in hcrow];

        heatmap_row_O = {'col_leaves':col_leaves,
                        'row_leaves':row_leaves,
                        'col_icoord':col_icoord,
                        'row_icoord':row_icoord,
                        'col_dcoord':col_dcoord,
                        'row_dcoord':row_dcoord,
                        'col_ivl':col_ivl,
                        'row_ivl':row_ivl,
                        'col_labels':col_labels,
                        'row_labels':row_labels,
                        'col_pdist_metric':col_pdist_metric_I,
                        'row_pdist_metric':row_pdist_metric_I,
                        'col_linkage_method':col_linkage_method_I,
                        'row_linkage_method':row_linkage_method_I,
                        'heatmap_data':heatmap_data};
        return heatmap_row_O;
    def heatmap_v1(self,data_I,row_labels_I,column_labels_I):
        '''Generate a heatmap using pandas and scipy
        DEPRECATED: kept for compatibility with old io methods'''

        """dendrogram documentation:

        Output:
        'color_list': A list of color names. The k?th element represents the color of the k?th link.
        'icoord' and 'dcoord':  Each of them is a list of lists. Let icoord = [I1, I2, ..., Ip] where Ik = [xk1, xk2, xk3, xk4] and dcoord = [D1, D2, ..., Dp] where Dk = [yk1, yk2, yk3, yk4], then the k?th link painted is (xk1, yk1) - (xk2, yk2) - (xk3, yk3) - (xk4, yk4).
        'ivl':  A list of labels corresponding to the leaf nodes.
        'leaves': For each i, H[i] == j, cluster node j appears in position i in the left-to-right traversal of the leaves, where \(j < 2n-1\) and \(i < n\). If j is less than n, the i-th leaf node corresponds to an original observation. Otherwise, it corresponds to a non-singleton cluster."""

        #parse input into col_labels and row_labels
        #TODO: pandas is not needed for this.
        mets_data = pd.DataFrame(data=data_I, index=row_labels_I, columns=column_labels_I)

        mets_data = mets_data.dropna(how='all').fillna(0.)
        #mets_data = mets_data.replace([np.inf], 10.)
        #mets_data = mets_data.replace([-np.inf], -10.)
        col_labels = list(mets_data.columns)
        row_labels = list(mets_data.index)

        #heatmap data matrix
        heatmap_data = []
        for i,g in enumerate(mets_data.index):
            for j,c in enumerate(mets_data.columns):
                #heatmap_data.append({"col": j+1, "row": i+1, "value": mets_data.ix[g][c]})
                heatmap_data.append({"col": j, "row": i, "value": mets_data.ix[g][c]})

        #perform the custering on the both the rows and columns
        dm = mets_data
        D1 = squareform(pdist(dm, metric='euclidean'))
        D2 = squareform(pdist(dm.T, metric='euclidean'))

        Y = linkage(D1, method='single')
        Z1 = dendrogram(Y, labels=dm.index)

        Y = linkage(D2, method='single')
        Z2 = dendrogram(Y, labels=dm.columns)

        #parse the output
        hccol = Z2['leaves'] # no hclustering; same as heatmap_data['col']
        hcrow = Z1['leaves'] # no hclustering; same as heatmap_data['row']
        hccolicoord = Z2['icoord'] # no hclustering; same as heatmap_data['col']
        hcrowicoord = Z1['icoord'] # no hclustering; same as heatmap_data['row']
        hccoldcoord = Z2['dcoord'] # no hclustering; same as heatmap_data['col']
        hcrowdcoord = Z1['dcoord'] # no hclustering; same as heatmap_data['row']
        
        #hccol = [x+1 for x in hccol]; # hccol index should match heatmap_data index
        #hcrow = [x+1 for x in hcrow];

        return {'hcrow': hcrow, 'hccol': hccol, 'row_labels':row_labels,
                                            'col_labels':col_labels,
                                            'heatmap_data':heatmap_data,
                                            'maxval' : max([x['value'] for x in heatmap_data]),
                                            'minval' : min([x['value'] for x in heatmap_data])}

    # histogram and kde
    def histogram(self, data_I, n_bins_I=50, calc_bins_I=True):
        '''generate lower bound of the bins, the bin widths, and frequency of the data'''

        x_O = []; #the lower bound of the bin (inclusive)
        dx_O = []; #the width of the bin; x + dx is the upper bound (exclusive).
        y_O = []; #the count (if frequency is true), or the probability (if frequency is false).

        if calc_bins_I:
            n_bins = ceil(sqrt(len(data_I)));
        else:
            n_bins = n_bins_I;

        hist = numpy.histogram(data_I,n_bins);
        y_O = hist[0];
        edges = hist[1];

        for i in range(len(edges)-1):
            x_O.append(edges[i])
            dx_O.append(edges[i+1]-edges[i])

        return x_O,dx_O,y_O
    def pdf_kde(self,data_I,min_I=None,max_I=None,points_I=1000,bandwidth_I=None):
        '''compute the pdf from the kernal density estimate'''

        if min_I and max_I:
            min_point = min_I;
            max_point = max_I;
        else:
            min_point = min(data_I);
            max_point = max(data_I);

        x_grid = numpy.linspace(min_point, max_point, 1000)
        try:
            kde_scipy=scipy.stats.gaussian_kde(data_I, bw_method=bandwidth_I);
        except RuntimeError as e:
            print e
            return [0],[0];
        pdf = kde_scipy(x_grid);

        return x_grid,pdf