// Javascipt file for Building Management

// console.log("Javascript loaded!")

var rIDGlobal = "";

function setRoomId(rid){
    rIDGlobal=parseInt(rid);
}
function getRoomId(){
    return rIDGlobal;
}
function setRoomInfo(roomID, button){ 
    // '''For populating panel onClick of Edit button. updateHTML is called'''
    //Sets room ID based on what room (row) Edit button was clicked
     setRoomId(roomID);
    // console.log("RoomID:", roomID )
     movePanel(roomID);
     if (roomID > 0){
             var url = '/getRoomData/'+roomID;
             $.ajax({
                    url: url,
                    dataType: 'json',//Corresponds with controller json dumps
                    type: "GET",
                    success: function(response){
                        if (response["success"] != 0) {//If successful
                            updateHtml(response);//Update the panel with the data
                            // console.log("Success"+response)
                        }
                    },
                    error: function(error) {
                        // console.log("Error"+error);
                    }
                });
    }
    
}
function movePanel(rID) { 
    //Takes rID to ensure correct room per row
    //Called in setRoomInfo
    var targetDiv = document.getElementById("hiddenRow_"+getRoomId());// hidden row where content will be placed
    //console.log("Target"+targetDiv);
    //console.log("hiddenRow_"+getRoomId());
    var sourceDiv = document.getElementById("roomDetails");// content to be placed in targetDiv
    $(targetDiv).html($(sourceDiv)); // moves modal content into current row
    $(sourceDiv).collapse('show');
}

function createTimestamp(){
    //Creates timestamp and puts it in innerHTML of Last Modified column
    //Should be called at the end of saveChanges and the save of education tech data
    var datetime = new Date();
    console.log("DATETIME:"+datetime)
    $("#datetime").html(datetime.toDateString());
    // document.getElementById()
    // event.preventDefault();
}

function updateHtml(response) { 
    //Updates the HTML in panel. 
    //Called in AJAX of setRoomInfo
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
    //my_div.innerHTML = response['educationTech'];
    //The following three are different, due to it being a Select rather than an input
    var visualAccValue = "option[value ='" + response['visualAcc'] +"']";
    $("#visualAcc " + visualAccValue ).prop('selected', true); 
    var audioAccValue = "option[value ='" + response['audioAcc'] +"']";
    $("#audioAcc " + audioAccValue ).prop('selected', true);
    var physicalAccValue = "option[value ='" + response['physicalAcc'] +"']";
    $("#physicalAcc " + physicalAccValue ).prop('selected', true);
}

function saveChanges(roomID){ 
    //Posts data to DB and reloads the page
    //Should update time/date in Last Modified column (TODO)
    // console.log("saveChanges() called")
    var roomDetails = {}//For passing into Ajax data field (multiple attributes to pass)
    roomDetails["roomCapacity"] = document.getElementById('roomCapacity').value;
    roomDetails["roomType"] = document.getElementById('roomType').value;
    roomDetails["specializedEq"] = document.getElementById('specializedEq').value;
    roomDetails["specialFeatures"] = document.getElementById('specialFeatures').value;
    roomDetails["movableFurniture"] = document.getElementById('movableFurniture').checked;
    roomDetails["visualAcc"] = $('#visualAcc option:selected').text();  
    roomDetails["audioAcc"] = $('#audioAcc option:selected').text();    
    roomDetails["physicalAcc"] = $('#physicalAcc option:selected').text(); 
    // console.log("RoomID" , getRoomId())
    var url = '/saveChanges/'+getRoomId();
         $.ajax({
             type: "POST",
                url: url,
                data: roomDetails,                              //Dictionary pass
                dataType: 'json',
                success: function(response){
                        window.location = "/buildingManagement" //Refresh page
                },
                error: function(error){
                    console.log("ERROR")
                    window.location.assign("/buildingManagement")
                }
         }); 
   createTimestamp();                      //Sets time stamp for Last Modified column, so that it is created after data is saved
}

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
    
//TODO: create ajax call that saves Ed Tech to db. onclick INSIDE edtech modal.
    

    