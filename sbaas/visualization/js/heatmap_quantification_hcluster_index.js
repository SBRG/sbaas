function convert_time_point_id(time_point_id) {
    var parts = time_point_id.split('/');
    return parts[1];
}
function convert_concentration_unit_id(concentration_unit_id) {
    var parts = concentration_unit_id.split('/');
    return parts[3];
}
function submit() {
    var time_point_value = d3.select('#time_points').node().value,
	concentration_unit_value = d3.select('#concentration_units').node().value,
	add = [],
	url;
    if (time_point_value != 'none')
        add.push('time_point_name=' + convert_time_point_id(time_point_value));
    if (concentration_unit_value != 'none')
        add.push('concentration_unit_name=' + convert_concentration_unit_id(concentration_unit_value));

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

function setup(data_I) {
    // GO
    draw_time_points_select(data_I);
    draw_concentration_units_select(data_I);

    // update filters
    d3.select('#time_points')
	.on('change', function () {
	    draw_concentration_units_select(data_I);
	});

    // update filters
    d3.select('#concentration_units')
	.on('change', function () {
	    draw_time_points_select(data_I);
	    draw_concentration_units_select(data_I);
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
