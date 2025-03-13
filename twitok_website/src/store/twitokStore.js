import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import router from '@/router';

export const useTwitokStore = defineStore('useTwitokStore', () => {
    // STATE pour déclarer des variables réactives dans le store
    // const state = ref({
    //     authorizedConnection: sessionStorage.getItem('authorizedConnection') ?? false, // si rien alors false par défaut. 
    //     actualUser: sessionStorage.getItem('actualUser')
    // });

    const state = ref({
        authorizedConnection: sessionStorage.getItem('authorizedConnection') === 'true', // permet d'avoir un vrai booléen car sessionStorage stocke uniquement des str et non des bool meme si on met = true ca va stocker 'true' odnc la condition serait toujours validé car 'true' ou 'false' et dans tous les cas non vides donc true
        actualUser: sessionStorage.getItem('actualUser'),
        clipsReturned: JSON.parse(localStorage.getItem('clipsReturned')) || [] 
    });


    // GETTER permet de récupérer des valeurs du state, et éventuellement faire des calculs à partir de ces infos
    const authorizedConnection = computed(() => state.value.authorizedConnection);
    const actualUser = computed(() => state.value.actualUser);
    const clipsReturned = computed(()=> state.value.clipsReturned); 

    // ACTION permet d'éxecuter des fonctions asynchrones ou logiques complexes qui modifient le state cette fois
    const autorized = () => {
        state.value.authorizedConnection = true
        sessionStorage.setItem('authorizedConnection', true) // localstorage = sauvgaerager meme avec refresh (dans navigateur) p(peut que enregistrer string jcrois) 
    }

    const unauthorized = () => {
        state.value.authorizedConnection = false
        sessionStorage.removeItem('authorizedConnection')
    }

    const logout = () => {
        unauthorized()
        console.log("déconexion de l'utilisateur... ")
    } 

    const setClipsReturned = (clips) => {
        state.value.clipsReturned = clips
        localStorage.setItem('clipsReturned', JSON.stringify(clips))
    }

    // const setActualUser = (user) => {
    //     state.value.actualUser = 
    // }

    // Exposer les props et méthodes
    return {
        authorizedConnection,
        actualUser,
        clipsReturned,
        autorized,
        unauthorized,
        logout,
        setClipsReturned,
    }
})
