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

function closealert(){
$("#dismiss").alert('fade');
};
 

 
$('#code').on('shown.bs.modal', function (e) {
  showalert()// do something...
})



function assignflasher() { //Getting flash to show up on rresolutions, dependant on action on rresview
  document.getElementById("demo").innerHTML = "Hello World";
}

function updatemodal(){ //For switching value in assign modal (Are you sure you want to assign (user select) to course CSC-236?)
  
}


$(document).on("click", ".assignroombutton", function () {
     var roomID = $(this).data('id');
     console.log(roomID);
     var linktoroom = document.getElementById("hidden"+roomID);
    console.log(linktoroom);
    console.log(linktoroom.innerText);
    console.log(linktoroom.innerHTML);
    console.log(linktoroom.value);
    
    
     $("#assignroomdiv").html("Are you sure you would like to assign this course to "+ linktoroom.value); //Need course name
     
     console.log($("#assignroomdiv").innerHTML);
})