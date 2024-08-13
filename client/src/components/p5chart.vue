<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
import p5 from 'p5';
import axios from 'axios';
// const props = defineProps(['board','time','stepSize', 'device','buffered','animate','radius','canvas'])
const props = defineProps({
                            board: { type: Number,default: 2},
                            time: { type: Number,default: -(15*60)},
                            stepSize: { type: Number,default: 10},
                            device: { type: String,default: "FungalFrequencies_7483aff9d108"},
                            buffered: { type: Boolean,default: false},
                            animate: { type: Boolean, default: false},
                            spiker: { type: Boolean, default: false},
                            slicesToShow: { type: Number, default: 8},
                            radius: { type: Number, default: 130},
                            cWidth: { type: Number, default: 320},
                            canvas: { type: String, required: true}
                          });

// 
let time = props.time;
let stepSize = props.stepSize;
let radius = props.radius;
let cWidth = props.cWidth;
let board = props.board;
let device = props.device;
let canvas = props.canvas;
let buffered = props.buffered;
let animate = props.animate;
let spiker = props.spiker;
let slicesToShow = props.slicesToShow;

let rawData;

let spike = {
board: 0,
channel: 0,
spikeWord: "" };

let dataAutoUpdate = true;
let myp5 ;
let updateInt = 10000 + Math.random()*1000;
let animationCounter = 0
let animationChannel = 0


onMounted(() => {
  console.log("p5chart mounted on: " + canvas);
  myp5 = new p5(s, canvas);

  setInterval(() => {
    
    upData();
  }, updateInt)
});


// create p5 canvas draw
let s = function( p ) { 
  p.setup = function() {
    p.createCanvas(cWidth  , cWidth);
    // p.angleMode(p.DEGREES);

    // Set text color, size, and alignment
    p.fill(255);
    p.textSize(20);
    p.textAlign(p.CENTER, p.CENTER);
    p.frameRate(1);
    
    upData();
    // getData(board,time, stepSize,device);
  };

  p.draw = function() {
    plot(p);
  };
}

function getData(board, time, stepSize, device) {
  var url = "./idata?b=" + board + "&t=" + time + "&d=" + device + "&s=" + stepSize; 

  fetch(url)
    .then(res => res.json())
    .then(out => {
      rawData = out;
    })
    .catch(err => console.log(err));
}

function getBufferedData(id){

  var url = "./bdata?b=" + id; 

  fetch(url)
    .then(res => res.json())
    .then(out => {
      rawData = out.data;
    })
    .catch(err => console.log(err));  
}

function upData()
{
  console.log("update Data");

  if(dataAutoUpdate)
  {
    if(buffered)
    {
      getBufferedData(board);
    }
    else
    {
      getData(board,time,stepSize,device);
    }
    if(spiker)
    {
      dataAutoUpdate = false
    }
  }

  if(spiker){
    var url = "./spike";
    fetch(url)
      .then(res => res.json())
      .then(out => {
        if((spike.board != out.board)||
        (spike.channel != out.channel)||
        (spike.spikeWord != out.spikeWord)
        ){
          saveIMG();
          board = spike.board;
          dataAutoUpdate = true;
          spike = out;
          console.log("spike update board" + board + " channel:" + spike.channel + " Word:" + spike.spikeWord);
          
        }
      })
      .catch(err => console.log(err));
  }
}


function dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(dataURI.split(',')[1]);
    else
        byteString = unescape(dataURI.split(',')[1]);
    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ia], {type:mimeString});
}

