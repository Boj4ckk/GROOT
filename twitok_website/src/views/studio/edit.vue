<script setup>

import { useTwitokStore } from '@/store/twitokStore';
import router from '@/router';

const TwitokStore = useTwitokStore() 

const json_clips = TwitokStore.clipsReturned

const clips = json_clips["clips"]

// const final_urls = []

// for (let clip in clips) {
//     const temp_clip = "../" + clips[clip]
//     final_urls.push(temp_clip)
//     console.log(temp_clip)
// }


console.log (clips) 
</script>

<template>
    yo t 'es dans edit 
    <br>
    voici les clips dipos pour toi : 
    <ul>
        <li v-for="clip in clips" :key="clip"> <video :src="clip" controls></video> </li>
    </ul>

</template>