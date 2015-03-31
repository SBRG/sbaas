function submit() {
    var project_id_value = d3.select('#project_ids').node().value,

	add = [],
	url;
    if (project_id_value != 'none')
        add.push('project_id_name=' + project_id_value);

    url = 'data.html';
    url += '?';
    for (var i = 0, l = add.length; i < l; i++) {
        if (i > 0) url += '&';
        url += add[i];
    }
    window.location.href = url;
}

function draw_project_ids_select(data) {
    var project_id = d3.select('#project_ids').selectAll('.project_id')
	    .data(data.project_id);

    project_id.enter()
	.append('option')
	.classed('project_id', true)
	.attr('value', function (d) { return d; })
	.text(function (d) {
	    return d;
	});
}

function setup() {
    // GO
    draw_project_ids_select(data);

    // update filters
    d3.select('#project_ids')
	.on('change', function () {
	    draw_project_ids_select(data);
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
