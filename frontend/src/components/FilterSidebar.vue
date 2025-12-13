<template>
  <div class="w-80 bg-white shadow-lg p-6 overflow-y-auto border-r">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Livability Filters</h2>

    <!-- Filters Section -->
    <div class="space-y-3 mb-8">
      <div v-for="indicator in indicators" :key="indicator.id" class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition">
        <input
          :id="`filter-${indicator.id}`"
          type="checkbox"
          :checked="localFilters[indicator.id]"
          @change="onFilterChange(indicator.id, $event.target.checked)"
          class="w-5 h-5 text-emerald-600 rounded focus:ring-emerald-500"
        />
        <label :for="`filter-${indicator.id}`" class="text-gray-700 font-medium cursor-pointer flex-1">
          {{ indicator.emoji }} {{ indicator.label }}
        </label>
      </div>
    </div>

    <!-- Weight Adjustment Section -->
    <div class="border-t pt-6">
      <h3 class="font-semibold text-gray-800 mb-4">📊 Adjust Weights</h3>
      
      <!-- Weight sliders -->
      <div class="space-y-4 max-h-72 overflow-y-auto">
        <div v-for="indicator in indicators" :key="indicator.id" :class="{ 'opacity-50': !localFilters[indicator.id] }">
          <div class="flex justify-between items-center mb-2">
            <label class="text-sm font-medium" :class="localFilters[indicator.id] ? 'text-gray-700' : 'text-gray-400'">
              {{ indicator.emoji }} {{ indicator.label }}
            </label>
            <span class="text-sm font-semibold" :class="localFilters[indicator.id] ? 'text-emerald-600' : 'text-gray-400'">{{ Math.round(localWeights[indicator.id]) }}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            :value="localWeights[indicator.id]"
            @input="onWeightChange(indicator.id, $event.target.value)"
            :disabled="!localFilters[indicator.id]"
            class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-emerald-600 disabled:cursor-not-allowed disabled:opacity-50"
          />
        </div>
      </div>

      <p class="text-xs text-gray-500 mt-4 p-3 bg-blue-50 rounded">
        💡 <strong>Tip:</strong> Weights must total exactly 100% for accurate scoring. Adjust sliders—they'll rebalance automatically.
      </p>
    </div>

    <!-- Preset Presets -->
    <div class="border-t pt-6 mt-6">
      <h3 class="font-semibold text-gray-800 mb-3">🎯 Quick Presets</h3>
      <div class="grid grid-cols-2 gap-2">
        <button
          @click="applyPreset('balanced')"
          class="text-xs py-2 px-3 rounded bg-gray-100 hover:bg-gray-200 transition font-medium"
        >
          ⚖️ Balanced
        </button>
        <button
          @click="applyPreset('health')"
          class="text-xs py-2 px-3 rounded bg-gray-100 hover:bg-gray-200 transition font-medium"
        >
          💚 Health
        </button>
        <button
          @click="applyPreset('nature')"
          class="text-xs py-2 px-3 rounded bg-gray-100 hover:bg-gray-200 transition font-medium"
        >
          🌿 Nature
        </button>
        <button
          @click="applyPreset('urban')"
          class="text-xs py-2 px-3 rounded bg-gray-100 hover:bg-gray-200 transition font-medium"
        >
          🏙️ Urban
        </button>
      </div>
    </div>

    <!-- Action Buttons -->
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

    <!-- Loading State -->
    <div v-if="store.loading" class="mt-4 text-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
      <p class="text-sm text-gray-600 mt-2">Updating scores...</p>
    </div>

    <!-- Error State -->
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
import { ref, watch, computed } from 'vue'
import { useNeighborhoodStore } from '@/stores/neighborhoods'

const store = useNeighborhoodStore()

// Define all livability indicators
const indicators = [
  { id: 'air', label: 'Air Quality', emoji: '💨', description: 'PM2.5 and pollutants' },
  { id: 'noise', label: 'Noise Pollution', emoji: '🔊', description: 'Traffic and ambient noise' },
  { id: 'greenSpaces', label: 'Green Spaces', emoji: '🌳', description: 'Parks and vegetation' },
  { id: 'treeGreenness', label: 'Tree Greenness', emoji: '🌲', description: 'Tree canopy coverage' },
  { id: 'urbanHeat', label: 'Urban Heat', emoji: '🌡️', description: 'Temperature and cooling' }
]

// Local state for filters and weights
const localFilters = ref({})
const localWeights = ref({})

// Initialize from store
const initializeState = () => {
  localFilters.value = { ...store.filters }
  localWeights.value = { ...store.weights }
}

initializeState()

