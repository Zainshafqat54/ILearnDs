$(document).ready(function(){
	$(".ANN_Form").hide()
	$(".RNN_Form").hide()
	$(".CNN_Form").hide()
    $(".DeepLearningFormFillingArea").hide()
    $(".DisplayStructure").hide()

  $(".d_card_ANN").click(function(){
	$(".clickToBackText").show()
    $(".MainWorkingArea").toggle();
    $(".DeepLearningFormFillingArea").toggle();
	$(".ANN_Form").show();

  });

    $(".d_card_CNN").click(function(){
	$(".clickToBackText").show()
    $(".MainWorkingArea").toggle();
    $(".DeepLearningFormFillingArea").toggle();
	$(".CNN_Form").show()

  });

    $(".d_card_RNN").click(function(){
	$(".clickToBackText").show()
    $(".MainWorkingArea").toggle();
    $(".DeepLearningFormFillingArea").toggle();
	$(".RNN_Form").show()

  });

  $(".DrawFigureButton").click(function(){
    $(".FormFillingArea").toggle();
    $(".DisplayStructure").toggle();
  });

  $(".RegenerateStructure").click(function(){

	$(".clickToBackText").show()
	 $(".DisplayStructure").toggle();
    $(".FormFillingArea").toggle();     
  });


 $(".clickToBackText").click(function(){
	$(".FormtoDrawStructure").hide(); 
    $(".DeepLearningFormFillingArea").toggle()
	$(".MainWorkingArea").toggle();
  });



});



$(document).ready(function() {
  $('.ANN-input-neurons').on('input', function() {
    $('.ANN-input-neurons-value').text($(this).val());
  });

  $('.ANN-hidden-layers').on('input', function() {
    $('.ANN-hidden-layers-value').text($(this).val());
  });

  $('.ANN-neurons-per-layer').on('input', function() {
    $('.ANN-neurons-per-layer-value').text($(this).val());
  });

  $('.ANN-output-neurons').on('input', function() {
    $('.ANN-output-neurons-value').text($(this).val());
  });
});

$(document).ready(function() {
  $('.CNN-Conv-Layers').on('input', function() {
    $('.CNN-Conv-Layers-value').text($(this).val());
  });

  $('.CNN-hidden-layers').on('input', function() {
    $('.CNN-hidden-layers-value').text($(this).val());
  });

  $('.CNN-neurons-per-layer').on('input', function() {
    $('.CNN-neurons-per-layer-value').text($(this).val());
  });

  $('.CNN-output-neurons').on('input', function() {
    $('.CNN-output-neurons-value').text($(this).val());
  });
});

$(document).ready(function() {
  $('.RNN-input-neurons').on('input', function() {
    $('.RNN-input-neurons-value').text($(this).val());
  });

  $('.RNN-hidden-layers').on('input', function() {
    $('.RNN-hidden-layers-value').text($(this).val());
  });

  $('.RNN-neurons-per-layer').on('input', function() {
    $('.RNN-neurons-per-layer-value').text($(this).val());
  });

  $('.RNN-output-neurons').on('input', function() {
    $('.RNN-output-neurons-value').text($(this).val());
  });
});


var submittedClass=''


$(document).ready(function() {
  $('form').on('submit', function(event) {
    event.preventDefault();

    // Get the class of the submitted form
  submittedClass = $(this).attr('class');
  console.log('Submitted form class:', submittedClass);

    // Serialize the form data
    var formDataArray = $(this).serializeArray();
    console.log(formDataArray);

    // Convert the array to a dictionary object
    var formData = {};
    for (var i = 0; i < formDataArray.length; i++) {
      formData[formDataArray[i].name] = formDataArray[i].value;
    }
    console.log("----------");
    console.log(formData);

    // Send the form data to the server using AJAX
    $.ajax({
      type: 'POST',
      url: '/Get-Input-Values-OF-Form',
      data: JSON.stringify(formData),
      contentType: 'application/json',
      success: function(response) {
        console.log('Form data submitted successfully!');
      },
      error: function(error) {
        console.error('Failed to submit form data:', error);
      }
    });

    var words = submittedClass.split(' ');
    var formClass = words[1];
    console.log(formClass);
    $.ajax({
        url: '/Create-Structure/'+ (formClass),
        method: 'POST',
        data: {form_class: formClass},
        success: function(response) {
            // Handle the successful response from the server
            console.log(response.file_name);
            fileLink='/download_file/' + response.file_name;
            $('.download-btn').attr('href',fileLink);
        },
        error: function(error) {
            // Handle the error response from the server
        }
    });




  });
});
