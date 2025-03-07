function draw_svg(container_id, margin, width, height) {
    svg = d3.select("#" + container_id)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    return svg;
}

function draw_axes(plot_name, svg, width, height, domainx, domainy, x_discrete) {
    var x_scale = d3.scaleLinear().domain(domainx).range([0, width]);
    var y_scale = d3.scaleLinear().domain(domainy).range([height, 0]);

    svg.append("g").attr("class", plot_name + "-xaxis").attr("transform", "translate(0," + height + ")").call(d3.axisBottom(x_scale));
    svg.append("g").attr("class", plot_name + "-yaxis").call(d3.axisLeft(y_scale));

    return { 'x': x_scale, 'y': y_scale };
}

function draw_slider(column, min, max, scatter_svg, scatter2_svg, scatter_scale, scatter2_scale){
    slider = document.getElementById(column+'-slider')
    noUiSlider.create(slider, {
      start: [min, max],
      connect: false,
          tooltips: true,
      step: 1,
      range: {'min': min, 'max': max}
    });
    // slider.noUiSlider.on('change', function(){
    //     update(scatter_svg, scatter2_svg, scatter_scale, scatter2_scale)
    // });
}

// extracts the selected days and minimum/maximum values for each slider
function get_params(){
    var ea = [];
    var pt = [];
    var cgpa = [0, 0]
    var internships = [0, 0]
    var projects = [0, 0]
    var wc = [0, 0]
    var ats = [0, 0]
    var ssr = [0, 0]
    
    document.querySelectorAll('#ExtracurricularActivities').forEach(function(radio){
        ea.push(radio.value);
    });
    document.querySelectorAll('#PlacementTraining').forEach(function(radio){
        pt.push(radio.value);
    });

    var cgpaSlider = document.getElementById('cgpa-slider');
    if (cgpaSlider && cgpaSlider.noUiSlider) {
        cgpa = cgpaSlider.noUiSlider.get().map(Number);
    }
    var internshipsSlider = document.getElementById('internships-slider');
    if (internshipsSlider && internshipsSlider.noUiSlider) {
        internships = internshipsSlider.noUiSlider.get().map(Number);
    }
    var projectsSlider = document.getElementById('projects-slider');
    if (projectsSlider && projectsSlider.noUiSlider) {
        projects = projectsSlider.noUiSlider.get().map(Number);
    }
    var wcSlider = document.getElementById('wc-slider');
    if (wcSlider && wcSlider.noUiSlider) {
        wc = wcSlider.noUiSlider.get().map(Number);
    }
    var atsSlider = document.getElementById('ats-slider');
    if (atsSlider && atsSlider.noUiSlider) {
        ats = atsSlider.noUiSlider.get().map(Number);
    }
    var ssrSlider = document.getElementById('ssr-slider');
    if (ssrSlider && ssrSlider.noUiSlider) {
        ssr = ssrSlider.noUiSlider.get().map(Number);
    }

    return {'ea': ea, 'pt': pt, 'cgpa': cgpa, 'internships': internships, 
        'projects': projects, 'wc': wc, 'ats': ats, 'ssr': ssr}
}

function draw_scatter(data, svg, scale) {
    svg.selectAll("circle").remove();

    svg.selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => scale.x(d.X))
        .attr("cy", d => scale.y(d.Y))
        .attr("r", 5)
        .style("fill", "darkred")
        .style("stroke", "black");
}

function update() {
    fetch('/update', {
        method: 'POST',
        body: JSON.stringify({}),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        draw_scatter(data['scatter1_data'], scatter1_svg, scatter1_scale);
        draw_scatter(data['scatter2_data'], scatter2_svg, scatter2_scale);
    })
    .catch(error => console.error("Error:", error));
}
