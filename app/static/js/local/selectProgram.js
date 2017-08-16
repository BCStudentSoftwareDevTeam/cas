/*global $ */
$(window).on('load',function(){
    $('#selectProgramModal').modal('show');
});


function redirectCourses(){
    console.log("I am not sure what is happening!")
    var pid = document.getElementById("programInfo").value
    console.log(pid)
    window.location.replace("/courses/"+pid+"/")
}
