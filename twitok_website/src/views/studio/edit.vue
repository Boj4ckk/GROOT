<script setup>

import { useTwitokStore } from '@/store/twitokStore';
import router from '@/router';
import axios from 'axios';
import { ref } from 'vue';

const TwitokStore = useTwitokStore() 

const objet_clipsUrls = TwitokStore.clipsUrls_Returned
console.log("voici les urls des clips : ", objet_clipsUrls)
const clipsUrls = objet_clipsUrls["clipsUrls"]
console.log(clipsUrls)

const clips = ref([])

const getClips = async () => {
    try {
        for (let url of clipsUrls) {
            // const url = objet_url[0]
            console.log("envoi de la requete pour aller chercher la vidéo, nom vidéo : ", url)
            clips.value.push(`http://127.0.0.1:5000/clips/${url}`)
            console.log("etat du dossier de vidéos : ", clips)
        }
    }
    catch (error) {
        console.error("erreur lorsqu'on a été cherché la vidéo finale", error)
    }
    return clips
}

getClips() 

const goToVideoId = async(videoId) => {
    console.log("redirection vers videoId : ", videoId)
    await router.push({
        name:'videoEdit', 
        params:{videoId:videoId},
    })
    location.reload()
}

</script>

<template>
    yo t 'es dans edit 
    <br>
    voici les clips dipos pour toi : 
    <ul>
        <li v-for="clip in clips" :key="clip">
            <button @click="goToVideoId(clip)">
                <video :src="clip" controls></video>
            </button>
        </li>
    </ul>
</template>