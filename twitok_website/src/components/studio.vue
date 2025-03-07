<script setup>
import axios from 'axios';
import { ref } from 'vue';
import apiClient from '@/api';
import router from '@/router';
import { useTwitokStore } from '@/store/twitokStore';

const twitokstore = useTwitokStore()
const logout = () => {
    twitokstore.unauthorized()
    router.push('/login')
} 

// const getCurrentUser = async () => {
//     response = await axios.get('http://127.0.0.1:5000/get')
// }

</script>

<template>
    <br>
    yo t'es connecté 

    <form>
        <input type="submit" @click.prevent="logout()" value="logout">
    </form>
</template>
