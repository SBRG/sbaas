function convert_model_id_id(model_id_id) {
    var parts = model_id_id.split('/');
    return parts[1];
}
function convert_mapping_id_id(mapping_id_id) {
    var parts = mapping_id_id.split('/');
    return parts[3];
}
function convert_sample_id(sample_id) {
    var parts = sample_id.split('/');
    return parts[5];
}
function convert_map_id_id(map_id_id) {
    var parts = map_id_id.split('/');
    return parts[7];
}
function submit() {
    var model_id_value = d3.select('#model_ids').node().value,
    sample_value = d3.select('#samples').node().value,
	mapping_id_value = d3.select('#mapping_ids').node().value,
	map_id_value = d3.select('#map_ids').node().value,
	add = [],
	url;
    if (model_id_value != 'none')
        add.push('model_id_name=' + convert_model_id_id(model_id_value));
    if (mapping_id_value != 'none')
        add.push('mapping_id_name=' + convert_mapping_id_id(mapping_id_value));
    if (sample_value != 'none')
	add.push('sample_name=' + convert_sample_id(sample_value));
    if (map_id_value != 'none')
        add.push('map_id_name=' + convert_map_id_id(map_id_value));

    parts = window.location.href.split('&model_id_name=');
    url = parts[0];
    url += '&';
    for (var i = 0, l = add.length; i < l; i++) {
        if (i > 0) url += '&';
        url += add[i];
    }
    window.location.href = url;
}

function draw_mapping_ids_select(data) {
    /* Draw the mapping_ids selector.*/

    var filter_mapping_ids = function (mapping_id_id) {
        var org = d3.select('#model_ids').node().value;
        if (org == 'all')
            return true;
        if (org.split('/')[1] == mapping_id_id.split('/')[1])
            return true;
        return false;
    };

    var mapping_id_data = data.mapping_id.filter(filter_mapping_ids),
	mapping_ids_select = d3.select('#mapping_ids'),
	mapping_ids = mapping_ids_select.selectAll('.mapping_id')
	    .data(mapping_id_data).classed('mapping_id', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var mapping_id = d.split('/')[3];
	    return mapping_id;
	});
    mapping_ids.enter()
	.append('option')
	.classed('mapping_id', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var mapping_id = d.split('/')[3];
	    return mapping_id;
	});
    mapping_ids.exit().remove();

    var n = mapping_ids_select.node();
    if (mapping_id_data.length > 0 && n.selectedIndex == 0)
        n.selectedIndex = 1;
}
function draw_samples_select(data) {
    /* Draw the samples selector.*/
    
    var filter_samples = function (sample_id) {
        // filter by model_ids
        var org = d3.select('#model_ids').node().value;
        // filter by mapping_id
        var type = d3.select('#mapping_ids').node().value;
        if (org == 'all' && type == 'all')
            return true;
        if (org.split('/')[1] == sample_id.split('/')[1] && type == 'all')
            return true;
        if (org == 'all' && type.split('/')[3] == sample_id.split('/')[3])
            return true;
        if (org.split('/')[1] == sample_id.split('/')[1] && type.split('/')[3] == sample_id.split('/')[3])
            return true;
        return false;
    };

    var sample_data = data.sample.filter(filter_samples),
	samples_select = d3.select('#samples'),
	samples = samples_select.selectAll('.sample')
	    .data(sample_data).classed('sample', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var sample = d.split('/')[5];
	    return sample;
	});
    samples.enter()
	.append('option')
	.classed('sample', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var sample = d.split('/')[5];
	    return sample;
	});
    samples.exit().remove();

    var n = samples_select.node();
    if (sample_data.length > 0 && n.selectedIndex == 0)
        n.selectedIndex = 1;
}
function draw_map_ids_select(data) {
    /* Draw the map_ids selector.*/

    var filter_map_ids = function (map_id_id) {
        // filter by mapping_ids
        var org = d3.select('#model_ids').node().value;
        // filter by concentration_unit
        var type = d3.select('#mapping_ids').node().value;
        // filter by component
        var templ = d3.select('#samples').node().value;
        if (org == 'all' && type == 'all' && templ == 'all')
            return true;
        if (org.split('/')[1] == map_id_id.split('/')[1] && type == 'all' && templ == 'all')
            return true;
        if (org == 'all' && type.split('/')[3] == map_id_id.split('/')[3] && templ == 'all')
            return true;
        if (org == 'all' && type == 'all' && templ.split('/')[5] == map_id_id.split('/')[5])
            return true;
        if (org.split('/')[1] == map_id_id.split('/')[1] && type == 'all' && templ.split('/')[5] == map_id_id.split('/')[5])
            return true;
        if (org.split('/')[1] == map_id_id.split('/')[1] && type.split('/')[3] == map_id_id.split('/')[3] && templ == 'all')
            return true;
        if (org.split('/')[1] == map_id_id.split('/')[1] && type.split('/')[3] == map_id_id.split('/')[3] && templ.split('/')[5] == map_id_id.split('/')[5])
            return true;
        return false;
    };

    var map_id_data = data.map_id.filter(filter_map_ids),
	map_ids_select = d3.select('#map_ids'),
	map_ids = map_ids_select.selectAll('.map_id')
	    .data(map_id_data).classed('map_id', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var map_id = d.split('/')[7]
	    return map_id;
	});
    map_ids.enter()
	.append('option')
	.classed('map_id', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var map_id = d.split('/')[7]
	    return map_id;
	});
    map_ids.exit().remove();

    var n = map_ids_select.node();
    if (map_id_data.length > 0 && n.selectedIndex == 0)
        n.selectedIndex = 1;
}
function draw_model_ids_select(data) {
    var model_id = d3.select('#model_ids').selectAll('.model_id')
	    .data(data.model_id).classed('model_id', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var parts = d.split('/').slice(-1)[0].split('_');
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
	});
    model_id.enter()
	.append('option')
	.classed('model_id', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var parts = d.split('/').slice(-1)[0].split('_');
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
	});
}

function setup(data_I) {
    // GO
    draw_model_ids_select(data_I);
    draw_mapping_ids_select(data_I);
    draw_samples_select(data_I);
    draw_map_ids_select(data_I);

    // update filters
    d3.select('#model_ids')
	.on('change', function () {
	    draw_mapping_ids_select(data_I);
	    draw_samples_select(data_I);
	    draw_map_ids_select(data_I);
	});

    // update filters
    d3.select('#mapping_ids')
	.on('change', function () {
	    draw_model_ids_select(data_I);
	    draw_mapping_ids_select(data_I);
	    draw_samples_select(data_I);
	    draw_map_ids_select(data_I);
	});

    // update filters
    d3.select('#samples')
	.on('change', function () {
	    draw_model_ids_select(data_I);
	    draw_mapping_ids_select(data_I);
	    draw_samples_select(data_I);
	    draw_map_ids_select(data_I);
	});
    
    // update filters
    d3.select('#map_ids')
	.on('change', function () {
	    draw_model_ids_select(data_I);
	    draw_mapping_ids_select(data_I);
	    draw_samples_select(data_I);
	    draw_map_ids_select(data_I);
	});

    // submit button
    d3.select('#submit').on('click', submit);

    // submit on enter
    var selection = d3.select(window),
	kc = 13;
    selection.on('keydown.' + kc, function () {
        if (d3.event.keyCode == kc) {
            submit();
        }
    });
}
