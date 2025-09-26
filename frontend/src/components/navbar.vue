<script setup>

import { RouterView } from 'vue-router';
import { useTwitokStore } from '@/store/twitokStore';
import { useRouter } from 'vue-router';
import login from '@/views/login.vue';
import { computed, ref } from 'vue';
import redirectionLink from './redirectionLink.vue';
import customButton from './customButton.vue';
import {Bars2Icon, Bars3Icon, BeakerIcon, AtSymbolIcon} from '@heroicons/vue/24/solid'
import BorderButton from './customButton.vue';

const router = useRouter() 

const twitokstore = useTwitokStore()

const logout = () => {
    twitokstore.unauthorized()
}
const connected = computed(() => twitokstore.authorizedConnection)
const isMobileMenuOpen = ref(false)

function toggleMobileMenu (){
    isMobileMenuOpen.value = !isMobileMenuOpen.value
    console.log(isMobileMenuOpen.value)

}

function closeMobileMenu (){
    isMobileMenuOpen.value = false
}

console.log("etat actuel de la variable connected : ", connected)

</script>

<template>
    <header class=" shadow-lg fixed top-0 left-0 right-0 z-50 ">
        <div class="">  

            <div class="flex justify-between items-center h-12 md:h-16">
                <div class=" flex-shrink-0 flex items-center">
                    <redirection-link to="/" class="text-[12px] md:text-[20px] transform transition-transform duration-300 hover:scale-105">Home</redirection-link>
                </div>

                <nav id="mainNav" class="hidden lg:flex w-1/2 max-w-7xl justify-center">
                    <div class="flex space-x-6">
                        <redirection-link to="/studio" class=" transform transition-transform duration-300 hover:scale-105">Studio</redirection-link>
                        <redirection-link to="/help" class=" transform transition-transform duration-300 hover:scale-105">Help</redirection-link>
                        <redirection-link to="/pricing" class=" transform transition-transform duration-300 hover:scale-105">Pricing</redirection-link>
                    </div>
                </nav>

                <div class="flex justify-center">
                    <customButton v-if='!connected' to="/register" >Sign up</customButton>
                    <customButton v-if='connected' to="/login"  @click="logout" >Log out</customButton>
                    <button class=" md:hidden ml-2 p-2 text-white" @click='toggleMobileMenu'>
                      <Bars3Icon class=" h-6 w-6 text-gray-700" />
                    </button>
                    
                    
                </div>

                    
            </div>
        </div>
        <transition name="slide-down">
           <div v-if="isMobileMenuOpen" class="md:hidden">
                <div class=" py-16 flex flex-col items-center bg-white min-h-screen w-full md:hidden absolute top-full left-0 right-0 z-40">
                        <redirection-link @click='closeMobileMenu' to="/studio" class="py-2 font-medium text-2xl">Studio</redirection-link>
                        <redirection-link @click='closeMobileMenu' to="/help" class="py-2 font-medium text-2xl">Help</redirection-link>
                        <redirection-link @click='closeMobileMenu' to="/pricing" class="py-2 font-medium text-2xl">Pricing</redirection-link>
                </div>     
            </div>

        </transition>
    
    </header>

</template>


<style scoped>

.slide-down-enter-active,
.slide-down-leave-active{
    transition: 0.3s ease-in-out;
}


.slide-down-enter-from {
    max-height: 0;
    opacity: 0;
}
.slide-down-enter-to{
    max-height: 100vh;
    opacity: 1;
}


.slide-down-leave-from{
    max-height: 100vh;
    opacity: 1;
}

.slide-down-leave-to{
    max-height: 0;
    opacity: 0;
}

</style>