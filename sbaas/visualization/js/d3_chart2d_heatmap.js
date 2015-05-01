"use strict";
d3_chart2d.prototype.set_heatmapdata1 = function (cellsize_I) {
    //add heatmap to the plot

    var listdatafiltered = this.data1.listdatafiltered;
    var columnslabel = this.data1keymap.columnslabel;
    var rowslabel = this.data1keymap.rowslabel;
    var zdata = this.data1keymap.zdata;
    var rowsleaves = this.data1keymap.rowsleaves;
    var columnsleaves = this.data1keymap.columnsleaves;
    var columnsindex = this.data1keymap.columnsindex;
    var rowsindex = this.data1keymap.rowsindex;
    
    //heatmap specific properties
    this.cellsize = cellsize_I;
    this.legendelementwidth = cellsize_I*1.5;

    this.uniquecollabels = this.get_uniquelabels(listdatafiltered,columnslabel);
    this.uniquerowlabels = this.get_uniquelabels(listdatafiltered,rowslabel);

    //reduce the data to index and corresponding leaves
    var collabelsset = d3.set();
    var rowlabelsset = d3.set();
    listdatafiltered.forEach(function(d){
        collabelsset.add(Math.round(d[columnsindex]));
        rowlabelsset.add(Math.round(d[rowsindex]));
        });
    var colindexmin = Math.round(d3.min(collabelsset.values()));
    var rowindexmin = Math.round(d3.min(rowlabelsset.values()));
    var colindexmax = collabelsset.values().length-1;
    var rowindexmax = rowlabelsset.values().length-1;
    var collabelsordered = [];
    var rowlabelsordered = [];
    for (var i=colindexmin;i<=colindexmax;i++){
        collabelsordered.push(i);
    };
    for (i=rowindexmin;i<=rowindexmax;i++){
        rowlabelsordered.push(i);
    };
    var columnleavesordered = [];
    var rowleavesordered = [];
    for (var i=0;i<collabelsordered.length;i++){
        for (var j=0;j<listdatafiltered.length;j++){
            if (collabelsordered[i]===listdatafiltered[j][columnsindex]){
                columnleavesordered.push(listdatafiltered[j][columnsleaves]);
                break;
            };
        };
    };
    for (var i=0;i<rowlabelsordered.length;i++){
        for (var j=0;j<listdatafiltered.length;j++){
            if (rowlabelsordered[i]===listdatafiltered[j][rowsindex]){
                rowleavesordered.push(listdatafiltered[j][rowsleaves]);
                break;
            };
        };
    };
    this.columnleavesordered=columnleavesordered;
    this.rowleavesordered=rowleavesordered;

    this.colnumber = this.uniquecollabels.length;
    this.rownumber = this.uniquerowlabels.length;

    //define the width and height
    this.width = cellsize_I*this.uniquecollabels.length;
    this.height = cellsize_I*this.uniquerowlabels.length;

    var values = [];
    listdatafiltered.forEach(function(d){values.push(d[zdata]);});
    this.maxvalue = d3.max(values);
    this.minvalue = d3.min(values);

    //initial row/col sort order
    this.rowsortorder=false;
    this.colsortorder=false;

};
d3_chart2d.prototype.add_heatmapdata1rowlabels = function (tileid_I) {
    //add heatmap to the plot
    var uniquerowlabels = this.uniquerowlabels;
    var this_ = this;
    var rowsortorder = this.rowsortorder;
    var tileid = tileid_I;
    var cellsize = this.cellsize;
    var rowleavesordered = this.rowleavesordered

    this.rowlabels = this.svgg.append("g").selectAll(".rowLabelg")
        .data(uniquerowlabels);

    this.rowlabelsenter = this.rowlabels.enter()
        .append("text")
        .text(function (d) { 
            return d; })
        .attr("x", 0)
        .attr("y", function (d, i) { 
            return rowleavesordered.indexOf(i) * cellsize; })
        .style("text-anchor", "end")
        .attr("transform", "translate(" + (-cellsize) + "," + cellsize / 1.5 + ")")
        .attr("class", function (d,i) { return "rowLabel mono r"+i;} )
        .on("mouseover", function(d) {d3.select(this).classed("text-hover",true);})
        .on("mouseout" , function(d) {d3.select(this).classed("text-hover",false);})
        .on("click", function(d,i) {
            rowsortorder=!rowsortorder; 
            this_.sortbylabel("r",i,rowsortorder); 
            d3.select('#'+tileid+'datalist').property("selectedIndex", 4).node().focus();
            });

};
d3_chart2d.prototype.add_heatmapdata1columnlabels = function (tileid_I) {
    //add heatmap to the plot
    var uniquecollabels = this.uniquecollabels;
    var this_ = this;
    var colsortorder = this.colsortorder;
    var tileid = tileid_I;
    var cellsize = this.cellsize;
    var columnleavesordered = this.columnleavesordered

    this.collabels = this.svgg.append("g").selectAll(".colLabelg")
        .data(uniquecollabels);

    this.collabelsenter = this.collabels.enter()
        .append("text")
        .text(function (d) { return d; })
        .attr("x", 0)
        .attr("y", function (d, i) { return columnleavesordered.indexOf(i) * cellsize; })
            .style("text-anchor", "left")
            .attr("transform", "translate("+cellsize/2 + "," + (-cellsize) + ") rotate (-90)")
            .attr("class",  function (d,i) { return "colLabel mono c"+i;} )
            .on("mouseover", function(d) {d3.select(this).classed("text-hover",true);})
            .on("mouseout" , function(d) {d3.select(this).classed("text-hover",false);})
            .on("click", function (d, i) {
                colsortorder = !colsortorder;
                this_.sortbylabel("c", i, colsortorder);
                //d3.select('#'+tileid+'datalist').property("selectedIndex", 4).node().focus(); 
                });

};
d3_chart2d.prototype.sortbylabel = function (rORc,i,sortOrder){
    var columnsindex_I = this.data1keymap.columnsindex;
    var rowsindex_I = this.data1keymap.rowsindex;
    var cellsize_I = this.cellsize;
    var col_number = this.colnumber;
    var row_number = this.rownumber;

    var t = this.svgg.transition().duration(3000); //todo: broken
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
       .attr("x", function(d) { return sorted.indexOf(d[columnsindex_I]) * cellsize_I; })
       ;
     t.selectAll(".colLabel")
      .attr("y", function (d, i) { return sorted.indexOf(i) * cellsize_I; })
     ;
    }else{ // sort log2ratio of a contrast
     sorted=d3.range(row_number).sort(function(a,b){if(sortOrder){ return log2r[b]-log2r[a];}else{ return log2r[a]-log2r[b];}});
     t.selectAll(".cell")
       .attr("y", function(d) { 
        return sorted.indexOf(d[rowsindex_I]) * cellsize_I; })
       ;
     t.selectAll(".rowLabel")
      .attr("y", function (d, i) { 
      return sorted.indexOf(i) * cellsize_I; });
    };
};
d3_chart2d.prototype.heatmaporder = function (cellsize_I,value_I,
            rowsindex_I,columnsindex_I,
            rowleavesordered_I,columnleavesordered_I,
            svgg_I){
    if(value_I=="hclust"){
        var t = svgg_I.transition().duration(3000);
        t.selectAll(".cell")
            //check indexing (may need to add +1)
          .attr("x", function(d) { return columnleavesordered_I.indexOf(d[columnsindex_I]) * cellsize_I; })
          .attr("y", function(d) { return rowleavesordered_I.indexOf(d[rowsindex_I]) * cellsize_I; })
          ;

        t.selectAll(".rowLabel")
          .attr("y", function (d, i) { return rowleavesordered_I.indexOf(i) * cellsize_I; })
          ;

        t.selectAll(".colLabel")
          .attr("y", function (d, i) { return columnleavesordered_I.indexOf(i) * cellsize_I; })
          ;

    }else if (value_I=="probecontrast"){
        var t = svgg_I.transition().duration(3000);
        t.selectAll(".cell")
          .attr("x", function(d) { return (d[columnsindex_I]) * cellsize_I; })
          .attr("y", function(d) { return (d[rowsindex_I]) * cellsize_I; })
          ;

        t.selectAll(".rowLabel")
          .attr("y", function (d, i) { return i * cellsize_I; })
          ;

        t.selectAll(".colLabel")
          .attr("y", function (d, i) { return i * cellsize_I; })
          ;

    }else if (value_I=="probe"){
        var t = svgg_I.transition().duration(3000);
        t.selectAll(".cell")
          .attr("y", function(d) { return (d[rowsindex_I]) * cellsize_I; })
          ;

        t.selectAll(".rowLabel")
          .attr("y", function (d, i) { return i * cellsize_I; })
          ;
    }else if (value_I=="contrast"){
        var t = svgg_I.transition().duration(3000);
        t.selectAll(".cell")
          .attr("x", function(d) { return (d[columnsindex_I]) * cellsize_I; })
          ;
        t.selectAll(".colLabel")
          .attr("y", function (d, i) { return i * cellsize_I; })
          ;
    };
};
d3_chart2d.prototype.add_heatmapdata1 = function () {
    //add heatmap to the plot

    var listdatafiltered = this.data1.listdatafiltered;
    var columnslabel = this.data1keymap.columnslabel;
    var rowslabel = this.data1keymap.rowslabel;   
    var columnsindex = this.data1keymap.columnsindex;
    var rowsindex = this.data1keymap.rowsindex;   
    var columnsleaves = this.data1keymap.columnsleaves;
    var rowsleaves = this.data1keymap.rowsleaves;   
    var zdata = this.data1keymap.zdata;
    var colorscale = this.colorscale;
    var cellsize = this.cellsize

    this.heatmap = this.svgg.append("g")
        .attr("class","g3")
        .selectAll(".cellg")
        .data(listdatafiltered,function(d){return d[rowsindex]+":"+d[columnsindex];});
    
    this.heatmapenter = this.heatmap
        .enter()
        .append("rect")
        .attr("x", function(d) { return d[columnsleaves] * cellsize; })
        .attr("y", function(d) { return d[rowsleaves] * cellsize; })
        .attr("class", function(d){return "cell cell-border cr"+(d[rowsindex])+" cc"+(d[columnsindex]);})
        .attr("width", cellsize)
        .attr("height", cellsize)
        .style("fill", function(d) { return colorscale(d[zdata]); });
};
d3_chart2d.prototype.add_heatmapdata1animation = function () {
    //add animation to heatmapdata1

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
                     (this.x.baseVal.value)+cellsize >= d.x && (this.x.baseVal.value)<=d.x+d.width &&
                     (this.y.baseVal.value)+cellsize >= d.y && (this.y.baseVal.value)<=d.y+d.height
                 ) {

                     d3.select(this)
                     .classed("cell-selection", true)
                     .classed("cell-selected", true);

                     d3.select(".r"+(cell_d[rowsindex]))
                     .classed("text-selection",true)
                     .classed("text-selected",true);

                     d3.select(".c"+(cell_d[columnsindex]))
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
d3_chart2d.prototype.add_heatmapdata1tooltipandfill = function () {
    //add tooltip and fill on cell mouseover

    var listdatafiltered = this.data1.listdatafiltered;
    var columnslabel = this.data1keymap.columnslabel;
    var rowslabel = this.data1keymap.rowslabel;   
    var columnsindex = this.data1keymap.columnsindex;
    var rowsindex = this.data1keymap.rowsindex;   
    var zdata = this.data1keymap.zdata;
    var colorscale = this.colorscale;
    var id = this.id;

    this.heatmapenter
        .on("mouseover", function(d){
               //highlight text
               d3.select(this).classed("cell-hover",true);
               d3.selectAll(".rowLabel").classed("text-highlight",function(r,ri){ return ri==(d[rowsindex]);});
               d3.selectAll(".colLabel").classed("text-highlight",function(c,ci){ return ci==(d[columnsindex]);});
            //Update the tooltip position and value
                d3.select("#" + id + "tooltip")
                 .style("left", (d3.event.pageX+10) + "px")
                 .style("top", (d3.event.pageY-10) + "px")
                     .select("#" + id + "value")
                     .text(rowslabel + ": " + d[rowslabel] + ",\n" + columnslabel + ": " + d[columnslabel] + ",\n" + zdata + ": " + d[zdata]);
                     //.text(d[rowslabel]+","+d[columnslabel]+"\ndata:"+d[zdata]);
            //Show the tooltip
               d3.select("#" + id + "tooltip").classed("hidden", false);
        })
        .on("mouseout", function(){
               d3.select(this).classed("cell-hover",false);
               d3.selectAll(".rowLabel").classed("text-highlight",false);
               d3.selectAll(".colLabel").classed("text-highlight", false);
               d3.select("#" + id + "tooltip").classed("hidden", true);
        });

};
d3_chart2d.prototype.add_heatmapdata1legend = function(){
    // add lengend to the heatmap

    var listdatafiltered = this.data1.listdatafiltered;
    var columnslabel = this.data1keymap.columnslabel;
    var rowslabel = this.data1keymap.rowslabel;   
    var columnsindex = this.data1keymap.columnsindex;
    var rowsindex = this.data1keymap.rowsindex;   
    var zdata = this.data1keymap.zdata;
    var colorscale = this.colorscale;
    var id = this.id;
    var minvalue = this.minvalue;
    var maxvalue = this.maxvalue;
    var legendelementwidth = this.legendelementwidth;
    var cellsize = this.cellsize;
    var height = this.height;
    var width = this.width;

    //var colorfactor = Math.ceil(colorscale.length / (maxvalue - minvalue));
    if (minvalue===0.0 && maxvalue ===1.0){
        this.legenddata1 = this.svgg.selectAll(".legend")
          .data(d3.range(minvalue, maxvalue + (maxvalue - minvalue) / 10, (maxvalue - minvalue) / 10)); //specific to resequencing data (domain 0.0-1.0)
        this.legenddata1enter = this.legenddata1
          .enter().append("g")
          .attr("class", "legend");
        var colorfactor = 0.1;
    } else{
        this.legenddata1 = this.svgg.selectAll(".legend")
          .data(d3.range(Math.floor(minvalue), Math.ceil(maxvalue))); //use for expression data (domain -10.0-10.0)
        this.legenddata1enter = this.legenddata1
          .enter().append("g")
          .attr("class", "legend");
        var colorfactor = Math.ceil(21.0 / (maxvalue - minvalue));
          };
    
    this.legenddata1.exit().remove();

    this.legenddata1.select("rect").transition()
        .attr("x", function (d, i) { return legendelementwidth * i; })
        .attr("y", height + (cellsize * 2))
        .attr("width", legendelementwidth)
        .attr("height", cellsize)
        .style("fill", function (d, i) { return colorscale(i * colorfactor); });

    this.legenddata1enter.append("rect")
        .attr("x", function (d, i) { return legendelementwidth * i; })
        .attr("y", height + (cellsize * 2))
        .attr("width", legendelementwidth)
        .attr("height", cellsize)
        .style("fill", function (d, i) { return colorscale(i * colorfactor); });

    this.legenddata1.select("text").transition()
        .attr("class", "mono")
        .text(function (d) { 
                return d; })
        .attr("width", legendelementwidth)
        .attr("x", function (d, i) { return legendelementwidth * i; })
        .attr("y", height + (cellsize * 4));

    this.legenddata1enter.append("text")
        .attr("class", "mono")
        .text(function (d) { 
            return d; })
        .attr("width", legendelementwidth)
        .attr("x", function (d, i) { 
            return legendelementwidth * i; })
        .attr("y", height + (cellsize * 4));

};
d3_chart2d.prototype.add_heatmapdata1drowpdownmenu = function (tileid_I){
    // add data list (menu) to tile for the heatmap
    var tileid = this.tileid;
    var heatmaporder = this.heatmaporder;
    var svgg = this.svgg;
   
    var columnsindex = this.data1keymap.columnsindex;
    var rowsindex = this.data1keymap.rowsindex;
    var cellsize = this.cellsize;
    var columnleavesordered = this.columnleavesordered;
    var rowleavesordered = this.rowleavesordered;

//     d3.select("#"+tileid_I + 'dropdownli').on("click",function(){
//         heatmaporder(cellsize,this.value,
//             rowsindex,columnsindex,
//             rowleavesordered, columnleavesordered,svgg);
//     });
    d3.select("#"+tileid + 'dropdownul').on("change",function(){
        heatmaporder(cellsize,this.value,
            rowsindex,columnsindex,
            rowleavesordered, columnleavesordered,svgg);
    });
};
d3_chart2d.prototype.add_heatmapdata1datalist = function (tileid_I){
    // add data list (menu) to tile for the heatmap
    var tileid = this.tileid;
    var heatmaporder = this.heatmaporder;
    var svgg = this.svgg;
   
    var columnsindex = this.data1keymap.columnsindex;
    var rowsindex = this.data1keymap.rowsindex;
    var cellsize = this.cellsize;
    var columnleavesordered = this.columnleavesordered;
    var rowleavesordered = this.rowleavesordered;

    d3.select("#"+tileid_I+"datalist").on("change",function(){
        heatmaporder(cellsize,this.value,
            rowsindex,columnsindex,
            rowleavesordered, columnleavesordered,svgg);
    });
}
d3_chart2d.prototype.set_heatmapdata1css = function () {
    //set predefined heatmap style

    var selector1 = '#' + this.id + ' rect.selection';
    var style1 = {
        'stroke': '#333',
        'stroke-dasharray': '4px',
        'stroke-opacity': '0.5',
        'fill': 'transparent'
    };
    var selector2 = '#' + this.id + ' rect.cell-border';
    var style2= {
        'stroke': '#eee',
        'stroke-width': '0.3px'
    };
    var selector3 = '#' + this.id + ' rect.cell-selected';
    var style3 = {
        'stroke': 'rgb(51,102,153)',
        'stroke-width': '0.5px'
    };
    var selector4 = '#' + this.id + ' rect.cell-hover';
    var style4 = {
        'stroke': '#F00',
        'stroke-width': '0.3px'
    };
    var selector5 = '#' + this.id + ' text.mono';
    var style5 = {
        'font-size': '10pt',
        'font-family': 'Consolas, courier',
        'fill': '#aaa'
    };
    var selectorstyle = [{ 'selection': selector1, 'style': style1 },
                     { 'selection': selector2, 'style': style2 },
                     { 'selection': selector3, 'style': style3 },
                     { 'selection': selector4, 'style': style4 },
                     { 'selection': selector5, 'style': style5 }];
    this.set_svggcss(selectorstyle);
};