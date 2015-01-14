function convert_experiment_id_id(experiment_id_id) {
    var parts = experiment_id_id.split('/');
    return parts[1];
}
function convert_experiment_type_id(experiment_type_id) {
    var parts = experiment_type_id.split('/');
    return parts[3];
}
function convert_template_id(template_id) {
    var parts = template_id.split('/');
    return parts[5];
}
function convert_data_id(data_id) {
    var parts = data_id.split('/');
    return parts[7];
}
function submit() {
    var experiment_id_value = d3.select('#experiment_ids').node().value,
    template_value = d3.select('#templates').node().value,
	experiment_type_value = d3.select('#experiment_types').node().value,
	data_value = d3.select('#data_ids').node().value,
	add = [],
	url;
    if (experiment_id_value != 'none')
        add.push('experiment_id_name=' + convert_experiment_id_id(experiment_id_value));
    if (experiment_type_value != 'none')
        add.push('experiment_type_name=' + convert_experiment_type_id(experiment_type_value));
    if (template_value != 'none')
	    add.push('template_name=' + convert_template_id(template_value));
    if (data_value != 'none')
        add.push('data_name=' + convert_data_id(data_value));

    //if (options_value == 'local_viewer') {
    //    url = 'local/viewer.html';
    //} else if (options_value == 'local_builder') {
    //    url = 'local/builder.html';
    //} else if (options_value == 'viewer') {
    //    url = 'viewer.html';
    //} else {
    //    url = 'builder.html';
    //}

    url = 'data.html';
    url += '?';
    for (var i = 0, l = add.length; i < l; i++) {
        if (i > 0) url += '&';
        url += add[i];
    }
    window.location.href = url;
}

function draw_experiment_types_select(data) {
    /* Draw the experiment_types selector.*/

    var filter_experiment_types = function (experiment_type_id) {
        var org = d3.select('#experiment_ids').node().value;
        if (org == 'all')
            return true;
        if (org.split('/')[1] == experiment_type_id.split('/')[1])
            return true;
        return false;
    };

    var experiment_type_data = data.experiment_type.filter(filter_experiment_types),
	experiment_types_select = d3.select('#experiment_types'),
	experiment_types = experiment_types_select.selectAll('.experiment_type')
	    .data(experiment_type_data).classed('experiment_type', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var experiment_type = d.split('/')[3];
	    return experiment_type;
	});
    experiment_types.enter()
	.append('option')
	.classed('experiment_type', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var experiment_type = d.split('/')[3];
	    return experiment_type;
	});
    experiment_types.exit().remove();

    var n = experiment_types_select.node();
    if (experiment_type_data.length > 0 && n.selectedIndex == 0)
        n.selectedIndex = 1;
}
function draw_templates_select(data) {
    /* Draw the templates selector.*/
    
    var filter_templates = function (template_id) {
        // filter by experiment_ids
        var org = d3.select('#experiment_ids').node().value;
        // filter by experiment_type
        var type = d3.select('#experiment_types').node().value;
        if (org == 'all' && type == 'all')
            return true;
        if (org.split('/')[1] == template_id.split('/')[1] && type == 'all')
            return true;
        if (org == 'all' && type.split('/')[3] == template_id.split('/')[3])
            return true;
        if (org.split('/')[1] == template_id.split('/')[1] && type.split('/')[3] == template_id.split('/')[3])
            return true;
        return false;
    };

    var template_data = data.template.filter(filter_templates),
	templates_select = d3.select('#templates'),
	templates = templates_select.selectAll('.template')
	    .data(template_data).classed('template', true)
	    .attr('value', function (d) { return d; })
	    .text(function (d) {
	        var template = d.split('/')[5];
	        return template;
	});
    templates.enter()
	.append('option')
	.classed('template', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var template = d.split('/')[5];
	    return template;
	});
    templates.exit().remove();

    var n = templates_select.node();
    if (template_data.length > 0 && n.selectedIndex == 0)
        n.selectedIndex = 1;
}
function draw_data_ids_select(data) {
    /* Draw the data_ids selector.*/

    var filter_data_ids = function (data_id_id) {
        // filter by experiment_ids
        var org = d3.select('#experiment_ids').node().value;
        // filter by experiment_type
        var type = d3.select('#experiment_types').node().value;
        // filter by template
        var templ = d3.select('#templates').node().value;
        if (org == 'all' && type == 'all' && templ == 'all')
            return true;
        if (org.split('/')[1] == data_id_id.split('/')[1] && type == 'all' && templ == 'all')
            return true;
        if (org == 'all' && type.split('/')[3] == data_id_id.split('/')[3] && templ == 'all')
            return true;
        if (org == 'all' && type == 'all' && templ.split('/')[5] == data_id_id.split('/')[5])
            return true;
        if (org.split('/')[1] == data_id_id.split('/')[1] && type == 'all' && templ.split('/')[5] == data_id_id.split('/')[5])
            return true;
        if (org.split('/')[1] == data_id_id.split('/')[1] && type.split('/')[3] == data_id_id.split('/')[3] && templ == 'all')
            return true;
        if (org.split('/')[1] == data_id_id.split('/')[1] && type.split('/')[3] == data_id_id.split('/')[3] && templ.split('/')[5] == data_id_id.split('/')[5])
            return true;
        return false;
    };

    var data_id_data = data.data_id.filter(filter_data_ids),
	data_ids_select = d3.select('#data_ids'),
	data_ids = data_ids_select.selectAll('.data_id')
	    .data(data_id_data)
	    .classed('data_id', true)
	    .attr('value', function (d) { return d; })
	    .text(function (d) {
	        var data_id = d.split('/')[7]
	        return data_id;
	    });
    data_ids.enter()
	.append('option')
	.classed('data_id', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var data_id = d.split('/')[7]
	    return data_id;
	});
    data_ids.exit().remove();

    var n = data_ids_select.node();
    if (data_id_data.length > 0 && n.selectedIndex == 0)
        n.selectedIndex = 1;
}
function draw_experiment_ids_select(data) {
    var experiment_id = d3.select('#experiment_ids').selectAll('.experiment_id')
	    .data(data.experiment_id);
    experiment_id.enter()
	.append('option')
	.classed('experiment_id', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var parts = d.split('/').slice(-1)[0].split('_');
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
	});
}

