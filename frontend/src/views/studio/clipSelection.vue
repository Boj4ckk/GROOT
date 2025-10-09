<script setup>


import { useTwitokStore } from '@/store/twitokStore';

import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { watch } from 'vue'
import '../../components/studioHeader.vue'
import StudioHeader from '../../components/studioHeader.vue';

const TwitokStore = useTwitokStore() // import store
const router = useRouter() // import router to redirect into tiktok page after editing

// Create a reactive local copy of clips from store
const clips = ref([])
const selectedClipIndex = ref(0);
const edited_clip = ref([])
const preview_video = ref('');

//Editing choices
const webcam_detection = ref(false);
const clip_format = ref("portrait")

// Initialize clips from store and set up initial preview
const initializeClips = () => {
    const storeClips = TwitokStore.clipsUrls_Returned
    console.log("Store clips:", storeClips)
    
    if (storeClips && storeClips.length > 0) {
        // Create local copy with just URLs for easier manipulation
        clips.value = storeClips.map(clip => clip.url)
        selectedClipIndex.value = 0
        preview_video.value = clips.value[0]
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

// Handle clip selection
const handleVideoClip = (video, index) => {
    preview_video.value = video;
    selectedClipIndex.value = index;
};

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
    
    <div class="filtrate-container">
        <div class="video-container">
            <video 
                v-for="(clip, index) in clips" 
                :key="index" 
                :src="clip" 
                class="video" 
                :class="{ 'selected': selectedClipIndex === index }"
                @click="handleVideoClip(clip, index)"
            ></video>
        </div>

        <div class="preview-container">
            <video 
                v-if="preview_video" 
                :src="preview_video" 
                controls 
                class="preview_video"
            ></video>
            <div v-else class="no-video-message">
                <p>Aucun clip disponible</p>
            </div>

            <div class="edit_params_container">
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" v-model="webcam_detection">
                    <label class="form-check-label" for="flexSwitchCheckDefault">Web cam détection</label>
                </div>

                <div class="video_format_container">
                    <div class="video_format_container_title">
                        <h6>Video format</h6>
                    </div>
                    
                    <div class="video_format_check_container">
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1" v-model="clip_format" value="portrait" checked>
                            <label class="form-check-label" for="flexRadioDefault1">
                                portrait
                            </label>

                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" v-model="clip_format" value="landscape" checked>
                            <label class="form-check-label" for="flexRadioDefault2">
                                landscape
                            </label>
                        </div>
                    </div>

                <button 
                    type="submit" 
                    class="sumbitbutton" 
                    :disabled="!preview_video"
                    @click="handleform()"
                >
                    soumettre
                </button>
                
                
                </div>
               
                
            </div>
            
        </div>
    </div>
</template>

<style scoped>
    .filtrate-container{
        padding: 20px;
       
        display: flex;
        flex-direction: row;
        justify-content: space-between;

    }
    .video-container {
    
        display: flex;
        flex-direction: column; /* pour une disposition verticale */
        align-items: center;
        justify-content: space-between;
        height: 100%;
        width: 25%;
    }
    .video{

        padding-top: 2px;
        width: 90%;
        height: 90%;
        display: flex;
       
    }
    .preview-container{
        
        display: flex;
        width: 70%;
        padding: 10px;
       
        justify-content: space-evenly;
     
        
    }
    .preview_video{
        
        width: 50%;
        height: 50%;

    }
    .edit_params_container{
        margin-top: 70px;
        
        width: 40%;
        height: 40%;
    

    }
  
    .video_format_check_container{
        display: flex;
        justify-content: row;
        justify-content: space-evenly;
       
    }
    .video.selected {
        border: 3px solid #007bff;
        box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
    }
    
    .no-video-message {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 50%;
        height: 300px;
        background-color: #f8f9fa;
        border: 2px dashed #dee2e6;
        border-radius: 8px;
    }
    
    .sumbitbutton:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    
 
</style>