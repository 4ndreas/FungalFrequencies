<script setup>
const props = defineProps(['board', 'time', 'device'])

board = props.board;
time = props.time;
device = props.device;

onMounted(() => {
  console.log("p5chart mounted");

  var myp5 = new p5(s, 'vue-canvas');
  // this.getData();
  });

  // this.getAsData(props.board,props.time, props.device);

  // setInterval(() => {
  //   getData(this.board,this.time,this.device)
  //   console.log("update Data");
  //   console.log(rawData);
  // }, 3000)

</script>


<script>
import { ref, onMounted } from 'vue'
import p5 from 'p5';

let board = 3;
let time = -10;
let device = ""


console.log(board);
console.log(time);
console.log(device);

// export default {
//   props: ['board'],
//   setup(props) {
//     // setup() receives props as the first argument.
//     console.log(props.board)
//   }
// }

// import * as influxData from './influxData.js'
let rawData;



var s = function( p ) { // p could be any variable name
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

    // Set the color mode to hue-saturation-brightness (HSB)
    // p.colorMode(p.HSB);
    
    getData(board,time, device);
    console.log(rawData)


    // p.background(0);
    // let data = Array.from({length: 20}, () => Math.floor(Math.random() *2+ 20));
    // drawDataSlice(data,(Math.random() * 200),0,p);
    // data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    // drawDataSlice(data,(Math.random() * 200),1,p);    
    // data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    // drawDataSlice(data,(Math.random() * 200),2,p);
    // data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    // drawDataSlice(data,(Math.random() * 200),3,p);
    // data = Array.from({length: 20}, () => Math.floor(Math.random() * 2+ 20));
    // drawDataSlice(data,(Math.random() * 200),4,p);
    // data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    // drawDataSlice(data,(Math.random() * 200),5,p);
    // data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    // drawDataSlice(data,(Math.random() * 200),6,p);
    // data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    // drawDataSlice(data,(Math.random() * 200),7,p);        
  };

  p.draw = function() {
    plot();
};

function getData(board, time, device) {
	// let rawData;
  let url = "./idata?b=" + board + "&t=" + time + "&d=" + device
//   console.log(url)
	fetch(url)
		.then(res => res.json())
		.then(out => {
      rawData = out;
    })
		.catch(err => console.log(err));


    // const response = await fetch(url);
    // // response = response.json();
    // let rawData = await response.json();
    // // console.log(rawData)
    // return  (await Promise.all(rawData));
    // // return(await response.json());
	}

  async function getAsData(board, time, device) {
    let url = "./idata?b=" + board + "&t=" + time + "&d=" + device
    const response = await fetch(url);
    rawData = await response.json();
    // console.log(rawData);
    // return(rawData);
	}

function plot()
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
}

function logData()
{
  console.log(rawData);
}

function drawDataSlice(data,min,max,r,nSlices,n,p)
{
  let nSegments = data.length;

  // console.log(data);

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
      //  console.log(v)
      
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
    // let grad = p.drawingContext.createLinearGradient(250, 250, 250+r, 250);
		let s = (Math.PI*2)/(n);

    // Add three color stops
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
    <div>
      <div id="vue-canvas"></div>
      <button @click="getData">update Data</button>
      <button @click="getAsData">update AsData</button>
      <button @click="plot">plot</button>
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
