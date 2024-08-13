<script setup>
import { onMounted, ref } from 'vue';

const start = Date.now();
console.log('starting timer...');

const millis = ref(0)

function update()
{
  millis.value = Date.now() - start;
}

onMounted(() => {
  setInterval(update, 10);
});

</script>

<template>
  <div>Online: {{ millis }} ms</div>
</template>

<style scoped>
  div {
    /* background-color: blue; */
    color: white;
  }
</style>