heatmap_d3=function(data_I,chart_I){
    var margin = { top: 200, right: 10, bottom: 150, left: 400 },
    //var margin = { top: 175, right: 10, bottom: 150, left: 400 },
    //var margin = { top: 400, right: 10, bottom: 150, left: 175},
    cellSize=18,
        // - margin.top - margin.bottom,
        //gridSize = Math.floor(width / 24),
    legendElementWidth = cellSize*1.5,
    //colorBuckets = 21; //use for expression data (domain -10.0-10.0)
    colorBuckets = 10; //specific to resequencing data (domain 0.0-1.0)
    //colors = ['#005824','#1A693B','#347B53','#4F8D6B','#699F83','#83B09B','#9EC2B3','#B8D4CB','#D2E6E3','#EDF8FB','#FFFFFF','#F1EEF6','#E6D3E1','#DBB9CD','#D19EB9','#C684A4','#BB6990','#B14F7C','#A63467','#9B1A53','#91003F'];
    //var colors = ["#081d58", "#162876", "#253494", "#23499E", "#2253A3", "#225ea8", "#1F77B4", "#1d91c0", "#2FA3C2", "#38ACC3", "#41b6c4", "#60C1BF", "#7fcdbb", "#91D4B9", "#A3DBB7", "#c7e9b4", "#DAF0B2", "#E3F4B1", "#edf8b1", "#F6FBC5", "#ffffd9"];
    var colors = ["#081d58", "#253494", "#2253A3", "#1F77B4", "#2FA3C2", "#7fcdbb", "#A3DBB7", "#DAF0B2", "#edf8b1", "#ffffd9"]; //specific to resequencing data (domain 0.0-1.0)
    var rowLabel = data_I.row_labels;
    var colLabel = data_I.col_labels;
    var data = data_I.heatmap_data;
    var hcrow = data_I.hcrow;
    var hccol = data_I.hccol;
    var options = data_I.options;

    var col_number = colLabel.length,
        row_number = rowLabel.length;

    var width = cellSize*col_number, // - margin.left - margin.right,
        height = cellSize*row_number;

    //var maxval = JSON.parse(data_I.maxval);
    //var minval = JSON.parse(data_I.minval);
    var maxval = data_I.maxval;
    var minval = data_I.minval;

    //var colorScale = d3.scale.quantile()
    //                    .domain([ minval , 0, maxval])
    //                    .range(colors); // use for expression data
    var colorScale = d3.scale.quantile()
                        .domain([minval, 0.5, maxval])
                        .range(colors);
    d3.select("svg")
       .remove();

    //var svg = d3.select("#"+chart_I).append("svg")
    //    .attr("width", width + margin.left + margin.right)
    //    .attr("height", height + margin.top + margin.bottom)
    //    .append("g")
    //    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var svgElem = d3.select("#" + chart_I).selectAll('svg')
            .data([data]);

    var gEnter = svgElem.enter().append('svg')
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svgElem.attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    var svg = svgElem.select('g');

    //css styling
    svg.selectAll('rect.selection').style({
        'stroke': '#333',
        'stroke-dasharray': '4px',
        'stroke-opacity': '0.5',
        'fill': 'transparent'
    });

    svg.selectAll('rect.cell-border').style({
        'stroke': '#eee',
        'stroke-width': '0.3px'
    });

    svg.selectAll('rect.cell-selected').style({
        'stroke': 'rgb(51,102,153)',
        'stroke-width': '0.5px'
    });

    svg.selectAll('rect.cell-hover').style({
        'stroke': '#F00',
        'stroke-width': '0.3px'
    });

    svg.selectAll('text.mono').style({
        'font-size': '10pt',
        'font-family': 'Consolas, courier',
        'fill': '#aaa'
    });

    svg.selectAll('text.text-selected').style({ 'fill': '#000' });

    svg.selectAll('text.text-highlight,text.text-hover').style({ 'fill': '#c00' });

    var rowSortOrder=false;
    var colSortOrder=false;
    var rowLabels = svg.append("g")
            .selectAll(".rowLabelg")
            .data(rowLabel)
            .enter()
            .append("text")
            .text(function (d) { return d; })
            .attr("x", 0)
            .attr("y", function (d, i) { return hcrow.indexOf(i+1) * cellSize; })
            .style("text-anchor", "end")
            .attr("transform", "translate(-25," + cellSize / 1.5 + ")")
            .attr("class", function (d,i) { return "rowLabel mono r"+i;} )
            .on("mouseover", function(d) {d3.select(this).classed("text-hover",true);})
            .on("mouseout" , function(d) {d3.select(this).classed("text-hover",false);})
            .on("click", function(d,i) {rowSortOrder=!rowSortOrder; sortbylabel("r",i,rowSortOrder); this.$('#order').property("selectedIndex", 4).node().focus();;});

    var colLabels = svg.append("g")
            .selectAll(".colLabelg")
            .data(colLabel)
            .enter()
            .append("text")
            .text(function (d) { return d; })
            .attr("x", 0)
            .attr("y", function (d, i) { return hccol.indexOf(i+1) * cellSize; })
            .style("text-anchor", "left")
            .attr("transform", "translate("+cellSize/2 + ",-25) rotate (-90)")
            .attr("class",  function (d,i) { return "colLabel mono c"+i;} )
            .on("mouseover", function(d) {d3.select(this).classed("text-hover",true);})
            .on("mouseout" , function(d) {d3.select(this).classed("text-hover",false);})
            .on("click", function (d, i) { colSortOrder = !colSortOrder; sortbylabel("c", i, colSortOrder); this.$('#order').property("selectedIndex", 4).node().focus();; });

    var heatMap = svg.append("g").attr("class","g3")
        .selectAll(".cellg")
        .data(data,function(d){return d.row+":"+d.col;})
        .enter()
        .append("rect")
        .attr("x", function(d) { return hccol.indexOf(d.col) * cellSize; })
        .attr("y", function(d) { return hcrow.indexOf(d.row) * cellSize; })
        .attr("class", function(d){return "cell cell-border cr"+(d.row-1)+" cc"+(d.col-1);})
        .attr("width", cellSize)
        .attr("height", cellSize)
        .style("fill", function(d) { return colorScale(d.value); })
        /* .on("click", function(d) {
               var rowtext=d3.select(".r"+(d.row-1));
               if(rowtext.classed("text-selected")==false){
                   rowtext.classed("text-selected",true);
               }else{
                   rowtext.classed("text-selected",false);
               }
        })*/
        .on("mouseover", function(d){
               //highlight text
               d3.select(this).classed("cell-hover",true);
               d3.selectAll(".rowLabel").classed("text-highlight",function(r,ri){ return ri==(d.row-1);});
               d3.selectAll(".colLabel").classed("text-highlight",function(c,ci){ return ci==(d.col-1);});
            //Update the tooltip position and value
               //var coordinates = [0, 0];
               //coordinates = d3.mouse(this);
               //var x = coordinates[0];
               //var y = coordinates[1];
                d3.select("#tooltip")
                   //.style("left", (coordinates[0]+10) + "px")
                   //.style("top", (coordinates[1]-10) + "px")
                 .style("left", (d3.event.pageX+10) + "px")
                 .style("top", (d3.event.pageY-10) + "px")
                     .select("#value")
                     .text(options.row_axis_label + ": " + rowLabel[d.row - 1] + ",\n" + options.col_axis_label + ": " + colLabel[d.col - 1] + ",\n" + options.value_label + ": " + d.value);
                     //.text(rowLabel[d.row-1]+","+colLabel[d.col-1]+"\ndata:"+d.value);
            //Show the tooltip
               d3.select("#tooltip").classed("hidden", false);
        })
        .on("mouseout", function(){
               d3.select(this).classed("cell-hover",false);
               d3.selectAll(".rowLabel").classed("text-highlight",false);
               d3.selectAll(".colLabel").classed("text-highlight", false);
               d3.select("#tooltip").classed("hidden", true);
        })
    ;

    var legend = svg.selectAll(".legend")
      //.data(d3.range(Math.floor(minval), Math.ceil(maxval))) //use for expression data (domain -10.0-10.0)
      .data(d3.range(minval, maxval, (maxval - minval) / 10)) //specific to resequencing data (domain 0.0-1.0)
      .enter().append("g")
      .attr("class", "legend");

    //var color_factor = Math.ceil(colors.length / (maxval - minval));  //use for expression data (domain -10.0-10.0)
    var color_factor = 1.0; //specific to resequencing data (domain 0.0-1.0)
      console.log(height+(cellSize*2));
      legend.append("rect")
        .attr("x", function(d, i) { return legendElementWidth * i; })
        .attr("y", height+(cellSize*2))
        .attr("width", legendElementWidth)
        .attr("height", cellSize)
        .style("fill", function(d, i) { return colors[i*color_factor]; });

      legend.append("text")
        .attr("class", "mono")
        .text(function(d) { return d; })
        .attr("width", legendElementWidth)
        .attr("x", function(d, i) { return legendElementWidth * i; })
        .attr("y", height + (cellSize*4));

// Change ordering of cells

  function sortbylabel(rORc,i,sortOrder){
       var t = svg.transition().duration(3000);
       var log2r=[];
       var sorted; // sorted is zero-based index
       d3.selectAll(".c"+rORc+i)
         .filter(function(ce){
            log2r.push(ce.value);
          })
       ;
       if(rORc=="r"){ // sort log2ratio of a gene
         sorted=d3.range(col_number).sort(function(a,b){ if(sortOrder){ return log2r[b]-log2r[a];}else{ return log2r[a]-log2r[b];}});
         t.selectAll(".cell")
           .attr("x", function(d) { return sorted.indexOf(d.col-1) * cellSize; })
           ;
         t.selectAll(".colLabel")
          .attr("y", function (d, i) { return sorted.indexOf(i) * cellSize; })
         ;
       }else{ // sort log2ratio of a contrast
         sorted=d3.range(row_number).sort(function(a,b){if(sortOrder){ return log2r[b]-log2r[a];}else{ return log2r[a]-log2r[b];}});
         t.selectAll(".cell")
           .attr("y", function(d) { return sorted.indexOf(d.row-1) * cellSize; })
           ;
         t.selectAll(".rowLabel")
          .attr("y", function (d, i) { return sorted.indexOf(i) * cellSize; })
         ;
       }
  }

  //d3.select("#order").on("change",function(){
    this.$('#order').on("change",function(){
    order(this.value);
  });

  function order(value){
   if(value=="hclust"){
    var t = svg.transition().duration(3000);
    t.selectAll(".cell")
      .attr("x", function(d) { return hccol.indexOf(d.col) * cellSize; })
      .attr("y", function(d) { return hcrow.indexOf(d.row) * cellSize; })
      ;

    t.selectAll(".rowLabel")
      .attr("y", function (d, i) { return hcrow.indexOf(i+1) * cellSize; })
      ;

    t.selectAll(".colLabel")
      .attr("y", function (d, i) { return hccol.indexOf(i+1) * cellSize; })
      ;

   }else if (value=="probecontrast"){
    var t = svg.transition().duration(3000);
    t.selectAll(".cell")
      .attr("x", function(d) { return (d.col - 1) * cellSize; })
      .attr("y", function(d) { return (d.row - 1) * cellSize; })
      ;

    t.selectAll(".rowLabel")
      .attr("y", function (d, i) { return i * cellSize; })
      ;

    t.selectAll(".colLabel")
      .attr("y", function (d, i) { return i * cellSize; })
      ;

   }else if (value=="probe"){
    var t = svg.transition().duration(3000);
    t.selectAll(".cell")
      .attr("y", function(d) { return (d.row - 1) * cellSize; })
      ;

    t.selectAll(".rowLabel")
      .attr("y", function (d, i) { return i * cellSize; })
      ;
   }else if (value=="contrast"){
    var t = svg.transition().duration(3000);
    t.selectAll(".cell")
      .attr("x", function(d) { return (d.col - 1) * cellSize; })
      ;
    t.selectAll(".colLabel")
      .attr("y", function (d, i) { return i * cellSize; })
      ;
   }
  }
  //
  var sa=d3.select(".g3")
      .on("mousedown", function() {
          if( !d3.event.altKey) {
             d3.selectAll(".cell-selected").classed("cell-selected",false);
             d3.selectAll(".rowLabel").classed("text-selected",false);
             d3.selectAll(".colLabel").classed("text-selected",false);
          }
         var p = d3.mouse(this);
         sa.append("rect")
         .attr({
             rx      : 0,
             ry      : 0,
             class   : "selection",
             x       : p[0],
             y       : p[1],
             width   : 1,
             height  : 1
         })
      })
      .on("mousemove", function() {
         var s = sa.select("rect.selection");

         if(!s.empty()) {
             var p = d3.mouse(this),
                 d = {
                     x       : parseInt(s.attr("x"), 10),
                     y       : parseInt(s.attr("y"), 10),
                     width   : parseInt(s.attr("width"), 10),
                     height  : parseInt(s.attr("height"), 10)
                 },
                 move = {
                     x : p[0] - d.x,
                     y : p[1] - d.y
                 }
             ;

             if(move.x < 1 || (move.x*2<d.width)) {
                 d.x = p[0];
                 d.width -= move.x;
             } else {
                 d.width = move.x;
             }

             if(move.y < 1 || (move.y*2<d.height)) {
                 d.y = p[1];
                 d.height -= move.y;
             } else {
                 d.height = move.y;
             }
             s.attr(d);

                 // deselect all temporary selected state objects
             d3.selectAll('.cell-selection.cell-selected').classed("cell-selected", false);
             d3.selectAll(".text-selection.text-selected").classed("text-selected",false);

             d3.selectAll('.cell').filter(function(cell_d, i) {
                 if(
                     !d3.select(this).classed("cell-selected") &&
                         // inner circle inside selection frame
                     (this.x.baseVal.value)+cellSize >= d.x && (this.x.baseVal.value)<=d.x+d.width &&
                     (this.y.baseVal.value)+cellSize >= d.y && (this.y.baseVal.value)<=d.y+d.height
                 ) {

                     d3.select(this)
                     .classed("cell-selection", true)
                     .classed("cell-selected", true);

                     d3.select(".r"+(cell_d.row-1))
                     .classed("text-selection",true)
                     .classed("text-selected",true);

                     d3.select(".c"+(cell_d.col-1))
                     .classed("text-selection",true)
                     .classed("text-selected",true);
                 }
             });
         }
      })
      .on("mouseup", function() {
            // remove selection frame
         sa.selectAll("rect.selection").remove();

             // remove temporary selection marker class
         d3.selectAll('.cell-selection').classed("cell-selection", false);
         d3.selectAll(".text-selection").classed("text-selection",false);
      })
      .on("mouseout", function() {
         if(d3.event.relatedTarget.tagName=='html') {
                 // remove selection frame
             sa.selectAll("rect.selection").remove();
                 // remove temporary selection marker class
             d3.selectAll('.cell-selection').classed("cell-selection", false);
             d3.selectAll(".rowLabel").classed("text-selected",false);
             d3.selectAll(".colLabel").classed("text-selected",false);
         }
      });

}; 