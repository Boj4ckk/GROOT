

<template>
  <router-link :to="to" class="no-underline font-inter text-base font-medium text-gray-900 ">
    <slot></slot>
  </router-link>
</template>

<script setup>
defineProps({
  to: {
    type: String,
    required: true
  }
})
</script>