$(document).ready(function() {/* This function sets the focus of the enter and tab key. 
Then it graphs all the collapse alements to expand whenever the eneter key is pressed. This function created the make accessable for screen readers to
to use only enter and tab key to display all the information in each collapse*/
    $(this).keydown(function(e) {
        if(e.keyCode == 13 || e.keyCode == 32) { 
            console.log(this);
            row = $($(document.activeElement)[0]).attr("id").split("row")[1];
            // Sometimes you tab on the button, sometimes the h4. Now, it doesn't care
            if (!row) {
                row = $($(document.activeElement)[0]).attr("id").split("linkto")[1];
            }
            collapserow = $("#collapse"+row);
            if (collapserow.hasClass("in")){
                collapserow.removeClass("in");
            } else {
                $(".in").each(function(i) {
                    $(this).removeClass("in");
                  });
                collapserow.addClass("in");
            }
        }
    });
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
    console.log("conflictingcourse", conflictingcourse);
    let room = document.getElementById("pref" + prefID + "_room").value //Pulls room from hidden value from html
    roomID = room;
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
    