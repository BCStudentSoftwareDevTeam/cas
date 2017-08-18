/*global $ */
$(window).on('load',function(){
    $('#selectProgramModal').modal('show');
});


function redirectCourses(){
    console.log("I am not sure what is happening!")
    var pid_or_prefix= document.getElementById("programInfo").value
    window.location.replace("/courses/"+pid_or_prefix+"/")
}
