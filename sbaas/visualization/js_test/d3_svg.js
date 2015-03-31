d3_svg = function () {
    // generic chart
    this.id = '';
    this.tileid = '';
    this.svgelement = null;
    this.svgg = null;
    this.margin = {};
    this.width = 1;
    this.height = 1;
    this.xscale = 1;
    this.yscale = 1;
};
d3_svg.prototype.set_tileid = function (tileid_I) {
    // set svg tile id
    this.tileid=tileid_I;
};
d3_svg.prototype.set_id = function (id_I) {
    // set svg id
    this.id=id_I;
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
d3_svg.prototype.set_svgelement = function () {
    // set svg element

    this.svgelement = d3.select(this.tileid)
        .append("svg");

    this.svgelement.attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);
    
    this.svgg = this.svgelement.selectAll("svg")
        .append('g');
    
};
d3_svg.prototype.add_svgexportbutton = function () {
    // add button to export the svg element
    this.svgexportbutton = d3.select(this.tileid).append("form");

    this.svgexportbutton_label = this.svgexportbutton.selectAll("form").append("label");
    this.svgexportbutton_label.text("Export as SVG");

    this.svgexportbutton_input = this.svgexportbutton.selectAll("form").append("input");
    this.svgexportbutton_input.attr("type","button")
        .attr("value","Download")
        .attr("onclick",this.export_svgelement(true));

};
d3_svg.prototype.export_svgelement = function (do_beautify_I) {
    // add export the svg element
    //Input:
    // do_beautify = boolean (requires beautify plugin

    var a = document.createElement('a'), xml, ev;
    a.download = 'figure' + '.svg'; // file name
    // convert node to xml string
    //xml = (new XMLSerializer()).serializeToString(d3.select(svg_sel).node()); //div element interferes with reading the svg file in illustrator/pdf/inkscape
    xml = (new XMLSerializer()).serializeToString(d3.select(this.tileid).selectAll('svg')[0][0]);
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