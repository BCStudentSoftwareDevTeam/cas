// on click make a pop-out for the notes
$(document).ready(function(){
    $('[data-toggle="popover"]').popover({
        placement : 'bottom',
        animation : false,
        html : true
      });
        
      $(document).on("click", ".popover .close" , function(){
          $(this).parents(".popover").popover('hide');
      });
});
