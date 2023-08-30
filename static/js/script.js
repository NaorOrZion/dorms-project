  const createRoomSetting = (apt_id="newApt", selectedRoomsQuantity_value = null, roomsSettings_id = "") => {
    const roomsSettings = document.getElementById("roomsSettings" + roomsSettings_id);
    var selectedRoomsQuantity = document.getElementById("roomSelection" + roomsSettings_id).value;

    if(selectedRoomsQuantity_value != null){
      selectedRoomsQuantity = selectedRoomsQuantity_value;
    }

    roomsSettings.innerHTML = ``;

    if (selectedRoomsQuantity > 9) {
      selectedRoomsQuantity = 9;
    } else if (selectedRoomsQuantity <= 0 || isNaN(selectedRoomsQuantity)) {
      selectedRoomsQuantity = 0;
    }

    var content = "";
    for (let i = 1; i <= selectedRoomsQuantity; i++) {
      content +=  `
        <hr style="width:80%;height:2px;background-color:gray">
        <label class="col-form-label col-form-label-lg">חדר ` + i + `</label>
        <br>
        <label for="bunkBedSelection-` + apt_id + `-` + i + `" class="form-label mt-4">
          <strong>כמות מיטות קומותיים</strong>
        </label>
        <select class="form-select selectpicker-disable" name="bunkBedSelection-` + apt_id + `-` + i + `" id="bunkBedSelection-` + apt_id + `-` + i + `" style="width:17%" onchange="createBunkBedInfo('` + apt_id + `', ` + selectedRoomsQuantity_value + `, null, '` + roomsSettings_id +`');" onfocus="this.selectedIndex = -1;">
          <option selected>0</option>
          <option>1</option>
          <option>2</option>
          <option>3</option>
          <option>4</option>
        </select>

        <!-- Bunk bed info start -->
        <div name="bunkBedInfo-` + apt_id + `-` + i + `" id="bunkBedInfo-` + apt_id + `-` + i + `">
        </div>
        <!-- Bunk bed info end -->

        <label for="aminachBedSelection-` + apt_id + `-` + i + `" class="form-label mt-4">
          <strong>כמות מיטות עמינח</strong>
        </label>
        <select class="form-select selectpicker-disable" name="aminachBedSelection-` + apt_id + `-` + i + `" id="aminachBedSelection-` + apt_id + `-` + i + `" style="width:17%" onchange="createAminachBedInfo('` + apt_id + `', ` + selectedRoomsQuantity_value + `, null, '` + roomsSettings_id +`');" onfocus="this.selectedIndex = -1;">
          <option selected>0</option>
          <option>1</option>
          <option>2</option>
          <option>3</option>
          <option>4</option>
        </select>
        <!-- Aminach bed info start -->
        <div name="aminachBedInfo-` + apt_id + `-` + i + `" id="aminachBedInfo-` + apt_id + `-` + i + `">
        </div>
        <!-- Aminach bed info end -->
        <br>
      `;

    }
    
    roomsSettings.innerHTML += content;
    $('.selectpicker').selectpicker('refresh');
  };


