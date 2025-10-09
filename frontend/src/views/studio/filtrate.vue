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
import { onMounted, onUnmounted } from 'vue';


const twitokStore = useTwitokStore()

const streamer_name = ref("")
const game = ref(["Fortnite", "VALORANT"]) // Jeux par défaut
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
const limitedStreamerSuggestions = computed(() => streamerSuggestions.value); // Pas de limite
const showSuggestions = ref(false);



const gameInput = ref(""); // Pour la saisie
const gameError = ref(""); // Pour les messages d'erreur
const gameSuggestions = ref([]);
const limitedGameSuggestions = computed(() => gameSuggestions.value.slice(0, 10));
const showGameSuggestions = ref(false);



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

const onStreamerInputKeydown = (e) => {
  if (e.key === 'Enter' && streamerInput.value.trim() !== '') {
    e.preventDefault();
    const val = streamerInput.value.trim();
    if (streamerSuggestions.value.includes(val)) {
      selectStreamer(val);
    } else if (!streamerSuggestions.value.includes(val)) {
      streamerError.value = "This streamer is not in the list.";
    }
  }
  if (e.key === 'Escape') {
    showSuggestions.value = false;
  }
};

const selectStreamer = (streamerName) => {
  streamer_name.value = streamerName;
  streamerInput.value = streamerName;
  streamerError.value = "";
  showSuggestions.value = false;
  streamerSuggestions.value = [];
};

const onStreamerInputFocus = () => {
  if (streamerSuggestions.value.length > 0) {
    showSuggestions.value = true;
  }
};

const onStreamerInputBlur = () => {
  // Petit délai pour permettre le clic sur les suggestions
  setTimeout(() => {
    showSuggestions.value = false;
  }, 150);
};

const onGameInputKeydown = (e) => {
  if (e.key === 'Enter' && gameInput.value.trim() !== '') {
    e.preventDefault();
    const val = gameInput.value.trim();
    if (
      gameSuggestions.value.includes(val) &&
      !game.value.includes(val)
    ) {
      addGameFromSuggestion(val);
    } else if (!gameSuggestions.value.includes(val)) {
      gameError.value = "This game is not in the list.";
    }
  }
  if (e.key === 'Escape') {
    showGameSuggestions.value = false;
  }
};

const addGameFromSuggestion = (gameValue) => {
  if (!game.value.includes(gameValue)) {
    if (game.value.length < 5) {
      game.value.push(gameValue);
      gameError.value = "";
    } else {
      gameError.value = "Maximum 5 games allowed.";
    }
  }
  gameInput.value = '';
  showGameSuggestions.value = false;
  gameSuggestions.value = [];
};

const onGameInputFocus = () => {
  if (gameSuggestions.value.length > 0) {
    showGameSuggestions.value = true;
  }
};

const onGameInputBlur = () => {
  // Petit délai pour permettre le clic sur les suggestions
  setTimeout(() => {
    showGameSuggestions.value = false;
  }, 150);
};

const fetchStreamers = async (query) => {

  if (!query) {
 
    streamerSuggestions.value = [];
    return;
  }
  try {
 
    const resp = await axios.get(`/search_streamers?q=${query}`);
 
    streamerSuggestions.value = resp.data.streamers;
  } catch (e) {

    streamerSuggestions.value = [];
  }
};

watch(streamerInput, (newVal) => {
  fetchStreamers(newVal);
  if (newVal && streamerSuggestions.value.length > 0) {
    showSuggestions.value = true;
  } else {
    showSuggestions.value = false;
  }
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
  if (newVal && gameSuggestions.value.length > 0) {
    showGameSuggestions.value = true;
  } else {
    showGameSuggestions.value = false;
  }
});







</script>

