/* global $ */
// console.log("removeUser js loaded")

// These lines of code enables the interface to show only the access level first
$("#Programs").hide();
$("#Divisions").hide();
$("#Buildings").hide();
$("#Add").hide();
$("#Remove").hide();
var programs_prev_selected = divisions_prev_selected = buildings_prev_selected = false;

//Shows appropriate 2nd dropdown based on first dropdown selection
function show_access_level(s) {
        // console.log(s.value);
        $("#Programs").hide();
        $("#Divisions").hide();
        $("#Buildings").hide();
        $("#Add").hide();
        $("#Remove").hide();

        if (s.value == "program_chair"){
            $("#Programs").show();
            if (programs_prev_selected === true) {
              $("#Add").show();
              $("#Remove").show();
            }
        }
        else if (s.value == "division_chair"){
            $("#Divisions").show();
            if (divisions_prev_selected === true) {
              $("#Add").show();
              $("#Remove").show();
            }
        }
        else if(s.value == "building_manager"){
            $("#Buildings").show();
            if (buildings_prev_selected === true) {
              $("#Add").show();
              $("#Remove").show();
            }
        }
        else if(s.value == "administrator"){
             retrieveAdmins();
             $("#Add").show();
             $("#Remove").show();
        }
    }

//Program chair remove field
function fillProgramChairs(response){
    // console.log(response)
    var programselect = document.getElementById("RemoveDropdown");
    $("#RemoveDropdown").empty();
    var option = document.createElement("option");
    option.disabled = true;
    option.selected = true;
    option.text="---";
    option.value = "---";
    programselect.appendChild(option);

    for (var key in response){
        // console.log(response[key]['firstname']);
        var option = document.createElement("option");
        option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+"(" + response[key]["username"].toString() + ")";
        option.value = key;
        programselect.appendChild(option); //adds the selected user to program chair list
    }
    $('.selectpicker').selectpicker('refresh');
}

function retrievePrograms(obj){
     var selected_program = obj.value;
     if(selected_program){
         var url = '/get_program_chairs/'+selected_program;
        //  console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    // console.log(response)
          		    fillProgramChairs(response);
          			},
          			error: function(error){
          				console.log(error);
          			}
                }); }
}

function program_chairs_show_names(s) { //Called in HTML
            retrievePrograms(s);
            $("#Add").show();
            $("#Remove").show();
            programs_prev_selected = true;
}
//Division Chair remove field
function fillDivisionChairs(response){
    // console.log(response)
    var divisionselect = document.getElementById("RemoveDropdown");
    $("#RemoveDropdown").empty();
    var option = document.createElement("option");
    option.disabled = true;
    option.selected = true;
    option.text="---";
    option.value = "---";
    divisionselect.appendChild(option);
    for (var key in response){
        var option = document.createElement("option");
        option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+" ("+response[key]["username"].toString() + ")";
        option.value = key;
        divisionselect.appendChild(option); //adds the selected user to division chair
    }
    $('.selectpicker').selectpicker('refresh');
}
function retrieveDivisions(obj){
    console.log(obj.value)
    var selected_division = obj.value;
    if(selected_division){
        var url = '/get_division_chairs/'+selected_division;
        // console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    // console.log(response)
          		    fillDivisionChairs(response);
          			},
          			error: function(error){
          				console.log(error);
          			}
                }); }
}
 function division_chairs_show_names(s) { //Called in html
            retrieveDivisions(s);
            $("#Add").show();
            $("#Remove").show();
            divisions_prev_selected = true;
        }

//Building Manager Remove Field
function fillBuildingManagers(response){
    // console.log(response)
    var buildingselect = document.getElementById("RemoveDropdown");
    $("#RemoveDropdown").empty();
    var option = document.createElement("option");
    option.disabled = true;
    option.selected = true;
    option.text="---";
    option.value = "---";
    buildingselect.appendChild(option);
    for (var key in response){
        // console.log(response[key]['firstname']);
        var option = document.createElement("option");
        option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+" ("+response[key]["username"].toString() +")";
        option.value = key;
        buildingselect.appendChild(option);  //adds the selected user to building managers
    }
    $('.selectpicker').selectpicker('refresh');
}


function retrieveBuildings(obj){
    // console.log(obj.value)
    var selected_building = obj.value;
    console.log("Selected building: " + selected_building)
    if(selected_building){

         var url = '/get_building_managers/'+selected_building;
         console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
          		    fillBuildingManagers(response);
          			},
          			error: function(error){
          				console.log(error);
          			}
                }); }
}

function building_managers_show_names(s) {
    retrieveBuildings(s);
    $("#Add").show();
    $("#Remove").show();
    buildings_prev_selected = true;
    }


function fillAdmin(response){
    // console.log(response)
    var adminselect = document.getElementById("RemoveDropdown")
        $("#RemoveDropdown").empty();
        var count = 0;
        for (var key in response){
            // console.log(response[key]['firstname']);
            count = count + 1;
            var option = document.createElement("option");
                option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+" ("+ response[key]["username"].toString() + ")";
                option.value = key;
                adminselect.appendChild(option); //adds the selected user as Admin
        }
        if (count < 2) {
            //disables the remove button if there is only one admin so that all the users are not locked out of the system
            var disable_btn = document.getElementById("adminbtn");
            disable_btn.disabled = true;
        }

    $('.selectpicker').selectpicker('refresh');
}

function retrieveAdmins(){
     var url = '/get_admin/';
    //  console.log("URL: " + url);
     $.ajax({
            url: url,
            dataType: 'json',
            success: function(response){
                // console.log(response)
      		    fillAdmin(response);
      			},
      			error: function(error){
      				console.log(error);
      			}
            }); }
