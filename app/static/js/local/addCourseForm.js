/*global $*/
$("#showForm").click(function() {
   $("#createCourseFormJumbo").css('display', 'block');
   $(this).hide();
});

function validateForm()
{
    if ( $(specialTopicCourse).css('display') != 'none' ){
        var btn = $(document.activeElement).attr('id');
        if (btn == "submitAdd")
        {
            var credits = document.getElementById("credits").value;
            var desc = document.getElementById("cd").value;
            var prereqs = document.getElementById("cp").value;
            var majorReqs = document.getElementById("cm").value;
            var concReqs = document.getElementById("cc").value;
            var minorReqs = document.getElementById("cmi").value;
            var perspectives = document.getElementById("cpe").value;
            var valid = true;
            if (credits == '') {
                $("#credits").attr("required", true);
                valid = false;
            }
            if (desc == '') {
                $("#cd").attr("required", true);
                valid = false;
            }
            if (prereqs == '') {
                $("#cp").attr("required", true);
                valid = false;
            }
            if (majorReqs == '') {
                $("#cm").attr("required", true);
                valid = false;
            }
            if (concReqs == '') {
                $("#cc").attr("required", true);
                valid = false;
            }
            if (minorReqs == '') {
                $("#cmi").attr("required", true);
                valid = false;
            }
            if (perspectives == '') {
                $("#cpe").attr("required", true);
                valid = false;
            } 
          return valid;
            }
        else {return true;}
        }
    else
        {
            return true;
        }
    }

$("#hideForm").click(function() {
     $("#createCourseFormJumbo").css('display', 'none');
     $("#showForm").show();
});

var infoLabel = '<div class="form-group col-xs-12 notice alert alert-warning alert-dismissible" role="alert">\
                <p>Choosing a room does not guarantee that the room will assigned</p>\
              </div>';

$("#roomSelect").on('changed.bs.select', function(e) {
 var selectedOption= $('#roomSelect').find(":selected").text();
 console.log(selectedOption)
 if(selectedOption != '---'){
     if(!($('.notice')[0])){
  $("#notesText").before(infoLabel);
     }
 } else {
    $(".notice").remove();
 }
});



    var $window = $(window),
        $forms = $('.offset_input');

    function resize() {
        if ($window.width() < 992) {
            return $forms.removeClass('right');
        }

        $forms.addClass('right');
    }

    $window
        .resize(resize)
        .trigger('resize');

