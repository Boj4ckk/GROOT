<script setup>
import axios from 'axios'
import { ref } from 'vue'
import router from '@/router'
import { useTwitokStore } from '@/store/twitokStore'; //import. store 
import {AtSymbolIcon} from '@heroicons/vue/24/solid'

const user_email = ref("")
const user_password = ref("")
const twitokStore = useTwitokStore() // vient du store 


const connect = async () => {
    try {
        const dataToSend = {user_email: user_email.value, user_password: user_password.value}
        const response = await axios.post('/login', dataToSend)
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
<div class="">
        <div class='flex justify-center font-inter font-bold pt-20 md:pt-1 text-[20px] md:text-[35px] animate-fade-in-up'>
            Sign In
        </div>
        <div class=' flex justify-center py-4 animate-fade-in-up'>
            <div class=' border-1 border-black flex  py-1 px-1'>
                    <at-symbol-icon class=" h-4 w-5 md:h-8 md:w-9 text-gray-900" />
                    <h7 class='px-2 md:px-3 md:pt-1 font-inter font-medium text-[12px] md:font-semibold md:text-[17px]'>
                        Sign in with google
                    </h7>
                    
                
            </div>
        </div>

        <div class=' flex flex-col justify-center items-center '>
             <form class="flex flex-col justify-between  md:px-64 animate-fade-in-up" action="">
                 <div class=" flex flex-col px-4 py-1 items-center ">
                    <div class=" w-64 md:w-96 font-inter font-light text-[15px] md:text-[20px]">Email</div>
                    <input class='rounded-lg py-1 w-64 md:w-96 input-field border-1 border-black px-2' type="text" v-model="user_email"  required  >
                </div>
                <div class="flex flex-col px-4 py-1 items-center pb-5  ">
                    <div class=" w-64 md:w-96 font-inter font-light text-[15px] md:text-[20px]">Password</div>
                    <input class='rounded-lg py-1 w-64 md:w-96 input-field border-1 border-black px-2'  type="password" v-model="user_password"  required >
                </div>
              
               
                
                
            </form>
            <input type="submit" @click.prevent="connect()" class="border-1 border-black w-48 md:w-64 py-1 md:text-[20px] animate-fade-in-up" value='Login'> <!-- prevent c pour éviter que la page se recharge a chauqe fois qu'on soumet le form -->

         <router-link class="no-underline pt-2 text-black font-inter font-extralight text-[12px] md:text-[18px] animate-fade-in-up" to="register">Not registered ? Sign up</router-link>
        </div>
       
    </div>
</template>