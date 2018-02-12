function resize(textarea_obj){
        textarea_obj.style.height = 'auto';
        textarea_obj.style.height = textarea_obj.scrollHeight+'px';
}

function EditDeadline(deadline_id){    
    var display      = document.getElementById('displayDeadline' + deadline_id);
    var edit_display = document.getElementById('editDeadline'    + deadline_id);
    var save_button  = document.getElementById('saveButton' + deadline_id);
    var cancel_button = document.getElementById('cancelButton' + deadline_id);
    var edit_glyphicon = document.getElementById("edit_glyphicon" + deadline_id);
    
    if (display.style.display == "none") {
        display.style.display = "block";             //show the display div
        edit_display.style.display = "none";         //hide the textarea for the form
        save_button.style.display  = "none";         //hide save button for the form
        cancel_button.style.display = "none";        //hide cancel button for the form
        edit_glyphicon.style.display = "block";      //show the glyphicon
        
    } else {
        display.style.display        = "none";       //hide the display div
        edit_display.style.display   = "block";      //show the textarea for the form
        save_button.style.display    = "block";      //show save button for the form
        cancel_button.style.display  = "block";      //show cancel button for the form
        edit_glyphicon.style.display = "none";       //hide the glyphicon
    }
    resize(edit_display);
}

