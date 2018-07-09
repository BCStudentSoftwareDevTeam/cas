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