<script setup>


import { useTwitokStore } from '@/store/twitokStore';

import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const TwitokStore = useTwitokStore() 
const router = useRouter()
const objet_clipsUrls = TwitokStore.clipsUrls_Returned
console.log("voici les urls des clips : ", objet_clipsUrls)
const clipsUrls = objet_clipsUrls["clipsUrls"]
console.log(clipsUrls)

const objet_editedClip = TwitokStore.editedClipsUrl
const editedClipUrls = objet_editedClip["editedClipUrls"]

const clips = ref([])

const selectedClipIndex = ref(null);

const edited_clip = ref([])

const getClips = async () => {
    try {
        for (let url of clipsUrls) {
        
            console.log("envoi de la requete pour aller chercher la vidéo, nom vidéo : ", url)
            clips.value.push(`http://127.0.0.1:5000/clips/${url}`)
            console.log("etat du dossier de vidéos : ", clips)
        }
    }
    catch (error) {
        console.error("erreur lorsqu'on a été cherché la vidéo finale", error)
    }
    return clips
}

getClips() 




const preview_video = ref(clips.value[0]);
const webcam_detection = ref(false);
const clip_format = ref("portrait")


function set_preview_video(video) {
    preview_video.value = video;
}

function get_preview_video(){
    return preview_video.value;
}

const handleVideoClip = (video,index) => {
    set_preview_video(video);
    selectedClipIndex.value = index
   
};

const handleClipSubmit = () => {
    edited_clip.value.push(clips.value[selectedClipIndex])
    clips.value.splice(selectedClipIndex.value,1)
    set_preview_video(clips.value[0])
    if(clips.value.length == 0){
        router.push('/studio')

    }
    
    
   


    
}

const handleform = async () => {
    const payload = {
        webcam_detection : webcam_detection.value,
        clip_format : clip_format.value,
        clip_path : get_preview_video()
    };
   
    
    try{
        
        handleClipSubmit()
        const response = await fetch("http://127.0.0.1:5000/process_clip",{
            method: "POST",
            headers :{"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log("data", data)

        

        
    }
    catch(error) {
        console.log("erreur",  error)
    }

 

    
}



</script>

<template>

    <div class="filtrate-container">

        <div class="video-container">
            <video v-for="(clip, index) in clips" :key="index" :src="clip"  class="video"  @click="handleVideoClip(clip,index)"></video>
        </div>

        <div class="preview-container">
            <video :src="get_preview_video()"  controls class="preview_video"></video>

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

                <button type="submit" class="sumbitbutton" @click="handleform()">soumettre</button>
                
                
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
    
 
</style>