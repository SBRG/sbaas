"use strict";
//var ddt_table_responsivetable_01 = function () {
function ddt_table_responsivetable_01() {
    // responsive table
    // description:
    // data is formatted and presented in tabular form
    // parameters:
    // parameters_I = e.g., {"tabletype":'table_01',
	//					'tableid':'table1',
	//					"tablefilters":{'met_id':['glc-D','ac'],
	//					"tableclass":"table table-hover"}
    ddt_table.call(this);
};
ddt_table_responsivetable_01.prototype = Object.create(ddt_table.prototype);
ddt_table_responsivetable_01.prototype.constructor = ddt_table_responsivetable_01;
ddt_table_responsivetable_01.prototype.make_table = function(data_I,parameters_I){
	//

	this.ddttable = new d3_table();
	
	// general table properties
	this.set_parameters(parameters_I);
	this.set_ddttable()
    this.add_data(data_I);

	// table specific properties
    this.ddttable.set_tableclass("table table-hover");
    if (parameters_I.tableheaders){this.ddttable.set_tableheaders(parameters_I.tableheaders);}
    else {this.ddttable.extract_tableheaders();};
    this.ddttable.add_csvandjsonexportbutton2tile();
//     this.ddttable.add_datafiltermenuresetbutton(parameters_I.tableformtileid,parameters_I.tableresetbuttonid)
//     this.ddttable.add_datafiltermenusubmitbutton(parameters_I.tableformtileid,parameters_I.tablesubmitbuttonid)
    this.ddttable.render = function () {
    	// permanent filter on the data
    	if (parameters_I.tablefilters){
			this.data.change_filters(parameters_I.tablefilters);
			this.data.filter_stringdata();
    	};
        this.add_table2tile();
        this.set_tableheader();
		this.set_tablebody();
		this.add_tableheader();
		this.add_tablebody();
		this.set_tablestyle();
		this.set_headerstyle();
		this.set_cellstyle();
    };
}