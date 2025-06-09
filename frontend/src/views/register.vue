<script setup> 
import axios from 'axios';
import { ref } from 'vue';
import apiClient from '@/api';
import router from '@/router';
import { useTwitokStore } from '@/store/twitokStore'; //import. store 

const twitokStore = useTwitokStore() // vient du store 
// const authorizedConnection = twitokStore.authorizedConnection
console.log("twitokStore : ", twitokStore)

const username = ref("")
const password = ref("")
const tiktok_username = ref("")
const tiktok_password = ref("")

const insert_user = async () => {
    try {
        const dataToSend = {user_email: username.value, user_password: password.value}
        const response = await axios.post('http://127.0.0.1:5000/register', dataToSend)
        console.log("envoie nouvel user : ", response.data)
        twitokStore.autorized()
        router.push('studio')
    }
    catch (error) {
        console.error("erreur lors de la requete... ", error)
        alert("Nom d'utilisateur deja utilisé")
        // location.reload() 
    }
}

</script>

<template>

    <form class="form-container" action="">
        <label> Sign up </label>
        <input type="text" v-model="username" placeholder="username" required class="input-field">
        <input type="password" v-model="password" placeholder="password" required class="input-field">
        <input type="text" v-model="tiktok_username" placeholder="tiktok username" class="input-field">
        <input type="password" v-model="tiktok_password" placeholder="tiktok password" class="input-field">
        <input type="submit" @click.prevent="insert_user()" class="submit-btn"> <!-- prevent c pour éviter que la page se recharge a chauqe fois qu'on soumet le form -->
    </form>

    <router-link to="connection">Already an account ?</router-link>


</template>


<!-- <style scoped>
.form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #1e1e1e;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Style des champs de saisie */
.input-field {
    width: 100%;
    padding: 12px;
    margin: 8px 0;
    border: 2px solid #333;
    border-radius: 8px;
    background-color: #2a2a2a;
    color: #fff;
    font-size: 16px;
}

/* Focus sur les champs de saisie */
.input-field:focus {
    border-color: #e60000; /* Rouge Twitch */
    outline: none;
}

/* Style du bouton d'envoi */
.submit-btn {
    background-color: #ff4f56; /* Couleur rouge de TikTok */
    color: #fff;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
    width: 100%;
    margin-top: 10px;
}

/* Effet au survol du bouton */
.submit-btn:hover {
    background-color: #d92f3e; /* Rouge TikTok foncé */
}

/* Style pour le bouton au clic */
.submit-btn:active {
    background-color: #e60000; /* Rouge Twitch */
}

/* Responsivité */
@media (max-width: 600px) {
    .form-container {
        padding: 15px;
    }
    .input-field {
        padding: 10px;
    }
    .submit-btn {
        padding: 10px 20px;
    }
}
</style> -->