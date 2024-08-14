<script setup>
import { onMounted, ref } from 'vue';

const start = Date.now();
console.log('starting timer...');

const cboard = ref(0)

function update()
{
    cboard.value = Math.floor(Math.random() * (15 - 0 + 1)) + 0;
}

onMounted(() => {
  update();
  setInterval(update, 60000);
});

</script>


<script lang="ts">

</script>

<template>
    <div id="single" class="single" > 
            <div class = "vue-canvas_center" id = "vue-canvas_ce"></div>
            <!-- <p5chart :board="0" :buffered="true" :time="-3000" :stepSize="2" :spiker="true" :radius="350" :cWidth="1200" :slicesToShow="1" canvas="vue-canvas_ce" />  -->
            <p5chart :board=cboard :buffered="true" :time="-90" canvas="unten4"  /> 
    </div>
</template>

<style scoped>
body {
  margin-top:0;
  margin-right:0;
  margin-bottom:0;
  margin-left:0;
  }

.single {
    position: absolute;
    top: 0px;
    left: 0px;
}

.canvas {
  filter: blur(1.0px);
}

.vue-canvas_center {
    position: absolute;
    top: 360px;
    left: 360px;
}

#centerDisplay {
    background: #000;
    width: 1280px;
    height: 1280px;
    position: absolute;
    top: 320px;
    left: 320px;
}

</style>
