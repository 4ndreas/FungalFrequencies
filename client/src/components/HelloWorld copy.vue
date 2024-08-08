<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
  // d0: number,
	// d1: number,
	// d2: number,
	// d3: number,
	// d4: number,
	// d5: number,
	// d6: number,
	// d7: number,
})



</script>

<script type="module">
import Vizzu from 'vizzu'
  // 'https://cdn.jsdelivr.net/npm/vizzu@0.3.1/dist/vizzu.min.js';

  let vizzuData = {
    series : [{
            name: 'dx',
            type: 'measure',
            values: [0,1,2,4,5 ]
          }, {
            name: 'dy',
            type: 'measure',
            values: [0,1,1,1,1 ]
          }]
};
//   let vizzuData = {
//     series : [{
//             name: 'x',
//             values: [0,1,2,4,5 ]
//           }, {
//             name: 'y',
//             values: [[0,1,1,1,1 ],
//                     [0,1,1,1,1 ]]
//           }]
// };


// let vizzuData = {
//   records : [
//     [0,1 ],
//     [1,1 ],
//     [2,1 ],
//     [2,1 ],
//     [2,1 ],
//     [2,1 ],
//     [2,1 ]
//           ]
// };

  let chart = new Vizzu('myVizzu')
  getData();
  
  let data;
  let d0 = 0;
	let d1 = 0;
	let d2 = 0;
	let d3 = 0;
	let d4 = 0;
	let d5 = 0;
	let d6 = 0;
	let d7 = 0;


function setGraph(d)
{
  
  vizzuData.series[1].values = d;
  vizzuData.series[0].values = Array.from(Array(vizzuData.series[1].values.length).keys());

  chart.animate({
    data: vizzuData, 
    config: {

      channels: {
            x: { set: ["dx"],
                range: {
                  min: -10,
                  max: 10
                }
            },
            y: { set: ["dy"],
                range: {
                      min: -10,
                      max: 10
                    }
             },
          },
        //   },      
        "geometry": "line",
        // "coordSystem": "polar"
      }
    })

  console.log(vizzuData);
  console.log(chart);
}

  function getData() {
	fetch("./data")
		.then(res => res.json())
		.then(
		(out) =>{
			data = out;

			d0 = data[0][0];
			d1 = data[1][0];
			d2 = data[2][0];
			d3 = data[3][0];
			d4 = data[4][0];
			d5 = data[5][0];
			d6 = data[6][0];
			d7 = data[7][0];

      console.log(data);
      setGraph(data[0]);


		})
		.catch(err => console.log(err));
	}

  function logData() {
    console.log(d0);
    console.log(d1);
    console.log(d2);
    console.log(d3);
    console.log(d4);
    console.log(d5);
    console.log(d6);
    console.log(d7);
  }
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      You’ve successfully created a project with
    </h3>

    <!-- <div id="myVizzu" style="width:800px; height:480px;"></div> -->
    <PolarArea :data="data" :options="options" />

    <button @click="getData">get Data</button>
    <button @click="logData">log Data</button>
    
    <h1>Data 0 is {{d0}}!</h1>
    <h1>Data 1 is {{d1}}!</h1>
    <h1>Data 2 is {{d2}}!</h1>
    <h1>Data 3 is {{d3}}!</h1>
    <h1>Data 4 is {{d4}}!</h1>
    <h1>Data 5 is {{d5}}!</h1>
    <h1>Data 6 is {{d6}}!</h1>
    <h1>Data 7 is {{d7}}!</h1>


  </div>
</template>


<style scoped>

</style>
