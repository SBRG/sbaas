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
    svgexportbutton_input.on("click", this.export_svgelement);

};
d3_svg.prototype.export_svgelement = function () {
    // export the svg element

    //Input:
    // do_beautify = boolean (requires beautify plugin)

    var do_beautify_I = true;
    var a = document.createElement('a'), xml, ev;
    var id = this.id;
    a.download = 'figure' + '.svg'; // file name
    // convert node to xml string
    //xml = (new XMLSerializer()).serializeToString(d3.select(svg_sel).node()); //div element interferes with reading the svg file in illustrator/pdf/inkscape
    //xml = (new XMLSerializer()).serializeToString(this.svgelement[0][0]);
    var form = d3.select(this.parentNode);
    var tile = form.node().parentNode;
    // find the index of the svg element
    var svgid = null;
    for (i = 0; i < tile.children.length; i++) {
        if (tile.children[i].nodeName === 'svg') {
            svgid = i;};
    };
    xml = (new XMLSerializer()).serializeToString(tile.children[svgid]);
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
d3_chart2d = function () {
    // generic chart
    d3_svg.call(this);
    //this.svgdata = null;
    this.svgenter = null;
    //this.svgsvg = null;
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
    this.data1xdata = '';
    this.data1ydata = '';
    this.data1serieslabel = '';
    this.data1featurelabel = '';
    this.data2xdata = '';
    this.data2ydata = '';
    this.data2serieslabel = '';
    this.data2featureslabel = '';
    this.data1 = null; //d3_data
    this.data2 = null; //d3_data
    this.clippath = null;
    this.title = null;
    this.x1axisgridlines = null;
    this.y1axisgridlines = null;
    this.x1axisgridlinesenter = null;
    this.y1axisgridlinesenter = null;
    this.tooltip = null;
    this.pointsdata1 = null;
    this.pointsdata2 = null;
    this.pointsdata1enter = null;
    this.pointsdata2enter = null;
    this.legenddata1 = null;
    this.legenddata1enter = null;
    this.render = null; // function defining the calls to make the chart

};
d3_chart2d.prototype = Object.create(d3_svg.prototype);
d3_chart2d.prototype.constructor = d3_chart2d;
d3_chart2d.prototype.add_chart2d2tile = function(){
    // add char2d to tile

    this.svgelement = d3.select('#' + this.tileid).selectAll("svg")
        .data([this.data1.listdatafiltered]);
    this.svgenter = this.svgelement.enter()
        .append("svg")
        .attr("id", this.id)
        .append('g')
        .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
    this.svgelement.attr("width", this.width + this.margin.left + this.margin.right)
        .attr("height", this.height + this.margin.top + this.margin.bottom);

    this.svgg = this.svgelement.select('g');

    //this.svgelement = d3.select('#' + this.tileid).selectAll("svg");
    //this.svgdata = this.svgelement.data([this.data1.listdatafiltered]);
    //this.svgenter = this.svgdata.enter();
    //this.svgsvg = this.svgenter
    //    .append("svg").attr("id", this.id);
    //this.svgg = this.svgsvg.append('g')
    //    .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
    ////set the svgdata attribute after appending g
    //this.svgdata.attr("width", this.width + this.margin.left + this.margin.right)
    //    .attr("height", this.height + this.margin.top + this.margin.bottom);

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
          .attr("class", "clippath")
          .attr("id", this.id + "clippath")
        .append("rect")
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
    var x_data = this.data1xdata;
    var _this = this;
    this.x1scale.domain(d3.extent(_this.data1.listdatafiltered, function (d) { return d[x_data]; })).nice();
};
d3_chart2d.prototype.set_y1domain = function () {
    // set y1-domain of the plot
    var y_data = this.data1ydata;
    var _this = this;
    this.y1scale.domain(d3.extent(_this.data1.listdatafiltered, function (d) { return d[y_data]; })).nice();
};
d3_chart2d.prototype.set_x2domain = function () {
    // set x2-domain of the plot
    var x_data = this.data2xdata;
    var _this = this;
    this.x2scale.domain(d3.extent(_this.data2.listdatafiltered, function (d) { return d[x_data]; })).nice();
};
d3_chart2d.prototype.set_y2domain = function () {
    // set y2-domain of the plot
    var y_data = this.data2ydata;
    var _this = this;
    this.x2scale.domain(d3.extent(_this.data2.listdatafiltered, function (d) { return d[y_data]; })).nice();
};
d3_chart2d.prototype.set_colorscale = function () {
    // set color scale
    // add in option to change color scale
    this.colorscale = d3.scale.category20c();
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
    this.x1axis = this.svgenter.append("g")
            .attr("class", "x1axis")
            .attr("id", this.id + "x1axis")
            .attr("transform", "translate(0," + this.height + ")");
    //this.svgg.select('g.x1axis') //can be used as well
    this.x1axis.transition()
            .call(this._x1axis);
};
d3_chart2d.prototype.add_x2axis = function () {
    //add x2 axis
    this.x2axis = this.svgenter.append("g")
            .attr("class", "x2axis")
            .attr("id", this.id + "x2axis");
    this.x2axis.transition()
            .call(this._x2axis);
};
d3_chart2d.prototype.add_y1axis = function () {
    //add y1 axis
    this.y1axis = this.svgenter.append("g")
            .attr("class", "y1axis")
            .attr("id", this.id + "y1axis");
    //this.svgg.select('g.y1axis') //can be used as well
    this.y1axis.transition()
            .call(this._y1axis);
};
d3_chart2d.prototype.add_y2axis = function () {
    //add y2 axis
    this.y2axis = this.svgenter.append("g")
            .attr("class", "y2axis")
            .attr("id", this.id + "y2axis")
            .attr("transform", "translate(" + width + ",0)");

    this.y2axis.transition()
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
d3_chart2d.prototype.add_x1axisgridlines = function () {
    //x axis grid lines properties
    //TODO:
    var y_data = this.data1ydata;
    var x1scale = this.x1scale;
    var listdatafiltered = this.data1.listdatafiltered;

    this.x1axisgridlines = this.svgg.selectAll("line")
      .data(this.x1scale.ticks(10));

    this.x1axisgridlines.exit().remove();

    this.x1axisgridlinesenter = this.x1axisgridlines.enter()
      .append("line")
      .attr("class", "xgridlines")
      .attr("id", this.id + "xgridlines")
      .attr("x1", x1scale)
      .attr("x2", x1scale)
      .attr("y1", d3.min(listdatafiltered, function (d) { return d[y_data]; }))
      .attr("y2", d3.max(listdatafiltered, function (d) { return d[y_data]; }))
      .style("stroke", "#ccc");
};
d3_chart2d.prototype.add_y1axisgridlines = function () {
    //y axis grid lines properties
    //TODO:
    var x_data = this.data1ydata;
    var y1scale = this.y1scale;
    var listdatafiltered = this.data1.listdatafiltered;

    this.y1axisgridlines = this.svgg.selectAll(".ygridlines")
    .data(this.y1scale.ticks(10));

    this.y1axisgridlines.exit().remove();

    this.y1axisgridlinesenter = this.y1axisgridlines.enter()
        .append("line")
        .attr("class", "ygridlines")
        .attr("id", this.id + "ygridlines")
        .attr("x1", d3.min(listdatafiltered, function (d) { return d[x_data]; }))
        .attr("x2", d3.max(listdatafiltered, function (d) { return d[x_data]; }))
        .attr("y1", y1scale)
        .attr("y2", y1scale)
        .style("stroke", "#ccc");
};
d3_chart2d.prototype.add_x1axislabel = function (x1axislabel_I) {
    //add x1axis label properties
    this.x1axis.append("text")
        .attr("class", "label")
        .attr("x", this.width / 2)
        .attr("y", 28)
        .style("text-anchor", "middle")
        .text(x1axislabel_I);
};
d3_chart2d.prototype.add_x2axislabel = function (x2axislabel_I) {
    //set x2axis label properties
    this.x1axis.append("text")
        .attr("class", "label")
        .attr("x", this.width / 2)
        .attr("y", -28)
        .style("text-anchor", "middle")
        .text(x2axislabel_I);
};
d3_chart2d.prototype.add_y1axislabel = function (y1axislabel) {
    //set y1axis label properties
    this.y1axis.append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("y", -28)
        .attr("x", -this.height / 2)
        .style("text-anchor", "middle")
        .text(y1axislabel);
};
d3_chart2d.prototype.add_y2axislabel = function (y2axislabel) {
    //set y2axis label properties
    this.y2axis.append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("y", 28)
        .attr("x", -this.height / 2)
        .style("text-anchor", "middle")
        .text(y2axislabel);
};
d3_chart2d.prototype.set_tooltip = function () {
    //set tooltip properties
    var series_label = this.data1serieslabel;

    this.tooltip = d3.select("#" + this.tileid)
        .append("div")
        .attr('class', 'hidden')
        .attr('id', this.id + 'tooltip')
        .append('p')
        .attr('id', this.id + 'value');
};
d3_chart2d.prototype.set_tooltipstyle = function () {
    //set tooltip css properties
    var tooltipselector = "#" + this.id + 'tooltip';
    //var tooltipstyle = {
    //        'line-height': '1',
    //        'font-weight': 'bold',
    //        'padding': '12px',
    //        'background': 'rgba(0, 0, 0, 0.8)',
    //        'color': '#fff',
    //        'border-radius': '2px'
    //};
    var tooltipstyle = {'position': 'fixed',
        'width': '200px',
        'height': 'auto',
        'padding': '10px',
        'background-color': 'white',
        '-webkit-border-radius': '10px',
        '-moz-border-radius': '10px',
        'border-radius': '10px',
        '-webkit-box-shadow': '4px 4px 10px rgba(0, 0, 0, 0.4)',
        '-moz-box-shadow': '4px 4px 10px rgba(0, 0, 0, 0.4)',
        'box-shadow': '4px 4px 10px rgba(0, 0, 0, 0.4)',
        'pointer-events': 'none'
    };
    var selectionstyle = [{ 'selection': tooltipselector, 'style': tooltipstyle }];
    this.set_d3css(selectionstyle);
};
d3_chart2d.prototype.add_legenddata1filter = function () {
    //filter the data on click

    //update data and graphic upon click
    var series_label = this.data1serieslabel;
    var _this = this;

    this.legenddata1enter.on("click", function (d) {
        var filters = [];
        _this.data1.filters[series_label].forEach(function (n) { if (n !== d.key) { filters.push(n);}; });
        _this.data1.filters[series_label] = filters;
        _this.data1.filter_stringdata();
        _this.render();
    });
};
d3_chart2d.prototype.add_legenddata1 = function () {
    //legend properties
    //legend location is predifined

    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var series_label = this.data1serieslabel;
    var colorscale = this.colorscale;
    var width = this.width;
    var id = this.id;

    this.legenddata1 = this.svgg.selectAll('.legendelement')
        .data(this.data1.nestdatafiltered);

    //var legendg = this.svgg.append('g')
    //    .attr('class', 'legend')
    //    .attr('id', this.id + 'legend')
    //    .attr('transform', "translate(" + width + "," + 0 + ")");

    //this.legend = legendg.selectAll('legendelement')
    //    .data(this.data1.nestdatafiltered);

    this.legenddata1enter = this.legenddata1.enter()
         //adding the grouping here "hides" the rect and text
        .append('g')
        .attr('class', 'legendelement')
        .attr('id', function (d, i) { return id + 'legendelement' + i.toString() })
        .attr('transform', function (d, i) {
            return "translate(" + width + "," + 0 + ")";
        });

    //this.legendenterg = this.legendenter
    //    // adding the grouping here adds ungroups the rect and text from each legend element
    //    .append('g')
    //    .attr('class', 'legendelement')
    //    .attr('id', function (d, i) { return id + 'legendelement' + i.toString() })
    //    .attr('transform', function (d, i) {
    //        return "translate(" + width + "," + 0 + ")";
    //    });

    //set the legend transition
    this.legenddata1.transition()
        .attr('transform', function (d, i) {
            return "translate(" + (width + 10) + "," + 0 + ")";
        });

    //add filled rectangles
    this.legenddata1enter.append('rect')
        .attr('x', 0)
        .attr('width', 10)
        .attr('y', function (d, i) { return i * 20; })
        .attr('height', 10);

    this.legenddata1.select('rect')
        .transition()
        .attr('y', function (d, i) { return i * 20; })
        .style('fill', function (d) {
            return colorscale(d.key);
        });

    //annotate with text

    this.legenddata1enter.append('text')
        .attr('x', 12)
        .attr('y', function (d, i) {
            return i * 20 + 9;
        });
    this.legenddata1.select('text')
        .transition()
        .attr('x', 12)
        .attr('y', function (d, i) {
            return i * 20 + 9;
        })
        .text(function (d) {
            return d.key;
        });

    this.legenddata1.exit()
      .transition()
        .attr('transform', function (d, i) {
            return "translate(" + width + "," + 0 + ")";
        })
        .remove();
};
d3_chart2d.prototype.render = function () {
    //render the chart

    //your code here...
};
d3_chart2d.prototype.set_linedata1 = function (interoplate_I) {
    // set the line generator properties
    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;

    this.linedata1generator = d3.svg.line()
        .interpolate(interoplate_I)
        .x(function (d) { return x1scale(d[x_data]); })
        .y(function (d) { return y1scale(d[y_data]); });
};
d3_chart2d.prototype.set_linedata2 = function (interoplate_I) {
    var x_data = this.data2xdata;
    var y_data = this.data21ydata;
    var x2scale = this.x2scale;
    var y2scale = this.y2scale;

    this.linedata2generator = d3.svg.line()
        .interpolate(interoplate_I)
        .x(function (d) { return x2scale(d[x_data]); })
        .y(function (d) { return y2scale(d[y_data]); });
};
d3_chart2d.prototype.add_linedata1 = function () {
    //add lines to chart
    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var series_label = this.data1serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;
    var linedata1generator = this.linedata1generator;

    this.linedata1 = this.svgg.selectAll(".line")
        .data(this.data1.nestdatafiltered);

    this.linedata1enter = this.linedata1.enter()
        .append("g")
        .attr("class", "line");

    this.linedata1enter.append('path')
        .attr('class', 'lineseries')
        .attr('id', function (d,i) {
            return id+'lineseries'+i.toString();})
        .style("stroke", function (d) {
            return colorscale(d.key);
        });

    this.linedata1.select("path.lineseries")
        .style("stroke", function (d) {
            return colorscale(d.key);
        })
        .transition()
        .attr("d", function (d) {
            return linedata1generator(d.values);
        });

    this.linedata1enter.append('text')
        .attr("x", 3)
        .attr("dy", ".35em");

    this.linedata1.select("text")
        .datum(function (d) {
            return {values: d.values[d.values.length - 1]};
        })
        .attr("transform", function (d) {
            return "translate(" + x1scale(d.values[x_data]) + "," + y1scale(d.values[y_data]) + ")";
        })
        .text(function (d) {return d.key;});

    this.linedata1.exit()
      .remove();
};
d3_chart2d.prototype.add_linedata1tooltipandstroke = function () {
    // add tooltip and change in stroke color on mouseover
    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var series_label = this.data1serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;

    this.linedata1enter.on('mouseover', function (d, i) {
        d3.select(this)
            .style("stroke", 'black');
        d3.select("#" + id + "tooltip")
            .style("left", (d3.event.pageX + 10) + "px")
            .style("top", (d3.event.pageY - 10) + "px")
            .select("#value")
            .text("series_label" + ": " + d.key);
        //Show the tooltip
        d3.select("#" + id + "tooltip").classed("hidden", false);
    })
        .on("mouseout", function (d) {
            d3.select(this).style("stroke", color(d.key));
            d3.select("#"+id+"tooltip").classed("hidden", true);
        });
};
d3_chart2d.prototype.add_linedata1onstroke = function () {
    // add change in stroke color on mouseover
    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var series_label = this.data1serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;

    this.linedata1enter.on('mouseover', function (d, i) {
        d3.select(this).style("stroke", 'black');
        })
        .on("mouseout", function (d) {
            d3.select(this).style("stroke", color(d.key));
        });
};
d3_chart2d.prototype.add_linedata1tooltip = function () {
    // add tooltip on mouseover
    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var series_label = this.data1serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;

    this.linedata1enter.on('mouseover', function (d, i) {
        d3.select("#" + id + "tooltip")
            .style("left", (d3.event.pageX + 10) + "px")
            .style("top", (d3.event.pageY - 10) + "px")
            .select("#value")
            .text("series_label" + ": " + d.key);
        //Show the tooltip
        d3.select("#" + id + "tooltip").classed("hidden", false);
    })
        .on("mouseout", function (d) {
            d3.select("#" + id + "tooltip").classed("hidden", true);
        });
};
d3_chart2d.prototype.add_linedata1filter = function () {
    //filter data on click

    var _this = this;
    
    this.linedata1enter.on("click", function (d, i) {
        var filters = [];
        _this.data1.filters[series_label].forEach(function (n) { if (n !== d.key) { filters.push(n); }; });
        _this.data1.filters[series_label] = filters;
        _this.data1.filter_stringdata();
        _this.render();
    });
};
d3_chart2d.prototype.add_linedata2 = function () {
    //add lines to chart
    var x_data = this.data2xdata;
    var y_data = this.data2ydata;
    var series_label = this.data2serieslabel;
    var x2scale = this.x2scale;
    var y2scale = this.y2scale;
    var colorscale = this.colorscale;
    var id = this.id;
    var linedata2generator = this.linedata2generator;

    this.linedata2 = this.svgg.selectAll(".line")
        .data(this.data2.nestdatafiltered);

    this.linedata2enter = this.linedata2.enter()
        .append("g")
        .attr("class", "line");

    this.linedata2enter.append('path')
        .attr('class', 'lineseries')
        .attr('id', function (d, i) {
            return id + 'lineseries' + i.toString();
        })
        .style("stroke", function (d) {
            return colorscale(d.key);
        });

    this.linedata2.select("path.lineseries")
        .style("stroke", function (d) {
            return colorscale(d.key);
        })
        .transition()
        .attr("d", function (d) {
            return linedata2generator(d.values);
        });

    this.linedata2enter.append('text')
        .attr("x", 3)
        .attr("dy", ".35em");

    this.linedata2.select("text")
        .datum(function (d) {
            return { values: d.values[d.values.length - 1] };
        })
        .attr("transform", function (d) {
            return "translate(" + x2scale(d.values[x_data]) + "," + y2scale(d.values[y_data]) + ")";
        })
        .text(function (d) { return d.key; });

    this.linedata2.exit().remove();
};
d3_chart2d.prototype.add_linedata2tooltipandstroke = function () {
    // add tooltip and change in stroke color on mouseover
    var x_data = this.data2xdata;
    var y_data = this.data2ydata;
    var series_label = this.data2serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;

    this.linedata2enter.on('mouseover', function (d, i) {
        d3.select(this)
            .style("stroke", 'black');
        d3.select("#" + id + "tooltip")
            .style("left", (d3.event.pageX + 10) + "px")
            .style("top", (d3.event.pageY - 10) + "px")
            .select("#value")
            .text("series_label" + ": " + d.key);
        //Show the tooltip
        d3.select("#" + id + "tooltip").classed("hidden", false);
    })
        .on("mouseout", function (d) {
            d3.select(this).style("stroke", color(d.key));
            d3.select("#" + id + "tooltip").classed("hidden", true);
        });
};
d3_chart2d.prototype.add_linedata2onstroke = function () {
    // add change in stroke color on mouseover
    var x_data = this.data2xdata;
    var y_data = this.data2ydata;
    var series_label = this.data2serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;

    this.linedata2enter.on('mouseover', function (d, i) {
        d3.select(this).style("stroke", 'black');
    })
        .on("mouseout", function (d) {
            d3.select(this).style("stroke", color(d.key));
        });
};
d3_chart2d.prototype.add_linedata2tooltip = function () {
    // add tooltip on mouseover
    var x_data = this.data2xdata;
    var y_data = this.data2ydata;
    var series_label = this.data2serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;

    this.linedata2enter.on('mouseover', function (d, i) {
        d3.select("#" + id + "tooltip")
            .style("left", (d3.event.pageX + 10) + "px")
            .style("top", (d3.event.pageY - 10) + "px")
            .select("#value")
            .text("series_label" + ": " + d.key);
        //Show the tooltip
        d3.select("#" + id + "tooltip").classed("hidden", false);
    })
        .on("mouseout", function (d) {
            d3.select("#" + id + "tooltip").classed("hidden", true);
        });
};
d3_chart2d.prototype.add_linedata2filter = function () {
    //filter data on click

    var _this = this;

    this.linedata2enter.on("click", function (d, i) {
        var filters = [];
        _this.data2.filters[series_label].forEach(function (n) { if (n !== d.key) { filters.push(n); }; });
        _this.data2.filters[series_label] = filters;
        _this.data2.filter_stringdata();
        _this.render();
    });
};
d3_chart2d.prototype.add_pointsdata1update = function(){
    //add call to update when user clicks on the point
    var feature_label = this.data1featurelabel;
    
    this.pointsdata1.on("click", function (d) {
        if (features_filter[d[feature_label]]) { features_filter[d[feature_label]] = false; }
        else { features_filter[d[feature_label]] = true; }
        redraw(features_filter);
    });
};
d3_chart2d.prototype.add_data1featureslabels = function () {
    //add a change in color upon moving the mouse over the point
    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var colorscale = this.colorscale;
    var features_label = this.data1serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var id = this.id;

    //points text labels
    this.data1featureslabelstext = this.svgg.selectAll(".featureslabels")
        .data(this.data1.listdatafiltered);

    this.data1featureslabelstext
        .transition()
        .attr("x", function (d) { return x1scale(d[x_data]) + 5; })
        .attr("y", function (d) { return y1scale(d[y_data]) - 5; })
        .text(function (d) { return d[features_label]; });

    this.data1featureslabelstextenter = this.data1featureslabelstext.enter()

    data1featureslabelstextenter.append("text")
        .attr("class", "featureslabels")
        .attr("id", function (d) { return id + "featureslabels"+ d[features_label]; })
        .attr("x", function (d) { return x1scale(d[x_data]) + 5; })
        .attr("y", function (d) { return y1scale(d[y_data]) - 5; })
        .text(function (d) { return d[features_label]; });

    this.data1featureslabelstext.exit().remove();
};
d3_chart2d.prototype.add_pointsdata1onfill = function () {
    //add a change in color upon moving the mouse over the point
    var colorscale = this.colorscale;
    var series_label = this.data1serieslabel;
    var id = this.id;

    //change color upon mouseover/mouseout
    this.pointsdata1enter.on("mouseover", function (d, i) {
        d3.select(this).style('fill', 'red');
    })
        .on("mouseout", function (d, i) {
            d3.select(this).style("fill", colorscale(d[series_label]));
        });
};
d3_chart2d.prototype.add_pointsdata1tooltip = function () {
    //add a tooltip upon moving the mouse over the point
    var colorscale = this.colorscale;
    var series_label = this.data1serieslabel;
    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var id = this.id;

    //show tooltip
    this.pointsdata1enter.on("mouseover", function (d) {
        //Update the tooltip position and value
        d3.select("#" + id + "tooltip")
            .style("left", (d3.event.pageX + 10) + "px")
            .style("top", (d3.event.pageY - 10) + "px")
            .select("#" + id + "value")
            .text('x: ' + d[x_data].toFixed(2) + '; y: ' + d[y_data].toFixed(2));
        //Show the tooltip
        d3.select("#" + id + "tooltip").classed("hidden", false);
    })
        .on("mouseout", function (d) {
            d3.select("#" + id + "tooltip").classed("hidden", true);
        });
};
d3_chart2d.prototype.add_pointsdata1tooltipandfill = function () {
    //add a tooltip upon moving the mouse over the point
    //add a change in color upon moving the mouse over the point
    //NOTE: both must be within the same "on" method
    var colorscale = this.colorscale;
    var series_label = this.data1serieslabel;
    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var id = this.id;

    //show tooltip
    this.pointsdata1enter.on("mouseover", function (d) {
        //Change fill color
        d3.select(this).style('fill', 'red');
        //Update the tooltip position and value
        d3.select("#" + id + "tooltip")
            .style("left", (d3.event.pageX + 10) + "px")
            .style("top", (d3.event.pageY - 10) + "px")
            .select("#" + id + "value")
            .text('x: ' + d[x_data].toFixed(2) + '; y: ' + d[y_data].toFixed(2));
        //Show the tooltip
        d3.select("#" + id + "tooltip").classed("hidden", false);
    })
        .on("mouseout", function (d) {
            d3.select(this).style("fill", colorscale(d[series_label]));
            d3.select("#" + id + "tooltip").classed("hidden", true);
        });
};
d3_chart2d.prototype.add_pointsdata1seriesfilter = function () {
    //filter series on click
    var series_label = this.data1serieslabel;
    var _this = this;
    this.pointsdata1enter.on('click', function (d, i) {
        var filters = [];
        _this.data1.filters[series_label].forEach(function (n) { if (n !== d[series_labell]) { filters.push(n); }; });
        _this.data1.filters[series_label] = filters;
        _this.data1.filter_stringdata();
        _this.render();
    });
};
d3_chart2d.prototype.add_pointsdata1featurefilter = function () {
    //filter feature on click
    var feature_label = this.data1featurelabel
    var _this = this;
    this.pointsdata1enter.on('click', function (d, i) {
        var filters = [];
        _this.data1.filters[feature_label].forEach(function (n) { if (n !== d[feature_label]) { filters.push(n); }; });
        _this.data1.filters[feature_label] = filters;
        _this.data1.filter_stringdata();
        _this.render();
    });
};
d3_chart2d.prototype.add_pointsdata1 = function () {
    //points properties
    var x_data = this.data1xdata;
    var y_data = this.data1ydata;
    var series_label = this.data1serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;

    //var pointsdata1g = this.svgg.append('g')
    //    .attr("class", "points")
    //    .attr("id", this.id + "points");

    //this.pointsdata1 = pointsdata1g.selectAll("circle")
    //    .data(this.data1.listdatafiltered);

    this.pointsdata1 = this.svgg.selectAll(".points")
        .data(this.data1.listdatafiltered);

    this.pointsdata1.exit().remove();

    this.pointsdata1.transition()
        .attr("cx", function (d) { return x1scale(d[x_data]); })
        .attr("cy", function (d) { return y1scale(d[y_data]); })
        .style("fill", function (d) { return colorscale(d[series_label]); });

    this.pointsdata1enter = this.pointsdata1.enter()
        .append("circle")
        .attr("class", "points")
        .attr("id", this.id + "points")
        .attr("r", 3.5)
        .attr("id", function (d, i) { return id + "point" + i.toString(); })
        .attr("cx", function (d) { return x1scale(d[x_data]); })
        .attr("cy", function (d) { return y1scale(d[y_data]); })
        .style("fill", function (d) { return colorscale(d[series_label]); });

    //this.pointsdata1enter = this.pointsdata1.enter();
    
    //this.pointsdata1enter.append("circle")
    //    .attr("r", 3.5)
    //    .attr("id", function (d, i) { return id + "point" + i.toString(); })
    //    .attr("cx", function (d) { return x1scale(d[x_data]); })
    //    .attr("cy", function (d) { return y1scale(d[y_data]); })
    //    .style("fill", function (d) { return colorscale(d[series_label]); });
};
d3_chart2d.prototype.add_pointsdata2 = function () {
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
d3_chart2d.prototype.set_svggcss = function (selectionstyle_I) {
    //set custom css style to svgg
    //Input:
    // selectionstyle_I = [{selection: string e.g., '.axis line, .axis path'
    //                      style: key:value strings e.g., {'fill': 'none', 'stroke': '#000',
    //                                                      'shape-rendering': 'crispEdges'}}]
    for (i = 0; i < selectionstyle_I.length; i++) {
        this.svgg.selectAll(selectionstyle_I[i].selection)
            .style(selectionstyle_I[i].style);
    };
};
d3_chart2d.prototype.set_d3css = function (selectionstyle_I) {
    //set custom css style to d3
    //Input:
    // selectionstyle_I = [{selection: string e.g., '.axis line, .axis path'
    //                      style: key:value strings e.g., {'fill': 'none', 'stroke': '#000',
    //                                                      'shape-rendering': 'crispEdges'}}]
    for (i = 0; i < selectionstyle_I.length; i++) {
        d3.selectAll(selectionstyle_I[i].selection)
            .style(selectionstyle_I[i].style);
    };
};
d3_chart2d.prototype.set_x1andy1axessstyle = function () {
    // predefined css style for x1 and y1 axis
    var x1axisselector = '#' + this.id + 'x1axis' + ' path';
    var y1axisselector = '#' + this.id + 'y1axis' + ' path';
    var style = {
        'fill': 'none', 'stroke': '#000',
        'shape-rendering': 'crispEdges',
        'stroke-width': '1.5px'
    };
    var selectorstyle = [{ 'selection': x1axisselector, 'style': style },
                     { 'selection': y1axisselector, 'style': style }]
    this.set_svggcss(selectorstyle);
};
d3_chart2d.prototype.set_pointsstyle = function () {
    // predefined css style for points
    var pointsselector = '#' + this.id + 'points';
    var pointsstyle = {
        'stroke': 'none'
    };
    var selectorstyle = [{ 'selection': pointsselector, 'style': pointsstyle }]
    this.set_svggcss(selectorstyle);
};
d3_chart2d.prototype.set_data1ids = function (data1xdata_I, data1ydata_I, data1serieslabel_I, data1featurelabel_I) {
    //set the data1 column identifiers for x, y, series_label, and feature_label
    this.data1xdata = data1xdata_I;
    this.data1ydata = data1ydata_I;
    this.data1serieslabel = data1serieslabel_I;
    this.data1featurelabel = data1featurelabel_I;
};
d3_chart2d.prototype.set_data2ids = function (data2xdata_I, data2ydata_I, data2serieslabel_I, data2featurelabel_I) {
    //set the data2 column identifiers for x, y, series_label, and feature_label
    this.data2xdata = data2xdata_I;
    this.data2ydata = data2ydata_I;
    this.data2serieslabel = data2serieslabel_I;
    this.data2featureslabel = data2featurelabel_I;
};
var d3_data = function () {
    //data function
    this.keys = []; // list of columns that can be applied as nest keys and filters
    this.nestkey = ''; // key to apply to nest
    this.filters = {}; // {key1:[string1,string2,...],...}
    this.listdata = []; // data in database table form (must contain a column "_used");
    this.listdatafiltered = []; // data in database table form
    this.nestdatafiltered = []; // data in nested form
};
d3_data.prototype.convert_list2nestlist = function (data_I,key_I) {
    // convert a list of objects to a d3 nest by a key
    var nesteddata_O = d3.nest()
        .key(function (d) { return d[key_I]; })
        //.rollup()
        .entries(data_I);
    return nesteddata_O;
};
d3_data.prototype.convert_list2nestmap = function (data_I,key_I) {
    // convert a list of objects to a d3 nest by a key
    var nesteddata_O = d3.nest()
        .key(function (d) { return d[key_I]; })
        //.rollup()
        .map(data_I);
    return nesteddata_O;
};
d3_data.prototype.filter_stringdata = function () {
    // apply filters to listdata

    var listdatacopy = this.listdata;
    var listdatafiltered_O = [];
    
    //set _used to false:
    for (i = 0; i < listdatacopy.length; i++) {
        listdatacopy[i]['_used'] = true;
    };

    //pass each row through the filter
    for (i = 0; i < listdatacopy.length; i++) {
        for (filter in this.filters) {
            if (!listdatacopy[i][filter].match(this.filters[filter].join('|'))) {
                listdatacopy[i]['_used'] = false;
            };
        };
    };

    // add in the filtered data
    listdatacopy.forEach(function (d) {
        if (d['_used']) {
            listdatafiltered_O.push(d)
        };
    });

    // re-make the nestdatafiltered
    this.listdatafiltered = listdatafiltered_O;
    this.nestdatafiltered = this.convert_list2nestlist(listdatafiltered_O,this.nestkey);
};
d3_data.prototype.set_listdata = function (listdata_I,nestkey_I) {
    // set list data and initialize filtered data
    this.nestkey = nestkey_I;
    this.listdata = listdata_I;
    this.listdatafiltered = listdata_I;
    this.nestdatafiltered = this.convert_list2nestlist(listdata_I,this.nestkey);
};
d3_data.prototype.set_keys = function (keys_I) {
    // add list data
    this.keys = keys_I;
};
d3_data.prototype.reset_filters = function () {
    // generate the initial filter

    var filters = {};
    for (key_cnt = 0; key_cnt < this.keys.length;key_cnt++) {
        var colentries = d3.set();
        for (i = 0; i < this.listdata.length; i++) {
            colentries.add(this.listdata[i][this.keys[key_cnt]]);
        };
        filters[this.keys[key_cnt]] = colentries.values();
    };
    this.filters = filters;
};
d3_data.prototype.clear_data = function () {
    // add list data
    this.listdata = [];
    this.listdatafiltered = [];
    this.nestdatafiltered = [];
};
d3_data.prototype.change_filters = function (filter_I) {
    // modify the filter according to the new filter
    
    var filters_O = this.filters;
    for (key in filter_I) {
        filters_O[key] = filter_I[key];
    };
    this.filters = filters_O;
};