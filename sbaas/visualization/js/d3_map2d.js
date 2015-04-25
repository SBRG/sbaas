//TODO:
d3_map2d = function () {
    // generic map
    this.id = '';
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
d3_map2d.prototype = Object.create(d3_svg.prototype);
d3_map2d.prototype.constructor = d3_map2d;
d3_map2d.prototype.set_svgelement = function () {
    // set svg element
};
d3_map2d.prototype.set_title = function () {
    // set chart title
};
d3_map2d.prototype.set_margin = function () {
    // set margin properties
};
d3_map2d.prototype.set_width = function () {
    // set width properties
};
d3_map2d.prototype.set_height = function () {
    // set height properties
};
d3_map2d.prototype.add_svgexport = function () {
    //add svg element export
};