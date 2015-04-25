//implement sortable and editable table using d3 and bootstrap
var d3_table = function (){
    this.id = '';
    this.tileid = '';
    this.tableclass = '';
    this.table = null;
    this.data = null;  
    this.tableheaders = [];
};
d3_table.prototype.add_table2tile = function(){
    // set the table
    var id = this.id;
    var tileid = this.tileid;
    var tableclass = this.tableclass;
    var listdatafiltered = this.data.listdatafiltered;
    var tableheaders = this.tableheaders;

//     this.table = d3.select('#'+tileid+"panel-body").append("div")
//         .attr("class","table-responsive")
//         .append("table")
//         .attr("class",tableclass)
//         .attr("id",id+"table");

    this.tableelement = d3.select('#'+tileid+"panel-body").selectAll(".table-responsive")
        .data([listdatafiltered]);

    this.tableenter = this.tableelement.enter()
        .append("div")
        .attr("class","table-responsive")
        .append("table")
        .attr("class",tableclass)
        .attr("id",id+"table");

    this.table = this.tableelement.select("table");
    this.tableelement.exit().remove();

};
d3_table.prototype.set_tableheader = function(){
    // set the table header
    var id = this.id;
    var listdatafiltered = this.data.listdatafiltered;

//     this.thead = this.table
//         .append("thead")
//         .attr("id",id+"tableheader");
    
    this.theadelement = this.table.selectAll("thead")
        .data([listdatafiltered]);

    this.theadenter = this.theadelement.enter()
        .append("thead")
        .attr("id",id+"tableheader");

    this.thead = this.table.select("thead");
    //this.thead = this.theadelement.select("thead");
    this.theadelement.exit().remove();

};
d3_table.prototype.add_tableheader = function(){
    // add the table header
    var id = this.id;
    var tileid = this.tileid;
    var tableheaders = this.tableheaders;

    //table header
// //     this.tableheader = this.thead.append("tr").selectAll("th")
// //         .data(tableheaders);

//     this.tableheader = this.thead.append("tr").selectAll("th")
//         .data(tableheaders);
// //     this.tableheader = this.theadenter.append("tr").selectAll("th")
// //         .data(tableheaders);
        
    this.tableheaderrow = this.thead.selectAll("tr")
        .data([tableheaders]);

    this.tableheaderrowenter = this.tableheaderrow.enter()
        .append("tr");

    this.tableheader = this.tableheaderrow.selectAll("th")
        .data(tableheaders);

    this.tableheaderenter = this.tableheader.enter();
    this.tableheaderenter.append("th")
        .text(function (d) { return d; });

    this.tableheader.transition().text(function (d) { return d; });

    this.tableheader.exit().remove();

    this.tableheaderrow.exit().remove();

};
d3_table.prototype.set_tablebody = function(){
    // set the table body
    var id = this.id;
    var listdatafiltered = this.data.listdatafiltered;

    this.tbodyelement = this.table.selectAll("tbody")
        .data([listdatafiltered]);

    this.tbodyenter = this.tbodyelement.enter()
        .append("tbody")
        .attr("id",id+"tablebody");

    this.tbody = this.table.select("tbody");
    //this.tbody = this.tbodyelement.select("tbody");

    this.tbodyelement.exit().remove();

};
d3_table.prototype.add_tablebody = function(){
    // add the table body
    var id = this.id;
    var tileid = this.tileid;
    var datalistdatafiltered = this.data.listdatafiltered;
    var tableheaders = this.tableheaders;
        
    //table body

    this.tablerows = this.tbody.selectAll("tr")
        .data(datalistdatafiltered);

    this.tablerows.exit().remove();

    this.tablerowsenter = this.tablerows.enter()
        .append("tr");

    //this.tablecells = this.tablerowsenter.selectAll("td")
    this.tablecells = this.tablerows.selectAll("td")
        .data(function(row) {
            return tableheaders.map(function(column) {
                return {column: column, value: row[column]};
            });
        });

    this.tablecells.exit().remove();

    this.tablecellsenter = this.tablecells.enter();
    this.tablecellsenter.append("td")
        .html(function(d) { return d.value; });

    this.tablecells.html(function(d) { return d.value; });

};
d3_table.prototype.set_id = function(tableid_I){
    // set the tableid
    this.id = tableid_I;
};
d3_table.prototype.set_tileid = function(tabletileid_I){
    // set the table tileid
    this.tileid = tabletileid_I;
};
d3_table.prototype.set_tableclass = function(tableclass_I){
    // set the tableid
    this.tableclass = tableclass_I;
};
d3_table.prototype.add_data = function(data_I){
    // set the tableid
    this.data = data_I;
};
d3_table.prototype.partition_listdatafiltered2tableheaderandelements = function(){
    // partition list data to an array of headers and an array of values
    this.tableheaders = [];
    this.tableelements = [];
    var datalistdatafiltered = this.data.listdatafiltered;
    for (i=0;i<datalistdatafiltered.length;i++){
        for (key in datalistdatafiltered[i]){
            if (i===0){
                this.tableheaders.push(key);
            };
            this.tableelements.push(datalistdatafiltered[i][key])
        };
    };
};
d3_table.prototype.extract_tableheaders = function(){
    // extract out headers from listdatafiltered
    this.tableheaders = [];
    var datalistdatafiltered = this.data.listdatafiltered;
    for (key in datalistdatafiltered[0]){
        this.tableheaders.push(key);
    };
};
d3_table.prototype.set_tableheaders = function(headers_I){
    // set headers
    this.tableheaders = headers_I;
};
d3_table.prototype.add_tablecellfilter = function(){
    //filter the data on click
    //TODO:...
    var _this = this;

    this.tablecellsenter.on("click", function (d) {
        var column = null;
        var filters = [];
        _this.data.filters[column].forEach(function (n) { if (n !== d) { filters.push(n);}; });
        _this.data.filters[column] = filters;
        _this.data.filter_stringdata();
        _this.render();
    });
};
d3_table.prototype.render = function(){
    //define the render function here...
};
d3_table.prototype.add_csvexportbutton2tile = function () {
    // add button to export the table element
    var csvexportbutton = d3.select('#'+this.tileid+"panel-footer").append("form");

//     var csvexportbutton_label = csvexportbutton.append("label");
//     csvexportbutton_label.text("Export as csv");

    var csvexportbutton_input = csvexportbutton.append("input");
    csvexportbutton_input.attr("type", "button")
        .attr("value", "Download CSV");
    csvexportbutton_input.on("click", this.export_tableelementcsv);

};
d3_table.prototype.add_jsonexportbutton2tile = function () {
    // add button to export the table element
    var jsonexportbutton = d3.select('#'+this.tileid+"panel-footer").append("form");

//     var jsonexportbutton_label = jsonexportbutton.append("label");
//     jsonexportbutton_label.text("Export as json");

    var jsonexportbutton_input = jsonexportbutton.append("input");
    jsonexportbutton_input.attr("type", "button")
        .attr("value", "Download JSON");
    jsonexportbutton_input.on("click", this.export_tableelementjson);

};
d3_table.prototype.add_csvandjsonexportbutton2tile = function () {
    // add button to export the table element
    var exportbutton = d3.select('#'+this.tileid+"panel-footer").append("form")
        .attr("class","form-group")
        .append("div")
        .attr("class","btn-group");

    var csvexportbutton_input = exportbutton.append("input");
    csvexportbutton_input.attr("type", "button")
        .attr("value", "Download CSV");
    csvexportbutton_input.on("click", this.export_tableelementcsv);

    var jsonexportbutton_input = exportbutton.append("input");
    jsonexportbutton_input.attr("type", "button")
        .attr("value", "Download JSON");
    jsonexportbutton_input.on("click", this.export_tableelementjson);

};
d3_table.prototype.export_tableelementjson = function () {
    // export the table element as json
    //TODO:...

    var a = document.createElement('a');
    a.download = name + '.json'; // file name
    var j = JSON.stringify(json);
    a.setAttribute("href-lang", "application/json");
    a.href = 'data:application/json,' + j;
    // <a> constructed, simulate mouse click on it
    var ev = document.createEvent("MouseEvents");
    ev.initMouseEvent("click", true, false, self, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    a.dispatchEvent(ev);

    // definitions
    function utf8_to_b64(str) {
        return window.btoa(unescape(encodeURIComponent(str)));
    }
};
d3_table.prototype.set_tablecss = function (selectionstyle_I) {
    //set custom css style to table
    //Input:
    // selectionstyle_I = [{selection: string e.g., '.axis line, .axis path'
    //                      style: key:value strings e.g., {'fill': 'none', 'stroke': '#000',
    //                                                      'shape-rendering': 'crispEdges'}}]
    for (i = 0; i < selectionstyle_I.length; i++) {
        this.table.selectAll(selectionstyle_I[i].selection)
            .style(selectionstyle_I[i].style);
    };
};
d3_table.prototype.set_headerstyle = function () {
    // predefined css style for table header rows
    var headerselector = ' th';
    var headerstyle = {
        'font-size': '10px',
        'word-wrap':'break-word',
        'text-align': 'center'
        };
    var selectorstyle = [{ 'selection': headerselector, 'style': headerstyle }]
    this.set_tablecss(selectorstyle);
};
d3_table.prototype.set_cellstyle = function () {
    // predefined css style table cells
    var cellselector = ' td';
    var cellstyle = {
        'font-size': '8px',
        'word-wrap':'break-word',
        'text-align': 'center'
    };
    var selectorstyle = [{ 'selection': cellselector, 'style': cellstyle }]
    this.set_tablecss(selectorstyle);
};
d3_table.prototype.set_tablestyle = function () {
    // predefined css style for table header rows
    var tableselector = "#" + this.tileid + " .table-responsive";
    var tablestyle = {
        //'table-layout': 'fixed',
        'width': '100%',
        'margin-bottom': '15px',
        'overflow-y': 'hidden',
        'overflow-x': 'scroll',
        '-ms-overflow-style': '-ms-autohiding-scrollbar',
        //'border': '1px solid #ddd',
        '-webkit-overflow-scrolling': 'touch'
    };
    var selectorstyle = [{ 'selection': tableselector, 'style': tablestyle }]
    this.set_d3css(selectorstyle);
};
d3_table.prototype.set_d3css = function (selectionstyle_I) {
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
d3_table.prototype.add_datafiltermenusubmitbutton = function (tileid_I,submitbuttonid_I){
    // add data list (menu) to tile for the heatmap
    if (tileid_I){var tileid = tileid_I;}
    else{var tileid = this.tileid;};
    if (submitbuttonid_I){var submitbuttonid = submitbuttonid_I;}
    else{var submitbuttonid = this.submitbuttonid;};

    var this_ = this;

    function submit(){
        var filterstringmenu = [];
        for (key in this_.data.filters){
            var filterkey = d3.select("#"+tileid+'formlabel'+key).text();
            var filterstring = d3.select("#"+tileid+'forminput'+key).node().value;
            filterstringmenu.push({"text":filterkey,"value":filterstring});
        };
        this_.data.convert_stringmenuinput2filter(filterstringmenu);
        this_.data.filter_stringdata();
        this_.render();
    };

    this.submitbutton = d3.select("#"+tileid+'submitbutton'+submitbuttonid)
        .on("mousedown",submit);
};
d3_table.prototype.add_datafiltermenuresetbutton = function (tileid_I,resetbuttonid_I){
    // add data list (menu) to tile for the heatmap
    if (tileid_I){var tileid = tileid_I;}
    else{var tileid = this.tileid;};
    if (resetbuttonid_I){var resetbuttonid = resetbuttonid_I;}
    else{var resetbuttonid = this.resetbuttonid;};

    var this_ = this;
    
    function reset(){
        this_.data.reset_filters();
        this_.data.filter_stringdata();
        this_.render();
    };

    this.resetbutton = d3.select("#"+tileid+'submitbutton'+resetbuttonid)
        .on("click",reset);
};