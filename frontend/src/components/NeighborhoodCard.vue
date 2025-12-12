<template>
  <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
    <!-- Header -->
    <div class="flex items-start justify-between mb-4">
      <div>
        <h3 class="text-xl font-bold text-gray-800">{{ neighborhood.name }}</h3>
        <p class="text-sm text-gray-500">{{ neighborhood.id }}</p>
      </div>
      <div
        class="px-4 py-2 rounded-full text-white font-bold text-lg"
        :style="{ backgroundColor: scoreColor }"
      >
        {{ neighborhood.livability_score }}
      </div>
    </div>

    <!-- Scores -->
    <div class="space-y-3 mb-4">
      <div class="flex items-center justify-between">
        <span class="text-gray-700 flex items-center gap-2">
          <span>💨</span>
          <span>Air Quality</span>
        </span>
        <div class="flex gap-1">
          <span
            v-for="n in 5"
            :key="n"
            class="text-lg"
            :class="n <= Math.round(neighborhood.air_quality) ? 'text-emerald-500' : 'text-gray-300'"
          >
            ★
          </span>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <span class="text-gray-700 flex items-center gap-2">
          <span>🔊</span>
          <span>Noise Level</span>
        </span>
        <div class="flex gap-1">
          <span
            v-for="n in 5"
            :key="n"
            class="text-lg"
            :class="n <= Math.round(neighborhood.noise_level) ? 'text-emerald-500' : 'text-gray-300'"
          >
            ★
          </span>
        </div>
      </div>
    </div>

    <!-- Action Button -->
    <button
      @click="$emit('view-details', neighborhood.id)"
      class="w-full bg-emerald-600 text-white py-2 rounded-lg hover:bg-emerald-700 transition font-medium"
    >
      View Details
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  neighborhood: {
    type: Object,
    required: true
  }
})

defineEmits(['view-details'])

const scoreColor = computed(() => {
  const score = props.neighborhood.livability_score
  if (score >= 8.0) return '#4ade80'
  if (score >= 6.0) return '#fbbf24'
  return '#f87171'
})
</script>