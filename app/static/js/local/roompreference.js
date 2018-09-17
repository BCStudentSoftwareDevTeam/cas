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
    console.log(lastButtonPressed)
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
    if (getRoomId()<=0){
        $("#collapseOne #Details #withoutSelectButton").hide();
    }
}

/*sets the glyhicicons for education tech for each room*/
function education_detail(response){
    if(response['educationTech']['dvd']){
        document.getElementById("dvdIcon").innerHTML = "<span class='glyphicon glyphicon-ok pull-left'> </span>";
    } else {
        document.getElementById("dvdIcon").innerHTML = "<span class='glyphicon glyphicon-remove'> </span>";
    }
    if(response['educationTech']['audio']){
        document.getElementById("audioIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("audioIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['blu_ray']){
        document.getElementById("blu_rayIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("blu_rayIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['extro']){
        document.getElementById("extroIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("extroIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['doc_cam']){
        document.getElementById("doc_camIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("doc_camIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['vhs']){
        document.getElementById("vhsIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("vhsIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['tech_chart']){
        document.getElementById("tech_chartIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("tech_chartIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
    }
    if(response['educationTech']['mondopad']){
        document.getElementById("mondopadIcon").innerHTML = "<span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("mondopadIcon").innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
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
    $("#" + getLastPressedButton()).removeClass("btn-primary"); /this jquery makes the preference button active when you click one of them */
    $("#" + getLastPressedButton()).addClass("btn-secondary");
    $("#"+currentButton).removeClass("btn-secondary");
    $("#"+currentButton).addClass("btn-primary");
    
    if (getPrefId() == 1) {
        document.getElementById("noRoom").innerHTML = "This Course Does not Required A Room";
    } 
    else { //Changes text to "This course does not need a room" if on first preference only
        document.getElementById("noRoom").innerHTML = "No Other Rooms Work";
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
    var pID = $("#prefButton"+getPrefId()+"_"+getCourseId()).val();
    var new_value = getPrefId() + '_' + pID + "_" + getCourseId();
    $("#selectButton").val(new_value);
    setSelectedRoom(pID);
   
    disableRoom(p1,p2, p3);
    
    moveModal(getCourseId());
    $("#collapseOne #Details").hide();

    if (getPrefList(getPrefId())>0){
        goToRDetails(document.getElementById("selectedRoom"),true);
    }
    
    
    PageLoad();
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
    $('#selectedRoom option[value="'+pID+'"]').prop("selected", true).selectpicker('refresh');
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
                    disableRoom(getRoomId());//does disableRooms belong inside of this function.
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
    $(pref_button).removeClass("btn-primary");
    $(pref_button).addClass("btn-success");
}


/* Goes to the next preference after one prefrence value is selected */
function goToNextPref() {
    var button = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId()).value;
        
    if (getPrefId() < 3 && (button > 0)) {
        setPrefID(getPrefId() + 1);
        var nextButton = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
        nextButton.value = 0;
        nextButton.innerText  = "Any Room Works";
        nextButton.disabled = false;
    }
    
    var button = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
    button.click();
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
        if (arguments[i] != 0){
            $('#selectedRoom option[value="'+arguments[i]+'"]').prop('disabled', true);
        }
    }
    // $("#selectedRoom").selectpicker('refresh'); // commented out this refresh to disable the selected room 
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
    var button = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId()).value;
    
    if (getPrefId() < 3 && (button > 0) ) {
        setPrefID(getPrefId() + 1);
        var nextButton = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
        nextButton.value = -1;
        nextButton.innerText  = "No Other Rooms Work";
        nextButton.disabled = false;
        setRoomId(-1);
        
        var url= '/postPreference';
        $.ajax({
             type: "POST",
                url: url,
                data:{"roomID":"-1", "ogCourse": getCourseId(), "pref_id": getPrefId()},
                dataType: 'json',
                    success: function(response){
                    disableRoom(getRoomId());//does disableRooms belong inside of this function.
                    postNotes(getPrefId(),getCourseId());
                    },
                    error: function(xhr, status, error) {
                      var err = eval("(" + xhr.responseText + ")");
                      alert(err.Message);
                   }
        });
    }
    
    var button = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
    button.click();
}


/*sets the conditions for the note instruction ids in html span from note1-7*/
function getNoteId() {
    var noteId = 0;
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
    hideFirstPreferences();
}

function hideFirstPreferences(){
    var allCourses = $(".notesHolders");
    for(var i = 0; i < (allCourses.length); i++){
        var course = allCourses[i].id.split("_")[1];
        var pref1 = document.getElementById("prefButton1_" + course);
        var pref2 = document.getElementById("prefButton2_" + course);
        var pref3 = document.getElementById("prefButton3_" + course);
        if(pref1.value == -1){
            pref1.innerText  = "This course does not require a room";
        }
        
        else if(pref2.value == -1){
            pref2.innerText  = "No other rooms work";
        }
        
        else if(pref3.value == -1){
            pref3.innerText  = "No other rooms work";
        }
        
        pref1.disabled = false;
        if (pref1.value > 0){
            pref2.disabled = false;
            if (pref2.value >0){
                pref3.disabled = false;
            }
        }    
    }
}


PageLoad();
