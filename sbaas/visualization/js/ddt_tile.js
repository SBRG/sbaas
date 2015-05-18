"use strict";
//var ddt_tile = function(){
function ddt_tile(){
    this.parameters = {};
    this.tile = null;
};
ddt_tile.prototype.set_parameters = function(parameters_I){
    // set input tile parameters
    if (parameters_I){this.parameters = parameters_I;}
    else {this.parameters = {tileid:"tile1",rowid:"row1",colid:"col1",
        tileclass:"panel panel-default",rowclass:"row",colclass:"col-sm-12"};};
    
};
ddt_tile.prototype.set_tile = function(){
    // set input tile parameters
    var tileid = this.parameters.tileid
    var rowid = this.parameters.rowid
    var colid = this.parameters.colid
    var tileclass = this.parameters.tileclass
    var rowclass = this.parameters.rowclass
    var colclass = this.parameters.colclass

    this.tile = new d3_tile();
    this.tile.set_tileid(tileid);
    this.tile.set_rowid(rowid);
    this.tile.set_colid(colid);
    this.tile.set_tileclass(tileclass);
    this.tile.set_rowclass(rowclass);
    this.tile.set_colclass(colclass);
};
ddt_tile.prototype.make_tile = function(){
    // make the tile
    // define tile make function call sequence here...
};
// update functions
ddt_tile.prototype.update_tile = function(){
    // update the tile
    // define tile update function call sequence here...
};
//var ddt_tile_svg = function () {
function ddt_tile_svg() {
    // form tile
    ddt_tile.call(this);
    this.ddtsvg = null;
};
ddt_tile_svg.prototype = Object.create(ddt_tile.prototype);
ddt_tile_svg.prototype.constructor = ddt_tile_svg;
ddt_tile_svg.prototype.make_tile = function(data_I,parameters_I){
    // make chart2d tile
    var header_I = parameters_I.tileheader;
    var svgtype_I = parameters_I.svgtype;

    this.set_parameters(parameters_I);
    this.set_tile();

    this.tile.add_tile2container();
    this.tile.add_header2tile();
    this.tile.add_removebutton2header();
    this.tile.add_title2header(header_I);
    this.tile.add_body2tile();
    this.tile.add_footer2tile();

    //svg
    this.ddtsvg = this.get_svg(svgtype_I);
    this.ddtsvg.make_svg(data_I,parameters_I)

    this.ddtsvg.ddtsvg.render();
};
ddt_tile_svg.prototype.update_tile = function(data_I){
    // update tile

    //update the data filters...
    //this.ddtsvg.add_data(data_I);
    //this.ddtsvg.filter_data1and2stringdata();
    //re-render the svg
    this.ddtsvg.ddtsvg.render();
};
ddt_tile_svg.prototype.get_svg = function(svgtype_I){
    // return the appropriate tile object
    if (svgtype_I=='heatmap2d_01'){
        return new ddt_svg_heatmap_01();
    } else if (svgtype_I=='scatterlineplot2d_01'){
        return new ddt_svg_scatterlineplot2d_01();
    } else if (svgtype_I=='scatterlineplot2d_02'){
        return new ddt_svg_scatterlineplot2d_02();
    } else if (svgtype_I=='scatterplot2d_01'){
        return new ddt_svg_scatterplot2d_01();
    } else if (svgtype_I=='verticalbarschart2d_01'){
        return new ddt_svg_verticalbarschart2d_01();
    } else if (svgtype_I=='boxandwhiskersplot2d_01'){
        return new ddt_svg_boxandwhiskersplot2d_01();
    } else if (svgtype_I=='volcanoplot2d_01'){
        return new ddt_svg_volcanoplot2d_01();
    //} else if (svgtype_I=='pcaplot2d_loadings_01'){
    //    return new ddt_svg_pcaplot2d_loadings_01();
    } else if (svgtype_I=='pcaplot2d_scores_01'){
        return new ddt_svg_pcaplot2d_scores_01();
    } else {
        return null;
    };
};
//var ddt_tile_table = function () {
function ddt_tile_table() {
    // table tile
    ddt_tile.call(this);
    this.ddttable = null;
};
ddt_tile_table.prototype = Object.create(ddt_tile.prototype);
ddt_tile_table.prototype.constructor = ddt_tile_table;
ddt_tile_table.prototype.make_tile = function(data_I,parameters_I){
    // make table tile
    var header_I = parameters_I.tileheader;
    var tabletype_I = parameters_I.tabletype;

    this.set_parameters(parameters_I);
    this.set_tile();

    this.tile.add_tile2container();
    this.tile.add_header2tile();
    this.tile.add_removebutton2header();
    this.tile.add_title2header(header_I);
    this.tile.add_body2tile();
    this.tile.add_footer2tile();

    //table
    this.ddttable = this.get_table(tabletype_I);
    this.ddttable.make_table(data_I,parameters_I);
    //this.ddttable.make_table(parameters_I);

    this.ddttable.ddttable.render();
    //this.ddttable.ddttable.render(data_I[0]);
};
ddt_tile_table.prototype.update_tile = function(data_I){
    // update tile

    //update the data filters...
    //this.ddttable.add_data(data_I);
    //this.ddttable.ddttable.data.filter_stringdata();
    //re-render the table
    this.ddttable.ddttable.render();
};
ddt_tile_table.prototype.get_table = function(tabletype_I){
    // return the appropriate tile object
    if (tabletype_I=='responsivetable_01'){
        return new ddt_table_responsivetable_01();
    } else {
        return null;
    };
};
//var ddt_tile_html = function () {
function ddt_tile_html() {
    // html tile
    ddt_tile.call(this);
    this.ddthtml = null;
};
ddt_tile_html.prototype = Object.create(ddt_tile.prototype);
ddt_tile_html.prototype.constructor = ddt_tile_html;
ddt_tile_html.prototype.make_tile = function(data_I,parameters_I){
    // make chart2d tile
    var header_I = parameters_I.tileheader;
    var htmltype_I = parameters_I.htmltype;

    this.set_parameters(parameters_I);
    this.set_tile();

    this.tile.add_tile2container();
    this.tile.add_header2tile();
    this.tile.add_removebutton2header();
    this.tile.add_title2header(header_I);
    this.tile.add_body2tile();
    this.tile.add_footer2tile();
    if (parameters_I.formsubmitbuttonidtext){
        this.tile.add_submitbutton2footer(parameters_I.formsubmitbuttonidtext);
        };
    if (parameters_I.formresetbuttonidtext){
        this.tile.add_submitbutton2footer(parameters_I.formresetbuttonidtext);
        };
    if (parameters_I.formupdatebuttonidtext){
        this.tile.add_submitbutton2footer(parameters_I.formupdatebuttonidtext);
        };

    //html
    this.ddthtml = this.get_html(htmltype_I);
    this.ddthtml.make_html(data_I,parameters_I);
    //this.ddthtml.make_html(parameters_I);

    this.ddthtml.ddthtml.render();
    //this.ddthtml.ddthtml.render(data_I[0]);
};
ddt_tile_html.prototype.update_tile = function(data_I){
    // update tile

    //update the data filters...
    //this.ddthtml.add_data(data_I);
    //re-render the html
    this.ddthtml.ddthtml.render();
    //this.ddthtml.update_html(data_I);
};
ddt_tile_html.prototype.get_html = function(htmltype_I){
    // return the appropriate tile object
    if (htmltype_I=='form_01'){
        return new ddt_html_form_01();
    } else if (htmltype_I=='datalist_01'){
        return new ddt_html_datalist_01();
    } else if (htmltype_I=='href_01'){
        return new ddt_html_href_01();
    } else if (htmltype_I=='media_01'){
        return new ddt_html_media_01();
    } else if (htmltype_I=='escher_01'){
        return new ddt_html_escher_01();
    } else {
        return null;
    };
};