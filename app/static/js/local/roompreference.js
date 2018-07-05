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
    



 $(document).ready(function(){
        $("#txt_name").keyup(function(){
            alert($(this).val());
        });
    })
    
    
    
// ui-button-icon-primary 