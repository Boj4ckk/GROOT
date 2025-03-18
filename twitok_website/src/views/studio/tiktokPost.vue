<script setup>
import { useTwitokStore } from '@/store/twitokStore';


const  TwitokStore = useTwitokStore()
const objet_editedClip = TwitokStore.editedClipsUrl
const editedClipUrls = objet_editedClip["processed_clip_url"]
console.log(TwitokStore.editedClipsUrl)

for (let clip in objet_editedClip["processed_clip_url"]) {
    console.log("clip sur lequel on boucle : ",clip)
}

// const dossier = '../../media/processed_clips'


</script>

<template>

yo t'es la pour poster du tiktok 

<ul>
    <li v-for="clip in objet_editedClip">
        <p>voici le clip sur lequel on boucle : {{ clip['processed_clip_url'] }}</p>
        <video :src="clip['processed_clip_url']" controls></video>
        <video src="../../media/processed_clips/782017dd-f29d-48ed-9913-95a28f04e7a0_processed.mp4"></video>
    </li>
</ul>
    
</template>