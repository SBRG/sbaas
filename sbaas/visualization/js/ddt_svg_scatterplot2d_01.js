ddt_svg_scatterlot2d_01 = function () {
    // scatterplot
    // description:
    // generic scatter plot
    ddt_svg.call(this);
};
ddt_svg_scatterlot2d_01.prototype = Object.create(ddt_svg.prototype);
ddt_svg_scatterlot2d_01.prototype.constructor = ddt_svg_scatterlot2d_01;
ddt_svg_scatterlot2d_01.prototype.make_svg = function(data_I,parameters_I){
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
    this.ddtsvg.set_tooltip();
    this.ddtsvg.set_tooltipstyle();
    this.ddtsvg.set_zoom();
    this.ddtsvg.render = function () {
        this.add_chart2d2tile();
        this.set_svgstyle();
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
        this.add_pointsdata1();
        this.add_legenddata1();
        this.add_legenddata1filter();
        this.add_pointsdata1tooltipandfill();
        this.set_x1andy1axesstyle();
        this.set_x1andy1axestickstyle();
        this.set_pointsstyle();
        this.add_x1axislabel(parameters_I.svgx1axislabel);
        this.add_y1axislabel(parameters_I.svgy1axislabel);
        this.set_x1andy1axeslabelstyle();
    };
};