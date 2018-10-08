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
                            // room_detail(response);
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
//     $.ajax({
//          type: "POST",
//             url: getRoomData,
//             data: {"":};
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
//  }
    //json dumps to controller

function movePanel(rID) { //Makes dropdown appear between rows
    var targetDiv = document.getElementById("hiddenRow_"+getRoomId());// hidden row where content will be placed
    console.log("Target");
    console.log("hiddenRow_"+getRoomId());
    var sourceDiv = document.getElementById("roomDetails");// content to be placed in targetDiv
    $(targetDiv).html($(sourceDiv)); // moves modal content into current row
    $(sourceDiv).collapse('show');
    
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

    