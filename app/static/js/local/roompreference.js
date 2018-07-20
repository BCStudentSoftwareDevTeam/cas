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
    
    
       var my_div = document.getElementById('specializedEq');
     console.log(my_div);
     my_div.innerHTML = response['specializedEq'];
     
     var my_div = document.getElementById('specialFeatures');
     console.log(my_div);
     my_div.innerHTML = response['specialFeatures'];
     
     
     var my_div = document.getElementById('movableFurniture');
     console.log(my_div);
     my_div.innerHTML = response['movableFurniture'];
    
    
    
    
    // document.getElementById("visualAcc").checked = response["visualAcc"];
    
    
    if(response['audioAcc']){
        document.getElementById("audioAccIcon").innerHTML = "Audio Accessibility: <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("audioAccIcon").innerHTML = "Audio Accessibility: <span class='glyphicon glyphicon-remove'></span>";
    }
        
   
     if(response['visualAcc']){
        document.getElementById("visualAccIcon").innerHTML = "Visual Accessibility: <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("visualAccIcon").innerHTML = "Visual Accessibility: <span class='glyphicon glyphicon-remove'></span>";
    }
        
    if(response['physicalAcc']){
        document.getElementById("physicalAccIcon").innerHTML = "Physical Accessibility: <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("physicalAccIcon").innerHTML = "Physical Accessibility: <span class='glyphicon glyphicon-remove'></span>";
    }
       
       
       
    if(response['dvd']){
        document.getElementById("dvdIcon").innerHTML = "DVD : <span class='glyphicon glyphicon-ok'></span>";
    } else {
        document.getElementById("dvdIcon").innerHTML = "Physical Accessibility: <span class='glyphicon glyphicon-remove'></span>";
    }    
    
  
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



// continue on monday based creating education tech materials 

   
function goto_educationTech(edu) { // this function serves to take data from the python file and dumps into html file 
    
    console.log(edu.value);
    var room_materials= edu.value;

   
    console.log("education_Tech " + room_materials);
    if(room_materials){
         var url = '/education_Tech/'+room_materials;
         console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    console.log(response);
                    education_detail(response);// will create this function 
                },
                error: function(error) {
                console.log(error); 
                }
            });
            
$("#Details").show();}
}

//end



            

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
                    console.log("success" + response["success"] );
                    console.log(response)
                    
                    // console.log($("option[value="+roomNumber+"]").val());
                    
                    // ($("option[value="+roomNumber+"]").attr('disabled', 'disabled'));
                    
                    
                    // var isDisabled = $("option[value="+roomNumber+"]").attr("id");
                    // var isD2 = document.getElementById(isDisabled);
              

                    // var picker = document.getElementById("selectedRoom");
                 
                 
                    // isD2.classList.add('hidden');
                    // picker.classList.add('disabled');
                    // $("#selectedRoom").selectpicker('refresh');
                    // // // console.log(isDisabled.is('[disabled=disabled]'));
                    
                    // // console.log( isDisabled == $("option[value="+roomNumber+"]"));
                    // 
                   // 
                   },
                     error: function(error){
                        console.log("Error: " + error);
                        
                     }
                    // 
        });
     pref_button.click();
}



// $("#selectedRoom").change(function(){ 

//     var value = $("#theSelect option:selected").val();
//     var theDiv = $(".is" + value);
//       
 