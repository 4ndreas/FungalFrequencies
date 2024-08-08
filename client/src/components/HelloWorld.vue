<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
})



</script>

<script type="module">
import Vizzu from 'vizzu'
  // 'https://cdn.jsdelivr.net/npm/vizzu@0.3.1/dist/vizzu.min.js';


  let data = {
    dimensions: [ 
        { name: 'Genres', values: [ 'Pop', 'Rock', 'Jazz', 'Metal' ] },
        { name: 'Types', values: [ 'Hard', 'Smooth', 'Experimental' ] }
    ],
    measures: [
        {
            name: 'Popularity',
            values: [
                [ 114, 96, 78, 52 ],
                [ 56, 36, 174, 121 ],
                [ 127, 83, 94, 58 ]
            ]
        }
    ]
};

  let chart = new Vizzu('myVizzu')
  // let data = [31,265,1321,1613,1631];
  chart.animate({
    data: data, 
    config: {
        channels: {
                x: { set: null },
                y: { set: ['Genres','Popularity'] }
        }
    }
})


// chart.initializing.then(
//   chart => chart.animate({ /* ... */ }) 
// )

</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      You’ve successfully created a project with
    </h3>

    <div id="myVizzu" style="width:800px; height:480px;"></div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
