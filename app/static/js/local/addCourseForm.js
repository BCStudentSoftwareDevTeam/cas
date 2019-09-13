/*global $*/
$("#showForm").click(function() {
   $("#createCourseFormJumbo").css('display', 'block');
   $(this).hide();
});

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



const createCourseForm = document.getElementById("createCourseForm");
if(createCourseForm.addEventListener){
    createCourseForm.addEventListener("submit", callback, false);  //Modern Browsers
}else if(createCourseForm.attachEvent){
    createCourseForm.attachEvent('onsubmit', callback);
}
function callback(e){
  //This is just for rosslisted, but there was a. e.preventdefault that was giving us a bad request on submit or save of special topics courses. (kat n brian 9/13/19)
    if($('#crossListSelect').val() == null){
        document.getElementById("crossListed").value = 0;
    }else{
        document.getElementById("crossListed").value = 1;
    }
    createCourseForm.submit();
}


function callme(event){
    //const values =  document.getElementById("crossListSelect")
    //const vals = values.options[values.selectedIndex].text;
    //console.log(vals);
    console.log("TODO");
}
