/* global $ */

var Timeline = function() {
};

var loadTimeline = function(responses) {
  let timeline = $('#timeline');
  for (let i = 0; i < responses.length; ++i) {
    let response = responses[i];
    let div = $('<div/>').appendTo(timeline);;
    $('<a/>').attr('href', response.url).text(response.created).appendTo(div);
    $('<p/>').html(response.a).appendTo(div);
  }
};

if (username != '') {
  $.getJSON('/app/api/timeline/' + username, null, loadTimeline);
}
