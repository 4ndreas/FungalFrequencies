<script setup>
import { onMounted, ref } from 'vue';

const min = ref(0)
const max = ref(1)
const wordCount = ref(2)
const lastWord = ref(3)

function update()
{
    var url = "./api/stats";
    fetch(url)
      .then(res => res.json())
      .then(out => {
        min.value = out.min;
        max.value = out.max;
        wordCount.value = out.wordCount;
        lastWord.value = out.spikeWord;
      })
      .catch(err => console.log(err));
}

onMounted(() => {
  setInterval(update, 5000);
});

</script>

<template>
  <div class="stats">
    Min: {{ min }} mV<br>
    Max: {{ max }} mV<br>
    Spikes: {{ wordCount }} events<br>
    Spike: {{ lastWord }}<br>
  </div>
</template>

<style scoped>
  .stats {
    /* background-color: blue; */
    /* width: 320px;
    height: 320px; */
    /* padding: 100px 100px; */
    position: absolute;
    top: 100px;
    left: 100px;    
    color: white;
    font-family: Helvetica;
    font-size: 20px;
    /* text-align: center; */
  }
</style>