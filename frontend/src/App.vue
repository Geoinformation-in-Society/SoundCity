<template>
  <div id="app">
    <NavBar />
    <RouterView />
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import { RouterView } from 'vue-router'
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>