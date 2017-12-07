var new_table;
var approved_table;
var incomplete_table;
var denied_table;
var sent_table;

function reload(element){
    $("#"+element.dataset.table).DataTable().ajax.reload();
}

function setup(){
    incomplete_table = $('#incomplete_table').DataTable({
        ajax:{
            url:"/courseManagement/specialTopics/get/201712",
            dataSrc: "0"
        }
    });

    incomplete_table.on("draw", function(){
      $('[data-toggle="popover"]').popover();
    });

    new_table = $('#new_table').DataTable({
        ajax:{
            url:"/courseManagement/specialTopics/get/201712",
            dataSrc: "1"
        }
    });

    new_table.on("draw", function(){
      $('[data-toggle="popover"]').popover();
    });

    sent_table = $('#sent_table').DataTable({
        ajax:{
            url:"/courseManagement/specialTopics/get/201712",
            dataSrc: "2"
        }
    });

    sent_table.on("draw", function(){
      $('[data-toggle="popover"]').popover();
    });

    approved_table = $('#approved_table').DataTable({
        ajax:{
            url:"/courseManagement/specialTopics/get/201712",
            dataSrc: "3"
        }
    });

    approved_table.on("draw", function(){
      $('[data-toggle="popover"]').popover();
    });


    denied_table = $('#denied_table').DataTable({
        ajax:{
            url:"/courseManagement/specialTopics/get/201712",
            dataSrc: "4"
        }

    });

    denied_table.on("draw", function(){
      $('[data-toggle="popover"]').popover();
    });

}

$(document).ready(function(){
    setup();
})
