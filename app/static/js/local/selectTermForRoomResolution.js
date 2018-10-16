/*global $ */
$(window).on('load',function(){
    $('#selectTermModal').modal('show');
});


function redirectRP(){
    var termCode = document.getElementById("termInfo").value
    window.location.replace("/roomResolution/"+termCode)
}
