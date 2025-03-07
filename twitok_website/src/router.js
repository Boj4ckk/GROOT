import { createRouter, createWebHistory } from 'vue-router'
import Connected from './components/connected.vue'
import { useTwitokStore } from './store/twitokStore'
import Inscription from './components/inscription.vue'
import Connection from './components/connection.vue'
import Test_autre_connected from './components/test_autre_connected.vue'
import Showuser from './components/showuser.vue'

const routes = [
    { path:'/inscription', name:'Inscription', component: Inscription }, 
    { path:'/connection', name:'Connection', component: Connection},
    { path:'/connected', name:'Connected', component: Connected, meta: {requiresAuth: true} },   
    { path:'/autreConnected', name:'AutreConnected', component: Test_autre_connected, meta: {requiresAuth: true} },   
    { path:'/showuser', name:'Showuser', component: Showuser },   
]

const router = createRouter({
    history: createWebHistory(), 
    routes, 
})

router.beforeEach((to, from, next)=> {
    const twitokStore = useTwitokStore()
    if (to.meta.requiresAuth && !twitokStore.authorizedConnection){
        console.log(twitokStore.authorizedConnection, ': utilisateur non autorisé : redirection dans /connection')
        return next('connection')
    }
    else if (!twitokStore.authorizedConnection){
        console.log(twitokStore.authorizedConnection, ': utilisateur déconnecté')
        return next() 
    }
    else {
        console.log(twitokStore.authorizedConnection, ': utilisateur connecté')
        return next()
    }
})

export default router