import { createRouter, createWebHistory } from 'vue-router'
import Connected from './components/connected.vue'
import Accueil from './components/accueil.vue'
import { useTwitokStore } from './store/twitokStore'
import { ref } from 'vue'

const routes = [
    { path:'/', name:'Accueil', component: Accueil }, 
    { path:'/connected', name:'Connected', component: Connected},   
]

const router = createRouter({
    history: createWebHistory(), 
    routes, 
})

router.beforeEach((to, from, next) => {
    console.log("user autorisé à entrer : ", useTwitokStore.authorizedConnection)
    if (!useTwitokStore.authorizedConnection && to.name !== 'Accueil'){
        next ({name:'Accueil'})
    }else {
        next() 
    }
    // return false //false c pour annuler la navigation en cours si l'user a modifie l'url via l'url ou le bouton de rtour
    // return emplacement different (par exemple pour reidirger vers home )
})

export default router