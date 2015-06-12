import csv, sys, json

class base_exportData():
    """a class to export data"""

    def __init__(self,data_I):
        self.data = data_I;

    def clear_data(self):
        """clear existing data"""
        del self.data[:];

    def write_dict2csv(self,filename,headers=None):
        # write dict to csv
        with open(filename, 'w') as f:
            if headers: fieldname = headers;
            else: fieldname = list(self.data[0].keys())
            writer = csv.DictWriter(f, fieldnames = fieldname)
            try:
                writer.writeheader();
                writer.writerows(self.data);
            except csv.Error as e:
                sys.exit(e);

    def write_dict2json(self,filename):
        # write dict to json file
        with open(filename, 'w') as outfile:
            json.dump(self.data, outfile, indent=4);

    def write_dict2tsv(self,filename):
        # write dict to tsv
        with open(filename, 'w') as f:
            writer = csv.DictWriter(f,fieldnames = list(self.data[0].keys()),dialect = 'excel-tab')
            try:
                writer.writeheader();
                writer.writerows(self.data);
            except csv.Error as e:
                sys.exit(e);

    def write_headerAndColumnsAndElements2csv(self,header_I,columns_I,filename):
        # make header
        header = [''];
        header.extend(header_I);
        # make rows
        rows = self.data;
        for i in range(len(columns_I)):
            rows[i].insert(0,columns_I[i]);

        with open(filename, 'w') as f:
            writer = csv.writer(f);
            try:
                writer.writerow(header);
                writer.writerows(rows);
            except csv.Error as e:
                sys.exit(e);

    def write_headersAndElements2csv(self,header_I,filename):
        # write data to csv file
        with open(filename, 'wb') as f:
            writer = csv.writer(f);
            try:
                writer.writerows(header_I);
                writer.writerows(self.data);
            except csv.Error as e:
                sys.exit(e);

    def write_headersAndElements2txt(self,header_I,filename):
        # write data to txt file
        with open(filename, 'wb') as f:
            writer = csv.writer(f, delimiter='\t');
            try:
                writer.writerows(header_I);
                writer.writerows(self.data);
            except csv.Error as e:
                sys.exit(e);

    def write_dict2js(self,filename,varname):
        # write dict to js file
        json_str = 'var ' + varname + ' = ' + json.dumps(self.data);
        with open(filename,'w') as file:
            file.write(json_str);

