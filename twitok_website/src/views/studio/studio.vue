<script setup>
import axios from 'axios';
import { ref } from 'vue';
import apiClient from '@/api';
import { useRouter } from 'vue-router';
import router from '@/router';
import { useTwitokStore } from '@/store/twitokStore';
import State_bar from '@/components/state_bar.vue';


const twitokStore = useTwitokStore()

const streamer_name = ref("talmo")
const game = ref([""])
const min_views = ref(0)
const max_views = ref(1000000)
// const min_duration = ref(0)
const max_duration = ref(30)
const min_date_release = ref("2024-01-01") // formater 
const max_date_release = ref("2025-01-01") // formater
const number_of_clips = ref(1) 
const chargement = ref(false)

const getClips = async() => {
    chargement.value = true
    try {
        number_of_clips.value +=1
        const dataToSend = {streamer_name:streamer_name.value, game: game.value, min_views:min_views.value, max_views:max_views.value, min_views:min_views.value, max_duration:max_duration.value, min_date_release:min_date_release.value, max_date_release:max_date_release.value, number_of_clips:number_of_clips.value}
        console.log('Tentative de récupératon des clips [avant requete]')
        

        const response = await axios.post("http://127.0.0.1:5000/recup_infos_clips", dataToSend)
        console.log("Tentative d'envoie des informations sur les clips a récupérer...")
        console.log("voici le streamer qu'on tente de recup les clips", dataToSend.streamer_name)
        try {
            const clipsUrls_returned = await axios.get("http://127.0.0.1:5000/send_clipsUrls")
            console.log("voici ce que nous a retourné l'api : ", clipsUrls_returned.data)
            if (Array.isArray(clipsUrls_returned.data.clipsUrls) && clipsUrls_returned.data.clipsUrls.length === 0){
                console.log("aucune vidéo trouvé pour le STREAMER", dataToSend.streamer_name)
                alert(`Aucun vidéo trouvé pour le streamer ${dataToSend.streamer_name} avec les informations que vous avez saisi. `)
                chargement.value = false
                router.push('/studio')
                return
            }
            twitokStore.setclipsUrls_Returned(clipsUrls_returned.data)
            console.log("clipsReterned du STORE : ", twitokStore.clipsUrls_Returned)
        }
        catch(err){
            console.error('Impossible de récupérer les clips de neuilles', err)
            chargement.value = false
            router.push('studio')
        }
        chargement.value = false
        router.push('/studio/filtrate')
    }
    catch (error) {
        console.error('erreur lors de la récupération des clips...', error)
        alert("impossible de récuperer les clips")
        chargement.value = false

        // return jsonify({"error": "Clips not retrieved"})
    }
    // return jsonify({"message": "Clips retrieved successfully", "clips": data})
}


</script>

<template>, 
    <State_bar/> 
    
    <div> <!-- body -->
        <div> <!-- formulaire -->
            <form action="">
                <label for="streamer_name">Streamer's name</label>
                <input type="text" id="streamer_name" name="streamer_name" v-model="streamer_name">
                <label for="game">Game</label>
                <input type="text" id="game" name="game" list="game-list" v-model="game">
                <datalist id="game-list"></datalist>
                <label for="duration">Duration <span>in sec</span></label>
                <input type="range" id="duration" name="duration" min="20" max="90" step="10" list="tickmarks" v-model="max_duration">
                <datalist id="tickmarks">
                    <option value="35"></option>
                    <option value="50"></option>
                    <option value="65"></option>
                    <option value="90"></option>        
                </datalist>
                <label for="views">Views</label>
                <div>
                    <label for="views_min">Min</label>
                    <input type="number" id="views_min" name="views_min" min="0" v-model="min_views">
                </div>
                <label for="min_date_release">Min date of release</label>
                <input type="date" id="min_date_release" name="min_date_release" v-model="min_date_release">
                <label for="max_date_release">Max date of release</label>
                <input type="date" id="max_date_release" name="max_date_release" v-model="max_date_release">
                <label for="number_clips">Nb of clips (max 10)</label>
                <input type="number" min="1" max="10" id="number_of_clips" name="number_of_clips" v-model="number_of_clips" value="1">
                
                
                <input type="submit" value="Find" @click.prevent="getClips()">
            </form>
            <div v-if="chargement">
                <br><br>
                <p v-if="chargement"> Vos videos sont en cours de téléchargement... </p>
            </div>
        </div>
    </div>
</template>
