
function submit() {
    // append the datafile webpage
    var project_id_value = d3.select('#project_ids').node().value
    add = [],
	url;
    if (project_id_value != 'none')
        add.push('project_id_name=' + convert_project_id_id(project_id_value));

    url = 'container.html';
    url += '?';
    for (var i = 0, l = add.length; i < l; i++) {
        if (i > 0) url += '&';
        url += add[i];
    }
    window.location.href = url;

    // append the visualization file to the webpage
} 
function setup() {
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