// Javascipt file for Building Management

console.log("Javascript loaded!")

var rIDGlobal = "";

function setRoomId(rid){
    rIDGlobal=parseInt(rid);
}
function getRoomId(){
    return rIDGlobal;
}
function setRoomInfo(roomID, button){ //Sets room ID based on what room (row) Edit button was clicked
     setRoomId(roomID);
    console.log("RoomID:", roomID )
     movePanel(roomID);
     if (roomID > 0){
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
                        console.log("Roomss")
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
    }
}


function movePanel(rID) { //Makes dropdown appear between rows
    var targetDiv = document.getElementById("hiddenRow_"+getRoomId());// hidden row where content will be placed
    console.log("Target");
    console.log("hiddenRow_"+getRoomId());
    var sourceDiv = document.getElementById("roomDetails");// content to be placed in targetDiv
    $(targetDiv).html($(sourceDiv)); // moves modal content into current row
    $(sourceDiv).collapse('show');
}

function updateHtml(response) { //Updates the HTML in panel. Called in AJAX of setRoomPanel
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
    my_div.removeAttribute("checked"); //It was getting stuck
    if (response['movableFurniture']) {
        my_div.setAttribute("checked", "checked");
    }
    //TODO: PULL ED TECH
    //my_div.innerHTML = response['educationTech'];
    var visualAccValue = "option[value ='" + response['visualAcc'] +"']";
    console.log('VAC', visualAccValue)
    $("#visualAcc " + visualAccValue ).prop('selected', true); 
    var audioAccValue = "option[value ='" + response['audioAcc'] +"']";
    $("#audioAcc " + audioAccValue ).prop('selected', true);
    var physicalAccValue = "option[value ='" + response['physicalAcc'] +"']";
    $("#physicalAcc " + physicalAccValue ).prop('selected', true);
}

function saveChanges(){ //Posts data to DB and reloads the page
    // var submitChangesButton = document.getElementById("submitChanges");
    document.getElementById("datetime").innerHTML = new Date(2018, 11, 24).toDateString();
    document.getElementById("submitChanges").value

//TODO Create an ajax call that populates the data to the education tech
// function educationTech(){
//     var room_id = getRoomId();
//     if(room_id){
//         var url = '/education_Tech'+ room_id;
//         $.ajax({
//             url = url;
//             dataType: 'json',
//                 success: function(response){
//                     education_detail(response); //a function with education tech details
//                 },
//                 error: function(error) {
//                 console.log(error);
//                 }
//             });
//     $("#Details").show();{
//         })
//     }
    
// }
    
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

    