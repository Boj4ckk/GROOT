<script setup>
import { computed } from 'vue';

const props = defineProps({
    clip: {
        type: Object,
        required: true
    },
    boxArtUrl: {
        type: String,
        default: '' 
    }
});

// Ajoute un fragment de temps à l'URL pour forcer l'affichage de la 1ère image
const videoSrcWithFragment = computed(() => {
    if (!props.clip.url) return '';
    return `${props.clip.url}#t=0.1`;
});

const formattedBoxArtUrl = computed(() => {
    if (!props.boxArtUrl) {
        return '';
    }
    return props.boxArtUrl.replace('{width}', '40').replace('{height}', '54');
});
</script>

<template>
    <div class="flex-shrink-0 w-48 mr-4 cursor-pointer group">
        
        <div class="relative aspect-video bg-black rounded-md overflow-hidden">
            <video 
                :src="videoSrcWithFragment"
                class="w-full h-full object-cover" 
                preload="auto"
                muted
                playsinline
            >
                Votre navigateur ne supporte pas la balise vidéo.
            </video>
        </div>

        <div class="mt-2 flex flex-row items-start">
            <img 
                v-if="formattedBoxArtUrl" 
                :src="formattedBoxArtUrl" 
                class="w-10 h-auto rounded-sm flex-shrink-0" 
                alt="Game Box Art"
            >
            <div class="ml-2 min-w-0">
                <div class="text-sm font-medium text-white truncate" :title="props.clip.title">
                    {{ props.clip.title || 'Titre non disponible' }}
                </div>
                <div class="text-xs text-gray-400 truncate" :title="props.clip.broadcaster_name">
                    {{ props.clip.broadcaster_name || 'Streamer inconnu' }}
                </div>
            </div>
        </div>
    </div>
</template>