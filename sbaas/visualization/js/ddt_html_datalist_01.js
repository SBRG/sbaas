"use strict";
//var ddt_html_datalist_01 = function () {
function ddt_html_datalist_01() {
    // data list tile
    ddt_html.call(this);
};
ddt_html_datalist_01.prototype = Object.create(ddt_html.prototype);
ddt_html_datalist_01.prototype.constructor = ddt_html_datalist_01;
ddt_html_datalist_01.prototype.make_html = function(data_I,parameters_I){   
    // make the data list
    // INPUT:
    // parameters_I = e.g., {
    //        'datalist': [{'value':'hclust','text':'by cluster'},
    //                        {'value':'probecontrast','text':'by row and column'},
    //                        {'value':'probe','text':'by row'},
    //                        {'value':'contrast','text':'by column'},
    //                        {'value':'custom','text':'by value'}]};

	this.ddthtml = new d3_html();
    var datalist_I = parameters_I.datalist;
	
	// general html properties
	this.set_parameters(parameters_I);
	this.set_ddthtml()
    this.add_data(data_I[0]);
    this.set_datakeymap(parameters_I.htmlkeymap);

	// html specific properties
	this.ddthtml.add_html2tile();
    this.ddthtml.add_datalist(datalist_I);
};