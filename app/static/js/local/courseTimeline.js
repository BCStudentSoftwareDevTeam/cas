/* global google */
/* global $ */

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

function drawBasic() {
    var chart_order = ['Monday','Tuesday','Wednesday','Thursday','Friday'];
    var google_chart_dict = google_data_json();    
    for (var i = 0; i < chart_order.length; i++){
        var day = chart_order[i];        
        var data = new google.visualization.DataTable();
        data.addColumn('timeofday', 'X');
        data.addColumn('number', '# Courses');
        data.addRows(google_chart_dict[day]);               
        var options = {
            title: day, 
        
            hAxis: {
                title: 'Time',
                showTextEvery: 1,
            },
            vAxis: {
                title: '# Courses'
            }
        };
        var chart = new google.visualization.LineChart(document.getElementById(day));
        chart.draw(data, options);
    }
}
    

function append_url(){
   var current_url = window.location.href;
   var list = current_url.split('/');
   for ( var i = 0; i < list.length; i++ ){
     if (list[i] == 'courseTimeline'){
       i = i + 100;
     }
     else{
        list.shift();
     }
   }
   list.push('json');
   var new_url = '/' + list.join('/');
   return new_url
}

