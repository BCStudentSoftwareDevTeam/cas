// Javascipt file for Building Management
// console.log("Javascript loaded!")

var rIDGlobal = "";
var lastRoomID = null;

function setRoomId(rid){
    rIDGlobal=parseInt(rid);
}
function getRoomId(){
    return rIDGlobal;
}

function setRoomInfo(roomID, button){
    // '''For populating panel onClick of Edit button. updateHTML is called'''
    //Sets room ID based on what room (row) Edit button was clicked
    // A new room was selected; show roomDetails

    if (roomID != lastRoomID) {
      setRoomId(roomID);
      movePanel();
      // console.log("changing RID from " + lastRoomID + " to " + roomID)
      lastRoomID = roomID;
      getRoomDetails();
      $("#roomDetails").collapse('show');
    } else {
      $("#roomDetails").collapse('toggle');
      // lastRoomID = null;
    }

}

function movePanel() {
    //Takes rID to ensure correct room per row
    //Called in setRoomInfo
    var targetDiv = document.getElementById("hiddenRow_"+getRoomId());// hidden row where content will be placed
    var sourceDiv = document.getElementById("roomDetails");// content to be placed in targetDiv
    $(targetDiv).html($(sourceDiv)); // moves modal content into current row
    // $(sourceDiv).collapse('show');
}

function updateHtml(response) {
    //Updates the HTML in panel.
    //Called in AJAX of setRoomInfo()
    // console.log("Starting updateHTML");

    $('#roomNumber').text((response['building'] + " " + response['number']).toString()).data('text');
    var my_div = document.getElementById('roomCapacity');
    my_div.value = response['capacity'];
    var my_div = document.getElementById('roomType');
    my_div.value = response['type'];
    var my_div = document.getElementById('specializedEq');
    my_div.value = response['specializedEq'];
    var my_div = document.getElementById('specialFeatures')
    my_div.value = response['specialFeatures'];
    var my_div = document.getElementById('movableFurniture');
    // console.log("moveble: ", my_div.value)
    // my_div.removeAttribute("checked"); //It was getting stuck
    if (response['movableFurniture']) {
        my_div.setAttribute("checked", "checked");
    }

    // Update the selectpickers with values from DB
    aa = $("#accessibility #audioAcc");
    va = $("#accessibility #visualAcc");
    pa = $("#accessibility #physicalAcc");
    aa.selectpicker();
    va.selectpicker();
    pa.selectpicker();
    if (response['audioAcc'] != null) {
      $("#audioAcc").selectpicker('val', response['audioAcc']);
    } else {
      $("#audioAcc").selectpicker('val', 0);
    };
    if (response['visualAcc'] != null) {
      $("#visualAcc").selectpicker('val', response['visualAcc']);
    } else {
      $("#visualAcc").selectpicker('val', 0);
    };
    if (response['physicalAcc'] != null) {
      $("#physicalAcc").selectpicker('val', response['physicalAcc']);
    } else {
      $("#physicalAcc").selectpicker('val', 0);
    };
    $("#audioAcc").selectpicker('refresh');
    $("#visualAcc").selectpicker('refresh');
    $("#physicalAcc").selectpicker('refresh');
};

function getRoomDetails() {
  // console.log(this.id + " was shown")
  if (rIDGlobal > 0){
           var url = '/getRoomData/'+rIDGlobal;
           $.ajax({
                  url: url,
                  dataType: 'json',//Corresponds with controller json dumps
                  type: "GET",
                  success: function(response){
                    // console.log(response);
                      if (response["success"] != 0) {//If successful
                          updateHtml(response);//Update the panel with the data
                          doDropzoneSetup();
                      }
                  },
                  error: function(error) {
                      console.log("Error" + error);
                  }
              });
  }
};

