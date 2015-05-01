"use strict";
//var ddt_svg_heatmap_01 = function () {
function ddt_svg_heatmap_01() {
    // heatmap
    // description:
    // generic heatmap
    // parameters:
    // parameters_I = e.g., {"svgtype":'heatmap2d_01',"svgkeymap":[data1_keymap],
    //                        'svgid':'svg1',
    //                         'svgcellsize':18,'svgmargin':{ 'top': 200, 'right': 150, 'bottom': 50, 'left': 10 },
    //                        'svgcolorscale':'quantile',
    //                        'svgcolorcategory':'heatmap10',
    //                        'svgcolordomain':[0,1], (frequency) or "min,0,max" (log normalized)
    //                        'svgcolordatalabel':'value',
    //                        'svgdatalisttileid':'tile1'};
    //                  where data1_keymap = {'xdata':'row_leaves','ydata':'col_leaves','zdata':'value',
    //                          'rowslabel':'row_label','columnslabel':'col_label',
    //                          'rowsindex':'row_index','columnsindex':'col_index',
    //                          'rowsleaves':'row_leaves','columnsleaves':'col_leaves'};
    ddt_svg.call(this);
};
ddt_svg_heatmap_01.prototype = Object.create(ddt_svg.prototype);
ddt_svg_heatmap_01.prototype.constructor = ddt_svg_heatmap_01;
ddt_svg_heatmap_01.prototype.make_svg = function(data_I,parameters_I){
	// heatmap definition

	this.ddtsvg = new d3_chart2d();

	// general svg properties
	this.set_parameters(parameters_I);
	this.set_ddtsvg()
    this.add_data(data_I);
    this.set_datakeymaps(parameters_I.svgkeymap);

	// heatmap properties
    this.ddtsvg.set_margin(parameters_I.svgmargin);
    this.ddtsvg.set_heatmapdata1(parameters_I.svgcellsize); //must be done initially to set the height/width correctly
    this.ddtsvg.add_svgexportbutton2tile();
    this.ddtsvg.set_tooltip();
    this.ddtsvg.set_tooltipstyle();
    this.ddtsvg.set_zoom();
    this.ddtsvg.data1.filter_stringdata();
    this.ddtsvg.set_colorscale(parameters_I.svgcolorscale,
								parameters_I.svgcolorcategory,
								parameters_I.svgcolordomain,
								parameters_I.svgcolordatalabel);
    this.ddtsvg.render = function () {
        this.add_chart2d2tile();
        this.set_svgstyle();
        this.set_heatmapdata1(18); //update the heatmap properties
        this.add_heatmapdata1();
        this.add_heatmapdata1animation();
        this.add_heatmapdata1rowlabels(parameters_I.svgdatalisttileid);
        this.add_heatmapdata1columnlabels(parameters_I.svgdatalisttileid);
        this.add_heatmapdata1legend();
        //this.add_heatmapdata1drowpdownmenu("tile1");
        this.add_heatmapdata1datalist(parameters_I.svgdatalisttileid);
        this.add_heatmapdata1tooltipandfill();
        this.set_heatmapdata1css();
    };
};