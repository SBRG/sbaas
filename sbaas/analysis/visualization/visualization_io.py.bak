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
                                                     d['pipeline_id'],
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
                            'pipeline_id':d['pipeline_id'],
                            'analysis_id':d['analysis_id'],
                            'data_export_id':d['data_export_id'],
                            'container_export_id':d['container_export_id'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_visualizationUser_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_visualizationUser(data.data);
        data.clear_data();

    def add_visualizationUser(self, data_I):
        '''add rows of visualization_user'''
        if data_I:
            for d in data_I:
                try:
                    data_add = visualization_user(d['project_ids'],
                            d['user_name'],
                            d['user_password'],
                            d['user_role'],
                            d['user_host'],
                            d['user_database'],
                            d['user_schema'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_visualizationUser_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_visualizationUser(data.data);
        data.clear_data();

    def update_visualizationUser(self,data_I):
        '''update rows of visualization_user'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(visualization_user).filter(
                            visualization_user.id == d['id']).update(
                            {
                            'project_ids':d['project_ids'],
                            'user_name':d['user_name'],
                            'user_password':d['user_password'],
                            'user_role':d['user_role'],
                            'user_host':d['user_host'],
                            'user_database':d['user_database'],
                            'user_schema':d['user_schema'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_visualizationProject_js(self,project_id_I,data_dir_I="tmp"):
        """export visualization_project for visualization"""

        print "exporting visualization_project..."

        # query the project info
        data1_project = {};
        data1_project = self.visualization_query.get_project_projectID_visualizationProject(project_id_I);
        data1_O = [];
        data1_O = self.visualization_query.get_rows_projectID_visualizationProject(project_id_I);
        # query the project description
        data2_O = [];
        data2_O = self.visualization_query.get_rows_projectID_visualizationProjectDescription(project_id_I);
        # data parameters
        data1_keys = ['analysis_id','data_export_id','pipeline_id'#,'container_export_id'
                      ];
        data1_nestkeys = ['data_export_id'];
        data1_keymap = {'buttonparameter':'data_export_id','liparameter':'analysis_id',
                        'buttontext':'data_export_id','litext':'analysis_id'};
        data2_keys = ['project_id','project_section','project_heading','project_tileorder'
                      ];
        data2_nestkeys = ['project_id'];
        data2_keymap = {'htmlmediasrc':'project_media','htmlmediaalt':'',
                        'htmlmediahref':'project_href','htmlmediaheading':'project_heading',
                        'htmlmediaparagraph':'project_paragraph'};
        # make the data, parameters, and tile2datamap variables:
        dataobject_O = [];
        parametersobject_O = [];
        tile2datamap_O = {};
        tile_cnt = 0;
        # project_description:
        for i,d in enumerate(data2_O):
            tileid = "tile" + str(tile_cnt);
            colid = "col" + str(i);
            tileheader = d['project_section'];
            htmlid = "html" + str(tile_cnt);
            tileparameters = {'tileheader':tileheader,'tiletype':'html','tileid':tileid,'rowid':"row1",'colid':colid,
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-6"};
            htmlparameters={"htmlkeymap":[data2_keymap],
                        'htmltype':'media_01','htmlid':htmlid};
            tileparameters.update(htmlparameters);
            parametersobject_O.append(tileparameters);
            dataobject_O.append({"data":[d],"datakeys":data2_keys,"datanestkeys":data2_nestkeys});
            tile2datamap_O.update({tileid:[tile_cnt]});
            tile_cnt+=1;
        # project:
        data1_dict = {};
        for data_export_id in data1_project['data_export_id']:
            data1_dict[data_export_id]=[];
        for d in data1_O:
            data1_dict[d['data_export_id']].append(d);
        data1_keys = data1_dict.keys();
        data1_keys.sort();
        col_cnt = 0;
        #for k,v in data1_dict.iteritems():
        for k in data1_keys:
            tileid = "tile" + str(tile_cnt);
            colid = "col" + str(col_cnt);
            tileheader = data1_dict[k][0]['pipeline_id'];
            htmlid = "html" + str(tile_cnt);
            #tileparameters = {'tileheader':tileheader,'tiletype':'html','tileid':tileid,'rowid':"row2",'colid':colid,
            #    'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-6"};
            #hrefparameters = {"hrefurl":'project.html',"htmlkeymap":[data1_keymap],
            #                'htmltype':'href_01','htmlid':htmlid};
            tileparameters = {'tileheader':tileheader,'tiletype':'html','tileid':tileid,'rowid':"row2",'colid':colid,
                'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-6","formsubmitbuttonidtext":{'id':'submit1','text':'submit'}};
            hrefparameters = {"hrefurl":'project.html',"htmlkeymap":[data1_keymap],
                            'htmltype':'href_02','htmlid':htmlid};
            tileparameters.update(hrefparameters);
            parametersobject_O.append(tileparameters);
            dataobject_O.append({"data":data1_dict[k],"datakeys":data1_keys,"datanestkeys":data1_nestkeys});
            tile2datamap_O.update({tileid:[tile_cnt]});
            tile_cnt+=1;
            col_cnt+=1;

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
    