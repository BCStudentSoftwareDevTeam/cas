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
    console.log("setRoomPanel is called")
    var RoomID = setRoomId($("#selectedRoom").val());
    console.log("RoomID:", roomID )
    moveModal(roomID);
    $("#roomDetails #Details").hide();
}

function moveModal(rID) { //Makes dropdown appear between rows
    var targetDiv = document.getElementById(""+getRoomId());// hidden row where content will be placed
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

    