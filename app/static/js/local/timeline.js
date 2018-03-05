/* global google */
/* global $ */
//DEPENDENCIES
//used on deadline.js
//used on courseTimeline.js
$(document).ready(function() {
   $('.selectpicker').selectpicker();
});

google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawBasic);
function google_data_json(){    
    var data =  $.ajax({
       url: append_url(),
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
    //console.log(typeof(data));
    //Convert string to dictionary    
    var jsonData = JSON.parse(data);
    //console.log(typeof(jsonData));    
    return jsonData
}
function newJSON(){
    google.charts.load('current', {packages: ['corechart', 'line']});
    google.charts.setOnLoadCallback(drawBasic);
}
newJSON()
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

function append_url(){
   //URL Location: courseTime.py
   var list = ['courseTimeline'];
   //TODO: get TID
   var select = document.getElementById("tid_selector").valueOf();
   var tid = select.options[select.selectedIndex].value;
   list.push(tid);
   list.push('json');
   var json_url = '/' + list.join('/');
   return json_url
}

