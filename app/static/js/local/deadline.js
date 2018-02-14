/* global google */
/* global $ */ 
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

google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawBasic);
function google_data_json(){    
    var data =  $.ajax({
       url: '/courseTimeline/0/json', //This will alwasy show the current semester,
       method: 'GET',
       async: false, //this is neccessary to get the return. 
       done: function(results){
         JSON.parse(results);
         return results;
       },
       fail: function( jqXHR, textStatus, errorThrown ) {
        console.log( 'Could not get posts, server response: ' + textStatus + ': ' + errorThrown );
    }
    }).responseJSON;    
    //data is returned as a string
    //Convert string to dictionary    
    var jsonData = JSON.parse(data);
    return jsonData
}

function drawBasic() {
    var chart_order = ['Monday','Tuesday','Wednesday','Thursday','Friday'];
    var google_chart_dict = google_data_json();
    for (var i = 0; i < chart_order.length; i++){
        var day = chart_order[i];
        var data = new google.visualization.DataTable();
        data.addColumn('timeofday', 'X');
        data.addColumn('number', '# Courses');
        data.addColumn('number', 'Danger');
        data.addColumn('number', 'Warning')
        var new_structure = [];
        for(var h=0; h < google_chart_dict[day].length; h++){
            var hList = google_chart_dict[day][h]
            hList.push(50)
            hList.push(40)
            new_structure.push(hList)
        }
        new_structure.push([[18,0,0], 0, 50,40]);
        data.addRows(new_structure);
        var options = {
            title: day, 
        
            hAxis: {
                title: 'Time',
                showTextEvery: 1,
                viewWindow: {
                    min: [8,0,0],
                    max: [18,0,0]},                
                format: 'h:mm aa'
            },
            vAxis: {
                title: '# Courses',
                ticks: [10,20,30,40,50,60,70]
            }
        };
        
        var chart = new google.visualization.LineChart(document.getElementById(day));
        chart.draw(data, options);
    }
    var header = document.getElementById("timelineHeader");
    header.style.display = 'block';
}
