//TODO:
d3_chart2d.prototype.set_diameter = function(diameter_I){
    // set uniform width and height
    this.width = diameter_I;
    this.height= diameter_I;
};
d3_chart2d.prototype.set_packlayout = function(padding_I){
    //set pack layout
    var margin = this.margin;
    var width = this.width;
    var height = this.height;

    this.packlayout = d3.layout.pack()
        .padding(padding_I)
        .size([width - margin.left - margin.right, height - margin.top - margin.bottom])
        .value(function(d) { return d.size; })
};
d3_chart2d.prototype.set_packlayoutfocusdata1 = function(packlayoutfocus_I){
    //set pack layout focus
    if (packlayoutfocus_I){this.packlayoutfocus = packlayoutfocus_I;}
    else {this.packlayoutfocus=this.data1.nestdatafiltered[0]};    
};
d3_chart2d.prototype.set_packlayoutnodesdata1 = function(){
    //set pack layout nodes
    this.packlayoutnodes = this.packlayout.nodes(this.data1.nestdatafiltered[0]);
};
d3_chart2d.prototype.set_packlayoutviewdata1 = function(packlayoutview_I){
    //set pack layout view
    if (packlayoutview_I){this.packlayoutview = packlayoutview_I;}
    else {this.packlayoutview=null}; 
};
d3_chart2d.prototype.add_packlayoutcirclesdata1 = function(){
    // add circles to pack layout
    var focus = this.packlayoutfocus;
    var nodes = this.packlayoutnodes;
    var root = this.data1.nestdatafiltered[0];
    var colorscale = this.colorscale;
    var zoom_packlayout = this.zoom_packlayout;
    
    this.packlayoutcircle = this.svgg.selectAll("circle")
        .data(nodes);

//     this.packlayoutcircle.exit().remove();

//     this.packlayoutcircle.transition()
//         .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
//         .style("fill", function(d) { return d.children ? colorscale(d.depth) : null; })
//         .on("click", function(d) { if (focus !== d){ zoom_packlayout(d), d3.event.stopPropagation(); };});

    this.packlayoutcircleenter = this.packlayoutcircle.enter()
        .append("circle")
        .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
        .style("fill", function(d) { return d.children ? colorscale(d.depth) : null; })
        .on("click", function(d) { if (focus !== d){ zoom_packlayout(d), d3.event.stopPropagation(); };});

};
d3_chart2d.prototype.add_packlayouttextdata1 = function(){
    // add text to pack layout
    var focus = this.packlayoutfocus;
    var nodes = this.packlayoutnodes;
    var root = this.data1.nestdatafiltered[0];
    var colorscale = this.colorscale;
    var packlayoutzoom = this.packlayoutzoom;
    
    this.packlayouttext = this.svgg.selectAll("text")
        .data(nodes);

//     this.packlayouttext.exit().remove();

//     this.packlayouttext.transition()
//         .attr("class", "label")
//         .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
//         .style("display", function(d) { return d.parent === root ? null : "none"; })
//         .text(function(d) { return d.key; });

    this.packlayouttextenter = this.packlayouttext.enter()
        .append("text")
        .attr("class", "label")
        .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
        .style("display", function(d) { return d.parent === root ? null : "none"; })
        .text(function(d) { return d.key; });

};
d3_chart2d.prototype.set_packlayoutnode = function(d){
    // set the node selection for the packlayoutzoom
    this.node = this.svgg.selectAll("circle,text");
}
d3_chart2d.prototype.zoom_packlayout = function(d){
   // pack layout zoom function 
    this.set_packlayoutfocusdata1(d);
    var focus = this.packlayoutfocus;
    var view = this.packlayoutview;
    var margin = this.margin.top;
    var diameter = this.width;
    var packlayoutzoomto = this.zoomto_packlayout;

    var transition = d3.transition()
        .duration(d3.event.altKey ? 7500 : 750)
        .tween("zoom", function(d) {
          var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
          return function(t) { packlayoutzoomto(i(t),diameter); };
        });

    transition.selectAll("text")
      .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
        .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
        .each("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
        .each("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
};
d3_chart2d.prototype.zoomto_packlayout = function(view_I,diameter_I){
    // pack layout zoomto function
    // INPUT: 
    // view_I = [root.x, root.y, root.r * 2 + margin]
    if (view_I && diameter_I){
        var k = diameter_I / view_I[2]; 
        this.set_packlayoutviewdata1(view_I);
        var view = this.view;
    } else {
        var k = this.width / this.data1.nestdatafiltered[0].r + this.margin.top;
        var view = [this.data1.nestdatafiltered[0].x,this.data1.nestdatafiltered[0].y,this.data1.nestdatafiltered[0].r*2 + this.margin.top];
    };
    this.node.attr("transform", function(d) { return "translate(" + (d.x - view[0]) * k + "," + (d.y - view[1]) * k + ")"; });
    this.packlayoutcircle.attr("r", function(d) { return d.r * k; });
};
d3_chart2d.prototype.add_packlayoutdata1zoom = function(){
    // add zoom to svg element of the packlayoutzoom
    var packlayoutzoom = this.packlayoutzoom;
    var id = this.id
    var root = this.data1.nestdatafiltered[0];
    d3.select("#"+this.id).on("click",function() { packlayoutzoom(root); });
};
// TODO: css
// <style>

// .node {
//   cursor: pointer;
// }

// .node:hover {
//   stroke: #000;
//   stroke-width: 1.5px;
// }

// .node--leaf {
//   fill: white;
// }

// .label {
//   font: 11px "Helvetica Neue", Helvetica, Arial, sans-serif;
//   text-anchor: middle;
//   text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff, 0 -1px 0 #fff;
// }

// .label,
// .node--root,
// .node--leaf {
//   pointer-events: none;
// }

// </style>