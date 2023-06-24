  const createRoomSetting = (apt_id="newApt", selectedQuantity_value = null, roomsSettings_id = "roomsSettings") => {
    const roomsSettings = document.getElementById(roomsSettings_id);
    var selectedQuantity = document.getElementById("roomSelection").value;
    
    if(selectedQuantity_value != null){
      selectedQuantity = selectedQuantity_value;
    }

    roomsSettings.innerHTML = ``;

    if (selectedQuantity > 9) {
      selectedQuantity = 9;
    } else if (selectedQuantity <= 0 || isNaN(selectedQuantity)) {
      selectedQuantity = 0;
    }

    var content = "";
    for (let i = 1; i <= selectedQuantity; i++) {
      content +=  `
        <hr style="width:80%;height:2px;background-color:gray">
        <label class="col-form-label col-form-label-lg">חדר ` + i + `</label>
        <br>
        <label for="bunkBedSelection-` + apt_id + `-` + i + `" class="form-label mt-4">
          <strong>כמות מיטות קומותיים</strong>
        </label>
        <select class="form-select" name="bunkBedSelection-` + apt_id + `-` + i + `" id="bunkBedSelection-` + apt_id + `-` + i + `" style="width:15%" onchange="createBunkBedInfo('` + apt_id + `', ` + selectedQuantity_value + `);" onfocus="this.selectedIndex = -1;">
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

        <label for="aminachBedSelection-` + i + `" class="form-label mt-4">
          <strong>כמות מיטות עמינח</strong>
        </label>
        <select class="form-select" name="aminachBedSelection-` + apt_id + `-` + i + `" id="aminachBedSelection-` + apt_id + `-` + i + `" style="width:15%" onchange="createAminachBedInfo('` + apt_id + `', ` + selectedQuantity_value + `);" onfocus="this.selectedIndex = -1;">
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


const createBunkBedInfo = (apt_id="newApt", selectedQuantity_value = null) => {
    var selectedQuantity = document.getElementById("roomSelection").value;

    if(selectedQuantity_value != null){
      selectedQuantity = selectedQuantity_value;
    }

    if (selectedQuantity > 9) {
      selectedQuantity = 9;
    } else if (selectedQuantity <= 0 || isNaN(selectedQuantity)) {
      selectedQuantity = 1;
    }

    for (let i = 1; i <= selectedQuantity; i++) {
      const BedInfoDiv = document.getElementById("bunkBedInfo-" + apt_id + "-" + i);
      const selectedBunkBed = document.getElementById("bunkBedSelection-" + apt_id + "-" + i);
      var selectedBunkBedQuantity = selectedBunkBed.value;
      BedInfoDiv.innerHTML = ``;
      var content = "";

      for (let j = 1; j <= selectedBunkBedQuantity; j++) {
        content += `
          <label class="col-form-label col-form-label-sm mt-4" for="inputBunkBed-` + apt_id + `-` + i + `-` + j + `">שמות מיטת קומותיים</label>
          <div class="container pb-2">
            <select class="selectpicker selectpicker-bunk-bed" data-live-search="true" name="inputBunkBed1-` + apt_id + `-` + i + `-` + j + `" id="inputBunkBed1-` + apt_id + `-` + i + `-` + j + `">
            </select>
          </div>
          <div class="container pb-2">
            <select class="selectpicker selectpicker-bunk-bed" data-live-search="true" name="inputBunkBed2-` + apt_id + `-` + i + `-` + j + `" id="inputBunkBed2-` + apt_id + `-` + i + `-` + j + `">
            </select>
          </div>
        `;

      } 
      BedInfoDiv.innerHTML += content;
      $('.selectpicker').selectpicker('refresh');
      populateDropdownOptions(".selectpicker-bunk-bed");
    }
  };

  const createAminachBedInfo = (apt_id="newApt", selectedQuantity_value = null) => {
    var selectedQuantity = document.getElementById("roomSelection").value;

    if(selectedQuantity_value != null){
      selectedQuantity = selectedQuantity_value;
    }

    if (selectedQuantity > 9) {
      selectedQuantity = 9;
    } else if (selectedQuantity <= 0 || isNaN(selectedQuantity)) {
      selectedQuantity = 1;
    }

    for (let i = 1; i <= selectedQuantity; i++) {
      const BedInfoDiv = document.getElementById("aminachBedInfo-" + apt_id + "-" + i);
      const selectedAminachBed = document.getElementById("aminachBedSelection-" + apt_id + "-" + i);
      var selectedAminachBedQuantity = selectedAminachBed.value;
      BedInfoDiv.innerHTML = ``;
      var content = "";

      for (let j = 1; j <= selectedAminachBedQuantity ; j++) {
        content += `
          <label class="col-form-label col-form-label-sm mt-4" for="inputAminachBed-` + apt_id + `-` + i + `-` + j + `">שם מיטת עמינח</label>
          <div class="container">
            <select class="selectpicker selectpicker-aminach-bed" data-live-search="true" name="inputAminachBed-` + apt_id + `-` + i + `-` + j + `" id="inputAminachBed-` + apt_id + `-` + i + `-` + j + `">
            </select>
          </div>
        `;

      } 
      BedInfoDiv.innerHTML += content;
      $('.selectpicker').selectpicker('refresh');
      populateDropdownOptions(".selectpicker-aminach-bed");
    }
  };

  const populateDropdownOptions = (select_picker_class) => {
    

    // Send an AJAX request to fetch the resident data from the server
    $.ajax({
      url: "/get-residents", // Replace with your Flask route for fetching residents
      type: "GET",
      success: function (response) {
        // Populate the dropdown options dynamically
        $(select_picker_class).empty();
        response.forEach((resident) => {
          $(select_picker_class).append(
            `<option value="${resident}">${resident}</option>`
          );
        });
  
        $(select_picker_class).selectpicker('refresh');
      },
      error: function (error) {
        console.log("Error:", error);
      },
    });
  };

  $(document).on("click", ".send-building-id", function () {
    var buildingId = $(this).data('id');
    $(".modal-body #building-id").val( buildingId );
  });

  $(function () {
    $(".date-picker").datepicker({ 
          autoclose: true, 
          todayHighlight: true
    }).datepicker('update', new Date());
  });

  $(document).ready(function() {
    $('.selectpicker').selectpicker();
});
  