function doDropzoneSetup() {
  if (typeof dz != "undefined") {
    dz.remove();
    newdz = "<div id='myId' class='dropzone'></div>";
    $("#imageUploaderDiv").append(newdz);
  };
  dz = $("div#myId").dropzone({ url: "/imageUpload/" + getRoomId(),
                                renameFile: function (file) {
                                  return "room_" + getRoomId() + "_" + new Date().getTime() + '.' + file.name.split(".").pop();
                                },
                                addRemoveLinks: true,
                                parallelUploads: 1,
                                thumbnailWidth:"120",
                                thumbnailHeight:"120",
                                acceptedFiles: "image/*",
                                removedfile: function (file) {
                                  // console.log("Remove from server");
                                  $.ajax({
                                     type: "POST",
                                        url: "/removeImage",
                                        data: {"rid": getRoomId(),
                                               "file": file.name
                                              },   //Dictionary pass
                                        dataType: 'json',
                                        success: function(response){
                                          // console.log(response)
                                          file.previewElement.remove();
                                        },
                                        error: function(error){
                                          console.log(error);
                                        }
                                  });
                                },
                                init: function () {
                                  let myDropzone = this;
                                  $.ajax({
                                     type: "GET",
                                        url: "/getImages/" + getRoomId(),
                                        dataType: 'json',
                                        success: function(response){
                                          // console.log(response)
                                          for (i = 0; i < response.length; i++) {
                                            filename = response[i]["name"]
                                            fileExt = filename.split(".").pop()
                                            fileSize = response[i]["size"]
                                            var mockFile = {
                                                name: filename,
                                                type: 'image/' + fileExt,
                                                size: fileSize
                                            };

                                            myDropzone.displayExistingFile(mockFile, "/static/images/" + response[i]["name"]);
                                          }
                                        },

                                        error: function(error){
                                          console.log(error);
                                        }
                                  });
                                }});
  // console.log(getRoomId());

};

function saveChanges(roomID){
    // KEEPING FOR POSTERITIES SAKE - SH

    //Sets up datetime, passes all room attributes into a dictionary for ajax,then posts data to DB and reloads the page

    // //Datetime setup
    // var dateTime = new Date();
    // var currHour = dateTime.getHours();
    // if (currHour < 12) //AM/PM setup
    //    {
    //    a_p = "AM";
    //    }
    // else
    //    {
    //    a_p = "PM";
    //    }
    // if (currHour == 0)
    //    {
    //    currHour = 12;
    //    }
    // if (currHour > 12)
    //    {
    //    currHour = currHour - 12;
    //    }
    //
    // var currMin = dateTime.getMinutes();
    // currMin = currMin + "";
    // if (currMin.length == 1) //Getting JS to not do single digit minutes
    // {
    //     currMin = "0" + currMin;
    // }
    // var savedDateTime=(dateTime.toDateString()+",  "+ currHour + ":" +currMin + " " + a_p); //Concatenation of all date elements into one var for passing into dictionary
    //End datetime setup

    //Begin dictionary pass for Ajax
    var roomDetails = {}//For passing into Ajax data field (multiple attributes to pass)
    roomDetails["roomCapacity"] = document.getElementById('roomCapacity').value;
    roomDetails["roomType"] = document.getElementById('roomType').value;
    roomDetails["specializedEq"] = document.getElementById('specializedEq').value;
    roomDetails["specialFeatures"] = document.getElementById('specialFeatures').value;
    roomDetails["movableFurniture"] = document.getElementById('movableFurniture').checked;
    roomDetails["visualAcc"] = $('#visualAcc option:selected').text();
    roomDetails["audioAcc"] = $('#audioAcc option:selected').text();
    roomDetails["physicalAcc"] = $('#physicalAcc option:selected').text();

    var url = '/saveChanges/'+getRoomId();
    $.ajax({
       type: "POST",
          url: url,
          data: roomDetails,                              //Dictionary pass
          dataType: 'json',
          success: function(response){
                  window.location = "/buildingManagement" //Refresh page
          },
          error: function(error){
              console.log("ERROR" + error)
              window.location.assign("/buildingManagement")
          }
    });


}


  /*sets the radio checkbox for education tech for each room*/
