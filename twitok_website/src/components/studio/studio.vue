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
    <br><br><br>
    <div> <!-- body -->
        <div> <!-- formulaire -->
            <form action="">
                <label for="streamer_name"> Streamer's name </label>
                <input type="text" name="streamer_name">
                <label for="game"> Streamer's name </label>
                <input type="text" name="game">
                <label for="duration"> Duration </label>
                <input type="range" min="0" max="90" step="10" list="tickmarks">
                <datalist id="tickmarks">
                    <option value="0"></option>
                    <option value="30"></option>
                    <option value="60"></option>
                    <option value="90"></option> <!-- je crois avec du css on peut afficher les valeurs genre 60 90 et tt -->
                </datalist>
            </form>
        </div>
    </div>
</template>
