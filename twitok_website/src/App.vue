<script setup>
// import accueil from './components/accueil.vue';
// import Connected from './components/connected.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <!-- <accueil/>
  <connected/>  -->
  <router-view/> 

  ptn de pb la c que y reconnait pas le authorizedConnection du store donc il peut pas validere l'autorisation et on peut pas accéder à '/connected'
</template>