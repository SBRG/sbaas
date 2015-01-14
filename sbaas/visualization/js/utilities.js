
download_json = function (json, name) {
    var a = document.createElement('a');
    a.download = name + '.json'; // file name
    var j = JSON.stringify(json);
    a.setAttribute("href-lang", "application/json");
    a.href = 'data:application/json,' + j;
    // <a> constructed, simulate mouse click on it
    var ev = document.createEvent("MouseEvents");
    ev.initMouseEvent("click", true, false, self, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    a.dispatchEvent(ev);

    function utf8_to_b64(str) {
        return window.btoa(unescape(encodeURIComponent(str)));
    }
}

load_json = function(f, callback) {
    // Check for the various File API support.
    if (!(window.File && window.FileReader && window.FileList && window.Blob))
        callback("The File APIs are not fully supported in this browser.", null);

    // The following is not a safe assumption.
    // if (!f.type.match("application/json"))
    //     callback.call(target, "Not a json file.", null);

    var reader = new window.FileReader();
    // Closure to capture the file information.
    reader.onload = function (event) {
        var json = JSON.parse(event.target.result);
        callback(null, json);
    };
    // Read in the image file as a data URL.
    reader.readAsText(f);
}

export_svg = function (name, svg_sel, do_beautify) {
    //Input:
    // name = name of the file
    // svg_sel = dom element id that specifies the svg element
    // do_beautify = boolean (requires beautify plugin)
    var a = document.createElement('a'), xml, ev;
    a.download = name + '.svg'; // file name
    // convert node to xml string
    //xml = (new XMLSerializer()).serializeToString(d3.select(svg_sel).node()); //div element interferes with reading the svg file in illustrator/pdf/inkscape
    xml = (new XMLSerializer()).serializeToString(d3.select(svg_sel).selectAll('svg')[0][0]);
    if (do_beautify) xml = vkbeautify.xml(xml);
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

function isInArray(value, array) {
    return array.indexOf(value) > -1;
}