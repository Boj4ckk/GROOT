<script setup>
import axios from 'axios';
import { ref } from 'vue';
import apiClient from '@/api';
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import router from '@/router';
import { useTwitokStore } from '@/store/twitokStore';
import State_bar from '@/components/state_bar.vue';
import StudioHeader from '@/components/studioHeader.vue';
import { watch } from 'vue';


const twitokStore = useTwitokStore()

const streamer_name = ref("talmo")
const game = ref([])
const min_views = ref(0)
const max_views = ref(100)
// const min_duration = ref(0)
const duration = ref(60)
const startDate = ref("2024-01-01") // formater 
const endDate = ref("2025-01-01") // formater
const number_of_clips = ref(1) 
const chargement = ref(false)


const streamerInput = ref(""); // Pour la saisie
const streamerSuggestions = ref([]);
const streamerError = ref("");
const limitedStreamerSuggestions = computed(() => streamerSuggestions.value.slice(0, 10));



const gameInput = ref(""); // Pour la saisie
const gameError = ref(""); // Pour les messages d'erreur
const gameSuggestions = ref([]);
const limitedGameSuggestions = computed(() => gameSuggestions.value.slice(0, 10));





const getClips = async() => {
    chargement.value = true
    try {
        if (twitokStore.already_upload == 0) {
            console.log(number_of_clips.value)
            console.log("\naucun clip upload jusqu'ici. => On ajoute 1 au chiffre rentré par l'utilisateur\n")
            
           
        }
        else {
            console.log("\nDes clips ont deja été uploadé. => On ajoute 1 au nombre de clip rentré par l'utilisateur.\n")
         
        }
        const dataToSend = {
            
             streamer_name:streamer_name.value,
             game: game.value, min_views:min_views.value, 
             max_views:max_views.value,
             min_views:min_views.value,
             max_duration:duration.value,
             min_date_release:startDate.value,
             max_date_release:endDate.value,
             number_of_clips:number_of_clips.value,
        }
        console.log('Tentative de récupératon des clips [avant requete]')
        

        const response = await axios.post("/recup_infos_clips", dataToSend, {withCredentials: true})
        console.log("Tentative d'envoie des informations sur les clips a récupérer...")
        console.log("voici le streamer qu'on tente de recup les clips", dataToSend.streamer_name)
        try {
            const clipsUrls_returned = await axios.get("/send_clips_urls",{withCredentials: true})
            console.log("voici ce que nous a retourné l'api : ", clipsUrls_returned.data)
            if (Array.isArray(clipsUrls_returned.data.clipsUrls) && clipsUrls_returned.data.clipsUrls.length === 0){
                console.log("aucune vidéo trouvé pour le STREAMER", dataToSend.streamer_name)
                alert(`Aucun vidéo trouvé pour le streamer ${dataToSend.streamer_name} avec les informations que vous avez saisi. `)
                chargement.value = false
                router.replace('studio/filtrate')
                return
            }
            
            twitokStore.setclipsUrls_Returned(clipsUrls_returned.data)
            
            console.log("clipsReterned du STORE : ", twitokStore.clipsUrls_Returned)
        }
        catch(err){
            console.error('Impossible de récupérer les clips de neuilles', err)
            chargement.value = false
            router.push('/studio')
        }
        chargement.value = false
        router.push('/studio/clip_selection')
    }
    catch (error) {
        console.error('erreur lors de la récupération des clips...', error)
        alert("impossible de récuperer les clips")
        chargement.value = false

        // return jsonify({"error": "Clips not retrieved"})
    }
    // return jsonify({"message": "Clips retrieved successfully", "clips": data})
}

const onGameInputKeydown = (e) => {
  if (e.key === 'Enter' && gameInput.value.trim() !== '') {
    e.preventDefault();
    const val = gameInput.value.trim();
    if (
      gameSuggestions.value.includes(val) &&
      !game.value.includes(val)
    ) {
      if (game.value.length < 5) {
        game.value.push(val);
        gameError.value = "";
      } else {
        gameError.value = "Maximum 5 games allowed.";
      }
    } else if (!gameSuggestions.value.includes(val)) {
      gameError.value = "This game is not in the list.";
    }
    gameInput.value = '';
    gameSuggestions.value = [];
  }
};
const fetchStreamers = async (query) => {

  if (!query) {
    console.log("no")
    streamerSuggestions.value = [];
    return;
  }
  try {
    console.log("yes")
    const resp = await axios.get(`/search_streamers?q=${query}`);
    console.log(resp);
    streamerSuggestions.value = resp.data.streamers;
  } catch (e) {
    console.log("re")
    streamerSuggestions.value = [];
  }
};

