<script setup>
import { useTwitokStore } from '@/store/twitokStore';
import { ref } from 'vue';
import axios from 'axios';



const TwitokStore = useTwitokStore()
const objet_editedClip = TwitokStore.editedClipsUrl
const editedClipUrls = objet_editedClip["processed_clip_url"]
console.log(TwitokStore.editedClipsUrl)

const chargement = ref(false)

// const dossier = '../../media/processed_clips'

console.log("Objet édité : ", objet_editedClip);
const tableau_urls_clips = []
for (let index in objet_editedClip){
    console.log(objet_editedClip[index]["processed_clip_url"])
    tableau_urls_clips.push(objet_editedClip[index]["processed_clip_url"])
    console.log("etat actuel du tablau d'url : ", tableau_urls_clips)
}

const selected_video = ref(tableau_urls_clips[0])

const selected = (video) => {
    selected_video.value = video
}

const envoyer_infos_pour_tiktok = async(video, desfription="description par défaut") => {
    alert("Vous etes sur le point de poster une video sur tiktok, n\'appuyez sur aucun bouton de l'écran. \n Il vous suffira de répondre au Captcha dans quelques secondes, rien d'autre ne vous sera demandé. \n Merci d'avoir fait confiance à TwitokBot")
    chargement.value = true
    const data_to_send = {vue_chemin_video:video, description:desfription}
    console.log("Envoie des informations pour publication du clip [avant requete]")
    console.log("on va envoyer ce chemin : PROJET/GROOT/public/media/", video)
    try {
        const response = await axios.post("http://127.0.0.1:5000/publication", data_to_send)
        chargement.value = false
    }
    catch(err){
        console.log("Echec de la publication du clip lors de l'envoie à l'api", err)
        chargement.value = false
    }
} 

</script>

<template>

yo t'es la pour poster du tiktok 

<ul>
    <li v-for="clip, index in tableau_urls_clips">
        <p> clip_url : {{ clip }}</p>
        <video :src="clip" :key="index" controls @click="selected(clip)"></video>
    </li>
</ul>
    <br><hr>
    <p> video que t'es sur le point d'exporter sur tiktok : </p>
        <video :src="selected_video"></video>
        <input type="button" value="export" @click="envoyer_infos_pour_tiktok(selected_video, description)">
    <div v-if="chargement">
        <br>
        <h5> Publication de la video... Ne pas toucher à l'écran pendant toute la durée de la publication</h5>
    </div>

    
</template>