
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
     $("#roomCapacity").innerHTML=response["maxCapacity"];
     var my_div = document.getElementById('roomCapacity');
     console.log(my_div);
     my_div.innerHTML = response['maxCapacity'];
     console.log(response["maxCapacity"]);
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


   
function goto_rdetails(r) {
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
            
            
            


function setPreference(pref){
    console.log(pref);
    $("#assignButton").val(pref);
    
}
    
    
    
    
// function setRoomToPref(number){
//     if(number){
//     setPreference(number);
        
//     }
// }
function setButtonText(button){
    console.log(button.value);
var e = document.getElementById("selectedRoom");
var roomNumber= e.options[e.selectedIndex].text;
console.log(setPreference(roomNumber));

}


// $(function() {
//     $('button').click(function() {
//         $.ajax({
//             url: '/setPreference',
//             data: $('form').serialize(),
//             type: 'POST',
//             success: function(response) {
//                 console.log(response);
//             },
//             error: function(error) {
//                 console.log(error);
//             }
//         });
//     });
// });

    
    


