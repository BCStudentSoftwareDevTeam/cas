// Javascipt file for Building Management

console.log("Javascript loaded!")

var rIDGlobal = "";

function setRoomId(rid){
    rIDGlobal=parseInt(rid);
}

function getRoomId(){
    return rIDGlobal;
}

function setRoomPanel(roomID, button){ //Sets room ID based on what room (row) Edit button was clicked
     setRoomId(roomID);
    // console.log("RoomID:", roomID )
     movePanel(roomID);
    
    //ajax call to pull room data into panel
    $("#roomDetails #selectedRoom").show();
    if($("#selectedRoom").val() > 0) {
        setRoomId($("#selectedRoom").val());
        //movePanel(roomID);
        console.log("Room data", getRoomId());
        
    }
     if (roomID > 0){
        // var room_materials= r.value;
        // if(room_materials){
             var url = '/getRoomData/'+roomID;
             $.ajax({
                    url: url,
                    dataType: 'json',
                    type: "GET",
                    success: function(response){
                        if (response["success"] != 0) {
                            updateHtml(response);
                            console.log(response)
                        }
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
        // }
    }
}

    //json dumps to controller

function movePanel(rID) { //Makes dropdown appear between rows
    var targetDiv = document.getElementById("hiddenRow_"+getRoomId());// hidden row where content will be placed
    console.log("Target");
    console.log("hiddenRow_"+getRoomId());
    var sourceDiv = document.getElementById("roomDetails");// content to be placed in targetDiv
    $(targetDiv).html($(sourceDiv)); // moves modal content into current row
    $(sourceDiv).collapse('show');
    
}

function updateHtml(response) { //Updates the HTML in panel. Called in AJAX of setRoomPanel
    //Modeling after roompreferences jamal_basanta
    $('#roomNumber').text((response['number']).toString()).data('text');
    var my_div = document.getElementById('roomCapacity'); 
    my_div.value = response['capacity'];
    var my_div = document.getElementById('roomType');
    my_div.value = response['type'];
    var my_div = document.getElementById('specializedEq');
    my_div.value = response['specializedEq'];
    var my_div = document.getElementById('specialFeatures')
    my_div.value = response['specialFeatures'];
    var my_div = document.getElementById('movableFurniture');
    my_div.value = response['movableFurniture'];
    //var my_div = document.getElementById('educationTech'); //Will this be any different?
    //my_div.innerHTML = response['educationTech'];
    var my_div = document.getElementById('visualAcc');
    my_div.value = response['visualAcc'];
    var my_div = document.getElementById('audioAcc');
    my_div.value = response['audioAcc'];
    var my_div = document.getElementById('physicalAcc');
    my_div.value = response['physicalAcc'];
}

function saveChanges(){ //Posts data to DB and reloads the page
    // var submitChangesButton = document.getElementById("submitChanges");
    document.getElementById("datetime").innerHTML = new Date(2018, 11, 24).toDateString();
    
    //TODO: FIX AJAX CALL TO POST CHANGES TO DB
//     $.ajax({
//          type: "POST",
//             url: url,
//             data: {"": },
//             dataType: 'json',
//             success: function(response){ 
//                 console.log(response)
//                 console.log("I updated the room data")
//                  if (response['success'] == 1)
//                     window.location = "/buildingManagement"
//                     else
//                     window.location.assign("/buildingManagement")                    
//       			},
//       			error: function(error){
//       			    console.log("It didnt work")
//       				console.log(error); 
//                     window.location.assign("/buildingManagement")
//       			}
//     }
 }

    