

$(document).ready(function(){

$('.ReplaceNullVal').click(function() 
{ 
  $('.RelaceNullValueoptions').slideToggle("fast");
});


$('.dropNullval').click(function() 
{ 
  $('.DropNullValueOptions').slideToggle("fast");
});

$('.removeAmbiguity').click(function() 
{ 
  $('.removeAmbiguityOptions').slideToggle("fast");
});

$('.RemoveAmbiguityUrls_Emojis').click(function() 
{ 

  $('.removeAmbiguityAxisOptionUrl_Emoji').slideToggle("fast");

}
);

$('.RemoveAmbiguityHTMLTag').click(function() 
{ 
  $('.removeAmbiguityAxisOptionHTMLTag').slideToggle("fast");

}
);

$('.dropDuplicates').click(function() 
{ 
  $('.dropDuplicateOptionColumnName').slideToggle("fast");

}
);


$('.ReplaceValue').click(function() 
{ 
  $('.replaceColOrRowValOptions').slideToggle("fast");

}
);

$('.replaceColVal').click(function() 
{ 
  $('.replaceColValOptions').slideToggle("fast");

}
);

$('.replaceRowVal').click(function() 
{ 
  $('.replaceRowValOptions').slideToggle("fast");

}
);

$('.droprowOrColumn').click(function() 
{ 
  $('.droprowOrColumnOptions').slideToggle("fast");

}
);

$('.dropColumnOption').click(function() 
{ 
  $('.dropColumnOptionForm').slideToggle("fast");

}
);

$('.dropRow').click(function() 
{ 
  $('.dropRowOptions').slideToggle("fast");

}
);

// $('.featureSelection').click(function() 
// { 
//   $('.featureSelectionOptions').slideToggle();

// }
// );

$('.featureSelectionChi_SQROption').click(function() 
{ 
  $('.featureSelectionChi_SQROptionForm').slideToggle();

}
);

$(function() { // Dropdown toggle
$('.filter').click(function() 
{ 

$('.DataFrameDisplay').slideToggle();

});


});


});


function getColumnNames()
{
    $.get("/getAllColumnsName", function(data) {

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
$(document).ready(function()
{
  getColumnNames();
});



function getRowCount()
{

  var LastIndexOfRow = $.ajax({type: "GET", url: "/getRowcount", async: false}).responseText;
  return parseInt(LastIndexOfRow);
}

function getColumnCount()
{

  var NmbrOfColumns = $.ajax({type: "GET", url: "/getColumncount", async: false}).responseText;
  return parseInt(NmbrOfColumns);
}


function RowIndexValidation() {
  // Get the value of the input field with id="numb"
  let x = document.getElementById("RowIndex").value;
  let y = document.getElementById("ReplaceWith").value;
  console.log(x)
  // If x is Not a Number or less than one or greater than 10
  let text;
  var LastRange = getRowCount();
  // console.log(LastRange);
  if (isNaN(x) || x < 0 || x > LastRange || x=='' || y=='' ) {
    text = "Input not valid or feild missing";
    $(".replaceRowValValidty").append('<p id="ValidationOfInputRowIndex"> </p>');
    $("#ValidationOfInputRowIndex").text(text);
  }
  else {
    $("#replaceRowValOptions").submit();
  }
  // document.getElementById("ValidationOfInputRowIndex").innerHTML = text;
};

function RangeValidation() {
  // Get the value of the input field with id="numb"
  let x = (document.getElementById("RangeStart").value);
  let y = (document.getElementById("RangeEnd").value);
  // console.log($.type(x));
  // console.log($.type(y));
  var FormFilled=true;
  $(".RowRangeStartValValidity").append('<p id="ValidationOfInputRowRangeStart"> </p>');
  $("#ValidationOfInputRowRangeStart").text("");
  $(".RowRangeEndValValidity").append('<p id="ValidationOfInputRowRangeEnd"> </p>');
  $("#ValidationOfInputRowRangeEnd").text("");
  // If x is Not a Number or less than one or greater than 10
  let text;
  var LastRange = getRowCount();
  // console.log($.type(LastRange));
  if (isNaN(x) || x < 0 || x > LastRange || (!$('#RangeStart').val()))
  {
    FormFilled=false;
    text = "Input not valid or Field missing";    
    $("#ValidationOfInputRowRangeStart").text(text);
  }

  if (isNaN(y) || y < 0 || y > LastRange || (!$('#RangeEnd').val()))
  {
    FormFilled=false;
    text = "Input not valid or Field missing";    
    $("#ValidationOfInputRowRangeEnd").text(text);
  }
  if(FormFilled)
  {
    // console.log("done");
    $("#dropRowForm").submit();
  }
  // document.getElementById("ValidationOfInputRowIndex").innerHTML = text;
};

function FeatureSelectionValidation() {
  // Get the value of the input field with id="numb"
  let x = document.getElementById("NumberOfColRqrdForChiSqr").value;
  console.log(x)
  // If x is Not a Number or less than one or greater than 10
  let text;
  var NmbrOfColumns = getColumnCount();
  console.log(NmbrOfColumns);
  if (isNaN(x) || x < 0 || x > NmbrOfColumns || (!$('#NumberOfColRqrdForChiSqr').val()) || (!$('#AllColumnNameDropDownListForfeatureSelectionChiSquare').val()) ) {
    text = "Invalid Input Entered  OR Feild Missing";
    $(".featureSelectionViaChiSqrNumberOfColValidity").append('<p id="ValidationOfInputNumberOfColumn"> </p>');
    $("#ValidationOfInputNumberOfColumn").text(text);
  }
  else {
    // console.log("done");
    $("#featureSelectionChi_SQROptionForm").submit();
  }
  // document.getElementById("ValidationOfInputRowIndex").innerHTML = text;
};

$(document).ready(function(){
    $('.parameterForm input[type="text"]').blur(function(){
        if(!$(this).val()){
            $(this).addClass("error");
        } else{
            $(this).removeClass("error");
        }
    });
});



/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function DisplayFilterDropDownOptions() {
  $("#FilterDropdown").slideToggle("show");
}
$("#FilterDropdown").click(function()
{
  $(this).hide();
});