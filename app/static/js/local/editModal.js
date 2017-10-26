
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
            $("#section").empty();
            for (section in data){
                select = "<option value=" + data[section] + ">" + data[section] + "</option"
                $("#section").append(select);
            } 
            $("#section").selectpicker("refresh");
        },
    })
}
get_sections(title);
