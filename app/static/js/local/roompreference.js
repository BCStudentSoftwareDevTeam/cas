
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
   
function goto_rdetails(r) {
   
    console.log(r.value);

      $("#Details").show();
    

      
      // make ajax request
        // --> goes to server
      // on success of ajax request, populate all the fields in UI
            $("#roomCapacity").value = response['roomCapacity']
      $("#Details").show();

      
}
    
    
    
    
    


