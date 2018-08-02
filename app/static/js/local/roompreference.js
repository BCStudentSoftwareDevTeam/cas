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
$("#Details").show();}
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
            

function setPreference(pref, cID){ // This method serves to differentiate three preference and tells you which one you are looking at the moment
    //pref is the loop index from jinja
    //cID is the course info from room preference
    var pID = $("#prefButton"+pref+"_"+cID).val();
    var new_value = pref + '_' + pID + "_" + cID;
    $("#assignButton").val(new_value);
    var p1 = $("#prefButton1_"+cID).val();
    var p2 = $("#prefButton2_"+cID).val();
    var p3 = $("#prefButton3_"+cID).val();
    setSelectedRoom(pID);
        console.log("modal function cID", cID);
    disableRoom(p1, p2, p3); // 
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
                    console.log("success in setPrefButton");
                    disableRoom(roomNumber); //does disableRoom belong inside of this function.
                    postNotes(pref_id,cid);
                   },
                    error: function(xhr, status, error) {
                      var err = eval("(" + xhr.responseText + ")");
                      alert(err.Message);
                   }
        });
   
    pref_button.click();
}

function disableRoom() {
    //what should be passed as arguements
    //roomids
    var selectRoom = document.getElementById('selectedRoom'); //get dropdown
    for(var i = 0; i < selectRoom.length; i++) { //enables everything and it works
        if(selectRoom[i].id != 'donotTouch') {
            selectRoom[i].disabled = false;
        }
     }
    for (var i = 0; i < arguments.length; i++) { //disables options
        var option_val= arguments[i];;
        $('#selectedRoom option[value="'+arguments[i]+'"]').prop('disabled', true);
        $("#selectedRoom").selectpicker('refresh');      
    }
}

// This function takes the ID and then displays the Modal regarding the notes
$(document).ready(function(){
	$("#myModal").on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);  // Button that triggered the modal
        var titleData = button.data('title'); // Extract value from data-* attributes
        $(this).find('.modal-title').text(titleData );
    });
});

function postNotes(pref_id,cid){
  //console.log('the parameters pref_id then cid for postNotes');
  //console.log(pref_id);
  //console.log(cid);
  var url = "/postNotes";
  var textarea = document.getElementById('message-text');
  //console.log(textarea);
  var note = textarea.value;
  //console.log('I am a note')
  //console.log(note);
  $.ajax({
    type: "POST",
     url: url,
     data:{"note": note, "cid": cid.toString(), "pref_id": pref_id.toString()},
    dataType: 'json',
    success: function(response){
        console.log("success" + response);
                   },
    error: function(xhr, status, error) {
            var err = eval("(" + xhr.responseText + ")");
            alert(err.Message);
        }
        });
}










// this function was set up to trigger the options for second preference after the first preference is selected. // copied from SetPrefButton

// function setNotePref(){
    
   
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