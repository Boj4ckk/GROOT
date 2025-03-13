<script setup>

import { useTwitokStore } from '@/store/twitokStore';
import router from '@/router';

const TwitokStore = useTwitokStore() 

const clips = TwitokStore.clipsReturned

const index_of_clips = [] 


console.log (clips) 
</script>

<template>
    yo t 'es dans edit 
    <br>
    voici les clips dipos pour toi : 
    <ul>
        <li v-for="clip in clips"> {{ clip }} </li>
    </ul>

</template>