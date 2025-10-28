<script setup>
import { computed } from 'vue';
import deleteButton from '../components/deleteButton.vue'
import DeleteButton from '../components/deleteButton.vue';

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
        default: '68'
    },
    boxArtHeight: {
        type: [String, Number],
        default: '78' // Valeur par défaut si non fournie
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
console.log(props)

const formattedViewCount = computed(() => {
    if (props.viewCount === null || props.viewCount === undefined) return '';
    const num = props.viewCount;

    if (num < 1000) {
        return num.toString();
    } else if (num < 1000000) {
        // Format to '1k', '12.3k', '123k'
        return (num / 1000).toFixed(num % 1000 < 100 ? 0 : 1).replace('.0', '') + 'k';
    } else if (num < 1000000000) {
        // Format to '1M', '12.3M', '123M'
        return (num / 1000000).toFixed(num % 1000000 < 100000 ? 0 : 1).replace('.0', '') + 'M';
    } else {
        // Format to '1B', '12.3B', '123B'
        return (num / 1000000000).toFixed(num % 1000000000 < 100000000 ? 0 : 1).replace('.0', '') + 'B';
    }
});

const formattedCreationDate = computed(() => {
    // Si la date n'est pas valide, on ne retourne rien
    if (!props.creationDate) return '';

    try {
        const date = new Date(props.creationDate);
        // Vérifier si la date est valide après la conversion
        if (isNaN(date.getTime())) {
            return 'Date invalide';
        }

        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Les mois sont de 0 à 11
        const year = String(date.getFullYear()).slice(-2); // Récupère les 2 derniers chiffres

        return `${day}/${month}/${year}`;
    } catch (error) {
        return 'Date invalide';
    }
});

</script>




// ...existing code...
<template>
    <!-- Le conteneur principal prend toute la largeur et centre son contenu -->
    <div class="w-full flex flex-col items-center">

        <!-- Conteneur pour la vidéo et les détails -->
        <!-- C'est LUI qui doit avoir la largeur variable -->
        <div class="w-5/6 sm:w-4/5 md:w-96 flex flex-col items-center">

            <!-- Vidéo -->
            <video :src="props.videoUrl" class="w-full rounded-md" controls></video>

            <!-- Détails -->
            <div class="mt-2 w-full flex flex-row">
                <div class="w-1/6 "> <!-- Ajusté pour la nouvelle structure -->
                    <img :src="formattedBoxArtUrl" class="w-full h-full rounded-md">
                </div>
                <div class="w-5/6 min-w-0  "> <!-- Ajusté pour la nouvelle structure -->
                    <div class="px-1 font-inter text-xs sm:text-sm font-medium truncate">{{ props.title }}</div>
                    <div class="px-1 text-gray-500 font-inter text-xs sm:text-sm font-medium truncate ">{{ props.broadcasterName }}</div>
                    <div class="w-full flex flex-row items-end ">
                        <div class="flex-grow flex flex-row  px-1 items-center min-w-0 ">
                             <div class=" font-inter text-[10px] font-medium w-auto flex justify-center items-baseline text-center">
                                <div class="">{{ formattedViewCount }}</div>
                                <div class="ml-1 flex-shrink-0">views</div>
                            </div>
                            <div class="ml-2  font-inter text-[10px] font-medium flex justify-center items-center h-5/6  pt-1">{{ formattedCreationDate }}</div>
                        </div>
                        <DeleteButton></DeleteButton>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>