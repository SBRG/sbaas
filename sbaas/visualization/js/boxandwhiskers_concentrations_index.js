function convert_time_point_id(time_point_id) {
    var parts = time_point_id.split('/');
    return parts[1];
}
function convert_feature_id(feature_id) {
    var parts = feature_id.split('/');
    return parts[3];
}
function submit() {
    var time_point_value = d3.select('#time_points').node().value,
	feature_value = d3.select('#features').node().value,
	add = [],
	url;
    if (time_point_value != 'none')
        add.push('time_point_name=' + convert_time_point_id(time_point_value));
    if (feature_value != 'none')
        add.push('feature_name=' + convert_feature_id(feature_value));

    parts = window.location.href.split('&time_point_name=');
    url = parts[0];
    url += '&';
    for (var i = 0, l = add.length; i < l; i++) {
        if (i > 0) url += '&';
        url += add[i];
    }
    window.location.href = url;
}

function draw_features_select(data) {
    /* Draw the features selector.*/

    var filter_features = function (feature_id) {
        var org = d3.select('#time_points').node().value;
        if (org == 'all')
            return true;
        if (org.split('/')[1] == feature_id.split('/')[1])
            return true;
        return false;
    };

    var feature_data = data.feature.filter(filter_features),
	features_select = d3.select('#features'),
	features = features_select.selectAll('.feature')
	    .data(feature_data).classed('feature', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var feature = d.split('/')[3];
	    return feature;
	});
    features.enter()
	.append('option')
	.classed('feature', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var feature = d.split('/')[3];
	    return feature;
	});
    features.exit().remove();

    var n = features_select.node();
    if (feature_data.length > 0 && n.selectedIndex == 0)
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
    draw_features_select(data_I);

    // update filters
    d3.select('#time_points')
	.on('change', function () {
	    draw_time_points_select(data_I);
	    draw_features_select(data_I);
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
