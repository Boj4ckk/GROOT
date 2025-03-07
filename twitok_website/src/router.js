import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import Connected from './components/connected.vue'
import { useTwitokStore } from './store/twitokStore'
import Inscription from './components/inscription.vue'
import Connection from './components/connection.vue'
import Test_autre_connected from './components/test_autre_connected.vue'
import Showuser from './components/showuser.vue'
import Home from './components/home.vue'

const routes = [
    { path:'/inscription', name:'Inscription', component: Inscription, meta: {logoutWhenAccess: true} }, 
    { path:'/connection', name:'Connection', component: Connection, meta: {logoutWhenAccess: true}},
    { path:'/connected', name:'Connected', component: Connected, meta: {requiresAuth: true} },   
    { path:'/autreConnected', name:'AutreConnected', component: Test_autre_connected, meta: {requiresAuth: true} },   
    { path:'/showuser', name:'Showuser', component: Showuser },   
    { path:'/', name:'Home', component: Home }, 
]

const router = createRouter({
    history: createWebHistory(), 
    // history: createWebHashHistory(), 
    routes, 
})

router.beforeEach((to, from, next)=> {
    const twitokStore = useTwitokStore()
    console.log("from page : ", from.fullPath)

    if (to.meta.logoutWhenAccess && twitokStore.authorizedConnection){
        console.log("from page : ", from.fullPath)
        if (confirm("This action will disconnect your profile")){
            twitokStore.logout()
            console.log(twitokStore.authorizedConnection, ': utilisateur déconnecté')
            return next()
        }
        else {
            // return next(from.fullPath) // pour annuler la redirection 
            return next('/connected') // ici normalement je voulais rediriger vers la page de ou on venait mais impossible car from.path = "/" jsp prq
        }
    }
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