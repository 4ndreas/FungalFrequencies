<script setup lang="ts">
defineProps({
  msg: {
    type: String,
    required: false
  }
})

  onMounted(() => {
    

  setInterval(() => {
    getData();
    data.value = influxData();
    console.log("update Data");
  }, 10000)
})

</script>


<script type="module"  lang="ts">
import { ref, onMounted } from 'vue'
import {
  Chart as ChartJS,
  RadialLinearScale,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  ChartData
} from 'chart.js'

// import type { ChartData } from 'chart.js'
import * as chartConfig from './chartConfig.js'
import { Bar } from 'vue-chartjs'
import { PolarArea } from 'vue-chartjs'


let rawData = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]];

const influxData= () => ({
  labels: [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7'
  ],
  datasets: [
    {
      label: 't 0',
      backgroundColor: 'rgba(179,181,198,0.2)',
      pointBackgroundColor: 'rgba(179,181,198,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(179,181,198,1)',
      data: getChannelData(0)
    },
    {
      label: 't -1',
      backgroundColor: 'rgba(255,99,132,0.2)',
      pointBackgroundColor: 'rgba(255,99,132,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(255,99,132,1)',
      data: getChannelData(1)
    }
  ]
})

ChartJS.register(RadialLinearScale, ArcElement, Tooltip);
// ChartJS.register(RadialLinearScale, ArcElement, Tooltip, Legend);
const data = ref<ChartData<'polarArea'>>({
  datasets: []
});
  

function getChannelData(time)
{
  return([rawData[0][time],
          rawData[1][time],
          rawData[2][time],
          rawData[3][time],
          rawData[4][time],
          rawData[5][time],
          rawData[6][time],
          rawData[7][time]]);
}

  function getData() {
	fetch("./data")
		.then(res => res.json())
		.then(
		(out) =>{
			rawData = out;
      console.log(rawData);
      data.value = influxData();
		})
		.catch(err => console.log(err));
	}

  function logData() {

    data.value = influxData()
    console.log(getChannelData(0));
    console.log(getChannelData(1));
  }


</script>

<template>
  <div class="chart">

    
    <div> 
      <PolarArea :data="data" :options="chartConfig.options" />
    </div>

    <!-- <button @click="getData">get Data</button>
    <button @click="logData">update Data</button> -->
    
    
  </div>
</template>


<style scoped>
.chart{
  width: 100%;
  /* height: 1000; */

}
</style>
