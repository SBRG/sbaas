from analysis.analysis_base import *
from visualization_query import visualization_query

class visualization_io(base_analysis):

    def __init__(self, session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.visualization_query = visualization_query(self.session);

    def import_visualizationProject_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_visualizationProject(data.data);
        data.clear_data();

    def add_visualizationProject(self, data_I):
        '''add rows of visualization_project'''
        if data_I:
            for d in data_I:
                try:
                    data_add = visualization_project(d['project_id'],
                                    d['analysis_id'],
                                    d['data_export_id'],
                                    d['container_export_id'],
                                    d['used_'],
                                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_visualizationProject_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_visualizationProject(data.data);
        data.clear_data();

    def update_visualizationProject(self,data_I):
        '''update rows of visualization_project'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(visualization_project).filter(
                            visualization_project.id == d['id']).update(
                            {
                            'project_id':d['project_id'],
                            'analysis_id':d['analysis_id'],
                            'data_export_id':d['data_export_id'],
                            'container_export_id':d['container_export_id'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_visualizationProject_js(self,project_id_I,data_dir_I="tmp"):
        """export visualization_project for visualization"""

        print "exporting visualization_project..."

        # query the analysis info
        data1_O = [];
        data1_O = self.visualization_query.get_rows_projectID_visualizationProject(project_id_I);
        # data parameters
        data1_keys = ['analysis_id','data_export_id'#,'container_export_id'
                      ];
        data1_nestkeys = ['data_export_id'];
        data1_keymap = {'buttontext':'data_export_id','litext':'analysis_id'};
        # make the data object
        dataobject_O = [{"data":data1_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys},
                        {"data":data1_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys},
                        {"data":data1_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys},
                        {"data":data1_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys},
                        {"data":data1_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys}];
        # make the tile parameter objects
        parametersobject_O = [];
        # ale:
        dropdownbuttongrouptileparameters1_O = {'tileheader':'ALE','tiletype':'html','tileid':"tile1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-3"};
        dropdownbuttongroupparameters1_O = {"htmlfilters":{'data_export_id':['export_dataStage01AleTrajectories_js']},"hrefurl":'project.html',"htmlkeymap":data1_keymap,
                        'buttonparameter':'data_export_id','liparameter':'analysis_id','htmltype':'dropdownbuttongrouphref_01','htmlid':"html1"};
        dropdownbuttongrouptileparameters1_O.update(dropdownbuttongroupparameters1_O);
        parametersobject_O.append(dropdownbuttongrouptileparameters1_O);
        # physiology:
        dropdownbuttongrouptileparameters1_O = {'tileheader':'Physiology','tiletype':'html','tileid':"tile2",'rowid':"row1",'colid':"col2",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-3"};
        dropdownbuttongroupparameters1_O = {"htmlfilters":{'data_export_id':['export_dataStage01PhysiologyRatesAverages_js']},"hrefurl":'project.html',"htmlkeymap":data1_keymap,
                        'buttonparameter':'data_export_id','liparameter':'analysis_id','htmltype':'dropdownbuttongrouphref_01','htmlid':"html2"};
        dropdownbuttongrouptileparameters1_O.update(dropdownbuttongroupparameters1_O);
        parametersobject_O.append(dropdownbuttongrouptileparameters1_O);
        # resequencing:
        dropdownbuttongrouptileparameters1_O = {'tileheader':'Resequencing','tiletype':'html','tileid':"tile3",'rowid':"row1",'colid':"col3",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-3"};
        dropdownbuttongroupparameters1_O = {"htmlfilters":{'data_export_id':['export_dataStage01ResequencingHeatmap_js','export_dataStage01ResequencingLineage_js','export_dataStage02ResequencingHeatmap_js']},
                                            "hrefurl":'project.html',"htmlkeymap":data1_keymap,
                        'buttonparameter':'data_export_id','liparameter':'analysis_id','htmltype':'dropdownbuttongrouphref_01','htmlid':"html3"};
        dropdownbuttongrouptileparameters1_O.update(dropdownbuttongroupparameters1_O);
        parametersobject_O.append(dropdownbuttongrouptileparameters1_O);
        # quantification:
        dropdownbuttongrouptileparameters1_O = {'tileheader':'Quantification','tiletype':'html','tileid':"tile4",'rowid':"row1",'colid':"col4",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-3"};
        dropdownbuttongroupparameters1_O = {"htmlfilters":{'data_export_id':['Quantification']},"hrefurl":'project.html',"htmlkeymap":data1_keymap,
                        'buttonparameter':'data_export_id','liparameter':'analysis_id','htmltype':'dropdownbuttongrouphref_01','htmlid':"html4"};
        dropdownbuttongrouptileparameters1_O.update(dropdownbuttongroupparameters1_O);
        parametersobject_O.append(dropdownbuttongrouptileparameters1_O);
        # isotopomer:
        dropdownbuttongrouptileparameters1_O = {'tileheader':'Isotopomer','tiletype':'html','tileid':"tile5",'rowid':"row1",'colid':"col5",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-3"};
        dropdownbuttongroupparameters1_O = {"htmlfilters":{'data_export_id':['Isotopomer']},"hrefurl":'project.html',"htmlkeymap":data1_keymap,
                        'buttonparameter':'data_export_id','liparameter':'analysis_id','htmltype':'dropdownbuttongrouphref_01','htmlid':"html5"};
        dropdownbuttongrouptileparameters1_O.update(dropdownbuttongroupparameters1_O);
        parametersobject_O.append(dropdownbuttongrouptileparameters1_O);
        # make the tile2datamap
        tile2datamap_O = {"tile1":[0],"tile2":[1],"tile3":[2],"tile4":[3],"tile5":[4]};

        # dump the data to a json file
        data_str = 'var ' + 'data' + ' = ' + json.dumps(dataobject_O) + ';';
        parameters_str = 'var ' + 'parameters' + ' = ' + json.dumps(parametersobject_O) + ';';
        tile2datamap_str = 'var ' + 'tile2datamap' + ' = ' + json.dumps(tile2datamap_O) + ';';
        if data_dir_I=='tmp':
            filename_str = settings.visualization_data + '/tmp/ddt_data.js'
        elif data_dir_I=='project':
            filename_str = settings.visualization_data + '/project/' + analysis_id_I + '_data_stage01_resequencing_lineage' + '.js'
        elif data_dir_I=='data_json':
            data_json_O = data_str + '\n' + parameters_str + '\n' + tile2datamap_str;
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(data_str);
            file.write(parameters_str);
            file.write(tile2datamap_str);
    