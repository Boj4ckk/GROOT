import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useTwitokStore = defineStore('useTwitokStore', () => {
    // STATE pour déclarer des variables réactives dans le store
    const state = ref({
        authorizedConnection: localStorage.getItem('authorizedConnection'),
    });

    // GETTER permet de récupérer des valeurs du state, et éventuellement faire des calculs à partir de ces infos
    const authorizedConnection = computed(() => state.value.authorizedConnection);

    // ACTION permet d'éxecuter des fonctions asynchrones ou logiques complexes qui modifient le state cette fois
    const autorized = () => {
        state.value.authorizedConnection = true
        localStorage.setItem('authorizedConnection', 'true') // localstorage = sauvgaerager meme avec refresh (dans navigateur) p(peut que enregistrer string jcrois) 
    }

    const unauthorized = () => {
        state.value.authorizedConnection = false
        localStorage.removeItem('authorizedConnection')
    }

    // Exposer les props et méthodes
    return {
        authorizedConnection,
        autorized,
        unauthorized,
    }
})
