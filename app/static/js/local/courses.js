console.log("course js loaded")

function getSelectedCourse(elementId) {
   var selectedCourse = document.getElementById(elementId);

   if (selectedCourse.selectedIndex == -1){
      return null;
   }
   return selectedCourse.options[selectedCourse.selectedIndex].text;

}
function fillCourses(response, id){
//   console.log('Response', response);
    var selectPicker = document.getElementById("multipleCoursesSelect");
        
    $(selectPicker).find('option').remove();
    $(selectPicker).selectpicker('refresh');
   if (response !== "Error"){
        var courses = document.getElementById("coursesDiv");
        courses.style.display = 'inline';// do enabled/disabled instead of hidden
        
        for (var key in response){
            var option = document.createElement("option");
            /*CSC 111 - COURSE NAME (startTime - endTime) [instructor_lastname]*/
            // console.log("Course: ", response[key]);
            //  console.log(response[key].schedule_object);
            option.text=response[key].prefix["prefix"].toString()+" "+response[key].bannerRef["number"].toString();
            if (response[key].section != null && response[key].section != "None") {
                // console.log("Section: ", response[key].section);
                option.text+=" " + response[key].section;
            }
            option.text+=" - "+response[key].bannerRef["ctitle"].toString()
            // Add schedule, if it exists
            if (response[key].schedule_object == true){
                // console.log("Start time: ", response[key].schedule['startTime'] )
                option.text += " (" +response[key].schedule['startTime'] + "-" +response[key].schedule['endTime']+")" ;
            }
            
            // Add Instructors, if they exist
            if (response[key].instructors != null && response[key].instructors.length > 0) {
                // console.log(response[key].instructors);
                option.text += " [";
                first = true;
                for (inst in response[key].instructors) {
                    // console.log(response[key].instructors[inst]);
                    if (first) {
                        option.text += response[key].instructors[inst];    
                        first = !first;
                    } else {
                        option.text += ", " + response[key].instructors[inst];    
                    }
                    
                }
                option.text += "]";
            }
            
            option.value = key;
            selectPicker.appendChild(option);
            $('.selectpicker').selectpicker('refresh');
        }    
    } else{
         $("multipleCoursesSelect").empty();
         var selectPicker = document.getElementById("multipleCoursesSelect");
         var option = document.createElement("option");
         option.text="No courses available";
         option.key="None";
         option.disabled = "disabled";
        //  console.log("return value is None");
         selectPicker.appendChild(option);

         $('.selectpicker').selectpicker('refresh');
    }
}


function retrieveCourses(obj){
    var selectPicker = document.getElementById("multipleCoursesSelect");
    
    //$(selectPicker).find('option').remove();
    $(selectPicker).selectpicker('refresh');
    console.log("Retrieve courses is called!")
    var id = $(obj).attr('id');
    var x = window.location.href
    var y =x.split("/"); 
    var e = document.getElementById(id);
    var selected_term = e.options[e.selectedIndex].value;
    //   console.log('selected_term', selected_term)
    if(selected_term){
        $.ajax({
            url: '/get_termcourses/'+selected_term+"/"+y[5],
            dataType: 'json',
            success: function(response){
                // console.log('Response', response)
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
      var coursesDiv = document.getElementById('specialTopicCourse');
      var courseCredits = document.getElementById('ccredits');
      if (course.length == 1 && courseTitle.includes("Special Topics")){
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
