/*global $ */
$(window).on('load',function(){
    $('#selectTermModal').modal('show');
});

var termCode = document.getElementById("termInfo").value
function redirectCourses(prefix){
    console.log("The function is being used.")
    if (lastVisited !== null){
        window.location("/courses/termCode/" + prefix)
    }
    else{
        window.location("/courses/termCode/MAT")
    }
}