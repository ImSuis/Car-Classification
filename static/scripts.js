$(document).ready(function () {
  // Handle button click to trigger file input
  $("#classify-button").click(function () {
    $("#file-input").click(); // Trigger the file input click event
  });

  // Handle file input change event
  $("#file-input").on("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      var formData = new FormData($("#upload-form")[0]);
      $.ajax({
        url: "/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
          // Populate the results section with the response data
          $("#car-name").text(`Car Name: ${response.classified_car.name}`);
          $("#car-price").text(
            `Estimated Price: $${response.classified_car.price}`
          );
          $("#car-confidence").text(
            `Confidence: ${response.classified_car.confidence}`
          );
          $("#cheapest-car-name").text(
            `Car Name: ${response.cheapest_car.name}`
          );
          $("#cheapest-car-price").text(
            `Price: $${response.cheapest_car.price}`
          );

          // Show the results section
          $("#results").removeClass("d-none");
        },
        error: function (xhr) {
          alert("Error: " + xhr.responseJSON.error);
        },
      });
    }
  });
});
