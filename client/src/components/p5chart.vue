<script setup>
defineProps({
  data: {
    required: false
  }  
});

onMounted(() => {
  console.log("p5chart mounted");

  var myp5 = new p5(s, 'vue-canvas');

  });

</script>


<script>
import { ref, onMounted } from 'vue'
import p5 from 'p5';

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

    // Set the color mode to hue-saturation-brightness (HSB)
    // p.colorMode(p.HSB);
    p.background(0);
    let data = Array.from({length: 20}, () => Math.floor(Math.random() *2+ 20));
    drawDataSlice(data,(Math.random() * 200),0,p);
    data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    drawDataSlice(data,(Math.random() * 200),1,p);    
    data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    drawDataSlice(data,(Math.random() * 200),2,p);
    data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    drawDataSlice(data,(Math.random() * 200),3,p);
    data = Array.from({length: 20}, () => Math.floor(Math.random() * 2+ 20));
    drawDataSlice(data,(Math.random() * 200),4,p);
    data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    drawDataSlice(data,(Math.random() * 200),5,p);
    data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    drawDataSlice(data,(Math.random() * 200),6,p);
    data = Array.from({length: 20}, () => Math.floor(Math.random() *2+  20));
    drawDataSlice(data,(Math.random() * 200),7,p);        
  };

  p.draw = function() {
    // p.background(100);
    // p.fill(1);
    // x += speed; 
    // if(x > p.width){
    //   x = 0; 
    // }
    // p.ellipse(x,y,50,50);
    // // console.log(x);


  // Clear the background
  // p.background(0);

  // // Loop through angles 0, 30, 60, 90 degrees
  // // for (let angle=0; angle <= 360; angle += 30) {
  // let nSegments = 20;
  // for (var i=0;i<nSegments;i+=1)
  // {
  //     let angle = i* (Math.PI*2)/nSegments/8;
  //     // console.log(angle);


  //     // Save current coordinate system
  //     p.push();                       

  //     // Translate to center of canvas and rotate by angle
  //     p.translate(p.width/2, p.height/2);
  //     p.rotate(angle);

  //     // Set color based on angle and draw line along x-axis
  //     // p.stroke(angle+100, 100, 100);
  //     // p.strokeWeight(5);
  //     // p.line(0, 0, 150, 0);

  //     drawSlice(0,0,150,0.5,nSegments,p)

  //     // // Display the angle
  //     // p.strokeWeight(1);              
  //     // p.text(angle, 170, 0);

  //     // Restore coordinate system
  //     p.pop();                        
  // }

    // Draw the animated line
    // p.translate(p.width/2, p.height/2);
    // p.rotate(p.frameCount);
    // p.stroke(255);
    // p.strokeWeight(5);
    // p.line(0, 0, 150, 0);   
    
    // let data = Array.from({length: 20}, () => Math.floor(Math.random() * 20));
    // drawDataSlice(data,0,p);
    // data = Array.from({length: 20}, () => Math.floor(Math.random() * 20));
    // drawDataSlice(data,3,p);

  };
};

function drawDataSlice(data,r,n,p)
{
  let nSegments = data.length;
  let min = Math.min(... data);
  let max = Math.max(... data) * 1.2;
  let nSlices = 8;

  for (var i=0;i<nSegments;i+=1)
  {
      let angle = (i* (Math.PI*2)/(nSegments * nSlices)) + (n* (Math.PI*2)/nSlices);
      let v = data[i]/max;
      
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
    <div id="vue-canvas"></div>
</template>

<style scoped>
#vue-canvas {
  display: block;
  margin: 0 auto;
  padding: 0;
  width: 500px;
  height: 500px;
  border-radius: 20px;
  overflow: hidden;
}
</style>
