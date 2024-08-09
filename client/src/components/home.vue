<script setup lang="ts">
import p5chart from './p5chart.vue';
// import p5chart2 from './p5chart2.vue';
</script>

<script>
</script>

<template>
    <div id="home"> 
        <!-- <HelloWorld /> -->
        <!-- <div id = "vue-canvas_1"></div> -->
        <!-- <p5chart board="3" time="-60" device="FungalFrequencies_7483aff9d108" canvas="vue-canvas_1" id="p5chart_1" /> -->
        <div>
            <div id = "vue-canvas_2"></div>
            <!-- <p5chart board="2" time="-60" device="FungalFrequencies_7483aff9d108" canvas="vue-canvas_2" id="p5chart_2" /> -->
        </div>
        <div>
            <div id = "vue-canvas_3"></div>
            <p5chart id="p5chart_3" board="4" time="-20" device="FungalFrequencies_50f776b3a3a0" canvas="vue-canvas_2"  />
        </div>
    </div>
</template>

<style scoped>

</style>
