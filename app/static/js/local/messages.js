// Fade out success messages after 5 seconds; error messages stay until closed
setTimeout(function() {
  $(".alert.auto-dismiss").fadeOut(500, function() { $(this).remove(); });
}, 5000);
