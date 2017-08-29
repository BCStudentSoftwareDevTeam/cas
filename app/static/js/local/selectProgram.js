/*global $ */
$(window).on('load',function(){
    $('#selectProgramModal').modal('show');
});


function redirectCourses(){
    console.log("I am not sure what is happening!")
    var prefix= document.getElementById("programInfo").value
    window.location.replace("/courses/"+prefix+"/")
}
