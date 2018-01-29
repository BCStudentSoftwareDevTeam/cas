function reload_table(request, table){
    $("#" + table).find("tr:gt(0)").remove()
    for (let row in request) {
        let table_row = $("<tr>")
        for (let cell in request[row]){

            let cell_text = request[row][cell]

            switch (cell){
                case "1":
                    cell_text = cell_text.replace(/,/g,"<br />")
                    break;

                case "6":
                    if(request[row][cell] == "Notes"){
                        cell_text = "Notes"
                    }else{
                        cell_text = "<a href='javascript:;'  data-toggle='popover' title='Course Notes' data-content='" + request[row][cell] + "'>Notes</a>"
                    }
                    break;

                case "8":
                    let url_points = cell_text.split(",")
                    let term = url_points[0]
                    let prefix = url_points[1]
                    let sid = url_points[2]
                    cell_text = "<a href='/editSTCourseModal/" + term + "/" + prefix + "/" + sid + "/specialCourses'><span class='glyphicon glyphicon-edit' aria-hidden='true'></span></a>"
                    cell_text += '<br/>'
                    cell_text +=  "<a href=# data-toggle='modal' data-target='#deleteSTModal' data-stid='" + sid + "' data-post-url='/deletestcourse/" + term + "/" + prefix +"'><span class='glyphicon glyphicon-trash text-danger' aria-hidden='true'></span></a>"
                    break;
            }
            let entry = $("<td>").append(cell_text)
            table_row.append(entry)
        }
        $("#" + table).append(table_row)
    }
}

function reload(term,table){
    $.ajax({
        url:"/courseManagement/specialTopics/get/" + term + "/" + table,
        success: function (results){
            reload_table(results,table)
            $('[data-toggle="popover"]').popover()
        },
    });
}

