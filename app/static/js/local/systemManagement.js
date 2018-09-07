var lastTerm = "";
function showPanel(termCode, button){
    var show_id = button.dataset.target;    // The target panel for the term (e.g., Fall 2018)
    var disable_btn = document.getElementsByClassName("theButtons"); // All of the state buttons 
    disable_btn.disabled = true;            // Disables all the state buttons
    button.disabled = false;                // Disables the term button
    // console.log("Term code: " + termCode);
    var targetDiv = $("#divForPanel"+termCode);  // The target location for the panel (which row to put it under)
    // console.log("target div: " + targetDiv);
    var subjectDiv = $("#allPanels");           // The panel itself, to be moved
    // console.log("subject div: " + subjectDiv);
    // subjectDiv.attr("hidden", false);
    targetDiv.html(subjectDiv);                 // Move the panel
    // Hides all the panels and removes any styling
    for (var i = 0; i <= 7; i++ ){ 
        var build_id = '#order' + i.toString();
        $(build_id).collapse('hide');
        $(build_id).removeAttr("style")

    }
    // console.log(show_id);
    // $(show_id).collapse('show');
    if (lastTerm == "") {               // if this is the first click (no lastTerm set)
        // console.log("First click")
        $(show_id).collapse('show');    // Show the panel for this term
    }
    if (lastTerm != termCode && lastTerm != "") {       // if the lastTerm selected is the same
        // console.log($(show_id).attr('aria-expanded'))
        $(show_id).collapse('show');    // show the target panel for this term
        // console.log($(show_id).attr('aria-expanded'))
        $(show_id).addClass("in");      

        // console.log("Toggling");
    } else {
        $(show_id).collapse('toggle');      // Otherwise, toggle open/closed panel
    }
    // console.log("Last term: ", lastTerm)
    lastTerm = termCode;                // Update lastTerm to the term you're currently on
    // console.log("Last term 2: ", lastTerm)
}

// Disables all the state buttons 
function disableAlltheButtons(){
    var x = document.getElementsByClassName('theButtons'); 
    // console.log(x);
    for (var i = 0; i < x.length; i++) {
        x[i].disabled = true
        // console.log("Disabled button: " + x[i])
    }
}

// Enables one state button
function enableTheOne() {
    // console.log(arguments);
    disableAlltheButtons();
    for (var i = 0; i < arguments.length; i++) {
        // console.log(arguments[i])
        //b = document.getElementById(arguments[i]);           // Grabs the button
        b = $(arguments[i]);
        // console.log("Der button", b);
        b.disabled = false;
    }
}

// Adds the color for the completed processes
function prevcolor(btn) {
    // console.log(btn)
        var allPanelsDiv = $("#allPanels");
        var theTR = allPanelsDiv.parent().parent()[0].id.split("_").pop();
        // console.log(theTR);
        // console.log("color changed");
        // console.log("#"+theTR +" #" +btn);
        var remove_color = $("#"+theTR +" #" +btn); //Removes the color of the previous process to ensure there is no overide
        // console.log(remove_color);
        remove_color.removeClass("btn-dark");
        var prev = $("#"+theTR+" #" + btn);
        prev.addClass('btn-success');
    
}

/** Reverses the color and the state of buttons when one clicks on unlock, 
 * applicable for two argumnets only for now uness adjusted 
 * @params {HTML Buttons} btns - all the buttons
 */
function reverseFunc(btns) {
    // disableAlltheButtons(arguments[btns]);
    // console.log(arguments[btns]);
    // var go_back = document.getElementById(arguments[0]);
    // console.log(go_back)
    // go_back.disabled = false;
    // var reverse_color = document.getElementById(arguments[0]);
    // console.log('reverse_color', reverse_color)
    // reverse_color.className += ' new_color ';
}

function change_btn_name(){
    var elem = document.getElementById("Archive");
    if (elem.value=="Archive"){ 
        elem.value = "Unarchive";
        $("#myModal .modal-body").text('Are you sure you want to unarchive the term');
    }
    else if (elem.value == "Unarchive"){
        elem.value = "Archive";
        $("#myModal .modal-body").text('Are you sure you want to archive the term');
    }
}

$(document).on('click', '.finalize', function(){
    $('.finish').collapse('hide');
    $('#archive').collapse('show');

});

function change_text() {
    var elem = document.getElementById("btn1");
    // console.log("Changed")
    if (elem.value=="Open Scheduling") elem.value = "Opened";
}

window.onload = function() {

  document.getElementsByClassName("theButtons").disabled= true;

    
}

