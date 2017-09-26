/*global $ */
$(window).on('load',function(){
    $('#selectProgramModal').modal('show');
});


function redirectCourses(){
    var prefix= document.getElementById("programInfo").value
    window.location.replace("/courses/"+prefix+"/")
}

function redirecthome(){
    window.location.href = "/"
    console.log("redirect")
}
