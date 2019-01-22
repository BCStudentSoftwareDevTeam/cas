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
    //Created timestamp and puts it in Last Modified column
    //Should be called at the end of saveChanges and the save of education tech data
    new Date().getTime()
    console.log(Date.now())
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
    // console.log("moveble: ", my_div.value)
    // my_div.removeAttribute("checked"); //It was getting stuck
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
    // it is getting the right room ID even in the python file. However, it is not printing from the python file when changes are made. SO we still need
    // work on saving the data the right way
    var url = '/saveChanges/'+getRoomId();
         $.ajax({
             type: "POST",
                url: url,
                data: roomDetails,                              //Dictionary pass
                dataType: 'json',
                success: function(response){
                        window.location = "/buildingManagement" //Refresh page
                         createTimestamp() ;
                         //Sets time stamp for Last Modified column, so that it is created after data is saved
                },
                error: function(error){
                    console.log("ERROR")
                    window.location.assign("/buildingManagement")
                }
         }); 

}
   
   
  

 

function education_detail(response){
    
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
     var my_div = document.getElementById('whiteboards');
    my_div.value = response['whiteboards'];
    
    var my_div1 = document.getElementById('vhs');  

    if (response['vhs']) {
        
        my_div1.setAttribute("checked", "checked");
    }
    
     var my_div2 = document.getElementById('dvd');
    if (response['dvd']) {
        my_div2.setAttribute("checked", "checked");
    }
    
     var my_div3 = document.getElementById('blu_ray');
    if (response['blu_ray']) {
        my_div3.setAttribute("checked", "checked");
    }
    
     var my_div4 = document.getElementById('doc_cam');
    if (response['doc_cam']) {
        my_div4.setAttribute("checked", "checked");
    }
    
     var my_div5 = document.getElementById('extro');
    if (response['extro']) {
        my_div5.setAttribute("checked", "checked");
    }
    
     var my_div6 = document.getElementById('audio');
    if (response['audio']) {
        my_div6.setAttribute("checked", "checked");
    }
    
     var my_div7 = document.getElementById('mondopad');
    if (response['mondopad']) {
        my_div7.setAttribute("checked", "checked");
    }
    
     var my_div8 = document.getElementById('tech_chart');
    if (response['tech_chart']) {
        my_div8.setAttribute("checked", "checked");
    }
   

}


function seteducationTech() {
    setRoomId(getRoomId());
    if(getRoomId()){
         var url = '/getEducationData/'+ getRoomId();
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
   
    }
}
    
function saveEdTechChanges(roomID){ /*this functions saves the edecuationtech things on the front-end 
                                  and updated them as thier values change*/
   
    var edtechDetails = {}//For passing into Ajax data field (multiple attributes to pass)
    edtechDetails["projector"] = document.getElementById('projectors').value;
    edtechDetails["smartboards"] = document.getElementById('smartboards').value;
    edtechDetails["instructor_computers"] = document.getElementById('instructor_computers').value;
    edtechDetails["podium"] = document.getElementById('podiums').value;
    edtechDetails["student_workspace"] = document.getElementById('student_workspace').value;
    edtechDetails["chalkboards"] = document.getElementById('chalkboards').value;
    edtechDetails["whiteboards"] = document.getElementById('whiteboards').value;
    
    edtechDetails["vhs"] = document.getElementById('vhs').checked;
    edtechDetails["dvd"] = document.getElementById('dvd').checked;
    edtechDetails["blu_ray"] = document.getElementById('blu_ray').checked;
    edtechDetails["audio"] = document.getElementById('audio').checked;
    edtechDetails["mondopad"] = document.getElementById('mondopad').checked;
    edtechDetails["doc_cam"] = document.getElementById('doc_cam').checked;
    edtechDetails["extro"] = document.getElementById('extro').checked;
    edtechDetails["tech_chart"] = document.getElementById('tech_chart').checked;
    
    

    var url = '/saveEdTechChanges/'+getRoomId();
   
         $.ajax({
             type: "POST",
                url: url,
                data: edtechDetails, 
                dataType: 'json',
                success: function(response){
                    if (response["success"] != 0) {
                        console.log("SUCCESSFUL JS AJAX CALL")
                    }
                    else{
                     
                        console.log("Else in ajax")
                    }
                },
                error: function(error){
                    console.log("ERROR")

                }
         }); 
}

    

    

    