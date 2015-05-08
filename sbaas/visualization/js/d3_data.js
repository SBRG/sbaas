"use strict";
//var d3_data = function () {
function d3_data() {
    //data function
    this.keys = []; // list of columns that can be applied as nest keys and filters
    this.nestkey = ''; // key to apply to nest
    this.filters = {}; // {key1:[string1,string2,...],...}
    this.listdata = []; // data in database table form (must contain a column "_used");
    this.listdatafiltered = []; // data in database table form
    this.nestdatafiltered = []; // data in nested form
};
d3_data.prototype.add_nestkey = function(key_I){
    //closure to add additional nest keys within a loop
    return function(d){
        return d[key_I];
    };
}
d3_data.prototype.convert_list2nestlist = function (data_I,key_I,rollup_I) {
    // convert a list of objects to a d3 nest by a key
    var add_nestkey = this.add_nestkey;
    var nesteddata_O = d3.nest();
    for (var i=0;i<key_I.length;i++){
        nesteddata_O = nesteddata_O.key(add_nestkey(key_I[i]));
    };
    if (rollup_I){nesteddata_O = nesteddata_O.rollup(rollup_I)};
    nesteddata_O = nesteddata_O.entries(data_I);
    return nesteddata_O;
};
d3_data.prototype.convert_list2nestmap = function (data_I,key_I) {
    // convert a list of objects to a d3 nest by a key
    var nesteddata_O = d3.nest()
        .key(function (d) { return d[key_I]; })
        //.rollup()
        .map(data_I);
    return nesteddata_O;
};
d3_data.prototype.filter_stringdata = function () {
    // apply filters to listdata

    var listdatacopy = this.listdata;
    var listdatafiltered_O = [];
    
    //set _used to false:
    for (var i = 0; i < listdatacopy.length; i++) {
        listdatacopy[i]['used_'] = true;
    };

    //pass each row through the filter
    for (var i = 0; i < listdatacopy.length; i++) {
        for (var filter in this.filters) {
            //console.log(filter);
            if (typeof listdatacopy[i][filter] !== "undefined"){
                var str_compare = listdatacopy[i][filter].toString(); //ensure that the value is a string
                var str_filter = this.filters[filter].join('|');  //breaks for 'mmol*gDCW*hr-1' because * is a regular expression
                if (!str_compare.match(str_filter)) {
                    listdatacopy[i]['used_'] = false;
                };
            };
        };
    };

    // add in the filtered data
    listdatacopy.forEach(function (d) {
        if (d['used_']) {
            listdatafiltered_O.push(d)
        };
    });

    // re-make the nestdatafiltered
    this.listdatafiltered = listdatafiltered_O;
    this.nestdatafiltered = this.convert_list2nestlist(listdatafiltered_O,this.nestkey);

    // update the filters
    this.update_filters();
};
d3_data.prototype.set_listdata = function (listdata_I,nestkey_I) {
    // set list data and initialize filtered data
    this.nestkey = nestkey_I;
    this.listdata = listdata_I;
    this.listdatafiltered = listdata_I;
    this.nestdatafiltered = this.convert_list2nestlist(listdata_I,this.nestkey);
};
d3_data.prototype.set_keys = function (keys_I) {
    // add list data
    this.keys = keys_I;
};
d3_data.prototype.reset_filters = function () {
    // generate the initial filter

    var filters = {};
    for (var key_cnt = 0; key_cnt < this.keys.length;key_cnt++) {
        var colentries = d3.set();
        for (var i = 0; i < this.listdata.length; i++) {
            colentries.add(this.listdata[i][this.keys[key_cnt]]);
        };
        filters[this.keys[key_cnt]] = colentries.values();
    };
    this.filters = filters;
};
d3_data.prototype.update_filters = function () {
    // update the filter based on the current filtered data

    var filters = {};
    for (var key_cnt = 0; key_cnt < this.keys.length;key_cnt++) {
        var colentries = d3.set();
        for (var i = 0; i < this.listdatafiltered.length; i++) {
            colentries.add(this.listdatafiltered[i][this.keys[key_cnt]]);
        };
        filters[this.keys[key_cnt]] = colentries.values();
    };
    this.filters = filters;
};
d3_data.prototype.clear_data = function () {
    // add list data
    this.listdata = [];
    this.listdatafiltered = [];
    this.nestdatafiltered = [];
};
d3_data.prototype.change_filters = function (filter_I) {
    // modify the filter according to the new filter
    
    for (var key in filter_I) {
        this.filters[key] = filter_I[key];
    };
};
d3_data.prototype.format_keyvalues2namechildren = function(lastchild_I){
    // format nest key/values to name/children for use with layouts and clusters
    function rename(d){
        if (d.key){
            d['name']=d.key;
            delete d.key;
        } else {
            lastchild = d[lastchild_I];
            for(var key in d){delete d[key];}; //remove all object properties
                                           //needed for proper rendering of data for d3 layouts
            d['name']=lastchild;
        };
        if (d.values){
            d['children'] = d.values;
            d['children'].forEach(rename);
            delete d.values;
        };
    };
    this.nestdatafiltered.forEach(rename)
};
d3_data.prototype.convert_filter2stringmenuinput = function(){
    // convert filter list to filter string list
    var filterstring = [];
    for (var key in this.filters){
        filterstring.push({"text":key,"value":this.filters[key].toString()});
        };
    return filterstring;
};
d3_data.prototype.convert_stringmenuinput2filter = function(filterstring_I){
    // convert filter list to filter string list
    var filtermap = {};
    for (var i=0;i<filterstring_I.length;i++){
        //this.filters[filterstring_I[i].text]=filterstring_I[i].value.split(",");
        filtermap[filterstring_I[i].text]=filterstring_I[i].value.split(",");
    };
    this.change_filters(filtermap)
};
d3_data.prototype.change_nestkeys = function(nestkey_I) {
    // change the nest keys and update nestdatafiltered
    this.nestkey = nestkey_I;
    var listdatafiltered = this.listdatafiltered;
    this.nestdatafiltered = this.convert_list2nestlist(listdatafiltered,nestkey_I);
};