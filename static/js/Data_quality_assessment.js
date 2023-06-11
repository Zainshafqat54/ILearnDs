var flag=false;



const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
const pages = document.querySelectorAll(".page");
    const translateAmount = 100; 
    let translate = 0;

    slide = (direction) => {

      direction === "next" ? translate -= translateAmount : translate += translateAmount;

      pages.forEach(
        pages => (pages.style.transform = `translateX(${translate}%)`)
      );
    }


$(document).ready(function(){
  var messages = ["Data is being fetched, in just a moment ......", "We are getting the data for you. Hang tight .......","Hold on a second, Your data is on its way......."];
  var index = 0;
  setInterval(function(){
    $("#message").fadeOut("slower",function(){
      $(this).text(messages[index]).fadeIn();
      index = (index + 1) % messages.length;
    });
  }, 2000);  // 2 seconds
});






$(document).ready(function() {

$.get("/getAllColumns", function(data) {
  NoOfCol=$.parseJSON(data).length;
  setTimeout(myFunctionValueCount, 1);
  setTimeout(myFunctionStatistics, NoOfCol*2000);
  setTimeout(myFunctionDistribution, NoOfCol*2000*2);
  setTimeout(myFunctionOutliers, NoOfCol*2000*3);
  setTimeout(myFunctionNullValue, (NoOfCol*2000*4));
  setTimeout(myFunctionCorr, (NoOfCol*2000*4)+1000);
  setTimeout(myFunctionContinueBtnClick, (NoOfCol*2000*4)+1000);

})

});

function myFunctionContinueBtnClick() {
  $("#message").remove();
  $(".StartBtn").text("Click To Continue");
}

function myFunctionValueCount() {
  createColumnButtonsValuecount("ValueCount","/getAllColumns","/visualization_ValueCount/");
}
function myFunctionStatistics() {
  createColumnButtonsStatistics("Statistics","/getNumericColumns","/visualization_Statistics/");
}

function myFunctionDistribution() {
  createColumnButtonsDistribution("Distribution","/getNumericColumns","/visualization_Distribution/");
}

function myFunctionOutliers() {
  createColumnButtonsOutliers("Outliers","/getNumericColumns","/visualization_Outliers/");
}

function myFunctionCorr() {
  imgClass='.SlidingDisplayAreaSingleFigureImg_'+'corr';
  Imgurl="/visualization_corr";
  drawFigures(imgClass,Imgurl);
  flag=true;
}
function myFunctionNullValue() {
  imgClass='.SlidingDisplayAreaSingleFigureImg_'+'null_val';
  Imgurl="/visualization_NullValue";
  drawFigures(imgClass,Imgurl);
}

$(document).ready(function()
{
  $(".SlidingDisplayArea").hide();
}
);

// $( ".Value_count" ).one( "click", function() {
//   createColumnButtonsValuecount("ValueCount","/getAllColumns","/visualization_ValueCount/");
//   // createColumnButtons("Statistics","/getNumericColumns","/visualization_Statistics/");
//   // createColumnButtons("Distribution","/getNumericColumns","/visualization_Distribution/");
//   // createColumnButtons("Outliers","/getNumericColumns","/visualization_Outliers/");
// });

// $( ".Statistics" ).one( "click", function() {
//   createColumnButtonsStatistics("Statistics","/getNumericColumns","/visualization_Statistics/");
// });
// $( ".Distribution" ).one( "click", function() {
//   createColumnButtonsDistribution("Distribution","/getNumericColumns","/visualization_Distribution/");
// });
// $( ".Outliers" ).one( "click", function() {
//   createColumnButtonsOutliers("Outliers","/getNumericColumns","/visualization_Outliers/");
// });

$(".Value_count").click(function(){
  $(".SlidingDisplayArea_ValueCount").slideToggle();
});

$(".Statistics").click(function(){
  $(".SlidingDisplayArea_Statistics").slideToggle();
});

$(".Distribution").click(function(){
  $(".SlidingDisplayArea_Distribution").slideToggle();
});

$(".Outliers").click(function(){
  $(".SlidingDisplayArea_Outliers").slideToggle();
});

$(".null_val").click(function(){
  $(".SlidingDisplayArea_null_val").slideToggle();

});

$(".Correlation").click(function(){
  $(".SlidingDisplayArea_corr").slideToggle();

});