function loadStateToTerm(){
    //This function makes sure that on load we can tell where each term was left off
    var x = document.getElementsByClassName("terms_btn");
    var btn_arr = []

    for (var i = 0; i < x.length; i++) {
        var btn_id = x[i].id;
        btn_arr.push(btn_id)
        var state = parseInt(btn_id.slice(7)) + 1;
        $('#'+btn_id).attr('data-target','#order'+state.toString())
        $('#'+btn_id).attr('aria-controls', 'order'+state.toString())
    }
    for (var i = 0; i < x.length; i++){
    var term = btn_arr[i].slice(0,6);
    var state = btn_arr[i].slice(7);
    var count = parseInt(state);
    for (var c = 1; c < count +1; c++){
    var btnToColor = $('#'+term +' #btn'+c.toString());
    btnToColor.removeClass("btn-dark");
    btnToColor.addClass('btn-success');
    }
    }
    }

function updateStateDataTarget(termCode,termState){
    var next_state = parseInt(termState)+1;        // shift to the next state\
    var previous_state = (parseInt(termState)-1)
    var term_btn = $('#' + termCode+'_' + previous_state.toString());
    var new_id = termCode+'_'+termState.toString()
   // console.log('Before any update:', term_btn);
    term_btn.attr("id", new_id);
    term_btn.attr('data-target','#order'+next_state.toString())
    term_btn.attr('aria-controls', 'order'+next_state.toString())
   // console.log("After any update", term_btn);
}
    
function submit_data(stateOrder){
    var allPanelsDiv = $("#allPanels");
    var termCode = allPanelsDiv.parent().parent()[0].id.split("_").pop();
    // console.log('termcode', termCode)
    // console.log('stateOrder passed', stateOrder)
    // console.log(theTR)
    $.ajax({
        url:'/admin/systemManagement/updateTermState',
        data:{'stateOrder':stateOrder,'termCode':termCode},
        type: "POST",
        cache: false,
        success: function () {
            console.log('Success')
            updateStateDataTarget(termCode, stateOrder);
          
        },
        error: function (xhr, ajaxOptions, thrownError) {
           console.log("saving data to database failed")
        }
        
    })
    
    
} 

// function remove_class(finishButton){
//     // This function is  to cause the finish panel to disappear. 
//     var finish_id = button.dataset.target;  
//     $(finish_id).removeClass("in");
// }

// $(document).on('click', '.terms_btn', function(){
//       document.getElementById("theButtons").disabled=false;
// });



/* global $ */
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
        loadStateToTerm();
});

// $(window).bind('load', function(){
//     console.log('Here')
//     loadStateToTerm();
// });

























// /* global $ */
// //Checks whether there is currently an admin selected and enables/disables remove button accordingly
// function updateFormEnabled1() {
//     if (verifyAdmin1()) {
//         $('#adminAdd').prop('disabled', false);
//     } else {
//         $('#adminAdd').prop('disabled', true);
//     }
// }
// function verifyAdmin1() {
//     if ($('#adminPicker1').val() != "None") {
//         return true;
//     } else {
//         return false
//     }
// }
// function updateFormEnabled() {
//     if (verifyAdmin()) {
//         $('#adminRemove').prop('disabled', false);
//     } else {
//         $('#adminRemove').prop('disabled', true);
//     }
// }
// function verifyAdmin() {
//     if ($('#adminPicker').val() != "None") {
//         return true;
//     } else {
//         return false
//     }
// }
// $('#adminPicker').change(updateFormEnabled);
// $('#adminPicker1').change(updateFormEnabled1);
// window.onload=updateFormEnabled();
// window.onload=updateFormEnabled1();
// $( function() {
//     $( "#datepicker" ).datepicker();
//   } );

// // Changes the text and post action in the modal based on the selected state 
// function changeModalText(state, termcode){
//     if (state == "locked"){
//         $("#modalTitleText").text("Lock this term?")
//         $("#modalBodyText").html("Are you sure you want to <b>lock</b> submissions for this term?")
//         $("#modalForm").attr('action',"/editTerm/locked")
//     }
//     else if (state == "tracking"){
//         $("#modalTitleText").text("Track this term's changes?")
//         $("#modalBodyText").html("Are you sure you want to <b>track</b> submissions for this term?")
//         $("#modalForm").attr('action',"/editTerm/tracking")
//     }
//     else{
//         $("#modalTitleText").text("Open this term?")
//         $("#modalBodyText").html("Are you sure you want to <b>open</b> submissions for this term?")
//         $("#modalForm").attr('action',"/editTerm/open")
//     }
//     $("#termCode").prop("value",termcode)
// }
// // Activate the tooltips and modals
// $(document).ready(function(){
//         $('[data-tooltip="true"]').tooltip({trigger:"hover"}); 
//         $('[data-toggle="modal"]').modal({show:false}); 
// });

// // Shows all the panels to the tab butons