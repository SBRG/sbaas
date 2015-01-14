create_d3js_drawing = function (data_I_filename) {
    var diameter = 960;
    //var diameter = 480;

    var tree = d3.layout.tree()
        .size([360, diameter / 3 - 120])
        .separation(function (a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

    var diagonal = d3.svg.diagonal.radial()
        .projection(function (d) { return [d.y, d.x / 180 * Math.PI]; });

    //var svg = d3.select("body").append("svg")
    var svg = d3.select("#ex1").append("svg")
        .attr("width", diameter)
        //.attr("height", diameter - 150)
        .attr("height", diameter)
      .append("g")
        .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

    d3.json(data_I_filename, function (error, root) {
        var nodes = tree.nodes(root),
            links = tree.links(nodes);

        var link = svg.selectAll(".link")
            .data(links)
          .enter().append("path")
            .attr("class", "link")
            .attr("d", diagonal);

        var node = svg.selectAll(".node")
            .data(nodes)
          .enter().append("g")
            .attr("class", "node")
            .attr("transform", function (d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

        node.append("circle")
            .attr("r", 4.5);

        node.append("text")
            .attr("dy", ".31em")
            .attr("text-anchor", function (d) { return d.x < 180 ? "start" : "end"; })
            .attr("transform", function (d) { return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)"; })
            .text(function (d) { return d.name; });
    });

    d3.select(self.frameElement).style("height", diameter - 150 + "px");
};