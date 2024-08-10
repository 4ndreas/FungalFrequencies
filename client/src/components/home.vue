<script setup lang="ts">
import p5chart from './p5chart.vue';
import { ref, onMounted } from 'vue'
// const props = defineProps(['sampletime'])

// import p5chart2 from './p5chart2.vue';
// import buttonCounter from './buttonCounter.vue';

// const sampletime = ref(0);
// sampletime.value = -120;
// onMounted(() => {
//     props.sampletime = -120;
//   });
// let sampletime  = -120;// console.log("Sampletime: " + props.sampletime )
const sampletime = -120;

</script>


<script lang="ts">

</script>

<template>
    <div id="home" class="home" > 

    <table style="width: 1920px" cellspacing="0" cellpadding="0">
        <tr style="height:320px">
            <th>
                <td style="width:320px" >
                    <!-- leer -->
                </td>
                <td style="width:320px">
                    <!-- Oben board 4 -->
                    <div id = "vue-canvas_11"></div>
                    <p5chart board="5" time="-90" device="FungalFrequencies_7483aff9d108" canvas="vue-canvas_11"/>  
                </td>
                <td style="width:320px">
                    <!-- Oben board 3 -->
                    <div id = "vue-canvas_12"></div>
                    <p5chart board="4" time="-90" device="FungalFrequencies_7483aff9d108" canvas="vue-canvas_12"/>  
                </td>
                <td style="width:320px">
                    <!-- Oben board 2 -->
                    <div id = "vue-canvas_13"></div>
                    <p5chart board="3" time="-90" device="FungalFrequencies_7483aff9d108" canvas="vue-canvas_13"/>  
                </td>                                    
                <td style="width:320px">
                    <!-- Oben board 1 -->
                    <div id = "vue-canvas_14"></div>
                    <p5chart board="2" time="-90" device="FungalFrequencies_7483aff9d108" canvas="vue-canvas_14" />   
                </td>
                <td style="width:320px">
                    <!-- leer -->
                </td>     
            </th>        
        </tr>
        <tr style="height:320px">
            <th>
                <td style="width:320px">
                    <!-- Links board 1 -->
                    <div id = "vue-canvas_21"></div>
                    <p5chart board="2" time="-90" device="FungalFrequencies_944e71b3a3a0" canvas="vue-canvas_21" />                       
                </td>
                <td style="width:1280px">

                </td>
                <td style="width:320px">
                    <!-- Rechts board 4 -->
                    <div id = "vue-canvas_22"></div>
                    <p5chart board="5" time="-90" device="FungalFrequencies_50f776b3a3a0" canvas="vue-canvas_22" />       
                </td>  
            </th>                                           
        </tr>         
        <tr style="height:320px">
            <th>
                <td style="width:320px">
                    <!-- Links board 2 -->
                    <div id = "vue-canvas_31"></div>
                    <p5chart board="3" time="-90" device="FungalFrequencies_944e71b3a3a0" canvas="vue-canvas_31" />                   
                </td>
                <td style="width:1280px">

                </td>
                <td style="width:320px">
                    <!-- Rechts board 3 -->
                    <div id = "vue-canvas_32"></div>
                    <p5chart board="4" time="-90" device="FungalFrequencies_50f776b3a3a0" canvas="vue-canvas_32" />                      
                </td>    
            </th>                                         
        </tr> 
        <tr style="height:320px">
            <th>
                <td style="width:320px">
                    <!-- Links board 3 -->
                    <div id = "vue-canvas_41"></div>
                    <p5chart board="4" time="-90" device="FungalFrequencies_944e71b3a3a0" canvas="vue-canvas_41" />  
                </td>
                <td style="width:1280px">
                </td>
                <td style="width:320px">
                    <!-- Rechts board 2 -->
                    <div id = "vue-canvas_42"></div>
                    <p5chart board="3" time="-90" device="FungalFrequencies_50f776b3a3a0" canvas="vue-canvas_42" />       
                </td>   
            </th>                                         
        </tr>
        <tr style="height:320px">
            <th>
                <td style="width:320px">
                    <!-- Links board 4 -->
                    <div id = "vue-canvas_51"></div>
                    <p5chart board="5" time="-90" device="FungalFrequencies_944e71b3a3a0" canvas="vue-canvas_51" />  
                </td>
                <td style="width:1280px">

                </td>
                <td style="width:320px">
                    <!-- Rechts board 1 -->
                    <div id = "vue-canvas_52"></div>
                    <p5chart board="2" time="-90" device="FungalFrequencies_50f776b3a3a0" canvas="vue-canvas_52" />  
                </td>
            </th>                                            
        </tr>        
        <tr style="height:320px">
            <th>
                <td style="width:320px">
                    <!-- leer -->
                </td>
                <td style="width:320px">
                    <!-- Unten board 4 -->
                    <div id = "vue-canvas_61"></div>
                    <p5chart board="5" time="-90" device="FungalFrequencies_10d1aff9d108" canvas="vue-canvas_61"  />                 
                </td>
                <td style="width:320px">
                    <!-- Unten board 3 -->
                    <div id = "vue-canvas_62"></div>
                    <p5chart board="4" time="-90" device="FungalFrequencies_10d1aff9d108" canvas="vue-canvas_62"  />   
                </td>
                <td style="width:320px">
                    <!-- Unten board 2 -->
                    <div id = "vue-canvas_63"></div>
                    <p5chart board="3" time="-90" device="FungalFrequencies_10d1aff9d108" canvas="vue-canvas_63"  />  
                </td>                                    
                <td style="width:320px">
                    <!-- Unten board 1 -->
                    <div id = "vue-canvas_64"></div>
                    <p5chart board="2" time="-90" device="FungalFrequencies_10d1aff9d108" canvas="vue-canvas_64"  />  
                </td>
                <td style="width:320px">

                </td>  
            </th>           
        </tr>                   
    </table>
    </div>
</template>

<style scoped>
body {
  margin-top:0;
  margin-right:0;
  margin-bottom:0;
  margin-left:0;
  }
.home {
    position: absolute;
    top: 0px;
    left: 0px;
}
table, tr, th, td {
  /* border: 1px solid rgb(255, 255, 255); */
  border: none;
}

* {
  padding: 0;
  margin: 0;
}
div {
  top: 0;
  left: 0;
  margin: 0 0;
  padding: 0 0;
}

</style>
