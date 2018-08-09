/*global $*/

console.log("Javascript is loaded!");

var cIDGlobal = '';
var prefIDGlobal = "";
var rIDGlobal='';
var termIDGlobal = '';
var lastButtonPressed = "";   // used to track button select changes
var buildingIDGlobal = "";
var prefListGlobal = [0,0,0];//default before setting in U
// if preflistGlobal[0] = None
// setprefListGlobal([1]) = None//stores values of pref 1 2 and 3 Roompreferences.pref1, etc
// setprefList([2]) = None

function setPrefID(pref_id){// (DECLARATION OF VARIABLE) this function sets up the preference id of each preference: 1, 2, 3 only valid values
    prefIDGlobal=parseInt(pref_id); 
}

function getPrefId(){// (PRINT VARIABLE)this method gets the value of each preference that is used globally
    return prefIDGlobal;
}

function setCourseId(cid){// this function sets the course id which is also the row id 
    cIDGlobal= parseInt(cid);
}

function getCourseId(){// this function serves to get the id of each course in order to access a particular a course 
    return cIDGlobal;
}

function setRoomId(rid){// this function sets the room id globally 
    rIDGlobal=parseInt(rid); 
}

function getRoomId(){// this function gets the room ids so you can access each room independently 
    return rIDGlobal;
}

function setTermId(tID){// This function serves to set the ids of each term  
    termIDGlobal= parseInt(tID);
}

function getTermId(){// This method serves to get the va
    return termIDGlobal;
}

function buildingID(bID){
    buildingIDGlobal=parseInt(bID); 
}

function getBuildingId(){
    return buildingIDGlobal;
}

function setLastButtonPressed(lastPressedButtonID){
    lastButtonPressed= lastPressedButtonID;
}

function getLastPressedButton(){
    return lastButtonPressed;
}

function setprefList(index,value){ //(location of value, actual value set on click)
    prefListGlobal[index-1]=value; //pref 1 to index 0, pref 2 to index 1, 3 to index 2
}

function getprefList(){
    if (arguments.length == 0){
        return prefListGlobal;
    }
    else{
        return prefListGlobal[arguments[0]-1]; //pref 1 to index 0, pref 2 to index 1, 3 to index 2
    }
}




function room_detail(response){
    // this function accesses room details using its id and then printing it out
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

  
function goto_rdetails(r) { // this function serves to take data from the python file and dumps into html file 
    setRoomId($("#selectedRoom").val());
    console.log("selected value",getPrefId($("#selectedRoom").val()));
    var room_materials= r.value;
    if(room_materials){
         var url = '/room_details/'+room_materials;
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    room_detail(response);
                },
                error: function(error) {
                console.log(error); 
                }
            });
        
    }
    
    
}


// continue on monday based creating education tech materials 
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
   
 
function goto_educationTech(edu) { // this function serves to take data from the python file and dumps into html file ;
    var educationTech= edu.value;
    if(educationTech){
         var url = '/education_Tech/'+educationTech;
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    education_detail(response);// will create this function 
                },
                error: function(error) {
                console.log(error); 
                }
            });
    $("#Details").show();}
}
            