const createBunkBedInfo = (apt_id="newApt", selectedRoomsQuantity_value = null, roomsData = null, roomSelectionId = "") => {
    var selectedRoomsQuantity = document.getElementById("roomSelection" + roomSelectionId).value;

    if(selectedRoomsQuantity_value != null){
      selectedRoomsQuantity = selectedRoomsQuantity_value;
    }

    if (selectedRoomsQuantity > 9) {
      selectedRoomsQuantity = 9;
    } else if (selectedRoomsQuantity <= 0 || isNaN(selectedRoomsQuantity)) {
      selectedRoomsQuantity = 1;
    }

    for (let i = 1; i <= selectedRoomsQuantity; i++) {
      // Wrap the code inside the for loop in an IIFE to create a new scope
      (function(i) {
        const BedInfoDiv = document.getElementById("bunkBedInfo-" + apt_id + "-" + i);
        const selectedBunkBed = document.getElementById("bunkBedSelection-" + apt_id + "-" + i);
        var selectedBunkBedQuantity = selectedBunkBed.value;
        var residentsInRoom = null;

        if(selectedBunkBedQuantity < 0 || isNaN(selectedBunkBedQuantity)) {
          selectedBunkBedQuantity = 0;
        } else if(selectedBunkBedQuantity > 4) {
          selectedBunkBedQuantity = 4;
        }

        if(roomsData != null) {
          selectedBunkBedQuantity = Object.keys(roomsData[i][0]).length;

          // If there is at least one bunk bed in a room then retrieve the data of the residents sleeping on the bed
          if(selectedBunkBedQuantity > 0) {
            residentsInRoom = roomsData[i][0];

            // Set the selected value of the select picker
            $(`#bunkBedSelection-${apt_id}-${i}`).val(selectedBunkBedQuantity);
          }
        }

        BedInfoDiv.innerHTML = ``;
        var content = "";

        for (let j = 1; j <= selectedBunkBedQuantity; j++) {
          content += `
            <label class="col-form-label col-form-label-sm mt-4" for="inputBunkBed-` + apt_id + `-` + i + `-` + j + `">שמות מיטת קומותיים</label>
            <div class="container pb-2">
              <select class="selectpicker selectpicker-disable selectpicker-bunk-bed-` + apt_id + `-` + i + `" data-width="65%" data-live-search="true" name="inputBunkBed1-` + apt_id + `-` + i + `-` + j + `" id="inputBunkBed1-` + apt_id + `-` + i + `-` + j + `">
              </select>
            </div>
            <div class="container pb-2">
              <select class="selectpicker selectpicker-disable selectpicker-bunk-bed-` + apt_id + `-` + i + `" data-width="65%" data-live-search="true" name="inputBunkBed2-` + apt_id + `-` + i + `-` + j + `" id="inputBunkBed2-` + apt_id + `-` + i + `-` + j + `">
              </select>
            </div>
          `;
        }
        
        BedInfoDiv.innerHTML += content;
        
        // Populate the select pickers with options and wait for the Promise to resolve
        populateDropdownResidentsOptions(`.selectpicker-bunk-bed-${apt_id}-${i}`).then(() => {
          if(residentsInRoom != null) {
            for (let j = 1; j <= selectedBunkBedQuantity; j++) {      
              resident1 = residentsInRoom[j][0];
              resident2 = residentsInRoom[j][1];

              $(`#inputBunkBed1-${apt_id}-${i}-${j}`).val(resident1);
              $(`#inputBunkBed2-${apt_id}-${i}-${j}`).val(resident2);
            }

            $(`.selectpicker-bunk-bed-${apt_id}-${i}`).selectpicker('refresh');
          }
        });
      })(i);
    }
  };

  const createAminachBedInfo = (apt_id="newApt", selectedRoomsQuantity_value = null, roomsData = null, roomSelectionId = "") => {
    var selectedRoomsQuantity = document.getElementById("roomSelection" + roomSelectionId).value;

    if(selectedRoomsQuantity_value != null){
      selectedRoomsQuantity = selectedRoomsQuantity_value;
    }

    if (selectedRoomsQuantity > 9) {
      selectedRoomsQuantity = 9;
    } else if (selectedRoomsQuantity <= 0 || isNaN(selectedRoomsQuantity)) {
      selectedRoomsQuantity = 1;
    }

    for (let i = 1; i <= selectedRoomsQuantity; i++) {
      // Wrap the code inside the for loop in an IIFE to create a new scope
      (function(i) {
        const BedInfoDiv = document.getElementById("aminachBedInfo-" + apt_id + "-" + i);
        const selectedAminachBed = document.getElementById("aminachBedSelection-" + apt_id + "-" + i);
        var selectedAminachBedQuantity = selectedAminachBed.value;
        var residentsInRoom = null;
        var content = "";
        BedInfoDiv.innerHTML = ``;

        if(selectedAminachBedQuantity < 0 || isNaN(selectedAminachBedQuantity)) {
          selectedAminachBedQuantity = 0;
        } else if(selectedAminachBedQuantity > 4) {
          selectedAminachBedQuantity = 4;
        }

        if(roomsData != null) {
          selectedAminachBedQuantity = Object.keys(roomsData[i][1]).length;

          // If there is at least one bunk bed in a room then retrieve the data of the residents sleeping on the bed
          if(selectedAminachBedQuantity > 0) {
            residentsInRoom = roomsData[i][1];

             // Set the selected value of the select picker
            $(`#aminachBedSelection-${apt_id}-${i}`).val(selectedAminachBedQuantity);
          }
        }

        for (let j = 1; j <= selectedAminachBedQuantity ; j++) {
          content += `
            <label class="col-form-label col-form-label-sm mt-4" for="inputAminachBed-` + apt_id + `-` + i + `-` + j + `">שם מיטת עמינח</label>
            <div class="container">
              <select class="selectpicker selectpicker-disable selectpicker-aminach-bed-` + apt_id + `-` + i + `" data-width="65%" data-live-search="true" name="inputAminachBed-` + apt_id + `-` + i + `-` + j + `" id="inputAminachBed-` + apt_id + `-` + i + `-` + j + `">
              </select>
            </div>
          `;
        } 

        BedInfoDiv.innerHTML += content;

        // Populate the select pickers with options and wait for the Promise to resolve
        populateDropdownResidentsOptions(`.selectpicker-aminach-bed-${apt_id}-${i}`).then(() => {
          if(residentsInRoom != null) {
            for (let j = 1; j <= selectedAminachBedQuantity; j++) {      
              resident1 = residentsInRoom[j][0];
              $(`#inputAminachBed-${apt_id}-${i}-${j}`).val(resident1);
            }

            $(`.selectpicker-aminach-bed-${apt_id}-${i}`).selectpicker('refresh');
          }
        });
      })(i);
    }
  };

  const populateDropdownResidentsOptions = (select_picker_class) => {
    // Return a new Promise
    return new Promise((resolve, reject) => {
      // Send an AJAX request to fetch the resident data from the server
      $.ajax({
        url: "/get-residents-selection", // Replace with your Flask route for fetching residents
        type: "GET",
        data: {is_new_apartment: true},
        success: function (response) {
          // Populate the dropdown options dynamically
          $(select_picker_class).empty();
          
          // Add default value
          $(select_picker_class).append(
            `<option class="card-text-right names-options" value="מיטה פנויה">מיטה פנויה</option>`
          );

          // Populate the selectpicker with residents from db
          response.forEach((resident) => {
            $(select_picker_class).append(
              `<option class="card-text-right names-options" value="${resident[2]} - ${resident[0]} - ${resident[1]}">${resident[2]} - ${resident[0]} - ${resident[1]}</option>`
            );
          });
  
          $(select_picker_class).selectpicker('refresh');
  
          // Resolve the Promise
          resolve();
        },
        error: function (error) {
          console.log("Error:", error);
  
          // Reject the Promise
          reject(error);
        },
      });
    });
  };
  
  const populateDropdownResidentsNoFramesOptions = (select_picker_class) => {
    // Return a new Promise
    return new Promise((resolve, reject) => {
      // Send an AJAX request to fetch the resident data from the server
      $.ajax({
        url: "/get-residents-selection", // Replace with your Flask route for fetching residents
        type: "GET",
        data: {is_new_apartment: true},
        success: function (response) {
          // Populate the dropdown options dynamically
          $(select_picker_class).empty();
          

          // Populate the selectpicker with residents from db
          response.forEach((resident) => {
            $(select_picker_class).append(
              `<option class="card-text-right names-options" value="${resident[2]} - ${resident[0]}">${resident[2]} - ${resident[0]}</option>`
            );
          });
  
          $(select_picker_class).selectpicker('refresh');
  
          // Resolve the Promise
          resolve();
        },
        error: function (error) {
          console.log("Error:", error);
  
          // Reject the Promise
          reject(error);
        },
      });
    });
  };

  const populateDropdownApartmentsOptions = (select_picker_class) => {
    // Return a new Promise
    return new Promise((resolve, reject) => {
      // Send an AJAX request to fetch the resident data from the server
      $.ajax({
        url: "/get-apartments-selection", // Replace with your Flask route for fetching residents
        type: "GET",
        success: function (response) {
          // Populate the dropdown options dynamically
          $(select_picker_class).empty();

          // Populate the selectpicker with residents from db
          response.forEach((apartment) => {
            $(select_picker_class).append(
              `<option class="card-text-right apts-options" value="${apartment}">${apartment}</option>`
            );
          });
    
          $(select_picker_class).selectpicker('refresh');
    
          // Resolve the Promise
          resolve();
        },
        error: function (error) {
          console.log("Error:", error);
    
          // Reject the Promise
          reject(error);
        },
      });
    });
  };

  const populateDropdownFramesOptions = (select_picker_class) => {
    // Return a new Promise
    return new Promise((resolve, reject) => {
      // Send an AJAX request to fetch the resident data from the server
      $.ajax({
        url: "/get-frames-selection", // Replace with your Flask route for fetching residents
        type: "GET",
        success: function (response) {
          // Populate the dropdown options dynamically
          $(select_picker_class).empty();

          // Populate the selectpicker with residents from db
          response.forEach((frame) => {
            $(select_picker_class).append(
              `<option class="card-text-right frames-options" value="${frame}">${frame}</option>`
            );
          });
    
          $(select_picker_class).selectpicker('refresh');
    
          // Resolve the Promise
          resolve();
        },
        error: function (error) {
          console.log("Error:", error);
    
          // Reject the Promise
          reject(error);
        },
      });
    });
  };


  document.addEventListener('DOMContentLoaded', function () {
    const apartmentButtons = document.querySelectorAll(".apartment-btn");
    populateDropdownResidentsOptions(".filter-selectpicker-names");
    populateDropdownResidentsNoFramesOptions(".filter-selectpicker-names-residents-page");
    populateDropdownApartmentsOptions(".filter-selectpicker-apartments");
    populateDropdownFramesOptions(".filter-selectpicker-frames");
  
    // Define the isLoggedIn variable in a higher scope
    var isLoggedIn = false;
  
    // Send the checked values to the server using an AJAX POST request
    $.ajax({
      type: 'GET',
      url: '/is-logged-in',
      success: function(response) {
          // Update the value of isLoggedIn
          isLoggedIn = response.is_logged_in;
      },
      error: function(error) {
          // Handle error here
          console.log(error);
      }
    });
  
    apartmentButtons.forEach(button => {
        button.addEventListener('click', function () {
            const apartmentId = this.dataset.apartmentId;
  
            // Make an AJAX request to fetch data for the apartment
            fetch(`/apt-data/${apartmentId}`)
                .then(response => response.json())
                .then(data => {
                    apartmentIdSetting = "-" + apartmentId;
                    buildingId = data.apartment[0].building_id;
                    gender = data.apartment[0].gender;
                    roomsQuantity = data.apartment[0].rooms_in_apt;
                    roomsData = data.rooms_data;
  
                    // Create a new modal dynamically
                    createRoomSetting(apartmentId, roomsQuantity, apartmentIdSetting);
                    createBunkBedInfo(apartmentId, roomsQuantity, roomsData, apartmentIdSetting);
                    createAminachBedInfo(apartmentId, roomsQuantity, roomsData, apartmentIdSetting);
  
                    if (!isLoggedIn) {
                      // Code to disable all selectpickers with the class "selectpicker-disable"
                      var selectpickers = document.querySelectorAll('.selectpicker-disable');
                      for (var i = 0; i < selectpickers.length; i++) {
                        selectpickers[i].disabled = true;
                      }
                    }
                    
                })
                .catch(error => console.log(error));
        });
    });
  });
  


