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
    var sourceDiv = document.getElementById("roomDetails");// content to be placed in targetDiv
    $(targetDiv).html($(sourceDiv)); // moves modal content into current row
    $(sourceDiv).collapse('show');
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
    //Sets up datetime, passes all room attributes into a dictionary for ajax,then posts data to DB and reloads the page
    
    //Datetime setup
    var dateTime = new Date();
    var currHour = dateTime.getHours();
    if (currHour < 12) //AM/PM setup
       {
       a_p = "AM";
       }
    else
       {
       a_p = "PM";
       }
    if (currHour == 0)
       {
       currHour = 12;
       }
    if (currHour > 12)
       {
       currHour = currHour - 12;
       }
    
    var currMin = dateTime.getMinutes();
    currMin = currMin + "";
    if (currMin.length == 1) //Getting JS to not do single digit minutes
    {
        currMin = "0" + currMin;
    }
    var savedDateTime=(dateTime.toDateString()+",  "+ currHour + " : " +currMin + " " + a_p); //Concatenation of all date elements into one var for passing into dictionary
    //End datetime setup
    //Begin dictionary pass for Ajax
    var roomDetails = {}//For passing into Ajax data field (multiple attributes to pass)
    roomDetails["roomCapacity"] = document.getElementById('roomCapacity').value;
    roomDetails["roomType"] = document.getElementById('roomType').value;
    roomDetails["specializedEq"] = document.getElementById('specializedEq').value;
    roomDetails["specialFeatures"] = document.getElementById('specialFeatures').value;
    roomDetails["movableFurniture"] = document.getElementById('movableFurniture').checked;
    roomDetails["visualAcc"] = $('#visualAcc option:selected').text();  
    roomDetails["audioAcc"] = $('#audioAcc option:selected').text();    
    roomDetails["physicalAcc"] = $('#physicalAcc option:selected').text(); 
    roomDetails["lastModified"] = savedDateTime// document.getElementById('lastModified').value;
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
         
}
    

    