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
        clipsUrls_Returned: JSON.parse(sessionStorage.getItem('clipsUrls_Returned')) || [],
        editedClipsUrl: JSON.parse(sessionStorage.getItem('editedClipsUrl')) || [],

        already_upload: sessionStorage.getItem('already_upload') || 0,
    });

    // GETTER permet de récupérer des valeurs du state, et éventuellement faire des calculs à partir de ces infos
    const authorizedConnection = computed(() => state.value.authorizedConnection);
    const actualUser = computed(() => state.value.actualUser);
    const clipsUrls_Returned = computed(()=> state.value.clipsUrls_Returned);
    const editedClipsUrl = computed(() => state.value.editedClipsUrl);
    const already_upload = computed(()=> state.value.already_upload); 

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

    const setclipsUrls_Returned = (clips) => {
        state.value.clipsUrls_Returned = clips
        sessionStorage.setItem('clipsUrls_Returned', JSON.stringify(clips))
    }
    const setEditedClipUrl = (clips) => {
        state.value.editedClipsUrl.push(clips)
        sessionStorage.setItem('editedClipsUrl', JSON.stringify(state.value.editedClipsUrl))
    }
    const setAlreadyUpload = () => {
        state.value.already_upload = 1
        sessionStorage.setItem('already_upload', '1') // ici pas besoin de Jsonifier parce que '1' est deja une str, on utilise ca que quand on on manipule des objets ou des tableaux etc pour garantir que ce sont des chaines JSON pour etre stocké comme telles
    }

    // const setActualUser = (user) => {
    //     state.value.actualUser = 
    // }
    return {
        authorizedConnection,
        actualUser,
        clipsUrls_Returned,
        editedClipsUrl,
        already_upload, 
        autorized,
        unauthorized,
        logout,
        setclipsUrls_Returned,
        setEditedClipUrl, 
        setAlreadyUpload,
    }
})
