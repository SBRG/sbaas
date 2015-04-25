d3_tile = function () {
    // generic d3_tile element
    // based on the bootstrap panel model
    // panel panel-default
    // panel-heading
    // panel-body
    // panel-footer
    this.containerid = 'container'
    this.tileid = '';
    this.rowid = '';
    this.colid = '';
    this.rowclass = '';
    this.colclass = '';
    this.tileclass = '';
    this.tile = null;
    this.width = 1;
    this.height = 1;
};
d3_tile.prototype.set_tileid = function (tileid_I) {
    // set d3_tile id
    this.tileid = tileid_I;
};
d3_tile.prototype.set_rowid = function (rowid_I) {
    // set row id
    this.rowid = rowid_I;
};
d3_tile.prototype.set_colid = function (colid_I) {
    // set column id
    this.colid = colid_I;
};
d3_tile.prototype.set_rowclass = function (rowclass_I) {
    // set row class
    this.rowclass = rowclass_I;
};
d3_tile.prototype.set_colclass = function (colclass_I) {
    // set column class
    this.colclass = colclass_I;
};
d3_tile.prototype.set_tileclass = function (tileclass_I) {
    // set tile class
    this.tileclass = tileclass_I;
};
d3_tile.prototype.add_tile2container = function () {
    // add tile to container
    if (d3.select("#" + this.containerid).select("#" + this.rowid).select("#" + this.colid).select("#" + this.tileid).node()){
        this.tile = d3.select("#" + this.containerid).select("#" + this.rowid).select("#" + this.colid).select("#" + this.tileid);
    } else if (d3.select("#" + this.containerid).select("#" + this.rowid).select("#" + this.colid).node()){
        this.append_tile2col();
    } else if (d3.select("#" + this.containerid).select("#" + this.rowid).node()){
        this.append_tile2row();
    } else if (d3.select("#" + this.containerid).node()){
        this.append_tile2container();
    };
};
d3_tile.prototype.append_tile2container = function () {
    // set column id
    var row = d3.select("#" + this.containerid).append("div").attr("class", this.rowclass).attr("id", this.rowid);
    var col = row.append("div").attr("class", this.colclass).attr("id", this.colid);
    this.tile = col.append("div").attr("class", this.tileclass).attr("id", this.tileid);
};
d3_tile.prototype.append_tile2row = function () {
    // add tile as new column in an existing row
    var col = d3.select("#" + this.containerid).select("#" + this.rowid).append("div").attr("class", this.colclass).attr("id", this.colid);
    this.tile = col.append("div").attr("class", this.tileclass).attr("id", this.tileid);
};
d3_tile.prototype.append_tile2col = function () {
    // add tile to as a new row in an existing column
    this.tile = d3.select("#" + this.containerid).select("#" + this.rowid).select("#" + this.colid).append("div").attr("class", this.tileclass).attr("id", this.tileid);
};
d3_tile.prototype.set_height = function () {
    // set d3_tile height
};
d3_tile.prototype.add_draganddrop = function () {
    // add file drag and drop for input
};
d3_tile.prototype.add_form2body = function (textarea_valuetext_I) {
    // add text area for input
    // INPUT:
    //e.g. [{'value':'hclust','text':'by cluster'},...];

    var tileid = this.tileid;

    this.tileform = this.tilebody.append("div")
        .attr("class","form-group")
        .attr("id", tileid + 'form');

    for (i=0;i<textarea_valuetext_I.length;i++){
        var formlabel = this.tileform.append("label")
            .text(textarea_valuetext_I[i].text)
            .attr("id", tileid + 'formlabel' + textarea_valuetext_I[i].text);
        var forminput = this.tileform.append("input")
            .attr("class","form-control")
            .attr("type","text")
            .attr("placeholder",textarea_valuetext_I[i].value)
            .attr("value",textarea_valuetext_I[i].value)
            .attr("id", tileid + 'forminput'+ textarea_valuetext_I[i].text);
    };
};
d3_tile.prototype.update_form = function(textarea_valuetext_I){
    // update the form
    var tileid = this.tileid;

    for (i=0;i<textarea_valuetext_I.length;i++){
        d3.select("#"+tileid + 'forminput'+ textarea_valuetext_I[i].text).node().value=textarea_valuetext_I[i].value;
    };
};
d3_tile.prototype.add_checkbox = function () {
    // add checkbox for input
};
d3_tile.prototype.add_color = function () {
    // add color pallet for input
};
d3_tile.prototype.add_range = function () {
    // add range slider for input
};
d3_tile.prototype.add_footer2tile = function () {
    // add footer to tile

    var tileid = this.tileid;

    this.tilefooter = d3.select('#'+tileid).append("div")
        .attr("class","panel-footer")
        .attr("id",tileid+"panel-footer");
};
d3_tile.prototype.add_submitbutton2form = function (button_idtext_I) {
    // add submit button
    // INPUT:
    //e.g. {'id':'submit1','text':'submit'};
    if (!button_idtext_I){var button_idtext = {'id':'submit1','text':'submit'};}
    else{var button_idtext = button_idtext_I;}

    var tileid = this.tileid;

    var submitbutton = this.tileform.append("button")
        .attr("class","btn btn-default")
        .attr("type","submit")
        .attr("id", tileid + 'submitbutton'+button_idtext.id)
        .text(button_idtext.text);
};
d3_tile.prototype.add_submitbutton2footer = function (button_idtext_I) {
    // add submit button
    // INPUT:
    //e.g. {'id':'submit1','text':'submit'};
    if (!button_idtext_I){var button_idtext = {'id':'submit1','text':'submit'};}
    else{var button_idtext = button_idtext_I;}

    var tileid = this.tileid;

    var submitbuttonrow = this.tilefooter.append("button")
        .attr("class","btn btn-default column-button")
        .attr("id", tileid + 'submitbutton'+button_idtext.id)
        .text(button_idtext.text);
};
d3_tile.prototype.add_table = function () {
    // add button for output
};
d3_tile.prototype.add_svg = function () {
    // add svg for interaction
};
d3_tile.prototype.remove_tile = function(){
    // remove tile from the container
    var tileid = this.tileid;
    d3.selectAll('#'+tileid).remove();
    this.tile = null;
};
d3_tile.prototype.add_datalist2body = function (datalist_valuetext_I) {
    // add datalist (menu) for input
    // INPUT:
    //e.g. [{'value':'hclust','text':'by cluster'},...];

    var tileid = this.tileid;  

    var datalist = this.tilebody.append("select")
        .attr("id", tileid + 'datalist');

    for (i=0;i<datalist_valuetext_I.length;i++){
        datalist.append("option")
            .attr("value",datalist_valuetext_I[i].value)
            .text(datalist_valuetext_I[i].text);
    };  
};
d3_tile.prototype.add_dropdown2body = function (datalist_valuetext_I) {
    // add datalist (menu) for input
    // INPUT:
    //e.g. [{'value':'hclust','text':'by cluster'},...];

    var tileid = this.tileid;

    var tiledropdown = this.tilebody.append("div")
        .attr("class","dropdown")
    var tiledropdownbutton = tiledropdown
        .append("button")
        .attr("class","btn btn-default dropdown-toggle")
        .attr("type","button")
        .attr("id",tileid + 'dropdownbutton')
        .attr("data-toggle","dropdown")
        .attr("aria-expanded","true")
        .text("sort")
        .append("span")
        .attr("class","caret");    

    var tiledropdownul = tiledropdown
        .append("ul")
        .attr("class","dropdown-menu")
        .attr("role","menu")
        .attr("id",tileid + 'dropdownul')
        .attr("aria-labelledby",tileid + 'dropdownbuttonul');

    for (i=0;i<datalist_valuetext_I.length;i++){
        var tiledropdownli = tiledropdownul.append("li")
            .attr("role","presentation")
            .append("a")
            .attr("role","menuitem")
            .attr("tabindex","-1")
            .attr("value",datalist_valuetext_I[i].value)
            .attr("id",tileid + 'dropdownli'+datalist_valuetext_I[i].value)
            .text(datalist_valuetext_I[i].text);
    };


};
d3_tile.prototype.add_header2tile = function (title_I){
    //add title to tileid

    var tileid = this.tileid;

    this.tileheader = d3.select('#'+tileid).append("div")
        .attr("class","panel-heading")
        .attr("id",tileid+"panel-heading");
};
d3_tile.prototype.add_title2header = function (title_I){
    //add title to tileid

    var tileid = this.tileid;

    var title = this.tileheader.append("h3")
        .text(title_I);
};
d3_tile.prototype.add_removebutton2header = function(){
    // add button to remove tile from the container

    var tileid = this.tileid;
    var this_ = this;
    var remove_tile = this.remove_tile;

    function removetile(){
        d3.selectAll('#'+tileid).remove();
        this_.tile = null;
    };

    var removebutton = this.tileheader.append("a")
        .attr("class","pull-right")
        .attr("id", tileid + 'removebutton')
        .text("remove")
        .on("click",removetile);
};
d3_tile.prototype.add_body2tile = function (title_I){
    //add title to tileid

    var tileid = this.tileid;

    this.tilebody = d3.select('#'+tileid).append("div")
        .attr("class","panel-body")
        .attr("id",tileid+"panel-body")
};
