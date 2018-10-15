/*global $ */
$(window).on('load',function(){
    $('#selectTermModal').modal('show');
});


function redirectCourses(pref){
    var termCode = document.getElementById("termInfo").value
    window.location.replace("/courses/"+termCode+"/" + pref)
}
function redirectTerm(){
    var termCode = document.getElementById("termInfo").value
    window.location.replace("/roomResolution/"+termCode)
}