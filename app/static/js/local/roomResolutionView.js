console.log('I have been loaded!')
// function() {
  // ("#accordion").show().accordion({
  //     active: false,
  //     autoHeight: false,
  //     navigation: true,
  //     collapsible: true
  // });
  // });
  // window.alert('Your eroimn saved!');
  // var secretDiv = document.getElementById('here');
  // console.log(secretDiv)
  // function hidealert(){
  //   secretDiv.style.visibility = 'hidden';
  // }
      // Hide


// function showalert() { 
// secretDiv.style.visibility = 'visible';     // Show
// };

// function closealert(){
// $("#dismiss").alert('fade');
// };
 

 
// $('#code').on('shown.bs.modal', function (e) {
//   showalert()// do something...
// })


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
     
     console.log($("#assignroomdiv").innerHTML);
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
    
    // var which_room = document.getElementById("hidden") //Which room the preference is referring to
    // console.log("which_room.value"+which_room.value);
    
    // var which_course = document.getElementById("hidden") //Course ID of the room that ia currently occupying that room
    // console.log("which_course.value"+which_course.value);
    
    
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
        submitcoursetoroom()
    }
    else{
        replacecourseinroom()    
        }
    }
function submitcoursetoroom(){  //Inserting data into db AVAILABLE ROOMS ONLY
     var url = '/assignRoom/'+window.location.href.split("/").pop();
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
                    // window.location = "/roomResolution"
          			},
          			error: function(error){
          				console.log(error); 
          			}
                }); }
                
function replacecourseinroom(){ //Removing current occupant and putting the current course in
    var url= '/updateRoom/'+window.location.href.split("/").pop();
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
                    // window.location = "/roomResolution"
                    },
                    error: function(error){
                        console.log(error);
                    }
                
                
        });}
