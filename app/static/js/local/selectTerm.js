/*global $ */
$(window).on('load',function(){
    $('#selectTermModal').modal('show');
});


//Test last visited when empyt
//fix redirect for else
// remove the random print on the html that says CSC

function redirectCourses(prefix){
    var termCode = document.getElementById("termInfo").value
    console.log("The function is being used.")
    if (prefix !== null){
        var href = "/courses/termCode/" + prefix
        console.log(href)
        window.location.replace("/courses/"+ termCode +"/"+ prefix)
    }
    else{
        window.location("/courses/termCode/MAT")
    }
}