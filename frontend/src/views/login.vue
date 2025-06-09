<script setup>
import axios from 'axios'
import { ref } from 'vue'
import router from '@/router'
import { useTwitokStore } from '@/store/twitokStore'; //import. store 

const user_email = ref("")
const user_password = ref("")
const twitokStore = useTwitokStore() // vient du store 


const connect = async () => {
    try {
        const dataToSend = {user_email: user_email.value, user_password: user_password.value}
        const response = await axios.post('http://127.0.0.1:5000/login', dataToSend)
        console.log("tentative de connexion de l'user : ", response.data)
        twitokStore.autorized()
        router.push('studio')
    }
    catch (error) {
        console.error("erreur lors de la requete... ", error)
        alert("username ou password incorrect(s)")
        // location.reload() 
    }
}
</script>

<template>

<form class="form-container" action="">
        <label> Sign up </label>
        <input type="text" v-model="user_email" placeholder="email" required class="input-field">
        <input type="password" v-model="user_password" placeholder="password" required class="input-field">
        <input type="submit" @click.prevent="connect()" class="submit-btn"> <!-- prevent c pour éviter que la page se recharge a chauqe fois qu'on soumet le form -->
    </form>

    <router-link 
    to="register">Not yet an account ?</router-link>

</template>