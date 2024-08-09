<script setup lang="ts">
import HelloWorld  from './HelloWorld.vue';
import p5chart from './p5chart.vue';
// import p5chart2 from './p5chart2.vue';
</script>


<script>

</script>


<template>
    <div id="home"> 
        <!-- <HelloWorld /> -->
        <div id = "vue-canvas_1"></div>
        <p5chart id ="b1" key="b1" :board="2" time="-10" device="FungalFrequencies_7483aff9d108" canvas="vue-canvas_1"/>
        <div id = "vue-canvas_2"></div>
        <p5chart id ="b2" key="b2" :board="3" time="-10" device="FungalFrequencies_7483aff9d108" canvas="vue-canvas_2"/>
        <!-- <p5chart :board="4" time="-10" device="FungalFrequencies_7483aff9d108" />
        <p5chart :board="5" time="-10" device="FungalFrequencies_7483aff9d108" /> -->
    </div>
</template>

<style scoped>

</style>
