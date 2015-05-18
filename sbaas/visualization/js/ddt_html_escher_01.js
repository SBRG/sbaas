"use strict";
//var ddt_html_escher_01 = function () {
function ddt_html_escher_01() {
    // dropdown button group with href tile
    ddt_html.call(this);
};
ddt_html_escher_01.prototype = Object.create(ddt_html.prototype);
ddt_html_escher_01.prototype.constructor = ddt_html_escher_01;
ddt_html_escher_01.prototype.make_html = function(data_I,parameters_I){
    // make href

	this.ddthtml = new d3_html();
	
	// general html properties
	this.set_parameters(parameters_I);
	this.set_ddthtml()

	// html specific properties
    this.ddthtml.add_ndata(data_I);
    if (parameters_I.htmlkeymap){this.ddthtml.set_ndatakeymap(parameters_I.htmlkeymap);}
	this.ddthtml.set_escher(parameters_I.escherdataindex,parameters_I.escherembeddedcss,parameters_I.escheroptions)
    this.ddthtml.render = function(){
    	// permanent filter on the data
    	if (typeof parameters_I.htmlfilters != "undefined"){
			this.data.change_filters(parameters_I.htmlfilters);
			this.data.filter_stringdata();
    	};
        this.add_html2tile();
		this.set_htmlescherstyle();
        this.add_escher();
    };
};