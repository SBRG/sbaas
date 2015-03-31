function convert_time_point_id(time_point_id) {
    var parts = time_point_id.split('/');
    return parts[1];
}
function convert_concentration_unit_id(concentration_unit_id) {
    var parts = concentration_unit_id.split('/');
    return parts[3];
}
function convert_component_id(component_id) {
    var parts = component_id.split('/');
    return parts[5];
}
function convert_score_loading_id(score_loading_id) {
    var parts = score_loading_id.split('/');
    return parts[7];
}
function submit() {
    var time_point_value = d3.select('#time_points').node().value,
    component_value = d3.select('#components').node().value,
	concentration_unit_value = d3.select('#concentration_units').node().value,
	score_loading_value = d3.select('#score_loadings').node().value,
	add = [],
	url;
    if (time_point_value != 'none')
        add.push('time_point_name=' + convert_time_point_id(time_point_value));
    if (concentration_unit_value != 'none')
        add.push('concentration_unit_name=' + convert_concentration_unit_id(concentration_unit_value));
    if (component_value != 'none')
	    add.push('component_name=' + convert_component_id(component_value));
    if (score_loading_value != 'none')
	add.push('score_loading_name=' + convert_score_loading_id(score_loading_value));

    parts = window.location.href.split('&time_point_name=');
    url = parts[0];
    url += '&';
    for (var i = 0, l = add.length; i < l; i++) {
        if (i > 0) url += '&';
        url += add[i];
    }
    window.location.href = url;
}

function draw_concentration_units_select(data) {
    /* Draw the concentration_units selector.*/

    var filter_concentration_units = function (concentration_unit_id) {
        var org = d3.select('#time_points').node().value;
        if (org == 'all')
            return true;
        if (org.split('/')[1] == concentration_unit_id.split('/')[1])
            return true;
        return false;
    };

    var concentration_unit_data = data.concentration_unit.filter(filter_concentration_units),
	concentration_units_select = d3.select('#concentration_units'),
	concentration_units = concentration_units_select.selectAll('.concentration_unit')
	    .data(concentration_unit_data).classed('concentration_unit', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var concentration_unit = d.split('/')[3];
	    return concentration_unit;
	});
    concentration_units.enter()
	.append('option')
	.classed('concentration_unit', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var concentration_unit = d.split('/')[3];
	    return concentration_unit;
	});
    concentration_units.exit().remove();

    var n = concentration_units_select.node();
    if (concentration_unit_data.length > 0 && n.selectedIndex == 0)
        n.selectedIndex = 1;
}
function draw_components_select(data) {
    /* Draw the components selector.*/
    
    var filter_components = function (component_id) {
        // filter by time_points
        var org = d3.select('#time_points').node().value;
        // filter by concentration_unit
        var type = d3.select('#concentration_units').node().value;
        if (org == 'all' && type == 'all')
            return true;
        if (org.split('/')[1] == component_id.split('/')[1] && type == 'all')
            return true;
        if (org == 'all' && type.split('/')[3] == component_id.split('/')[3])
            return true;
        if (org.split('/')[1] == component_id.split('/')[1] && type.split('/')[3] == component_id.split('/')[3])
            return true;
        return false;
    };

    var component_data = data.component.filter(filter_components),
	components_select = d3.select('#components'),
	components = components_select.selectAll('.component')
	    .data(component_data).classed('component', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var component = d.split('/')[5];
	    return component;
	});
    components.enter()
	.append('option')
	.classed('component', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var component = d.split('/')[5];
	    return component;
	});
    components.exit().remove();

    var n = components_select.node();
    if (component_data.length > 0 && n.selectedIndex == 0)
        n.selectedIndex = 1;
}
function draw_score_loadings_select(data) {
    /* Draw the score_loadings selector.*/

    var filter_score_loadings = function (score_loading_id) {
        // filter by time_points
        var org = d3.select('#time_points').node().value;
        // filter by concentration_unit
        var type = d3.select('#concentration_units').node().value;
        // filter by component
        var templ = d3.select('#components').node().value;
        if (org == 'all' && type == 'all' && templ == 'all')
            return true;
        if (org.split('/')[1] == score_loading_id.split('/')[1] && type == 'all' && templ == 'all')
            return true;
        if (org == 'all' && type.split('/')[3] == score_loading_id.split('/')[3] && templ == 'all')
            return true;
        if (org == 'all' && type == 'all' && templ.split('/')[5] == score_loading_id.split('/')[5])
            return true;
        if (org.split('/')[1] == score_loading_id.split('/')[1] && type == 'all' && templ.split('/')[5] == score_loading_id.split('/')[5])
            return true;
        if (org.split('/')[1] == score_loading_id.split('/')[1] && type.split('/')[3] == score_loading_id.split('/')[3] && templ == 'all')
            return true;
        if (org.split('/')[1] == score_loading_id.split('/')[1] && type.split('/')[3] == score_loading_id.split('/')[3] && templ.split('/')[5] == score_loading_id.split('/')[5])
            return true;
        return false;
    };

    var score_loading_data = data.score_loading.filter(filter_score_loadings),
	score_loadings_select = d3.select('#score_loadings'),
	score_loadings = score_loadings_select.selectAll('.score_loading')
	    .data(score_loading_data).classed('score_loading', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var score_loading = d.split('/')[7]
	    return score_loading;
	});
    score_loadings.enter()
	.append('option')
	.classed('score_loading', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var score_loading = d.split('/')[7]
	    return score_loading;
	});
    score_loadings.exit().remove();

    var n = score_loadings_select.node();
    if (score_loading_data.length > 0 && n.selectedIndex == 0)
        n.selectedIndex = 1;
}
function draw_time_points_select(data) {
    var time_point = d3.select('#time_points').selectAll('.time_point')
	    .data(data.time_point).classed('time_point', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var parts = d.split('/').slice(-1)[0].split('_');
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
	});
    time_point.enter()
	.append('option')
	.classed('time_point', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var parts = d.split('/').slice(-1)[0].split('_');
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
	});
}

function setup(data) {
    // GO
    draw_time_points_select(data);
    draw_concentration_units_select(data);
    draw_components_select(data);
    draw_score_loadings_select(data);

    // update filters
    d3.select('#time_points')
	.on('change', function () {
	    draw_concentration_units_select(data);
	    draw_components_select(data);
	    draw_score_loadings_select(data);
	});

    // update filters
    d3.select('#concentration_units')
	.on('change', function () {
	    draw_time_points_select(data);
	    draw_concentration_units_select(data);
	    draw_components_select(data);
	    draw_score_loadings_select(data);
	});

    // update filters
    d3.select('#components')
	.on('change', function () {
	    draw_time_points_select(data);
	    draw_concentration_units_select(data);
	    draw_components_select(data);
	    draw_score_loadings_select(data);
	});

    // update filters
    d3.select('#score_loadings')
	.on('change', function () {
	    draw_time_points_select(data);
	    draw_concentration_units_select(data);
	    draw_components_select(data);
	    draw_score_loadings_select(data);
	});
    //// make it a builder with a concentration_unit, and vice-versa
    //d3.select('#concentration_units')
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
