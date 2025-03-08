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
  // var x_scale = d3.scaleLinear().domain(domainx).range([0, width]);
  var x_scale = x_discrete 
  ? d3.scaleBand()
      .domain(domainx)
      .range([0, width])
      .padding(0.1)  
  : d3.scaleLinear()
      .domain(domainx)
      .range([0, width]);

  var y_scale = d3.scaleLinear().domain(domainy).range([height, 0]);

  svg.append("g").attr("class", plot_name + "-xaxis").attr("transform", "translate(0," + height + ")").call(d3.axisBottom(x_scale));
  svg.append("g").attr("class", plot_name + "-yaxis").call(d3.axisLeft(y_scale));

  return { 'x': x_scale, 'y': y_scale };
}

function draw_slider(column, min, max, scatter_svg, bar_svg, scatter_scale, bar_scale){
  slider = document.getElementById(column+'-slider')
  noUiSlider.create(slider, {
    start: [min, max],
    connect: false,
        tooltips: true,
    step: 1,
    range: {'min': min, 'max': max}
  });
  slider.noUiSlider.on('change', function(){
      update(scatter_svg, bar_svg, scatter_scale, bar_scale)
  });
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
  
  document.querySelectorAll('[name="ExtracurricularActivities"]').forEach(function(radio){
    if(radio.checked){
        ea.push(radio.value);
    }
  });
  document.querySelectorAll('[name="PlacementTraining"]').forEach(function(radio){
    if(radio.checked){
        pt.push(radio.value);
    }
  });
  // document.querySelectorAll('#PlacementStatus').forEach(function(radio){
  //     pt.push(radio.value);
  // });
  
  var cgpaSlider = document.getElementById('CGPA-slider');
  if (cgpaSlider && cgpaSlider.noUiSlider) {
      cgpa = cgpaSlider.noUiSlider.get().map(Number);
  }
  var internshipsSlider = document.getElementById('Internships-slider');
  if (internshipsSlider && internshipsSlider.noUiSlider) {
      internships = internshipsSlider.noUiSlider.get().map(Number);
  }
  var projectsSlider = document.getElementById('Projects-slider');
  if (projectsSlider && projectsSlider.noUiSlider) {
      projects = projectsSlider.noUiSlider.get().map(Number);
  }
  var wcSlider = document.getElementById('Workshops/Certifications-slider');
  if (wcSlider && wcSlider.noUiSlider) {
      wc = wcSlider.noUiSlider.get().map(Number);
  }
  var atsSlider = document.getElementById('AptitudeTestScore-slider');
  if (atsSlider && atsSlider.noUiSlider) {
      ats = atsSlider.noUiSlider.get().map(Number);
  }
  var ssrSlider = document.getElementById('SoftSkillsRating-slider');
  if (ssrSlider && ssrSlider.noUiSlider) {
      ssr = ssrSlider.noUiSlider.get().map(Number);
  }
  var sscSlider = document.getElementById('SSC_Marks-slider');
  if (sscSlider && sscSlider.noUiSlider) {
      ssc = sscSlider.noUiSlider.get().map(Number);
  }
  var hscSlider = document.getElementById('HSC_Marks-slider');
  if (hscSlider && hscSlider.noUiSlider) {
      hsc = hscSlider.noUiSlider.get().map(Number);
  }

  return {'ea': ea, 'pt': pt, 'cgpa': cgpa, 'internships': internships, 
      'projects': projects, 'wc': wc, 'ats': ats, 'ssr': ssr, 'ssc': ssc, 'hsc': hsc};
}

function draw_scatter(data, svg, scale) {
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

function draw_bar(data, svg, scale) {
  svg.selectAll("rect")
      .data(data)
      .enter()
      .append("rect")
      .attr("x", d => scale.x(d.X))
      .attr("y", d => scale.y(d.Y))
      .attr("width", scale.x.bandwidth())
      .attr("height", d => scale.y(0) - scale.y(d.Y))
      .style("fill", "darkred")
      .style("stroke", "black");
}

// removes the old data points and redraws the scatterplot
function update_scatter(data, svg, scale){
  svg.selectAll("circle").remove();
  
  draw_scatter(data, svg, scale);
}

function update_bar(data, svg, scale) {
  svg.selectAll("g").remove();
  svg.selectAll("rect").remove();

  const yMax = d3.max(data, d => d.Y);
  scale.y.domain([0, yMax]);

  draw_bar(data, svg, scale);
}


function update() {
  params = get_params()
  // console.log(params)
  fetch('/update', {
      method: 'POST',
      credentials: 'include',
      body: JSON.stringify(params),
      cache: 'no-cache',
      headers: new Headers({
          'content-type': 'application/json'
      })
  }).then(async function(response){
      var results = JSON.parse(JSON.stringify(await response.json()));
      update_scatter(results['scatter1_data'], scatter1_svg, scatter1_scale);
      update_bar(results['bar_data'], bar_svg, bar_scale);  // Now correctly passing placement_count
  });
}