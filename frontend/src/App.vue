<script setup>
import { RouterView } from 'vue-router';
import navbar from './components/navbar.vue';


</script>

<template>
  <div class="px-2 md:px-54 pt-40 md:pt-72">
    <navbar /> 
    <router-view/> 

    <br><br><br><br><br>
  </div>
 

</template>