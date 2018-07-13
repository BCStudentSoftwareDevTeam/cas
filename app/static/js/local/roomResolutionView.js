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
function assignflasher() { //FIXME:Getting flash to show up on rresolutions, dependant on action on rresview
  document.getElementById("demo").innerHTML = "Hello World";
}


$(document).on("click", ".assignroombutton", function () { //Updating assign room modal for available rooms tab
     roomID = $(this).data('id');
     console.log(roomID);
     var linktoroom = document.getElementById("hiddenroom"+roomID);
     var linktocourse = document.getElementById("hiddencourse");
    
    
     $("#assignroomdiv").html("Are you sure you would like to assign "+ linktoroom.value + " to "+linktocourse.value); //Need course name
     
     console.log($("#assignroomdiv").innerHTML);
});

$(document).on("click",".assignprefbutton", function () { //Updating assign room modal for preferences tabs
    var prefID = $(this).data('id');
    console.log(prefID);
    var linktopref = document.getElementById("hidden"+prefID);
    console.log("link to pref"+linktopref);
    console.log("linktopref.value"+linktopref.value);
    var linktocourse = document.getElementById("hiddencourse");
    console.log(linktocourse)
    
    
    $("#assignroomdiv").html("Are you sure you would like to assign "+ linktopref.value + " to "+linktocourse.value); //Need course name
     
     console.log($("#assignroomdiv").innerHTML);
});

function submitcoursetoroom(){  //Inserting data into db AVAILABLE ROOMS ONLY
     var url = '/assignRoom/'+window.location.href.split("/").pop();
         console.log("URL: " + url);
         console.log("RoomID: " + roomID)
         $.ajax({
             type: "POST",
                url: url,
                data: {"roomID": roomID},
                dataType: 'json',
                success: function(response){
                    console.log(response)
                    window.location = "/roomResolution"
          			},
          			error: function(error){
          				console.log(error); 
          			}
                }); }
                
function replacecourseinroom(){ //Removing current occupant and playing the current course in
    var url= '/assignRoom'+window.location.href.split("/").pop;
        console.log("URL: " + url);
         console.log("RoomID: " + roomID)
    
    
}
