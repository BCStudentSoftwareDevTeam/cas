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

function setPrefID(pref_id){        // (set is used for the Declaration of the variable) this  sets up the preference id of each preference: 1, 2, 3 only valid values
    prefIDGlobal=parseInt(pref_id);
    //console.log("SETTING PREF ID")
}

function getPrefId(){       //(get is used as a print for the declared variable)this method gets the value of each preference that is used globally
    return parseInt(prefIDGlobal);
}

function setCourseId(cid){      //this sets the course id which is also the row id
    cIDGlobal= parseInt(cid);
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
    my_div.innerHTML = response['movableFurniture'];
    if(response['audioAcc']){
        document.getElementById("audioAccIcon").innerHTML = "Audio Accessibility : <span class='glyphicon glyphicon-font'></span>";
    } else {
        document.getElementById("audioAccIcon").innerHTML = "Audio Accessibility : <span class='glyphicon glyphicon-bold'></span>";
    }
     if(response['visualAcc']){
        document.getElementById("visualAccIcon").innerHTML = "Visual Accessibility : <span class='glyphicon glyphicon-font'></span>";
    } else {
        document.getElementById("visualAccIcon").innerHTML = "Visual Accessibility : <span class='glyphicon glyphicon-bold'></span>";
    }
    if(response['physicalAcc']){
        document.getElementById("physicalAccIcon").innerHTML = "Physical Accessibility : <span class='glyphicon glyphicon-font'></span>";
    } else {
        document.getElementById("physicalAccIcon").innerHTML = "Physical Accessibility : <span class='glyphicon glyphicon-bold'></span>";
    }
    education_detail(response);
}

/* The function below serves to take data from the python file and dumps it into the html file*/
function goToRDetails(r,doishow) {
    $("#collapseOne #Details #withoutSelectButton").show();
    setRoomId($("#selectedRoom").val());
    if (r.value > 0){
        //console.log("selected value",getPrefId($("#selectedRoom").val()));
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
                    console.log(error);
                    }
                });
        }
    }
    if (doishow){
        $("#collapseOne #Details").show();
    }
    if (getRoomId()==0){
        $("#collapseOne #Details #withoutSelectButton").hide();
    }
    if (getRoomId()==-1){
        $("#collapseOne #Details #withoutSelectButton").hide();
    }
}

/*sets the glyhicicons for education tech for each room*/
function education_detail(response){
    if(response['educationTech']['dvd']){
        document.getElementById("dvdIcon").innerHTML = "DVD : <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("dvdIcon").innerHTML = "DVD: <span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['audio']){
        document.getElementById("audioIcon").innerHTML = "  Audio: <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("audioIcon").innerHTML = "  Audio: <span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['blu_ray']){
        document.getElementById("blu_rayIcon").innerHTML = "BluRay: <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("blu_rayIcon").innerHTML = "BluRay: <span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['extro']){
        document.getElementById("extroIcon").innerHTML = "Extro: <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("extroIcon").innerHTML = "Extro: <span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['doc_cam']){
        document.getElementById("doc_camIcon").innerHTML = "DocCam : <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("doc_camIcon").innerHTML = "DocCam: <span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['vhs']){
        document.getElementById("vhsIcon").innerHTML = "VHS: <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("vhsIcon").innerHTML = "VHS: <span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['tech_chart']){
        document.getElementById("tech_chartIcon").innerHTML = "TechChart: <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("tech_chartIcon").innerHTML = "TechChart: <span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['mondopad']){
        document.getElementById("mondopadIcon").innerHTML = "Mondopad: <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("mondopadIcon").innerHTML = "Mondopad: <span class='glyphicon glyphicon-remove'></span>";
    }
}

