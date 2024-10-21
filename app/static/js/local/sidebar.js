/* global $ */

$(document).ready(function(){
   $('.first-level').on('click', function(){
      $(this).children().toggleClass('glyphicon-chevron-down');
      $(this).children().toggleClass('glyphicon-chevron-up');
   
   })
   

   $('#divisionSelect').on('change', function(){
      console.log("division select changed")
   })
})

