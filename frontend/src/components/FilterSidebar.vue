<template>
  <div class="w-80 bg-white shadow-lg p-6 overflow-y-auto border-r">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Filters</h2>

    <div class="space-y-4 mb-8">
      <div class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition">
        <input
          id="air-filter"
          type="checkbox"
          v-model="localFilters.airQuality"
          class="w-5 h-5 text-emerald-600 rounded focus:ring-emerald-500"
        />
        <label for="air-filter" class="text-gray-700 font-medium cursor-pointer flex-1">
          💨 Air Quality (PM2.5)
        </label>
      </div>

      <div class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition">
        <input
          id="noise-filter"
          type="checkbox"
          v-model="localFilters.noise"
          class="w-5 h-5 text-emerald-600 rounded focus:ring-emerald-500"
        />
        <label for="noise-filter" class="text-gray-700 font-medium cursor-pointer flex-1">
          🔊 Noise Pollution
        </label>
      </div>
    </div>

    <div class="border-t pt-6">
      <h3 class="font-semibold text-gray-800 mb-4">Weight Each Factor</h3>

      <div class="mb-6">
        <div class="flex justify-between text-sm text-gray-600 mb-2">
          <span>💨 Air Quality</span>
          <span class="font-semibold text-emerald-600">{{ localWeights.air }}%</span>
        </div>
        <input
          type="range"
          min="0"
          max="100"
          v-model.number="localWeights.air"
          @input="updateNoiseWeight"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
        />
      </div>

      <div class="mb-6">
        <div class="flex justify-between text-sm text-gray-600 mb-2">
          <span>🔊 Noise Level</span>
          <span class="font-semibold text-emerald-600">{{ localWeights.noise }}%</span>
        </div>
        <input
          type="range"
          min="0"
          max="100"
          v-model.number="localWeights.noise"
          @input="updateAirWeight"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
        />
      </div>

      <p class="text-xs text-gray-500 mb-4">
        💡 Tip: Weights are automatically balanced to sum to 100%
      </p>
    </div>

    <div class="flex gap-3 mt-6">
      <button
        @click="applyFilters"
        :disabled="store.loading"
        class="flex-1 bg-emerald-600 text-white py-3 rounded-lg hover:bg-emerald-700 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ store.loading ? 'Loading...' : 'Apply' }}
      </button>
      <button
        @click="resetFilters"
        :disabled="store.loading"
        class="flex-1 border-2 border-gray-300 text-gray-700 py-3 rounded-lg hover:bg-gray-50 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Reset
      </button>
    </div>

    <div v-if="store.loading" class="mt-4 text-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
      <p class="text-sm text-gray-600 mt-2">Updating scores...</p>
    </div>

    <div v-if="store.error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
      <p class="text-sm text-red-600">{{ store.error }}</p>
      <button
        @click="store.clearError"
        class="text-xs text-red-700 underline mt-1"
      >
        Dismiss
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useNeighborhoodStore } from '@/stores/neighborhoods'

const store = useNeighborhoodStore()

// Local state for filters
const localFilters = ref({ ...store.filters })
const localWeights = ref({ ...store.weights })

// Keep weights balanced (sum to 100)
const updateNoiseWeight = () => {
  localWeights.value.noise = 100 - localWeights.value.air
}

const updateAirWeight = () => {
  localWeights.value.air = 100 - localWeights.value.noise
}

// Apply filters
const applyFilters = async () => {
  store.updateFilters(localFilters.value)
  await store.updateWeights(localWeights.value.air, localWeights.value.noise)
}

// Reset to defaults
const resetFilters = async () => {
  localFilters.value = { airQuality: true, noise: true }
  localWeights.value = { air: 50, noise: 50 }
  store.updateFilters(localFilters.value)
  await store.resetWeights()
}

// Sync with store changes
watch(
  () => store.weights,
  (newWeights) => {
    localWeights.value = { ...newWeights }
  },
  { deep: true }
)
</script>