

<script setup>
import { ref } from 'vue';
    const video_path_list = [
        "test/20250304_InnocentSillyDiamondRickroll-dzkdq1YJbq_a9FjU_source.mp4",
        "twitok_website\\src\\views\\studio\\test\\20250306_ArtsyFlaccidJellyfishPMSTwin-W-Wo2UKWga0ue4JJ_source.mp4",
        "twitok_website\\src\\views\\studio\\test\\20250307_RoundBreakableOwlLitFam-BBcfT87VFwV298kj_source.mp4",
        "twitok_website\\src\\views\\studio\\test\\20250308_HandsomeBrightSardineOMGScoots-GD4vbQ32Fl4GyGdK_source.mp4"
    ] 
    const videos = ref(video_path_list)


    const preview_video = ref(video_path_list[0]);

    function set_preview_video (video) {
        preview_video.value = video
    }

    function get_preview_video (){
        return preview_video.value
    }

    const handleVideoClip = (video) =>{
        set_preview_video(video)
        console.log("g")
       
    }
  
</script>



<template>

    <div class="filtrate-container">
        <div class="video-container">

            <video v-for="(video,index) in videos" src="..\\test\\20250304_InnocentSillyDiamondRickroll-dzkdq1YJbq_a9FjU_source.mp4" :key="index" controls class="video"  @click="handleVideoClip(video)">
               
            </video>

        </div>


        <div class="preview-container">
            <video controls >
                <source v-bind:src="get_preview_video()"  type="video/mp4">
            </video>
        </div>

    </div>
    

</template>
<style scoped>
    .filtrate-container{
        padding: 20px;
        background-color: green;
        display: flex;
        flex-direction: row;
        justify-content: space-between;

    }
    .video-container {
        background-color: red;
        display: flex;
        flex-direction: column; /* pour une disposition verticale */
        align-items: center;
        justify-content: space-between;
        height: 100%;
        width: 25%;
    }
    .video{

        padding-top: 2px;
        display: flex;
       
    }
    .preview-container{

        background-color:blue;
        width: 70%;
     
        
    }
    
 
</style>