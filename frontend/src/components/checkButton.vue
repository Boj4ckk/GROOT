<script setup>
import { CheckIcon} from '@heroicons/vue/24/solid';


const props = defineProps({
    checked: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:checked'])

function toggle() {
    emit('update:checked', !props.checked)
}
</script>


<template>

    <button 
        @click="toggle" 
        class="w-4 h-4 md:w-7 md:h-7 rounded-sm transform transition-transform duration-300 hover:scale-105 border border-black flex items-center justify-center aspect-square flex-shrink-0"
        :class="{'bg-black': props.checked, 'bg-white': !props.checked}">
        <CheckIcon v-if="props.checked" class="text-white w-3/4 h-3/4"></CheckIcon>
    </button>
</template>