/** This method serves to differentiate three preferences 
 *  and tells you which one you are looking at the moment.
 *  @param {int} pref - the loop index from jinja (i.e., the preference being manipulated)
 *  @param {int} cID - the course id from RoomPreferences
*/
function setPreference(){ //This function serves to set up the value of each preference after you click it
    
    if (arguments.length > 0) {
        setPrefID(arguments[0]);
        setCourseId(arguments[1]);
    }
    var p1 = $("#prefButton1_"+getCourseId()).val();
    console.log("pref1 value", p1);
    var p2 = $("#prefButton2_"+getCourseId()).val();
    var p3 = $("#prefButton3_"+getCourseId()).val();
    setprefList(1,p1);
    setprefList(2,p2);
    setprefList(3,p3);
    var currentButton = "prefButton"+getPrefId()+"_"+getCourseId();
    //console.log("Current button: ", currentButton);
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
    
    if (getPrefId() == 1) {     //Disables no other rooms work for the fist preference
        disableRoom(p1, p2, p3, -1); //     // -1 is the value of the option for no rooms work
       
    } else {
        disableRoom(p1, p2, p3);
        
    } 
    
    moveModal(getCourseId());
            $("#collapseOne #Details").hide();
    console.log("Preflist",getprefList())
    if (getprefList(getPrefId())!=0){
        goto_rdetails(document.getElementById("selectedRoom"));
        $("#collapseOne #Details").show();
    }
}
/** A function to clean up the selectpicker. 
 *  Only needed because bootstrap selectpicker acts dumb without. 
*/
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
    var sourceDiv = document.getElementById("collapseOne");             // content to be placed in targetDiv
    var targetDivs = $(".hiddenRow .hiddenDiv");                        // all hidden row divs (must be cleared first)
    
    for (var i = 0; i < targetDivs.length; i++) {
        $(targetDivs[i]).empty();           // empty all the hiddenRows
    }
    
    $(targetDiv).html($(sourceDiv));        // moves modal content into current row
    $(targetDiv).collapse('show');
    fixSelectPicker();
    $("#selectedRoom").selectpicker('refresh');     // must refresh or causes UI issues
}
    
function setSelectedRoom(pID){
    // FIXME: This is wrong: setPrefID(pID);
    
    $('#selectedRoom option[value="'+getprefList(getPrefId())+'"]').prop("selected", true).selectpicker('refresh');
}

var room = 0; //bldg + number
// var roomNumber = 0;

function setModalText(button){//helps add accurate information to the button after the value is assigned, and replaces the value of any.
    var e = document.getElementById("selectedRoom");
    room = e.options[e.selectedIndex].text;
    console.log('room + plus building', room);
    setRoomId(e.options[e.selectedIndex].value);
    var roomModel= document.getElementById("modelRoom");
    var courseinfo= document.getElementById("courseInfo");
    var modelSentence = "Are you sure you want to assign " + room + " to " + courseinfo.innerHTML + " ?";
    roomModel.innerHTML= modelSentence;
    document.getElementById("selectButton").value = button.value;
    console.log("selected value ", document.getElementById("selectButton").value );
  
}


function saveValue(){//Sets button to values
    console.log(getPrefId());
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
                    console.log("success in SaveValue");
                    disableRoom(getRoomId()); //does disableRoom belong inside of this function.
                    postNotes(getPrefId(),getCourseId());
                   
                   },
                    error: function(xhr, status, error) {
                      var err = eval("(" + xhr.responseText + ")");
                      alert(err.Message);
                   }
        });

    if (getRoomId() == 0) {
        setprefList(getPrefId(),0);    
    } else {
        setprefList(getPrefId(), getRoomId());    
      
    }
   

    goToNextPref();
}

function goToNextPref() {// Go to the next preference
    if (getPrefId() < 3) {
        setPrefID(getPrefId() + 1);
    }
    var nextButton = document.getElementById("prefButton"+ getPrefId() + "_" +  getCourseId());
    $("#exampleModal").removeClass("fade");
    $("#exampleModal").modal('hide');
    nextButton.click();
}

function disableRoom() {//disables selected room from other pref dropdowns
    var selectRoom = document.getElementById('selectedRoom'); //get dropdown
    for(var i = 0; i < selectRoom.length; i++) { //enables everything and it works
        if(selectRoom[i].id != 'donotTouch') {
            selectRoom[i].disabled = false;
        }
     }
    for (var i = 0; i < arguments.length; i++) { //disables options
        var option_val= arguments[i];;
        $('#selectedRoom option[value="'+arguments[i]+'"]').prop('disabled', true);
    }
    $("#selectedRoom").selectpicker('refresh');   
}

function postNotes(pref_id,cid){ 
/*this function access the preference and course id in order 
to save and post the note of each preference to the database */

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

