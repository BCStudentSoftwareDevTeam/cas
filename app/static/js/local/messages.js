// Fade out flashed messages on their own. Each alert sets its own delay (ms) in
// data-delay so errors and warnings stay on screen longer than success messages.
$(".alert.auto-dismiss").each(function() {
  var alert = $(this);
  var delay = parseInt(alert.data("delay"), 10) || 5000;
  setTimeout(function() {
    alert.fadeOut(500, function() { alert.remove(); });
  }, delay);
});
