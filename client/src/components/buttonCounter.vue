<script setup>
import { ref } from 'vue'

const count = ref(0)
let cC = 0;
function bplus()
{
  cC = cC+1;
  count.value = cC;
}

</script>

<template>
  <button @click="bplus">You clicked me {{ count }} times.</button>
</template>


