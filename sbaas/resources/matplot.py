from sys import exit
from math import log, sqrt, exp, ceil
import csv
import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats import linregress
from Bio.Statistics import lowess

class matplot():
    # analysis visualization with matplotlib     
    def densityPlot(self, dataMat_I, points_I=200, covariance_factor_I=0.25):
        '''Generate a density plot of the data using matplotlib'''
        from scipy.stats import gaussian_kde
        if type(dataMat_I)==type([]):
            concentrations_1d = numpy.array(dataMat_I);
        else:
            concentrations_1d = dataMat_I.reshape(dataMat_I.shape[0]*dataMat_I.shape[1])
        density = gaussian_kde(concentrations_1d)
        xs = numpy.linspace(concentrations_1d.min(),concentrations_1d.max(),points_I)
        density.covariance_factor = lambda : covariance_factor_I;
        density._compute_covariance()
        plt.plot(xs,density(xs))
        plt.show()
    def barPlot(self,title_I,xticklabels_I,ylabel_I,xlabel_I,mean_I,var_I=None,se_I=None,add_labels_I=True):
        '''generate a bar plot using matplotlib'''
        
        #calculate the stdev
        if var_I:
            stdev = [sqrt(x) for x in var_I];
        else:
            stdev = se_I; # use standard error instead

        ind = numpy.arange(len(mean_I))  # the x locations for the groups
        width = 0.5       # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, mean_I, width, color='r', yerr=stdev)

        # add some
        ax.set_ylabel(ylabel_I)
        ax.set_xlabel(xlabel_I)
        ax.set_title(title_I)
        ax.set_xticks(ind+width)
        ax.set_xticklabels(xticklabels_I)
        
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                if rect.get_y()>=0:
                    ax.text(rect.get_x()+rect.get_width()/2., 1.1*height, numpy.round(height,decimals=3),
                            ha='center', va='bottom')
                else:
                    ax.text(rect.get_x()+rect.get_width()/2., -1.1*height, -numpy.round(height,decimals=3),
                            ha='center', va='bottom')

        if add_labels_I: autolabel(rects1)

        #force scientific notation
        #ax.get_xaxis().get_major_formatter().set_scientific(True)
        #ax.get_yaxis().get_major_formatter().set_scientific(True)
        #ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        plt.show()
    def volcanoPlot(self,title_I,xlabel_I,ylabel_I,x_data_I,y_data_I,text_labels_I):
        # Create a Figure object.
        fig = plt.figure()
        # Create an Axes object.
        ax = fig.add_subplot(1,1,1) # one row, one column, first plot
        # Plot the data.
        ax.scatter(x_data_I, y_data_I, color="blue", marker="o")
        # Add a title.
        ax.set_title(title_I)
        # Add some axis labels.
        ax.set_xlabel(xlabel_I)
        ax.set_ylabel(ylabel_I)
        # Label data points.
        for i, txt in enumerate(text_labels_I):
            ax.annotate(txt, (x_data_I[i],y_data_I[i]))
        # Produce an image.
        #fig.savefig("scatterplot.png")
        # Show the image.
        plt.show();
    def boxAndWhiskersPlot(self,title_I,xticklabels_I,ylabel_I,xlabel_I,data_I,mean_I=None,ci_I=None,filename_I=None,show_plot_I=True,bootstrap_I=5000,notch_I = 0):
        '''generates a box and whiskers plot using the mean instead of the median
        default: Make a box and whisker plot for each column of data_I or each vector in sequence data_I.
                 The box extends from the lower to upper quartile values of the data, with a line at the median.
                 The whiskers extend from the box to show the range of the data.
                 Flier points are those past the end of the whiskers.
        mean_I: defines the median
        ci_I and notch_I: defines the notch confidence intervals
        Use case 1: set the whiskers to the 95% confidence intervals and median to the mean
                    data_I = [[ci_lb,ci_ub,mean],...]'''

        whiskers_I=[5,95]
        ha = ['right', 'center', 'left']
        try:
            fig, ax = plt.subplots()
            pos = numpy.array(list(range(len(data_I))))+1
            bp = ax.boxplot(data_I, sym='k+', #whis=whiskers_I,
                            positions=pos,
                            notch=notch_I, bootstrap=bootstrap_I,
                            usermedians=mean_I,
                            conf_intervals=ci_I)

            ax.set_xlabel(xlabel_I)
            ax.set_ylabel(ylabel_I)
            ax.set_xticklabels(xticklabels_I, size=6, rotation=15, ha=ha[1])
            ax.set_title(title_I)
            plt.setp(bp['whiskers'], color='k',  linestyle='-' )
            plt.setp(bp['fliers'], markersize=3.0)
            # Produce an image.
            if filename_I:
                fig.savefig(filename_I)
            # Show the image.
            if show_plot_I:
                plt.show();
        except IndexError as e:
            print(e);
    def _extractPCAScores(self,data_I,axis1_I=1,axis2_I=2):
        '''extract out pca data from [{},{},{}] format'''
        x_data = [];
        y_data = [];
        xlabel = '';
        ylabel = '';
        title = '';
        text_labels = [];
        samples = [];
        # TODO:
        # create custom color scheme based on sample_name_abbreviations
        
        # determine the number of samples and axes
        sns = []
        axes = []
        for d in data_I:
                sns.append(d['sample_name_short']);
                axes.append(d['axis'])
        sns_sorted = sorted(set(sns))
        axes_sorted = sorted(set(axes))
        #extract out all axes
        #perc_var = numpy.zeros(len(axes_sorted));
        perc_var = numpy.zeros(len(axes_sorted));
        scores_mat = numpy.zeros((len(sns_sorted),len(axes_sorted)));
        for i,r in enumerate(sns_sorted):
            for j,c in enumerate(axes_sorted):
                for d in data_I:
                    if d['sample_name_short'] == r and d['axis'] == c:
                        scores_mat[i,j] = d['score'];
                        #perc_var[j] = 1 - d['var_cumulative'];
                        perc_var[j] = d['var_proportion'];
                        if j==0:
                            samples.append(d['sample_name_abbreviation'])
        #extract out specified axis
        x_data = scores_mat[:,axis1_I];
        y_data = scores_mat[:,axis2_I];
        xlabel = 'PC' + str(axis1_I) + ' [' + str(perc_var[axis1_I-1]*100) + '%]';
        ylabel = 'PC' + str(axis2_I) + ' [' + str(perc_var[axis2_I-1]*100) + '%]';
        title = 'Scores';
        text_labels = sns_sorted;

        return title,xlabel,ylabel,x_data,y_data,text_labels,samples
    def _extractPCAScores_tablerows(self,data_I,axis1_I=1,axis2_I=2):
        '''extract out pca data from [{},{},{}] format'''
        
        # determine the number of samples and axes
        sns = []
        axes = []
        cus = []
        for d in data_I:
                sns.append(d['sample_name_short']);
                axes.append(d['axis'])
                cus.append(d['calculated_concentration_units'])
        sns_sorted = sorted(set(sns))
        axes_sorted = sorted(set([axis1_I,axis2_I]))
        cus_sorted = sorted(set(cus))
        #extract out all axes
        data_O = [];
        for i,r in enumerate(sns_sorted):
            for k,z in enumerate(cus_sorted):
                cus_tmp = {};
                for j,c in enumerate(axes_sorted):
                    tmp = {};
                    for d in data_I:
                        if d['sample_name_short'] == r and d['axis'] == c and d['calculated_concentration_units'] == z:
                            tmp['score_'+str(c)] = d['score'];
                            tmp['var_proportion_'+str(c)] = d['var_proportion'];
                            tmp['var_cumulative_'+str(c)] = d['var_cumulative'];
                            tmp['axislabel'+str(c)] = 'PC' + str(c) + ' [' + str(d['var_proportion']*100) + '%]';
                            if j==0:
                                tmp['sample_name_abbreviation'] = d['sample_name_abbreviation'];
                                tmp['sample_name_short'] = d['sample_name_short'];
                                tmp['calculated_concentration_units'] = d['calculated_concentration_units'];
                                tmp['analysis_id'] = d['analysis_id'];
                            break;
                    if tmp: cus_tmp.update(tmp);
                if cus_tmp: data_O.append(cus_tmp);

        return data_O;
    def _extractPCALoadings(self,data_I,axis1_I=1,axis2_I=2):
        '''extract out pca data from [{},{},{}] format'''
        x_data = [];
        y_data = [];
        xlabel = '';
        ylabel = '';
        title = '';
        text_labels = [];
        
        # determine the number of samples and axes
        cn = []
        axes = []
        for d in data_I:
                cn.append(d['component_group_name']);
                axes.append(d['axis'])
        cn_sorted = sorted(set(cn))
        axes_sorted = sorted(set(axes))
        #extract out all axes
        loadings_mat = numpy.zeros((len(cn_sorted),len(axes_sorted)));
        for i,r in enumerate(cn_sorted):
            for j,c in enumerate(axes_sorted):
                for d in data_I:
                    if d['component_group_name'] == r and d['axis'] == c:
                        loadings_mat[i,j] = d['loadings'];
        #extract out specified axis
        x_data = loadings_mat[:,axis1_I];
        y_data = loadings_mat[:,axis2_I];
        xlabel = 'Loadings' + str(axis1_I);
        ylabel = 'Loadings' + str(axis2_I);
        title = 'Loadings';
        text_labels = cn_sorted;

        return title,xlabel,ylabel,x_data,y_data,text_labels
    def _extractPCALoadings_tablerows(self,data_I,axis1_I=1,axis2_I=2):
        '''extract out pca data from [{},{},{}] format'''
        
        # determine the number of samples and axes
        cn = []
        axes = []
        cus = []
        for d in data_I:
                cn.append(d['component_name']);
                axes.append(d['axis'])
                cus.append(d['calculated_concentration_units'])
        cn_sorted = sorted(set(cn))
        axes_sorted = sorted(set([axis1_I,axis2_I]))
        cus_sorted = sorted(set(cus))
        #extract out all axes
        data_O = [];
        for i,r in enumerate(cn_sorted):
            for k,z in enumerate(cus_sorted):
                cus_tmp = {};
                for j,c in enumerate(axes_sorted):
                    tmp = {};
                    for d in data_I:
                        if d['component_name'] == r and d['axis'] == c and d['calculated_concentration_units'] == z:
                            tmp['loadings_'+str(c)] = d['loadings'];
                            tmp['axislabel'+str(c)] = 'Loadings' + str(c);
                            if j==0:
                                tmp['component_group_name'] = d['component_group_name'];
                                tmp['component_name'] = d['component_name'];
                                tmp['calculated_concentration_units'] = d['calculated_concentration_units'];
                                tmp['analysis_id'] = d['analysis_id'];
                            break;
                    if tmp: cus_tmp.update(tmp);
                if cus_tmp: data_O.append(cus_tmp);

        return data_O;
    def heatPlot(self,title_I):
        #TODO:
        # Generate some test data
        x = np.random.randn(8873)
        y = np.random.randn(8873)

        heatmap, xedges, yedges = np.histogram2d(x, y, bins=(50,50))
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        cb = plt.colorbar()
        cb.set_label('mean value')

        plt.clf()
        #plt.imshow(heatmap, extent=extent) #inverts the image
        plt.imshow(heatmap.T, extent=extent, origin = 'lower')
        plt.show()
    def scatterLinePlot(self,title_I,xlabel_I,ylabel_I,x_data_I,y_data_I,text_labels_I=[],fit_func_I='linear',show_eqn_I=True,show_r2_I=True,filename_I=None,show_plot_I=True):
        '''Create a scatter line plot and fitted line'''
        # Create the fit:
        if fit_func_I == 'linear':
            slope, intercept, r_value, p_value, std_err = linregress(x_data_I, y_data_I);
            r2 = r_value**2; #coefficient of determination
            x2 = x_data_I;
            y2 = [];
            for d in x2:
                y2.append(d*slope+intercept);
        elif fit_func_I=='lowess':
            #lowess
            x2 = numpy.array(x_data_I);
            y2_lowess = lowess.lowess(x2,numpy.array(y_data_I),f=0.1,iter=100)
            y2 = numpy.zeros_like(y2_lowess);
            for i,y2s in enumerate(y2_lowess):
                if i==0:
                    y2[i] = y2s;
                elif i!=0 and y2s<y2[i-1]:
                    y2[i] = y2[i-1];
                else:
                    y2[i] = y2s;
        # Create a Figure object.
        fig = plt.figure()
        # Create an Axes object.
        ax = fig.add_subplot(1,1,1) # one row, one column, first plot
        # Plot the data.
        ax.scatter(x_data_I, y_data_I, color="blue", marker="o")
        ax.plot(x2,y2,color='red',linestyle='-')
        # Add a title.
        ax.set_title(title_I)
        # Add some axis labels.
        ax.set_xlabel(xlabel_I)
        ax.set_ylabel(ylabel_I)
        # Label data points.
        if text_labels_I:
            for i, txt in enumerate(text_labels_I):
                ax.annotate(txt, (x_data_I[i],y_data_I[i]))
        # Show fit equation
        if show_eqn_I:
            fit_eqn = "y = " + str(slope) + "*x";
            if intercept < 0: fit_eqn += " " + str(intercept);
            elif intercept > 0: fit_eqn += " +" + str(intercept);
            ax.annotate(fit_eqn,(min(x_data_I),max(y_data_I)));
        # Show r2 value
        if show_r2_I:
            r2_label = "r2 = " + str(r2);
            ax.annotate(r2_label,(min(x_data_I),max(y_data_I)-0.5));
        # Show legend
        # Produce an image.
        if filename_I:
            fig.savefig(filename_I)
        # Show the image.
        if show_plot_I:
            plt.show();
    def multiScatterLinePlot(self,title_I,xlabel_I,ylabel_I,x_data_I=[],y_data_I=[],data_labels_I=[],text_labels_I=[],fit_func_I='linear',show_eqn_I=True,show_r2_I=True,filename_I=None,show_plot_I=True,show_legend_I=True):
        '''Create a scatter line plot and fitted line'''
        #Input:
        #   x_data_I = [[a1,a2,a3...],[b1,b2,b3,...],...] of type float
        #   y_data_I = [[a1,a2,a3...],[b1,b2,b3,...],...] of type float
        #   data_labels_I = [a,b,...] of type string
        #   text_labels_I = [[a1,a2,a3...],[b1,b2,b3,...],...] of type string
        
        # Create a Figure object.
        fig = plt.figure()
        # Create an Axes object.
        ax = fig.add_subplot(1,1,1) # one row, one column, first plot
        # Generate colors
        colors=iter(cm.rainbow(numpy.linspace(0,1,len(x_data_I))))

        for cnt_data, data in enumerate(y_data_I):
            # Create the fit:
            if fit_func_I == 'linear':
                slope, intercept, r_value, p_value, std_err = linregress(x_data_I[cnt_data], y_data_I[cnt_data]);
                r2 = r_value**2; #coefficient of determination
                x2 = x_data_I;
                y2 = [];
                for d in x2:
                    y2.append(d*slope+intercept);
            elif fit_func_I=='lowess':
                #lowess
                x2 = numpy.array(x_data_I[cnt_data]);
                y2_lowess = lowess.lowess(x2,numpy.array(y_data_I[cnt_data]),f=0.1,iter=100)
                y2 = numpy.zeros_like(y2_lowess);
                for i,y2s in enumerate(y2_lowess):
                    if i==0:
                        y2[i] = y2s;
                    elif i!=0 and y2s<y2[i-1]:
                        y2[i] = y2[i-1];
                    else:
                        y2[i] = y2s;
            # Plot the data.
            c = next(colors);
            ax.scatter(x_data_I[cnt_data], y_data_I[cnt_data],color=c, marker="o",label=data_labels_I[cnt_data])
            if fit_func_I:
                ax.plot(x2,y2,linestyle='-',color=c,label=data_labels_I[cnt_data]+'_fitted')
            # Add a title.
            ax.set_title(title_I)
            # Add some axis labels.
            ax.set_xlabel(xlabel_I)
            ax.set_ylabel(ylabel_I)
            # Label data points.
            if text_labels_I:
                for i, txt in enumerate(text_labels_I[cnt_data]):
                    ax.annotate(txt, (x_data_I[cnt_data][i],y_data_I[cnt_data][i]))
            # Show fit equation
            if fit_func_I == 'linear' and show_eqn_I:
                fit_eqn = "y = " + str(slope) + "*x";
                if intercept < 0: fit_eqn += " " + str(intercept);
                elif intercept > 0: fit_eqn += " +" + str(intercept);
                ax.annotate(fit_eqn,(min(x_data_I[cnt_data]),max(y_data_I[cnt_data])));
            # Show r2 value
            if fit_func_I == 'linear' and show_r2_I:
                r2_label = "r2 = " + str(r2);
                ax.annotate(r2_label,(min(x_data_I[cnt_data]),max(y_data_I[cnt_data])-0.5));

        # Show legend
        if show_legend_I:
            plt.legend(loc='best');
        # Produce an image.
        if filename_I:
            fig.savefig(filename_I)
        # Show the image.
        if show_plot_I:
            plt.show();
    def multiPanelBarPlot(self,title_I,xticklabels_I,xlabel_I,ylabel_I,panelLabels_I,mean_I,var_I=None,se_I=None,add_labels_I=True):
        
        #definitions
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                if rect.get_y()>=0:
                    ax.text(rect.get_x()+rect.get_width()/2., 1.1*height, numpy.round(height,decimals=3),
                            ha='center', va='bottom')
                else:
                    ax.text(rect.get_x()+rect.get_width()/2., -1.1*height, -numpy.round(height,decimals=3),
                            ha='center', va='bottom')
        # Calculate the number of panels
        if len(panelLabels_I)<=6:
            panel_rows = 3;
        elif len(panelLabels_I)>6:
            panel_rows = 4;
        panel_columns = int(ceil(float(len(panelLabels_I))/float(panel_rows)));
        # Create a Figure object.
        fig = plt.figure();
        for panel_cnt,panel in enumerate(panelLabels_I):
            # Create an Axes object.
            ax = fig.add_subplot(panel_rows,panel_columns,panel_cnt) # row, column, element
            
            #calculate the stdev
            if var_I:
                stdev = [sqrt(x) for x in var_I[panel_cnt]];
            elif se_I:
                stdev = se_I[panel_cnt]; # use standard error instead
            else:
                stdev = None;

            ind = numpy.arange(len(mean_I[panel_cnt]))  # the x locations for the groups
            width = 0.5       # the width of the bars

            rects1 = ax.bar(ind, mean_I[panel_cnt], width, color='r', yerr=stdev)

            # add some
            ax.set_ylabel(ylabel_I)
            ax.set_xlabel(xlabel_I)
            ax.set_title(panel)
            ax.set_xticks(ind+width)
            ax.set_xticklabels(xticklabels_I[panel_cnt])

            if add_labels_I: autolabel(rects1)

            #force scientific notation
            #ax.get_xaxis().get_major_formatter().set_scientific(True)
            #ax.get_yaxis().get_major_formatter().set_scientific(True)
            #ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        plt.show()
    def histogram(self,data_I,title_I=None,label_I=None,bins_I=50,range_I=None):
        '''Generate a histogram using matplotlib'''

        plt.figure()
        n, bins, patches = plt.hist(data_I,bins_I,label = label_I)
        plt.legend()
        plt.show()
        