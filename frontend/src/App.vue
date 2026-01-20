<template>
  <div id="app">
    <NavBar />
    <RouterView />
    <FeedbackModal />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import FeedbackModal from '@/components/FeedbackModal.vue'
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>