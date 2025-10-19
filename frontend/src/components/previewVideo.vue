

<script setup>
import { computed } from 'vue';

const props = defineProps({
    videoUrl:{
        type: String,
        required:true
    },
    
  
})

const formattedDuration = computed(() => {
  if (props.videoDuration == null) return '00:00';

  const totalSeconds = Math.floor(props.videoDuration);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  // Ajoute un '0' devant si le nombre est inférieur à 10
  const paddedMinutes = String(minutes).padStart(2, '0');
  const paddedSeconds = String(seconds).padStart(2, '0');

  return `${paddedMinutes}:${paddedSeconds}`;
});

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