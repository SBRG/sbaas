barchart_d3 = function (data_I, chart_id_I) {
    // clear any existing svg elements
    d3.select("svg")
       .remove();

    var margin = { top: 50, right: 150, bottom: 30, left: 40 },
    width = 990 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    var x0 = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var x1 = d3.scale.ordinal();

    var y = d3.scale.linear()
        .range([height, 0]);

    var data = data_I.data;
    var samplenames = data_I.samplenames;
    var options = null;

    var color = d3.scale.ordinal() //TODO improve contrast of color scheme and add additional colors
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    function redraw(data_I, samplenames_I, options) {

        var xAxis = d3.svg.axis()
            .scale(x0)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .tickFormat(d3.format(".2s"));

        var svg = d3.select("#" + chart_id_I).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .style({
                'font-size': '10px', 'font-family': 'sans-serif',
                'font-style': 'normal', 'font-variant': 'normal',
                'font-weight': 'normal'
            });

        x0.domain(data.map(function (d) { return d.label; }));
        x1.domain(samplenames).rangeRoundBands([0, x0.rangeBand()]);
        //y.domain([0, d3.max(data, function (d) { return d3.max(d.samples, function (d) { return d.value; }); })]);
        //Altered to allow for negative and positive values
        y.domain([d3.min(data, function (d) { return d3.min(d.samples, function (d) { return d.value; }); }),
            d3.max(data, function (d) { return d3.max(d.samples, function (d) { return d.value; }); })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Rate");

        //css styling
        svg.selectAll('.axis line, .axis path')
            .style({
                'fill': 'none', 'stroke': '#000',
                'shape-rendering': 'crispEdges'
            });

        svg.selectAll('.bar')
            .style({
                'fill': 'steelblue'
            });

        svg.selectAll('.x.axis path')
            .style({
                'display':'none'
            });

        var label = svg.selectAll(".label")
            .data(data)
            .enter().append("g")
            .attr("class", "g")
            .attr("transform", function (d) { return "translate(" + x0(d.label) + ",0)"; });

        label.selectAll("rect")
            .data(function (d) { return d.samples; })
            .enter().append("rect")
            .attr("width", x1.rangeBand())
            .attr("x", function (d) { return x1(d.name); })
            //.attr("y", function (d) { return y(d.value); }) //altered to display negative and positive bars
            .attr("y", function (d) { return y(Math.max(d.value, 0)); })
            //.attr("height", function (d) { return height - y(d.value); }) //altered to display negative and positive bars
            .attr("height", function (d) { return Math.abs(y(d.value) - y(0)); })
            .style("fill", function (d) { return color(d.name); })
            .on("mouseover", function (d) {
                //change color of the bar
                d3.select(this).style('fill', 'black');
                //Update the tooltip position and value
                d3.select("#tooltip")
                    .style("left", (d3.event.pageX + 10) + "px")
                    .style("top", (d3.event.pageY - 10) + "px")
                        .select("#value")
                        .text("Sample name: " + d.name + ', ' + "Met id: " + d.label + ', ' + "Value: " + d.value.toFixed(2) + ', ' + "95% CI: " + d.value_lb.toFixed(2) + "/" + d.value_ub.toFixed(2));
                //Show the tooltip
                d3.select("#tooltip").classed("hidden", false);
            })
            .on("mouseout", function (d) {
                d3.select(this).style("fill", color(d.name));
                d3.select("#tooltip").classed("hidden", true);
            });

        //Add error bars
        label.selectAll("polyline")
            .data(function (d) { return d.samples; })
            .enter().append("polyline")
            .attr("points", function (d) { //use upper and lower 95% confidence intervals for error bars
                return x1(d.name) + ',' + y(d.value_ub) + ' ' +
                    (x1(d.name) + x1.rangeBand()) + ',' + y(d.value_ub) + ' ' +
                    (x1(d.name) + x1.rangeBand() * 0.5) + ',' + y(d.value_ub) + ' ' +
                    (x1(d.name) + x1.rangeBand() * 0.5) + ',' + y(d.value_lb) + ' ' +
                    x1(d.name) + ',' + y(d.value_lb) + ' ' +
                    x1(d.name) + ',' + y(d.value_lb) + ' ' +
                    (x1(d.name) + x1.rangeBand()) + ',' + y(d.value_lb)
            })
            //.attr("points", function (d) { //use standard deviation for the error bars
            //    return x1(d.name) + ',' + y(d.value + Math.sqrt(d.value_var)) + ' ' +
            //        (x1(d.name) + x1.rangeBand()) + ',' + y(d.value + Math.sqrt(d.value_var)) + ' ' +
            //        (x1(d.name) + x1.rangeBand() * 0.5) + ',' + y(d.value + Math.sqrt(d.value_var)) + ' ' +
            //        (x1(d.name) + x1.rangeBand() * 0.5) + ',' + y(d.value - Math.sqrt(d.value_var)) + ' ' +
            //        x1(d.name) + ',' + y(d.value - Math.sqrt(d.value_var)) + ' ' +
            //        x1(d.name) + ',' + y(d.value - Math.sqrt(d.value_var)) + ' ' +
            //        (x1(d.name) + x1.rangeBand()) + ',' + y(d.value - Math.sqrt(d.value_var));
            //})
            .style("fill", "none")
            .style("stroke", "#000000")
            .style("stroke-width", function (d) { if (d.value == 0.0) { return 0; } else { return 1; } });

        var legend = svg.selectAll(".legend")
            .data(samplenames.slice().reverse())
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function (d, i) { return "translate(0," + i * 20 + ")"; });

        legend.append("rect")
            .attr("x", width - 18)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", color);

        legend.append("text")
            .attr("x", width + 4)
            .attr("y", 9)
            .attr("dy", ".35em")
            .style("text-anchor", "start")
            .text(function (d) { return d; });
    };
    redraw(data,samplenames,options)

}