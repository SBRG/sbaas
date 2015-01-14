from sys import exit
from math import log, sqrt, exp
import csv
import numpy
from analysis.analysis_base.base_analysis import base_analysis

from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
r = robjects.r

class r_calculate(base_analysis):
    def __init__(self):
        self.stats = importr('stats');
        self.tools = importr('tools');
        self._import_RPackages();

    def _import_RPackages(self):
        '''load required R packages
        NOTE: must be run as administrator if packages need to be installed!'''

        #lib_loc = '"C:/Users/Douglas/Documents/Douglas/R/win-library/3.0"';
        #r_statement = ('library("Amelia",lib.loc = %s)' % lib_loc);
        #Amelia (missing value imputation)
        try:
            r_statement = ('library("Amelia")');
            ans = robjects.r(r_statement);
            r_statement = ('require(Amelia)');
            ans = robjects.r(r_statement);
        except:
            r_statement = ('install.packages("Amelia")');
            ans = robjects.r(r_statement);
            r_statement = ('library("Amelia")');
            ans = robjects.r(r_statement);
            r_statement = ('require(Amelia)');
            ans = robjects.r(r_statement);
        #Upgrade bioconductor
        r_statement = ('source("http://bioconductor.org/biocLite.R")');
        ans = robjects.r(r_statement);
        r_statement = ('biocLite("BiocUpgrade")');
        ans = robjects.r(r_statement);
        #Biobase
        try:
            r_statement = ('library("Biobase")');
            ans = robjects.r(r_statement);
            r_statement = ('require(Biobase)');
            ans = robjects.r(r_statement);
        except:
            r_statement = ('source("http://bioconductor.org/biocLite.R")');
            ans = robjects.r(r_statement);
            r_statement = ('biocLite("Biobase")');
            ans = robjects.r(r_statement);
            r_statement = ('library("Biobase")');
            ans = robjects.r(r_statement);
            r_statement = ('require(Biobase)');
            ans = robjects.r(r_statement);
        #LMGene (glog)
        try:
            r_statement = ('library("LMGene")');
            ans = robjects.r(r_statement);
            r_statement = ('require(LMGene)');
            ans = robjects.r(r_statement);
        except:
            r_statement = ('source("http://bioconductor.org/biocLite.R")');
            ans = robjects.r(r_statement);
            r_statement = ('biocLite("LMGene")');
            ans = robjects.r(r_statement);
            r_statement = ('library("LMGene")');
            ans = robjects.r(r_statement);
            r_statement = ('require(LMGene)');
            ans = robjects.r(r_statement);
        #mixOmics (plsda, pca, clustering)
        #an alternative for plsda would be "caret"
        try:
            r_statement = ('library("mixOmics")');
            ans = robjects.r(r_statement);
            r_statement = ('require(mixOmics)');
            ans = robjects.r(r_statement);
        except:
            r_statement = ('install.packages("mixOmics")');
            ans = robjects.r(r_statement);
            r_statement = ('library("mixOmics")');
            ans = robjects.r(r_statement);
            r_statement = ('require(mixOmics)');
            ans = robjects.r(r_statement);
        #pcaMethods (missing value and pca analysis)
        try:
            r_statement = ('library("pcaMethods")');
            ans = robjects.r(r_statement);
            r_statement = ('require(pcaMethods)');
            ans = robjects.r(r_statement);
        except:
            r_statement = ('source("http://bioconductor.org/biocLite.R")');
            ans = robjects.r(r_statement);
            r_statement = ('biocLite("pcaMethods")');
            ans = robjects.r(r_statement);
            r_statement = ('library("pcaMethods")');
            ans = robjects.r(r_statement);
            r_statement = ('require(pcaMethods)');
            ans = robjects.r(r_statement);

    def _make_ExpressionSet(self, data_I):
        '''make an ExpressionSet datafram for use with Bioconductor packages'''
        #all variables will be loaded into the R workspace

        #format into R matrix and list objects
        # convert data dict to matrix filling in missing values
        # with 'NA'
        sns = []
        cgn = []
        replicates = [];
        for d in data_I:
                sns.append(d['sample_name_short']);    
                replicates.append(d['sample_replicate']);   
                cgn.append(d['component_name']);
        sns_sorted = sorted(set(sns))
        replicates_sorted = sorted(set(replicates))
        cgn_sorted = sorted(set(cgn))
        concentrations = ['NA' for r in range(len(sns_sorted)*len(cgn_sorted))];
        cnt = 0;
        cnt_bool = True;
        cnt_reps = 0;
        sna = []
        replicates = []
        for c in cgn_sorted:
                for s in sns_sorted:
                    if cnt_bool:
                        sna.append(d['sample_name_abbreviation']);
                        replicates.append(replicates_sorted[cnt_reps]); 
                        if cnt_reps < len(replicates_sorted)-1:
                            cnt_reps+=1;
                        else:
                            cnt_reps=0;
                    for d in data_I:
                        if d['sample_name_short'] == s and d['component_name'] == c:
                            if d['calculated_concentration']:
                                concentrations[cnt] = d['calculated_concentration'];
                                break;
                    cnt = cnt+1
                cnt_bool = False;
        # check if there were any missing values in the data set in the first place
        mv = 0;
        for c in concentrations:
            if c=='NA':
                mv += 1;
        if mv>0:
            # Call to R
            try:
                # convert lists to R matrix
                concentrations_r = '';
                for c in concentrations:
                    concentrations_r = (concentrations_r + ',' + str(c));
                concentrations_r = concentrations_r[1:];
                r_statement = ('concentrations = c(%s)' % concentrations_r);
                ans = robjects.r(r_statement);
                r_statement = ('concentrations_m = matrix(concentrations, nrow = %s, ncol = %s, byrow = TRUE)' %(len(cgn_sorted),len(sns_sorted)));
                ans = robjects.r(r_statement);
            except Exception as e:
                print(e);
                exit(-1);
            # Call to R
            try:
                # convert lists to R list
                sna_r = '';
                for c in sna:
                    sna_r = (sna_r + ',' + c);
                sna_r = sna_r[1:];
                replicates_r = '';
                for c in replicates:
                    replicates_r = (replicates_r + ',' + c);
                replicates_r = replicates_r[1:];
                r_statement = ('sna = c(%s)' % sna_r);
                ans = robjects.r(r_statement);
                r_statement = ('replicates = c(%s)' % replicates_r);
                ans = robjects.r(r_statement);
                r_statement = ('concentrations_l = list(sna=sna,replicates=replicates)');
                ans = robjects.r(r_statement);
            except Exception as e:
                print(e);
                exit(-1);
            try:
                #convert to Expression Set
                concentrations_r = '';
                for c in concentrations:
                    concentrations_r = (concentrations_r + ',' + str(c));
                concentrations_r = concentrations_r[1:];
                r_statement = ('eS = neweS(concentrations_m,concentrations_l)');
                ans = robjects.r(r_statement);
            except Exception as e:
                print(e);
                exit(-1);
            
    # calls to R
    def calculate_ave_CV_R(self,data_I):
        # calculate average and CV of data
        # Call to R
        try:
            # convert lists to R objects
            data_R = robjects.FloatVector(data_I);

            data_ave_R = self.stats.ave(data_R);
            data_ave_O = data_ave_R.rx2(1)[0];

            data_var_R = self.stats.var(data_R);
            data_var = data_var_R.rx2(1)[0];
            data_CV_O = sqrt(data_var)/data_ave_O*100;

            return data_ave_O, data_CV_O;
        except:
            print('error in R')
    def calculate_ave_var_R(self,data_I):
        # calculate average and CV of data
        # Call to R
        try:
            # convert lists to R objects
            data_R = robjects.FloatVector(data_I);

            data_ave_R = self.stats.ave(data_R);
            data_ave_O = data_ave_R.rx2(1)[0];

            data_var_R = self.stats.var(data_R);
            data_var_O = data_var_R.rx2(1)[0];

            return data_ave_O, data_var_O;
        except Exception as e:
            print(e);
            exit(-1);
    def calculate_missingValues(self,data_I,n_imputations_I = 1000):
        # calculate missing values using the AmeliaII R package
        # 1000 imputations (default) are computed and averaged to generate
        # the resulting data without missing values

        # convert data dict to matrix filling in missing values
        # with 'NA'
        sns = []
        cgn = []
        for d in data_I:
                sns.append(d['sample_name_short']);
                cgn.append(d['component_name']);
        sns_sorted = sorted(set(sns))
        cgn_sorted = sorted(set(cgn))
        concentrations = ['NA' for r in range(len(sns_sorted)*len(cgn_sorted))];
        cnt = 0;
        for c in cgn_sorted:
                for s in sns_sorted:
                    for d in data_I:
                        if d['sample_name_short'] == s and d['component_name'] == c:
                            if d['calculated_concentration']:
                                concentrations[cnt] = d['calculated_concentration'];
                                break;
                    cnt = cnt+1

        sns_O = [];
        cn_O = [];
        cc_O = [];
        # check if there were any missing values in the data set in the first place
        mv = 0;
        for c in concentrations:
            if c=='NA':
                mv += 1;
        if mv>0:
            # Call to R
            try:
                # convert lists to R objects
                # concentrations_R = robjects.FloatVector(concentrations);
                concentrations_r = '';
                for c in concentrations:
                    concentrations_r = (concentrations_r + ',' + str(c));
                concentrations_r = concentrations_r[1:];
                r_statement = ('concentrations = c(%s)' % concentrations_r);
                ans = robjects.r(r_statement);
                r_statement = 'concentrations_log = log(concentrations)'
                ans = robjects.r(r_statement);
                r_statement = ('concentrations_m = matrix(concentrations_log, nrow = %s, ncol = %s, byrow = TRUE)' %(len(cgn_sorted),len(sns_sorted)));
                ans = robjects.r(r_statement);
                r_statement = ('a.out = amelia(concentrations_m, m=%s)' % n_imputations_I);
                ans = robjects.r(r_statement);
                # direct calls to R
           
                # extract out data matrices
                concentrations_2d = numpy.zeros((len(cgn_sorted)*len(sns_sorted),n_imputations_I));
                for n in range(n_imputations_I):
                    cnt_data = 0;
                    for d in ans.rx2('imputations')[0]:
                        #NOTE: the matrix is linearized by column (opposite of how the matrix was made)
                        concentrations_2d[cnt_data,n] = exp(d);
                        cnt_data = cnt_data + 1;
                # calculate the average
                concentrations_1d_ave = numpy.zeros((len(cgn_sorted)*len(sns_sorted)));
                cnt_imputations = 0;
                for n in range(len(cgn_sorted)*len(sns_sorted)):
                    concentrations_1d_ave[n] = numpy.average(concentrations_2d[n][:]);
                # convert array back to dict
                #data_O = [];
                for c in range(len(sns_sorted)):
                    for r in range(len(cgn_sorted)):
                        #data_tmp = {};
                        #data_tmp['sample_name_short'] = sns_sorted[c]
                        #data_tmp['component_name'] = cgn_sorted[r]
                        #data_tmp['calculated_concentration'] = concentrations_1d_ave[c*len(sns_sorted)+r];
                        #data_O.append(data_tmp);
                        if isinstance(concentrations_1d_ave[c*len(cgn_sorted)+r], (int, long, float)) and not numpy.isnan(concentrations_1d_ave[c*len(cgn_sorted)+r]):
                            sns_O.append(sns_sorted[c]);
                            cn_O.append(cgn_sorted[r]);
                            cc_O.append(concentrations_1d_ave[c*len(cgn_sorted)+r]);

            # expand the array
            #concentrations_2d_ave = numpy.zeros((len(cgn_sorted),len(sns_sorted))); # transpose of input
            #for c in range(len(sns_sorted)):
            #    for r in range(len(cgn_sorted)):
            #        concentrations_2d_ave[r][c] = concentrations_1d_ave[c*len(sns_sorted)+r];

            except Exception as e:
                print(e);
                exit(-1);
        else:
            for r in range(len(cgn_sorted)):
                for c in range(len(sns_sorted)):
                    #data_O.append(data_tmp);
                    sns_O.append(sns_sorted[c]);
                    cn_O.append(cgn_sorted[r]);
                    cc_O.append(concentrations[r*len(sns_sorted)+c]);

        # reformat the matrix of element averages to dict
        return sns_O,cn_O,cc_O; #data_O;
    def calculate_glogNormalization(self,data_I):
        '''normalize the data using a glog transformation using LMGene'''

        #make the ExpressionSet
        
        #format into R matrix and list objects
        # convert data dict to matrix filling in missing values
        # with 'NA'
        sns = []
        cgn = []
        replicates = [];
        for d in data_I:
                sns.append(d['sample_name_short']);    
                replicates.append(d['sample_replicate']);   
                cgn.append(d['component_name']);
        sns_sorted = sorted(set(sns))
        replicates_sorted = sorted(set(replicates))
        cgn_sorted = sorted(set(cgn))
        concentrations = ['NA' for r in range(len(sns_sorted)*len(cgn_sorted))];
        cnt = 0;
        cnt_bool = True;
        cnt_reps = 0;
        sna = []
        replicates = []
        for c in cgn_sorted:
                for s in sns_sorted:
                    for d in data_I:
                        if d['sample_name_short'] == s and d['component_name'] == c:
                            if d['calculated_concentration']:
                                concentrations[cnt] = d['calculated_concentration'];
                                if cnt_bool:
                                    sna.append(d['sample_name_abbreviation']);
                                    replicates.append(replicates_sorted[cnt_reps]); 
                                    if cnt_reps < len(replicates_sorted)-1:
                                        cnt_reps+=1;
                                    else:
                                        cnt_reps=0;
                                break;
                    cnt = cnt+1
                cnt_bool = False;
        # check if there were any missing values in the data set in the first place
        mv = 0;
        for c in concentrations:
            if c=='NA':
                mv += 1;
        if mv==0:
            # Call to R
            try:
                # convert lists to R matrix
                concentrations_r = '';
                for c in concentrations:
                    concentrations_r = (concentrations_r + ',' + str(c));
                concentrations_r = concentrations_r[1:];
                r_statement = ('concentrations = c(%s)' % concentrations_r);
                ans = robjects.r(r_statement);
                r_statement = ('concentrations_m = matrix(concentrations, nrow = %s, ncol = %s, byrow = TRUE)' %(len(cgn_sorted),len(sns_sorted)));
                ans = robjects.r(r_statement);
                # convert lists to R list
                sna_r = '';
                for c in sna:
                    sna_r = (sna_r + ',' + '"' + c + '"');
                sna_r = sna_r[1:];
                replicates_r = '';
                for c in replicates:
                    replicates_r = (replicates_r + ',' + str(c));
                replicates_r = replicates_r[1:];
                r_statement = ('sna = c(%s)' % sna_r);
                ans = robjects.r(r_statement);
                r_statement = ('replicates = c(%s)' % replicates_r);
                ans = robjects.r(r_statement);
                r_statement = ('concentrations_l = list(sna=sna,replicates=replicates)');
                ans = robjects.r(r_statement);
                #convert to Expression Set
                r_statement = ('eS = neweS(concentrations_m,concentrations_l)');
                ans = robjects.r(r_statement);
                #estimate the parameters for g-log transformation
                #r_statement = ('tranpar = tranest(eS)');
                #r_statement = ('tranpar = tranest(eS, lowessnorm=TRUE)');
                #r_statement = ('tranpar = tranest(eS, mult=TRUE, lowessnorm=TRUE)');
                r_statement = ('tranpar = tranest(eS, mult=TRUE)'); # Matches metabo-analyst and produces the most uniform distribution
                ans = robjects.r(r_statement);
                r_statement = ('eS_transformed <- transeS(eS, tranpar$lambda, tranpar$alpha)');
                ans = robjects.r(r_statement);
                # extract out data matrices
                r_statement = ('exprs(eS_transformed)');
                ans = robjects.r(r_statement);
                concentrations_glog = numpy.array(ans);
                # convert array back to dict
                data_O = [];
                for c in range(len(sns_sorted)):
                    for r in range(len(cgn_sorted)):
                        if isinstance(concentrations_glog[r,c], (int, long, float, complex)):
                            data_tmp = {};
                            data_tmp['sample_name_short'] = sns_sorted[c]
                            data_tmp['component_name'] = cgn_sorted[r]
                            data_tmp['calculated_concentration'] = concentrations_glog[r,c];
                            data_O.append(data_tmp);
                            #sns_O.append(sns_sorted[c]);
                            #cn_O.append(cgn_sorted[r]);
                            #cc_O.append(ans[c*len(cgn_sorted)+r]);
            except Exception as e:
                print(e);
                exit(-1);

        # reshape original concentrations
        concentrations_original = numpy.array(concentrations);
        concentrations = concentrations_original.reshape(len(cgn_sorted),len(sns_sorted));
        return data_O, concentrations, concentrations_glog;
    def calculate_anova(self,data_I):
        '''calculate the 1-way anova using R's built in Stats package
        Note: 1-way anova is equivalent to an independent t-test'''

        #make the dataFrame
        
        #format into R matrix and list objects
        # convert data dict to matrix filling in missing values
        # with 'NA'
        sns = []
        cn = []
        replicates = [];
        for d in data_I:
                sns.append(d['sample_name_short']);    
                replicates.append(d['sample_replicate']);   
                cn.append(d['component_name']);
        sns_sorted = sorted(set(sns))
        replicates_sorted = sorted(set(replicates))
        cn_sorted = sorted(set(cn))
        concentrations = ['NA' for r in range(len(sns_sorted)*len(cn_sorted))];
        cnt = 0;
        cnt_bool = True;
        cnt_reps = 0;
        sna = []
        replicates = []
        for c in cn_sorted:
                for s in sns_sorted:
                    for d in data_I:
                        if d['sample_name_short'] == s and d['component_name'] == c:
                            if d['calculated_concentration']:
                                concentrations[cnt] = d['calculated_concentration'];
                                if cnt_bool:
                                    sna.append(d['sample_name_abbreviation']);
                                    replicates.append(replicates_sorted[cnt_reps]); 
                                    if cnt_reps < len(replicates_sorted)-1:
                                        cnt_reps+=1;
                                    else:
                                        cnt_reps=0;
                                break;
                    cnt = cnt+1
                cnt_bool = False;
        # check that there is only one component_name:
        if len(cn_sorted)>1:
            print 'more than one component detected!'
            return None,None;
        #check if there were any missing values in the data set in the first place
        mv = 0;
        for c in concentrations:
            if c=='NA':
                mv += 1;
        if mv==0:
            # Call to R
            try:
                # convert lists to R matrix
                concentrations_r = '';
                for c in concentrations:
                    concentrations_r = (concentrations_r + ',' + str(c));
                concentrations_r = concentrations_r[1:];
                r_statement = ('concentrations_v = c(%s)' % concentrations_r);
                ans = robjects.r(r_statement);
                # convert lists to R list
                sna_r = '';
                for c in sna:
                    sna_r = (sna_r + ',' + '"' + c + '"');
                sna_r = sna_r[1:];
                r_statement = ('sna_v = c(%s)' % sna_r);
                ans = robjects.r(r_statement);
                # get basic stats
                mean = None; #same order as sna
                var = None;
                n = None;
                r_statement = ('tapply(concentrations_v,sna_v,mean)'); # calculate the mean
                ans = robjects.r(r_statement);
                mean = numpy.array(ans);
                r_statement = ('tapply(concentrations_v,sna_v,var)'); # calculate the variance
                ans = robjects.r(r_statement);
                var = numpy.array(ans);
                r_statement = ('tapply(concentrations_v,sna_v,length)'); # calculate the # of samples
                ans = robjects.r(r_statement);
                n = numpy.array(ans);
                #convert to Data Frame
                r_statement = ('dF = data.frame(concentrations_v,sna_v)');
                ans = robjects.r(r_statement);
                r_statement = ('names(dF) = c("concentrations","sna")');
                ans = robjects.r(r_statement);
                r_statement = ('attach(dF)');
                ans = robjects.r(r_statement);
                # call anova
                r_statement = ('aov.out = aov(concentrations ~ sna, data=dF)'); # call anova
                ans = robjects.r(r_statement);
                r_statement = ('summary(aov.out)'); # anova summary
                ans = robjects.r(r_statement);
                f_stat = ans[0].rx2('F value')[0] # f_value
                pvalue = ans[0].rx2('Pr(>F)')[0] # pvalue
                # other attributes available: ['Df', 'Sum Sq', 'Mean Sq', 'F value', 'Pr(>F)']
                r_statement = ('TukeyHSD(aov.out)'); # TukeyHSD post Hoc
                ans = robjects.r(r_statement);
                postHocTest = [x for x in ans[0].rownames];
                # ans[0].colnames
                # ['diff', 'lwr', 'upr', 'p adj']
                postHocTest_pvalue = [x for x in numpy.array(ans[0])[:,3]];
                postHocTest_description = 'TukeyHSD'
                # convert array back to dict
                data_anova = [];
                data_pairwise = [];
                # extract out unique sna's in order
                sna_set = [];
                for s in sna:
                    if not(s in sna_set):
                        sna_set.append(s);
                for r in range(len(cn_sorted)):
                    data_tmp = {};
                    data_tmp['sample_name_abbreviation'] = sna_set;
                    data_tmp['component_name'] = cn_sorted[r];
                    data_tmp['test_stat'] = f_stat;
                    data_tmp['test_description'] = '1-way ANOVA; F value';
                    data_tmp['pvalue'] = pvalue;
                    data_tmp['pvalue_corrected'] = None;
                    data_tmp['pvalue_corrected_description'] = None;
                    data_anova.append(data_tmp);
                ## extract out unique sna's in order
                #sna_set = [];
                #for s in sna:
                #    if not(s in sna_set):
                #        sna_set.append(s);
                #for c in range(len(sna_set)):
                #    # extract out post hoc results
                #    postHocTest_tmp = '';
                #    PostHocTest_pvalue_tmp = None;
                #    for r in range(len(cn_sorted)):
                #        data_tmp = {};
                #        data_tmp['sample_name_abbreviation'] = sna_set[c];
                #        data_tmp['component_name'] = cn_sorted[r];
                #        data_tmp['mean'] = mean[c];
                #        data_tmp['var'] = var[c];
                #        data_tmp['n'] = n[c];
                #        data_tmp['test_stat'] = f_stat;
                #        data_tmp['test_description'] = 'F value';
                #        data_tmp['pvalue'] = pvalue;
                #        data_tmp['pvalue_corrected'] = pvalue;
                #        data_tmp['pvalue_corrected_description'] = '1-way ANOVA';
                #        data_tmp['postHocTest'] = postHocTest
                #        data_tmp['postHocTest_pvalue'] = postHocTest_pvalue
                #        data_tmp['postHocTest_description'] = postHocTest_description
                #        data_O.append(data_tmp);
                # extract out unique sna's in order
                for c1 in range(len(sna_set)):
                    for c2 in range(len(sna_set)):
                        if c1 != c2:
                            # extract out post hoc results
                            PostHocTest_tmp = '';
                            PostHocTest_pvalue_tmp = None;
                            foldChange = None;
                            for i,pht in enumerate(postHocTest):
                                if sna_set[c1] in pht and sna_set[c2] in pht:
                                    PostHocTest_tmp = sna_set[c2];
                                    PostHocTest_pvalue_tmp = postHocTest_pvalue[i];
                                    foldChange = mean[c2]/mean[c1];
                            for r in range(len(cn_sorted)):
                                data_tmp = {};
                                data_tmp['sample_name_abbreviation_1'] = sna_set[c1];
                                data_tmp['sample_name_abbreviation_2'] = PostHocTest_tmp;
                                data_tmp['component_name'] = cn_sorted[r];
                                data_tmp['mean'] = None;
                                #data_tmp['mean'] = mean[c1];
                                #data_tmp['var'] = var[c1];
                                #data_tmp['n'] = n[c1];
                                data_tmp['test_stat'] = None;
                                data_tmp['test_description'] = postHocTest_description;
                                data_tmp['pvalue'] = PostHocTest_pvalue_tmp;
                                data_tmp['pvalue_corrected'] = None;
                                data_tmp['pvalue_corrected_description'] = None;
                                data_tmp['ci_lb'] = None;
                                data_tmp['ci_ub'] = None;
                                data_tmp['ci_level'] = None;
                                data_tmp['fold_change'] = foldChange;
                                data_pairwise.append(data_tmp);
            except Exception as e:
                print(e);
                exit(-1);
        return data_anova,data_pairwise;
    def calculate_pairwiseTTest(self,data_I,pooled_sd_I = "FALSE", paired_I="TRUE",padjusted_method_I = "bonferroni",alternative_I = "two.sided"):
        '''calculate a pairwise t-test using R's built in Stats package'''
        # padjusted_methods: ("holm", "hochberg", "hommel", "bonferroni", "BH", "BY", "fdr", "none"
        # alternative_tests: ("greater","less","two.sided")
        # Note pooled_sd and paired cannot both be True

        #make the dataFrame
        
        #format into R matrix and list objects
        # convert data dict to matrix filling in missing values
        # with 'NA'
        sns = []
        cn = []
        replicates = [];
        for d in data_I:
                sns.append(d['sample_name_short']);    
                replicates.append(d['sample_replicate']);   
                cn.append(d['component_name']);
        sns_sorted = sorted(set(sns))
        replicates_sorted = sorted(set(replicates))
        cn_sorted = sorted(set(cn))
        concentrations = ['NA' for r in range(len(sns_sorted)*len(cn_sorted))];
        cnt = 0;
        cnt_bool = True;
        cnt_reps = 0;
        sna = []
        replicates = []
        for c in cn_sorted:
                for s in sns_sorted:
                    for d in data_I:
                        if d['sample_name_short'] == s and d['component_name'] == c:
                            if d['calculated_concentration']:
                                concentrations[cnt] = d['calculated_concentration'];
                                if cnt_bool:
                                    sna.append(d['sample_name_abbreviation']);
                                    replicates.append(replicates_sorted[cnt_reps]); 
                                    if cnt_reps < len(replicates_sorted)-1:
                                        cnt_reps+=1;
                                    else:
                                        cnt_reps=0;
                                break;
                    cnt = cnt+1
                cnt_bool = False;
        if len(cn_sorted)>0:
            print 'more than one component detected!'
            return None;
        # check if there were any missing values in the data set in the first place
        mv = 0;
        for c in concentrations:
            if c=='NA':
                mv += 1;
        if mv==0:
            # Call to R
            try:
                # convert lists to R matrix
                concentrations_r = '';
                for c in concentrations:
                    concentrations_r = (concentrations_r + ',' + str(c));
                concentrations_r = concentrations_r[1:];
                r_statement = ('concentrations_v = c(%s)' % concentrations_r);
                ans = robjects.r(r_statement);
                # convert lists to R list
                sna_r = '';
                for c in sna:
                    sna_r = (sna_r + ',' + '"' + c + '"');
                sna_r = sna_r[1:];
                r_statement = ('sna_v = c(%s)' % sna_r);
                ans = robjects.r(r_statement);
                # get basic stats
                mean = None; #same order as sna
                var = None;
                n = None;
                r_statement = ('tapply(concentrations_v,sna_v,mean)'); # calculate the mean
                ans = robjects.r(r_statement);
                mean = numpy.array(ans);
                r_statement = ('tapply(concentrations_v,sna_v,var)'); # calculate the variance
                ans = robjects.r(r_statement);
                var = numpy.array(ans);
                r_statement = ('tapply(concentrations_v,sna_v,length)'); # calculate the # of samples
                ans = robjects.r(r_statement);
                n = numpy.array(ans);
                #convert to Data Frame
                r_statement = ('dF = data.frame(concentrations_v,sna_v)');
                ans = robjects.r(r_statement);
                r_statement = ('names(dF) = c("concentrations","sna")');
                ans = robjects.r(r_statement);
                r_statement = ('attach(dF)');
                ans = robjects.r(r_statement);
                # call paired T-test with without correction
                r_statement = ('pairwise.t.test(concentrations_v, sna_v, p.adjust.method = "none", pool.sd = %s, paired = %s, alternative = "%s")' %(pooled_sd_I, paired_I ,alternative_I));
                ans = robjects.r(r_statement);
                test_description = ans.rx('method')[0][0]
                pvalues = numpy.array(ans.rx('p.value')[0]);
                rownames = numpy.array(ans[2].rownames);
                colnames = numpy.array(ans[2].colnames);
                # call paired T-test with correction
                r_statement = ('pairwise.t.test(concentrations_v, sna_v, p.adjust.method = "%s", pool.sd = %s, paired = %s, alternative = "%s")' %(padjusted_method_I, pooled_sd_I, paired_I ,alternative_I))
                ans = robjects.r(r_statement);
                test_description = ans.rx('method')[0][0]
                pvalues_adjusted = numpy.array(ans.rx('p.value')[0]);
                pvalue_adjusted_description = ans.rx('p.adjust.method')[0][0]
                rownames_adjusted = numpy.array(ans[2].rownames);
                colnames_adjusted = numpy.array(ans[2].colnames);
                # convert array back to dict
                data_pairwise = [];
                # extract out unique sna's in order
                sna_set = [];
                for s in sna:
                    if not(s in sna_set):
                        sna_set.append(s);
                # extract out unique sna's in order
                for c1 in range(len(rownames)):
                    for c2 in range(len(colnames)):
                        if c1 != c2 and pvalues[c1,c2]!='NA':
                            # extract out post hoc results
                            pair = colnames[c2];
                            pvalue = pvalues[c1,c2];
                            pvalue_adjusted = pvalues_adjusted[c1,c2];
                            #foldChange = mean[c2]/mean[c1];
                            for r in range(len(cn_sorted)):
                                data_tmp = {};
                                data_tmp['sample_name_abbreviation_1'] = rownames[c1];
                                data_tmp['sample_name_abbreviation_2'] = pair;
                                data_tmp['component_name'] = cn_sorted[r];
                                #data_tmp['mean'] = mean[c1];
                                #data_tmp['var'] = var[c1];
                                #data_tmp['n'] = n[c1];
                                data_tmp['test_stat'] = None;
                                data_tmp['test_description'] = test_description;
                                data_tmp['pvalue'] = pvalue;
                                data_tmp['pvalue_corrected'] = pvalue_adjusted;
                                data_tmp['pvalue_corrected_description'] = pvalue_adjusted_description;
                                #data_tmp['fold_change'] = foldChange;
                                data_pairwise.append(data_tmp);
            except Exception as e:
                print(e);
                exit(-1);
        return data_anova,data_pairwise;
    def calculate_twoSampleTTest(self,data_1_I, data_2_I, alternative_I = "two.sided", mu_I = 0, paired_I="TRUE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni"):
        '''calculate a two Sample t-test using R's built in Stats package'''
        # padjusted_methods: ("holm", "hochberg", "hommel", "bonferroni", "BH", "BY", "fdr", "none"
        # alternative_tests: ("greater","less","two.sided")

        #make the dataFrame

        #format into R matrix and list objects
        # convert data dict to matrix filling in missing values
        # with 'NA'
        concentrations_1 = [];
        for d in data_1_I:
            if d:
                concentrations_1.append(d);
            else:
                concentrations_1.append('NA')
        concentrations_2 = [];
        for d in data_2_I:
            if d:
                concentrations_2.append(d);
            else:
                concentrations_2.append('NA')
        # Call to R
        try:
            # convert lists to R lists
            concentrations_1_r = '';
            for c in concentrations_1:
                concentrations_1_r = (concentrations_1_r + ',' + str(c));
            concentrations_1_r = concentrations_1_r[1:];
            r_statement = ('concentrations_1_v = c(%s)' % concentrations_1_r);
            ans = robjects.r(r_statement);
            concentrations_2_r = '';
            for c in concentrations_2:
                concentrations_2_r = (concentrations_2_r + ',' + str(c));
            concentrations_2_r = concentrations_2_r[1:];
            r_statement = ('concentrations_2_v = c(%s)' % concentrations_2_r);
            ans = robjects.r(r_statement);
            # call paired T-test without correction
            r_statement = ('t.test(concentrations_1_v,concentrations_2_v, alternative = "%s", mu = %s,  paired = %s, var.equal = %s, conf.level = %s)'\
                %(alternative_I,mu_I, paired_I, var_equal_I ,ci_level_I));
            ans = robjects.r(r_statement);
            test_stat = ans.rx2('statistic')[0]
            test_description = ans.rx2('method')[0]
            pvalue = ans.rx2('p.value')[0]
            mean = ans.rx2('estimate')[0]
            ci = numpy.array(ans.rx2('conf.int'))
            # adjust the p-value
            r_statement = ('p.adjust(%s, method = "%s")' %(pvalue,padjusted_method_I));
            ans = robjects.r(r_statement);
            pvalue_adjusted = ans[0]
            pvalue_adjusted_description = padjusted_method_I
            # extract out data
            data_tmp = {};
            data_tmp['mean'] = mean;
            data_tmp['ci_lb'] = ci[0];
            data_tmp['ci_ub'] = ci[1];
            data_tmp['ci_level'] =ci_level_I;
            data_tmp['test_stat'] = test_stat;
            data_tmp['test_description'] = test_description;
            data_tmp['pvalue'] = pvalue;
            data_tmp['pvalue_corrected'] = pvalue_adjusted;
            data_tmp['pvalue_corrected_description'] = pvalue_adjusted_description;
        except Exception as e:
            print(e);
            exit(-1);
        return data_tmp;
    def calculate_oneSampleTTest(self,data_1_I, alternative_I = "two.sided", mu_I = 0, paired_I="TRUE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni"):
        '''calculate a two Sample t-test using R's built in Stats package'''
        # padjusted_methods: ("holm", "hochberg", "hommel", "bonferroni", "BH", "BY", "fdr", "none"
        # alternative_tests: ("greater","less","two.sided")

        #make the dataFrame

        #format into R matrix and list objects
        # convert data dict to matrix filling in missing values
        # with 'NA'
        concentrations_1 = [];
        for d in data_1_I:
            if d:
                concentrations_1.append(d);
            else:
                concentrations_1.append('NA')
        # Call to R
        try:
            # convert lists to R lists
            concentrations_1_r = '';
            for c in concentrations_1:
                concentrations_1_r = (concentrations_1_r + ',' + str(c));
            concentrations_1_r = concentrations_1_r[1:];
            r_statement = ('concentrations_1_v = c(%s)' % concentrations_1_r);
            ans = robjects.r(r_statement);
            # call paired T-test without correction
            r_statement = ('t.test(concentrations_1_v,alternative = "%s", mu = %s,  paired = %s, var.equal = %s, conf.level = %s)'\
                %(alternative_I,mu_I, paired_I, var_equal_I ,ci_level_I));
            ans = robjects.r(r_statement);
            test_stat = ans.rx2('statistic')[0]
            test_description = ans.rx2('method')[0]
            pvalue = ans.rx2('p.value')[0]
            #mean = ans.rx2('estimate')[0]
            ci = numpy.array(ans.rx2('conf.int'))
            # adjust the p-value
            r_statement = ('p.adjust(%s, method = "%s")' %(pvalue,padjusted_method_I));
            ans = robjects.r(r_statement);
            pvalue_adjusted = ans[0]
            pvalue_adjusted_description = padjusted_method_I
            # get basic stats
            mean = None; #same order as sna
            var = None;
            n = None;
            r_statement = ('mean(concentrations_1_v)'); # calculate the mean
            ans = robjects.r(r_statement);
            mean = ans[0];
            r_statement = ('var(concentrations_1_v)'); # calculate the variance
            ans = robjects.r(r_statement);
            var = ans[0];
            r_statement = ('length(concentrations_1_v)'); # calculate the # of samples
            ans = robjects.r(r_statement);
            n = ans[0];

            # convert array back to dict
            data_tmp = {};
            data_tmp['mean'] = mean;
            data_tmp['var'] = var;
            data_tmp['cv'] = sqrt(var)/abs(mean)*100 #glog normalization will have negative values
            data_tmp['n'] = n;
            data_tmp['ci_lb'] = ci[0];
            data_tmp['ci_ub'] = ci[1];
            data_tmp['ci_level'] =ci_level_I;
            data_tmp['test_stat'] = test_stat;
            data_tmp['test_description'] = test_description;
            data_tmp['pvalue'] = pvalue;
            data_tmp['pvalue_corrected'] = pvalue_adjusted;
            data_tmp['pvalue_corrected_description'] = pvalue_adjusted_description;
        except Exception as e:
            print(e);
            exit(-1);
        return data_tmp;
    def calculate_pca_princomp(self,data_I,cor_I = "FALSE", scores_I = "TRUE", covmat_I="NULL", na_action_I='na.omit'):
        '''PCA analysis using princomp from R
        Note: The calculation is done using eigen on the correlation or covariance matrix, as determined by cor'''

        #TODO:

        # format into R matrix and list objects
        # convert data dict to matrix filling in missing values
        # with 'NA'
        sns = []
        cgn = []
        replicates = [];
        for d in data_I:
                sns.append(d['sample_name_short']);    
                replicates.append(d['sample_replicate']);   
                cgn.append(d['component_name']);
        sns_sorted = sorted(set(sns))
        replicates_sorted = sorted(set(replicates))
        cgn_sorted = sorted(set(cgn))
        concentrations = ['NA' for r in range(len(sns_sorted)*len(cgn_sorted))];
        cnt = 0;
        cnt_bool = True;
        cnt_reps = 0;
        sna = []
        replicates = []
        for c in cgn_sorted:
                for s in sns_sorted:
                    for d in data_I:
                        if d['sample_name_short'] == s and d['component_name'] == c:
                            if d['calculated_concentration']:
                                concentrations[cnt] = d['calculated_concentration'];
                                if cnt_bool:
                                    sna.append(d['sample_name_abbreviation']);
                                    replicates.append(replicates_sorted[cnt_reps]); 
                                    if cnt_reps < len(replicates_sorted)-1:
                                        cnt_reps+=1;
                                    else:
                                        cnt_reps=0;
                                break;
                    cnt = cnt+1
                cnt_bool = False;
        # check if there were any missing values in the data set in the first place
        mv = 0;
        for c in concentrations:
            if c=='NA':
                mv += 1;
        if mv==0:
            # Call to R
            try:
                # convert lists to R matrix
                concentrations_r = '';
                for c in concentrations:
                    concentrations_r = (concentrations_r + ',' + str(c));
                concentrations_r = concentrations_r[1:];
                r_statement = ('concentrations = c(%s)' % concentrations_r);
                ans = robjects.r(r_statement);
                r_statement = ('concentrations_m = matrix(concentrations, nrow = %s, ncol = %s, byrow = TRUE)' %(len(cgn_sorted),len(sns_sorted)));
                ans = robjects.r(r_statement);
                # calls for pca analysis
                #pcascores <- prcomp(t(x), na.action=na.omit, scale=TRUE)
                #pcascores <- prcomp(t(x), na.action=na.omit)
                #summary(pcascores)
                r_statement = ('pc = princomp(concentrations_m, na.action=%s, core=%s, scores=%s, covmat=%s' %(na_action_I,cor_I, scores_I,covmat_I));
                ans = robjects.r(r_statement);
                sdev = [];
                loadings = [];
                center = [];
                scale = None;
                n_obs = None;
                scores = [];
            except Exception as e:
                print(e);
                exit(-1);
    def calculate_pca_prcomp(self,data_I,retx_I = "TRUE", center_I = "TRUE", na_action_I='na.omit',scale_I="TRUE"):
        '''PCA analysis using prcomp from R
        Note: calculations are made using svd'''

        # format into R matrix and list objects
        # convert data dict to matrix filling in missing values
        # with 'NA'
        sns = []
        cn = []
        replicates = [];
        for d in data_I:
                sns.append(d['sample_name_short']);    
                replicates.append(d['sample_replicate']);   
                cn.append(d['component_name']);
        sns_sorted = sorted(set(sns))
        replicates_sorted = sorted(set(replicates))
        cn_sorted = sorted(set(cn))
        concentrations = ['NA' for r in range(len(sns_sorted)*len(cn_sorted))];
        cnt = 0;
        cnt_bool = True;
        cnt2_bool = True;
        cnt_reps = 0;
        sna = []
        cgn = []
        replicates = []
        for c in cn_sorted:
                cnt2_bool = True;
                for s in sns_sorted:
                    for d in data_I:
                        if d['sample_name_short'] == s and d['component_name'] == c:
                            if d['calculated_concentration']:
                                concentrations[cnt] = d['calculated_concentration'];
                                if cnt_bool:
                                    sna.append(d['sample_name_abbreviation']);
                                    replicates.append(replicates_sorted[cnt_reps]); 
                                    if cnt_reps < len(replicates_sorted)-1:
                                        cnt_reps+=1;
                                    else:
                                        cnt_reps=0;
                                if cnt2_bool:
                                    cgn.append(d['component_group_name']);
                                    cnt2_bool = False;
                                break;
                    cnt = cnt+1
                cnt_bool = False;
        # check if there were any missing values in the data set in the first place
        mv = 0;
        for c in concentrations:
            if c=='NA':
                mv += 1;
        if mv==0:
            # Call to R
            try:
                # convert lists to R matrix
                concentrations_r = '';
                for c in concentrations:
                    concentrations_r = (concentrations_r + ',' + str(c));
                concentrations_r = concentrations_r[1:];
                r_statement = ('concentrations = c(%s)' % concentrations_r);
                ans = robjects.r(r_statement);
                r_statement = ('concentrations_m = matrix(concentrations, nrow = %s, ncol = %s, byrow = TRUE)' %(len(cn_sorted),len(sns_sorted))); 
                ans = robjects.r(r_statement);
                # calls for pca analysis
                r_statement = ('pc = prcomp(t(concentrations_m), na.action=%s, retx=%s, center=%s, scale=%s)' %(na_action_I,retx_I,center_I,scale_I));
                #need to send in the transpose
                ans = robjects.r(r_statement);
                r_statement = ('summary(pc)')
                ans = robjects.r(r_statement);
                importance = numpy.array(ans.rx2('importance'))
                stdev = numpy.array(ans.rx2('sdev')) # or importance[0,:]
                var_proportion = importance[1,:]
                var_cumulative = importance[2,:]
                loadings = numpy.array(ans.rx2('rotation')) #nrow = mets x ncol = loadings axis
                scores = numpy.array(ans.rx2('x')) #nrow = samples x ncol = pc axis
                # extract out scores
                data_scores = [];
                for r in range(scores.shape[0]):
                    for c in range(scores.shape[1]):
                        data_tmp = {};
                        data_tmp['sample_name_short'] = sns_sorted[r];
                        data_tmp['score'] = scores[r,c];
                        data_tmp['axis'] = c+1;
                        data_tmp['var_proportion'] = var_proportion[c];
                        data_tmp['var_cumulative'] = var_cumulative[c];
                        data_scores.append(data_tmp);
                # extract out loadings
                data_loadings = [];
                for r in range(loadings.shape[0]):
                    for c in range(loadings.shape[1]):
                        data_tmp = {};
                        data_tmp['component_name'] = cn_sorted[r]; #need to double check
                        data_tmp['component_group_name'] = cgn[r];
                        data_tmp['loadings'] = loadings[r,c]; #need to double check
                        data_tmp['axis'] = c+1;
                        data_loadings.append(data_tmp);
            except Exception as e:
                print(e);
                exit(-1);
            return data_scores,data_loadings
    def calculate_svm(self):
        # TODO
        # Call to R
        try:
            # format the data into R objects
            # call tune
            r_statement = ('concentrations_m = matrix(concentrations, nrow = %s, ncol = %s, byrow = TRUE)' %(len(cn_sorted),len(sns_sorted))); 
            #tune.svm(train.x, train.y = NULL, data = list(), validation.x = NULL,
            #    validation.y = NULL, ranges = NULL, predict.func = predict,
            #    tunecontrol = tune.control(), ...)
            #tune.control(random = FALSE, nrepeat = 1, repeat.aggregate = min,
            #   sampling = c("cross", "fix", "bootstrap"), sampling.aggregate = mean,
            #   sampling.dispersion = sd,
            #   cross = 10, fix = 2/3, nboot = 10, boot.size = 9/10, best.model = TRUE,
            #   performances = TRUE, error.fun = NULL)
            #best.tune(...)
            #svm(x, y = NULL, scale = TRUE, type = NULL, kernel = "radial",
            #   degree = 3, gamma = if (is.vector(x)) 1 else 1 / ncol(x),
            #   coef0 = 0, cost = 1, nu = 0.5,
            #   class.weights = NULL, cachesize = 40, tolerance = 0.001, epsilon = 0.1,
            #   shrinking = TRUE, cross = 0, probability = FALSE, fitted = TRUE, seed = 1L)
            ans = robjects.r(r_statement);
            return
        except Exception as e:
            print(e);
            exit(-1);