function setup() {
    // GO
    draw_experiment_ids_select(data);
    draw_experiment_types_select(data);
    draw_templates_select(data);
    draw_data_ids_select(data);

    // update filters
    d3.select('#experiment_ids')
	.on('change', function () {
	    draw_experiment_ids_select(data);
	    draw_experiment_types_select(data);
	    draw_templates_select(data);
	    draw_data_ids_select(data);
	    //d3.select('#experiment_types').node().value = 'None';
	    //d3.select('#templates').node().value = 'None';
	    //d3.select('#data_ids').node().value = 'None';
	});

    // update filters
    d3.select('#experiment_types')
	.on('change', function () {
	    draw_experiment_ids_select(data);
	    draw_experiment_types_select(data);
	    draw_templates_select(data);
	    draw_data_ids_select(data);
	    //d3.select('#templates').node().value = 'None';
	    //d3.select('#data_ids').node().value = 'None';
	});

    // update filters
    d3.select('#templates')
	.on('change', function () {
	    draw_experiment_ids_select(data);
	    draw_experiment_types_select(data);
	    draw_templates_select(data);
	    draw_data_ids_select(data);
	    //d3.select('#data_ids').node().value = 'None';
	});

    // update filters
    d3.select('#data_ids')
	.on('change', function () {
	    draw_experiment_ids_select(data);
	    draw_experiment_types_select(data);
	    draw_templates_select(data);
	    draw_data_ids_select(data);
	});
    //// make it a builder with a experiment_type, and vice-versa
    //d3.select('#experiment_types')
	//.on('change', function () {
	//    var is_none = this.value == 'none';
	//    d3.select('#tools').selectAll('.tool')
	//	.attr('disabled', function () {
	//	    if (is_none || this.value.indexOf('viewer') == -1)
	//	        return null;
	//	    return true;
	//	});
	//    // make sure a disabled option is not selected
	//    var n = d3.select('#tools').node();
	//    if (!is_none && n.value.indexOf('viewer') != -1) {
	//        n.selectedIndex = n.selectedIndex + 1;
	//    }
	//});

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