/*This function serves to take data from the python file and dumps into html file on the UI after taking from the education_detail()*/
function goto_educationTech(edu) {
    var educationTech= edu.value;
    if(educationTech){
         var url = '/education_Tech/'+educationTech;
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    education_detail(response); //a function with eduation tech details
                },
                error: function(error) {
                console.log(error);
                }
            });
    $("#Details").show();}
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
    var p1 = $("#prefButton1_"+getCourseId()).val(); // setting the pref values
    var p2 = $("#prefButton2_"+getCourseId()).val();
    var p3 = $("#prefButton3_"+getCourseId()).val();
    setPrefList(1,p1);
    setPrefList(2,p2);
    setPrefList(3,p3);
    var currentButton = "prefButton"+getPrefId()+"_"+getCourseId();
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
    
    var pID = $("#prefButton"+getPrefId()+"_"+getCourseId()).val();
    var new_value = getPrefId() + '_' + pID + "_" + getCourseId();
    $("#selectButton").val(new_value);
    setSelectedRoom(pID);
    
    if (getPrefId() == 1) {//Changes text to "This course does not need a room" if on first preference
        document.getElementById("noRoom").innerHTML = "This Course Does Not Require A Room";
    } 
    else { //Changes text to "This course does not need a room" if on first preference only
        var no_room = document.getElementById("noRoom").innerHTML;
        document.getElementById("noRoom").innerHTML = "No Other Rooms Work";
    }
    disableRoom(p1, p2, p3); //Disables selection(s) to prevent double selecting
    moveModal(getCourseId());
    $("#collapseOne #Details").hide();

    if (getPrefList(getPrefId())>0){
        goToRDetails(document.getElementById("selectedRoom"),true);
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

function setSelectedRoom(pID){
    $('#selectedRoom option[value="'+getPrefList(getPrefId())+'"]').prop("selected", true).selectpicker('refresh');
}


/*helps add accurate information to the button after the value is assigned, and replaces the value of any*/
function setModalText(button){
    var e = document.getElementById("selectedRoom");
    room = e.options[e.selectedIndex].text;
    setRoomId(e.options[e.selectedIndex].value);
    var roomModel= document.getElementById("modelRoom");
    var courseinfo= document.getElementById("courseInfo");
    var modelSentence = "Are you sure you want to assign " + room + " to " + courseinfo.innerHTML + " ?";
    roomModel.innerHTML= modelSentence;
    document.getElementById("selectButton").value = button.value;
}


/* Saves values, and Sets button to value*/
function saveValue(){
    var info =  $("#selectButton").val();
    var pref_button = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
    pref_button.value =  getRoomId();
    pref_button.innerHTML = room;
      var url= '/postPreference';
        $.ajax({
             type: "POST",
                url: url,
                data:{"roomID":getRoomId(), "ogCourse": getCourseId(), "pref_id": getPrefId()},
                dataType: 'json',
                    success: function(response){
                        
                    
                    disableRoom(getRoomId());//does disableRoom belong inside of this function.
                    postNotes(getPrefId(),getCourseId());
                    },
                   
                    error: function(xhr, status, error) {
                      var err = eval("(" + xhr.responseText + ")");
                      alert(err.Message);
                   }
        });

    setPrefList(getPrefId(), getRoomId());
    setInstructions(getCourseId());
    $("#exampleModal").removeClass("fade");
    $("#exampleModal").modal('hide');
}


/* Goes to the next preference after one prefrence value is selected */
function goToNextPref() {
    if (getPrefId() < 3) {
        setPrefID(getPrefId() + 1);
    }
    var nextButton = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
    $("#exampleModal").removeClass("fade");
    $("#exampleModal").modal('hide');
    nextButton.click();
}

/*Disables selected room from other preference*/
function disableRoom() {
    var selectRoom = document.getElementById('selectedRoom');// gets the dropdown for rooms
    for(var i = 0; i < selectRoom.length; i++) {// enables everything
        if(selectRoom[i].id != 'donotTouch') {
            selectRoom[i].disabled = false;
        }
     }
    for (var i = 0; i < arguments.length; i++) {// Disables options
        var option_val= arguments[i]; // Remove the redudancy of the variable
        if (option_val != 0){
        $('#selectedRoom option[value="'+arguments[i]+'"]').prop('disabled', true);
        }
    }
    $("#selectedRoom").selectpicker('refresh');
}

/*This function access the prefrence and course ID in order to save and post of each preference to the database */
function postNotes(pref_id,cid){
  var url = "/postNotes";
  var textarea = document.getElementById('message-text');
  var note = textarea.value;
  $.ajax({
    type: "POST",
     url: url,
     data:{"note": note, "cid": getCourseId(), "pref_id": getPrefId()},

    dataType: 'json',
    success: function(response){
                   },
    error: function(xhr, status, error) {
            var err = eval("(" + xhr.responseText + ")");
            alert(err.Message);
        }
        });
}


/*This function hadles no other rooms work button to set the remaining preferences to NONE */
function remainingToNone(){
    if (getPrefId()==1){
        setPrefList(2,-1);
        setPrefList(3,-1);
        var pref_button = document.getElementById("prefButton2" + "_" +  getCourseId());
        pref_button.value =  -1;
        pref_button.innerHTML = "No Other Rooms Work";
        var pref_button = document.getElementById("prefButton3" + "_" +  getCourseId());
        pref_button.value =  -1;
        pref_button.innerHTML = "No Other Rooms Work";
    }
    else if (getPrefId()==2){
        setPrefList(3,-1);
        var pref_button = document.getElementById("prefButton3"+ "_" +  getCourseId());
        pref_button.value =  -1;
        pref_button.innerHTML = "No Other Rooms Work";
    }
  //HIDE BUTTON ON THIRD ONE
}


/*sets the conditions for the note instruction ids in html span from note1-7*/
function getNoteId() {
    var noteId = 0;
    if (getPrefList(1)==0){//Caters for the case Notes1 Any available rooms, (0,0,0)
        console.log("Notes 1 case");
        noteId = 1;    
    } 
    else if  (getPrefList(1)>0 && getPrefList(2)==0){ //(#,0,0)
        console.log("notes2 Case");
        noteId = 2;
    }
    else if (getPrefList(1)>0 && getPrefList(2)>0 && getPrefList(3)==0){ //Notes3 Pref 1 value, pref 2 value, any (#,#,0)
        console.log("notes3 Case");
        noteId = 3;
    }
    else if (getPrefList(1)>0 && getPrefList(2)>0 && getPrefList(3)>0){ //Notes3 Pref 1 value, pref 2 value, any (#,#,0)
        console.log("notes4 Case");
        noteId = 4;
    }
    else if  (getPrefList(1)>0 && getPrefList(2)<0){ //(#,-1,-1)
        console.log("notes5 Case");
        noteId = 5; 
    }
    else if(getPrefList(1)>0 && getPrefList(2)>0 && getPrefList(3)<0){ //Notes6 Pref 1 value, pref 2 value, no other rooms work (#,#,-1)
        console.log("notes6 Case");
        noteId = 6; 
    }
    else if(getPrefList(1)<0){// handles case Notes7 where the professor chooses no room needed for the course
        console.log("notes7 Case");
        noteId = 7; 
    }
    return noteId;
}

/*Manages the instruction notes on the preference button clicks depending on the preferences the user picks */
function setInstructions(course) {
    var destination = $("#NotesHolder_" + course); //Links the span in the html to the td where notes are to appear for each course
    var target = $("#Notes" + getNoteId()).clone(); // gets the span id's
    var target_text = target.html();
    target_text = target_text.replace("||pref_1||", getRoomValueList(1));
    target_text = target_text.replace("||pref_2||", getRoomValueList(2));
    target_text = target_text.replace("||pref_3||", getRoomValueList(3));
    target.html(target_text);
    target.show();
    destination.html(target.html());    
}
 
/* Connects with the setInstrucions function to initialize RoomValueList and PrefList on firstPageLoad() */    
function setRoomValueListFirstTime(course) { //Initializes RoomValueList. Called in firstPageload
    console.log("#prefButton1" + "_" + course);
    setRoomValueList(1, $("#prefButton1" + "_" + course).html()); 
    setRoomValueList(2, $("#prefButton2" + "_" + course).html()); 
    setRoomValueList(3, $("#prefButton3" + "_" + course).html()); 
    setPrefList(1, $("#prefButton1" + "_" + course).val()); 
    setPrefList(2, $("#prefButton2" + "_" + course).val()); 
    setPrefList(3, $("#prefButton3" + "_" + course).val());
}

/*Sets the notes for all the courses on page load*/
function firstPageLoad () {
    var allCourses = $(".notesHolders");
    for (var i = 0; i < allCourses.length; i++) {
        var course = allCourses[i].id.split("_")[1];
        setRoomValueListFirstTime(course);
        var divId = allCourses[i].id;
        // console.log("course id",allCourses[i].id.split("_")[1]); // gross way of getting course id
        setInstructions(course);
    }
}

function hideBlankPreferences(){
    //Hides the preferences that shouldn't be able to be seen
    
    //Case 1: any, hidden, hidden
    
    //Case 2:  room, any, hidden
    
    //Case 3: room, room, any
    
    //Case 4: room, room, room
    
    //Case 5: 1 room, none_Choice, hidden
    
    //Case 6: room, room, none_choice
    
    //Case 7: none_choice, hidden, hidden
}

firstPageLoad();


$(".btn-group > .btn").click(function(){
    $(".btn-group > .btn").removeClass("active");
    $(this).addClass("active");
});