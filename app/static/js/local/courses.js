function getSelectedCourse(elementId) {
   var selectedCourse = document.getElementById(elementId);

   if (selectedCourse.selectedIndex == -1){
      return null;
   }
   return selectedCourse.options[selectedCourse.selectedIndex].text;

}

function fillCourses(courseList){
    var multipleCourseSelect = document.getElementById("multipleCoursesSelect");
    $(multipleCourseSelect).find('option').remove();
    $(multipleCourseSelect).selectpicker('refresh');
    var courses = document.getElementById("coursesDiv");
    courses.style.display = 'inline'; // do enabled/disabled instead of hidden

    if (courseList.length == 0) {
      $("multipleCoursesSelect").empty();
      var option = document.createElement("option");
      option.text="No courses available";
      option.value="None";
      option.disabled = "disabled";

      multipleCourseSelect.appendChild(option);
      $('.selectpicker').selectpicker('refresh');

    } else {
      courseList.forEach((item) => {
        var option = document.createElement("option");
        option.text = item.course_info
        option.value = item.course_id;

        multipleCourseSelect.appendChild(option);
        $('.selectpicker').selectpicker('refresh');
      });
    }
}


function retrieveCourses(obj){
    var selectPicker = document.getElementById("multipleCoursesSelect");
    $(selectPicker).selectpicker('refresh');

    var courseId = $(obj).attr('id');
    var e = document.getElementById(courseId);
    var selectedTerm = e.options[e.selectedIndex].value;

    var pageUrl = window.location.href
    var pageUrlSplit = pageUrl.split("/");
    var departmentPrefix = pageUrlSplit[5]

    if(selectedTerm){
        $.ajax({
            url: '/get_termcourses/' + selectedTerm + "/" + departmentPrefix,
            dataType: 'json',
            success: function(coursesList){
      			   fillCourses(coursesList);
      			},
      			error: function(error){
      				console.log(error);
      			}
        });
    } else {
      if (id=="selected_term_one") {
         var courses = document.getElementById("coursesDivOne");
         courses.style.visibility = 'hidden';}

      else {
           var courses = document.getElementById("coursesDiv");
           courses.style.visibility = 'hidden';// do enabled/disabled instead of hidden
         }
    }

}


$(".hide_prereqs_descrip").slideUp();
function stn(){
  //WHAT DOES THIS EVEN DO? what kind of name is this? jesus
  //I think it is for enabling/displaying/disabling/hiding elements. (Such as special topics course fields)
   var courseTitle = getSelectedCourse('courseInfo');
   if (courseTitle){
     $(".hide_prereqs_descrip").hide();
   }
   if (courseTitle === "---"){
      document.getElementById("submitAdd").disabled = true;
      $("#section_select").hide()
   }
   else{
      document.getElementById("submitAdd").disabled = false;
      var course = courseTitle.match(/\d/g).join("");
      //Then remove the numbers 86 from the string
      course = course.split("86").join("");
      var coursesDiv = document.getElementById('specialTopicCourse'); //Div for add ST course modal
      var courseCredits = document.getElementById('ccredits');
      if (course.length == 1 && courseTitle.includes("Special Topics")){
        //If the course is a special topics course
            $('#specialTopicsName').removeAttr('disabled');
            // coursesDiv.style.display = 'block';
            courseCredits.style.display = 'block';
            $('#submitSave').removeClass("hide");
             $(".hide_prereqs_descrip").show()
           }
      else {
         $('#specialTopicsName').attr('disabled','disabled');
        coursesDiv.style.display = 'none';
        courseCredits.style.display = 'none';
        $('#submitSave').addClass("hide");
         $(".hide_prereqs_descrip").hide();
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
