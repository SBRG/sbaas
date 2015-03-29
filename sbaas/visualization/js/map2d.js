map2d = function () {
    // generic chart
    this.id = '';
    this.svgelement = null;
    this.margin = {};
    this.width = 1;
    this.height = 1;
    this.duration = 1;
    this.mapprojection = null;
    this.xnscale = null; //x scale for each data type
    this.ynscale = null; //y scale for each data type
    this.mapcolorscale = null;
    this.datancolorscale = null; //color scale for each data type
    this.mapdata = {};
    this.datan = {}; //container for each data type
};
map2d.prototype.set_id = function () {
    // set map id
};
map2d.prototype.set_svgelement = function () {
    // set svg element
};
map2d.prototype.set_title = function () {
    // set chart title
};
map2d.prototype.set_margin = function () {
    // set margin properties
};
map2d.prototype.set_width = function () {
    // set width properties
};
map2d.prototype.set_height = function () {
    // set height properties
};
map2d.prototype.add_svgexport = function () {
    //add svg element export
};