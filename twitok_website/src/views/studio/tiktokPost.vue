<script setup>
import { useTwitokStore } from '@/store/twitokStore';


const  TwitokStore = useTwitokStore()
const objet_editedClip = TwitokStore.editedClipsUrl
const editedClipUrls = objet_editedClip["processed_clip_url"]
console.log(TwitokStore.editedClipsUrl)



</script>

<template>

<ul>
    <li v-for="clip in editedClipUrls">
        <video :src="clip" controls></video>
    </li>
</ul>
    
</template>