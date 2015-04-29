function convert_project_id_id(project_id_id) {
    var parts = project_id_id.split('/');
    return parts[0];
}
function submit() {
    var project_id_value = d3.select('#project_ids').node().value;
    var add = [];

    if (project_id_value != 'none')
        add.push('project_id=' + convert_project_id_id(project_id_value));

    var url = 'project.html';
    url += '?';
    for (var i = 0, l = add.length; i < l; i++) {
        if (i > 0) url += '&';
        url += add[i];
    }
    window.location.href = url;
}
function new_container() {
    url = 'container.html';
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
	    var parts = d.split('/');
	    //return parts[0].toUpperCase() + '. ' + parts[1];
	    return parts[0];
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

    // new_container button
    d3.select('#new').on('click', new_container);

    // new_container on enter
    var selection = d3.select(window),
	kc = 13;
    selection.on('keydown.' + kc, function () {
        if (d3.event.keyCode == kc) {
            new_container();
        }
    });
}
