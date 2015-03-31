d3_tile = function () {
    // generic d3_tile element
    this.containerid = 'container'
    this.tileid = '';
    this.rowid = '';
    this.colid = '';
    this.rowclass = '';
    this.colclass = '';
    this.tile = null;
    this.width = 1;
    this.height = 1;
};
d3_tile.prototype.set_tileid = function (tileid_I) {
    // set d3_tile id
    this.tileid = tileid_I;
};
d3_tile.prototype.set_rowid = function (rowid_I) {
    // set row id
    this.rowid = rowid_I;
};
d3_tile.prototype.set_colid = function (colid_I) {
    // set column id
    this.colid = colid_I;
};
d3_tile.prototype.set_rowclass = function (rowclass_I) {
    // set row class
    this.rowclass = rowclass_I;
};
d3_tile.prototype.set_colclass = function (colclass_I) {
    // set column class
    this.colclass = colclass_I;
};
d3_tile.prototype.add_tile2container = function () {
    // set column id
    var row = d3.select("#" + this.containerid).append("div").attr("class", this.rowclass).attr("id", this.rowid);
    var col = row.append("div").attr("class", this.colclass).attr("id", this.colid);
    this.tile = col.append("div").attr("id", this.tileid);
};
d3_tile.prototype.set_height = function () {
    // set d3_tile height
};
d3_tile.prototype.add_datalist = function () {
    // add datalist (menu) for input
};
d3_tile.prototype.add_draganddrop = function () {
    // add file drag and drop for input
};
d3_tile.prototype.add_textarea = function () {
    // add text area for input
};
d3_tile.prototype.add_checkbox = function () {
    // add checkbox for input
};
d3_tile.prototype.add_color = function () {
    // add color pallet for input
};
d3_tile.prototype.add_range = function () {
    // add range slider for input
};
d3_tile.prototype.add_submitbutton = function () {
    // add submit button
};
d3_tile.prototype.add_table = function () {
    // add button for output
};
d3_tile.prototype.add_svg = function () {
    // add svg for interaction
};
d3_tile.prototype.add_chart2d = function () {
    // add chart for interaction
};
d3_tile.prototype.add_map2d = function () {
    // add chart for interaction
};
d3_svg = function () {
    // generic chart
    this.id = '';
    this.tileid = '';
    this.svgelement = null;
    this.svgg = null;
    this.margin = {};
    this.width = 1;
    this.height = 1;
};
d3_svg.prototype.set_tileid = function (tileid_I) {
    // set svg tile id
    this.tileid = tileid_I;
};
d3_svg.prototype.set_id = function (id_I) {
    // set svg id
    this.id = id_I;
};
d3_svg.prototype.set_margin = function (margin_I) {
    // set margin properties
    this.margin = margin_I;
};
d3_svg.prototype.set_width = function (width_I) {
    // set width properties
    this.width = width_I;
};
d3_svg.prototype.set_height = function (height_I) {
    // set height properties
    this.height = height_I;
};
d3_svg.prototype.add_svgelement2tile = function () {
    // add svg element to parent tile

    this.svgelement = d3.select('#'+this.tileid)
        .append("svg").attr("id",this.id);

    this.svgelement.attr("width", this.width + this.margin.left + this.margin.right)
        .attr("height", this.height + this.margin.top + this.margin.bottom);

    this.svgg = this.svgelement
        .append('g').attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

};
d3_svg.prototype.add_svgexportbutton2tile = function () {
    // add button to export the svg element
    var svgexportbutton = d3.select('#'+this.tileid).append("form");

    var svgexportbutton_label = svgexportbutton.append("label");
    svgexportbutton_label.text("Export as SVG");

    var svgexportbutton_input = svgexportbutton.append("input");
    svgexportbutton_input.attr("type", "button")
        .attr("value", "Download");
    svgexportbutton_input.on("click",this.export_svgelement);

};
d3_svg.prototype.export_svgelement = function () {
    // export the svg element

    //Input:
    // do_beautify = boolean (requires beautify plugin)

    var do_beautify_I = true;
    var a = document.createElement('a'), xml, ev;
    a.download = 'figure' + '.svg'; // file name
    // convert node to xml string
    //xml = (new XMLSerializer()).serializeToString(d3.select(svg_sel).node()); //div element interferes with reading the svg file in illustrator/pdf/inkscape
    //xml = (new XMLSerializer()).serializeToString(this.svgelement[0][0]);
    var form = d3.select(this.parentNode);
    var tile = form.node().parentNode;
    //assumption: the svg element is the first child of the tile
    xml = (new XMLSerializer()).serializeToString(tile.children[0]);
    if (do_beautify_I) xml = vkbeautify.xml(xml);
    xml = '<?xml version="1.0" encoding="utf-8"?>\n \
            <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n \
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n' + xml;
    a.setAttribute("href-lang", "image/svg+xml");
    a.href = 'data:image/svg+xml;base64,' + utf8_to_b64(xml); // create data uri
    // <a> constructed, simulate mouse click on it
    ev = document.createEvent("MouseEvents");
    ev.initMouseEvent("click", true, false, self, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    a.dispatchEvent(ev);

    // definitions
    function utf8_to_b64(str) {
        return window.btoa(unescape(encodeURIComponent(str)));
    }
};
d3_map2d = function () {
    // generic chart
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
d3_chart2d = function () {
    // generic chart
    // data1 = [{x_data:float,y_data:float,series_label:string,text_labels:string}]
    d3_svg.call(this);
    this.svgdata = null;
    this.svgenter = null;
    this.svgsvg = null;
    this.svgg = null;
    this.duration = 1;
    this.x1scale = null;
    this.y1scale = null;
    this.x2scale = null;
    this.y2scale = null;
    this._x1axis = null;
    this._x2axis = null;
    this._y1axis = null;
    this._y2axis = null;
    this.x1axis = null;
    this.x2axis = null;
    this.y1axis = null;
    this.y2axis = null;
    this.colorscale = null;
    this.data1 = {};
    this.data2 = {};
    this.clippath = null;
    this.title = null;

};
d3_chart2d.prototype = Object.create(d3_svg.prototype);
d3_chart2d.prototype.constructor = d3_chart2d;
d3_chart2d.prototype.add_chart2d2tile = function(){
    // add char2d to tile

    this.svgelement = d3.select('#' + this.tileid).selectAll("svg");
    this.svgdata = this.svgelement.data([0]); //can also be [this.data1]
    this.svgenter = this.svgdata.enter();
    this.svgsvg = this.svgenter
        .append("svg").attr("id", this.id);
    this.svgg = this.svgsvg.append('g')
        .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
    //set the svgdata attribute after appending g
    this.svgdata.attr("width", this.width + this.margin.left + this.margin.right)
        .attr("height", this.height + this.margin.top + this.margin.bottom);

};
d3_chart2d.prototype.add_title = function (title_I) {
    // add chart title
    this.title = this.svgg.append("text")
    .attr("x", this.width / 2)
    .attr("y", -this.margin.top / 2)
    .attr("class", "title")
    .attr("id", this.id+"title")
    .style("text-anchor", "middle")
    .text(title_I);
};
d3_chart2d.prototype.remove_title = function () {
    // add chart title
    this.title.remove();
    this.title = null;
};
d3_chart2d.prototype.add_clippath = function () {
    // add clippath to chart
    this.clippath = this.svgg.append("clippath")
          .attr("id", "clip")
        .append("rect")
          .attr("class", "mesh")
          .attr("width", this.width)
          .attr("height", this.height);
};
d3_chart2d.prototype.remove_clippath = function () {
    // remove clippath from chart
    this.clippath.node().parentNode.remove();
    this.clippath = null;
};
d3_chart2d.prototype.set_x1range = function (scale_I) {
    // set x1-range of the plot
    if (scale_I === 'linear') {
        this.x1scale = d3.scale.linear().range([0,this.width])
    }
};
d3_chart2d.prototype.set_y1range = function (scale_I) {
    // set y1-range of the plot
    if (scale_I === 'linear') {
        this.y1scale = d3.scale.linear().range([this.height, 0])
    }
};
d3_chart2d.prototype.set_x2range = function (scale_I) {
    // set x2-range of the plot
    if (scale_I === 'linear') {
        this.x2scale = d3.scale.linear().range([0, this.width])
    }
};
d3_chart2d.prototype.set_y2range = function (scale_I) {
    // set y1-range of the plot
    if (scale_I === 'linear') {
        this.y2scale = d3.scale.linear().range([this.height, 0])
    }
};
d3_chart2d.prototype.add_data1 = function (data1_I) {
    //add data1
    this.data1 = data1_I;
};
d3_chart2d.prototype.add_data2 = function (data2_I) {
    //add data2 element export
    this.data2 = data2_I;
};
d3_chart2d.prototype.set_x1domain = function () {
    // set x1-domain of the plot
    this.x1scale.domain(d3.extent(this.data1, function (d) { return d.x_data; })).nice();
};
d3_chart2d.prototype.set_y1domain = function () {
    // set y1-domain of the plot
    this.y1scale.domain(d3.extent(this.data1, function (d) { return d.y_data; })).nice();
};
d3_chart2d.prototype.set_x2domain = function () {
    // set x2-domain of the plot
    this.x2scale.domain(d3.extent(this.data2, function (d) { return d.x_data; })).nice();
};
d3_chart2d.prototype.set_y2domain = function () {
    // set y2-domain of the plot
    this.x2scale.domain(d3.extent(this.data2, function (d) { return d.y_data; })).nice();
};
d3_chart2d.prototype.set_colorscale = function () {
    // set color scale
    // add in option to change color scale
    this.colorscale = d3_chart2d.scale.category20c();
};
d3_chart2d.prototype.set_x1axis = function () {
    //x1 axis properties
    this._x1axis = d3.svg.axis().scale(this.x1scale)
            .orient("bottom");
};
d3_chart2d.prototype.set_x2axis = function () {
    //x2 axis properties
    this._x2axis = d3.svg.axis().scale(this.x2scale)
            .orient("top");
};
d3_chart2d.prototype.set_y1axis = function () {
    //y1 axis properties
    this._y1axis = d3.svg.axis()
            .scale(this.y1scale)
            .orient("left");
};
d3_chart2d.prototype.set_y2axis = function () {
    //y2 axis properties
    this._y2axis = d3.svg.axis()
            .scale(this.y2scale)
            .orient("right");
};
d3_chart2d.prototype.add_x1axis = function () {
    //add x1 axis
    this.x1axis = this.svgg.append("g")
            .attr("class", "x1axis")
            .attr("id", this.id + "x1axis")
            .attr("transform", "translate(0," + this.height + ")")
            .transition()
            .call(this._x1axis);
};
d3_chart2d.prototype.add_x2axis = function () {
    //add x2 axis
    this.x2axis = this.svgg.append("g")
            .attr("class", "x2axis")
            .attr("id", this.id + "x2axis")
            .transition()
            .call(this._x2axis);
};
d3_chart2d.prototype.add_y1axis = function () {
    //add y1 axis
    this.y1axis = this.svgg.append("g")
            .attr("class", "y1axis")
            .attr("id", this.id + "y1axis")
            .transition()
            .call(this._y1axis);
};
d3_chart2d.prototype.add_y2axis = function () {
    //add y2 axis
    this.y2axis = this.svgg.append("g")
            .attr("class", "y2axis")
            .attr("id", this.id + "y2axis")
            .attr("transform", "translate(" + width + ",0)")
            .transition()
            .call(this._y2axis);
};
d3_chart2d.prototype.set_x1tickformat = function () {
    //set x1ticklabels properties
};
d3_chart2d.prototype.set_x2tickformat = function () {
    //set x2ticklabels properties
};
d3_chart2d.prototype.set_y1tickformat = function () {
    //set y1ticklabels properties
};
d3_chart2d.prototype.set_y2tickformat = function () {
    //set y2ticklabels properties
};
d3_chart2d.prototype.add_xgridlines = function () {
    //x axis grid lines properties
    this.x1axisgridlines = this.svgg.selectAll("xgridlines")
      .data(this.x1scale.ticks(10))
      .enter().append("line")
      .attr("class", "xgridlines")
      .attr("id", this.id+"xgridlines")
      .attr("x1", this.x1scale)
      .attr("x2", this.x1scale)
      .attr("y1", d3.min(this.data1, function (d) { return d.y_data; }))
      .attr("y2", d3.max(this.data1, function (d) { return d.y_data; }))
      .style("stroke", "#ccc");
};
d3_chart2d.prototype.add_ygridlines = function () {
    //y axis grid lines properties
};
d3_chart2d.prototype.set_x1axislabel = function (x1axislabel_I) {
    //set x1axis label properties
    this.x1axis.append("text")
        .attr("class", "label")
        .attr("x", this.width / 2)
        .attr("y", 28)
        .style("text-anchor", "middle")
        .text(x1axislabel_I);
};
d3_chart2d.prototype.set_x2axislabel = function () {
    //set x2axis label properties
};
d3_chart2d.prototype.set_y1axislabel = function (y1axislabel) {
    //set y1axis label properties
    this.x2axis.append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("y", -28)
        .attr("x", -height / 2)
        .style("text-anchor", "middle")
        .text(y1axislabel);
};
d3_chart2d.prototype.set_y2axislabel = function () {
    //set y2axis label properties
};
d3_chart2d.prototype.set_x1axisstyle = function (x1axissyle_I) {
    //set x1axis style properties
    d3.selectAll('#' + this.id + 'y1axis').style(x1axissyle_I);
};
d3_chart2d.prototype.set_y1axisstyle = function (y1axissyle_I) {
    //set y1axis style properties
    this.y1axis.style(y1axissyle_I);
};
d3_chart2d.prototype.add_tooltip = function () {
    //tooltip properties
};
d3_chart2d.prototype.add_legend = function () {
    //legend properties
};
d3_chart2d.prototype.update = function () {
    //update the chart
};
d3_chart2d.prototype.draw = function () {
    //draw the chart
};
d3_chart2d.prototype.filter_data = function () {
    //filter chart data
}
d3_chart2d.prototype.make_lines = function () {
    //make lines
};
d3_chart2d.prototype.add_lines = function () {
    //add lines to chart
};
d3_chart2d.prototype.add_points = function () {
    //points properties
};
d3_chart2d.prototype.add_verticalbars = function () {
    //add vertical bars to the plot
};
d3_chart2d.prototype.add_verticalerrorbars = function () {
    //add vertical error bars to the plot
};
d3_chart2d.prototype.add_horizontalbars = function () {
    //add horizontal bars to the plot
};
d3_chart2d.prototype.add_horizontalerrorbars = function () {
    //add horizontal error bars to the plot
};
d3_chart2d.prototype.add_boxandwhiskers = function () {
    //add box and whiskers to the plot
};
d3_chart2d.prototype.add_heatmap = function () {
    //add heatmap to the plot
};
d3_chart2d.prototype.remove_x1axis = function () {
    //remove x1 axis
    d3.selectAll('#'+this.id + 'x1axis').remove();
    this.x1axis = null;
};
d3_chart2d.prototype.remove_x2axis = function () {
    //remove x2 axis
    d3.selectAll('#' + this.id + 'x2axis').remove();
    this.x2axis = null;
};
d3_chart2d.prototype.remove_y1axis = function () {
    //remove y1 axis
    d3.selectAll('#' + this.id + 'y1axis').remove();
    this.y1axis = null;
};
d3_chart2d.prototype.remove_y2axis = function () {
    //remove y2 axis
    d3.selectAll('#' + this.id + 'y2axis').remove();
    this.y2axis = null;
};