/*global $*/ //Allows easy access of variables that are used in multiple places
var cIDGlobal = '';
var prefIDGlobal = "";
var rIDGlobal='';
var termIDGlobal = '';
var lastButtonPressed = "";     // used to track button select changes
var buildingIDGlobal = "";
var prefListGlobal = [0,0,0];       //default before setting in U
var roomValueListGlobal = ["","",""] //for room value html, not values like in setPrefList
var room = 0; // this gives bldg shortname + room number e.g DR200
var states= ['AAA', 'RAA', 'RNN', 'RRN', 'RRA', 'RRR', 'NNN'];
// var getCurrentState()= states[0];

function getCurrentState() {
    return $("#row_state_" + getCourseId()).val();
}

function setCurrentState(the_state) {
    // console.log(the_state);    
    $("#row_state_" + getCourseId()).attr('value', the_state);
    // console.log($("#row_state_" + getCourseId()).val());
}

function setPrefID(pref_id){        // (set is used for the Declaration of the variable) this  sets up the preference id of each preference: 1, 2, 3 only valid values
    prefIDGlobal = parseInt(pref_id);
}

function getPrefId(){       //(get is used as a print for the declared variable)this method gets the value of each preference that is used globally
    return parseInt(prefIDGlobal);
}

function setCourseId(cid){      //this sets the course id which is also the row id
    cIDGlobal = parseInt(cid);
}

function getCourseId(){     //this gets the id of each course in order to access a particular a course
    return cIDGlobal;
}

function setRoomId(rid){        //this sets the room id globally
    rIDGlobal=parseInt(rid);
}

function getRoomId(){       //this gets the room ids so you can access each room independently
    return rIDGlobal;
}

function setTermId(tID){        //sets the ids of each term
    termIDGlobal= parseInt(tID);
}

function getTermId(){       //gets the value of the term id
    return termIDGlobal;
}

function setBuildingID(bID){        //sets the id for the building
    buildingIDGlobal=parseInt(bID);
}

function getBuildingId(){       //gets the builiding id of each building
    return buildingIDGlobal;
}

function setLastButtonPressed(lastPressedButtonID){     //sets the id of each last button pressed in the UI
    lastButtonPressed= lastPressedButtonID;
}

function getLastPressedButton(){            //getthe value of each last button pressed in the UI
    // console.log(lastButtonPressed)
    return lastButtonPressed;
}

function setPrefList(index,value){              //(location of value, actual value set on click) this function is used to set the hmtml alues of the preferences on page load and after the user clicks
    prefListGlobal[index-1]=parseInt(value);    //pref 1 to index 0, pref 2 to index 1, 3 to index 2
}

function getPrefList(){                 //gets the values of the prefrences of the user,p1, p2, p3 in form of html
    if (arguments.length == 0){
        return prefListGlobal;
    }
    else{
        return prefListGlobal[arguments[0]-1];      //pref 1 to index 0, pref 2 to index 1, 3 to index 2
    }
}
function setRoomValueList(index,value){             //Similar to PrefList, but is holding the html instead of the values, to avoid dupication of html and values
    roomValueListGlobal[index-1]=value;
}

function getRoomValueList(){                    // gets the values of the room prefrences
    if (arguments.length == 0){
        return roomValueListGlobal;
    }
    else{
        return roomValueListGlobal[arguments[0]-1];         //pref 1 to index 0, pref 2 to index 1, 3 to index 2
    }
    
}


