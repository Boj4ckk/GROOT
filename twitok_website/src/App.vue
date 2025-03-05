<script setup>
// import accueil from './components/accueil.vue';
// import Connected from './components/connected.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <router-view/> 


</template>

<!-- TODO : 
    - fonction de logout 
    - optimiser la connexion a la bdd car la dès qu'on fait une requete on se reconnecte
    - régler le probleme du before each pour quand on tape connected dans l'url qui est deja connected et que ca nous redirige vers connection 
      
-->

