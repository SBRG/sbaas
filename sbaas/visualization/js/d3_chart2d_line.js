"use strict";
d3_chart2d.prototype.set_linedata1 = function (interoplate_I) {
    // set the line generator properties
    var x_data = this.data1keymap.xdata;
    var y_data = this.data1keymap.ydata;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;

    this.linedata1generator = d3.svg.line()
        .interpolate(interoplate_I)
        .x(function (d) { return x1scale(d[x_data]); })
        .y(function (d) { return y1scale(d[y_data]); });
};
d3_chart2d.prototype.set_linedata2 = function (interoplate_I) {
    var x_data = this.data2keymap.xdata;
    var y_data = this.data2keymap.ydata;
    var x2scale = this.x2scale;
    var y2scale = this.y2scale;

    this.linedata2generator = d3.svg.line()
        .interpolate(interoplate_I)
        .x(function (d) { return x2scale(d[x_data]); })
        .y(function (d) { return y2scale(d[y_data]); });
};
d3_chart2d.prototype.add_linedata1 = function () {
    //add lines to chart
    var x_data = this.data1keymap.xdata;
    var y_data = this.data1keymap.ydata;
    var series_label = this.data1keymap.serieslabel;
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
        .attr('class', id+'lineseries')
        .attr('id', function (d,i) {
            return id+'lineseries'+i.toString();})
        .style("stroke", function (d) {
            return colorscale(d.key);
        });

    this.linedata1.select("path."+id+'lineseries')
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
    var x_data = this.data1keymap.xdata;
    var y_data = this.data1keymap.ydata;
    var series_label = this.data1keymap.serieslabel;
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
            d3.select(this).style("stroke", colorscale(d.key));
            d3.select("#"+id+"tooltip").classed("hidden", true);
        });
};
d3_chart2d.prototype.add_linedata1onstroke = function () {
    // add change in stroke color on mouseover
    var x_data = this.data1keymap.xdata;
    var y_data = this.data1keymap.ydata;
    var series_label = this.data1keymap.serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;

    this.linedata1enter.on('mouseover', function (d, i) {
        d3.select(this).style("stroke", 'black');
        })
        .on("mouseout", function (d) {
            d3.select(this).style("stroke", colorscale(d.key));
        });
};
d3_chart2d.prototype.add_linedata1tooltip = function () {
    // add tooltip on mouseover
    var x_data = this.data1keymap.xdata;
    var y_data = this.data1keymap.ydata;
    var series_label = this.data1keymap.serieslabel;
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
        if (_this.filterdata1and2){
            _this.data2.filters[series_label] = filters;
            _this.data2.filter_stringdata();
        };
        _this.render();
    });
};
d3_chart2d.prototype.add_linedata2 = function () {
    //add lines to chart
    var x_data = this.data2keymap.xdata;
    var y_data = this.data2keymap.ydata;
    var series_label = this.data2keymap.serieslabel;
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
        .attr('class', id+'lineseries')
        .attr('id', function (d, i) {
            return id + 'lineseries' + i.toString();
        })
        .style("stroke", function (d) {
            return colorscale(d.key);
        });

    this.linedata2.select("path."+id+'lineseries')
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
    var x_data = this.data2keymap.xdata;
    var y_data = this.data2keymap.ydata;
    var series_label = this.data2keymap.serieslabel;
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
            .select("#" + id + "value")
            .text("series_label" + ": " + d.key);
        //Show the tooltip
        d3.select("#" + id + "tooltip").classed("hidden", false);
    })
        .on("mouseout", function (d) {
            d3.select(this).style("stroke", colorscale(d.key));
            d3.select("#" + id + "tooltip").classed("hidden", true);
        });
};
d3_chart2d.prototype.add_linedata2onstroke = function () {
    // add change in stroke color on mouseover
    var x_data = this.data2keymap.xdata;
    var y_data = this.data2keymap.ydata;
    var series_label = this.data2keymap.serieslabel;
    var x1scale = this.x1scale;
    var y1scale = this.y1scale;
    var colorscale = this.colorscale;
    var id = this.id;

    this.linedata2enter.on('mouseover', function (d, i) {
        d3.select(this).style("stroke", 'black');
    })
        .on("mouseout", function (d) {
            d3.select(this).style("stroke", colorscale(d.key));
        });
};
d3_chart2d.prototype.add_linedata2tooltip = function () {
    // add tooltip on mouseover
    var x_data = this.data2keymap.xdata;
    var y_data = this.data2keymap.ydata;
    var series_label = this.data2keymap.serieslabel;
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
    var series_label = this.data2keymap.serieslabel;
    var _this = this;

    this.linedata2enter.on("click", function (d, i) {
        var filters = [];
        _this.data2.filters[series_label].forEach(function (n) { if (n !== d.key) { filters.push(n); }; });
        _this.data2.filters[series_label] = filters;
        _this.data2.filter_stringdata();
        if (_this.filterdata1and2){
            _this.data1.filters[series_label] = filters;
            _this.data1.filter_stringdata();
        }
        _this.render();
    });
};
d3_chart2d.prototype.set_linestyle = function () {
    // predefined css style for x1 and y1 axis
    var lineselector = 'path.'+ this.id + 'lineseries';
    var style = {
        'fill': 'none',
        'shape-rendering': 'crispEdges',
        'stroke-width': '1.5px'
    };
    var selectorstyle = [{ 'selection': lineselector, 'style': style }]
    this.set_svggcss(selectorstyle);
};