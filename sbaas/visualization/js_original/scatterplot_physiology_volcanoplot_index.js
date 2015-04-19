function convert_sample_id(sample_id) {
    var parts = sample_id.split('/');
    return parts[1];
}
function submit() {
    var sample_value = d3.select('#samples').node().value,
	add = [],
	url;
    if (sample_value != 'none')
        add.push('sample_name=' + convert_sample_id(sample_value));

    parts = window.location.href.split('&sample_name=');
    url = parts[0];
    url += '&';
    for (var i = 0, l = add.length; i < l; i++) {
        if (i > 0) url += '&';
        url += add[i];
    }
    window.location.href = url;
}

function draw_samples_select(data) {
    var sample = d3.select('#samples').selectAll('.sample')
	    .data(data.sample).classed('sample', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var parts = d.split('/').slice(-1);
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
	});
    sample.enter()
	.append('option')
	.classed('sample', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    var parts = d.split('/').slice(-1);
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
	});
}

function setup(data_I) {
    // GO
    draw_samples_select(data_I);

    // update filters
    d3.select('#samples')
	.on('change', function () {
	    draw_samples_select(data_I);
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
