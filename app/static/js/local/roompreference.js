/*global $*/

$(function() {
   $( "#openDialog").on("click", function(){ 
       $( "#dialog-modal" ).dialog({
          height: 500,
          width: 300,
          modal: true,
        });
        $("#dialog-modal").dialog({
      buttons : {
        "Close" : function() {
          $(this).dialog("close");
        }
      }
    });
       $( "#dialog-modal" ).show();
    });
 });
    
function validateForm() {
    var x = document.forms["myForm"].value;
    if (x != "") {
        alert("the notes have been saved");
        return false;
    }
}


function room_detail(response){
    // this function accesses room details using its id and then printing it out
    
     $("#roomCapacity").innerHTML=response["maxCapacity"];
     var my_div = document.getElementById('roomCapacity');
     console.log(my_div);
     my_div.innerHTML = response['maxCapacity'];
    //  console.log(response["maxCapacity"]);
     var my_div = document.getElementById('roomNumber');
     console.log(my_div);
     my_div.innerHTML = response['number'];

    document.getElementById("visualAcc").checked = response["visualAcc"];
    document.getElementById("audioAcc").checked = response["audioAcc"];
    document.getElementById("physicalAcc").checked = response["physicalAcc"];
    
     var my_div = document.getElementById('specializedEq');
     console.log(my_div);
     my_div.innerHTML = response['specializedEq'];
     
     var my_div = document.getElementById('specialFeatures');
     console.log(my_div);
     my_div.innerHTML = response['specialFeatures'];
     
     
     var my_div = document.getElementById('movableFurniture');
     console.log(my_div);
     my_div.innerHTML = response['movableFurniture'];
}


   
   
function goto_rdetails(r) { // this function serves to take data from the python file and dumps into html file 
    
    console.log(r.value);
    var room_materials= r.value;

   
    console.log("room_details " + room_materials);
    if(room_materials){
         var url = '/room_details/'+room_materials;
         console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    console.log(response);
                    room_detail(response);
                },
                error: function(error) {
                console.log(error); 
                }
            });
            
$("#Details").show();}
}
            

function setPreference(pref, pID, cID){ // This method serves to differentiate three preference and tells you which one you are looking at the moment
    console.log(pref);
    console.log(cID);
    var new_value = pref + '_' + pID + "_" + cID;
    console.log( pID);
   
    $("#assignButton").val(new_value);
}
    

var room = 0;
var roomNumber = 0;
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
    pref_button.innerHTML = room;
   
      var url= '/postPreference'

        $.ajax({
             type: "POST",
                url: url,
                data:{"roomID": roomNumber, "ogCourse": cid, "pref_id": pref_id},
                dataType: 'json',
                success: function(response){
                    console.log("success" +response["success"] );
                    console.log(response)
                    // window.location = "/roomResolution"
                    },
                    error: function(error){
                        console.log("Error: " + error);
                    }
        });
     pref_button.click();
}