function animationOfButton(btnToAnimate)
{
  // alert(btnToAnimate);
  var temp=btnToAnimate.split(" ");
  var visualizationName=temp[1].match(/^(.*?)_item_btn_/);

  var classArr = btnToAnimate.match(/item_btn_(.*)/);

  $(".SlidingDisplayAreaAllButtons_"+ visualizationName[1]).hide();

  $('<div/>', { 
        class: 'singleItemVisualizationArea  singleItemVisualizationArea_'+visualizationName[1],
    }).appendTo(".SlidingDisplayArea_" + visualizationName[1]);

    $('<img/>', { 
        class: 'center singleItemVisualization  singleItemVisualization_'+visualizationName[1],
    }).appendTo('.singleItemVisualizationArea_'+visualizationName[1]);

    $('<p/>', { 
        text: "Click To Back",
        class: 'singleItemVisualizationText  singleItemVisualizationText_'+visualizationName[1],
    }).appendTo('.singleItemVisualizationArea_'+visualizationName[1]);

  imgUrl=("/visualization_"+visualizationName[1]+"/").concat("",classArr[classArr.length-1]);
  imgClass='.singleItemVisualization_'+visualizationName[1];
  drawFigures(imgClass,imgUrl);
  $('.singleItemVisualizationArea_'+visualizationName[1]).animate({
   width: "640px",
   height: "500px",  
    }, 3000 );
   var  SIVA='.singleItemVisualizationArea_'+visualizationName[1];
   var  SDAAB='.SlidingDisplayAreaAllButtons_'+ visualizationName[1];
  $('.singleItemVisualizationArea_'+visualizationName[1]).click(function()
  {
    $('.SlidingDisplayAreaAllButtons_'+ visualizationName[1]).slideToggle();
    $('.singleItemVisualizationArea_'+visualizationName[1]).remove();
  });

  }



