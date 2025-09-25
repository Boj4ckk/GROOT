<script setup> 
import axios from 'axios';
import { ref } from 'vue';
import apiClient from '@/api';
import router from '@/router';
import { useTwitokStore } from '@/store/twitokStore'; //import. store 
import {AtSymbolIcon} from '@heroicons/vue/24/solid'

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

    <div class="">
        <div class='flex justify-center font-inter font-bold pt-20 md:pt-1 text-[20px] md:text-[35px] animate-fade-in-up'>
            Create an account
        </div>
        <div class=' flex justify-center py-4 animate-fade-in-up'>
            <div class=' border-1 border-black flex  py-1 px-1'>
                    <at-symbol-icon class=" h-4 w-5 md:h-8 md:w-9 text-gray-900" />
                    <h7 class='px-2 md:px-3 md:pt-1 font-inter font-medium text-[12px] md:font-semibold md:text-[17px]'>
                        Sign up with google
                    </h7>
                    
                
            </div>
        </div>

        <div class=' flex flex-col justify-center items-center '>
             <form class="flex flex-col justify-between  md:px-64 animate-fade-in-up" action="">
                 <div class=" flex flex-col px-4 py-1 items-center ">
                    <div class=" w-64 md:w-96 font-inter font-light text-[15px] md:text-[20px]">Email</div>
                    <input class='rounded-lg py-1 w-64 md:w-96 input-field border-1 border-black px-2' type="text" v-model="username"  required  >
                </div>
                <div class=" flex flex-col px-4 py-1 items-center ">
                    <div class=" w-64 md:w-96 font-inter font-light text-[15px] md:text-[20px]">Password</div>
                    <input class='rounded-lg py-1 w-64 md:w-96 input-field border-1 border-black px-2'  type="password" v-model="password"  required >
                </div>
                <div class=" flex flex-col px-4 py-1 pb-5 items-center ">
                    <div class=" w-64 md:w-96 font-inter font-light text-[15px] md:text-[20px]">Re-enter Password</div>
                    <input class='rounded-lg py-1  w-64 md:w-96 input-field border-1 border-black px-2'  type="password" v-model="password"  required >
                </div>
              
               
                
                
            </form>
            <input type="submit" @click.prevent="insert_user()" class="submit-btn border-1 border-black w-48 md:w-64 py-1 md:text-[20px] animate-fade-in-up" value='Register'> <!-- prevent c pour éviter que la page se recharge a chauqe fois qu'on soumet le form -->

         <router-link class="no-underline pt-2 text-black font-inter font-extralight text-[12px] md:text-[18px] animate-fade-in-up" to="login">Already an account ?</router-link>
        </div>
       
    </div>

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