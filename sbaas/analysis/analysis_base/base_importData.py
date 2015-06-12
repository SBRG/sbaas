import csv, sys, json

class base_importData():
    """a class to import data"""

    def __init__(self):
        self.data = [];

    def clear_data(self):
        """clear existing data"""
        del self.data[:];

    def format_data(self):
        """remove specific sequences for utf-8 compatibility"""
        if self.data:
            data_cpy = []
            for d in self.data:
                try:
                    row = {};
                    for key, value in d.items():
                        # replace multiquant-specific output
                        if (value == 'N/A' or value == '< 0' or value == '<2 points' or
                           value == 'degenerate' or value == '(No IS)'): value = None;
                        # replace empty strings with None
                        if not(value):
                            value = None;
                        else:
                            #value.decode('utf-8', "ignore"); # convert to utf-8      
                            value = value;           
                        row[key] = value;
                    data_cpy.append(row);
                except BaseException as e:
                    sys.exit('error formating data %s' % d);  
            del self.data[:];
            self.data = data_cpy;
                   
    def read_csv(self, filename):
        """read table data from csv file"""
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile);
                try:
                    keys = reader.fieldnames;
                    for row in reader:
                        self.data.append(row);
                except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e));
        except IOError as e:
            sys.exit('%s does not exist' % e);
                   
    def read_tab(self, filename):
        """read table data from tab file"""
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile,delimiter='\t');
                try:
                    keys = reader.fieldnames;
                    for row in reader:
                        self.data.append(row);
                except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e));
        except IOError as e:
            sys.exit('%s does not exist' % e); 
                        
    def read_tab_fieldnames(self, filename, fieldnames, header=False):
        """read table data from tab file"""
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile,fieldnames,delimiter='\t');
                headers = '';
                try:
                    for i,row in enumerate(reader):
                        if i==0 and header: headers = row;
                        else: self.data.append(row);
                except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e));
        except IOError as e:
            #sys.exit('%s does not exist' % e);
            print(('%s does not exist' % e)); 

    def read_json(self, filename):
        '''import values from a json file'''
        data = json.load(open(filename))
        self.data = data;