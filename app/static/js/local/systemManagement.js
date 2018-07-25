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

// for the menus for each term





$(document).on('click', '#btn1', function(){
    console.log("Am I called?");
//   $('.collapse').hide();
  $('#lock_course').collapse('hide');
  $('#open_room').collapse('hide');
  $('#lock_room').collapse('hide');
  $('#assign_room').collapse('hide');
  $('#open_course').collapse('show');
  $('#finish').collapse('hide');
});



$(document).on('click', '#btn2', function(){
  //$('.collapse').collapse('hide');
  $('#lock_course').collapse('show');
  $('#open_room').collapse('hide');
  $('#lock_room').collapse('hide');
  $('#assign_room').collapse('hide');
  $('#open_course').collapse('hide');
  $('#finish').collapse('hide');
});

$(document).on('click', '#btn3', function(){
  //$('.collapse').collapse('hide');
  $('#lock_course').collapse('hide');
  $('#open_room').collapse('show');
  $('#lock_room').collapse('hide');
  $('#assign_room').collapse('hide');
  $('#open_course').collapse('hide');
  $('#finish').collapse('hide');
});

$(document).on('click', '#btn4', function(){
  //$('.collapse').collapse('hide');
  $('#lock_course').collapse('hide');
  $('#open_room').collapse('hide');
  $('#lock_room').collapse('show');
  $('#assign_room').collapse('hide');
  $('#open_course').collapse('hide');
  $('#finish').collapse('hide');
});

$(document).on('click', '#btn5', function(){
  //$('.collapse').collapse('hide');
  $('#lock_course').collapse('hide');
  $('#open_room').collapse('hide');
  $('#lock_room').collapse('hide');
  $('#assign_room').collapse('show');
  $('#open_course').collapse('hide');
  $('#finish').collapse('hide');
});

$(document).on('click', '#btn6', function(){
  //$('.collapse').collapse('hide');
  $('#lock_course').collapse('hide');
  $('#open_room').collapse('hide');
  $('#lock_room').collapse('hide');
  $('#assign_room').collapse('hide');
  $('#open_course').collapse('hide');
  $('#finish').collapse('show');
  $('#archive').collapse('hide');
});


// Shows all the panels to the tab butons
function showPanel(termCode){
    console.log("Term code: " + termCode);
    var targetDiv = $("#divForPanel"+termCode);
    console.log("target div: " + targetDiv);
    var subjectDiv = $("#allPanels");
    console.log("subject div: " + subjectDiv);
    subjectDiv.attr("hidden", false);
    targetDiv.html(subjectDiv);
}

// Disenables all the buttons and then enable one at time in the enableTheOne function
function disableAlltheButtons(){
    var x = document.getElementsByClassName('theButtons'); 
    console.log(x);
    for (var i = 0; i < x.length; i++) {
        x[i].disabled = true
        console.log("Disabled button: " + x[i])
    }
}

// Enables one button
function enableTheOne() {
    console.log(arguments);
    disableAlltheButtons();
    for (var i = 0; i < arguments.length; i++) {
        console.log(arguments[i])
        b = document.getElementById(arguments[i])
        console.log(b)
        b.disabled = false;
        
    }
}

// Adds the color for the completed processes
function prevcolor(btns) { 
        console.log("color changed")
        var remove_color = document.getElementById(btns) //Removes the color as a reult of the result fuction to ensure there is no overide
        remove_color.classList.remove("new_color")
        var prev = document.getElementById(btns)
        prev.className += ' green_btn ';
    
}

// Reverses the color and the state of buttons when one clicks on unlock, applicable for two argumnets only for now uness adjusted
function reverseFunc(btns) {
    disableAlltheButtons(arguments[btns]);
    console.log(arguments[btns]);
    var go_back = document.getElementById(arguments[0]);
    go_back.disabled = false;
    var reverse_color = document.getElementById(arguments[0]);
    reverse_color.className += ' new_color ';
     
}

function change_btn_name(){
    var elem = document.getElementById("Archive");
    if (elem.value=="Archive"){ elem.value = "Unarchive";    $("#myModal .modal-body").text('Are you sure you want to unarchive the term');}

    else if (elem.value == "Unarchive"){ 
    elem.value = "Archive"; 
    elem.disabled=true;
}
    else elem.value = "Archive";
}

// Hides the finish button
$(document).on('click', '#finalize', function(){
  $('#finish').collapse('hide');
});














































































