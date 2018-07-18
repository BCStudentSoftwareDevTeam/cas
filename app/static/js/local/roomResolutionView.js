console.log('I have been loaded!')

var roomID="";
var ogCourse="";
function assignflasher() { //FIXME:Getting flash to show up on rresolutions, dependant on action on rresview
  document.getElementById("demo").innerHTML = "Hello World";
}

 //Updating assign room modal for available rooms tab
$(document).on("click", ".assignroombutton", function () {
     roomID = $(this).data('id');
     console.log(roomID);
     var linktoroom = document.getElementById("hiddenroom"+roomID);
     var linktocourse = document.getElementById("hiddencourse");
    
    
     $("#assignroomdiv").html("Are you sure you would like to assign "+ linktoroom.value + " to "+linktocourse.value); //Need course name
     
    //  console.log($("#assignroomdiv"));
});
 //Updating assign room modal for preferences tabs
$(document).on("click",".assignprefbutton", function () {
    var prefID = $(this).data('id'); //Preference ID (1,2,or3)
    console.log(prefID);
    //NEED TO GET ROOM INFO, PREF INFO, and CONFLICTING COURSE INFO
    var main_course = window.location.href.split("/").pop();
    console.log("main course: " + main_course)
    ogCourse = "";
    var conflictingcourse = document.getElementById("pref"+ prefID +"_confcourse");
    console.log(conflictingcourse == null); //null
    if (conflictingcourse != null){
        conflictingcourse = conflictingcourse.value;
        console.log("conflicting course:" + conflictingcourse)
        ogCourse = conflictingcourse;
    }
    var room = document.getElementById("pref" + prefID + "_roominfo").value
    roomID = room
    console.log("room:"+ room)
    var which_preference = document.getElementById("hidden"+ room) //Which preference you have selected
    console.log("which_preference.value"+which_preference.value);
   
    
    
    // // var linktopref = document.getElementById("hidden"+prefID);
    // // console.log("link to pref"+linktopref);
    // // console.log("linktopref.value"+linktopref.value);
    var linktocourse = document.getElementById("hiddencourse"); //Course A
    
    // // console.log(linktocourse)
    
    
    
    $("#assignroomdiv").html("Are you sure you would like to assign "+ which_preference.value + " to "+linktocourse.value + "?"); //Need course name
     
     console.log($("#assignroomdiv").innerHTML);
});
function submitorreplace(){
    if (ogCourse == ""){
        submitcoursetoroom();
    }
    else{
        replacecourseinroom();    
        }
    }
function submitcoursetoroom(){  //Inserting data into db AVAILABLE ROOMS ONLY
    var oldurl = window.location.href.split("/");
    var cid = oldurl[oldurl.length-1];
    var termcode = oldurl[oldurl.length-2];
    console.log("cid: " + cid);
    console.log("term code: " + termcode);
    var url = '/assignRoom/'+cid;  
         console.log("URL: " + url);
         console.log("RoomID: " + roomID)
         console.log("Inside submitcoursetoroom")
         $.ajax({
             type: "POST",
                url: url,
                data: {"roomID": roomID},
                dataType: 'json',
                success: function(response){ 
                    console.log(response)
                    console.log("It worked")
                    window.location = "/roomResolution/"+termcode
          			},
          			error: function(error){
          			    console.log("It didnt work")
          				console.log(error); 
          			}
                }); }
                
function replacecourseinroom(){ //Removing current occupant and putting the current course in
    var oldurl = window.location.href.split("/");
    var cid = oldurl[oldurl.length-1];
    var termcode = oldurl[oldurl.length-2];
    var url = '/updateRoom/'+cid;  
        console.log("URL: " + url);
        console.log("RoomID: " + roomID);
        console.log("Inside replacecourseinroom")
        $.ajax({  
             type: "POST",
                url: url,
                data:{"roomID": roomID, "ogCourse": ogCourse},
                dataType: 'json',
                success: function(response){
                    console.log(response)
                    console.log("It worked")
                    window.location = "/roomResolution/"+ termcode
                    },
                    error: function(error){
                        console.log("It didnt work")
                        console.log(error);
                    }
                
                
        });}
        
        
// function RedirectURL()
// {
//     window.location= createDynamicURL();
    
    
    
// }
