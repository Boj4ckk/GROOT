import { createRouter, createWebHistory } from 'vue-router'
import Connected from './components/connected.vue'
import { useTwitokStore } from './store/twitokStore'
import { ref } from 'vue'
import Inscription from './components/inscription.vue'
import Connection from './components/connection.vue'

const routes = [
    { path:'/inscription', name:'Inscription', component: Inscription }, 
    { path:'/connected', name:'Connected', component: Connected},   
    { path:'/connection', name:'Connection', component: Connection},
]

const router = createRouter({
    history: createWebHistory(), 
    routes, 
})

router.beforeEach((to, from, next) => {
    const twitokStore = useTwitokStore() 

    if (to.name == 'Connected' && twitokStore.authorizedConnection){
        console.log("user deja connecté, autorisé a entrer")
        return next()
    }
    // console.log("user autorisé à entrer : ", twitokStore.authorizedConnection)
    else if (!twitokStore.authorizedConnection && (to.name !== 'Inscription' && to.name !== 'Connection' ) ){
        return next ({name:'Connection'})
    }
    return next()
    // return false //false c pour annuler la navigation en cours si l'user a modifie l'url via l'url ou le bouton de rtour
    // return emplacement different (par exemple pour reidirger vers home )
})

export default router