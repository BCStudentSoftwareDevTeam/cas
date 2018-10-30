
let roomID="";
let ogCourse="";

$('.accordion').keydown(function(event) {
   var keyCode = event.which; // Capture which key was pressed
   switch(keyCode){
                
      case 13: case 32:
         // Either the enter key or space bar was pressed
         // You should toggle the focused accordion.
         // If it is open, close it now; if it is closed, open it now.
        row = $($(this)[0]).attr("id").split("row")[1];
        allDivs = $("#accordion")
        for (divs in allDivs) {
            if (($("#collapse"+row).addClass('in'))){
                $(this).collapse('show');
            }
            $(this).collapse('hide');                                   
        }
        break;

      default:
         // A key was pressed, but it is not actionable
   }
});


 //Updating assign room modal for available rooms tab
$(document).on("click", ".assignroombutton", function () {
     roomID = $(this).data('id');
     let linktoroom = document.getElementById("hiddenroom"+roomID);
     let linktocourse = document.getElementById("hiddencourse");
     $("#assignroomdiv").html("Are you sure you would like to assign "+ linktoroom.value + " to "+linktocourse.value); 
  
});

//Assign second room to conflict room  
$(document).on("click", ".assignconflicting", function () {
     roomID = $(this).data('id');
     let linktoroom = document.getElementById("hiddenroom"+roomID);
     let linktocourse = document.getElementById("hiddencourse");
     $("#assignConfDiv").html("WARNING: Are you sure you want to assign "+ linktoroom.value + " to "+linktocourse.value+"? The room will have more than one course in it."); 
  
});

 //Updating assign room modal for preferences tabs
$(document).on("click",".assignprefbutton", function () {
    let prefID = $(this).data('id');                                    //Preference ID (1,2,or3)
    let main_course = window.location.href.split("/").pop();            //Grabbing Course A's ID
    ogCourse = "";
    let conflictingcourse = document.getElementById("pref"+ prefID +"_confcourse"); //Seeing if there is a conflicting course
    let room = document.getElementById("pref" + prefID + "_room").value //Pulls room from hidden value from html
    roomID = room
    let which_preference = document.getElementById("hidden"+ room)       //Which preference you have selected
    let linktopref = document.getElementById("hidden"+room);
    let linktocourse = document.getElementById("hiddencourse");         //Course A
    if (conflictingcourse != null){                                     //If there is a conflicting course set it to ogCourse
        conflictingcourse = conflictingcourse.value;
        ogCourse = conflictingcourse;
        $("#assignConflictingDiv").html("<p>Are you sure you would like to assign "+ which_preference.value + " to "+linktocourse.value + "?</p>"); //Need course name);
    }
    else
    {
    
        $("#assignroomdiv").html("<p>Are you sure you would like to assign "+ which_preference.value + " to "+linktocourse.value + "?</p>"); //Need course name);  
    }
        
    });

//assign room to a course
function assignRoomCourse() {  //Inserting data into db AVAILABLE ROOMS ONLY
    let oldurl = window.location.href.split("/");
    let cid = oldurl[oldurl.length-1];
    let termcode = oldurl[oldurl.length-2];
    let url = '/assignRoom/'+cid;  
         $.ajax({
             type: "POST",
                url: url,
                data: {"roomID": roomID},
                dataType: 'json',
                success: function(response){ 
                     if (response['success'] == 1)
                        window.location = "/roomResolution/"+termcode
                    else{
                        window.location.assign("/roomResolution/"+ termcode)                    
                        }
                        
                    },
          			error: function(error){
          			    window.location.assign("/roomResolution/"+ termcode)
          			}
                }); }
                
//assign the preference room to a course and redirect to conflicted course
function resolveCourse() { 
    let oldurl = window.location.href.split("/");
    let cid = oldurl[oldurl.length-1];
    let termcode = oldurl[oldurl.length-2];
    let url = '/updateRoom/'+cid;  
    $.ajax({  
            type: "POST",
            url: url,
            data:{"roomID": roomID, "ogCourse": ogCourse},
            dataType: 'json'
         })
           .done(function(response){
                         window.location=response.url;}) 
           .fail(function(response){
                    alert("Please, try again.");});
}
      
function addSecond(){
    let oldurl = window.location.href.split("/");
    let cid = oldurl[oldurl.length-1];
    let termcode = oldurl[oldurl.length-2];
    let url = '/addSecond/'+cid;    
    $.ajax({  
            type: "POST",
            url: url,
            data:{"roomID": roomID},
            dataType: 'json'
         })
           .done(function(response){
                if (response['success'] == 1)
                        window.location = "/roomResolution/"+termcode
                    else{
                        window.location.assign("/roomResolution/"+ termcode)                    
                        }         
               
           }) 
           .fail(function(response){
                     window.location.assign("/roomResolution/"+ termcode);});
}
    