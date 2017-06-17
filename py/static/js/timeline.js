/* global $, d3 */

var Timeline = function() {
};

var loadTimeline = function(responses) {
  var svgContainer = d3.select('#timeline').append('p').text('Nothing on the timeline, yet.');
};

if (username != '') {
  $.getJSON('/app/api/timeline/' + username, null, loadTimeline);
}