/*this function accesses room details using its id and then printing it out*/
function room_detail(response){
    $("#roomCapacity").innerHTML=response["maxCapacity"];
    var my_div = document.getElementById('roomCapacity');
    my_div.innerHTML = response['maxCapacity'];
    var my_div = document.getElementById('roomNumber');
    my_div.innerHTML = response['number'];
    var my_div = document.getElementById('specializedEq');
    my_div.innerHTML = response['specializedEq'];
    var my_div = document.getElementById('specialFeatures')
    my_div.innerHTML = response['specialFeatures'];
    var my_div = document.getElementById('movableFurniture');
    if (response['movableFurniture']) {
        var check_or_x = '<span class="glyphicon glyphicon-ok"></span>';
    } else {
        var check_or_x = '<span class="glyphicon glyphicon-remove"></span>';
    }
    my_div.innerHTML = check_or_x;
    
   
    if(response['audioAcc']){
        document.getElementById("audioAccIcon").innerHTML = "Audio Accessibility : " + (response['audioAcc']).toString();
    } else {
        document.getElementById("audioAccIcon").innerHTML = "Audio Accessibility : ";
    }
     if(response['visualAcc']){
        
        document.getElementById("visualAccIcon").innerHTML = "Visual Accessibility : " + (response['visualAcc']).toString();
    } else {
        document.getElementById("visualAccIcon").innerHTML = "Visual Accessibility : ";
    }
    if(response['physicalAcc']){
        document.getElementById("physicalAccIcon").innerHTML = "Physical Accessibility : " + (response['physicalAcc']).toString()/*<span class='glyphicon glyphicon-font'></span>"*/;
    } else {
        document.getElementById("physicalAccIcon").innerHTML = "Physical Accessibility : ";
    }
    // education_detail(response);
}

/* The function below serves to take data from the python file and dumps it into the html file*/
function goToRDetails(r,doishow) {
    $("#collapseOne #Details #withoutSelectButton").show();
    if($("#selectedRoom").val()) {
       setRoomId($("#selectedRoom").val()); 
    }

    // console.log("inside RDets", getRoomId());
    if (r.value > 0){
        var room_materials= r.value;
        if(room_materials){
             var url = '/room_details/'+room_materials;
             $.ajax({
                    url: url,
                    dataType: 'json',
                    success: function(response){
                        if (response["success"] != 0) {
                            room_detail(response);
                        }
                    },
                    error: function(error) {
                        // console.log(error);
                    }
                });
        }
    }
    if (doishow){
        $("#collapseOne #Details").show();
    }
    if (getRoomId()<=0){
        $("#collapseOne #Details #withoutSelectButton").hide();
    }
    
}

