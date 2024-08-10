<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'

</script>

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
