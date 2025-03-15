<script setup>
import { useRoute } from 'vue-router';
import edit from './edit.vue';

const route = useRoute()
const videoId = route.params.videoId

</script>

<template>
    <edit/> 
    yo t'es dans le video edit de {{ videoId }}
    <video :src="videoId" controls> </video>
    
</template>

