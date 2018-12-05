// Javascipt file for Building Management

console.log("Javascript loaded!")

var rIDGlobal = "";

function setRoomId(rid){
    rIDGlobal=parseInt(rid);
}
function getRoomId(){
    return rIDGlobal;
}
function setRoomInfo(roomID, button){ 
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
                        console.log("Error"+error);
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
    //TODO: PULL ED TECH
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
   
    console.log("saveChanges() called")
    var roomDetails = {}//For passing into Ajax data field (multiple attributes to pass)
    roomDetails["roomCapacity"] = document.getElementById('roomCapacity').value;
    roomDetails["roomType"] = document.getElementById('roomType').value;
    roomDetails["specializedEq"] = document.getElementById('specializedEq').value;
    roomDetails["specialFeatures"] = document.getElementById('specialFeatures').value;
    roomDetails["movableFurniture"] = document.getElementById('movableFurniture').checked;
    roomDetails["visualAcc"] = $('#visualAcc option:selected').text();  
    roomDetails["audioAcc"] = $('#audioAcc option:selected').text();    

    roomDetails["physicalAcc"] = $('#physicalAcc option:selected').text(); 
    console.log("RoomID" , getRoomId())
    // it is getting the right room ID even in the python file. However, it is not printing from the python file when changes are made. SO we still need
    // work on saving the data the right way
    var url = '/saveChanges/'+getRoomId();
         $.ajax({
             type: "POST",
                url: url,
                data: roomDetails, 
                dataType: 'json',
                success: function(response){
                    if (response["success"] != 0) {
                        //If successful
                        console.log("SUCCESSFUL JS AJAX CALL")
                        window.location = "/buildingManagement"
                    }
                    else{
                        //If not successful
                        console.log("Else in ajax")
                        // window.location.assign("/builingManagement")
                    }
                },
                error: function(error){
                    console.log("ERROR")
                    // window.location.assign("/builingManagement")
                }
         }); 

}
    // var submitChangesButton = document.getElementById("submitChanges");
    // document.getElementById("datetime").innerHTML = new Date(2018, 11, 24).toDateString();
    // document.getElementById("submitChanges").value
// }



function education_detail(response){
     
    
    // document.getElementById("projectors").innerHTML = response['projector'];
    // document.getElementById("smartboards").innerHTML = response['smartboards'];
    // document.getElementById("instructor_computers").innerHTML = response['instructor_computers'];
    // document.getElementById("podiums").innerHTML = response['podium'];
    // document.getElementById("student_workstations").innerHTML = response['student_workspace'];
    // document.getElementById("chalkboards").innerHTML = response['chalkboards'];
    // document.getElementById("whiteboards").innerHTML = response['whiteboards']
    
    var my_div = document.getElementById('projectors');
    my_div.value = response['projector'];
    var my_div = document.getElementById('smartboards');
    my_div.value = response['smartboards'];
    var my_div = document.getElementById('instructor_computers');
    my_div.value = response['instructor_computers'];
    var my_div = document.getElementById('podiums'); 
    my_div.value = response['podium'];
    var my_div = document.getElementById('student_workspace');
    my_div.value = response['student_workspace'];
    var my_div = document.getElementById('chalkboards');
    my_div.value = response['chalkboards'];
    
    
    
    
    
}

function seteducationTech() {
    setRoomId(getRoomId());
    console.log("room id: ", getRoomId());
    if(getRoomId()){
         var url = '/getEducationData/'+getRoomId();
        //  console.log(url)
         $.ajax({
                url: url,
                dataType: 'json',
                type:'GET',
                success: function(response){
                     if (response["success"] != 0) {//If successful
                            education_detail(response); //a function with education tech details
                            console.log("Success"+response)
                        }
                   
                },
                error: function(error) {
                console.log(error);
                }
            });
    // $("#hiddenRow_").show();
    }
}
    
function saveEdTechChanges(roomID){ 
    //Posts data to DB and reloads the page
    //Should update time/date in Last Modified column (TODO)
   
   
    var edtechDetails = {}//For passing into Ajax data field (multiple attributes to pass)
    edtechDetails["projector"] = document.getElementById('projectors').value;
    edtechDetails["smartboards"] = document.getElementById('smartboards').value;
    edtechDetails["instructor_computers"] = document.getElementById('specializedEq').value;
    edtechDetails["podium"] = document.getElementById('podiums').value;
    edtechDetails["student_workspace"] = document.getElementById('student_workspace').value;
    edtechDetails["chalkboards"] = document.getElementById('chalkboards').value;
    // edtechDetails["visualAcc"] = $('#visualAcc option:selected').text();  
    // edtechDetails["audioAcc"] = $('#audioAcc option:selected').text();    

    // roomDetails["physicalAcc"] = $('#physicalAcc option:selected').text(); 
    // console.log("RoomID" , getRoomId())
    // it is getting the right room ID even in the python file. However, it is not printing from the python file when changes are made. SO we still need
    // work on saving the data the right way
    var url = '/saveEdTechChanges/'+getRoomId();
         $.ajax({
             type: "POST",
                url: url,
                data: edtechDetails, 
                dataType: 'json',
                success: function(response){
                    if (response["success"] != 0) {
                        //If successful
                        console.log("SUCCESSFUL JS AJAX CALL")
                        
                    }
                    else{
                        //If not successful
                        console.log("Else in ajax")
                        // window.location.assign("/builingManagement")
                    }
                },
                error: function(error){
                    console.log("ERROR")
                    // window.location.assign("/builingManagement")
                }
         }); 
}
    
//TODO: create ajax call that saves Ed Tech to db. onclick INSIDE edtech modal.
    

    