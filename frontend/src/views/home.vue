<script setup>
import customButton from '../components/customButton.vue';
</script>

<template>
    <br> 
    <div class="  flex flex-col justify-center items-center pt-40 md:pt-70"> <!-- page -->    

        <div class="w-full flex flex-col justify-center items-center space-y-2 md:space-y-6">
            <h2 class="text-xl md:text-5xl font-inter font-bold  animate-fade-in-up">
                First AI-powered highlight-based content generator
            </h2>
            <p class="text-base md:text-3xl font-inter font-medium text-center max-w-4xl  animate-fade-in-up">
                Tool that transforms your stream highlights into engaging, shareable clips optimized for any platform.
            </p>
        </div>

        <div class=" flex flex-col justify-center items-center pt-10  animate-fade-in-up"> <!-- BOUTON -->
            <customButton to="/help"
             backgroundColor="bg-black" 
             textColor="text-white"
             buttonSize="md"
             >Try for free</customButton >
            <div>
                <p class="pt-2  animate-fade-in-up text-[10px] md:text-lg"> No credit card needed </p>
            </div>
        </div> <!-- /> -->

     

    </div> <!-- page/> -->

</template>

<style>


video {
  width: 100%;
  max-width: 200px;
  height: auto;
}

</style>