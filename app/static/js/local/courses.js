console.log("course js loaded")

function getSelectedCourse(elementId) {
   var selectedCourse = document.getElementById(elementId);

   if (selectedCourse.selectedIndex == -1){
      return null;
   }
   return selectedCourse.options[selectedCourse.selectedIndex].text;

}
function fillCourses(response, id){
   if (response !== "Error"){
   if(id=="selected_term_one"){
      var courses = document.getElementById("coursesDivOne");
      courses.style.display = 'inline';// do enabled/disabled instead of hidden
      var selectPicker = document.getElementById("oneCoursesSelect");
      $("#oneCoursesSelect").empty();
   }
   else{
      var courses = document.getElementById("coursesDiv");
      console.log(courses);
      courses.style.display = 'inline';// do enabled/disabled instead of hidden
      var selectPicker = document.getElementById("multipleCoursesSelect");
      $("#multipleCoursesSelect").empty();
   }
   console.log("this is response", response);
   for (var key in response){
      var option = document.createElement("option");
      /*CSC 111 - COURSE NAME (time)*/
      console.log(response[key]);
      option.text=response[key].prefix["prefix"].toString()+" "+response[key].bannerRef["number"].toString()+" "+response[key].bannerRef["ctitle"].toString()+" " +response[key].schedule['letter'];
      option.value = key;
      selectPicker.appendChild(option);
   }
   $('.selectpicker').selectpicker('refresh');
}
else{console.log("return value is None");}
}


function retrieveCourses(obj){
   var id = $(obj).attr('id');
   var x = window.location.href
   var y =x.split("/"); 
   var e = document.getElementById(id);
   var selected_term = e.options[e.selectedIndex].value;
   if(selected_term){
   $.ajax({
            url: '/get_termcourses/'+selected_term+"/"+y[5],
            dataType: 'json',
            success: function(response){
      				fillCourses(response, id);
      			},
      			error: function(error){
      				console.log(error);
      			}
            }); }
   else{
      if(id=="selected_term_one"){
         var courses = document.getElementById("coursesDivOne");
         courses.style.visibility = 'hidden';}
      
      else{
           var courses = document.getElementById("coursesDiv");
           courses.style.visibility = 'hidden';// do enabled/disabled instead of hidden
         }
   }  
   
}



function stn(){
   var courseTitle = getSelectedCourse('courseInfo');
   if (courseTitle === "---"){
      document.getElementById("submitAdd").disabled = true;
      $("#section_select").hide()
   }
   else{
      document.getElementById("submitAdd").disabled = false;
      var course = courseTitle.match(/\d/g).join("");
      //Then remove the numbers 86 from the string
      course = course.split("86").join("");
      console.log(course);
      var coursesDiv = document.getElementById('specialTopicCourse');
      var courseCredits = document.getElementById('ccredits');
      if (course.length == 1){
         console.log('inside');
         $('#specialTopicsName').removeAttr('disabled');
        coursesDiv.style.display = 'block';
        courseCredits.style.display = 'block';
        $('#submitSave').removeClass("hide");

      }
      else{
         $('#specialTopicsName').attr('disabled','disabled');
        coursesDiv.style.display = 'none';
        courseCredits.style.display = 'none';
        $('#submitSave').addClass("hide");
      }
      get_sections(courseTitle)
   }
   
}

function get_sections(title){
    $("#section_select").show()
    $.ajax({
        dataType : "json",
        url:"/courses/get_sections/",
        data:JSON.stringify({"course":title, "term":$("#term").val()}),
        type:"POST",
    	contentType: 'application/json',
        success:function(data){
            $("#section").empty();
            for (section in data){
                select = "<option value=" + data[section] + ">" + data[section] + "</option"
                $("#section").append(select);
            } 
            $("#section").selectpicker("refresh");
        },
    })
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
