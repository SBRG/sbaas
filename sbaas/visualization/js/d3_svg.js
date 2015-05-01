"use strict";
//var d3_svg = function () {
function d3_svg() {
    // generic svg element
    this.id = '';
    this.tileid = '';
    this.svgelement = null;
    this.svgg = null;
    this.margin = {};
    this.width = 1;
    this.height = 1;
    this.updatecontainer = false;
};
d3_svg.prototype.set_tileid = function (tileid_I) {
    // set svg tile id
    this.tileid = tileid_I;
};
d3_svg.prototype.set_updatecontainer = function (updatecontainer_I) {
    // set container update status
    // INPUT:
    // boolean, if true, all function calls that re-render
    //          the svg image will trigger an update call
    //          to the container object, which will
    //          propagate out to all other container tiles
    this.containerupdate = containerupdate_I;
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

    var width = this.width;
    var height = this.height;
    var margin = this.margin;
    var tileid = this.tileid;
    var id = this.id;

//     this.svgelement = d3.select('#'+this.tileid+"panel-body")
//         .append("svg").attr("id",this.id);

//     this.svgelement.attr("width", this.width + this.margin.left + this.margin.right)
//         .attr("height", this.height + this.margin.top + this.margin.bottom);

//     this.svgg = this.svgelement
//         .append('g').attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

    this.svgelement = d3.select('#' + tileid+"panel-body").selectAll(".svg-responsive")
        .data([0]);
    
    this.svgenter = this.svgelement.enter()    
        .append("div")
        .attr("class",'svg-responsive')
        .append("svg")
        .attr("id", id)
        .append('g')
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    this.svgelement.selectAll("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    this.svgg = this.svgelement.select('g');

};
d3_svg.prototype.add_svgexportbutton2tile = function () {
    // add button to export the svg element
    var this_ = this;
    var svgexportbutton = d3.select('#'+this.tileid+"panel-footer").append("form");

    function exportsvgelement(){
        this_.export_svgelement(); //necessary to pass svg as "this"
    };

    var svgexportbutton_input = svgexportbutton.append("input");
    svgexportbutton_input.attr("type", "button")
        .attr("value", "Download SVG");
    svgexportbutton_input.on("click", exportsvgelement);

};
d3_svg.prototype.export_svgelement = function () {
    // export the svg element

    //Input:
    // do_beautify = boolean (requires beautify plugin)

    var do_beautify_I = true;
    var a = document.createElement('a'), xml, ev;
    var svg_sel = "#" + this.id;
    a.download = 'figure' + '.svg'; // file name
    // convert node to xml string
    xml = (new XMLSerializer()).serializeToString(d3.select(svg_sel).node()); //div element interferes with reading the svg file in illustrator/pdf/inkscape
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
d3_svg.prototype.add_datalist2tile = function (datalist_valuetext_I) {
    // add datalist (menu) for input

    var tileid = this.tileid;

    var datalist = d3.select('#'+this.tileid).append("select")
        .attr("id", tileid + 'datalist');

    for (i=0;i<datalist_valuetext_I.length;i++){
        datalist.append("option")
            .attr("value",datalist_valuetext_I[i].value)
            .text(datalist_valuetext_I[i].text);
    };

};
d3_svg.prototype.add_data1filtermenusubmitbutton = function (tileid_I,submitbuttonid_I){
    // add data list (menu) to tile for the heatmap
    if (tileid_I){var tileid = tileid_I;}
    else{var tileid = this.tileid;};
    if (submitbuttonid_I){var submitbuttonid = submitbuttonid_I;}
    else{var submitbuttonid = this.submitbuttonid;};

    var this_ = this;

    function submit(){
        var filterstringmenu = [];
        for (key in this_.data1.filters){
            var filterkey = d3.select("#"+tileid+'formlabel'+key).text();
            var filterstring = d3.select("#"+tileid+'forminput'+key).node().value;
            filterstringmenu.push({"text":filterkey,"value":filterstring});
        };
        this_.data1.convert_stringmenuinput2filter(filterstringmenu);
        this_.data1.filter_stringdata();
        this_.render();
    };

    this.submitbutton = d3.select("#"+tileid+'submitbutton'+submitbuttonid)
        .on("mousedown",submit);
};
d3_svg.prototype.add_data2filtermenusubmitbutton = function (tileid_I,submitbuttonid_I){
    // add data list (menu) to tile for the heatmap
    if (tileid_I){var tileid = tileid_I;}
    else{var tileid = this.tileid;};
    if (submitbuttonid_I){var submitbuttonid = submitbuttonid_I;}
    else{var submitbuttonid = this.submitbuttonid;};

    var this_ = this;

    function submit(){
        var filterstringmenu = [];
        for (key in this_.data2.filters){
            var filterkey = d3.select("#"+tileid+'formlabel'+key).text();
            var filterstring = d3.select("#"+tileid+'forminput'+key).node().value;
            filterstringmenu.push({"text":filterkey,"value":filterstring});
        };
        this_.data2.convert_stringmenuinput2filter(filterstringmenu);
        this_.data2.filter_stringdata();
        this_.render();
    };

    this.submitbutton = d3.select("#"+tileid+'submitbutton'+submitbuttonid)
        .on("mousedown",submit);
};
d3_svg.prototype.add_data2filtermenuresetbutton = function (tileid_I,resetbuttonid_I){
    // add data list (menu) to tile for the heatmap
    if (tileid_I){var tileid = tileid_I;}
    else{var tileid = this.tileid;};
    if (resetbuttonid_I){var resetbuttonid = resetbuttonid_I;}
    else{var resetbuttonid = this.resetbuttonid;};

    var this_ = this;
    
    function reset(){
        this_.data2.reset_filters();
        this_.data2.filter_stringdata();
        this_.render();
    };

    this.resetbutton = d3.select("#"+tileid+'submitbutton'+resetbuttonid)
        .on("click",reset);
};
d3_svg.prototype.add_data1filtermenuresetbutton = function (tileid_I,resetbuttonid_I){
    // add data list (menu) to tile for the heatmap
    if (tileid_I){var tileid = tileid_I;}
    else{var tileid = this.tileid;};
    if (resetbuttonid_I){var resetbuttonid = resetbuttonid_I;}
    else{var resetbuttonid = this.resetbuttonid;};

    var this_ = this;
    
    function reset(){
        this_.data1.reset_filters();
        this_.data1.filter_stringdata();
        this_.render();
    };

    this.resetbutton = d3.select("#"+tileid+'submitbutton'+resetbuttonid)
        .on("click",reset);
};
d3_svg.prototype.set_svgstyle = function () {
    // predefined css style for svg
    //var selector1 = "#" + this.id;
    var selector1 = "#" + this.tileid + ' .svg-responsive';
    var style1 = {
        'width': '100%',
        'margin-bottom': '15px',
        'overflow-y': 'hidden',
        'overflow-x': 'scroll',
        '-ms-overflow-style': '-ms-autohiding-scrollbar',
        //'border': '1px solid #ddd',
        '-webkit-overflow-scrolling': 'touch'
    };
    var selectorstyle = [{ 'selection': selector1, 'style': style1 }]
    this.set_d3css(selectorstyle);
};