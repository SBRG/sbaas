histogram_d3 = function (data_I, chart_I) {
    //TODO
    //Finish conversion from /Histogram_KernalDensity/index.html
    // histogram and kernal density plot

    // clear any existing svg elements
    d3.select("svg")
       .remove();

    var data = data_I.data; // data = [{x_data:float,samples:string},{},{},...]
    var data_fitted = data_I.data_fitted; // data_fitted = [{samples:string,x_data_fitted:float,y_data_fitted:float},{},{},...]
    var options = data_I.options; //options = {x_axis_I=[],y_axis_I=[],x_axis_label=None,y_axis_label=None,feature_name=None,
                //histogram-specific options: numHistBins_I=10, number of bins for the histogram
                                            //calcHistBinsAutomatically=true, calculate bins automatically? 
                                            //showKDP=true, bandwith (i.e., smoothing constant) h of the kernal density estimator
                                            //}

    // generate the initial filter object
    var features_unique = findUnique(data);
    var features_filter = {};
    for (var i = 0; i < features_unique.length; i++) {
        features_filter[features_unique[i]] = true;
    };

    var margin = { top: 20, right: 200, bottom: 30, left: 40 },
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.category20();

    function redraw(data_I, data_fitted_I, options, features_filter) {

        //filter data
        data = filterData(data_I, features_filter);
        data_fitted = filterData_fitted(data_fitted, features_filter)

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

        var xAxis2 = d3.svg.axis()
            .scale(x)
            .orient("top");

        var yAxis2 = d3.svg.axis()
            .scale(y)
            .orient("right");

        var svgElem = d3.select("#" + chart_I).selectAll('svg')
                .data([data]);

        var gEnter = svgElem.enter().append('svg')
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .style({
                'font-size': '10px', 'font-family': 'sans-serif',
                'font-style': 'normal', 'font-variant': 'normal',
                'font-weight': 'normal'
            });

        svgElem.attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom);

        var svg = svgElem.select('g');

        gEnter.append("clipPath")
          .attr("id", "clip")
        .append("rect")
          .attr("class", "mesh")
          .attr("width", width)
          .attr("height", height);

        gEnter.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .append("text")
            .attr("class", "label")
            .attr("x", width / 2)
            .attr("y", 28)
            .style("text-anchor", "middle")
            .text(options.x_axis_label);

        svg.select('g.x.axis').transition().call(xAxis);

        gEnter.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("class", "label")
            .attr("transform", "rotate(-90)")
            .attr("y", -28)
            .attr("x", -height / 2)
            .style("text-anchor", "middle")
            .text(options.y_axis_label);

        // reformat the fitted data to generate the line
        var samples_unique = findUnique(data_fitted);
        var samples_struct = [];
        for (var i = 0; i < samples_unique.length; i++) {
            samples_struct.push({ name: samples_unique[i], value: [] });
        };
        for (var i = 0; i < data_fitted.length; i++) {
            for (var j = 0; j < samples_struct.length; j++) {
                if (data_fitted[i].samples == samples_struct[j].name) {
                    samples_struct[j].value.push({ x_data_fitted: data_fitted[i].x_data_fitted, y_data_fitted: data_fitted[i].y_data_fitted });
                    break;
                }
            }
        }

        //line
        var interp = svg.selectAll(".interp")
            .data(samples_struct);

        var interpEnter = interp.enter()
            .append("g")
            .attr("class", "interp");

        interpEnter
            .append('path')
            .attr('class', 'line')
            .style("stroke", function (d) {
                return color(d.name);
            });

        interp.select("path.line")
            .style("stroke", function (d) {
                return color(d.name);
            })
            .transition()
            .attr("d", function (d) {
                return line(d.value);
            })

        interpEnter
            .on('mouseover', function (d, i) {
                d3.select(this)
                    .style("stroke", 'black');
                d3.select("#tooltip")
                    .style("left", (d3.event.pageX + 10) + "px")
                    .style("top", (d3.event.pageY - 10) + "px")
                    .select("#value")
                    .text(options.feature_name + ": " + d.name);
                //Show the tooltip
                d3.select("#tooltip").classed("hidden", false);
            })
            .on("mouseout", function (d) {
                d3.select(this).style("stroke", color(d.name));
                d3.select("#tooltip").classed("hidden", true);
            })
            .on("click", function (d) {
                if (features_filter[d.name]) { features_filter[d.name] = false; }
                else { features_filter[d.name] = true; }
                redraw(data, data_fitted, options, features_filter);
            });

        interpEnter.append('text')
            .attr("x", 3)
            .attr("dy", ".35em");

        interp.select("text")
            .datum(function (d) {
                return {
                    value: d.value[d.value.length - 1]
                };
            })
            .attr("transform", function (d) {
                return "translate(" + x(d.value.x_data_fitted) + "," + y(d.value.y_data_fitted) + ")";
            })
            .text(function (d) {
                return d.name;
            });

        interp.exit()
          .remove();

        //points
        var points = svg.selectAll(".dot")
            .data(data);

        var pointsEnter = points.enter().append("circle")
            .attr("class", "dot")

        points.transition()
            .attr("cx", function (d) { return x(d.x_data); })
            .attr("cy", function (d) { return y(d.y_data); })
            .style("fill", function (d) { return color(d.samples); });

        pointsEnter.attr("r", 3.5)
            .style("fill", function (d) { return color(d.samples); })
            .attr("cx", function (d) { return x(d.x_data); })
            .attr("cy", function (d) { return y(d.y_data); });

        pointsEnter.on("mouseover", function (d) {
                d3.select(this).style('fill', 'red');
                //Update the tooltip position and value
                d3.select("#tooltip")
                    .style("left", (d3.event.pageX + 10) + "px")
                    .style("top", (d3.event.pageY - 10) + "px")
                    .select("#value")
                    .text(options.feature_name + ": " + d.samples + ', ' + options.x_axis_label + ": " + d.x_data.toFixed(2) + ', ' + options.y_axis_label + ": " + d.y_data.toFixed(2));
                //Show the tooltip
                d3.select("#tooltip").classed("hidden", false);
            })
            .on("mouseout", function (d) {
                d3.select(this).style("fill", color(d.samples));
                d3.select("#tooltip").classed("hidden", true)
            });

        points.exit().remove();

        //line
        //var line = d3.svg.line()
        //    .interpolate(options.fit_function)
        //    .x(function (d) { return x(d.x_data_fitted); })
        //    .y(function (d) { return y(d.y_data_fitted); });

        //original
        var line = d3.svg.line()
            .x(function (d) { return x(d[0]); })
            .y(function (d) { return y(d[1]); });

        x.domain(d3.extent(data, function (d) { return d.x_data; })).nice();
        y.domain(d3.extent(data, function (d) { return d.y_data; })).nice();

        // histogram
        // calculate the number of histogram bins
        if (calcHistBinsAutomatic == true) {
            numHistBins = Math.ceil(Math.sqrt(data.length));  // global variable
        }
        // the histogram function
        histogram = d3.layout.histogram()
          .frequency(false)
          .bins(numHistBins);

        var histogram_data = histogram(data);
        var kde = kernelDensityEstimator(epanechnikovKernel(bandwith), x.ticks(100));

        svg.selectAll(".bar")
            .data(histogram_data)
          .enter().insert("rect", ".axis")
            .attr("class", "bar")
            .attr("x", function (d) { return x(d.x) + 1; })
            .attr("y", function (d) { return y(d.y); })
            .attr("width", x(data[0].dx + data[0].x) - x(data[0].x) - 1)
            .attr("height", function (d) { return height - y(d.y); });

        // kde
        // show the kernel density plot
        if (showKDP == true) {
            svg.append("path")
              .datum(kde(data))
              .attr("class", "line")
              .attr("d", line);
        }

        // legend
        var legend = svg.selectAll('g.legend')
            .data(samples_struct);

        var enterLegend = legend.enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', function (d, i) {
                return "translate(" + width + "," + 0 + ")";
            });

        legend
          .transition()
            .attr('transform', function (d, i) {
                return "translate(" + (width+10) + "," + 0 + ")";
            });

        enterLegend.append('rect')
            .attr('x', 0)
            .attr('width', 10)
            .attr('y', function (d, i) { return i * 20; })
            .attr('height', 10);

        legend.select('rect')
          .transition()
            .attr('y', function (d, i) { return i * 20; })
            .style('fill', function (d) {
                return color(d.name);
            });

        enterLegend.append('text')
              .attr('x', 12)
              .attr('y', function (d, i) {
                  return i * 20 + 9;
              });

        enterLegend.on("click", function (d) {
                if (features_filter[d.name]) { features_filter[d.name] = false; }
                else { features_filter[d.name] = true; }
                redraw(data, data_fitted, options, features_filter);
                });

        legend.select('text')
            .transition()
              .attr('x', 12)
              .attr('y', function (d, i) {
                  return i * 20 + 9;
              })
              .text(function (d) {
                  return d.name;
              });

        legend.exit()
          .transition()
            .attr('transform', function (d, i) {
                return "translate(" + width + "," + 0 + ")";
            })
            .remove();

        //css styling
        svg.selectAll('.axis line, .axis path')
            .style({
                'fill': 'none', 'stroke': '#000',
                'shape-rendering': 'crispEdges'
            });

        svg.selectAll('.dot')
            .style({
                'stroke': 'none'
            });

        svg.selectAll('.line')
            .style({
                'fill': 'none',
                'stroke-width': '1.5px'
            });

        svg.selectAll('.bar')
            .style({
                'fill': '#bbb',
                'shape-rendering': 'crispEdges'
            });
    };
    function findUnique(data_I) {
        var samples = [];
        for (var i = 0; i < data_I.length; i++) { samples[i] = data_I[i].samples };
        var samples_sorted = samples.sort();
        var samples_unique = [samples_sorted[0]];
        for (var i = 0; i < samples_sorted.length; i++) {
            var unique = true;
            for (var j = 0; j < samples_unique.length; j++) {
                if (samples_sorted[i] == samples_unique[j]) {
                    unique = false;
                };
            };
            if (unique) {
                samples_unique.push(samples_sorted[i]);
            };

        };
        return samples_unique;
    };
    function filterData(data,features_filter) {
        var data_filtered = [];
        for (i = 0; i < data.length; i++) {
            if (features_filter[data[i].samples]) {
                data_filtered.push({samples:data[i].samples,x_data:data[i].x_data,y_data:data[i].y_data})
            }
        }
        return data_filtered;
    };
    function filterData_fitted(data_fitted, features_filter) {
        var data_filtered_fitted = [];
        for (i = 0; i < data_fitted.length; i++) {
            if (features_filter[data_fitted[i].samples]) {
                data_filtered_fitted.push({ samples: data_fitted[i].samples, x_data_fitted: data_fitted[i].x_data_fitted, y_data_fitted: data_fitted[i].y_data_fitted })
            }
        }
        return data_filtered_fitted;
    }

    function kernelDensityEstimator(kernel, x) {
        return function (sample) {
            return x.map(function (x) {
                //console.log(x + " ... " + d3.mean(sample, function(v) { return kernel(x - v); }));		
                return [x, d3.mean(sample, function (v) { return kernel(x - v); })];
            });
        };
    }

    function epanechnikovKernel(bandwith) {
        return function (u) {
            //return Math.abs(u /= bandwith) <= 1 ? .75 * (1 - u * u) / bandwith : 0;
            if (Math.abs(u = u / bandwith) <= 1) {
                return 0.75 * (1 - u * u) / bandwith;
            } else return 0;
        };
    }
    redraw(data, data_fitted, options, features_filter);
};
