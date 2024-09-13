
$('#editModal' + cid).modal({
    backdrop: 'static',
    keyboard: false
})

$(window).load(function(){
        $('#editModal' + cid).modal('show');
});



function get_sections(){
    $.ajax({
        dataType : "json",
        url:"/courses/get_sections/",
        data:JSON.stringify({"course":title, "edit":true, "term":$("#term").val()}),
        type:"POST",
    	contentType: 'application/json',
        success:function(data){
            for (section in data){
                select = "<option value=" + data[section] + ">" + data[section] + "</option"
                $("#section").append(select);
            } 
            $("#section").selectpicker("refresh");
        },
    })
}
get_sections(title);



$('input[type=checkbox]').change(function () {
//Ensures state of None Required and all the other checkboxes can't be in an impossible state
    if($(this).prop('name') == "NoneRequired" && $(this).prop("checked")) {
        var courseCheckboxes = $("#courseMaterialsCheckboxesModal").find("input:checkbox");
        var first = true;
        $(courseCheckboxes).each(function() {
            $(this).prop('checked', first);
            if (first) {
                first = false;
            }
        });
    } else if ($(this).prop("checked")) {
        $("#courseMaterialsCheckboxesModal").find("input:checkbox#NoneRequired").prop("checked", false);
    }
});
