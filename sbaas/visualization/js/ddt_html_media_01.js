"use strict";
//var ddt_html_media_01 = function () {
function ddt_html_media_01() {
    // dropdown button group with href tile
    ddt_html.call(this);
};
ddt_html_media_01.prototype = Object.create(ddt_html.prototype);
ddt_html_media_01.prototype.constructor = ddt_html_media_01;
ddt_html_media_01.prototype.make_html = function(data_I,parameters_I){
    // make href

	this.ddthtml = new d3_html();
	
	// general html properties
	this.set_parameters(parameters_I);
	this.set_ddthtml()
    this.add_data(data_I);
    if (parameters_I.htmlkeymap){this.set_datakeymap(parameters_I.htmlkeymap);}

	// html specific properties
    this.ddthtml.render = function(){
    	// permanent filter on the data
    	if (typeof parameters_I.htmlfilters != "undefined"){
			this.data.change_filters(parameters_I.htmlfilters);
			this.data.filter_stringdata();
    	};
        this.add_html2tile();
		this.set_htmlstyle();
        this.add_mediasvg();
    };
};