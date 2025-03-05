<script setup>
import axios from 'axios';
import { ref } from 'vue';
import apiClient from '@/api';
import router from '@/router';
import { useTwitokStore } from '@/store/twitokStore';

const twitokstore = useTwitokStore()
const logout = () => {
    twitokstore.unauthorized()
    router.push('/connection')
} 

</script>

<template>
    yo t'es encoire connecté sur l'autre page connected 

    <form>
        <input type="submit" @click.prevent="logout()" value="logout">
    </form>
</template>
