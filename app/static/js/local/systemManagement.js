//Checks whether there is currently an admin selected and enables/disables remove button accordingly
function updateFormEnabled1() {
    if (verifyAdmin1()) {
        $('#adminAdd').prop('disabled', false);
    } else {
        $('#adminAdd').prop('disabled', true);
    }
}
function verifyAdmin1() {
    if ($('#adminPicker1').val() != "None") {
        return true;
    } else {
        return false
    }
}
function updateFormEnabled() {
    if (verifyAdmin()) {
        $('#adminRemove').prop('disabled', false);
    } else {
        $('#adminRemove').prop('disabled', true);
    }
}
function verifyAdmin() {
    if ($('#adminPicker').val() != "None") {
        return true;
    } else {
        return false
    }
}
$('#adminPicker').change(updateFormEnabled);
$('#adminPicker1').change(updateFormEnabled1);
window.onload=updateFormEnabled();
window.onload=updateFormEnabled1();
$( function() {
    $( "#datepicker" ).datepicker();
  } );

// Changes the text and post action in the modal based on the selected state 
function changeModalText(state, termcode){
    if (state == "locked"){
        $("#modalTitleText").text("Lock this term?")
        $("#modalBodyText").html("Are you sure you want to <b>lock</b> submissions for this term?")
        $("#modalForm").attr('action',"/editTerm/locked")
    }
    else if (state == "tracking"){
        $("#modalTitleText").text("Track this term's changes?")
        $("#modalBodyText").html("Are you sure you want to <b>track</b> submissions for this term?")
        $("#modalForm").attr('action',"/editTerm/tracking")
    }
    else{
        $("#modalTitleText").text("Open this term?")
        $("#modalBodyText").html("Are you sure you want to <b>open</b> submissions for this term?")
        $("#modalForm").attr('action',"/editTerm/open")
    }
    $("#termCode").prop("value",termcode)
}
// Activate the tooltips and modals
$(document).ready(function(){
        $('[data-tooltip="true"]').tooltip({trigger:"hover"}); 
        $('[data-toggle="modal"]').modal({show:false}); 
});


