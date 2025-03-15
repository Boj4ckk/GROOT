<script setup>
import { ref } from 'vue';

const video_path_list = [
    "\\test_clip\\20250304_InnocentSillyDiamondRickroll-dzkdq1YJbq_a9FjU_source.mp4",
    "\\test_clip\\20250306_ArtsyFlaccidJellyfishPMSTwin-W-Wo2UKWga0ue4JJ_source.mp4",
    "\\test_clip\\20250307_RoundBreakableOwlLitFam-BBcfT87VFwV298kj_source.mp4",
    "\\test_clip\\20250308_HandsomeBrightSardineOMGScoots-GD4vbQ32Fl4GyGdK_source.mp4"
];

const videos = ref(video_path_list);
const preview_video = ref(video_path_list[0]);





const webcam_detection = ref(false);
const clip_format = ref("portrait")


function set_preview_video(video) {
    preview_video.value = video;
}

function get_preview_video(){
    return preview_video.value;
}

const handleVideoClip = (video) => {
    set_preview_video(video);
   
};

const handleform = async () => {
    const payload = {
        webcam_detection : webcam_detection.value,
        clip_format : clip_format.value,
        clip_path : get_preview_video()
    };
    try{
        const response = await fetch("http://127.0.0.1:5000/process_clip",{
            method: "POST",
            headers :{"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log(data)
    }
    catch(error) {
        console.log("erreur",  error)
    }

 

    
}



</script>

<template>

    <div class="filtrate-container">

        <div class="video-container">
            <video v-for="(video, index) in videos" :key="index" :src="video"  class="video"  @click="handleVideoClip(video)"></video>
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
    .video_format_container{
        
       
    }
    .video_format_check_container{
        display: flex;
        justify-content: row;
        justify-content: space-evenly;
       
    }
    
 
</style>