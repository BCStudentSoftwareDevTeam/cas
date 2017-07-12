/*global $ */
$(window).on('load',function(){
    $('#selectTermModal').modal('show');
});


function redirectCourses(prefix){
    var termCode = document.getElementById("termInfo").value
    window.location.replace("/courses/"+termCode+"/" + prefix)
}
