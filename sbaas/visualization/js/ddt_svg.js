var ddt_svg = function(){
    // ddt_svg template class
    this.parameters = {};
    this.ddtsvg = null;
};
ddt_svg.prototype.set_parameters = function(parameters_I){
    // set chart2d parameters
    this.parameters = parameters_I;
};
ddt_svg.prototype.set_ddtsvg = function(){
    // set ddtsvg tileid
	var tileid_I = this.parameters.tileid;
	var id_I = this.parameters.svgid;

    this.ddtsvg.set_tileid(tileid_I);
    this.ddtsvg.set_id(id_I);
};
ddt_svg.prototype.add_data = function(data_I){
    // add data to ddtsvg
    this.ddtsvg.add_data(data_I);
};
ddt_svg.prototype.set_datakeymaps = function(set_datakeymaps_I){
    // add data to ddtsvg
    this.ddtsvg.set_datakeymaps(set_datakeymaps_I);
};
ddt_svg.prototype.filter_data1and2stringdata = function(){
    // add data to ddtsvg
    this.ddtsvg.filter_data1and2stringdata();
};