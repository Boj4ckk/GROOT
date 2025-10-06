<script setup>
import {useRoute} from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const currentPath = computed (() => route.path)

const isCurrentPath = (title) =>{
    
    if(currentPath.value.split('/')[2] == title){
       
        return true;
    }
    return false;
}

</script>


<template>
     <header class=" bg-black shadow-lg fixed top-14 left-0 right-0 z-50 h-[35px] flex justify-center items-center">
        <nav id="mainNav" class="  lg:flex  max-w-lg justify-center  mr-8">
                    <div class="space-x-12 md:space-x-16 flex justify-between">
                         <div :class="[
                            isCurrentPath('filtrate') 
                                ? 'text-white font-inter font-medium text-[13px] md:text-[16px]' 
                                : 'text-gray-400 font-inter font-medium text-[13px] md:text-[16px]'
                            ]">Filtrate</div>
                         <div :class="[
                            isCurrentPath('clip_selection') 
                                ? 'text-white font-inter font-medium text-[13px] md:text-[16px]' 
                                : 'text-gray-400 font-inter font-medium text-[13px] md:text-[16px]'
                            ]">Selection</div>
                         <div :class="[
                            isCurrentPath('video_edit') 
                                ? 'text-white font-inter font-medium text-[13px] md:text-[16px]' 
                                : 'text-gray-400 font-inter font-medium text-[13px] md:text-[16px]'
                            ]">Editing</div>
                    </div>
                </nav>
     </header>

</template>

<style scoped>
  

</style>
