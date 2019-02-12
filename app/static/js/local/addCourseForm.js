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



const element = document.getElementById("createCourseForm");
if(element.addEventListener){
    element.addEventListener("submit", callback, false);  //Modern Browsers
}else if(element.attachEvent){
    element.attachEvent('onsubmit', callback);
}
function callback(e){
    e.preventDefault();
    const values =   $('#crossListSelect').val();//document.getElementById("crossListSelect").value;
    console.log(values);
    if(values.length > 0){
        document.getElementById("crossListed").value = 1;
    }
    else{
        document.getElementById("crossListed").value = 0;
    }
    element.submit();
}


function callme(event){
    //const values =  document.getElementById("crossListSelect")
    //const vals = values.options[values.selectedIndex].text;
    //console.log(vals);
    console.log("TODO");
}