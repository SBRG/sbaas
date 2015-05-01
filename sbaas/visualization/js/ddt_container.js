"use strict";
function ddt_container(){
//var ddt_container = function (){
    // ddt_container class
    this.parameters = [];
    this.tiles = [];
    this.data = [];
    this.tile2datamap = {};
    this.containerid = 'container'
    this.container=null;
};
ddt_container.prototype.set_parameters = function(parameters_I){
    // set parameters to container
    //INPUT:
    // parameters_I = [
    //           {tileid:'',...//tileproperties 
    //            svgid:'',...//svgproperties},...]
    this.parameters=parameters_I;
};
ddt_container.prototype.set_tile = function(tiles_I){
    // set tile to container
    this.tiles=tiles_I;
};
ddt_container.prototype.set_data = function(data_I){
    // set data to container
    this.data=data_I;
};
ddt_container.prototype.set_tile2datamap = function(tile2datamap_I){
    // set tile2datamap to container
    // INPUT:
    // tile2datamap_I = {tileid:[dataindex,...],...}
    this.tile2datamap=tile2datamap_I;
};
ddt_container.prototype.add_parameters = function(parameters_I){
    // add parameters to container
    this.parameters.push(parameters_I);
};
ddt_container.prototype.add_tile = function(tile_I){
    // add tile to container
    this.tiles.push(tile_I);
};
ddt_container.prototype.add_data = function(data_I){
    // add data to container
    //INPUT:
    // data_I = [{data:[],datakeys:[],datanestkeys:[]},...]
    for (var cnt=0;cnt<data_I.length;cnt++){ //switched from i to cnt due to i changing within the loop
        var d3data = new d3_data();
        d3data.set_keys(data_I[cnt].datakeys);
        d3data.set_listdata(data_I[cnt].data,data_I[cnt].datanestkeys);
        d3data.reset_filters();
        this.data.push(d3data);
    };
};
ddt_container.prototype.add_containertiles = function(){
    // get all container tiles based on parameters
    // tiles will be added in the same order as the parameters
    for (var i=0;i<this.parameters.length;i++){
        var tiletype = this.parameters[i].tiletype
        var tile = this.get_tile(tiletype);
        this.tiles.push(tile);
    };
};
ddt_container.prototype.make_container = function(){
    // call all tile make functions
    var data = this.data;
    this.add_containertiles();
    for (var cnt=0;cnt<this.tiles.length;cnt++){ //switched from i to cnt due to i changing within the loop
        var tiledataindex = this.tile2datamap[this.parameters[cnt].tileid];
        var tiledata = [];
        tiledataindex.forEach(function(d){tiledata.push(data[d]);});
        this.tiles[cnt].make_tile(tiledata,this.parameters[cnt]);
    };
};
ddt_container.prototype.update_container = function(){
    // call all tile update functions
    var data = this.data;
    for (var cnt=0;cnt<this.tiles.length;cnt++){ //switched from i to cnt due to i changing within the loop
        var tiledataindex = this.tile2datamap[this.parameters[cnt].tileid];
        var tiledata = [];
        tiledataindex.forEach(function(d){tiledata.push(data[d]);});
        this.tiles[cnt].update_tile(tiledata);
    };     
};
ddt_container.prototype.reset_containerdata = function(){
    // reset data filters and call all tile update functions
    for (cnt=0;cnt<this.data.length;cnt++){ //switched from i to cnt due to i changing within the loop
        this.data[cnt].reset_filters();
    };
    var data = this.data;
    for (var cnt=0;cnt<this.tiles.length;cnt++){ //switched from i to cnt due to i changing within the loop
        var tiledataindex = this.tile2datamap[this.parameters[cnt].tileid];
        var tiledata = [];
        tiledataindex.forEach(function(d){tiledata.push(data[d]);});
        this.tiles[cnt].update_tile(tiledata);
    };     
};
ddt_container.prototype.get_tile = function(tiletype_I){
    // return the appropriate tile object
    if (tiletype_I=='html'){
        return new ddt_tile_html();
    } else if (tiletype_I=='svg'){
        return new ddt_tile_svg();
    } else if (tiletype_I=='table'){
        return new ddt_tile_table();
    } else {
        return null;
    };
};
ddt_container.prototype.filter_containerdata = function(filter_I){
    // apply a global filter to all container data
    // INPUT:
    // filter_I = {key:value,...}
    for (var cnt=0;cnt<this.data.length;cnt++){ //switched from i to cnt due to i changing within the loop
        this.data[cnt].change_filters(filter_I);
    };
};
ddt_container.prototype.sync_containerdata = function(){
    // update all tiles on tile change
    // TODO: 1. pass target syncs as parameters
    //       2. implement "onchange"
    var data = this.data;
    var tiles_ = this.tiles;
    var parameters_ = this.parameters;
    var tile2datamap_ = this.tile2datamap;
    function update(){
        for (var cnt=0;cnt<tiles_.length;cnt++){ //switched from i to cnt due to i changing within the loop
            var tiledataindex = tile2datamap_[parameters_[cnt].tileid];
            var tiledata = [];
            tiledataindex.forEach(function(d){tiledata.push(data[d]);});
            tiles_[cnt].update_tile(tiledata);
        };     
    };
    for (var cnt=0;cnt<this.tiles.length;cnt++){ //switched from i to cnt due to i changing within the loop
        // sync svg
        if (this.tiles[cnt].parameters.svgid){
            //var synctiles = d3.select("#" + this.tiles[cnt].parameters.svgid + " g").on("haschange",update);
            var synctiles = d3.select("#" + this.tiles[cnt].parameters.tileid + "panel-body").on("click",update);
        };
        // sync table elements
        if (this.tiles[cnt].parameters.tableid){
            //var synctiles = d3.select("#" + this.tiles[cnt].parameters.tileid + " tbody").on("haschange",update);
            var synctiles = d3.select("#" + this.tiles[cnt].parameters.tileid + "panel-body").on("click",update);
        };
    };
};
ddt_container.prototype.add_datafiltermenusubmitbutton = function (tileid_I,htmlid_I,submitbuttonid_I){
    // add filter menu submit button listener to tile
    if (tileid_I){var tileid = tileid_I;}
    else{var tileid = this.tiles[0].parameters.tileid;};
    if (htmlid_I){var htmlid = htmlid_I;}
    else{var htmlid = this.tiles[0].parameters.htmlid;};
    if (submitbuttonid_I){var submitbuttonid = submitbuttonid_I;}
    else{var submitbuttonid = 'submit1';};

    var this_ = this;

    function submit(){
        var filterstringmenu = [];
        var tileindex = 0;
        var tiledataindex = 0;
        this_.tiles.forEach(function(d,i){
            if (d.parameters.tileid === tileid){
                tileindex=i;
                tiledataindex = this_.tile2datamap[d.parameters.tileid];
            };
        })
        for (var key in this_.data[tiledataindex].filters){
            var filterkey = d3.select("#"+htmlid+'formlabel'+key).text();
            var filterstring = d3.select("#"+htmlid+'forminput'+key).node().value;
            filterstringmenu.push({"text":filterkey,"value":filterstring});
        };
        for (var cnt=0;cnt<this_.data.length;cnt++){
            this_.data[cnt].convert_stringmenuinput2filter(filterstringmenu);
            this_.data[cnt].filter_stringdata();
        };
//         this_.tiles[tileindex].data[0].convert_stringmenuinput2filter(filterstringmenu);
//         this_.tiles[tileindex].data[0].filter_stringdata();
        this_.update_container();  
    };

    this.submitbutton = d3.select("#"+tileid+'submitbutton'+submitbuttonid)
        .on("click",submit);
};
ddt_container.prototype.add_datafiltermenuresetbutton = function (tileid_I,resetbuttonid_I){
    // add filter menu reset button listener to tile
    if (tileid_I){var tileid = tileid_I;}
    //else{var tileid = this.tiles[0].parameters.htmlid;};
    else{var tileid = this.tiles[0].parameters.tileid;};
    if (resetbuttonid_I){var resetbuttonid = resetbuttonid_I;}
    else{var resetbuttonid = 'reset1';};
    
    var this_ = this;
    
    function reset(){
        // reset data filters and call all tile update functions
        for (var cnt=0;cnt<this_.data.length;cnt++){ //switched from i to cnt due to i changing within the loop
            this_.data[cnt].reset_filters();
            this_.data[cnt].filter_stringdata();
        };
        this_.update_container();    
    };

    this.resetbutton = d3.select("#"+tileid+'submitbutton'+resetbuttonid)
        .on("click",reset);
};
ddt_container.prototype.add_datafiltermenuupdatebutton = function (tileid_I,updatebuttonid_I){
    // add filter menu reset button listener to tile
    if (tileid_I){var tileid = tileid_I;}
    //else{var tileid = this.tiles[0].parameters.htmlid;};
    else{var tileid = this.tiles[0].parameters.tileid;};
    if (updatebuttonid_I){var updatebuttonid = updatebuttonid_I;}
    else{var updatebuttonid = 'update1';};
    
    var this_ = this;
    
    function update(){
        this_.update_container();    
    };

    this.updatebutton = d3.select("#"+tileid+'submitbutton'+updatebuttonid)
        .on("click",update);
};