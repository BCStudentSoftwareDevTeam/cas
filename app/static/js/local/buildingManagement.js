// Javascipt file for Building Management

console.log("Javascript loaded!")

var rIDGlobal = "";

// //added by skrt skrt group
// function set_datetime(){
//     var date_time = new Date(2018, 11, 24, 10);
//     document.getElementById("datetime").innerHTML = date_time.toDateString();
// }

//end added by skrt skrt group

function setRoomId(rid){
    rIDGlobal=parseInt(rid);
}

function getRoomId(){
    return rIDGlobal;
}

function setRoomPanel(){ //Sets room ID based on what room (row) Edit button was clicked
    //TODO: Pull RID of room that was clickd (each row) to save the data changes to the appropriate room
    console.log("setRoomPanel is called")
    //var roomID = setRoomId($("#selectedRoom").val());
    
    console.log("RoomID:", roomID )
    // TODO:Add to this function so that it can show the  collapse and expand level for each room.
    moveModal();
    $("#roomDetails #Details").hide();
}

function moveModal(rID) { //Makes dropdown appear between rows
    var targetDiv = document.getElementById("modalRowRoom"+getRoomId());// hidden row where content will be placed
    var sourceDiv = document.getElementById("roomDetails");// content to be placed in targetDiv
    var targetDivs = $(".hiddenRow .hiddenDiv");// all hidden row divs (must be cleared first)
    
    for (var i = 0; i < targetDivs.length; i++) {
        $(targetDivs[i]).empty();// empty all the hiddenRows
    }
    $(targetDiv).html($(sourceDiv)); // moves modal content into current row
    $(targetDiv).collapse('show');
    //fixSelectPicker();
    //$("#selectedRoom").selectpicker('refresh');// must refresh or causes UI issues
    
    
}

function saveChanges(){ //Posts data to DB and reloads the page
    // var submitChangesButton = document.getElementById("submitChanges");
    document.getElementById("datetime").innerHTML = new Date(2018, 11, 24).toDateString();
    
    //TODO: Ajax call? The page won't need to reload...
    //Some sort of call to post to the data base!
}

    