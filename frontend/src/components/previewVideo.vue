

<script setup>
import { computed } from 'vue';

const props = defineProps({
    videoUrl:{
        type: String,
        required:true
    },
    boxArtUrl:{
        type:String,
        required:true
    },
    boxArtWidth:{
        type:[String, Number],
        default: '144'
    },
    boxArtHeight: {
        type: [String, Number],
        default: '192' // Valeur par défaut si non fournie
    },
    viewCount:{
        type:Number,
        required:true
    },
    creationDate:{
        type:String,
        required:true
    },
    title:{
        type:String,
        required:true
    },
    broadcasterName:{
        type:String,
        required:true
    }
    


    
  
})

const formattedBoxArtUrl = computed(() => {
    if (!props.boxArtUrl) {
        return '';
    }
    // ✅ 2. Utiliser les props au lieu des valeurs en dur
    return props.boxArtUrl
        .replace('{width}', props.boxArtWidth)
        .replace('{height}', props.boxArtHeight);
});
console.log(formattedBoxArtUrl,props)


</script>




<template>
    <div class="flex flex-col justify-center items-center">
        <div class="bg-red-700 flex flex-col relative" >
                <video :src="props.videoUrl" class="w-72 md:w-96" controls></video>
        </div>

        <div class="bg-blue-700 mt-10">
            <div class="bg-green-700 w-full flex flex-row">
                <div class="bg-red-700 w-1/4"></div>
                <p>szoihrziorhizhrozhrz</p>
               
            </div>
        </div>

   
    </div>
</template>