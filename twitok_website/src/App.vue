<script setup>
// import accueil from './components/accueil.vue';
// import Connected from './components/connected.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <router-link to="/"> Logo </router-link>
  <router-link to="/studio"> Studio </router-link>
  <router-link to="/help"> Help </router-link>
  <router-link to="/login"> Log in </router-link>
  <router-link to="/register"> Register </router-link>

  <router-view/> 

</template>