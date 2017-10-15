$('#editSTModal' + stid).modal({
    backdrop: 'static',
    keyboard: false
})

$(window).load(function(){
        $('#editSTModal' + stid).modal('show');
   
});

function validateEditForm()
{
    var btn = $(document.activeElement).attr('id');
    if (btn == "formSubmit")
    {   
            var valid = true;
            var desc = document.getElementById("editcd").value;
            var prereqs = document.getElementById("editcp").value;
            var majorReqs = document.getElementById("editcm").value;
            var concReqs = document.getElementById("editcc").value;
            var minorReqs = document.getElementById("editcmi").value;
            var perspectives = document.getElementById("editcpe").value;
            
            if (desc == '' || desc == null) {
                $("#editcd").attr("required", true);
                valid = false;
            }
            if (prereqs == '' || prereqs == null) {
                $("#editcp").attr("required", true);
                valid = false;
            }
            if (majorReqs == '' || majorReqs == null) {
                $("#editcm").attr("required", true);
                valid = false;
            }
            if (concReqs == '' || concReqs == null) {
                $("#editcc").attr("required", true);
                valid = false;
            }
            if (minorReqs == '' || minorReqs == null) {
                $("#editcmi").attr("required", true);
                valid = false;
            }
            if (perspectives == '' || perspectives == null) {
                $("#editcpe").attr("required", true);
                valid = false;
            } 
        return valid;
        }
    else
        {
            return true;
        }
    }
