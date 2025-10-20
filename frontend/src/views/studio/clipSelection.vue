<script setup>


import { useTwitokStore } from '@/store/twitokStore';

import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { watch } from 'vue'
import '../../components/studioHeader.vue'
import StudioHeader from '../../components/studioHeader.vue';
import previewVideo from '@/components/previewVideo.vue';
import PreviewVideo from '@/components/previewVideo.vue';

const TwitokStore = useTwitokStore() // import store
const router = useRouter() // import router to redirect into tiktok page after editing

// Create a reactive local copy of clips from store
const clips = ref([])
const selectedClipIndex = ref(0);
const edited_clip = ref([])


const preview_video = ref('');
const preview_view_count = ref('');
const preview_date = ref('');
const preview_title = ref('');
const preview_broadcaster_name = ref('');
const preview_game_id = ref('');
const preview_box_art_url = ref('');



//Editing choices
const webcam_detection = ref(false);
const clip_format = ref("portrait")


const fetchGameBoxArt = async (gameId)  => {
    if(!gameId){
        preview_box_art_url.value = '';
        return;
    }
    try{

        const response = await axios.get(`/games/${gameId}/box_art`);
        preview_box_art_url.value = response.data.box_art_url;

    }catch(error){
        console.error("Error fetching game box art", error)
        preview_box_art_url.value = '';
    }
}

const handleVideoClip = (clip, index) => {
    preview_video.value = clip.url;
    preview_view_count.value = clip.view_count;
    preview_date.value = clip.date_creation;
    preview_title.value = clip.title;
    preview_game_id.value = clip.game_id;
    preview_broadcaster_name.value = clip.broadcaster_name;

    selectedClipIndex.value = index;

    fetchGameBoxArt(clip.game_id)


}
// Initialize clips from store and set up initial preview
const initializeClips = () => {
    const storeClips = TwitokStore.clipsUrls_Returned
    console.log("Store clips:", storeClips)
    
    if (storeClips && storeClips.length > 0) {
        const firstClip = storeClips[0];
        handleVideoClip(firstClip, 0);
        
   
    } else {
        clips.value = []
        preview_video.value = ''
        selectedClipIndex.value = null
    }
}

// Initialize on component mount
initializeClips()

// Watch for store changes and reinitialize
watch(
    () => TwitokStore.clipsUrls_Returned,
    (newClips) => {
        console.log("Store clips changed:", newClips)
        if (!newClips || newClips.length === 0) {
            router.push("/studio/filtrate")
        } else {
            initializeClips()
        }
    },
    { deep: true }
)





// Remove clip from local state and update store
const removeClipFromState = (clipPath) => {
    // Remove from local clips array
    clips.value = clips.value.filter(clip => clip !== clipPath)
    
    // Update store with remaining clips
    const remainingClipsObjects = clips.value.map(url => ({ url }))
    TwitokStore.setclipsUrls_Returned(remainingClipsObjects)
    
    // Reassign preview video
    if (clips.value.length > 0) {
        // If current selected clip was removed, adjust index
        if (selectedClipIndex.value >= clips.value.length) {
            selectedClipIndex.value = clips.value.length - 1
        }
        preview_video.value = clips.value[selectedClipIndex.value]
    } else {
        preview_video.value = ''
        selectedClipIndex.value = null
    }
}

// Remove clip from blob storage
const remove_clip_from_blob_storage = async (clip_path) => {
    try {
        const response = await axios.post("/delete_file_from_blob", { url: clip_path })
        return response
    } catch (error) {
        console.error("Error deleting clip from blob storage:", error)
        throw error
    }
}

// Handle form submission
const handleform = async () => {
    if (!preview_video.value) {
        console.error("No clip selected for processing")
        return
    }

    const payload = {
        webcam_detection: webcam_detection.value,
        clip_format: clip_format.value,
        clip_path: preview_video.value
    };
    
    console.log("Processing payload:", payload)
    
    try {
        // Remove clip from state first
        removeClipFromState(payload.clip_path)
        
        // Remove from blob storage
        await remove_clip_from_blob_storage(payload.clip_path)
        
        // Process the clip
        const response = await axios.post("/api/process_clip", payload)
        const data = response.data // Fix: use response.data instead of response.json
        
        // Store edited clip URL
        TwitokStore.setEditedClipUrl(data)
        TwitokStore.setAlreadyUpload()
        
        console.log("Processed clip successfully")
        console.log("Edited clips URL:", TwitokStore.editedClipsUrl)
        
        // Redirect if no more clips
        if (clips.value.length === 0) {
            router.push('/tiktokPost')
        }
        
    } catch (error) {
        console.error("Error processing clip:", error)
    }
}

</script>

<template>
    <StudioHeader/>
    <div class="bg-blue-700 w-full mt-20 md:mt-1">
         <PreviewVideo :videoUrl="preview_video" :broadcasterName="preview_broadcaster_name" :boxArtUrl='preview_box_art_url' :viewCount="preview_view_count" :creationDate="preview_date" :title="preview_title" ></PreviewVideo>
    </div>
</template>

