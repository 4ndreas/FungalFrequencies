<script setup lang="ts">
import HelloWorld  from './HelloWorld.vue';
import p5chart from './p5chart.vue';
</script>


<script>

</script>


<template>
    <div id="home"> 
        <!-- <HelloWorld /> -->
        <p5chart :board="2" time="-10" device="FungalFrequencies_7483aff9d108" />
        <p5chart :board="3" time="-10" device="FungalFrequencies_7483aff9d108" />
        <p5chart :board="4" time="-10" device="FungalFrequencies_7483aff9d108" />
        <p5chart :board="5" time="-10" device="FungalFrequencies_7483aff9d108" />
    </div>
</template>

<style scoped>

</style>
