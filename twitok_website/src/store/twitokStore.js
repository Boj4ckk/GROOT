import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useTwitokStore = defineStore('useTwitokStore', () => {
    // STATE pour déclarer des variables réactives dans le store
    const state = ref({
        authorizedConnection: false,
    });

    // GETTER permet de récupérer des valeurs du state, et éventuellement faire des calculs à partir de ces infos
    const authorizedConnection = computed(() => state.value.authorizedConnection);

    // ACTION permet d'éxecuter des fonctions asynchrones ou logiques complexes qui modifient le state cette fois
    const autorized = () => {
        state.value.authorizedConnection = true
    }

    const unauthorized = () => {
        state.value.authorizedConnection = false
    }

    // Exposer les props et méthodes
    return {
        authorizedConnection,
        autorized,
        unauthorized,
    }
})
