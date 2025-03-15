import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import { useTwitokStore } from './store/twitokStore'

import home from './views/home.vue'
import register from './views/register.vue'
import login from './views/login.vue'
import studio from './views/studio/studio.vue'
import edit from './views/studio/edit.vue'
import test_autre_connected from './views/test_autre_connected.vue'
import help from './views/help.vue'
import Showuser from './components/showuser.vue'
import videoEdit from './views/studio/videoEdit.vue'

const routes = [
    { path:'/', name:'Home', component: home }, 
    { path:'/register', name:'Register', component: register, meta: {logoutWhenAccess: true} }, 
    { path:'/login', name:'Login', component: login, meta: {logoutWhenAccess: true}},
    { path:'/studio', name:'Studio', component: studio, meta: {requiresAuth: true} },  
    { path:'/studio/edit', name:'Edit', component: edit, meta: {requiresAuth: true} },  
    { path:'/autreConnected', name:'AutreConnected', component: test_autre_connected, meta: {requiresAuth: true} },   
    { path:'/help', name:'Help', component: help },   
    { path:'/showuser', name:'Showuser', component: Showuser },   

    { path:'/videoEdit/:videoId', name:'videoEdit', component: videoEdit, meta: {requiresAuth:true}}, 
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
            return next(from.fullPath) // pour annuler la redirection 
            // return next('studio') // ici normalement je voulais rediriger vers la page de ou on venait mais impossible car from.path = "/" jsp prq
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