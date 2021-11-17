// on click make a pop-out for the notes
$(document).ready(function(){
    $('[data-toggle="popover"]').popover({               /* This creates and controls popover for course notes. */
        placement : 'top',
        html : true,
        trigger : 'focus',
        title : 'Course Notes <a href="#" class="close" data-dismiss="alert">&times;</a>'
      });

    $(document).on("click", ".popover .close" , function(){
        $('[data-toggle="popover"]').parents(".popover").popover('hide');
    });

    $('[data-toggle="tooltip"]').tooltip({              /* This creates and controls a tooltip for editActiveCourses */
      placement : 'top'
    })
});
