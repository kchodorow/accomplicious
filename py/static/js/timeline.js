/* global $, d3 */

var Timeline = function() {
};

var svg = d3.select('svg');
var width = svg.attr("width");
var height = svg.attr("height");
var simulation = d3.forceSimulation()
      .force("link", d3.forceLink().id(function(d) { return d.id; }))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2));

var loadTimeline = function(responses) {
  if (responses.length == 0) {
    svg.append('p').text('Nothing on the timeline, yet.');
    return;
  }
  var graph = {links : [], nodes : []};
  for (let i = 0; i < responses.length; ++i) {
    var a = responses[i];
    graph.nodes.push({id : i, group : 1, value : a.a});
    if (i > 0) {
      graph.links.push({source : i - 1, target : i, value : 16});
    }
  }

  var color = d3.scaleOrdinal(d3.schemeCategory20);

  var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
        .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

  var nodeGroups = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(graph.nodes)
        .enter();
  var node = nodeGroups.append("circle")
        .attr("r", 5)
        .attr("fill", function(d) { return color(d.group); })
        .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));

  var text = nodeGroups.append("text")
        .text(function(d) { return d.value; });

  simulation
    .nodes(graph.nodes)
    .on("tick", ticked);

  simulation.force("link")
    .links(graph.links);

  function ticked() {
    link
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

    node
      .attr("cx", function(d) { return d.x - 10; })
      .attr("cy", function(d) { return d.y - 5; });
    text
      .attr("x", function(d) { return d.x; })
      .attr("y", function(d) { return d.y; });
  }
};

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

if (username != '') {
  $.getJSON('/app/api/timeline/' + username, null, loadTimeline);
}
