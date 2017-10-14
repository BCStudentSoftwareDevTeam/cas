console.log("course js loaded")

function getSelectedCourse(elementId) {
   var selectedCourse = document.getElementById(elementId);
   
   if (selectedCourse.selectedIndex == -1){
      return null;
   }
   return selectedCourse.options[selectedCourse.selectedIndex].text;

}
function fillCourses(response, id){
   if(id=="selected_term_one"){
      var courses = document.getElementById("coursesDivOne");
      courses.style.visibility = 'visible';// do enabled/disabled instead of hidden
      var selectPicker = document.getElementById("oneCoursesSelect");
   }
   else{
      var courses = document.getElementById("coursesDiv");
      courses.style.visibility = 'visible';// do enabled/disabled instead of hidden
      var selectPicker = document.getElementById("multipleCoursesSelect");
   }
   
   for (var key in response){
      console.log(key);
      var option = document.createElement("option");
      option.text=response[key].prefix["prefix"].toString()+" "+response[key].bannerRef["ctitle"].toString()+" "+ response[key].schedule["startTime"];
      console.log("this is option text", option.text);
      option.value = key;
      selectPicker.appendChild(option);
   }
   $('.selectpicker').selectpicker('refresh');
}


function retrieveCourses(obj){
   var id = $(obj).attr('id');
   console.log("this is selected object", id);
   var x = window.location.href
   var y =x.split("/"); 
   console.log(y);
   var e = document.getElementById(id);
   var selected_term = e.options[e.selectedIndex].value;
   console.log("this is selected term", selected_term);
   console.log("/get_termcourses/"+selected_term+"/"+y[5])
   $.ajax({
            url: '/get_termcourses/'+selected_term+"/"+y[5],
            dataType: 'json',
            success: function(response){
      				fillCourses(response, id);
      			},
      			error: function(error){
      				console.log(error);
      			}
          
            });
  
}



function stn(){
   console.log('here');
   var courseTitle = getSelectedCourse('courseInfo');
   if (courseTitle === "---"){
      document.getElementById("submitAdd").disabled = true;
   }
   else{
      document.getElementById("submitAdd").disabled = false;
      var course = courseTitle.match(/\d/g).join("");
      //Then remove the numbers 86 from the string
      course = course.split("86").join("");
      console.log(course);
      if (course.length == 1){
         console.log('inside');
         $('#specialTopicsName').removeAttr('disabled');
      }
      else{
         $('#specialTopicsName').attr('disabled','disabled');
      }
   }
}


$(document).ready(function(){
    $('[data-toggle="popover"]').popover({
        placement : 'top'
    });
    
});

$(document).ready(function(){
    $('table').DataTable(
       {paging: false,
        "aaSorting":[]
       });
});
