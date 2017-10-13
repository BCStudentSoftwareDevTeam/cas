/* global google */
google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'X');
    data.addColumn('number', '# Courses');

    data.addRows([
        ["8:00", 0], ["8:00", 48],   ["8:40", 48],  ["9:10", 28],  ["9:20", 74],  ["9:50", 48],  ["10:30", 0],
        ["10:40", 45], ["11:50", 7], ["12:00", 26], ["12:30", 19], ["12:40", 30], ["1:10", 11],
        ["1:20", 40], ["2:30", 0], ["2:40", 34], ["3:50", 6], ["4:00", 8], ["4:30", 2], ["5:10", 0]
    ]);

    var options = {
        title: 'Mondays', 
    
        hAxis: {
        title: 'Time',
        showTextEvery: 1,
    },
    vAxis: {
      title: '# Courses'
    }
  };

  var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
  chart.draw(data, options);
}