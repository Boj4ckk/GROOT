<script setup>
    import { useTwitokStore } from '@/store/twitokStore';
    import redirectionLink from './redirectionLink.vue';
    import { useRouter } from 'vue-router';
    import { computed, ref } from 'vue';
    import { defineProps } from 'vue';

    const router = useRouter() 
    const twitokstore = useTwitokStore()

    const logout = () => {
    router.push("/login")
    }
    const connected = computed(() => twitokstore.authorizedConnection)
    

    const props = defineProps({
        to: {
            type : String,
            required : true
        },
        backgroundColor:{
            type: String,
            default: 'bg-white'

        },
        borderColor:{
            type: String,
            default: 'border-black'
        },
        textColor:{
            type:String,
            default: 'text-black'
        },
        buttonSize:{
            type:String,
            default:"sm"
        }

    })

    const sizeClasses = computed(() =>{
        const sizes = {
             sm: 'w-[64px] h-[22px] md:w-[96px] md:h-[31px] text-sm md:text-base',      // PETITE
             md: 'w-[120px] h-[35px] md:w-[260px] md:h-[60px] text-base md:text-lg ', // TON DESIGN (défaut)
             lg: 'w-72 h-20 md:w-96 md:h-24 text-lg md:text-xl',        // GRANDE  
             xl: 'w-80 h-24 md:w-[450px] md:h-28 text-xl md:text-2xl'   // TRÈS GRANDE
        };
        return sizes[props.buttonSize] || sizes.md;
     }
    )

</script>



<template>
   <router-link :to="to" class="no-underline font-inter text-base font-medium text-gray-900 flex justify-center items-center">
    <div class=" 
   
    text-xs sm:text-sm md:text-base 
    rounded-full  border-1 border-black 
    flex justify-center items-center 
    transform transition-transform duration-300 hover:scale-105 

    "
    :class="[backgroundColor, borderColor, textColor, sizeClasses]">
        <slot></slot>
        <input v-if="connected" type="submit" @click="logout" value="Logout">
    </div>
    </router-link>
    

</template>