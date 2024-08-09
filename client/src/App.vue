<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'

// import {
//   Chart as ChartJS,
//   RadialLinearScale,
//   ArcElement,
//   Tooltip,
//   Legend,
//   ChartData
// } from 'chart.js' 
// import { PolarArea } from 'vue-chartjs'

</script>


<!-- <script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import Vizzu from 'vizzu'

</script>

<template>
  <header>
    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>
  </header>
</template>

-->
<style >
.container div { margin: 0; }

.home {
    position: absolute;
    top: 0px;
    left: 0px;
}

body {
  margin-top:0;
  margin-right:0;
  margin-bottom:0;
  margin-left:0;
  background-color: hsl(0, 0%, 0%);
  }

  div {
  top: 0;
  left: 0;
  margin: 0 0 0 0;
  padding: 0 0 0 0;
}

* {
  top: 0;
  left: 0;
  margin: 0 0 0 0 ;
  padding: 0 0 0 0 ;
}
</style>
