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
        data.addColumn('number', 'Danger');
        //data.addColumn('number', 'Warning')
        var new_structure = [];
        for(var h=0; h < google_chart_dict[day].length; h++){
            var hList = google_chart_dict[day][h]
            hList.push(50)
            //hList.push(35)
            new_structure.push(hList)
        }        
        data.addRows(new_structure);              
        var options = {
            title: day, 
        
            hAxis: {
                title: 'Time',
                showTextEvery: 1,
            },
            vAxis: {
                title: '# Courses',
                ticks: [10,20,30,40,50,60,70,80]
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

