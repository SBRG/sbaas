var ddt_table = function(){
    // ddt_table template class
    this.parameters = {};
    this.ddttable = null;
};
ddt_table.prototype.set_parameters = function(parameters_I){
    // set chart2d parameters
    this.parameters = parameters_I;
};
ddt_table.prototype.set_ddttable = function(){
    // set ddttable tileid
	var tileid_I = this.parameters.tileid;
	var id_I = this.parameters.tableid;

    this.ddttable.set_tileid(tileid_I);
    this.ddttable.set_id(id_I);
};
ddt_table.prototype.add_data = function(data_I){
    // add data to ddttable
    this.ddttable.add_data(data_I[0]);
};