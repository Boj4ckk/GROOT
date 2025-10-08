<script setup>
import { RouterView } from 'vue-router';
import navbar from './components/navbar.vue';
</script>

<template>
  <div class="content-under-navbar px-[15px] pt-10 md:!px-64 md:pt-40">
    <navbar class="fixed-navbar px-[15px] md:px-64" /> 
    <router-view class=""/> 

    <br><br><br><br><br>
  </div>
 

</template>