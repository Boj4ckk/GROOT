import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useTwitokStore = defineStore('useTwitokStore', () => {
    // STATE pour déclarer des variables réactives dans le store
    const authorizedConnection = ref(false) 

    // GETTER permet de récupérer des valeurs du state, et éventuellement faire des calculs a partir de ces iunfos 

    // ACTION permet d'éxecuter des fonctions asynchrones ou logiques complexes qui modifient le state cette fois 
    const autorized = () => {
        authorizedConnection.value = true
    }

    // epxoser les prop et méthodes 
    return {
        authorizedConnection, 
        autorized,
    }
})