function saveIMG()
{
  var currentdate = new Date(); 
var datetime = + currentdate.getFullYear() + "-"
                + (currentdate.getMonth()+1)  + "-" 
                + currentdate.getDate() + "T"

                + currentdate.getHours() + "_"  
                + currentdate.getMinutes() + "_" 
                + currentdate.getSeconds();

var filename = datetime + "_B"+ board+ "_C"+ spike.channel + "W:" + spike.spikeWord +".png";
//   // var img = myp5.save( filename); 
//   var img = myp5.toDataURL("image/jpeg", 0.8);

// const blob = myp5.canvas.toBlob(function(blob){...}, 'image/jpeg', 0.95);

const blob = dataURItoBlob(myp5.canvas.toDataURL());
const mypostparameters= new FormData();
mypostparameters.append('image', blob, filename);
axios.post('/upload' , mypostparameters);

// const cCanvas = document.getElementById(canvas);
  // const canvasData = myp5.canvas.toDataURL();
  
  // fetch('/upload', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/octet-stream' },
  //   body: canvasData
  // });

// const mypostparameters= new FormData()
//  mypostparameters.append('image', canvasData, filename);
//  axios.post('/upload' , mypostparameters);
}

function manualUpdate()
{
  plot(myp5);
}

function plot(p)
{
  var nSlices = slicesToShow;
  if(animate)
  {
    animationCounter++;

    if(animationCounter > 30)
    {
      console.log(animationCounter)
      animationChannel ++;
      animationCounter = 0;
      if(animationChannel > 7)
        {
          animationChannel = 0;
        }
    }
  }

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

  var dMax = Math.max(Math.abs(min),Math.abs(max));
    for(let j= 0; j< nSlices; j++){

          var i = j;
          if(animate)
          {
            i = animationChannel;
          }
          if(spiker)
          {
            i = spike.channel;
          }
          if((mins[i] != 0 ) || (maxs[i] != 0)){
            var segRad = radius;
              segRad = (Math.max(Math.abs(mins[i]),Math.abs(maxs[i])) / dMax) * 0.20 * radius + radius;
            drawDataSlice(rawData[i],mins[i],maxs[i],segRad,nSlices,i,p);   
          }
        }
    }
  };




function drawDataSlice(data,min,max,r,nSlices,n,p)
{
  if(animate)
  {
    n = 0;
  }
  let nSegments = data.length;

  for (var i=0;i<nSegments;i+=1)
  {
      let angle = (i* (Math.PI*2)/(nSegments * nSlices)) + (n* (Math.PI*2)/nSlices);

      p.push();                       
      p.translate(p.width/2, p.height/2);
      p.rotate(angle);

      if((min != 0 ) || (max != 0)) //o only draw slice if valid data is available
      {
        var hue = 47;
        if (data[i] < 0){
          hue = 192;
        } 
        var amp = Math.abs(data[i])/((260)) *100; // use absolute range of data +-256mV
        amp = Math.min(Math.max(amp,50),100);

        // var color = p.color('HSB', hue,1,lightness).hex;
        // var color = p.color('hsl('+hue+', 100%, '+lightness+'%)');
        var Saturation = amp;
        var lightness = 50;
        var color = p.color('hsl('+hue+', '+Saturation+'%, '+lightness+'%)');
        // console.log(color)

        var sx = Math.max((Math.abs(min),Math.abs(max)));
        // v = Math.abs(data[i])/((sx)*1.5);
        let v = 0.5
        v = v + Math.abs(data[i])/((sx)*1.0);
        v = Math.min(Math.max(v,0),1);
        v = v*0.9;
 
        drawSlice(0,0,r,v,nSegments,nSlices,color,p)
      }

      p.pop();                        
  }

}


function drawSlice(cx,cy,r,v,n,ng,color,p)
{

  const grad = p.drawingContext.createLinearGradient(cx, cy, cx+r, cy);
  // const grad = p.drawingContext.createRadialGradient(cx, cy, r/2, cx+r, cy,r/2);

  let s = (Math.PI*2)/(n)*1.05;

  try{
    if(Number.isNaN(v))
    {
      v = 0.5;
    }
    
    grad.addColorStop(0, "black");
    if(v > 0.4)
    {
      grad.addColorStop(v-0.40, "black");
      grad.addColorStop(0.3, "black");
    }
    if(v > 0.05){
    grad.addColorStop(v-0.05, color);
    }
    grad.addColorStop(v, "white");

    if(v < 1-0.05){
      grad.addColorStop(v+0.05, color);
      
    }
    grad.addColorStop(1, "black");
  }
  catch(error)
  {
    console.log(error);
    console.log(v);
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
