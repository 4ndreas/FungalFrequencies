<script setup lang="ts">
import p5chart from './p5chart.vue';
import timerMS from './timerMS.vue';
import stats from './stats.vue';
import { ref, onMounted } from 'vue'
// const props = defineProps(['sampletime'])

// import p5chart2 from './p5chart2.vue';
// import buttonCounter from './buttonCounter.vue';

// const sampletime = ref(0);
// sampletime.value = -120;
// onMounted(() => {
//     props.sampletime = -120;
//   });
// let sampletime  = -120;// console.log("Sampletime: " + props.sampletime )
const sampletime = -120;


</script>


<script lang="ts">

</script>

<template>
    <div id="home" class="home" > 
        <div class="funghiGraph" id="oben0">

        </div>

        <div class="funghiGraph" id="oben1"></div>
        <p5chart :board="2" :buffered="true" :time="-90" canvas="oben1"/>  
        <div class="funghiGraph" id="oben2"></div>
        <p5chart :board="1" :buffered="true" :time="-90" canvas="oben2"/>  
        <div class="funghiGraph" id="oben3"></div>
        <p5chart :board="1" :buffered="true" :time="-90" canvas="oben3"/>  
        <div class="funghiGraph" id="oben4"></div>
        <p5chart :board="0" :buffered="true" :time="-90" canvas="oben4" />  

        <div class="funghiGraph" id="oben5">
            <timerMS/>
        </div>

        <div class="funghiGraph" id="links1"></div>
        <p5chart :board="4" :buffered="true" :time="-90" canvas="links1" />     
        <div class="funghiGraph" id="links2"></div>
        <p5chart :board="5" :buffered="true" :time="-90"  canvas="links2" /> 
        <div class="funghiGraph" id="links3"></div>
        <p5chart :board="6" :buffered="true" :time="-90" canvas="links3" />  
        <div class="funghiGraph" id="links4"></div>
        <p5chart :board="7" :buffered="true" :time="-90" canvas="links4" />      

        <div class="funghiGraph" id="rechts1"></div>
        <p5chart :board="15" :buffered="true" :time="-90" canvas="rechts1" />      
        <div class="funghiGraph" id="rechts2"></div>
        <p5chart :board="14" :buffered="true" :time="-90" canvas="rechts2" />
        <div class="funghiGraph" id="rechts3"></div>
        <p5chart :board="13" :buffered="true" :time="-90" canvas="rechts3" />       
        <div class="funghiGraph" id="rechts4"></div> 
        <p5chart :board="12" :buffered="true" :time="-90" canvas="rechts4" />     

        <div id="centerDisplay"></div>

        <div class="ecke" id="unten0"></div>
        <div class="funghiGraph" id="unten1"></div>
        <p5chart :board="8" :buffered="true" :time="-90" canvas="unten1"  />  
        <div class="funghiGraph" id="unten2"></div>
        <p5chart :board="9" :buffered="true" :time="-90" canvas="unten2"  />   
        <div class="funghiGraph" id="unten3"></div>
        <p5chart :board="10" :buffered="true" :time="-90" canvas="unten3"  />  
        <div class="funghiGraph" id="unten4"></div>
        <p5chart :board="11" :buffered="true" :time="-90" canvas="unten4"  />  
        <div class="ecke" id="unten5">
            <stats/>
        </div>        
        <div>
            <div class = "vue-canvas_center" id = "vue-canvas_ce"></div>
            <p5chart :board="0" :buffered="true" :time="-3000" :stepSize="2" :spiker="true" :radius="350" :cWidth="1200" :slicesToShow="1" canvas="vue-canvas_ce" /> 
        </div>

    </div>
</template>

<style scoped>
body {
  margin-top:0;
  margin-right:0;
  margin-bottom:0;
  margin-left:0;
  }
.home {
    position: absolute;
    top: 0px;
    left: 0px;
}

.vue-canvas_center {
    position: absolute;
    top: 360px;
    left: 360px;
}

table, tr, th, td {
  /* border: 1px solid rgb(255, 255, 255); */
  border: none;
}

* {
  padding: 0;
  margin: 0;
}
div {
  top: 0;
  left: 0;
  margin: 0 0;
  padding: 0 0;
}

.canvas {
  filter: blur(1.0px);
}

#oben0 {
    background: #000;
    width: 320px;
    height: 320px;
}

#oben1 {
    position: absolute;
    top: 0;
    left: 320px;
    width: 320px;
    height: 320px;
}

#oben2 {
    position: absolute;
    top: 0;
    left: 640px;
    width: 320px;
    height: 320px;
}

#oben3 {
    position: absolute;
    top: 0;
    left: 960px;
    width: 320px;
    height: 320px;
}

#oben4 {
    position: absolute;
    top: 0;
    left: 1280px;
    width: 320px;
    height: 320px;
}

#oben5 {
    background: #000;
    width: 320px;
    height: 320px;
    position: absolute;
    top: 0;
    left: 1600px;
 }

#links1 {
    position: absolute;
    top: 320px;
    left: 0px;
    width: 320px;
    height: 320px;
}
    
#links2 {
    position: absolute;
    top: 640px;
    left: 0px;
    width: 320px;
    height: 320px;
}

#links3 {
    position: absolute;
    top: 960px;
    left: 0px;
    width: 320px;
    height: 320px;
}

#links4 {
    position: absolute;
    top: 1280px;
    left: 0px;
    width: 320px;
    height: 320px;
}

#rechts1 {
    position: absolute;
    top: 320px;
    left: 1600px;
    width: 320px;
    height: 320px;
}
    
#rechts2 {
    position: absolute;
    top: 640px;
    left: 1600px;
    width: 320px;
    height: 320px;
}

#rechts3 {
    position: absolute;
    top: 960px;
    left: 1600px;
    width: 320px;
    height: 320px;
}

#rechts4 {
    position: absolute;
    top: 1280px;
    left: 1600px;
    width: 320px;
    height: 320px;
} 

#centerDisplay {
    background: #000;
    width: 1280px;
    height: 1280px;
    position: absolute;
    top: 320px;
    left: 320px;
}

#unten0 {
    background: #000;
    width: 320px;
    height: 320px;
    position: absolute;
    top: 1600px;
    left: 0px;
}

#unten1 {
    position: absolute;
    top: 1600px;
    left: 320px;
    width: 320px;
    height: 320px;
}

#unten2 {
    position: absolute;
    top: 1600px;
    left: 640px;
    width: 320px;
    height: 320px;
}

#unten3 {
    position: absolute;
    top: 1600px;
    left: 960px;
    width: 320px;
    height: 320px;
}

#unten4 {
    position: absolute;
    top: 1600px;
    left: 1280px;
    width: 320px;
    height: 320px;
}

#unten5 {
    background: #000;
    width: 320px;
    height: 320px;
    position: absolute;
    top: 1600px;
    left: 1600px;
}
</style>
