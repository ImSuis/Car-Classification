$(document).ready(function () {
  // Handle button click to trigger file input
  $("#classify-button").click(function () {
    $("#file-input").click(); // Trigger the file input click event
  });

  // Handle file input change event
  $("#file-input").on("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#image-preview").attr("src", e.target.result);
      };
      reader.readAsDataURL(file);

      var formData = new FormData($("#upload-form")[0]);
      $.ajax({
        url: "/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
          $("#results").removeClass("d-none");
          $("#car-name").text(`Car Name: ${response.model_name}`);
          $("#confidence").text(
            "Confidence: " + (response.confidence * 100).toFixed(2) + "%"
          );

          if (response.cheapest_cars && response.cheapest_cars.length > 0) {
            for (let i = 0; i < 3; i++) {
              const car = response.cheapest_cars[i];
              if (car) {
                $(`#option-${i + 1}-name`)
                  .text(car.Name)
                  .attr("href", car.URL || "#");
                $(`#option-${i + 1}-price`).text("$" + (car.Price || "N/A"));
                $(`#option-${i + 1}-mileage`).text(
                  car.Mileage ? `${car.Mileage.toLocaleString()}` : "N/A"
                );
              } else {
                $(`#option-${i + 1}-name`)
                  .text("N/A")
                  .attr("href", "#");
                $(`#option-${i + 1}-price`).text("N/A");
                $(`#option-${i + 1}-mileage`).text("N/A");
              }
            }
            $("#no-cars-message").addClass("d-none");
          } else {
            $("#no-cars-message").removeClass("d-none");
          }
        },
        error: function (xhr) {
          alert("Error: " + xhr.responseJSON.error);
        },
      });
    }
  });
});