$(document).ready(function() {
  $('#submit-delete-selected-residents').click(function() {
      // Get all checked checkboxes
      var checkedCheckboxes = $('.checkbox-selection:checked');
      // Create an array to store the values of the checked checkboxes
      var checkedValues = [];
      // Loop through each checked checkbox and add its value to the array
      checkedCheckboxes.each(function() {
          checkedValues.push($(this).val());
      });
      // Send the checked values to the server using an AJAX POST request
      $.ajax({
          type: 'POST',
          url: '/residents/delete-selected-residents',
          data: JSON.stringify(checkedValues),
          contentType: 'application/json',
          success: function(response) {
              // Redirect to the "residents" page
              window.location.href = '/residents';
          },
          error: function(error) {
              // Handle error here
              console.log(error);
          }
      });
  });
});


function updateToastVisibility() {
  var anySelected = false;

  $(".checkbox-selection").each(function() {
      if($(this).is(":checked")) {
          anySelected = true;
          return false;
      }
  });

  const fadeElement = document.querySelector('#toast-residents-selection');
  if(anySelected) {
    $("#toast-residents-selection").addClass('show');
    fadeElement.style.bottom = "0";
    fadeElement.style.display = "block";
    fadeElement.style.animation = "deleteFadeIn 0.3s ease-in";
  } else {
    fadeElement.style.animation = "deleteFadeOut 0.3s ease-out";
    // setTimeout(function(){ fadeElement.style.bottom = "-100px";
    // $("#toast-residents-selection").removeClass('show') }, 500);
    // fadeElement.style.bottom = "-100px";
    const animated = document.querySelector("#toast-residents-selection");

    function handleAnimationEnd() {
        $("#toast-residents-selection").removeClass('show');
        fadeElement.style.display = "none";
        animated.removeEventListener("animationend", handleAnimationEnd);
    }

    animated.addEventListener("animationend", handleAnimationEnd);
  }
}


$(".checkbox-selection").change(function() {
  updateToastVisibility();
});


