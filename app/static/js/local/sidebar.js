/* global $ */

$(document).ready(function(){
   $('.first-level').on('click', function(){
      $(this).children().toggleClass('glyphicon-chevron-down');
      $(this).children().toggleClass('glyphicon-chevron-up');
   
   })
   

   $('#divisionSelect').on('change', function(){
      let hrefs = JSON.parse($('#divisionSelect').data('hrefs').replace(/'/g, '"'))
      window.location.href = hrefs[$('#divisionSelect').val()]
   })
})

