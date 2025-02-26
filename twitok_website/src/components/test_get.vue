<script setup>
import axios from 'axios';
import { ref } from 'vue';

const users = ref([])

const getData = async() => {
    console.log("bouton cliqué")
    try{
        const responses = await axios.get('http://127.0.0.1:5000/showUsers')
        console.log(responses.data);
        users.value = responses.data
        console.log("users.value : ", users.value)
    }
    catch(error) {
        console.error('erreur', error) 
    }
}
</script>

<template>
    <button @click="getData()">yo clique moi pour voir les users</button><br>
    voici la liste des users : 
    <ul v-if="users.length > 0">
        <li v-for="user in users">
            {{ user.username }}
        </li>
    </ul>

</template>