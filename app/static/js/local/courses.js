console.log("course js loaded")

function getSelectedCourse(elementId) {
   var selectedCourse = document.getElementById(elementId);
   
   if (selectedCourse.selectedIndex == -1){
      return null;
   }
   return selectedCourse.options[selectedCourse.selectedIndex].text;

}
function fillCourses(response){
   var courses = document.getElementById("coursesDiv");
   courses.style.visibility = 'visible';// do enabled/disabled instead of hidden
   var selectPicker = document.getElementById("multipleCoursesSelect");
   for (var e = 0; e < response.length; e++){
      var option = document.createElement("option");
      option.text = response[e];
      option.value = response[e];
      //change data structure to use either a matrix or dictionary
      // where the cid is the key or first element
      // and the course title is the value or second element
      selectPicker.appendChild(option);
   }
   $('.selectpicker').selectpicker('refresh');
}



function retrieveCourses(){
   var e = document.getElementById("selected_term");
   var selected_term = e.options[e.selectedIndex].value;
   console.log(selected_term);
   console.log("/get_termcourses/"+selected_term)
   $.ajax({
            url: '/get_termcourses/'+selected_term,
            dataType: 'json',
            success: function(response){
      				console.log(response);
      				fillCourses(response);
      				
      				
      			},
      			error: function(error){
      				console.log(error);
      			}
          
            });
   
   
   //courses= $.getJSON("/get_termcourses", selected_term)
  
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
