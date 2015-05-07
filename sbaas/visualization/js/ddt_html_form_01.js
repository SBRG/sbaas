"use strict";
//var ddt_html_form_01 = function () {
function ddt_html_form_01() {
    // form tile
    ddt_html.call(this);
};
ddt_html_form_01.prototype = Object.create(ddt_html.prototype);
ddt_html_form_01.prototype.constructor = ddt_html_form_01;
ddt_html_form_01.prototype.make_html = function(data_I,parameters_I){
//ddt_html_form_01.prototype.make_html = function(parameters_I){
    // make form

	this.ddthtml = new d3_html();
	
	// general html properties
	this.set_parameters(parameters_I);
	this.set_ddthtml()
    this.add_data(data_I);
    if (parameters_I.htmlkeymap){this.set_datakeymap(parameters_I.htmlkeymap);}

	// html specific properties
    this.ddthtml.render = function(){
        this.add_html2tile();
        this.add_form();
        this.add_input2form();
        // The below code causes the application to crash
        // reason: unknown
        // hypothesis: binding of "onclick" event generates an infinite loop
        // workaround: added submitbuttons to the tile where they are not associated with any bound data
//         this.add_submitbutton2form([parameters_I.formsubmitbuttonidtext,
//         	parameters_I.formresetbuttonidtext,
//         	parameters_I.formupdatebuttonidtext]);
    };
};
ddt_html_form_01.prototype.update_html = function(data_I){
    // update form
    var input = data_I[0].convert_filter2stringmenuinput();
    this.ddthtml.update_forminput(input);
};