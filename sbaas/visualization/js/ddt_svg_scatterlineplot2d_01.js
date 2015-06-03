"use strict";
//var ddt_svg_scatterlineplot2d_01 = function () {
function ddt_svg_scatterlineplot2d_01() {
    // scatterlineplot
    // description:
    // data 1 and 2 are plotted along the same axis
    // data 1 = points
    // data 2 = line
    // parameters:
    // parameters_I = e.g., {"svgtype":'scatterlineplot2d_01',"svgkeymap":[data1_keymap,data1_keymap],
    //                        'svgid':'svg1',
    //                        "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
    //                        "svgwidth":500,"svgheight":350,
    //                        "svgx1axislabel":"jump_time_point","svgy1axislabel":"frequency",
    //						  'svgformtileid':'tile1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
    //                where data1_keymap = {'xdata':'time_point',
    //                    'ydata':'mutation_frequency',
    //                    'serieslabel':'mutation_id',
    //                    'featureslabel':''};
    ddt_svg.call(this);
};
ddt_svg_scatterlineplot2d_01.prototype = Object.create(ddt_svg.prototype);
ddt_svg_scatterlineplot2d_01.prototype.constructor = ddt_svg_scatterlineplot2d_01;
ddt_svg_scatterlineplot2d_01.prototype.make_svg = function(data_I,parameters_I){
	// scatterlineplot definition

	this.ddtsvg = new d3_chart2d();
	
	// general svg properties
	this.set_parameters(parameters_I);
	this.set_ddtsvg()
    this.add_data(data_I);
    this.set_datakeymaps(parameters_I.svgkeymap);

	// svg specific properties
    this.ddtsvg.set_margin(parameters_I.svgmargin);
    this.ddtsvg.set_filterdata1and2(true); //filter data 1 and 2 together
    this.ddtsvg.set_width(parameters_I.svgwidth);
    this.ddtsvg.set_height(parameters_I.svgheight);
    this.ddtsvg.set_colorscale(); //color for series_label will remain consistent
    this.ddtsvg.add_svgexportbutton2tile();
//     this.ddtsvg.add_data1filtermenuresetbutton(parameters_I.svgformtileid,parameters_I.svgresetbuttonid)
//     this.ddtsvg.add_data2filtermenuresetbutton(parameters_I.svgformtileid,parameters_I.svgresetbuttonid)
//     this.ddtsvg.add_data1filtermenusubmitbutton(parameters_I.svgformtileid,parameters_I.svgsubmitbuttonid)
//     this.ddtsvg.add_data2filtermenusubmitbutton(parameters_I.svgformtileid,parameters_I.svgsubmitbuttonid)
    //this.ddtsvg.set_tooltip();
    //this.ddtsvg.set_tooltipstyle();
    this.ddtsvg.set_zoom();
    this.ddtsvg.render = function () {
        this.add_chart2d2tile();
        this.set_svgstyle();
        //this.add_title(parameters.svgtitle);
        this.set_x1range("linear");
        this.set_y1range("linear");
        this.set_x1domain();
        this.set_y1domain();
        this.set_x1axis();
        this.set_y1axis();
        this.add_x1axis();
        this.add_y1axis();
        //this.set_x1axiszoom();
        //this.set_y1axiszoom();
        //this.add_zoom();
        // use the same x1/y1 scales for x2/y2
        this.copy_x1scalestox2scales();
        this.copy_y1scalestoy2scales();
        //this.set_colorscale(); //color for series_label will change each update
        // add points
        this.add_pointsdata1();
        this.add_legenddata1();
        this.add_legenddata1filter();
        this.set_legendstyle();
        this.add_pointsdata1tooltipandfill();
        this.set_x1andy1axesstyle();
        this.set_x1andy1axestickstyle();
        this.set_pointsstyle();
        this.add_x1axislabel(parameters_I.svgx1axislabel);
        this.add_y1axislabel(parameters_I.svgy1axislabel);
        this.set_x1andy1axeslabelstyle();
        // add line
		this.set_linedata2("linear");
		this.add_linedata2();
		this.add_linedata2tooltipandstroke();
		this.add_linedata2filter();
        this.set_linestyle();
    };
};