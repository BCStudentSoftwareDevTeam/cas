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


function prevcolor(btn) {
    // Adds the color for the completed processes

    var allPanelsDiv = $("#allPanels");
    
    var theTR = allPanelsDiv.parent().parent()[0].id.split("_").pop();
    
    var remove_color = $("#"+ theTR +" #" +btn); //Removes the color of the previous process to ensure there is no overide
    
    remove_color.removeClass("btn-dark");
    
    var prev = $("#"+ theTR +" #" + btn);
    
    prev.addClass('btn-success');
    
}

/** Reverses the color and the state of buttons when one clicks on unlock, 
 * applicable for two argumnets only for now uness adjusted 
 * @params {HTML Buttons} btns - all the buttons
 */
function reverseFunc(btn, StateOrder) {
    // This function handles what happens when the user chooses to reverse a state. It changes the color of the button and invokes the function that updates the database
    
    var allPanelsDiv = $("#allPanels");
    
    var theTR = allPanelsDiv.parent().parent()[0].id.split("_").pop();
    
    var remove_color = $("#"+theTR +" #" +btn); // This is the button whose color will need to be changed from btn-success. It is the button whose action will be reversed
    
    remove_color.removeClass("btn-success");
    
    var prev = $("#"+theTR+" #" + btn);
    
    prev.addClass('btn-dark');
    
    submit_data(parseInt(StateOrder)-1, 'true'); // Save the new state to the database through an ajax call
    
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
    //This function makes sure that on load we can tell where each term was left off when it comes to their state
   
    var x = document.getElementsByClassName("terms_btn"); // Get all the term buttons
    
    var btn_arr = [];

    for (var i = 0; i < x.length; i++) {
        
        var btn_id = x[i].id; // Get the id of each term button. The id of each term button consists of the termcode and the current state of that term
        
        btn_arr.push(btn_id); // Push the id of each term button to the button array
        
        var state = parseInt(btn_id.slice(7)) + 1; // Add 1 to the state of each button because the state order column table in the database starts with 0
        
        $('#'+btn_id).attr('data-target','#order'+state.toString()); // Update the data target of each term button 
        
        $('#'+btn_id).attr('aria-controls', 'order'+state.toString()); // Update the aria-controls of each term button
    }
    for (var i = 0; i < x.length; i++){
        // This for loop is to color the buttons for the state buttons already achieved
        
        var term = btn_arr[i].slice(0,6);
        
        var state = parseInt(btn_arr[i].slice(7));
   
        for (var c = 1; c < state +1; c++){
            
            var btnToColor = $('#'+term +' #btn'+c.toString());
            
            btnToColor.removeClass("btn-dark");
            
            btnToColor.addClass('btn-success');
            }
        }
    }

function updateStateDataTarget(termCode,termState, reverseStatus){
    // This function changes the data target of the term button that opens the panel where the user gets to move to the next state or reverse to a previous state
    
    var next_state = parseInt(termState) +1;        // the next state
   
    if (reverseStatus == 'true'){ // This is to recognize if the user tried to reverse an action
        
        var previous_state = (parseInt(termState)+1)
        
        var term_btn = $('#' + termCode+'_' + previous_state.toString());
    }
    else{
        
        var previous_state = (parseInt(termState)-1)
        
        var term_btn = $('#' + termCode+'_' + previous_state.toString());
    }
  
    var new_term_btn_id = termCode+'_'+termState.toString()
  
    term_btn.attr("id", new_term_btn_id);
    
    term_btn.attr('data-target','#order'+next_state.toString())
    
    term_btn.attr('aria-controls', 'order'+next_state.toString())
 
}
    
function submit_data(stateOrder, reverseStatus){
    // This function sends an ajax call to the controller to save the state of a term in the database 
    
    var allPanelsDiv = $("#allPanels");
    
    var termCode = allPanelsDiv.parent().parent()[0].id.split("_").pop();
   
    $.ajax({
        
        url:'/admin/systemManagement/updateTermState', // This is the link to the controller
        
        data:{'stateOrder':stateOrder,'termCode':termCode},
        
        type: "POST",
        
        cache: false,
        
        success: function () {
            //console.log('Success')
            
            updateStateDataTarget(termCode, stateOrder, reverseStatus); // On success of the saving to the database, update the data target for the term button
          
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

function downloadCourses(){
    // This function will make an ajax call to the controller that will handle the downloading of all the courses to an excel file
    var allPanelsDiv = $("#allPanels");
    
    var termCode = allPanelsDiv.parent().parent()[0].id.split("_").pop();
    
    window.location.href = '/excel/'+termCode;

    
}

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
        return false;
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
