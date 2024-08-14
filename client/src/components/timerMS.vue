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
  setInterval(update, 50);
});

</script>

<template>
  <div>
    <div class="box">Online: {{ millis }} ms</div>
    </div>
</template>

<style scoped>
  div {
    position: absolute;
    top: 0;
    left: 0;
    width: 320px;
    height: 320px;
  }
  .box{
    transform-origin: 250px 0px;
    transform: rotate(-90deg);
    display: flex;
    width: 70%;
    color: white;
    font-family: Helvetica;
    text-align: end;
    font-size: 20px;
}

</style>