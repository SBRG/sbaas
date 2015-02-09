'''Module for quantitation QC'''

from analysis.analysis_base import *
from sqlalchemy import func
from resources.r import robjects,importr

class stage01_quantification_QMethod(base_analysis):

    def execute_quantitationMethodUpdate(self, quant_method_ids_I = []):
        '''calculate regression parameters for all components
        that have not been determined'''

        if quant_method_ids_I:
            quant_method_ids = quant_method_ids_I;
        else:
            quant_method_ids = [];
            quant_method_ids = self.get_quantMethodIds();
        for id in quant_method_ids:
            # get the samples and components that make were used to make
            # the quantitation method
            print(id);
            component_names = [];
            component_names = self.get_quantSamplesAndComponents(id);
            for n in component_names:
                print(n);
                # get the quant method parameters for each component
                fit,weighting,use_area = self.get_quantMethodParameters(id,n);
                # calculate the quant regression parameters for each component
                slope,intercept,correlation,lloq,uloq,points = self.calculate_regressionParameters(n,fit,weighting,use_area);
                # update the quantitation_method table
                self.update_quantitationMethod(id,n,slope,intercept,correlation,lloq,uloq,points);

    def get_quantMethodIds(self):
        '''Query quantitation method IDs that do not have regression parameters
        Note: correlation==Null is used to identify which quantitation method
              IDs do not have regression parameters'''
        quant_method_ids = self.session.query(quantitation_method.id).filter(
                    quantitation_method.correlation.is_(None)).group_by(
                    quantitation_method.id).all();
        quant_method_ids_O = [];
        for id in quant_method_ids: quant_method_ids_O.append(id.id);
        return quant_method_ids_O;
    def get_quantSamplesAndComponents(self, quant_method_id_I):
        '''Query calibrator samples and components that were used
        for calibration
        NOTE: can be used within a loop if multiple
        there are multiple quantitation ids'''
        # input:
        #       quantitation_method_id
        # ouput:
        #       calibrators_samples
        #       calibrators_components
        # query experiment and samples that were used to create the given calibration method
        self.calibrators_samples = self.session.query(data_stage01_quantification_MQResultsTable.sample_name).filter(
                             quantitation_method.id==experiment.quantitation_method_id,
                             experiment.sample_name==data_stage01_quantification_MQResultsTable.sample_name,
                             data_stage01_quantification_MQResultsTable.sample_type.like('Standard'),
                             data_stage01_quantification_MQResultsTable.used_,
                             quantitation_method.id.like(quant_method_id_I)).group_by(
                             data_stage01_quantification_MQResultsTable.sample_name).subquery('calibrators_samples');
        # query components from quantitation method that were used to create the given calibration method
        calibrators_components = self.session.query(data_stage01_quantification_MQResultsTable.component_name).filter(
                            data_stage01_quantification_MQResultsTable.used_.is_(True),
                            data_stage01_quantification_MQResultsTable.is_.isnot(True), 
                            data_stage01_quantification_MQResultsTable.sample_name.like(self.calibrators_samples.c.sample_name)).group_by(
                            data_stage01_quantification_MQResultsTable.component_name).all(); #subquery('calibrators_components');
        #calibrators_components = self.session.query(quantitation_method.component_name).filter(
        #                    quantitation_method.id.like(quant_method_id_I)).group_by(
        #                    quantitation_method.component_name).all(); #subquery('calibrators_components');
        component_names_O = [];
        for cn in calibrators_components: component_names_O.append(cn.component_name);
        return component_names_O;
    def get_quantMethodParameters(self, quant_method_id_I, component_name_I):
        '''Query calibration parameters for a given component
        from a specified quantitation method id
        NOTE: intended to be used in a loop'''
        # input:
        #       component_name
        #       quantitation_method_id
        # ouput:
        #       fit
        #       weighting
        #       use_area
        calibrators_parameters = self.session.query(quantitation_method.component_name,
                            quantitation_method.fit,quantitation_method.weighting,
                            quantitation_method.use_area).filter(
                            quantitation_method.id.like(quant_method_id_I),
                            quantitation_method.component_name.like(component_name_I)).first();
        fit_O = calibrators_parameters.fit;
        weighting_O = calibrators_parameters.weighting;
        use_area_O = calibrators_parameters.use_area;

        return fit_O, weighting_O, use_area_O;
    def calculate_regressionParameters(self, component_name_I, fit_I, weighting_I, use_area_I):
        '''calculate regression parameters for a given component
        from a specified quantitation method id
        NOTE: intended to be used in a loop'''
        # input:
        #       component_name
        #       calibrators_samples (class member) 
        #       fit
        #       weighting
        #       use_area
        # ouput:
        #       slope
        #       intercept
        #       correlation
        #       lloq
        #       uloq
        #       points

        # query calibrators for specific component_name from specific experiment_id
        if use_area_I:
            calibrators = self.session.query(data_stage01_quantification_MQResultsTable.actual_concentration,
                                        data_stage01_quantification_MQResultsTable.area_ratio,
                                        data_stage01_quantification_MQResultsTable.dilution_factor).filter(
                                     data_stage01_quantification_MQResultsTable.sample_name.like(self.calibrators_samples.c.sample_name),
                                     data_stage01_quantification_MQResultsTable.used_.is_(True),
                                     data_stage01_quantification_MQResultsTable.is_.isnot(True),
                                     data_stage01_quantification_MQResultsTable.component_name.like(component_name_I)).all();
        else:
            calibrators = self.session.query(data_stage01_quantification_MQResultsTable.actual_concentration,
                                        data_stage01_quantification_MQResultsTable.height_ratio,
                                        data_stage01_quantification_MQResultsTable.dilution_factor).filter(
                                     data_stage01_quantification_MQResultsTable.sample_name.like(self.calibrators_samples.c.sample_name),
                                     data_stage01_quantification_MQResultsTable.used_.is_(True),
                                     data_stage01_quantification_MQResultsTable.is_.isnot(True),
                                     data_stage01_quantification_MQResultsTable.component_name.like(component_name_I)).all();
        # variable to check quantitation
        calc_regress = True;

        # extraction concentrations
        concentration = [];
        for c in calibrators: 
            if c.actual_concentration: concentration.append(c.actual_concentration);
            else: calc_regress = False;
        if len(concentration)==0:
            calc_regress = False;
        # extraction ratio
        ratio = [];
        if use_area_I:
            for c in calibrators: 
                if c.area_ratio: ratio.append(c.area_ratio);
                else: ratio.append(0.0);
        else:
            for c in calibrators:
                if c.height_ratio: ratio.append(c.height_ratio);
                else: ratio.append(0.0);
        if len(ratio)==0:
            calc_regress = False;
        # extraction diluton factor
        dilution_factor = [];
        for c in calibrators:
            if c.dilution_factor: dilution_factor.append(c.dilution_factor);
            else: dilution_factor.append(1.0);
        # correct the concentration for the dilution factor
        for n in range(len(concentration)):
            concentration[n] = concentration[n]/dilution_factor[n];

        if (not(calc_regress)):
            return 0,0,0,0,0,0;

        # lloq, uloq, points
        lloq_O = min(concentration);
        uloq_O = max(concentration);
        points_O = len(concentration);

        # Call to R
        try:
            stats = importr('stats');

            # generate weights:
            '''From MultiQuant Manual:
            Weighting type	Weight (w)
            None Always	1.0.
            1 / x	If |x| < 10-5 then w = 10e5; otherwise w = 1 / |x|.
            1 / x2	If |x| < 10-5 then w = 10e10; otherwise w = 1 / x2.
            1 / y	If |y| < 10-8 then w = 10e8; otherwise w = 1 / |y|.
            1 / y2	If |y| < 10-8 then w = 10e16; otherwise w = 1 / y2.
            ln x	If x < 0 an error is generated; otherwise if x < 10-5 then w = ln 105,
		            otherwise w = |ln x|.'''
            wts = []; 
            if weighting_I == 'ln (x)':
                for c in concentration:
                    if c<10e-5:
                        wts.append(log(10e5));
                    else:
                        wts.append(abs(log(c)));
            elif weighting_I == 'None':
                for c in concentration:
                    wts.append(1.0);
            elif weighting_I == '1 / x':
                for c in concentration:
                    if c<10e-5:
                        wts.append(1/10e5);
                    else:
                        wts.append(1/abs(c));
            elif weighting_I == '1 / y':
                for c in ratio:
                    if c<10e-8:
                        wts.append(1/10e8);
                    else:
                        wts.append(1/abs(c));

            else:
                print("weighting " + weighting_I + " not yet supported");
                print("linear weighting used instead");
                for c in concentration:
                    wts.append(1.0);
            
            # convert lists to R objects
            x = robjects.FloatVector(concentration);
            y = robjects.FloatVector(ratio);
            w = robjects.FloatVector(wts);
            if fit_I == 'Linear':
                fmla = robjects.Formula('y ~ x'); # generate the R formula for lm
            elif fit_I == 'Linear Through Zero':
                fmla = robjects.Formula('y ~ -1 + x'); # generate the R formula for lm
            elif fit_I == 'Quadratic':
                fmla = robjects.Formula('y ~ x + I(x^2)'); # generate the R formula for lm
            elif fit_I == 'Power':
                fmla = robjects.Formula('log(y) ~ log(x)'); # generate the R formula for lm
            else:
                print("fit " + fit_I + " not yet supported");
                print("linear model used instead");
                fmla = robjects.Formula('y ~ x');

            env = fmla.environment; # set the local environmental variables for lm
            env['x'] = x;
            env['y'] = y;
            #fit = r('lm(%s)' %fmla.r_repr()); # direct call to R
            fit = stats.lm(fmla, weights = w); # return the lm fitted model from R
            sum = stats.summary_lm(fit) # return the summary of the fit
            intercept_O = sum.rx2('coefficients')[0]; #intercept
            slope_O = sum.rx2('coefficients')[1]; #slope
            correlation_O = sum.rx2('r.squared')[0]; #r-squared

            return slope_O, intercept_O, correlation_O, lloq_O, uloq_O, points_O;
        except:
            print('error in R')
    def update_quantitationMethod(self, quant_method_id_I, component_name_I, 
                                  slope_I, intercept_I, correlation_I, lloq_I, uloq_I, points_I):
        try:
            quant_method_update = self.session.query(quantitation_method).filter(
                 quantitation_method.id.like(quant_method_id_I),
                 quantitation_method.component_name.like(component_name_I)).update(
                 {'slope': slope_I,'intercept':intercept_I,'correlation':correlation_I,
                  'lloq':lloq_I,'uloq':uloq_I,'points':points_I},synchronize_session=False);
            self.session.commit(); # could possible move if efficiency is poor
        except SQLAlchemyError as e:
            print(e);

    def execute_quantitationMethodComparison(self):
        '''Query and write calibration regression parameters to file'''

        # get the components that are in all of the calibration methods
        component_names = [];
        component_names = self.get_allComponents();
        # get all the quantitation method IDs
        quant_method_ids = [];
        quant_method_ids = self.get_allQuantMethodIds();
        with open('quantitationMethodComparison.csv', 'wb') as csvfile:
            # write header to file
            csv_writer = csv.writer(csvfile)
            header = [];
            columns = [];
            column_names = ['slope','intercept','correlation','lloq','uloq','points'];
            for c in column_names:
                for i in quant_method_ids:
                    header.append(i);
                    columns.append(c);
            header.insert(0,'');
            columns.insert(0,'Component_Name');
            csv_writer.writerow(header);
            csv_writer.writerow(columns);
            # loop through each component
            for n in component_names:
                slopes = [];
                intercepts = [];
                correlations = [];
                lloqs = [];
                uloqs = [];
                points = [];
                for id in quant_method_ids:
                    # query regression parameters
                    slope = 0;
                    intercept = 0;
                    correlation = 0;
                    lloq = 0;
                    uloq = 0;
                    point = 0;
                    slope,intercept,correlation,lloq,uloq,point = self.get_quantMethodRegression(id,n);
                    slopes.append(slope);
                    intercepts.append(intercept);
                    correlations.append(correlation);
                    lloqs.append(lloq);
                    uloqs.append(uloq);
                    points.append(point);

                # write row to file
                row = [n];
                row.extend(slopes);
                row.extend(intercepts);
                row.extend(correlations);
                row.extend(lloqs);
                row.extend(uloqs);
                row.extend(points);
                csv_writer.writerow(row);
    
    def get_components(self,quant_method_id_I):
        '''Query calibrator components that are in the calibration method
        NOTE: can be used within a loop if multiple
        there are multiple quantitation ids'''
        # input:
        #       quantitation_method_id
        # ouput:
        #       calibrators_components
        # query experiment and samples that were used to create the given calibration method
        try:
            calibrators_components = self.session.query(quantitation_method.component_name).filter(
                                quantitation_method.id.like(quant_method_id_I)).group_by(
                                quantitation_method.component_name).all();
            component_names_O = [];
            for cn in calibrators_components: component_names_O.append(cn.component_name);
            return component_names_O;

        except SQLAlchemyError as e:
            print(e);
    def get_allComponents(self):
        '''Query calibrator components that are in all of the calibration methods
        NOTE: can be used within a loop if multiple
        there are multiple quantitation ids'''
        # input:
        #       quantitation_method_id
        # ouput:
        #       calibrators_components
        # query experiment and samples that were used to create the given calibration method
        try:
            calibrators_components = self.session.query(quantitation_method.component_name).group_by(
                                quantitation_method.component_name).all();
            component_names_O = [];
            for cn in calibrators_components: component_names_O.append(cn.component_name);
            return component_names_O;

        except SQLAlchemyError as e:
            print(e);
    def get_allQuantMethodIds(self):
        '''Query quantitation method IDs that do not have regression parameters
        Note: correlation==Null is used to identify which quantitation method
              IDs do not have regression parameters'''
        try:
            quant_method_ids = self.session.query(quantitation_method.id).group_by(
                        quantitation_method.id).all();
            quant_method_ids_O = [];
            for id in quant_method_ids: quant_method_ids_O.append(id.id);
            return quant_method_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_quantMethodRegression(self, quant_method_id_I, component_name_I):
        '''Query calibration parameters for a given component
        from a specified quantitation method id
        NOTE: intended to be used in a loop'''
        # input:
        #       component_name
        #       quantitation_method_id
        # ouput:
        #       intercept
        #       slope
        #       correlation
        #       lloq
        #       uloq
        #       points
        try:
            calibrators_parameters = self.session.query(quantitation_method.intercept,
                                quantitation_method.slope,
                                quantitation_method.correlation,
                                quantitation_method.lloq,
                                quantitation_method.uloq,
                                quantitation_method.points,
                                quantitation_method.slope).filter(
                                quantitation_method.id.like(quant_method_id_I),
                                quantitation_method.component_name.like(component_name_I)).first();
                                #first(): primary key(quant_method_id,component_name)
            if calibrators_parameters:
                intercept_O = calibrators_parameters.intercept;
                slope_O = calibrators_parameters.slope;
                correlation_O = calibrators_parameters.correlation;
                lloq_O = calibrators_parameters.lloq;
                uloq_O = calibrators_parameters.uloq;
                points_O = calibrators_parameters.points;
                if (slope_O and intercept_O and correlation_O and lloq_O and uloq_O and points_O):
                    return slope_O, intercept_O, correlation_O, lloq_O, uloq_O, points_O;
                else:
                    return 0,0,0,0,0,0;
            else:
                return 0,0,0,0,0,0;

        except SQLAlchemyError as e:
            print(e);