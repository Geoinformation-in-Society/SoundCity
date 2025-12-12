<template>
  <div class="flex h-screen bg-gray-50">
    <FilterSidebar />
    <div class="flex-1 flex flex-col">
      <MapView />
    </div>
  </div>
</template>

<script setup>
import FilterSidebar from '@/components/FilterSidebar.vue'
import MapView from '@/components/MapView.vue'
</script>