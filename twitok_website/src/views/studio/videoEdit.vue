<script setup>
import { useRoute } from 'vue-router';


const route = useRoute()
const videoId = route.params.videoId

</script>

<template>
    <edit/> 
    yo t'es dans le video edit de {{ videoId }}
    <video :src="videoId"> </video>
    
</template>

