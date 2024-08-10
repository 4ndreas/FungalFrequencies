<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
import p5 from 'p5';
const props = defineProps(['board', 'time','stepSize', 'device','canvas'])

// props default values
let board = 2;
let time = -(15*60);
let device = "FungalFrequencies_7483aff9d108"
let stepSize = 10;
let canvas = "vue-canvas";

let rawData;
let myp5 ;

board = props.board;
// time = props.time;
// stepSize = props.stepSize;
device = props.device;
canvas = props.canvas;


onMounted(() => {
  console.log("p5chart mounted on: " +canvas);
  myp5 = new p5(s, canvas);
  // time = props.time;
  // console.log("chart sampleTime:" + time)
  setInterval(() => {
    
    upData();
  }, 5000)
  });


let s = function( p ) { 
  var x = 100; 
  var y = 100;
  var speed = 2.5;
  p.setup = function() {
    p.createCanvas(320  , 320);
    // p.angleMode(p.DEGREES);

    // Set text color, size, and alignment
    p.fill(255);
    p.textSize(20);
    p.textAlign(p.CENTER, p.CENTER);
    p.frameRate(1);
    
    getData(board,time, stepSize,device);
    // console.log(rawData);
  };

  p.draw = function() {
    plot(p);
  };

}


function getData(board, time, stepSize, device) {

let url = "./idata?b=" + board + "&t=" + time + "&d=" + device + "&s=" + stepSize; 

fetch(url)
  .then(res => res.json())
  .then(out => {
    rawData = out;
  })
  .catch(err => console.log(err));
}

// async function getAsData(board, time, device) {
// let url = "./idata?b=" + board + "&t=" + time + "&d=" + device
// const response = await fetch(url);
// rawData = await response.json();
// }

function logData()
{
console.log(rawData);
}

function upData()
{
  console.log("update Data");
  getData(board,time,stepSize,device);
}

function manualUpdate()
{
  plot(myp5);
}

function plot(p)
{
  var nSlices = 8;
  p.background(0);
  var min = 0;
  var max = 0;

  var mins = [];
  var maxs = [];

  if(rawData != undefined)
  {
    for(let i= 0; i< 8; i++){
      mins[i] = Math.min(... rawData[i]);
      maxs[i] = Math.max(... rawData[i]);

      min = Math.min(mins[i], min);
      max = Math.max(maxs[i], max);
    }

  var radius = 130;
  var dMax = Math.max(Math.abs(min),Math.abs(max));

  // console.log("max:" + max + " min:" + min);
    for(let i= 0; i< 8; i++){
          if((mins[i] != 0 ) || (maxs[i] != 0)){
            var segRad = radius;
            // if((mins[i] != 0 ) && (maxs[i] != 0)){

              segRad = (Math.max(Math.abs(mins[i]),Math.abs(maxs[i])) / dMax) * 0.15 * radius + radius;

            //   // console.log(i +" rad:" + segRad + " mins[i]"+ mins[i] + " maxs[i]"+ maxs[i] +" dMax:" + dMax);
            // }
            // if ((i == 3)||(i == 4))
            // {
          
            // }
            // console.log(rawData[i]);
            // }
            drawDataSlice(rawData[i],mins[i],maxs[i],segRad,nSlices,i,p);   
          }
        }
    }
  };




function drawDataSlice(data,min,max,r,nSlices,n,p)
{
  let nSegments = data.length;

  for (var i=0;i<nSegments;i+=1)
  {
      let angle = (i* (Math.PI*2)/(nSegments * nSlices)) + (n* (Math.PI*2)/nSlices);

      let v = 0.6
      if((min != 0 ) && (max != 0))
      {
        var dir = 1;
        if (data[i] < 0){
          dir = -1;
        }

        var sx = Math.max((Math.abs(min),Math.abs(max)));
        // v = Math.abs(data[i])/((sx)*1.5);

        v = v + Math.abs(data[i])/((sx)*1.0);

        v = Math.min(Math.max(v,0),1);
        v = v*0.9;
        

      }

      p.push();                       
      p.translate(p.width/2, p.height/2);
      p.rotate(angle);
      drawSlice(0,0,r,v,nSegments,nSlices,dir,p)

      p.pop();                        
  }

}


function drawSlice(cx,cy,r,v,n,ng,dir,p)
{

  const grad = p.drawingContext.createLinearGradient(cx, cy, cx+r, cy);
  // const grad = p.drawingContext.createRadialGradient(cx, cy, r/2, cx+r, cy,r/2);

  let s = (Math.PI*2)/(n);

  var color = 'orange'
  if(dir< 0)
  {
    color = 'cyan'
  }

  grad.addColorStop(0, "black");
  if(v > 0.4)
  {
    grad.addColorStop(0.3, "black");
  }
  if(v > 0.05){
  grad.addColorStop(v-0.05, color);
  }
  grad.addColorStop(v, "white");
  if(v < 1-0.05){
    grad.addColorStop(v+0.05, color);
    grad.addColorStop(1, "black");
  }

  p.drawingContext.beginPath();
  p.drawingContext.moveTo(cx,cy);
  p.drawingContext.fillStyle = grad;
  
  
  p.drawingContext.arc(cx,cy,r,0,s/ng,false); 
  p.drawingContext.closePath();
  
  p.drawingContext.fill();
}

</script>


<script>

</script>

<template>
    <div  class="p5chart">
      <!-- <button @click="manualUpdate">plot</button> -->
      <!-- <button @click="logData">logData</button> -->
    </div>
</template>

<style scoped>
#vue-canvas {
  display: block;
  margin: 0 0;
  padding: 0 0;
  /* width: 500px; */
  /* height: 500px; */
  border-radius: 0px;
  overflow: hidden;  
}

div {
  top: 0;
  left: 0;
  margin: 0 0;
  padding: 0 0;
}
</style>
