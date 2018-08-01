/*global $*/


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
    // $("#Details").empty();
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
        $("#collapseOne #Details").show();
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
            
var lastButtonPressed = "";   // used in below function to track button select changes
/** This method serves to differentiate three preferences 
 *  and tells you which one you are looking at the moment.
 *  @param {int} pref - the loop index from jinja (i.e., the preference being manipulated)
 *  @param {int} cID - the course id from RoomPreferences
*/
function setPreference(pref, cID){ 
    
    var currentButton = "prefButton"+pref+"_"+cID;
    if (lastButtonPressed != "") {
        var currentAriaState = document.getElementById(currentButton).getAttribute("aria-expanded"); 
        if (lastButtonPressed == currentButton) {
            currentAriaState = !currentAriaState;
            $('#firstCollapser').collapse('show');      // seems counterintuitive to show; bootstrap hides it, then this line shows it again
        } else {
            $('#firstCollapser').collapse('hide');      // seems counterintuitive to hide; bootstrap shows it, then this line hides it again
        }
    }
    lastButtonPressed = currentButton;
    
    fixSelectPicker();
    var pID = $("#prefButton"+pref+"_"+cID).val();
    var new_value = pref + '_' + pID + "_" + cID;
    $("#assignButton").val(new_value);
    var p1 = $("#prefButton1_"+cID).val();
    var p2 = $("#prefButton2_"+cID).val();
    var p3 = $("#prefButton3_"+cID).val();
    setSelectedRoom(pID);
    // console.log("modal function cID", cID);
    disableRoom(p1, p2, p3); // 
    
    moveModal(cID);
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
    var targetDiv = document.getElementById("modalRowCourse"+cID);      // hidden row where content will be placed
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
    
    $('#selectedRoom option[value="'+pID+'"]').prop("selected", true).selectpicker('refresh');
}

var room = 0;
var roomNumber = 0


function setButtonText(button){
 
    //helps add accurate information to the button after the value is assigned, and replaces the value of any.
    var e = document.getElementById("selectedRoom");
    room = e.options[e.selectedIndex].text;
    roomNumber= e.options[e.selectedIndex].value;
    var roomModel= document.getElementById("modelRoom");
    var courseinfo= document.getElementById("courseInfo");
    var modelSentence = "Are you sure you want to assign " + room + " to " + courseinfo.innerHTML + " ?";
    roomModel.innerHTML= modelSentence;
    document.getElementById("assignButton").value = button.value;
}


function setPrefButton(){
    var info =  $("#assignButton").val();
    var pref_id = info.split("_")[0];
    var cid = info.split("_")[2];
    var pref_button = document.getElementById("prefButton"+ pref_id + "_" +  cid);
    pref_button.value = roomNumber; //works
    pref_button.innerHTML = room;
    console.log('pref button');
    console.log(pref_id);    // $(pref_button).click(function(){
      var url= '/postPreference'
        $.ajax({
             type: "POST",
                url: url,
                data:{"roomID": roomNumber, "ogCourse": cid, "pref_id": pref_id},
                dataType: 'json',
                success: function(response){
                    console.log("success" + response["success"] );
                    disableRoom(roomNumber); //does disableRoom belong inside of this function.
                    postNotes();
                   },
                     error: function(error){
                        console.log("Error: " + error);
                     }
        });
   
    pref_button.click();
}


function disableRoom() {
    //what should be passed as arguements
    //roomids
    var selectRoom = document.getElementById('selectedRoom'); //get dropdown
    // console.log(selectRoom.length)
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

// This function takes the ID and then displays the Modal regarding the notes
$(document).ready(function(){
	$("#myModal").on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);  // Button that triggered the modal
        var titleData = button.data('title'); // Extract value from data-* attributes
        $(this).find('.modal-title').text(titleData );
    });
});





function postNotes(){
 
 
  var url= "/postNotes"
  $.ajax({
    type: "POST",
     url: url,
     data:{},
    
    dataType: 'json',
    success: function(response){
    console.log("success" + response);
    
                   },
    error: function(error){
        console.log("Error: " + error); 
    }
   
        });
         console.log("is this here?");
}










// this function was set up to trigger the options for second preference after the first preference is selected. // copied from SetPrefButton

// function setNotePref(){

function setNotePref(){

   
//     var info =  $("#assignButton").val();
//     var pref_id = info.split("_")[0];
//     var cid = info.split("_")[2];
//     var pref_button = document.getElementById("prefButton"+ pref_id + "_" +  cid);
//     pref_button.value = roomNumber; //works
//     pref_button.innerHTML = room;
//     console.log('pref button');
//     console.log(pref_id);    // $(pref_button).click(function(){
//       var url= '/postPreference'
//         $.ajax({
//              type: "POST",
//                 url: url,
//                 data:{"roomID": roomNumber, "ogCourse": cid, "pref_id": pref_id},
//                 dataType: 'json',
//                 success: function(response){
//                     console.log("success" + response["success"] );
//                     disableRoom(roomNumber); //does disableRoom belong inside of this function.
//                   },
//                      error: function(error){
//                         console.log("Error: " + error);
//                      }
//         });
   
//     pref_button.click();
// }


// var info =  $("#assignButton").val();
//     var pref_id = info.split("_")[0];
//     var cid = info.split("_")[2];
//     var pref_button = document.getElementById("prefButton"+ pref_id + "_" +  cid);
//     pref_button.value = roomNumber; //works
//     pref_button.innerHTML = room;
//     console.log('pref button');
//     console.log(pref_id);    // $(pref_button).click(function(){
//       var url= '/postPreference'
//         $.ajax({
//              type: "POST",
//                 url: url,
//                 data:{"roomID": roomNumber, "ogCourse": cid, "pref_id": pref_id},
//                 dataType: 'json',
//                 success: function(response){
//                     console.log("success" + response["success"] );
//                     disableRoom(roomNumber); //does disableRoom belong inside of this function.
//                   },
//                      error: function(error){
//                         console.log("Error: " + error);
//                      }
//         });
   
//     pref_button.click();
// }