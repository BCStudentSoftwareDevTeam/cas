$(function() {
   $( "#openDialog").on("click", function(){ 
       $( "#dialog-modal" ).dialog({
          height: 500,
          width: 300,
          modal: true,
        });
  
        $("#dialog-modal").dialog({
      buttons : {
        "Close" : function() {
          $(this).dialog("close");
        }
        
      }
    });
       $( "#dialog-modal" ).show();
    });
    
 });
    
function validateForm() {
    var x = document.forms["myForm"].value;
    if (x != "") {
        alert("the notes have been saved");
        return false;
    }
}
    
    
    
    
    
    
// //////////////////////////////////////////////////////////////////////////////    
// function opentextarea() {
//     var input = document.createElement('textarea');
//     input.name = 'post';
//     input.maxLength = 5000;
//     input.cols = 20;
//     input.rows = 10;
//     input.className = 'myCustomTextarea';
//     var oBody = document.getElementById("body");
//     while (oBody.childNodes.length > 0) {
//         oBody.removeChild(oBody.childNodes[0]);
//     }
//     oBody.appendChild(input);
//     document.body.appendChild(button)
//  }

// function editBox(){
//     var note;
//     var note=prompt("Please enter your notes below");
//     if (note != null){
//         alert("You edited your notes !");
//     }
// }

