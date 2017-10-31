/* global $ */
function buildURL(page){
    console.log(page)
    var selectedTerm = document.getElementById('termSelect').value
    if (page == "courseTimeline") {
        var url = '/'.concat(page).concat('/').concat(selectedTerm);
        console.log(url);
    }
    else{
        var url       = '/courseManagement/'.concat(page).concat('/').concat(selectedTerm);
    }
    window.location.replace(url);
}

function getCurrentTerm() {
        var termCode = document.getElementById('termSelect').value
        return termCode
}
    
$(document).ready(function ($) {
    var termCode = getCurrentTerm()
    $("#crossListedLink").attr("href", "/courseManagement/crossListed/" + termCode)
    $("#conflictsLink").attr("href", "/courseManagement/conflicts/" + termCode)
    $("#trackerLink").attr("href", "/courseManagement/tracker/" + termCode)
    $("#courseTimeline").attr("href", "/courseTimeline/" + termCode)
});