/*sets the glyphicons for education tech for each room*/
function education_detail(response){
    // console.log('response', response)
    
    
    document.getElementById("projectors").innerHTML = response['projector'];
    document.getElementById("smartboards").innerHTML = response['smartboards'];
    document.getElementById("instructor_computers").innerHTML = response['instructor_computers'];
    document.getElementById("podiums").innerHTML = response['podium'];
    document.getElementById("student_workstations").innerHTML = response['student_workspace'];
    document.getElementById("chalkboards").innerHTML = response['chalkboards'];
    document.getElementById("whiteboards").innerHTML = response['whiteboards'];
    
    
    if(response['dvd']){
        document.getElementById("dvdIcon").innerHTML = "<span class='glyphicon glyphicon-ok pull-left'> </span>";
    } else {
        document.getElementById("dvdIcon").innerHTML = "<span class='glyphicon glyphicon-remove'> </span>";
    }
    
    if(response['audio']){
        document.getElementById("audioIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("audioIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['blu_ray']){
        document.getElementById("blu_rayIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("blu_rayIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['extro']){
        document.getElementById("extroIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("extroIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['doc_cam']){
        document.getElementById("doc_camIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("doc_camIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['vhs']){
        document.getElementById("vhsIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("vhsIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['tech_chart']){
        document.getElementById("tech_chartIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("tech_chartIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['mondopad']){
        document.getElementById("mondopadIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("mondopadIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
}

/* This function serves to take data from the python file and dumps into html file on the UI after taking from the education_detail()*/
function goto_educationTech() {
    // var room_id= $("#selectedRoom").val()
    selected_value = $("#prefButton"+getPrefId()+"_"+getCourseId()).val();
    // console.log("goTo_edtech rID: ", getRoomId());
    // setRoomId(selected_value);
    var room_id = getRoomId();
    // console.log("room id: ", room_id);
    if(room_id){
         var url = '/education_Tech/'+room_id;
        //  console.log(url)
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    education_detail(response); //a function with education tech details
                },
                error: function(error) {
                console.log(error);
                }
            });
    $("#Details").show();}
}

/* Removes background color on all rows */
function removeAllStriping() {
    ctr = $(".courseTableRow1");
    for (var i = 0; i < ctr.length; i++) {
        ctr.removeClass("bg-cas");
    }
 }
 
 
 /*This function serves to set up the value of each preference after the user clicks on each prefrence
tracks which button are pressed last
managers the options in the room selecy drop down the first preferecne should have this room do not require a room while p2 and p3 have no other room works
caters for managing the NONE option*/
function setPreference(){
    if (arguments.length > 0) {
        setPrefID(arguments[0]);
        setCourseId(arguments[1]);
    }
    removeAllStriping();
    $("#courseTableRow_"+getCourseId()).addClass("bg-cas");
    var p1 = $("#prefButton1_"+getCourseId()).val(); // setting the pref values
    var p2 = $("#prefButton2_"+getCourseId()).val();
    var p3 = $("#prefButton3_"+getCourseId()).val();
    
    // console.log(p1, p2, p3)
    
    // Setting the current state in into the UI for future reference
    currentStateInitializer(p1, p2, p3);
    
    
    
    setPrefList(1,p1);
    setPrefList(2,p2);
    setPrefList(3,p3);
   
    enableAllRooms();
    // Disable three rooms if it's a room only
    if (p1 > 0) {
        disableRoom(p1); // selected rooms are being disabled here 
    }
    if (p2 > 0) {
        disableRoom(p2); // selected rooms are being disabled here 
    }
    if (p3 > 0) {
        disableRoom(p3); // selected rooms are being disabled here 
    }
    
   
    var currentButton = "prefButton"+getPrefId()+"_"+getCourseId();
    $("#" + getLastPressedButton()).removeClass("btn-primary"); /this jquery makes the preference button active when you click one of them */
    $("#" + getLastPressedButton()).addClass("btn-secondary");
    $("#"+currentButton).removeClass("btn-secondary");
    $("#"+currentButton).addClass("btn-primary");
    
    if (getPrefId() == 1) {
        document.getElementById("noRoom").innerHTML = "This Course Does not Required A Room";
    } 
    else { //Changes text to "This course does not need a room" if on first preference only
        document.getElementById("noRoom").innerHTML = "No other rooms work";
    }
    
    if (getLastPressedButton() != "") {
        var currentAriaState = document.getElementById(currentButton).getAttribute("aria-expanded");
        if (getLastPressedButton() == currentButton) {
            currentAriaState = !currentAriaState;
            $('#firstCollapser').collapse('show');      // seems counterintuitive to show; bootstrap hides it, then this line shows it again
            
        } else {
            $('#firstCollapser').collapse('hide');      // seems counterintuitive to hide; bootstrap shows it, then this line hides it again
        }
    }
    
    setLastButtonPressed(currentButton);
    fixSelectPicker();  
    
    // This section sets the value of the Select button used after a user chooses a room
    var pID = $("#prefButton"+getPrefId()+"_"+getCourseId()).val();     // THIS IS A ROOM ID!!!!
    // console.log("Inside SetPrefs", getRoomId(), "/", pID);
    setRoomId(pID);
    // console.log("Inside SetPrefs, after setroomid", getRoomId(), "/", pID);
    var new_value = getPrefId() + '_' + pID + "_" + getCourseId();
    $("#selectButton").val(new_value);
   
    setSelectedRoom(pID);
    
    moveModal(getCourseId());
    $("#collapseOne #Details").hide();

    if (getPrefList(getPrefId())>0){
        goToRDetails(document.getElementById("selectedRoom"),true);
    }
    
    $('#roomPickHeader').text('Pick a Room for Preference '+getPrefId()+":").data('text'); // Updates the 'Pick a room ' text for each preference
    
    PageLoad();
}

function stateZero(pref_num, val){// This function handles the functionalities of the first state which is 'AAA'= any room works in all three  preferences
    console.log("Going to ", states[6]);
    console.log("Val ", val);
    if (val == 0){
        return; // 'AAA'
    }
    
    else if (val == -1){
        setCurrentState(states[6]); // 'NNN'
    }
    else{
        setCurrentState(states[1]); // 'RAA'
    }
    
}

function stateOne(pref_num, val){ // State One is: 'RAA'
    if (val == 0){
        if (pref_num == 1){
            setCurrentState(states[0]); // 'AAA'
        } 
        else if (pref_num == 2 || pref_num == 3){
            return; // Returns to itself
        }
    }
    else if (val == -1){
        if (pref_num == 1) {
            setCurrentState(states[6]); // 'NNN'
        }
        else if (pref_num == 2){
            setCurrentState(states[2]); // 'RNN'
        }
    }
    else {
        if (pref_num == 1){
            return; // State One returns to itself
        }
        else if (pref_num == 2){
            setCurrentState(states[4]); // 'RRA'
        }
    
    }
}

function stateTwo(pref_num, val){ // State Two is: 'RNN'
    if (val == 0 ){
        if (pref_num == 1){
            setCurrentState(states[0]); // 'AAA'
        }    
        else if (pref_num == 2){
            setCurrentState(states[1]); // 'RAA'
        }
    }
    else if (val == -1){
        if (pref_num == 1){
            setCurrentState(states[6]); // 'NNN'
        }
        else if (pref_num == 2){
            return; // It returns to itself
        }
    }
    else{
        if (pref_num == 1){
            return; // It returns to itself
        }
        else if (pref_num == 2){
            setCurrentState(states [3]); // 'RRN'
        }
    }
}

function stateThree(pref_num, val){ //State Three is 'RRN'
    if (val == 0) {
        if (pref_num == 1){
            setCurrentState(states[0]); // 'AAA'
        } 
        else if (pref_num == 2){
            setCurrentState(states[1]); // 'RAA'
        }
        else if (pref_num == 3){
            setCurrentState(states[4]); //'RRA'
        }
    }
    else if (val == -1){
        if (pref_num == 1){
            setCurrentState(states[6]); // 'NNN'    
        }
        else if (pref_num == 2){
            setCurrentState(states[2]); // 'RNN'
        }
        else if (pref_num == 3) {
            return; // It returns to itself
        }
    }
    else {
        if (pref_num == 1 || pref_num == 2) {
            return; // It returns to itself
        }
        else if (pref_num == 3){
            setCurrentState(states [5]); // 'RRR'
        }
    }
}



function stateFour(pref_num, val){  // State Four: 'RRA'
    if (val == 0){
        if (pref_num == 1){
            setCurrentState(states[0]); // 'AAA'
        } 
        else if (pref_num == 2){
            setCurrentState(states[1]); // 'RAA'
        }
        else if (pref_num == 3){
            return; // It returns to itself
        }
    }
    else if (val == -1){
        if (pref_num == 1){
            setCurrentState(states[6]); // 'NNN'
        } 
        else if (pref_num == 2){
            setCurrentState(states[2]); // 'RNN'
        }
        else if (pref_num == 3){
            setCurrentState(states[3]); // 'RRN'
        }
    }
    else{
        if (pref_num == 1 || pref_num == 2){
            return; // It returns to itself
        }
        else if (pref_num == 3){
            setCurrentState(states[5]); // 'RRR'
        }
    }
}


function stateFive(pref_num, val){ // State Five is RRR
    if(val == 0){
        if (pref_num == 1){
            setCurrentState(states[0]); // 'AAA'
        }
        else if(pref_num == 2){
            setCurrentState(states[1]); // 'RAA'
        }
        else if (pref_num == 3){
            setCurrentState(states[4]); // 'RRA'
        }
    }
    else if (val == -1){
        if (pref_num == 1){
            setCurrentState(states[6]); // 'NNN'
        }
        else if (pref_num == 2){
            setCurrentState(states[2]); //'RNN'
        }
        else if (pref_num  == 3){
            setCurrentState(states[3]); // 'RRN'
        }
    }
    else{
        return; // Do nothing because the state is already in state RRR
    }
    
}

function stateSix(pref_num, val){ // State 6 is 'NNN'
    // console.log("Going to ", states[0]);
    // console.log("Val ", val);
    if (val == 0){
        setCurrentState(states[0]); // 'AAA'
    }
    else if (val == -1) {
        return; // Returns to itself 
    }
    else {
        setCurrentState(states[2]); // 'RNN'
    }
}

function preferenceHandler(pref_num, val){ /* -determines states of the course, handles all the activities performed on preferences*/
    // console.log("State before handler. ||", getCurrentState(), "||", states[0], "||");
    // console.log("State before handler. ||", getCurrentState());
   // console.log("Same as 0? ", getCurrentState() == states[0]);
  //  console.log("Same as 6? ", getCurrentState() == states[6]);
    if (getCurrentState() == states[0]){ // If the current state is state zero, call the stateZero function that will determine based on the choice the user made, what the next state will be for a course
        stateZero(pref_num, val); 
    }
    else if (getCurrentState() == states[1]){
        stateOne(pref_num, val);
    }
    else if (getCurrentState() == states[2]){
        stateTwo(pref_num, val);
    }
    else if (getCurrentState() == states[3]){
        stateThree(pref_num, val);
    }
    else if (getCurrentState() == states[4]){
        stateFour(pref_num, val);
    }
    else if (getCurrentState() == states[5]){
        stateFive(pref_num, val);
    }
    else if (getCurrentState() == states[6]){
        stateSix(pref_num, val);
    }
    // console.log("State after prefhandler", getCurrentState());
}

function currentStateInitializer(pref_button1,pref_button2,pref_button3){
    // This function initializes the state of a course whenever the user clicks on a preference button. 
    if (pref_button1 == 0) {
        // AAA
        setCurrentState(states[0]);
    } else if (pref_button1 == -1) {
        // NNN
        setCurrentState(states[6]);
    } else {
        if (pref_button2 == 0)  {
            /// RAA
            setCurrentState(states[1]);
        } else if (pref_button2 == -1) {
            // RNN
            setCurrentState(states[2]);
        } else {
            if (pref_button3 == 0) {
                // RRA
                setCurrentState(states[4]);
            } else if (pref_button3 == -1) {
                // RRN
                setCurrentState(states[3]);
            } else {
                // RRR
                setCurrentState(states[5]);
            }
        }
    }
    
    // console.log("Initializing State", getCurrentState());
}

function updateUIButtonStates(){ 
    // Goes through all three states and updates the text in the three buttons to match the state.  
    // Assumes currentState has the correct value
    for (var i = 0; i < getCurrentState().length; i++) {
            // go through each state and update UI
            // console.log("State ", i, ":", getCurrentState()[i]);
            var pref_button = document.getElementById("prefButton"+ (i+1).toString() + "_" +  getCourseId());
           
            if (getCurrentState()[i] == "A") {
                pref_button.value  = 0;
                pref_button.innerHTML = 'Any Room Works';
                // console.log("Set A to ", i);
                // console.log(pref_button);
            } else if (getCurrentState()[i] == "N") {
                // console.log("Da funny state", i)
                if (i == 0) {
                    pref_button.innerHTML = 'This Course Does not Require A Room.';
                    var next_button = document.getElementById("prefButton2_" +  getCourseId());
                    // console.log($(next_button));
                    $(next_button).prop('disabled', true);
                    var next_button = document.getElementById("prefButton3_" +  getCourseId());
                    // console.log($(next_button));
                    $(next_button).prop('disabled', true);
                } else {
                    pref_button.innerHTML = 'No other rooms work.';
                }
                pref_button.value  = -1;
                // console.log("N");
                // console.log(pref_button);
                
            } else if (getCurrentState()[i] == "R") {
                if (i + 1 == getPrefId()) {
                    pref_button.value  = getRoomId();
                    pref_button.innerHTML = room;
                    // console.log("R");
                    // console.log(pref_button);
                
                    if (i < 2) { // This enables the next button once you've set a preference
                        var next_button = document.getElementById("prefButton"+ (i+2).toString() + "_" +  getCourseId());
                        $(next_button).prop('disabled', false);
                    }
                }
        }
    }
    
    PageLoad();

}

// No longer needed
// function updateUIButtonClickability() {
//     for (var i = 0; i < getCurrentState().length; i++) {
        
//     }
    
// }


/* Saves values, and Sets button to value*/
function saveValue(){
    
    // preferenceHandler(getPrefId(), getRoomId());
    var textarea = document.getElementById('message-text');
    var note = textarea.value.trim();
    // console.log("Note: ", note.length);
    if (note.length > 0) {
        // console.log("Before save value: ", getRoomId());
        // console.log({"roomID":getRoomId(), "ogCourse": getCourseId(), "pref_id": getPrefId()})
          var url= '/postPreference';
            $.ajax({
                 type: "POST",
                    url: url,
                    data:{"roomID":getRoomId(), "ogCourse": getCourseId(), "pref_id": getPrefId(), "note": note},
                    dataType: 'json',
                        success: function(response){
                            // disableRoom(getRoomId());//does disableRooms belong inside of this function.
                            // postNotes();
                            setPrefList(getPrefId(), getRoomId());
                            setInstructions(getCourseId());
                            // update the current state value in the hidden UI element
                            // console.log("After saving: ", getRoomId());
                            preferenceHandler(getPrefId(), getRoomId());
                            updateUIButtonStates();// Update the text and the value of the pref buttons based on the new state
                            // updateUIButtonClickability();
                            var targetDiv = document.getElementById("modalRowCourse"+getCourseId());// hidden row where content will be placed
                            $(targetDiv).collapse('hide');
                            // $('#exampleModal').dismiss();
                        },
                        error: function(xhr, status, error) {
                            var err = eval("(" + xhr.responseText + ")");
                            alert(err.Message);
                       }
            });
    
         // Changes the color of the buttons
         
        $("#exampleModal").removeClass("fade");
        $("#exampleModal").modal('hide');
        // FIXME
        // $(pref_button).removeClass("btn-primary");
        // $(pref_button).addClass("btn-success");
    } else {
        // console.log("Alert time!");
        $(".alert").show();
    }
}



/** /** The function below, helps generating the mode in the right course row, move it up and down depending on which row you are on **/
function fixSelectPicker() {
    var realSelect = $("#selectedRoom");
    var roomSelectModalDiv  = $("#roomSelectModalDiv ");
    roomSelectModalDiv.empty();
    roomSelectModalDiv.html(realSelect);
    realSelect.selectpicker('refresh');
}

/** A function to move the modal into the hidden rows for each row of the table
  * @params {int} cID - the course ID for that row
*/
function moveModal(cID) {
    var targetDiv = document.getElementById("modalRowCourse"+getCourseId());// hidden row where content will be placed
    var sourceDiv = document.getElementById("collapseOne");// content to be placed in targetDiv
    var targetDivs = $(".hiddenRow .hiddenDiv");// all hidden row divs (must be cleared first)

    for (var i = 0; i < targetDivs.length; i++) {
        $(targetDivs[i]).empty();// empty all the hiddenRows
    }
    $(targetDiv).html($(sourceDiv)); // moves modal content into current row
    $(targetDiv).collapse('show');
    fixSelectPicker();
    $("#selectedRoom").selectpicker('refresh');// must refresh or causes UI issues
}

function setSelectedRoom(rID){
    // console.log("Setting selected room to ", rID)
   var  sr = $('#selectedRoom option[value="'+rID+'"]').prop("selected", "selected");
    sr.selectpicker('refresh');
}


/*helps add accurate information to the button after the value is assigned, and replaces the value of any*/
function setModalText(button){
    $(".alert").hide();     // Always hides the alert that appears if the Notes: field is empty
    var e = document.getElementById("selectedRoom");
    var course_id = getCourseId();
    room = e.options[e.selectedIndex].text;
    
    // FIXME: This is for the two buttons in the select/confirmation modal besides the Save & Close button at the bottomm
    // if (e.options[e.selectedIndex].value < 1){
    //     document.getElementById("selectAny").disabled = true;
    //     document.getElementById("selectNone").disabled = true;
    // }
    
    setRoomId(e.options[e.selectedIndex].value);
    var roomModel= document.getElementById("modelRoom");
    var courseinfo= document.getElementById("courseInfo_"+course_id.toString());
    if (room == 'This Course Does not Required A Room'){
        var modelSentence = "Are you sure you do not want a room for " + courseinfo.innerHTML + " ?";
    }
    else if (room =='Any Room Works' ){
        var modelSentence = "Are you sure you that any room works for" + courseinfo.innerHTML + " ?";
    }
    else{
        var modelSentence = "Are you sure you want to assign " + room + " to " + courseinfo.innerHTML + " ?";
    }
    // console.log(room)
    roomModel.innerHTML= modelSentence;
    document.getElementById("selectButton").value = button.value;
    
    getNotes()
}




/* Goes to the next preference after one preference value is selected */
// FIXME Delete? Probably 
function goToNextPref() {
    var button = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId()).value;
        
    if (getPrefId() < 3 && (button > 0)) {
        setPrefID(getPrefId() + 1);
        var nextButton = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
        if(nextButton.value != 0)
        {
        nextButton.value = 0;
        nextButton.innerText  = "Any Room Works";
        nextButton.disabled = false;
            
        }
    }
    
    var button = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
    button.click();
}

/* Enables all the room in the dropdown */
function enableAllRooms() {
    var selectRoom = document.getElementById('selectedRoom');// gets the dropdown for rooms
    for(var i = 0; i < selectRoom.length; i++) {// enables everything
        if(selectRoom[i].id != 'donotTouch') {
            selectRoom[i].disabled = false;
            
        }
    }
}

/*Disables selected room from other preference*/
function disableRoom() {
    var selectRoom = document.getElementById('selectedRoom');// gets the dropdown for rooms
     
    for (var i = 0; i < arguments.length; i++) {// Disables options
        if (arguments[i] != 0){
            $('#selectedRoom option[value="'+arguments[i]+'"]').prop('disabled', true);
        }
    }
    // $("#selectedRoom").selectpicker('refresh'); // commented out this refresh to disable the selected room 
}

/*This function access the preference and course ID in order to save and post of each preference to the database */
function postNotes(){
  var url = "/postNotes";
  var textarea = document.getElementById('message-text');
  var note = textarea.value;
//   console.log("Note: ", note);
  $.ajax({
    type: "POST",
     url: url,
     data:{"note": note, "cid": getCourseId(), "pref_id": getPrefId()},

    dataType: 'json',
    success: function(response){
        // console.log("Notes successfully posted");
                   },
    error: function(xhr, status, error) {
            // var err = eval("(" + xhr.responseText + ")");
            // alert(err.Message);
            // console.log("Notes failed to save");
        }
        });
}

/*This function retrieves the notes from the DB for a room preference */
function getNotes(){
  var url = "/getNotes/" + getCourseId();
  var textarea = document.getElementById('message-text');
  textarea.value = "";
  
  $.ajax({
    type: "GET",
     url: url,
     data:{},

    dataType: 'json',
    success: function(response){
            textarea.value = response["notes"];
            // console.log("Got response: ", response["notes"]);
                   },
    error: function(xhr, status, error) {
            var err = eval("(" + xhr.responseText + ")");
            alert(err.Message);
        }
        });
}


// REMOVED by SAH & KLN because it is not needed anymore
// /*This function hadles no other rooms work button to set the remaining preferences to NONE */
// function remainingToNone(){
//     var button = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId()).value;
    
//     if (getPrefId() < 3 && (button > 0) ) {
//         setPrefID(getPrefId() + 1);
//         var nextButton = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
//         nextButton.value = -1;
//         nextButton.innerText  = "No other room works";
//         nextButton.disabled = false;
//         setRoomId(-1);
        
//         var url= '/postPreference';
//         $.ajax({
//              type: "POST",
//                 url: url,
//                 data:{"roomID":getRoomId(), "ogCourse": getCourseId(), "pref_id": getPrefId()},
//                 dataType: 'json',
//                     success: function(response){
//                     // disableRoom(getRoomId());//does disableRooms belong inside of this function.
//                     postNotes(getPrefId(),getCourseId());
//                     },
//                     error: function(xhr, status, error) {
//                       var err = eval("(" + xhr.responseText + ")");
//                       alert(err.Message);
//                   }
//         });
//     }
    
//     var button = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
//     button.click();
// }


/*sets the conditions for the note instruction ids in html span from note1-7*/
function getNoteId() {
    var noteId = 1;
    if (getPrefList(1)==0){//Caters for the case Notes1 Any available rooms, (0,0,0)
        noteId = 1;    
    } 
    else if  (getPrefList(1)>0 && getPrefList(2)==0){ //(#,0,0)
        noteId = 2;
    }
    else if (getPrefList(1)>0 && getPrefList(2)>0 && getPrefList(3)==0){ //Notes3 Pref 1 value, pref 2 value, any (#,#,0)
        noteId = 3;
    }
    else if (getPrefList(1)>0 && getPrefList(2)>0 && getPrefList(3)>0){ //Notes3 Pref 1 value, pref 2 value, any (#,#,0)
        noteId = 4;
    }
    else if  (getPrefList(1)>0 && getPrefList(2)<0){ //(#,-1,-1)
        noteId = 5; 
    }
    else if(getPrefList(1)>0 && getPrefList(2)>0 && getPrefList(3)<0){ //Notes6 Pref 1 value, pref 2 value, no other rooms work (#,#,-1)
        noteId = 6; 
    }
    else if(getPrefList(1)<0){// handles case Notes7 where the professor chooses no room needed for the course
        noteId = 7; 
    }
    return noteId;
}

/* Manages the instruction notes on the preference button clicks depending on the preferences the user picks */
function setInstructions(course) {
    var destination = $("#NotesHolder_" + course); //Links the span in the html to the td where notes are to appear for each course
    var target = $("#Notes" + getNoteId()).clone(); // gets the span id's
    // console.log(target);
    var target_text = target.html();
    target_text = target_text.replace("||pref_1||", getRoomValueList(1));
    target_text = target_text.replace("||pref_2||", getRoomValueList(2));
    target_text = target_text.replace("||pref_3||", getRoomValueList(3));
    target.html(target_text);
    target.show();
    destination.html(target.html());    
}
 
/* Connects with the setInstrucions function to initialize RoomValueList and PrefList on PageLoad() */    
function setRoomValueListFirstTime(course) { //Initializes RoomValueList. Called in Pageload
    setRoomValueList(1, $("#prefButton1" + "_" + course).html());
    setRoomValueList(2, $("#prefButton2" + "_" + course).html()); 
    setRoomValueList(3, $("#prefButton3" + "_" + course).html()); 
    setPrefList(1, $("#prefButton1" + "_" + course).val()); 
    setPrefList(2, $("#prefButton2" + "_" + course).val()); 
    setPrefList(3, $("#prefButton3" + "_" + course).val());
}

/*Sets the notes for all the courses on page load*/
function PageLoad () {
    var allCourses = $(".notesHolders");
    for (var i = 0; i < allCourses.length; i++) {
        var course = allCourses[i].id.split("_")[1];
        setRoomValueListFirstTime(course);
        var divId = allCourses[i].id;
        setInstructions(course);
    }
    // hideFirstPreferences();
    enableButtonsOnPageLoad();    
    // Set hidden input to correct state on page load
}

PageLoad();

/* Sets text on buttons, enables and disables according to values in button */
function enableButtonsOnPageLoad(){
    var allCourses = $(".notesHolders");            // weird  choice... but works (Grabs Course ID from notesholder)
    for(var i = 0; i < (allCourses.length); i++){
        var course = allCourses[i].id.split("_")[1];
        var pref1 = document.getElementById("prefButton1_" + course);
        var pref2 = document.getElementById("prefButton2_" + course);
        var pref3 = document.getElementById("prefButton3_" + course);
        
        // Sets correct language based on which preference button
        if(pref1.value == -1){
            pref1.innerText  = "This course does not require a room";
        }
        else if(pref2.value == -1){
            pref2.innerText  = "No other rooms work";
        }
        else if(pref3.value == -1){
            pref3.innerText  = "No other rooms work";
        }
        
        // Enables disabled buttons as long as 
        pref1.disabled = false;
        if (pref1.value > 0){
            pref2.disabled = false;
        }
        if (pref2.value > 0){
                pref3.disabled = false;
        }
            
    }
}