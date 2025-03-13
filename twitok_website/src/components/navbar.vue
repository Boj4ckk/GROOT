<script setup>

import { RouterView } from 'vue-router';
import { useTwitokStore } from '@/store/twitokStore';
import { useRouter } from 'vue-router';
import login from '@/views/login.vue';
import { computed, ref } from 'vue';

const router = useRouter() 

const twitokstore = useTwitokStore()
const logout = () => {
    router.push("/login")
}

const connected = computed(() => twitokstore.authorizedConnection)

console.log("etat actuel de la variable connected : ", connected)

</script>

<template>

    <router-link to="/"> Logo </router-link>
    <router-link to="/studio"> Studio </router-link>
    <router-link to="/help"> Help </router-link>
    <router-link v-if="!connected" to="/login"> Log in </router-link>
    <router-link v-if="!connected" to="/register"> Register </router-link>
    <input v-if="connected" type="submit" @click="logout" value="logout">

</template>