function convert_feature_id(feature_id) {
    var parts = feature_id.split('/');
    return parts[1];
}
function submit() {
    var feature_value = d3.select('#features').node().value,
	add = [],
	url;
    if (feature_value != 'none')
        add.push('feature_name=' + convert_feature_id(feature_value));

    parts = window.location.href.split('&feature_name=');
    url = parts[0];
    url += '&';
    for (var i = 0, l = add.length; i < l; i++) {
        if (i > 0) url += '&';
        url += add[i];
    }
    window.location.href = url;
}

function draw_features_select(data) {
    var feature = d3.select('#features').selectAll('.feature')
	    .data(data.feature).classed('feature', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var parts = d.split('/').slice(-1)[0].split('_');
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
	});
    feature.enter()
	.append('option')
	.classed('feature', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var parts = d.split('/').slice(-1)[0].split('_');
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
	});
}

function setup(data_I) {
    // GO
    draw_features_select(data_I);

    // update filters
    d3.select('#features')
	.on('change', function () {
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
