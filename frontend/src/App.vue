<script setup>
import { RouterView } from 'vue-router';
import navbar from './components/navbar.vue';


</script>

<template>
  <div class="px-[15px] md:!px-64 pt-40 md:pt-72 ">
    <navbar class=" px-[15px] md:px-64" /> 
    <router-view class=""/> 

    <br><br><br><br><br>
  </div>
 

</template>