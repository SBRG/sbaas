"use strict";
function ddt_html_href_02() {
    // dropdown button group with href tile
    ddt_html.call(this);
};
ddt_html_href_02.prototype = Object.create(ddt_html.prototype);
ddt_html_href_02.prototype.constructor = ddt_html_href_02;
ddt_html_href_02.prototype.make_html = function(data_I,parameters_I){
    // make href

	this.ddthtml = new d3_html();
	
	// general html properties
	this.set_parameters(parameters_I);
	this.set_ddthtml()
    this.add_data(data_I);
    if (parameters_I.htmlkeymap){this.set_datakeymap(parameters_I.htmlkeymap);};

	// html specific properties
	this.ddthtml.set_url(parameters_I.hrefurl);
	if (parameters_I.formsubmitbuttonidtext){this.ddthtml.set_formsubmitbuttonidtext(parameters_I.formsubmitbuttonidtext)};
    this.ddthtml.render = function(){
    	// permanent filter on the data
    	if (typeof parameters_I.htmlfilters != "undefined"){
			this.data.change_filters(parameters_I.htmlfilters);
			this.data.filter_stringdata();
    	};
        this.add_html2tile();
		this.set_htmlstyle();
        this.add_headeranddatalist_href();
        if (parameters_I.formsubmitbuttonidtext){this.add_headeranddatalistsubmit_href()};
    };
};