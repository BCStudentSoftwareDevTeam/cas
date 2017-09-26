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