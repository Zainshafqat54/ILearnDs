var deleteBtn = d3.select(".RegenerateStructure");
var svgContainer = d3.select("#neural-network-Structure");
// Add a click event listener to the delete button
deleteBtn.on("click", function() {
  // Remove the SVG from the container
  svgContainer.selectAll("svg").remove();
});

$(document).ready(function() {

    $('.RNN_Form').submit(function(event) {
        // alert("Hello");
        event.preventDefault();
        $(".clickToBackText").hide()
// Prompt the user for the number of input nodes, hidden layers, nodes in a hidden layer, and output nodes
var numInputs = $('.RNN-input-neurons').val();
var numHiddenLayers = $('.RNN-hidden-layers').val();
var numNodesPerLayer = $('.RNN-neurons-per-layer').val();
var numOutputs = $('.RNN-output-neurons').val();



var inputNodeYVal =25;
var outputNodeYVal=25;
var hiddenNodeYVal=25;

var SpaceBtwNodes=70;
if(numNodesPerLayer>3)
{
let floatNum = numNodesPerLayer/2;
let intNum = parseInt(floatNum);

inputNodeYVal= 50*intNum - 25;
// console.log(inputNodeYVal);

 outputNodeYVal= 50*intNum - 25;

};

// prompt(inputNodeYVal);

// Define the dimensions of the SVG container
var svgWidth = document.getElementById('DisplayStructure').clientWidth;
var svgHeight = document.getElementById('DisplayStructure').clientHeight;


var margin = {top: 20, right: 20, bottom: 20, left: 20};

// Create the SVG container using D3
var svg = svgContainer
  .append("svg")
  // .attr("width", svgWidth + margin.left + margin.right)
  // .attr("width", svgWidth)
  // .attr("height", 50 + Math.max(numInputs, numOutputs, numHiddenLayers * numNodesPerLayer) * 50 + margin.top + margin.bottom)
//   .attr("height", svgHeight)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Define the zoom behavior
var zoom = d3.zoom()
  .scaleExtent([0.5, 5])
  .on("zoom", function() {
    svg.attr("transform", d3.event.transform);
  });

// Add the zoom behavior to the SVG container
svg.call(zoom);

// Define the zoom-in and zoom-out functions
function zoomIn(d) {
  d3.select(this).attr("r", radius * 1.5);
}

function zoomOut(d) {
  d3.select(this).attr("r", radius);
}



// Define the positions of the nodes in the neural network
var inputNodes = [];
for (var i = 0; i < numInputs; i++) {
  inputNodes.push({x: 50, y: inputNodeYVal + i * SpaceBtwNodes});
}

const RedirectLineRadius = 30;
var circleRadius = RedirectLineRadius;
var RedirectLineXpoint =0;
var RedirectLineYpoint = 0;
const lineGenerator = d3.line()
    .x(d => d[0])
    .y(d => d[1]);


var hiddenNodes = [];
for (var i = 0; i < numHiddenLayers; i++) {
  for (var j = 0; j < numNodesPerLayer; j++) {
    hiddenNodes.push({x: 200 + i * 100, y: hiddenNodeYVal + j * SpaceBtwNodes});
    const points = d3.range(0, 360, 10).map(angle => {
                    RedirectLineXpoint=200 + i * 100;
                    RedirectLineYpoint=hiddenNodeYVal + j * SpaceBtwNodes;
                    var radians = angle * Math.PI / 180;
  
                    return [RedirectLineXpoint + circleRadius * Math.cos(radians), RedirectLineYpoint + circleRadius * Math.sin(radians)];
                });

                const path = svg.append("path")
                    .attr("d", lineGenerator(points))
                    .attr("stroke", "red")
                    .attr("fill", "none")
                    .attr("marker-end", "url(#arrow)");

                svg.append("defs").append("marker")
                    .attr("id", "arrow")
                    .attr("viewBox", "0 -5 10 10")
                    .attr("refX", 8)
                    .attr("refY", 0)
                    .attr("markerWidth", 6)
                    .attr("markerHeight", 6)
                    .attr("orient", "auto")
                    .append("path")
                    .attr("d", "M0,-5L10,0L0,5")
                    .attr("fill", "red");
  }
  
}

var outputNodes = [];
// prompt(350 + (numHiddenLayers * 100));
for (var i = 0; i < numOutputs; i++) {
  outputNodes.push({x: 250 + (numHiddenLayers * 100), y: outputNodeYVal + i * SpaceBtwNodes});
}

 let radius=25;
// Draw the input nodes
svg.selectAll(".input-node")
  .data(inputNodes)
  .enter()
  .append("circle")
  .attr("class", "input-node")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("fill", "#FFA3FD")
  .attr("r", radius)
  .on("mouseover", zoomIn)
  .on("mouseout", zoomOut);

// Draw the hidden nodes
svg.selectAll(".hidden-node")
  .data(hiddenNodes)
  .enter()
  .append("circle")
  .attr("class", "hidden-node")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("r", radius)
  .attr("fill", "#95BDFF")
  .on("mouseover", zoomIn)
  .on("mouseout", zoomOut); 

// Draw the output nodes
svg.selectAll(".output-node")
  .data(outputNodes)
  .enter()
  .append("circle")
  .attr("class", "output-node")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("r", radius)
  .attr("fill", "#C36A2D")
  .on("mouseover", zoomIn)
  .on("mouseout", zoomOut);

// Draw the connections between nodes
var connections = [];
for (var i = 0; i < numInputs; i++) {
  for (var j = 0; j < numNodesPerLayer; j++) {
    connections.push([{x: 50, y: inputNodeYVal + i * SpaceBtwNodes}, {x: 200, y: 25 + j * SpaceBtwNodes}]);
  }
}

for (var i = 0; i < numHiddenLayers - 1; i++) {
  for (var j = 0; j < numNodesPerLayer; j++) {
	for (var k = 0; k < numNodesPerLayer; k++) {
	connections.push([{x: 200 + i * 100, y: 25 + j * SpaceBtwNodes}, {x: 200 + (i + 1) * 100, y: 25 + k * SpaceBtwNodes}]);
	}
	}
}

for (var i = 0; i < numNodesPerLayer; i++) {
for (var j = 0; j < numOutputs; j++) {
connections.push([{x: 200 + (numHiddenLayers - 1) * 100, y: 25 + i * SpaceBtwNodes}, {x: 250 + (numHiddenLayers * 100), y: outputNodeYVal + j * SpaceBtwNodes}]);
}
}




svg.selectAll(".connection")
.data(connections)
.enter()
.append("line")
.attr("class", "connection")
.attr("x1", function(d) { return d[0].x; })
.attr("y1", function(d) { return d[0].y; })
.attr("x2", function(d) { return d[1].x; })
.attr("y2", function(d) { return d[1].y; })
.attr("stroke-width",1)
.attr("stroke", "#999")


var nodeSize = 10; // initial size of nodes

// Add interactivity
d3.selectAll(".node")
  .attr("r", nodeSize) // set initial size of nodes
  .on("mouseover", function(d) {
    d3.selectAll(".connection")
      .filter(function(connection) {
        return connection.source !== d.id && connection.target !== d.id;
      })
      .style("opacity", "0.2");
    d3.selectAll(".node")
      .filter(function(node) {
        return node.id !== d.id;
      })
      .style("opacity", "0.2");
    d3.select(this)
      .attr("r", nodeSize + 5); // increase size of node on mouseover
  })
  .on("mouseout", function() {
    d3.selectAll(".connection")
      .style("opacity", "1");
    d3.selectAll(".node")
      .style("opacity", "1");
    d3.select(this)
      .attr("r", nodeSize); // reset size of node on mouseout
  });


  // define all connections
var connections = d3.selectAll(".connection")

// define mouseover and mouseout events on connections
connections.on("mouseover", function() {
  // get the current connection
  var currentConnection = d3.select(this)
                          
  
  // set opacity of current connection to 1 and all others to 0
  connections.style("opacity", function() {
    return (this === currentConnection.node()) ? 1 : 0;
  })
  .style("stroke-width", "4")
  .style("stroke", "red");

}).on("mouseout", function() {
  // reset opacity of all connections to 1
  connections.style("opacity", 1)
              .style("stroke-width", "1")
              .style("stroke", "#999");
});



// Define the data for the circles
var circleData = [
    { "color": "#FFA3FD", "radius": 15 , node:"Input"},
    { "color": "#95BDFF", "radius": 15 , node:"Hidden"},
    { "color": "#C36A2D", "radius": 15  ,node:"Output"}
];

// Get the computed style of the SVG container
var svgStyle = window.getComputedStyle(svgContainer.node());

// Get the height of the SVG container
var svgHeight = parseInt(svgStyle.getPropertyValue("height"), 10);


// Log the height to the console
// console.log("SVG Height: " + svgHeight);

// alert(svgHeight);

var circles = svg.selectAll(".legendsOfNeurons")
    .data(circleData)
    .enter()
    .append("circle");

circles.attr("cx", function(d, i) { return 150 + i * 200; })
    .attr("cy", svgHeight-100)
    .attr("r", function(d) { return d.radius; })
    .style("fill", function(d) { return d.color; });

var text = svg.selectAll("text")
    .data(circleData)
    .enter()
    .append("text");

text.attr("x", function(d, i) { return 200 + i * 200; })
    .attr("y", svgHeight-95)
    .text(function(d) { return d.node; })
    .style("text-anchor", "middle");

    });


//RNN 


$('.ANN_Form').submit(function(event) {
        // alert("Hello");
        event.preventDefault();
        $(".clickToBackText").hide()
// Prompt the user for the number of input nodes, hidden layers, nodes in a hidden layer, and output nodes
var numInputs = $('.ANN-input-neurons').val();
var numHiddenLayers = $('.ANN-hidden-layers').val();
var numNodesPerLayer = $('.ANN-neurons-per-layer').val();
var numOutputs = $('.ANN-output-neurons').val();



var inputNodeYVal =25;
var outputNodeYVal=25;
var hiddenNodeYVal=25;

var SpaceBtwNodes=70;
if(numNodesPerLayer>3)
{
let floatNum = numNodesPerLayer/2;
let intNum = parseInt(floatNum);

inputNodeYVal= 50*intNum - 25;
// console.log(inputNodeYVal);

 outputNodeYVal= 50*intNum - 25;

};

// prompt(inputNodeYVal);

// Define the dimensions of the SVG container
var svgWidth = document.getElementById('DisplayStructure').clientWidth;
var svgHeight = document.getElementById('DisplayStructure').clientHeight;


var margin = {top: 20, right: 20, bottom: 20, left: 20};

// Create the SVG container using D3
var svg = svgContainer
  .append("svg")
  // .attr("width", svgWidth + margin.left + margin.right)
  // .attr("width", svgWidth)
  // .attr("height", 50 + Math.max(numInputs, numOutputs, numHiddenLayers * numNodesPerLayer) * 50 + margin.top + margin.bottom)
//   .attr("height", svgHeight)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Define the zoom behavior
var zoom = d3.zoom()
  .scaleExtent([0.5, 5])
  .on("zoom", function() {
    svg.attr("transform", d3.event.transform);
  });

// Add the zoom behavior to the SVG container
svg.call(zoom);

// Define the zoom-in and zoom-out functions
function zoomIn(d) {
  d3.select(this).attr("r", radius * 1.5);
}

function zoomOut(d) {
  d3.select(this).attr("r", radius);
}



// Define the positions of the nodes in the neural network
var inputNodes = [];
for (var i = 0; i < numInputs; i++) {
  inputNodes.push({x: 50, y: inputNodeYVal + i * SpaceBtwNodes});
}

var hiddenNodes = [];
for (var i = 0; i < numHiddenLayers; i++) {
  for (var j = 0; j < numNodesPerLayer; j++) {
    hiddenNodes.push({x: 200 + i * 100, y: hiddenNodeYVal + j * SpaceBtwNodes});
  }
}

var outputNodes = [];
// prompt(350 + (numHiddenLayers * 100));
for (var i = 0; i < numOutputs; i++) {
  outputNodes.push({x: 250 + (numHiddenLayers * 100), y: outputNodeYVal + i * SpaceBtwNodes});
}

 let radius=25;
// Draw the input nodes
svg.selectAll(".input-node")
  .data(inputNodes)
  .enter()
  .append("circle")
  .attr("class", "input-node")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("fill", "#FFA3FD")
  .attr("r", radius)
  .on("mouseover", zoomIn)
  .on("mouseout", zoomOut);

// Draw the hidden nodes
svg.selectAll(".hidden-node")
  .data(hiddenNodes)
  .enter()
  .append("circle")
  .attr("class", "hidden-node")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("r", radius)
  .attr("fill", "#95BDFF")
  .on("mouseover", zoomIn)
  .on("mouseout", zoomOut); 

// Draw the output nodes
svg.selectAll(".output-node")
  .data(outputNodes)
  .enter()
  .append("circle")
  .attr("class", "output-node")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("r", radius)
  .attr("fill", "#C36A2D")
  .on("mouseover", zoomIn)
  .on("mouseout", zoomOut);

// Draw the connections between nodes
var connections = [];
for (var i = 0; i < numInputs; i++) {
  for (var j = 0; j < numNodesPerLayer; j++) {
    connections.push([{x: 50, y: inputNodeYVal + i * SpaceBtwNodes}, {x: 200, y: 25 + j * SpaceBtwNodes}]);
  }
}

for (var i = 0; i < numHiddenLayers - 1; i++) {
  for (var j = 0; j < numNodesPerLayer; j++) {
	for (var k = 0; k < numNodesPerLayer; k++) {
	connections.push([{x: 200 + i * 100, y: 25 + j * SpaceBtwNodes}, {x: 200 + (i + 1) * 100, y: 25 + k * SpaceBtwNodes}]);
	}
	}
}

for (var i = 0; i < numNodesPerLayer; i++) {
for (var j = 0; j < numOutputs; j++) {
connections.push([{x: 200 + (numHiddenLayers - 1) * 100, y: 25 + i * SpaceBtwNodes}, {x: 250 + (numHiddenLayers * 100), y: outputNodeYVal + j * SpaceBtwNodes}]);
}
}




svg.selectAll(".connection")
.data(connections)
.enter()
.append("line")
.attr("class", "connection")
.attr("x1", function(d) { return d[0].x; })
.attr("y1", function(d) { return d[0].y; })
.attr("x2", function(d) { return d[1].x; })
.attr("y2", function(d) { return d[1].y; })
.attr("stroke-width",1)
.attr("stroke", "#999")
.attr("marker-end", "url(#arrow-Connection)");

svg.append("defs").append("marker")
    .attr("id", "arrow-Connection")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 8)
    .attr("refY", 0)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M0,-5L10,0L0,5")
    .attr("fill", "#999");




var nodeSize = 10; // initial size of nodes

// Add interactivity
d3.selectAll(".node")
  .attr("r", nodeSize) // set initial size of nodes
  .on("mouseover", function(d) {
    d3.selectAll(".connection")
      .filter(function(connection) {
        return connection.source !== d.id && connection.target !== d.id;
      })
      .style("opacity", "0.2");
    d3.selectAll(".node")
      .filter(function(node) {
        return node.id !== d.id;
      })
      .style("opacity", "0.2");
    d3.select(this)
      .attr("r", nodeSize + 5); // increase size of node on mouseover
  })
  .on("mouseout", function() {
    d3.selectAll(".connection")
      .style("opacity", "1");
    d3.selectAll(".node")
      .style("opacity", "1");
    d3.select(this)
      .attr("r", nodeSize); // reset size of node on mouseout
  });


  // define all connections
var connections = d3.selectAll(".connection")

// define mouseover and mouseout events on connections
connections.on("mouseover", function() {
  // get the current connection
  var currentConnection = d3.select(this)
                          
  
  // set opacity of current connection to 1 and all others to 0
  connections.style("opacity", function() {
    return (this === currentConnection.node()) ? 1 : 0;
  })
  .style("stroke-width", "4")
  .style("stroke", "red");

}).on("mouseout", function() {
  // reset opacity of all connections to 1
  connections.style("opacity", 1)
              .style("stroke-width", "1")
              .style("stroke", "#999");
});



// Define the data for the circles
var circleData = [
    { "color": "#FFA3FD", "radius": 15 , node:"Input"},
    { "color": "#95BDFF", "radius": 15 , node:"Hidden"},
    { "color": "#C36A2D", "radius": 15  ,node:"Output"}
];

// Get the computed style of the SVG container
var svgStyle = window.getComputedStyle(svgContainer.node());

// Get the height of the SVG container
var svgHeight = parseInt(svgStyle.getPropertyValue("height"), 10);


// Log the height to the console
// console.log("SVG Height: " + svgHeight);

// alert(svgHeight);

var circles = svg.selectAll(".legendsOfNeurons")
    .data(circleData)
    .enter()
    .append("circle");

circles.attr("cx", function(d, i) { return 150 + i * 200; })
    .attr("cy", svgHeight-100)
    .attr("r", function(d) { return d.radius; })
    .style("fill", function(d) { return d.color; });

var text = svg.selectAll("text")
    .data(circleData)
    .enter()
    .append("text");

text.attr("x", function(d, i) { return 200 + i * 200; })
    .attr("y", svgHeight-95)
    .text(function(d) { return d.node; })
    .style("text-anchor", "middle");

    });



$('.CNN_Form').submit(function(event) {
        // alert("Hello");
        event.preventDefault();
        $(".clickToBackText").hide()

// Prompt the user for the number of input nodes, hidden layers, nodes in a hidden layer, and output nodes

var numconvlayer = $('.CNN-Conv-Layers').val();
var numHiddenLayers = $('.CNN-hidden-layers').val();
var numNodesPerLayer = $('.CNN-neurons-per-layer').val();
var numOutputs = $('.CNN-output-neurons').val();

numconvlayer = numconvlayer *2;


var inputNodeYVal=25;
var outputNodeYVal=25;

if(numNodesPerLayer>3)
{
let floatNum = numNodesPerLayer/2;
let intNum = parseInt(floatNum);

inputNodeYVal= 50*intNum - 25;
// console.log(inputNodeYVal);

 outputNodeYVal= 50*intNum - 25;

};

// prompt(inputNodeYVal);

// Define the dimensions of the SVG container
var svgWidth = 800;
var svgHeight = 900;

var margin = {top: 50, right: 50, bottom: 50, left: 50};

// Create the SVG container using D3
var svg = svgContainer
  .append("svg")
  .attr("width", svgWidth + margin.left + margin.right)
  .attr("height", svgHeight)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");



var convlayer = [];
var flattened = [];
for (var i = 0; i < numconvlayer; i++) {
  convlayer.push({x: 130+ i * 100, y: 30});
  if(i==numconvlayer-1)
  {
    if(numconvlayer<=2)
      {
        flattened.push({x: 195+ i * 100, y: 25});
      }
    else if (numconvlayer>2 && numconvlayer <=4)
      {
        flattened.push({x: 185+ i * 100, y: 25});
      }
    else if(numconvlayer>4 && numconvlayer <=6)
    {
      flattened.push({x: 172+ i * 100, y: 25});
    }
    //flattened.push({x: 180+ i * 100, y: 30});
  }
}
var convlayer2 = [];
for (var i = 0; i < numconvlayer; i++) {
  convlayer2.push({x: 125+ i * 100, y: 25});
}
var convlayer3 = [];
for (var i = 0; i < numconvlayer; i++) {
  convlayer3.push({x: 120+ i * 100, y: 20});
}
var convlayer4 = [];
for (var i = 0; i < numconvlayer; i++) {
  convlayer4.push({x: 115+ i * 100, y: 15});
}
var selectlayer = [];
for (var i = 0; i < numconvlayer-1; i++) {
  selectlayer.push({x: 134+ i * 100, y: 99});
}

var selectlayer2 = [];
for (var i = 0; i < numconvlayer; i++) {
  selectlayer.push({x: 155+ i * 100, y: 42 + i*4});
}

var hiddenNodes = [];
for (var i = 0; i < numHiddenLayers; i++) {
  for (var j = 0; j < numNodesPerLayer; j++) {
    if(numconvlayer<=2)
      {
        hiddenNodes.push({x: 200 * numconvlayer + i * 100, y: 25 + j * 60});
      }
    else if (numconvlayer>2 && numconvlayer <=4)
      {
        hiddenNodes.push({x: 160 * numconvlayer + i * 100, y: 25 + j * 60});
      }
    else if(numconvlayer>4 && numconvlayer <=6)
    {
      hiddenNodes.push({x: 130 * numconvlayer + i * 100, y: 25 + j * 60});
    } 
  }
}

var outputNodes = [];
// prompt(350 + (numHiddenLayers * 100));
for (var i = 0; i < numOutputs; i++) {
  if(numconvlayer<=2)
      {
        outputNodes.push({x: 200 * numconvlayer + (numHiddenLayers * 100), y: 25 + i * 60});
      }
    else if (numconvlayer>2 && numconvlayer <=4)
      {
        outputNodes.push({x: 160 * numconvlayer + (numHiddenLayers * 100), y: 25 + i * 60});
      }
    else if(numconvlayer>4 && numconvlayer <=6)
    {
      outputNodes.push({x: 130 * numconvlayer + (numHiddenLayers * 100), y: 25 + i * 60});
    } 
 // outputNodes.push({x: 160 * numconvlayer + (numHiddenLayers * 100), y: 25 + i * 60});
}

var textinfo = [];
// prompt(350 + (numHiddenLayers * 100));
for (var i = 0; i < numconvlayer; i++) {
  textinfo.push({x: 20 + i * 100, y: -50});
}
var hiddenlayerinfo = [];
// prompt(350 + (numHiddenLayers * 100));
for (var i = 0; i < numHiddenLayers; i++) {
  if(numconvlayer<=2)
      {
        hiddenlayerinfo.push({x: 120 * numconvlayer + i * 100, y: -50});
      }
    else if (numconvlayer>2 && numconvlayer <=4)
      {
        hiddenlayerinfo.push({x: 130 * numconvlayer + i * 100, y: -50});
      }
    else if(numconvlayer>4 && numconvlayer <=6)
    {
      hiddenlayerinfo.push({x: 108 * numconvlayer + i * 100, y: -50});
    } 
  //hiddenlayerinfo.push({x: 130 * numconvlayer + i * 100, y: -50});
}
outputnodeinfo=[];
if(numconvlayer<=2)
      {
        outputnodeinfo.push({x: 120 * numconvlayer + (numHiddenLayers * 100), y: -50});
      }
else if (numconvlayer>2 && numconvlayer <=4)
      {
        outputnodeinfo.push({x: 130 * numconvlayer + (numHiddenLayers * 100), y: -50});
      }
else if(numconvlayer>4 && numconvlayer <=6)
      {
        outputnodeinfo.push({x: 108 * numconvlayer + (numHiddenLayers * 100), y: -50});
      } 

dottedline=[];      
if(numconvlayer<=2)
      {
        dottedline.push([{x: 165 * numconvlayer + (numHiddenLayers * 100) , y: -30}, {x: 165 * numconvlayer + (numHiddenLayers * 100) , y: 100 + 50 * numOutputs}]);
      }
else if (numconvlayer>2 && numconvlayer <=4)
      {
        dottedline.push([{x: 152 * numconvlayer + (numHiddenLayers * 100) , y: -30}, {x: 152 * numconvlayer + (numHiddenLayers * 100) , y: 100 + 50 * numOutputs}]);
      }
else if(numconvlayer>4 && numconvlayer <=6)
    {
      dottedline.push([{x: 123 * numconvlayer + (numHiddenLayers * 100) , y: -30}, {x: 123 * numconvlayer + (numHiddenLayers * 100) , y: 100 + 50 * numOutputs}]);
    } 
 let radius=20;
svg.append("text")
			.text("Input Image")
			.attr("x", -100)
			.attr("y", -50)
			.attr("transform", "translate(100, 50)")
      .classed("bold-text", true);
svg.selectAll(".texti")
      .data(textinfo)
      .enter()
      .append("text")
      .attr("class", "texti")
      .attr("x", function(d) { return d.x; })
      .attr("y", function(d) { return d.y; })
      .attr("transform", "translate(100, 50)")
      .text(function(d, i) {
        if (i % 2 === 0) {
          return "CNN layer";
        } else {
          return "Max pooling";
        }
      })
      .classed("bold-text", true);

svg.selectAll(".textla")
      .data(hiddenlayerinfo)
      .enter()
      .append("text")
      .attr("class", "textla")
      .text("Hidden layer")
      .attr("x", function(d) { return d.x; })
      .attr("y", function(d) { return d.y; })
      .attr("transform", "translate(100, 50)")
      .classed("bold-text", true);
      
svg.selectAll(".textla1")
      .data(outputnodeinfo)
      .enter()
      .append("text")
      .attr("class", "textla1")
      .text("output layer")
      .attr("x", function(d) { return d.x; })
      .attr("y", function(d) { return d.y; })
      .attr("transform", "translate(100, 50)")
      .classed("bold-text", true);
      

    
const rect = svg.append("rect")
		.attr("x",10)
		.attr("y", 15)
		.attr("width", 70)
		.attr("height", 90)
		.attr("fill", "transparent")
    .attr('stroke','black');


// Create filter
svg.append("defs")
  .append("filter")
  .attr("id", "blur-filter")
  .append("feGaussianBlur")
  .attr("stdDeviation", 3);

    const image = svg.append("image")
            .attr("x", 10)
            .attr("y", 15)
            .attr("width",70)
            .attr("height", 90)
            .attr("filter", "url(#blur-filter)")
            .attr("xlink:href", "static/js/test_Img.jpg");

const rect1 = svg.append("rect")
		.attr("x",15)
		.attr("y", 75)
		.attr("width", 10)
    .attr("height", 14)
    .attr("fill", "#69b3a2")
    .attr('stroke','black');
  
//Draw the convolution layer
svg.selectAll(".conv-layer")
  .data(convlayer)
  .enter()
  .append("rect")
  .attr("class", "conv-layer")
  .attr("x", function(d) { return d.x; })
  .attr("y", function(d, i) { 
    if (i == 0) {  // for the first iteration, set y to 0
      return d.y;
    } else {  // for subsequent iterations, add multiples of 10 to y
      return d.y + (i*6);
    }
  })
  .attr("width", function(d, i) { return 70 - i*6; })
  .attr("height", function(d, i) { return 90 - i*6; })
  .attr("fill", "transparent")
  .attr('stroke','black')


svg.selectAll(".conv-layer2")
  .data(convlayer2)
  .enter()
  .append("rect")
  .attr("class", "conv-layer2")
  .attr("x", function(d) { return d.x; })
  .attr("y", function(d, i) { 
    if (i == 0) {  // for the first iteration, set y to 0
      return d.y;
    } else {  // for subsequent iterations, add multiples of 10 to y
      return d.y + (i*6);
    }
  })
  .attr("width", function(d, i) { return 70 - i*6; })
  .attr("height", function(d, i) { return 90 - i*6; })
  .attr("fill", "transparent")
  .attr('stroke','black');
svg.selectAll(".conv-layer3")
  .data(convlayer3)
  .enter()
  .append("rect")
  .attr("class", "conv-layer3")
  .attr("x", function(d) { return d.x; })
  .attr("y", function(d, i) { 
    if (i == 0) {  // for the first iteration, set y to 0
      return d.y;
    } else {  // for subsequent iterations, add multiples of 10 to y
      return d.y + (i*6);
    }
  })
  .attr("width", function(d, i) { return 70 - i*6; })
  .attr("height", function(d, i) { return 90 - i*6; })
  .attr("fill", "transparent")
  .attr('stroke','black');
svg.selectAll(".conv-layer4")
  .data(convlayer4)
  .enter()
  .append("rect")
  .attr("class", "conv-layer4")
  .attr("x", function(d) { return d.x; })
  .attr("y", function(d, i) { 
    if (i == 0) {  // for the first iteration, set y to 0
      return d.y;
    } else {  // for subsequent iterations, add multiples of 10 to y
      return d.y + (i*6);
    }
  })
  .attr("width", function(d, i) { return 70 - i*6; })
  .attr("height", function(d, i) { return 90 - i*6; })
  .attr("fill", "transparent")
  .attr('stroke','black');  
// Set up Three.js scene
// Define the D3-3D projection
// Define the projection

//Draw the convolution layer
svg.selectAll(".select-layer")
  .data(selectlayer)
  .enter()
  .append("rect")
  .attr("class", "select-layer")
  .attr("x", function(d) { return d.x; })
  .attr("y", function(d) { return d.y; })
  .attr("width", 10)
  .attr("height", 14)
  .attr('stroke','black')
  .attr("fill", "#69b3a2")
  .attr('stroke','black');

svg.selectAll(".select-layer2")
  .data(selectlayer2)
  .enter()
  .append("rect")
  .attr("class", "select-layer2")
  .attr("x", function(d) { return d.x; })
  .attr("y", function(d) { return d.y; })
  .attr("width", 10)
  .attr("height", 14)
  .attr('stroke','black')
  .attr("fill", "#69b3a2")
  .attr('stroke','black');


svg.selectAll(".flatten")
  .data(flattened)
  .enter()
  .append("rect")
  .attr("class", "flatten")
  .attr("x", function(d) { return d.x; })
  .attr("y", function(d) { return d.y; })
  .attr("width", 40)
  .attr("height", 110)
  .attr("fill", "transparent")
  .attr('stroke','black');
svg.selectAll(".textflatten")
  .data(flattened)
  .enter()
  .append("text")
  .text("Flattened")
  .attr("class", "textflatten")
  .attr("x", function(d) { return d.x+20; })
  .attr("y", function(d) { return d.y+55; })
  .attr("text-anchor", "middle")
  .attr("alignment-baseline", "middle")
  .attr("fill", "black")
  .attr("font-size", 20)
  .attr("transform", function(d) {
    return "rotate(-90 " + (d.x+20) + " " + (d.y+55) + ")";
  });

// Draw the hidden nodes
svg.selectAll(".hidden-node")
  .data(hiddenNodes)
  .enter()
  .append("circle")
  .attr("class", "hidden-node")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("r", radius)
  .attr("fill", "#95BDFF")
  .on("mouseover", function() {
    d3.select(this)
      .attr("fill", "#95BDFF")
      .attr("r", radius * 1.5);
  })
  .on("mouseout", function() {
    d3.select(this)
      .attr("fill", "#95BDFF")
      .attr("r", radius);
  });

// Draw the output nodes
svg.selectAll(".output-node")
  .data(outputNodes)
  .enter()
  .append("circle")
  .attr("class", "output-node")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("r", radius)
  .attr("fill", "#C36A2D")
  .on("mouseover", function() {
    d3.select(this)
      .attr("fill", "#C36A2D")
      .attr("r", radius * 1.5);
  })
  .on("mouseout", function() {
    d3.select(this)
      .attr("fill", "#C36A2D")
      .attr("r", radius);
  });
svg
  .append("line")
  .attr("x1", 100)
  .attr("y1", -30)
  .attr("x2", 100)
  .attr("y2", 200)
  .attr("stroke", "black")
  .attr("stroke-width", 1)
  .attr("stroke-dasharray", "5,5");
svg.selectAll(".seperation")
  .data(dottedline)
  .enter()
  .append("line")
  .attr("class", "seperation")
  .attr("x1", function(d) { return d[0].x; })
  .attr("y1", function(d) { return d[0].y; })
  .attr("x2", function(d) { return d[1].x; })
  .attr("y2", function(d) { return d[1].y; })
  .attr("stroke", "black")
  .attr("stroke-width", 1)
  .attr("stroke-dasharray", "5,5");
// svg
//   .append("line")
//   .attr("x1", 100)
//   .attr("y1", -30)
//   .attr("x2", 100)
//   .attr("y2", 200)
//   .attr("stroke", "black")
//   .attr("stroke-width", 1)
//   .attr("stroke-dasharray", "2,2");

//Draw the connections between nodes
 var connections = [];
//Draw the connections between convolution layer 
connections.push([{x:20 , y: 77}, {x: 162 , y: 47 }]);
connections.push([{x:20 , y: 89}, {x: 162 , y: 47 }])
for (var i = 0; i < numconvlayer; i++) { 
  var counter = numconvlayer - 1;
  if (i==counter){
    for (var j = 0; j < numNodesPerLayer; j++) {
      if(numconvlayer<=2)
      {
        connections.push([{x: 233 + i * 100, y: 80}, {x: 200 * numconvlayer, y: 25 + j * 60}]);
      }
    else if (numconvlayer>2 && numconvlayer <=4)
      {
        connections.push([{x: 223 + i * 100, y: 80}, {x: 160 * numconvlayer, y: 25 + j * 60}]);
      }
    else if(numconvlayer>4 && numconvlayer <=6)
    {
      connections.push([{x: 213 + i * 100, y: 80}, {x: 130 * numconvlayer, y: 25 + j * 60}]);
    }
      //connections.push([{x: 141 + i * 100, y: 107}, {x: 160 * numconvlayer, y: 25 + j * 60}]);
    } 
  }
  else {
  connections.push([{x: 141 + i * 100 , y: 100}, {x: 260 + i * 100, y: 50 + i*4 }]);
  connections.push([{x: 141 + i * 100 , y: 113}, {x: 260 + i * 100, y: 50 + i*4 }]);
  } 
}

for (var i = 0; i < numHiddenLayers - 1; i++) {
  for (var j = 0; j < numNodesPerLayer; j++) {
	for (var k = 0; k < numNodesPerLayer; k++) {
    if(numconvlayer<=2)
      {
        connections.push([{x: 200 * numconvlayer + i * 100, y: 25 + j * 60}, {x: 200 * numconvlayer + (i + 1) * 100, y: 25 + k * 60}]);
      }
    else if (numconvlayer>2 && numconvlayer <=4)
      {
        connections.push([{x: 160 * numconvlayer + i * 100, y: 25 + j * 60}, {x: 160 * numconvlayer + (i + 1) * 100, y: 25 + k * 60}]);
      }
    else if(numconvlayer>4 && numconvlayer <=6)
    {
      connections.push([{x: 130 * numconvlayer + i * 100, y: 25 + j * 60}, {x: 130 * numconvlayer + (i + 1) * 100, y: 25 + k * 60}]);
    } 
	//connections.push([{x: 160 * numconvlayer + i * 100, y: 25 + j * 60}, {x: 160 * numconvlayer + (i + 1) * 100, y: 25 + k * 60}]);
	}
	}
}

for (var i = 0; i < numNodesPerLayer; i++) {
for (var j = 0; j < numOutputs; j++) {
  if(numconvlayer<=2)
      {
        connections.push([{x: 200 * numconvlayer + (numHiddenLayers - 1) * 100, y: 25 + i * 60}, {x: 200 * numconvlayer + (numHiddenLayers * 100), y: 25 + j * 60}]);
      }
    else if (numconvlayer>2 && numconvlayer <=4)
      {
        connections.push([{x: 160 * numconvlayer + (numHiddenLayers - 1) * 100, y: 25 + i * 60}, {x: 160 * numconvlayer + (numHiddenLayers * 100), y: 25 + j * 60}]);
      }
    else if(numconvlayer>4 && numconvlayer <=6)
    {
      connections.push([{x: 130 * numconvlayer + (numHiddenLayers - 1) * 100, y: 25 + i * 60}, {x: 130 * numconvlayer + (numHiddenLayers * 100), y: 25 + j * 60}]);
    } 
//connections.push([{x: 160 * numconvlayer + (numHiddenLayers - 1) * 100, y: 25 + i * 60}, {x: 160 * numconvlayer + (numHiddenLayers * 100), y: 25 + j * 60}]);
}
}
//connections.push([{x: 50, y: inputNodeYVal + i * 50}, {x: 200, y: 25 + j * 50}]);
svg.selectAll(".connection")
.data(connections)
.enter()
.append("line")
.attr("class", "connection")
.attr("x1", function(d) { return d[0].x; })
.attr("y1", function(d) { return d[0].y; })
.attr("x2", function(d) { return d[1].x; })
.attr("y2", function(d) { return d[1].y; })
.attr("stroke-width", 2)
.attr("stroke", "#999");

// var nodeSize = 10; // initial size of nodes

d3.selectAll(".connection")
  .on("mouseover", function(d) {
    // Set the stroke color of the current connection to red
    d3.select(this)
      .style("stroke", "red")
      .style("stroke-width", 4);
    
    // Set the opacity of all non-selected connections to zero
    svg.selectAll(".connection")
      .filter(function(e) {
        return e !== d;
      })
      .style("opacity", 0);
    
    // Set the opacity of the selected connection to 1
    d3.select(this)
      .style("opacity", 1);
    
   
  })
  .on("mouseout", function() {
    // Reset the stroke color of the current connection to black
    d3.select(this)
      .style("stroke", "#999")
      .style("stroke-width", 2);
    
    // Reset the opacity of all connections to 1
    svg.selectAll(".connection")
      .style("opacity", 1);
    
    // Remove the label from the current connection
    svg.selectAll(".connection-label")
      .remove();
  });

});

});


