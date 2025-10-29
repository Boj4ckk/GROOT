<script setup>
import { useTwitokStore } from '@/store/twitokStore';
import axios from 'axios';
import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import StudioHeader from '../../components/studioHeader.vue';
import PreviewVideo from '@/components/previewVideo.vue';
import InQueuVideo from '@/components/inQueuVideo.vue';

const TwitokStore = useTwitokStore();
const router = useRouter();

const clips = ref([]);
const selectedClipIndex = ref(0);

const preview_video = ref('');
const preview_view_count = ref('');
const preview_date = ref('');
const preview_title = ref('');
const preview_broadcaster_name = ref('');
const preview_box_art_url = ref('');

const webcam_detection = ref(false);
const clip_format = ref("portrait");

const clipsInQueue = computed(() => TwitokStore.clipsUrls_Returned || []);

const fetchAllBoxArtsAndUpdateStore = async (clipsToUpdate) => {
    if (!clipsToUpdate || clipsToUpdate.length === 0 || (clipsToUpdate[0] && clipsToUpdate[0].box_art_url !== undefined)) {
        return;
    }

    console.log("Fetching box arts for all clips...");
    const clipsWithBoxArt = await Promise.all(
        clipsToUpdate.map(async (clip) => {
            if (clip.game_id) {
                try {
                    const response = await axios.get(`/games/${clip.game_id}/box_art`);
                    return { ...clip, box_art_url: response.data.box_art_url };
                } catch (error) {
                    console.error(`Error fetching box art for game ${clip.game_id}`, error);
                    return { ...clip, box_art_url: '' };
                }
            }
            return { ...clip, box_art_url: '' };
        })
    );
    
    TwitokStore.setclipsUrls_Returned(clipsWithBoxArt);
    console.log("Store updated with box arts.");
};

const handleVideoClip = (clip, index) => {
    if (!clip) {
        preview_video.value = '';
        preview_view_count.value = '';
        preview_date.value = '';
        preview_title.value = '';
        preview_broadcaster_name.value = '';
        preview_box_art_url.value = '';
        selectedClipIndex.value = -1;
        return;
    };
    preview_video.value = clip.url;
    preview_view_count.value = clip.view_count;
    preview_date.value = clip.date_creation;
    preview_title.value = clip.title;
    preview_broadcaster_name.value = clip.broadcaster_name;
    preview_box_art_url.value = clip.box_art_url;
    selectedClipIndex.value = index;
};

const initializeClips = (storeClips) => {
    if (storeClips && storeClips.length > 0) {
        clips.value = storeClips;
        handleVideoClip(storeClips[selectedClipIndex.value] || storeClips[0], selectedClipIndex.value);
        fetchAllBoxArtsAndUpdateStore(storeClips);
    } else {
        clips.value = [];
        handleVideoClip(null, -1);
    }
};

watch(
    () => TwitokStore.clipsUrls_Returned,
    (newClips) => {
        console.log("Store clips changed:", newClips);
        if (!newClips || newClips.length === 0) {
            if(router.currentRoute.value.path !== "/studio/filtrate") {
               router.push("/studio/filtrate");
            }
        } else {
            initializeClips(newClips);
        }
    },
    { deep: true, immediate: true }
);

const removeClipFromState = (clipUrl) => {
    const newIndex = selectedClipIndex.value >= clips.value.length - 1 ? clips.value.length - 2 : selectedClipIndex.value;
    const updatedClips = clips.value.filter(clip => clip.url !== clipUrl);
    TwitokStore.setclipsUrls_Returned(updatedClips);
    selectedClipIndex.value = newIndex < 0 ? 0 : newIndex;
};

const remove_clip_from_blob_storage = async (clip_path) => {
    try {
        await axios.post("/delete_file_from_blob", { url: clip_path });
    } catch (error) {
        console.error("Error deleting clip from blob storage:", error);
    }
};

const handleform = async () => {
    if (!preview_video.value) {
        console.error("No clip selected for processing");
        return;
    }

    const payload = {
        webcam_detection: webcam_detection.value,
        clip_format: clip_format.value,
        clip_path: preview_video.value
    };
    
    try {
        const clipToRemoveUrl = payload.clip_path;
        
        const response = await axios.post("/api/process_clip", payload);
        
        TwitokStore.setEditedClipUrl(response.data);
        TwitokStore.setAlreadyUpload();
        
        console.log("Processed clip successfully");

        removeClipFromState(clipToRemoveUrl);
        await remove_clip_from_blob_storage(clipToRemoveUrl);
        
        if (TwitokStore.clipsUrls_Returned.length === 0) {
            router.push('/tiktokPost');
        }
        
    } catch (error) {
        console.error("Error processing clip:", error);
    }
};
</script>

<template>
    <StudioHeader/>
    <div class="w-full mt-20 md:mt-4 lg:mt-0 lg:grid lg:grid-cols-[350px_1fr] lg:gap-5 lg:px-6">
        <aside class="hidden lg:block lg:pr-4  px-20">
            <h3 class="text-lg font-semibold mb-3">Up Next</h3>
            <div class="max-h-[80vh] overflow-y-auto space-y-3 pr-1">
                <InQueuVideo 
                    v-for="(clip, index) in clipsInQueue" 
                    :key="clip.url" 
                    :clip="clip"
                    :boxArtUrl="clip.box_art_url"
                    @click="handleVideoClip(clip, index)"
                    class="border-2 transition-all w-full"
                    :class="{'border-black px-1 py-1 rounded-md shadow-sm': index === selectedClipIndex, 'border-transparent': index !== selectedClipIndex}"
                />
            </div>
        </aside>
            <div class=" w-full">
                <PreviewVideo 
                v-if="preview_video"
                :videoUrl="preview_video" 
                :broadcasterName="preview_broadcaster_name" 
                :boxArtUrl='preview_box_art_url' 
                :viewCount="preview_view_count" 
                :creationDate="preview_date" 
                :title="preview_title"
                >   </PreviewVideo>
            
                <div class="lg:hidden bg-gray-400 h-[1px] mt-4"></div>
                
                <div class="mt-2 p-4 lg:hidden">
                    <div class="flex overflow-x-auto space-x-4 pb-4">
                        <InQueuVideo 
                            v-for="(clip, index) in clipsInQueue" 
                            :key="clip.url" 
                            :clip="clip"
                            :boxArtUrl="clip.box_art_url"
                            @click="handleVideoClip(clip, index)"
                            class="border-2"
                            :class="{'border-black rounded-md w-1/2 px-1 py-1': index === selectedClipIndex, 'border-transparent': index !== selectedClipIndex}"
                        />
                    </div>
                </div>
            </div>
            
  
    </div>
</template>