function education_detail(response){
    console.log("Starting ed tech filling");
    var my_div = document.getElementById('projectors');
    my_div.value = response['projector'];
    var my_div = document.getElementById('smartboards');
    my_div.value = response['smartboards'];
    var my_div = document.getElementById('instructor_computers');
    my_div.value = response['instructor_computers'];
    var my_div = document.getElementById('podiums');
    my_div.value = response['podium'];
    var my_div = document.getElementById('student_workspace');
    my_div.value = response['student_workspace'];
    var my_div = document.getElementById('chalkboards');
    my_div.value = response['chalkboards'];
     var my_div = document.getElementById('whiteboards');
    my_div.value = response['whiteboards'];

    var my_div1 = $("#vhs");
    if (response['vhs']) {
	my_div1.prop('checked', true);
    } else {
	my_div1.prop('checked', false);

    }

    var my_div1 = $("#dvd");
    if (response['dvd']) {
	my_div1.prop('checked', true);
    } else {
	my_div1.prop('checked', false);

    }

    var my_div1 = $("#blu_ray");
    if (response['blu_ray']) {
	my_div1.prop('checked', true);
    } else {
	my_div1.prop('checked', false);

    }

    var my_div1 = $("#doc_cam");
    if (response['doc_cam']) {
	my_div1.prop('checked', true);
    } else {
	my_div1.prop('checked', false);

    }

     var my_div1 = $("#extro");
    if (response['extro']) {
	my_div1.prop('checked', true);
    } else {
	my_div1.prop('checked', false);

    }

    var my_div1 = $("#audio");
    if (response['audio']) {
	my_div1.prop('checked', true);
    } else {
	my_div1.prop('checked', false);

    }

    var my_div1 = $("#mondopad");
    if (response['mondopad']) {
	my_div1.prop('checked', true);
    } else {
	my_div1.prop('checked', false);

    }

    var my_div1 = $("#tech_chart");
    if (response['tech_chart']) {
	my_div1.prop('checked', true);
    } else {
	my_div1.prop('checked', false);

    }

}

/*This function serves to take data from the python
file and dumps into html file on the UI after taking from the education_detail()*/
function seteducationTech() {
    setRoomId(getRoomId());
    if(getRoomId()){
         var url = '/getEducationData/'+ getRoomId();
        //  console.log(url)
         $.ajax({
                url: url,
                dataType: 'json',
                type:'GET',
                success: function(response){
                     if (response["success"] != 0) {//If successful
			                  education_detail(response); //a function with education tech details
                                                    }
                },
                error: function(error) {
                console.log(error);
                }
            });
    }
}

    /*this functions saves the edecuationtech materials on the front-end and updated them as thier values change*/
function saveEdTechChanges(roomID){
    var edtechDetails = {}//For passing into Ajax data field (multiple attributes to pass)
    edtechDetails["projector"] = document.getElementById('projectors').value;
    edtechDetails["smartboards"] = document.getElementById('smartboards').value;
    edtechDetails["instructor_computers"] = document.getElementById('instructor_computers').value;
    edtechDetails["podium"] = document.getElementById('podiums').value;
    edtechDetails["student_workspace"] = document.getElementById('student_workspace').value;
    edtechDetails["chalkboards"] = document.getElementById('chalkboards').value;
    edtechDetails["whiteboards"] = document.getElementById('whiteboards').value;
    edtechDetails["vhs"] = document.getElementById('vhs').checked;
    edtechDetails["dvd"] = document.getElementById('dvd').checked;
    edtechDetails["blu_ray"] = document.getElementById('blu_ray').checked;
    edtechDetails["audio"] = document.getElementById('audio').checked;
    edtechDetails["mondopad"] = document.getElementById('mondopad').checked;
    edtechDetails["doc_cam"] = document.getElementById('doc_cam').checked;
    edtechDetails["extro"] = document.getElementById('extro').checked;
    edtechDetails["tech_chart"] = document.getElementById('tech_chart').checked;
    var url = '/saveEdTechChanges/'+getRoomId();
         $.ajax({
             type: "POST",
                url: url,
                data: edtechDetails,
                dataType: 'json',
                success: function(response){
                    if (response["success"] != 0) {
                        console.log("SUCCESSFUL JS AJAX CALL")
                    }
                    else{

                        console.log("Else in ajax")
                    }
                },
                error: function(error){
                    console.log("ERROR")

                }
         });
}


/* keeps tracks of active modals, making sure that they remain responsive after closing an overlaying instance*/
var modal_counter = 0;
$(document).ready(function () {
  Dropzone.options.myId = false;

  $('.modal').on('shown.bs.modal', function () {
      modal_counter++;
  });
  $('.modal').on('hidden.bs.modal', function () {
      modal_counter--;
      if(modal_counter){
          $('body').addClass('modal-open');
      }
      else{
          $('body').removeClass('modal-open');
      }
  });
})
