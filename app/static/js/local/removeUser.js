/* global $ */
console.log("removeUser js loaded")

// These lines of code enables the interface to show only the access level first
$("#Programs").hide();
$("#Divisions").hide();
$("#Buildings").hide();
$("#Add").hide();
$("#Remove").hide(); 

//Shows appropriate 2nd dropdown based on first dropdown selection
function show_access_level(s) {
        console.log(s.value);
        $("#Programs").hide();
        $("#Divisions").hide();
        $("#Buildings").hide();
        $("#Add").hide();
        $("#Remove").hide();  
    
        if (s.value == "program_chair"){
            $("#Programs").show();
        }
        else if (s.value == "division_chair"){
            $("#Divisions").show();
        }
        else if(s.value == "building_manager"){
            $("#Buildings").show();
        }
        else if(s.value == "administrator"){
             retrieveAdmins();
             $("#Add").show();
             $("#Remove").show();
        }
    }

//Program chair remove field
function fillProgramChairs(response){
    console.log(response)
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
        programselect.appendChild(option);
    } 
    // $('.selectpicker').selectpicker('refresh');
}

function retrievePrograms(obj){
     var selected_program = obj.value;
     console.log("Selected program: " + selected_program)
     if(selected_program){
        
         var url = '/get_program_chairs/'+selected_program;
         console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    console.log(response)
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
}
//Division Chair remove field
function fillDivisionChairs(response){
    console.log(response)
    var divisionselect = document.getElementById("RemoveDropdown");
    $("#RemoveDropdown").empty();
    for (var key in response){
        // console.log(response[key]['firstname']);
        var option = document.createElement("option");
        option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+" ("+response[key]["username"].toString() + ")";
        option.value = key;
        divisionselect.appendChild(option);
    }
    // $('.selectpicker').selectpicker('refresh');
}
function retrieveDivisions(obj){
    console.log(obj.value)
     var selected_division = obj.value;
     console.log("Selected division: " + selected_division)
     if(selected_division){
        
         var url = '/get_division_chairs/'+selected_division;
         console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    console.log(response)
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
        }
        
//Building Manager Remove Field
function fillBuildingManagers(response){
    console.log(response)
    var buildingselect = document.getElementById("RemoveDropdown");
    $("#RemoveDropdown").empty();
    for (var key in response){
        // console.log(response[key]['firstname']);
        var option = document.createElement("option");
        option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+" ("+response[key]["username"].toString() +")";
        option.value = key;
        buildingselect.appendChild(option);
    }
    // $('.selectpicker').selectpicker('refresh');
}
 

function retrieveBuildings(obj){
    console.log(obj.value)
     var selected_building = obj.value;
     console.log("Selected building: " + selected_building)
     if(selected_building){
        
         var url = '/get_building_managers/'+selected_building;
         console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    console.log(response)
          		    fillBuildingManagers(response);
          			},
          			error: function(error){
          				console.log(error); 
          			}
                }); }
}

function building_managers_show_names(s) { 
            console.log("Got to show names")
            retrieveBuildings(s);
            $("#Add").show();
            $("#Remove").show();
        }


function fillAdmin(response){
    console.log(response)
    var adminselect = document.getElementById("RemoveDropdown");
    $("#RemoveDropdown").empty();
    for (var key in response){
        // console.log(response[key]['firstname']);
        var option = document.createElement("option");
        option.text=response[key]["firstname"].toString()+" "+response[key]["lastname"].toString()+" ("+ response[key]["username"].toString() + ")";
        option.value = key;
        adminselect.appendChild(option);
    }
    // $('.selectpicker').selectpicker('refresh');
}

function retrieveAdmins(){
         var url = '/get_admin/';
         console.log("URL: " + url);
         $.ajax({
                url: url,
                dataType: 'json',
                success: function(response){
                    console.log(response)
          		    fillAdmin(response);
          			},
          			error: function(error){
          				console.log(error); 
          			}
                }); }    


/*global $ */
// this creates the pop up for remove button
$(function() {
   $( "#openDialog").on("click", function(){ 
       $( "#dialog-modal" ).dialog({
          height: 180,
          width: 470,
          modal: true,
        });
        $("#dialog-modal").dialog({
      buttons : {
        "Yes" : function() {
          $(this).dialog("close");
        },
        "No" : function() {
            $(this).dialog("close");
        }
      }
    });
       $( "#dialog-modal" ).show();
    });
 });

$(function() {
   $( "#openDialog1").on("click", function(){ 
       $( "#dialog-modal1" ).dialog({
          height: 180,
          width: 470,
          modal: true,
        });
        $("#dialog-modal1").dialog({
      buttons : {
        "Yes" : function() {
          $(this).dialog("close");
        },
        "No" : function() {
            $(this).dialog("close");
        }
      }
    });
       $( "#dialog-modal1" ).show();
    });
 });
 

