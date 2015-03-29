chart2d = function () {
    // generic chart
    this.id = '';
    this.svgelement = null;
    this.margin = {};
    this.width = 1;
    this.height = 1;
    this.duration = 1;
    this.x1scale = null;
    this.y1scale = null;
    this.x2scale = null;
    this.y2scale = null;
    this.colorscale = null;
    this.data1 = {};
    this.data2 = {};
};
chart2d.prototype.set_id = function () {
    // set chart id
};
chart2d.prototype.set_svgelement = function () {
    // add svg element
};
chart2d.prototype.add_title = function () {
    // add chart title
};
chart2d.prototype.set_margin = function () {
    // set margin properties
};
chart2d.prototype.set_width = function () {
    // set width properties
};
chart2d.prototype.set_height = function () {
    // set height properties
};
chart2d.prototype.set_x1range = function () {
    // set x1-range of the plot
};
chart2d.prototype.set_y1range = function () {
    // set y1-range of the plot
};
chart2d.prototype.set_x1domain = function () {
    // set x1-domain of the plot
};
chart2d.prototype.set_y1domain = function () {
    // set y1-domain of the plot
};
chart2d.prototype.set_x2range = function () {
    // set x2-range of the plot
};
chart2d.prototype.set_y2range = function () {
    // set y2-range of the plot
};
chart2d.prototype.set_x2domain = function () {
    // set x2-domain of the plot
};
chart2d.prototype.set_y2domain = function () {
    // set y2-domain of the plot
};
chart2d.prototype.set_x1scale = function () {
    // set x1 scale
};
chart2d.prototype.set_x2scale = function () {
    // set x2 scale
};
chart2d.prototype.set_y1scale = function () {
    // set y1 scale
};
chart2d.prototype.set_y2scale = function () {
    // set y2 scale
};
chart2d.prototype.set_colorscale = function () {
    // set color scale
};
chart2d.prototype.add_x1axis = function () {
    //x1 axis properties
};
chart2d.prototype.add_x2axis = function () {
    //x2 axis properties
};
chart2d.prototype.add_y1axis = function () {
    //y1 axis properties
};
chart2d.prototype.add_y2axis = function () {
    //y2 axis properties
};
chart2d.prototype.add_x1labels = function () {
    //x1 lables properties
};
chart2d.prototype.add_x2labels = function () {
    //x2 lables properties
};
chart2d.prototype.add_y1labels = function () {
    //y1 lables properties
};
chart2d.prototype.add_y2labels = function () {
    //y2 lables properties
};
chart2d.prototype.add_xgridlines = function () {
    //x axis grid lines properties
};
chart2d.prototype.add_ygridlines = function () {
    //y axis grid lines properties
};
chart2d.prototype.add_x1title = function () {
    //x1 lables properties
};
chart2d.prototype.add_x2title = function () {
    //x2 lables properties
};
chart2d.prototype.add_y1title = function () {
    //y1 lables properties
};
chart2d.prototype.add_y2title = function () {
    //y2 lables properties
};
chart2d.prototype.add_tooltip = function () {
    //tooltip properties
};
chart2d.prototype.add_legend = function () {
    //legend properties
};
chart2d.prototype.update = function () {
    //update the chart
};
chart2d.prototype.draw = function () {
    //draw the chart
};
chart2d.prototype.filter_data = function () {
    //filter chart data
}
chart2d.prototype.make_lines = function () {
    //make lines
};
chart2d.prototype.add_lines = function () {
    //add lines to chart
};
chart2d.prototype.add_points = function () {
    //points properties
};
chart2d.prototype.add_verticalbars = function () {
    //add vertical bars to the plot
};
chart2d.prototype.add_verticalerrorbars = function () {
    //add vertical error bars to the plot
};
chart2d.prototype.add_horizontalbars = function () {
    //add horizontal bars to the plot
};
chart2d.prototype.add_horizontalerrorbars = function () {
    //add horizontal error bars to the plot
};
chart2d.prototype.add_boxandwhiskers = function () {
    //add box and whiskers to the plot
};
chart2d.prototype.add_heatmap = function () {
    //add heatmap to the plot
};
chart2d.prototype.add_svgexport = function () {
    //add svg element export
};