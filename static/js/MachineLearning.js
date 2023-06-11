$(document).ready(function(){

    $(".MachineLearningResultsArea").hide()
  $(".d_card").click(function(){
    $(".MainWorkingArea").toggle();
    $(".MachineLearningResultsArea").toggle();

  });

  $(".clickToBackText").click(function(){
    $('.FormDisplayArea').show();
    $(".MachineLearningResultsArea").toggle();
    $(".MainWorkingArea").toggle();    
  });

});

$(document).ready(function() {
  $('.algorithmBtn').click(function() {
    $('.resultsDisplayArea').hide();
    var classList = this.classList;
    // alert(classList[1]);
    $('.ParameterForm').prop('action', "/"+classList[1]);
    $(".ParameterForm").show();
  });
});

// $(document).ready(function() {
//     var classList = $('#plot').attr('class');
//     alert(classList);
// });

$(document).ready(function() {
  if ($('#plot').hasClass('js-plotly-plot')) {
    $(".MainWorkingArea").toggle();
    $(".MachineLearningResultsArea").toggle();
    $('.FormDisplayArea').hide();
   // the element has the class 'class-name'
  }
  else {
    // the element does not have the class 'class-name'
  }
});



$(document).ready(function(){
    $('.parameterForm input[type="text"]').blur(function(){
        if(!$(this).val()){
            $(this).addClass("error");
        } else{
            $(this).removeClass("error");
        }
    });
});

$(document).ready(function()
{
  $(".ParameterForm").hide();
});


function getColumnNames()
{
    $.get("/getAllColumnsNameForMachineLearning", function(data) {

    // console.log($.parseJSON(data))

    for(i = 0; i <$.parseJSON(data).length; i++) {

      var temp = $.parseJSON(data)[i];
      // Create New Option.
      var newOption = $('<option>');
      newOption.attr('value', temp).text(temp);
      // Append that to the DropDownList.
      $('.AllColumnNameDropDownList').append(newOption);
    }

  })
}
function getTestsizeValues()
{
    var tempVal=0.1;
    for(var i = 0; i < 5; i++) 
    {

      var temp = tempVal.toFixed(1);;
      // Create New Option.
      var newOption = $('<option>');
      newOption.attr('value', temp).text(temp);
      // Append that to the DropDownList.
      $('.TestSize').append(newOption);
      tempVal=tempVal + 0.1;
    }
}
function getNearestNeighborsValues()
{
    var tempVal=1;
    for(var i = 0; i < 12; i++) 
    {

      var temp =tempVal;
      // Create New Option.
      var newOption = $('<option>');
      newOption.attr('value', temp).text(temp);
      // Append that to the DropDownList.
      $('#NearestNeighbors').append(newOption);
      tempVal=tempVal + 1;
    }
}
$(document).ready(function()
{
  getColumnNames();
  getTestsizeValues();
});

function getRowCount()
{

  var LastIndexOfRow = $.ajax({type: "GET", url: "/getRowcountForMachineLearning", async: false}).responseText;
  return parseInt(LastIndexOfRow);
}
function InputValidation()
{
  if(InputValidationOfRandomState())
  {
    
    $(".ParameterForm").submit();
    $('.resultsDisplayArea').show();
    $('.FormDisplayArea').hide();
  }
}

function InputValidationOfRandomState() {
  // alert("InputValidationOfRandomState");
  var flag=true;
  let x = document.getElementById("RandomState").value;
  console.log(x)
  let text;
  var LastRange = getRowCount();
  console.log(LastRange);
  if (isNaN(x) || x < 0 || x > LastRange || x=='') {
    flag=false;
   text = "Input not valid or Field missing";
    $(".validity").append('<p id="ValidationOfValueEnteredText"> </p>');
    $("#ValidationOfValueEnteredText").text(text);
  }
  if(flag) 
  {
    // $(".ParameterForm").submit();
    return true;
  }
  else{return false;}
  // document.getElementById("ValidationOfInputRowIndex").innerHTML = text;
};


$('.algorithmBtn').click(function() {
  $(".F1ScoreAvrgOption").show();
  $('.additionalElement').remove();
});

$('.li').click(function() {
  $(".F1ScoreAvrgOption").hide();
});

$('.knn').click(function() {
  $('.additionalElements').append('<label class="additionalElement NearestNeighbor_Label" for="KNearestNeighbors">K Nearest Neighbors</label>');
  $('.additionalElements').append('<SELECT id="NearestNeighbors" class=" additionalElement NearestNeighbors" name="NearestNeighbors" placeholder="Select Nearest Neighbors" required></SELECT>');
  getNearestNeighborsValues();
});
