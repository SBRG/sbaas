boxandwhiskers_d3 = function (data_I, chart_I) {

    var margin = { top: 50, right: 75, bottom: 20, left: 75 },
        width = 170 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var min = Infinity,
        max = -Infinity;

    function redraw(data_I,chart_I) {
        //var data = data_I.data; //[[],[],[],[]...] an array for each sample data
        var labels = data_I.labels; //[sample_label1, sample_label2,...] an array of sample labels that matches the data array
        var options = data_I.options; //{x_axis_label: ,y_axis_label: }

        // initialize the boxandwhiskers plot
        var chart = d3.box()
            .whiskers(iqr(1.5))
            .width(width)
            .height(height)
            .labels(labels);

        var data = []; //[{'condition': ,'replicate':, 'value': }]

        data_I.data.forEach(function (x) {
            var e = Math.floor(x.condition),
                r = Math.floor(x.replicate),
                s = x.value,
                d = data[e];
            if (!d) d = data[e] = [s];
            else d.push(s);
            if (s > max) max = s;
            if (s < min) min = s;
        });

        chart.domain([min, max]);

        //var x = d3.scale.linear()
        //    .range([0, width]);

        //var y = d3.scale.linear()
        //    .range([height, 0]);

        //var xAxis = d3.svg.axis()
        //    .scale(x)
        //    .orient("bottom");

        //var yAxis = d3.svg.axis()
        //    .scale(y)
        //    .orient("left");

        var svgElem = d3.select("#" + chart_I).selectAll('svg')
                .data(data);

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

        //css styling
        svg.selectAll('.dot')
            .style({
                'stroke': '#000'
            });

        svg.selectAll('.line')
            .style({
                'fill': 'none', 'stroke': 'steelblue',
                'stroke-width': '1.5px'
            });

        //gEnter.append("clipPath")
        //  .attr("id", "clip")
        //.append("rect")
        //  .attr("class", "mesh")
        //  .attr("width", width)
        //  .attr("height", height);

        //gEnter.append("g")
        //    .attr("class", "x axis")
        //    .attr("transform", "translate(0," + height + ")")
        //    .append("text")
        //    .attr("class", "label")
        //    .attr("x", width / 2)
        //    .attr("y", 28)
        //    .style("text-anchor", "middle")
        //    .text(options.x_axis_label);

        //svg.select('g.x.axis').transition().call(xAxis);

        //gEnter.append("g")
        //    .attr("class", "y axis")
        //    .call(yAxis)
        //    .append("text")
        //    .attr("class", "label")
        //    .attr("transform", "rotate(-90)")
        //    .attr("y", -28)
        //    .attr("x", -height / 2)
        //    .style("text-anchor", "middle")
        //    .text(options.y_axis_label);

        //svg.select('g.y.axis').transition().call(yAxis);

        svg.call(chart);

        //setInterval(function () {
        //    svg.datum(randomize).call(chart.duration(1000));
        //}, 2000);
    };
    
    // Inspired by http://informationandvisualization.de/blog/box-plot

    d3.box = function() {
        var width = 1,
            height = 1,
            duration = 0,
            domain = null,
            value = Number,
            whiskers = boxWhiskers,
            quartiles = boxQuartiles,
            tickFormat = null,
            labels = [];

        // For each small multiple…
        function box(g) {
            g.each(function(d, i) {
                d = d.map(value).sort(d3.ascending);
                var g = d3.select(this),
                    n = d.length,
                    min = d[0],
                    max = d[n - 1];

                // Compute quartiles. Must return exactly 3 elements.
                var quartileData = d.quartiles = quartiles(d);

                // Compute whiskers. Must return exactly 2 elements, or null.
                var whiskerIndices = whiskers && whiskers.call(this, d, i),
                    whiskerData = whiskerIndices && whiskerIndices.map(function(i) { return d[i]; });

                // Compute outliers. If no whiskers are specified, all data are "outliers".
                // We compute the outliers as indices, so that we can join across transitions!
                var outlierIndices = whiskerIndices
                    ? d3.range(0, whiskerIndices[0]).concat(d3.range(whiskerIndices[1] + 1, n))
                    : d3.range(n);

                // Compute the new x-scale.
                var x1 = d3.scale.linear()
                    .domain(domain && domain.call(this, d, i) || [min, max])
                    .range([height, 0]);

                // Retrieve the old x-scale, if this is an update.
                var x0 = this.__chart__ || d3.scale.linear()
                    .domain([0, Infinity])
                    .range(x1.range());

                // Stash the new scale.
                this.__chart__ = x1;

                // Note: the box, median, and box tick elements are fixed in number,
                // so we only have to handle enter and update. In contrast, the outliers
                // and other elements are variable, so we need to exit them! Variable
                // elements also fade in and out.

                // Update center line: the vertical line spanning the whiskers.
                var center = g.selectAll("line.center")
                    .data(whiskerData ? [whiskerData] : []);

                center.enter().insert("line", "rect")
                    .attr("class", "center")
                    .attr("x1", width / 2)
                    .attr("y1", function(d) { return x0(d[0]); })
                    .attr("x2", width / 2)
                    .attr("y2", function(d) { return x0(d[1]); })
                    .style("opacity", 1e-6)
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px')
                    .attr("stroke-dasharray", '3,3')
                  .transition()
                    .duration(duration)
                    .style("opacity", 1)
                    .attr("y1", function(d) { return x1(d[0]); })
                    .attr("y2", function (d) { return x1(d[1]); })
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px')
                    .attr("stroke-dasharray", '3,3');

                center.transition()
                    .duration(duration)
                    .style("opacity", 1)
                    .attr("y1", function(d) { return x1(d[0]); })
                    .attr("y2", function(d) { return x1(d[1]); });

                center.exit().transition()
                    .duration(duration)
                    .style("opacity", 1e-6)
                    .attr("y1", function(d) { return x1(d[0]); })
                    .attr("y2", function(d) { return x1(d[1]); })
                    .remove();

                // Update innerquartile box.
                var box = g.selectAll("rect.box")
                    .data([quartileData]);

                box.enter().append("rect")
                    .attr("class", "box")
                    .attr("x", 0)
                    .attr("y", function(d) { return x0(d[2]); })
                    .attr("width", width)
                    .attr("height", function (d) { return x0(d[0]) - x0(d[2]); })
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px')
                  .transition()
                    .duration(duration)
                    .attr("y", function(d) { return x1(d[2]); })
                    .attr("height", function(d) { return x1(d[0]) - x1(d[2]); })
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px');

                box.transition()
                    .duration(duration)
                    .attr("y", function(d) { return x1(d[2]); })
                    .attr("height", function(d) { return x1(d[0]) - x1(d[2]); });

                // Update median line.
                var medianLine = g.selectAll("line.median")
                    .data([quartileData[1]]);

                medianLine.enter().append("line")
                    .attr("class", "median")
                    .attr("x1", 0)
                    .attr("y1", x0)
                    .attr("x2", width)
                    .attr("y2", x0)
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px')
                  .transition()
                    .duration(duration)
                    .attr("y1", x1)
                    .attr("y2", x1)
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px');

                medianLine.transition()
                    .duration(duration)
                    .attr("y1", x1)
                    .attr("y2", x1)
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px');

                // Update whiskers.
                var whisker = g.selectAll("line.whisker")
                    .data(whiskerData || []);

                whisker.enter().insert("line", "circle, text")
                    .attr("class", "whisker")
                    .attr("x1", 0)
                    .attr("y1", x0)
                    .attr("x2", width)
                    .attr("y2", x0)
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px')
                    .style("opacity", 1e-6)
                  .transition()
                    .duration(duration)
                    .attr("y1", x1)
                    .attr("y2", x1)
                    .style("opacity", 1)
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px');

                whisker.transition()
                    .duration(duration)
                    .attr("y1", x1)
                    .attr("y2", x1)
                    .style("opacity", 1)
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px');

                whisker.exit().transition()
                    .duration(duration)
                    .attr("y1", x1)
                    .attr("y2", x1)
                    .style("opacity", 1e-6)
                    .remove()
                    .attr("fill", '#fff')
                    .attr("stroke", '#000')
                    .attr("stroke-width", '1.5px');

                // Update outliers.
                var outlier = g.selectAll("circle.outlier")
                    .data(outlierIndices, Number);

                outlier.enter().insert("circle", "text")
                    .attr("class", "outlier")
                    .attr("r", 5)
                    .attr("cx", width / 2)
                    .attr("cy", function(i) { return x0(d[i]); })
                    .style("opacity", 1e-6)
                    .attr("fill", 'none')
                    .attr("stroke", '#ccc')
                  .transition()
                    .duration(duration)
                    .attr("cy", function(i) { return x1(d[i]); })
                    .style("opacity", 1)
                    .attr("fill", 'none')
                    .attr("stroke", '#ccc');

                outlier.transition()
                    .duration(duration)
                    .attr("cy", function(i) { return x1(d[i]); })
                    .style("opacity", 1)
                    .attr("fill", 'none')
                    .attr("stroke", '#ccc');

                outlier.exit().transition()
                    .duration(duration)
                    .attr("cy", function(i) { return x1(d[i]); })
                    .style("opacity", 1e-6)
                    .attr("fill", 'none')
                    .attr("stroke", '#ccc')
                    .remove();

                // Compute the tick format.
                var format = tickFormat || x1.tickFormat(8);

                // Update box ticks.
                var boxTick = g.selectAll("text.box")
                    .data(quartileData);

                boxTick.enter().append("text")
                    .attr("class", "box")
                    .attr("dy", ".3em")
                    .attr("dx", function(d, i) { return i & 1 ? 6 : -6 })
                    .attr("x", function(d, i) { return i & 1 ? width : 0 })
                    .attr("y", x0)
                    .attr("text-anchor", function(d, i) { return i & 1 ? "start" : "end"; })
                    .text(format)
                  .transition()
                    .duration(duration)
                    .attr("y", x1);

                boxTick.transition()
                    .duration(duration)
                    .text(format)
                    .attr("y", x1);

                // Update whisker ticks. These are handled separately from the box
                // ticks because they may or may not exist, and we want don't want
                // to join box ticks pre-transition with whisker ticks post-.
                var whiskerTick = g.selectAll("text.whisker")
                    .data(whiskerData || []);

                whiskerTick.enter().append("text")
                    .attr("class", "whisker")
                    .attr("dy", ".3em")
                    .attr("dx", 6)
                    .attr("x", width)
                    .attr("y", x0)
                    .text(format)
                    .style("opacity", 1e-6)
                  .transition()
                    .duration(duration)
                    .attr("y", x1)
                    .style("opacity", 1);

                whiskerTick.transition()
                    .duration(duration)
                    .text(format)
                    .attr("y", x1)
                    .style("opacity", 1);

                whiskerTick.exit().transition()
                    .duration(duration)
                    .attr("y", x1)
                    .style("opacity", 1e-6)
                    .remove();

                // Labels
                var labelsText = g.selectAll("text.labels").data(labels);

                labelsText.enter().append("text")
                    .attr("class", "whisker")
                    .attr("dy", ".3em")
                    .attr("dx", -75)
                    .attr("x", width)
                    .attr("y", -25)
                    .text(labels[i])
                    .style("opacity", 1e-6)
                  .transition()
                    .duration(duration)
                    .attr("y", -25)
                    .style("opacity", 1);

                labelsText.transition()
                    .duration(duration)
                    .text(labels[i])
                    .attr("y", -25)
                    .style("opacity", 1);

                labelsText.exit().transition()
                    .duration(duration)
                    .attr("y", -25)
                    .style("opacity", 1e-6)
                    .remove();

            });
            d3.timer.flush();
        }

        box.width = function(x) {
            if (!arguments.length) return width;
            width = x;
            return box;
        };

        box.height = function(x) {
            if (!arguments.length) return height;
            height = x;
            return box;
        };

        box.tickFormat = function(x) {
            if (!arguments.length) return tickFormat;
            tickFormat = x;
            return box;
        };

        box.duration = function(x) {
            if (!arguments.length) return duration;
            duration = x;
            return box;
        };

        box.domain = function(x) {
            if (!arguments.length) return domain;
            domain = x == null ? x : d3.functor(x);
            return box;
        };

        box.value = function(x) {
            if (!arguments.length) return value;
            value = x;
            return box;
        };

        box.whiskers = function(x) {
            if (!arguments.length) return whiskers;
            whiskers = x;
            return box;
        };

        box.quartiles = function(x) {
            if (!arguments.length) return quartiles;
            quartiles = x;
            return box;
        };

        box.labels = function (x) {
            if (!arguments.length) return labels;
            labels = x;
            return box;
        };

        return box;
    };
    //draw the chart
    redraw(data_I, chart_I);

    function boxWhiskers(d) {
        return [0, d.length - 1];
    }

    function boxQuartiles(d) {
        return [
          d3.quantile(d, .25),
          d3.quantile(d, .5),
          d3.quantile(d, .75)
        ];
    }

    function randomize(d) {
        if (!d.randomizer) d.randomizer = randomizer(d);
        return d.map(d.randomizer);
    }

    function randomizer(d) {
        var k = d3.max(d) * .02;
        return function (d) {
            return Math.max(min, Math.min(max, d + k * (Math.random() - .5)));
        };
    }

    // Returns a function to compute the interquartile range.
    function iqr(k) {
        return function (d, i) {
            var q1 = d.quartiles[0],
                q3 = d.quartiles[2],
                iqr = (q3 - q1) * k,
                i = -1,
                j = d.length;
            while (d[++i] < q1 - iqr);
            while (d[--j] > q3 + iqr);
            return [i, j];
        };
    }
};