<template>
    <studio-header />
    <div  class="content-under-header px-4 sm:px-6 lg:px-8 pt-[10vh] sm:pt-[18vh] md:pt-[6vh] lg:pt-[6vh] xl:pt-[5vh] 2xl:pt-[4vh] animate-fade-in-up max-w-7xl mx-auto  min-h-screen "> <!-- body -->
        <div  class=" w-full h-full"> <!-- formulaire -->
            <form v-if="!chargement" action="" class="space-y-2 sm:space-y-3">

                <div class="flex flex-col justify-center items-center w-full">
                    <div class="w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl font-inter font-medium text-sm sm:text-base md:text-lg lg:text-xl">Streamer's name</div>
                    <div class="relative w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl mt-2 ml-3">
                        <input
                            class="rounded-lg py-2 sm:py-3 h-6 sm:h-8 md:h-10 w-full input-field border border-black focus:border-black focus:ring-0 px-3 font-inter text-sm sm:text-base md:text-lg transition-all duration-200"
                            type="text"
                            id="streamer_name"
                            name="streamer_name"
                            v-model="streamerInput"
                            @keydown="onStreamerInputKeydown"
                            @focus="onStreamerInputFocus"
                            @blur="onStreamerInputBlur"
                            placeholder="talmo"
                            autocomplete="off"
                        >
                        
                        <!-- Liste de suggestions personnalisée -->
                        <div v-if="showSuggestions && limitedStreamerSuggestions.length > 0" 
                             class="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-lg mt-1 max-h-48 overflow-y-auto z-50 shadow-lg">
                            <div v-for="suggestion in limitedStreamerSuggestions" 
                                 :key="suggestion"
                                 @click="selectStreamer(suggestion)"
                                 class="px-3 py-2 hover:bg-gray-100 cursor-pointer text-sm sm:text-base border-b border-gray-100 last:border-b-0">
                                {{ suggestion }}
                            </div>
                        </div>
                    </div>
                    <div v-if="streamerError" class="text-red-500 text-xs sm:text-sm mt-1 w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl ml-3">{{ streamerError }}</div>
                </div>
                
                <div class="flex flex-col justify-center items-center w-full">
                    <div class="w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl font-inter font-medium text-sm sm:text-base md:text-lg lg:text-xl">Games</div>
                    <div class="relative w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl mt-2 ml-3">
                        <input 
                            class="rounded-lg py-2 sm:py-3 h-6 sm:h-8 md:h-10 w-full input-field border border-black focus:border-black focus:ring-0 px-3 font-inter text-sm sm:text-base md:text-lg transition-all duration-200" 
                            type="text" 
                            id="game" 
                            name="game" 
                            v-model="gameInput" 
                            @keydown="onGameInputKeydown" 
                            @focus="onGameInputFocus"
                            @blur="onGameInputBlur"
                            placeholder="Fortnite"
                            autocomplete="off"
                        >
                        
                        <!-- Liste de suggestions personnalisée -->
                        <div v-if="showGameSuggestions && gameSuggestions.length > 0" 
                             class="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-lg mt-1 max-h-48 overflow-y-auto z-50 shadow-lg">
                            <div v-for="suggestion in gameSuggestions" 
                                 :key="suggestion"
                                 @click="addGameFromSuggestion(suggestion)"
                                 class="px-3 py-2 hover:bg-gray-100 cursor-pointer text-sm sm:text-base border-b border-gray-100 last:border-b-0">
                                {{ suggestion }}
                            </div>
                        </div>
                    </div>
                    <div v-if="gameError" class="text-red-500 text-xs sm:text-sm mt-1 w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl ml-3">{{ gameError }}</div>
                </div>

                <div v-if="game.length && !(game.length === 1 && game[0] === '')" class="flex flex-wrap justify-center items-center gap-2 sm:gap-3 w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl mx-auto px-2">
                    <div v-for="g in game" :key="g"
                    class="relative border-1 border-black rounded-lg min-w-[80px] sm:min-w-[90px] md:min-w-[100px] lg:min-w-[110px] h-10 sm:h-11 md:h-12 font-inter font-medium flex justify-center items-center bg-gray-100 hover:bg-gray-200 transition-colors duration-200"
                    >
                    <span
                        class="truncate max-w-[70px] sm:max-w-[80px] md:max-w-[90px] lg:max-w-[100px] w-full flex justify-center items-center text-center text-xs sm:text-sm md:text-base"
                        style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; display:block;"
                    >{{ g }}</span>
                    <button
                        @click.prevent="game.splice(game.indexOf(g), 1)"
                        class="absolute -top-1 sm:-top-2 -right-1 sm:-right-2 bg-black hover:bg-red-600 text-white rounded-full w-5 h-5 sm:w-6 sm:h-6 flex items-center justify-center text-xs shadow-md hover:shadow-lg transition-all duration-150 hover:scale-105"
                        aria-label="Supprimer"
                        style="z-index:2;"
                    >×</button>
                    </div>
                </div>
               
                <div class="flex flex-col justify-center items-center w-full">
                    <div class="w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl font-inter font-medium text-sm sm:text-base md:text-lg lg:text-xl flex items-center">
                        <div class='font-inter'>Duration</div>
                        <div class='font-inter text-xs sm:text-sm md:text-base px-1 pt-1 text-gray-600'>(in sec)</div>
                    </div>
                    <div class="w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl relative mt-4 ml-3">
                        <!-- Valeur flottante -->
                        <div 
                        class="absolute -top-8 sm:-top-10 bg-black text-white px-2 py-1 rounded text-xs sm:text-sm transform -translate-x-1/2 transition-all duration-200"
                        :style="{ left: `${(duration / 90) * 100}%` }"
                        >
                        {{ duration }}s
                        </div>
                        
                        <!-- Container du slider -->
                        <div class="relative w-full h-4 sm:h-5 md:h-6 bg-white border-2 border-gray-300 rounded-full overflow-hidden">
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
                        <div class="flex justify-between text-xs sm:text-sm md:text-base text-gray-600 mt-2 font-inter">
                        <span>0s</span>
                        <span>45s</span>
                        <span>90s</span>
                        </div>
                    </div>
                </div>
                
                <div class="flex flex-col justify-center items-center w-full">
                    <div class="w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl font-medium text-sm sm:text-base md:text-lg lg:text-xl font-inter">View's</div>
                        <div class="flex flex-row justify-start items-center w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl mt-3 ml-3 px-2">
                            <div class="flex flex-row justify-center items-center gap-2">
                                <div class="font-inter font-light text-sm sm:text-base md:text-lg">Min</div>
                                <input class="rounded-lg py-1.5 sm:py-2 md:py-2.5 h-6 sm:h-8 md:h-10 w-16 sm:w-16 md:w-18 lg:w-20 input-field border border-black focus:border-black focus:ring-0 px-2 text-sm sm:text-base md:text-lg transition-all duration-200" type="number" id="views_min" name="views_min" min="0" v-model="min_views">
                            </div>

                            <div class="flex flex-row justify-center items-center gap-2 ml-2">
                                <div class="font-inter font-light text-sm sm:text-base md:text-lg">Max</div>
                                <input class="rounded-lg py-1.5 sm:py-2 md:py-2.5 h-8 sm:h-8 md:h-10 w-16 sm:w-16 md:w-18 lg:w-20 input-field border border-black focus:border-black focus:ring-0 px-2 text-sm sm:text-base md:text-lg transition-all duration-200" type="number" id="views_max" name="views_max" min="0" v-model="max_views">
                            </div>
                        </div>
                </div>
                

        <div class="flex flex-col justify-center items-center w-full">
            <label class="font-inter w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl font-medium text-sm sm:text-base md:text-lg lg:text-xl mb-3">
                Release Date
            </label>
            
            <!-- Container unifié -->
            <div class="flex flex-col sm:flex-row items-center border border-gray-300 rounded-lg w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl p-2 sm:p-3 md:p-4 gap-3 sm:gap-0 ml-3">
            <!-- Date de début -->
                    <div class="flex-1 w-full sm:w-auto ">
                        <label class="block text-xs sm:text-sm md:text-base text-gray-500 mb-1 sm:mb-2">Start date</label>
                        <input 
                        type="date"
                        v-model="startDate"
                        class="w-full border-none outline-none text-sm sm:text-base focus:ring-0 rounded"
                        >
                    </div>
                    
                    <!-- Séparateur -->
                    <div class="px-2 text-gray-400 hidden sm:block">
                        <svg class="w-4 h-4 md:w-5 md:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                    </div>
                    
                    <!-- Date de fin -->
                    <div class="flex-1 w-full sm:w-auto">
                        <label class="block text-xs sm:text-sm md:text-base text-gray-500 mb-1 sm:mb-2">End date</label>
                        <input 
                        type="date"
                        v-model="endDate"
                        :min="startDate"
                        class="w-full border-none outline-none text-sm sm:text-base focus:ring-0 rounded"
                        >
                    </div>
            </div>
        </div>
        <div class="flex flex-col justify-center items-center w-full">
            <div class='flex flex-row items-center gap-2 w-full max-w-xs sm:max-w-sm md:max-w-lg lg:max-w-2xl xl:max-w-3xl ml-3'>
                <div class="font-inter font-medium text-sm sm:text-base md:text-lg lg:text-xl">Number of clips</div>
                <div class="text-xs sm:text-sm md:text-base font-thin md:font-light text-gray-600">(max 10)</div>
                <input class='border border-black focus:border-black focus:ring-0 rounded-lg px-3 py-2 w-16 sm:w-18 md:w-20 h-8 sm:h-8 md:h-10 text-sm sm:text-base md:text-lg text-center transition-all duration-200' type="number" min="1" max="10" id="number_of_clips" name="number_of_clips" v-model="number_of_clips" value="1">
            </div>
        </div>
               
                    
                    
                   
               
               <div class="flex justify-center w-full pt-6">
                    <button 
                        type="button"
                        @click="getClips()"
                        class="!bg-black hover:!bg-gray-600 !transition-colors !duration-200 w-40 md:w-56 py-2 md:py-3 md:text-[20px] !text-white font-medium rounded-lg"
                    >
                        Find
                    </button>
                </div>
                
                
            </form>
            <div v-if="chargement" class="flex justify-center items-center w-full mt-6 sm:mt-8">
                <div class="text-center">
                    <div class="animate-spin rounded-full h-8 w-8 sm:h-10 sm:w-10 md:h-12 md:w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
                    <p class="text-sm sm:text-base md:text-lg font-inter text-gray-700">Vos vidéos sont en cours de téléchargement...</p>
                </div>
            </div>
        </div>
    </div>
</template>