function createColumnButtonsStatistics(selectedVisualization,GetColumnCondition,functionToCall)
{
  $(".LoadingDataMessageStatistics").remove();
  // alert("createColumnButtonsStatisticsCalled");
  selectedVisualizationClass=".SlidingDisplayArea_"+selectedVisualization;
  // selectedVisualizationClass="."+selectedVisualization;
  // $(selectedVisualizationClass).append("<div class='SlidingDisplayAreaAllButtons'> </div>");
  // alert(GetColumnCondition);
  $('<div/>', { 
        class: 'SlidingDisplayAreaAllButtons  SlidingDisplayAreaAllButtons_'+selectedVisualization,
    }).appendTo(selectedVisualizationClass);

  $.get(GetColumnCondition, function(data) {


        for(i = 0; i <$.parseJSON(data).length; i++) 
  {
          var item_class=selectedVisualization + '_item_'+$.parseJSON(data)[i];
          var item_btn_class=selectedVisualization + '_item_btn_'+$.parseJSON(data)[i];
          var item_btn_text_class=selectedVisualization + '_item_btn_text_'+$.parseJSON(data)[i];

      
           $('<div/>', { 
        class: 'item '+item_class,
    }).appendTo('.SlidingDisplayAreaAllButtons_'+selectedVisualization);

    
     $('<div/>', {
        // text: $.parseJSON(data)[i], 
        class: 'item_btn '+ item_btn_class,
        click:function(event)
        {
          var  indexOfButtonPressed= ($.parseJSON(data).indexOf($(this).attr("class")));
          var buttonPressedClass=($(this).attr("class"));
          // clicked($.parseJSON(data)[indexOfButtonPressed])
          if(flag)
          {
            animationOfButton(buttonPressedClass);
          }
          
        }
    }).appendTo("."+item_class);
    $('<p/>', {
        text: $.parseJSON(data)[i], 
        class: 'item_btn_text '+ item_btn_text_class,
    }).insertAfter("."+ item_btn_class);
  
  
  }


  for(i = 0; i <$.parseJSON(data).length; i++) 
  {
      var columnName=$.parseJSON(data)[i];
      var figureClassName='singleFigure '+selectedVisualization+'_figure_'+columnName;

      var $newDiv = $("<img>")   // creates a div element                
                 .addClass(figureClassName);   // add a class
      
      $('.'+ selectedVisualization + '_item_btn_' + columnName).append($newDiv);
      
      TimeDelay(i,'.'+selectedVisualization+'_figure_'+columnName,columnName);
  }

    function TimeDelay(i,figureClassName,columnName)
   {
      setTimeout(function() 
      {
      Imgurl=functionToCall.concat("",columnName)
      drawFiguresStatistics(figureClassName,Imgurl);
      }, 2000 * (i));
    }

    })
}
function createColumnButtonsValuecount(selectedVisualization,GetColumnCondition,functionToCall)
{
  $(".LoadingDataMessageValueCount").remove();
  // alert("CreateColumnsButtonCalled");
  selectedVisualizationClass=".SlidingDisplayArea_"+selectedVisualization;
  // selectedVisualizationClass="."+selectedVisualization;
  // $(selectedVisualizationClass).append("<div class='SlidingDisplayAreaAllButtons'> </div>");
  // alert(GetColumnCondition);
  $('<div/>', { 
        class: 'SlidingDisplayAreaAllButtons  SlidingDisplayAreaAllButtons_'+selectedVisualization,
    }).appendTo(selectedVisualizationClass);

  $.get(GetColumnCondition, function(data) {


        for(i = 0; i <$.parseJSON(data).length; i++) 
  {
          var item_class=selectedVisualization + '_item_'+$.parseJSON(data)[i];
          var item_btn_class=selectedVisualization + '_item_btn_'+$.parseJSON(data)[i];
          var item_btn_text_class=selectedVisualization + '_item_btn_text_'+$.parseJSON(data)[i];

      
           $('<div/>', { 
        class: 'item '+item_class,
    }).appendTo('.SlidingDisplayAreaAllButtons_'+selectedVisualization);

    
     $('<div/>', {
        // text: $.parseJSON(data)[i], 
        class: 'item_btn '+ item_btn_class,
        click:function(event)
        {
          var  indexOfButtonPressed= ($.parseJSON(data).indexOf($(this).attr("class")));
          var buttonPressedClass=($(this).attr("class"));
          // clicked($.parseJSON(data)[indexOfButtonPressed])
          
          if(flag)
          {
            animationOfButton(buttonPressedClass);
          }
        }
    }).appendTo("."+item_class);
    $('<p/>', {
        text: $.parseJSON(data)[i], 
        class: 'item_btn_text '+ item_btn_text_class,
    }).insertAfter("."+ item_btn_class);
  
  
  }


  for(i = 0; i <$.parseJSON(data).length; i++) 
  {
      var columnName=$.parseJSON(data)[i];
      var figureClassName='singleFigure '+selectedVisualization+'_figure_'+columnName;

      var $newDiv = $("<img>")   // creates a div element                
                 .addClass(figureClassName);   // add a class
      
      $('.'+ selectedVisualization + '_item_btn_' + columnName).append($newDiv);
      
      TimeDelay(i,'.'+selectedVisualization+'_figure_'+columnName,columnName);
  }

    function TimeDelay(i,figureClassName,columnName)
   {
      setTimeout(function() 
      {
      Imgurl=functionToCall.concat("",columnName)
      drawFiguresValueCount(figureClassName,Imgurl);
      }, 2000 * (i));
    }

    })
}
function createColumnButtonsDistribution(selectedVisualization,GetColumnCondition,functionToCall)
{
   $(".LoadingDataMessageDistribution").remove();
  // alert("createColumnButtonsDistributionCalled");
  selectedVisualizationClass=".SlidingDisplayArea_"+selectedVisualization;
  // selectedVisualizationClass="."+selectedVisualization;
  // $(selectedVisualizationClass).append("<div class='SlidingDisplayAreaAllButtons'> </div>");
  // alert(GetColumnCondition);
  $('<div/>', { 
        class: 'SlidingDisplayAreaAllButtons  SlidingDisplayAreaAllButtons_'+selectedVisualization,
    }).appendTo(selectedVisualizationClass);

  $.get(GetColumnCondition, function(data) {


        for(i = 0; i <$.parseJSON(data).length; i++) 
  {
          var item_class=selectedVisualization + '_item_'+$.parseJSON(data)[i];
          var item_btn_class=selectedVisualization + '_item_btn_'+$.parseJSON(data)[i];
          var item_btn_text_class=selectedVisualization + '_item_btn_text_'+$.parseJSON(data)[i];

      
           $('<div/>', { 
        class: 'item '+item_class,
    }).appendTo('.SlidingDisplayAreaAllButtons_'+selectedVisualization);

    
     $('<div/>', {
        // text: $.parseJSON(data)[i], 
        class: 'item_btn '+ item_btn_class,
        click:function(event)
        {
          var  indexOfButtonPressed= ($.parseJSON(data).indexOf($(this).attr("class")));
          var buttonPressedClass=($(this).attr("class"));
          // clicked($.parseJSON(data)[indexOfButtonPressed])
          
          if(flag)
          {
            animationOfButton(buttonPressedClass);
          }
        }
    }).appendTo("."+item_class);
    $('<p/>', {
        text: $.parseJSON(data)[i], 
        class: 'item_btn_text '+ item_btn_text_class,
    }).insertAfter("."+ item_btn_class);
  
  
  }


  for(i = 0; i <$.parseJSON(data).length; i++) 
  {
      var columnName=$.parseJSON(data)[i];
      var figureClassName='singleFigure '+selectedVisualization+'_figure_'+columnName;

      var $newDiv = $("<img>")   // creates a div element                
                 .addClass(figureClassName);   // add a class
      
      $('.'+ selectedVisualization + '_item_btn_' + columnName).append($newDiv);
      
      TimeDelay(i,'.'+selectedVisualization+'_figure_'+columnName,columnName);
  }

    function TimeDelay(i,figureClassName,columnName)
   {
      setTimeout(function() 
      {
      Imgurl=functionToCall.concat("",columnName)
      drawFiguresDistribution(figureClassName,Imgurl);
      }, 2000 * (i));
    }

    })
}
function createColumnButtonsOutliers(selectedVisualization,GetColumnCondition,functionToCall)
{
  $(".LoadingDataMessageOutliers").remove();
  // alert("createColumnButtonsOutliersCalled");
  selectedVisualizationClass=".SlidingDisplayArea_"+selectedVisualization;
  // selectedVisualizationClass="."+selectedVisualization;
  // $(selectedVisualizationClass).append("<div class='SlidingDisplayAreaAllButtons'> </div>");
  // alert(GetColumnCondition);
  $('<div/>', { 
        class: 'SlidingDisplayAreaAllButtons  SlidingDisplayAreaAllButtons_'+selectedVisualization,
    }).appendTo(selectedVisualizationClass);

  $.get(GetColumnCondition, function(data) {


        for(i = 0; i <$.parseJSON(data).length; i++) 
  {
          var item_class=selectedVisualization + '_item_'+$.parseJSON(data)[i];
          var item_btn_class=selectedVisualization + '_item_btn_'+$.parseJSON(data)[i];
          var item_btn_text_class=selectedVisualization + '_item_btn_text_'+$.parseJSON(data)[i];

      
           $('<div/>', { 
        class: 'item '+item_class,
    }).appendTo('.SlidingDisplayAreaAllButtons_'+selectedVisualization);

    
     $('<div/>', {
        // text: $.parseJSON(data)[i], 
        class: 'item_btn '+ item_btn_class,
        click:function(event)
        {
          var  indexOfButtonPressed= ($.parseJSON(data).indexOf($(this).attr("class")));
          var buttonPressedClass=($(this).attr("class"));
          // clicked($.parseJSON(data)[indexOfButtonPressed])
          
          if(flag)
          {
            animationOfButton(buttonPressedClass);
          }
        }
    }).appendTo("."+item_class);
    $('<p/>', {
        text: $.parseJSON(data)[i], 
        class: 'item_btn_text '+ item_btn_text_class,
    }).insertAfter("."+ item_btn_class);
  
  
  }


  for(i = 0; i <$.parseJSON(data).length; i++) 
  {
      var columnName=$.parseJSON(data)[i];
      var figureClassName='singleFigure '+selectedVisualization+'_figure_'+columnName;

      var $newDiv = $("<img>")   // creates a div element                
                 .addClass(figureClassName);   // add a class
      
      $('.'+ selectedVisualization + '_item_btn_' + columnName).append($newDiv);
      
      TimeDelay(i,'.'+selectedVisualization+'_figure_'+columnName,columnName);
  }

    function TimeDelay(i,figureClassName,columnName)
   {
      setTimeout(function() 
      {
      Imgurl=functionToCall.concat("",columnName)
      drawFiguresOutliers(figureClassName,Imgurl);
      }, 2000 * (i));
    }

    })
}

