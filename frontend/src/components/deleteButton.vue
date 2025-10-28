
<script setup>
import { XMarkIcon } from '@heroicons/vue/24/solid';


const props = defineProps({

    width:{
        type:String,
        required:true
    },
    height:{
        type:String,
        required:true
    }

})
</script>


<template>

    <button class="w-[30px] h-[30px] bg-red-700 rounded-sm transform transition-transform duration-300 hover:scale-105 ">
       <XMarkIcon class="text-white"></XMarkIcon>
    </button>
</template>