var new_table;
var approved_table;
var incomplete_table;
var denied_table;
var sent_table;

function reload(element){
    // $("#"+element.dataset.table).DataTable().ajax.reload()
}

function render_cells(request){
    for (let table in request){
        for (let row in request[table]) {
            let table_row = $("<tr>")
            for (let cell in request[table][row]){
                let cell_text = request[table][row][cell]
                switch (cell){
                    case "1":
                        cell_text = cell_text.replace(/,/g,"<br />")
                        break;
                    case "6":
                        if(request[table][row][cell] == "Notes"){
                            cell_text = "Notes"
                        }else{
                            cell_text = "<a href='javascript:;'  data-toggle='popover' title='Course Notes' data-content='" + request[table][row][cell] + "'>Notes</a>"
                        }
                        break;
                    case "8":
                        let url_points = cell_text.split(",")
                        let term = url_points[0]
                        let prefix = url_points[1]
                        let sid = url_points[2]
                        cell_text = "<a href='/editSTCourseModal/" + term + "/" + prefix + "/" + sid + "/specialCourses'><span class='glyphicon glyphicon-edit' aria-hidden='true'></span></a>"
			break;
                    case "9":
			let url_points = cell_text.split(",")
                        term = url_points[0]
                        prefix = url_points[1]
                        sid = url_points[2]
			cell_text = "<a href=# data-toggle='modal' data-target='#deleteSTModal' data-stid='" + sid + "' data-post-url='/deletestcourse/" + term + "/" + prefix +"/'><span class='glyphicon glyphicon-trash text-danger' aria-hidden='true'></span></a>"
                        break;
                }
                let entry = $("<td>").append(cell_text)
                table_row.append(entry)
            }
            switch(table){
                case "0":
                    $("#incomplete_table").append(table_row)
                    break;
                case "1":
                    $("#new_table").append(table_row)
                    break;
                case "2":
                    $("#sent_table").append(table_row)
                    break;
                case "3":
                    $("#approved_table").append(table_row)
                    break;
                case "4":
                    $("#denied_table").append(table_row)
                    break;
            }
        }
    }
}

function setup(){
    $.ajax({
        url:"/courseManagement/specialTopics/get/201712",
        dataSrc: "0",
        success: function (e){
            render_cells(e)
        },
    });
}

$(document).ready(function(){
    setup();
})
