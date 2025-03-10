import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import { useTwitokStore } from './store/twitokStore'
import Test_autre_connected from './components/test_autre_connected.vue'
import Showuser from './components/showuser.vue'
import Home from './components/home.vue'
import Login from './components/login.vue'
import Studio from './components/studio/studio.vue'
import Register from './components/register.vue'
import Help from './components/help.vue'

const routes = [
    { path:'/', name:'Home', component: Home }, 
    { path:'/register', name:'Register', component: Register, meta: {logoutWhenAccess: true} }, 
    { path:'/login', name:'Login', component: Login, meta: {logoutWhenAccess: true}},
    { path:'/studio/', name:'Studio', component: Studio, meta: {requiresAuth: true} },   
    { path:'/help', name:'Help', component: Help },   
    { path:'/autreConnected', name:'AutreConnected', component: Test_autre_connected, meta: {requiresAuth: true} },   
    { path:'/showuser', name:'Showuser', component: Showuser },   
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
            return next('studio') // ici normalement je voulais rediriger vers la page de ou on venait mais impossible car from.path = "/" jsp prq
        }
    }
    if (to.meta.requiresAuth && !twitokStore.authorizedConnection){
        console.log(twitokStore.authorizedConnection, ': utilisateur non autorisé : redirection dans /connection')
        return next('login')
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