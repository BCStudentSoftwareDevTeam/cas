// Javascipt file for Building Management

console.log("Javascript loaded!")

var rIDGlobal = "";

function setRoomId(rid){
    rIDGlobal=parseInt(rid);
}
function getRoomId(){
    return rIDGlobal;
}

function setRoomClicked(){ //Sets room ID based on what room (row) Edit button was clicked
    //TODO: Pull RID of room that was clicked (each row) to save the data changes to the appropriate room
    moveModal()
}

function moveModal(rid) { //Makes dropdown appear between rows
    var targetDiv = document.getElementById("modalRowRoom"+getRoomId());// hidden row where content will be placed
    var sourceDiv = document.getElementById("roomData");// content to be placed in targetDiv
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
    
}