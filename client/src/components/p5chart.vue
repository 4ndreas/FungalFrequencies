<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
const props = defineProps(['board', 'time', 'device','canvas'])
board = props.board;
time = props.time;
device = props.device;
canvas = props.canvas;

const id = ref(0)


onMounted(() => {
  console.log("p5chart mounted");
  console.log(canvas);
  myp5 = new p5(s, canvas);

  setInterval(() => {
    
    upData();
  }, 5000)

  });
</script>


<script type="module"  lang="ts">
import p5 from 'p5';


// props default values
let board = 2;
let time = -10;
let device = "FungalFrequencies_7483aff9d108"
let canvas = "vue-canvas";

let rawData;
let myp5 ;


let s = function( p ) { 
  var x = 100; 
  var y = 100;
  var speed = 2.5;
  p.setup = function() {
    p.createCanvas(500  , 500);
    // p.angleMode(p.DEGREES);

    // Set text color, size, and alignment
    p.fill(255);
    p.textSize(20);
    p.textAlign(p.CENTER, p.CENTER);
    p.frameRate(1);
    
    getData(board,time, device);
    // console.log(rawData);
  };

  p.draw = function() {
    plot(p);
  };

}

function manualUpdate()
{
  plot(myp5);
}

function plot(p)
{
  let nSlices = 8;
  p.background(0);
  let min = 0;
  let max = 0;

  for(let i= 0; i< 8; i++){
    min = Math.min(Math.min(... rawData[i]), min);
    max = Math.max(Math.max(... rawData[i]), max);
  }
  for(let i= 0; i< 8; i++){
        if(rawData != undefined){
          drawDataSlice(rawData[i],min,max,200,nSlices,i,p);   
        }
      }
  };


function upData()
{
  console.log("update Data");
  getData(board,time,device);
}

function getData(board, time, device) {

  let url = "./idata?b=" + board + "&t=" + time + "&d=" + device

  fetch(url)
    .then(res => res.json())
    .then(out => {
      rawData = out;
    })
    .catch(err => console.log(err));
}

async function getAsData(board, time, device) {
  let url = "./idata?b=" + board + "&t=" + time + "&d=" + device
  const response = await fetch(url);
  rawData = await response.json();
}

function logData()
{
  console.log(rawData);
}

function drawDataSlice(data,min,max,r,nSlices,n,p)
{
  let nSegments = data.length;

  for (var i=0;i<nSegments;i+=1)
  {
      let angle = (i* (Math.PI*2)/(nSegments * nSlices)) + (n* (Math.PI*2)/nSlices);

      let v = 0.5
       if((min != 0 ) && (max != 0))
       {
          v = data[i]/((Math.abs(min) + max)*1.5);
          v = v + 0.5;
          v = Math.min(Math.max(v,0),1);
       }
      
      p.push();                       
      p.translate(p.width/2, p.height/2);
      p.rotate(angle);
      drawSlice(0,0,r,v,nSegments,nSlices,p)

      p.pop();                        
  }

}


function drawSlice(cx,cy,r,v,n,ng,p)
{

  const grad = p.drawingContext.createLinearGradient(cx, cy, cx+r, cy);

		let s = (Math.PI*2)/(n);

    grad.addColorStop(0, "black");
    if(v > 0.3)
    {
      grad.addColorStop(0.2, "black");
    }
    if(v > 0.05){
    grad.addColorStop(v-0.05, "cyan");
    }
    grad.addColorStop(v, "white");
    if(v < 1-0.05){
      grad.addColorStop(v+0.05, "cyan");
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


<template>
    <div  class="p5chart">
      <!-- <div :id="dynamicId"></div> -->
      <!-- <button @click="getData">update Data</button> -->
      <!-- <button @click="getAsData">update AsData</button> -->
      <button @click="manualUpdate">plot</button>
      <button @click="logData">logData</button>
      
      
    </div>
</template>

<style scoped>
#vue-canvas {
  display: block;
  margin: 0 auto;
  padding: 0;
  width: 500px;
  height: 500px;
  border-radius: 0px;
  overflow: hidden;
}
</style>