function drawFiguresValueCount(imgClass,Imgurl)
{
  // alert(imgClass);
      fetch(Imgurl,{method:'GET',mode:'no-cors'})

    .then((response)=> response)
    .then((response)=>response.blob())
    .then((blob)=> {
    $(imgClass).attr('src',URL.createObjectURL(blob))
    })
};

function drawFiguresStatistics(imgClass,Imgurl)
{
  // alert(imgClass);
      fetch(Imgurl,{method:'GET',mode:'no-cors'})

    .then((response)=> response)
    .then((response)=>response.blob())
    .then((blob)=> {
    $(imgClass).attr('src',URL.createObjectURL(blob))
    })
};

function drawFiguresOutliers(imgClass,Imgurl)
{
  // alert(imgClass);
      fetch(Imgurl,{method:'GET',mode:'no-cors'})

    .then((response)=> response)
    .then((response)=>response.blob())
    .then((blob)=> {
    $(imgClass).attr('src',URL.createObjectURL(blob))
    })
};

function drawFiguresDistribution(imgClass,Imgurl)
{
  // alert(imgClass);
      fetch(Imgurl,{method:'GET',mode:'no-cors'})

    .then((response)=> response)
    .then((response)=>response.blob())
    .then((blob)=> {
    $(imgClass).attr('src',URL.createObjectURL(blob))
    })
};

function drawFigures(imgClass,Imgurl)
{
  // alert(imgClass);
      fetch(Imgurl,{method:'GET',mode:'no-cors'})

    .then((response)=> response)
    .then((response)=>response.blob())
    .then((blob)=> {
    $(imgClass).attr('src',URL.createObjectURL(blob))
    })
};