// Computed property for total weight
const totalWeight = computed(() => {
  return Object.values(localWeights.value).reduce((sum, val) => sum + (val || 0), 0)
})

// Weight change handler - maintains 100% total by redistributing other weights
const onWeightChange = (changedId, newValue) => {
  const numValue = parseFloat(newValue)
  const oldValue = localWeights.value[changedId]
  const difference = numValue - oldValue
  
  // Update the changed indicator
  localWeights.value[changedId] = numValue
  
  // Get other indicators
  const otherIds = indicators
    .filter(i => i.id !== changedId)
    .map(i => i.id)
  
  // Redistribute the difference proportionally from other indicators
  if (otherIds.length > 0) {
    const otherTotal = Object.entries(localWeights.value)
      .filter(([key]) => otherIds.includes(key))
      .reduce((sum, [, val]) => sum + val, 0)
    
    if (otherTotal > 0) {
      // Reduce proportionally from each other indicator
      otherIds.forEach(id => {
        const proportion = localWeights.value[id] / otherTotal
        localWeights.value[id] = Math.max(0, localWeights.value[id] - difference * proportion)
      })
    }
  }
  
  // Fine-tune to ensure exactly 100%
  const currentTotal = Object.values(localWeights.value).reduce((sum, val) => sum + val, 0)
  if (Math.abs(currentTotal - 100) > 0.01) {
    const adjustment = (100 - currentTotal) / otherIds.length
    otherIds.forEach(id => {
      localWeights.value[id] += adjustment
    })
  }
}

// Filter change handler - sets weight to 0 when unchecked, redistributes to others
const onFilterChange = (filterId, isChecked) => {
  localFilters.value[filterId] = isChecked
  
  if (!isChecked) {
    // When unchecking, set weight to 0 and redistribute
    const weightToRedistribute = localWeights.value[filterId]
    localWeights.value[filterId] = 0
    
    // Get checked indicators (excluding the one just unchecked)
    const checkedIds = indicators
      .filter(i => i.id !== filterId && localFilters.value[i.id])
      .map(i => i.id)
    
    // Redistribute the weight proportionally among checked indicators
    if (checkedIds.length > 0) {
      const weightPerIndicator = weightToRedistribute / checkedIds.length
      checkedIds.forEach(id => {
        localWeights.value[id] += weightPerIndicator
      })
    }
  } else {
    // When checking, give it equal share from other checked indicators
    const checkedIds = indicators
      .filter(i => i.id !== filterId && localFilters.value[i.id])
      .map(i => i.id)
    
    if (checkedIds.length > 0) {
      // Take 5% from each checked indicator to give to newly checked one
      const takePerIndicator = 5 / checkedIds.length
      checkedIds.forEach(id => {
        localWeights.value[id] -= takePerIndicator
      })
      localWeights.value[filterId] = 5
    } else {
      // If no other indicators checked, give it 100%
      localWeights.value[filterId] = 100
    }
  }
}

// Apply filters and weights
const applyFilters = async () => {
  store.updateFilters(localFilters.value)
  await store.updateWeights(localWeights.value)
}

// Reset to defaults
const resetFilters = async () => {
  initializeState()
  store.updateFilters(localFilters.value)
  await store.resetWeights()
}

// Apply preset configurations
const applyPreset = async (preset) => {
  const presets = {
    balanced: {
      air: 20,
      noise: 20,
      greenSpaces: 20,
      treeGreenness: 20,
      urbanHeat: 20,
    },
    health: {
      air: 35,
      noise: 25,
      greenSpaces: 15,
      treeGreenness: 15,
      urbanHeat: 10,
    },
    nature: {
      air: 20,
      noise: 12,
      greenSpaces: 35,
      treeGreenness: 25,
      urbanHeat: 8,
    },
    cooling: {
      air: 15,
      noise: 15,
      greenSpaces: 25,
      treeGreenness: 25,
      urbanHeat: 20,
    }
  }

  if (presets[preset]) {
    // Enable all indicators
    indicators.forEach(indicator => {
      localFilters.value[indicator.id] = true
    })
    // Apply preset weights
    localWeights.value = { ...presets[preset] }
    await applyFilters()
  }
}

// Sync with store changes
watch(
  () => store.weights,
  (newWeights) => {
    localWeights.value = { ...newWeights }
  },
  { deep: true }
)

watch(
  () => store.filters,
  (newFilters) => {
    localFilters.value = { ...newFilters }
  },
  { deep: true }
)
</script>

<style scoped>
input[type="range"] {
  background: linear-gradient(to right, #10b981 0%, #10b981 var(--value), #e5e7eb var(--value), #e5e7eb 100%);
}

input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #10b981;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #10b981;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>