watch(streamerInput, (newVal) => {
  fetchStreamers(newVal);
});




const fetchGames = async (query) => {
  if (!query) {
    gameSuggestions.value = [];
    return;
  }
  try {
    const resp = await axios.get(`/search_games?q=${query}`);
    console.log(resp.data.games);
    gameSuggestions.value = resp.data.games;
  } catch (e) {
    gameSuggestions.value = [];
  }
};

// Surveille les changements dans gameInput et fetch les suggestions de jeux
watch(gameInput, (newVal) => {
  fetchGames(newVal);
});







</script>

<template>, 
    <studioHeader/> 
    
    <div class=" px-2 pt-20 md:pt-5 "> <!-- body -->
        <div class=""> <!-- formulaire -->
            <form action="">

                <div class="flex flex-col justify-center items-center px-2">
                    <div class="w-80 md:w-[700px] font-inter font-light text-[15px] md:text-[20px] md:font-medium">Streamer's name</div>
                    <input
                        class="rounded-lg py-1 h-[30px] w-80 md:w-[700px] input-field border-1 border-black px-3 ml-3 font-inter text-[20px]"
                        type="text"
                        id="streamer_name"
                        name="streamer_name"
                        v-model="streamerInput"
                        @keydown="onStreamerInputKeydown"
                        list="streamer-list"
                        placeholder="talmo"
                        autocomplete="off"
                    >
                    <div v-if="streamerError" class="text-red-500 text-sm mt-1">{{ streamerError }}</div>
                    <datalist id="streamer-list">
                        <option v-for="s in limitedStreamerSuggestions" :key="s" :value="s">{{ s }}</option>
                    </datalist>
                </div>
                
                <div class=" flex flex-col justify-center items-center px-2 py-2">
                    <div  class="  w-80 md md:w-[700px] font-inter font-light text-[15px] md:text-[20px] md:font-medium ">Game</div>
                    <input class="rounded-lg py-1 h-[30px] w-80 md:w-[700px] input-field border-1 border-black px-3 ml-3 font-inter text-[20px]" type="text" id="game" name="game" list="game-list" v-model="gameInput" @keydown="onGameInputKeydown" placeholder="Fortnite">
                    <div v-if="gameError" class="text-red-500 text-sm mt-1">{{ gameError }}</div>
                    <datalist id="game-list">
                        <option v-for="g in limitedGameSuggestions" :key="g" :value="g">{{ g }}</option>
                   
                    </datalist>
                </div>

                <div v-if="game.length && !(game.length === 1 && game[0] === '')" class=" flex  px-2 pt-3  md:justify-center md:items-center ">
                    <div v-for="g in game" :key="g"
                    class="relative border-1 rounded-lg border-black md:w-[110px] h-[45px] font-inter font-medium flex justify-center items-center ml-4 bg-gray-200"
                    >
                    <span
                        class="truncate max-w-[90px] w-full flex justify-center items-center text-center"
                        style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; display:block;"
                    >{{ g }}</span>
                    <button
                        @click.prevent="game.splice(game.indexOf(g), 1)"
                        class="absolute -top-2 -right-2 bg-black text-white rounded-full w-6 h-6 flex items-center justify-center shadow hover:bg-red-700 transition-transform duration-150 hover:scale-105"
                        aria-label="Supprimer"
                        style="z-index:2;"
                    >×</button>
                    </div>

                  
                </div>
               
                <div class=" flex flex-col px-2 md:pt-3  md:justify-center md:items-center ">
                    <div class=" flex items-end px-1 md:w-[700px] md:font-medium md:text-[20px] font-inter">
                        <div class='font-inter'>Duration</div>
                        <div class='font-inter text-[12px] px-1'>in sec</div>
                    </div>
                    <div class="w-80 md:w-1/2 ml-2 relative ">
                        <!-- Valeur flottante -->
                        <div 
                        class="absolute -top-8 bg-black text-white px-2 py-1 rounded text-sm transform -translate-x-1/2 transition-all duration-200"
                        :style="{ left: `${(duration / 90) * 100}%` }"
                        >
                        {{ duration }}s
                        </div>
                        
                        <!-- Container du slider -->
                        <div class="relative w-full h-[20px] bg-white border-2 border-gray-300 rounded-full overflow-hidden">
                        <!-- Partie remplie en noir -->
                        <div 
                            class="absolute left-0 top-0 h-full bg-black transition-all duration-200"
                            :style="{ width: `${(duration / 90) * 100}%` }"
                        ></div>
                        
                        <!-- Input invisible par-dessus -->
                        <input 
                            type="range" 
                            v-model="duration"
                            min="0" 
                            max="90"
                            step="1"
                            class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        >
                        </div>
                        
                        <!-- Marqueurs de temps en bas -->
                        <div class="flex justify-between text-xs text-gray-600 mt-2 md:text-[15px] font-inter">
                        <span>0s</span>
                        <span>45s</span>
                        <span>90s</span>
                        </div>
                    </div>
                    
                </div>
                
                <div class=" flex flex-col px-3 md:w-full ">
                    <div class=" md:w-[730px] md:flex md:justify-center md:font-medium text-[20px] font-inter">View's</div>
                    <div class="px-3 flex  justify-between  w-4/5 items-center  md:justify-center md:items-center md:space-x-10">
                        <div class="flex flex-row justify-center items-center">
                             <div class=" font-inter font-light text-[15px] md:text-[15px] ">Min</div>
                             <input class="rounded-lg py-1 h-[27px] w-2/4 md:w-[93px] md:h-[35px] input-field border-1 border-black px-2 ml-1" type="number" id="views_min" name="views_min" min="0" v-model="min_views">
                        </div>
                       
                        <div class="flex flex-row justify-center items-center ">
                            <div class=" font-inter font-light text-[15px] md:text-[15px] ">Max</div>
                            <input class="rounded-lg py-1 h-[27px] w-2/4  md:w-[93px] md:h-[35px] input-field border-1 border-black px-2 ml-1" type="number" id="views_min" name="views_min" min="0" v-model="max_views">
                        </div>
                        
                    </div>
                        
                </div>
                

        <div class="px-3  md:flex flex-col md:items-center md:pt-5">
            <label class="font-inter   w-[700px] md:font-medium md:text-[20px] md:mb-1 md:justify-start md:flex">
                Release Date
            
            </label>
            
            <!-- Container unifié -->
            <div class="flex items-center border border-gray-300  md:w-1/2 md:px-2 ">
            <!-- Date de début -->
                    <div class="flex-1  py-2">
                        <label class="block text-xs text-gray-500 mb-1 md:text-[15px]">Start date</label>
                        <input 
                        type="date"
                        v-model="startDate"
                        class="w-5/6 border-1  outline-none text-sm"
                        >
                    </div>
                    
                    <!-- Séparateur -->
                    <div class="px-2 text-gray-400">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                    </div>
                    
                    <!-- Date de fin -->
                    <div class="flex-1 px-3 py-2">
                        <label class="block text-xs text-gray-500 mb-1 md:text-[15px]">End date</label>
                        <input 
                        type="date"
                        v-model="endDate"
                        :min="startDate"
                        class="w-full border-none outline-none text-sm"
                        >
                    </div>
            </div>
                    
        </div>
        <div class=" flex flex-col items-center pt-2 w-full ">
            <div class='pt-2 mr-10 flex justify-around md:justify-start md:px-5 md:w-1/2 '>
                <div class="flex items-center  md:text-[20px] md:font-medium ">
                    <div class="font-inter">Number of clips</div>
                    <div class="text-sm md:text-lg px-2 font-thin md:font-light">(max 10)</div>
                </div>
                <input class='border-1 border-black rounded-lg px-1 md:w-[80px] md:h-[30px]' type="number" min="1" max="10" id="number_of_clips" name="number_of_clips" v-model="number_of_clips" value="1">
            </div>
        </div>
               
                    
                    
                   
               
               <div class=" flex justify-center pt-5">
                
                    <input class="border-1 border-black px-4 rounded-sm md:w-[131px] md:h-[40px] md:text-[18px] md:font-medium" type="submit" value="Find" @click.prevent="getClips()">
                 
                    
                </div>
                
                
            </form>
            <div v-if="chargement">
                <br><br>
                <p v-if="chargement"> Vos videos sont en cours de téléchargement... </p>
            </div>
        </div>
    </div>
</template>
