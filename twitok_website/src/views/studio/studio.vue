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
                <label for="streamer_name">Streamer's name</label>
                <input type="text" id="streamer_name" name="streamer_name">
                <label for="game">Game</label>
                <input type="text" id="game" name="game" list="game-list">
                <datalist id="game-list"></datalist>
                <label for="duration">Duration <span>in sec</span></label>
                <input type="range" id="duration" name="duration" min="0" max="90" step="10" list="tickmarks">
                <datalist id="tickmarks">
                    <option value="0"></option>
                    <option value="30"></option>
                    <option value="60"></option>
                    <option value="90"></option>
                </datalist>
                <label for="views">Views</label>
                <div>
                    <label for="views_min">Min</label>
                    <input type="number" id="views_min" name="views_min" min="0">
                    <label for="views_max">Max</label>
                    <input type="number" id="views_max" name="views_max" min="0">
                </div>
                <label for="release">Date of release</label>
                <input type="date" id="release" name="release">
                
                <input type="submit" value="Find">
            </form>

        </div>
    </div>
</template>
