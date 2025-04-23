<script setup>


import { useTwitokStore } from '@/store/twitokStore';

import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const TwitokStore = useTwitokStore() // import store
const router = useRouter() // import router to redirect into tiktok page after editing


// retrieve clips url fetched in studio page
const objet_clipsUrls = TwitokStore.clipsUrls_Returned  
const clipsUrls = objet_clipsUrls["clipsUrls"] 
console.log("clipsUrls : ", clipsUrls)

//clips var which will dynamicly store clips to edit.
const clips = ref([])

//Dynamicly store the clicked index of the clip (current clip to edit)
const selectedClipIndex = ref(null);

//Dynamicly store edited clips.
const edited_clip = ref([])

//Dynamcly store the current video (video displayed in the leftside of the webpage)

//Editing choices
const webcam_detection = ref(false);//Dynamicly store the editing choice for the webcam detection.
const clip_format = ref("portrait")//Dynamcly store the clip_format for editing.

// function to retrieve clips for their stored urls.
const getClips = async () => {
   
    try {
        for (let url of clipsUrls) {
        
            console.log("envoi de la requete pour aller chercher la vidéo, nom vidéo : ", url)
            clips.value.push(`http://127.0.0.1:5000/api/clips/${url}`)
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

// Getter/ Setter - for current video to edit(displayed in the left side of the web page)
function set_preview_video(video) { //SETTER
    preview_video.value = video;
}

function get_preview_video(){ //GETTER
    return preview_video.value;
}

//Handle the click on one displayed clip the select it and his index.
const handleVideoClip = (video,index) => {
    set_preview_video(video);
    selectedClipIndex.value = index
   
};
// Handle submit clip after chosing preferences for editing.
const handleClipSubmit = () => {
    
    clips.value.splice(selectedClipIndex.value,1)//remove the sumbited clip from the non-editing clips liste (right side of the page carousel)
    set_preview_video(clips.value[0])//automaticaly set a new clips for the selected clips.    
}

// handle sumbit form
const handleform = async () => {
    // prepare payload (clip to edit and preferences to pass to videoProcessor to edit)
    
    const payload = {
        webcam_detection : webcam_detection.value,
        clip_format : clip_format.value,
        clip_path : get_preview_video()
    }; 
    console.log(payload)
    try{
      
        handleClipSubmit() // call the handlesubmit to update the dynamic state of refs.
        console.log("after handleSubmit")
        const response = await axios.post("http://127.0.0.1:5000/api/process_clip", payload)
        //retrive edited clips urls.
        console.log("after response")
        const data = await response.json();
        TwitokStore.setEditedClipUrl(data)
        if(clips.value.length == 0){
            router.push('/tiktokPost') // if all the avalaible clips have been submtied, redirect to 'Studio' (faut changer par la page post sur tiktok quand on l'aura)
        }
        console.log("Changement de twitokStore.already_upload, tentative pour avoir les bons nombre de clips...")
        TwitokStore.setAlreadyUpload()
        console.log("twitokStore.editedClipsUrl : ",TwitokStore.editedClipsUrl)
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
            <video :src="preview_video"  controls class="preview_video"></video>

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