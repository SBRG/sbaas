ddt_svg_boxandwhiskersplot2d_01 = function () {
    // boxandwhiskersplot
    // description:
    // data 1 and 2 are plotted along the same axis
    // data 1 = points
    // data 2 = line
    // parameters:
    // parameters_I = e.g., {"svgtype":'boxandwhiskersplot2d_01',"svgkeymap":[data1_keymap],
    //                        'svgid':'svg1',
    //                        "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
    //                        "svgwidth":500,"svgheight":350,
    //                        "svgx1axislabel":"jump_time_point","svgy1axislabel":"frequency"};
    ddt_svg.call(this);
};
ddt_svg_boxandwhiskersplot2d_01.prototype = Object.create(ddt_svg.prototype);
ddt_svg_boxandwhiskersplot2d_01.prototype.constructor = ddt_svg_boxandwhiskersplot2d_01;
ddt_svg_boxandwhiskersplot2d_01.prototype.make_svg = function(data_I,parameters_I){
	// boxandwhiskersplot definition

	this.ddtsvg = new d3_chart2d();
	
	// general svg properties
	this.set_parameters(parameters_I);
	this.set_ddtsvg()
    this.add_data(data_I);
    this.set_datakeymaps(parameters_I.svgkeymap);

	// svg specific properties
    this.ddtsvg.set_margin(parameters_I.svgmargin);
    this.ddtsvg.set_width(parameters_I.svgwidth);
    this.ddtsvg.set_height(parameters_I.svgheight);
    this.ddtsvg.set_colorscale(); //color for series_label will remain consistent
    this.ddtsvg.add_svgexportbutton2tile();
    this.ddtsvg.set_tooltip();
    this.ddtsvg.set_tooltipstyle();
    this.ddtsvg.set_zoom();
    this.ddtsvg.render = function () {
        this.add_chart2d2tile();
        this.set_svgstyle();
    };
};