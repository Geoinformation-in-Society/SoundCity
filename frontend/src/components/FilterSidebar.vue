<template>
  <div class="w-80 bg-white shadow-lg p-6 overflow-y-auto border-r">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Livability Filters</h2>

    <!-- Filters Section -->
    <div class="space-y-3 mb-8">
      <div v-for="indicator in indicators" :key="indicator.id" class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition group relative">
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
        <!-- Data source tooltip (Issue #39 - Enhanced Metadata) -->
        <div class="relative">
          <span class="text-gray-400 text-xs cursor-help group-hover:text-gray-600 transition">ⓘ</span>
          <div class="absolute right-0 bottom-full mb-2 w-56 bg-gray-800 text-white text-xs rounded-lg p-3 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 shadow-lg">
            <div class="font-semibold mb-2 pb-1 border-b border-gray-600">{{ indicator.label }}</div>
            
            <div class="space-y-1.5">
              <div class="flex justify-between items-center">
                <span class="text-gray-400">Freshness:</span>
                <span :class="['px-1.5 py-0.5 rounded text-[10px] font-medium', indicator.freshnessColor]">{{ indicator.freshness }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-400">Last Updated:</span>
                <span class="text-white">{{ indicator.lastUpdated }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-400">Frequency:</span>
                <span class="text-white">{{ indicator.updateFrequency }}</span>
              </div>
              
              <div class="pt-1 mt-1 border-t border-gray-600">
                <span class="text-gray-400">Source:</span>
                <div class="text-white text-[10px] mt-0.5">{{ indicator.source }}</div>
              </div>
            </div>
            
            <div class="absolute top-full right-2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
          </div>
        </div>
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

    <!-- Quick Presets -->
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
          @click="applyPreset('cooling')"
          class="text-xs py-2 px-3 rounded bg-gray-100 hover:bg-gray-200 transition font-medium"
        >
          🌳 Cooling
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
import { ref, watch } from 'vue'
import { useNeighborhoodStore } from '@/stores/neighborhoods'

const store = useNeighborhoodStore()

// Define all livability indicators with full metadata (Issue #39)
const indicators = [
  { 
    id: 'air', 
    label: 'Air Quality', 
    emoji: '💨', 
    description: 'PM2.5, PM10, and NO2 pollutants',
    freshness: 'Live',
    freshnessColor: 'bg-green-500 text-white',
    lastUpdated: 'Real-time',
    updateFrequency: 'Hourly',
    source: 'LUQS NRW (LANUV) + Sensor.Community citizen science network'
  },
  { 
    id: 'noise', 
    label: 'Noise Pollution', 
    emoji: '🔊', 
    description: 'Traffic and industrial noise levels',
    freshness: 'Old',
    freshnessColor: 'bg-amber-500 text-white',
    lastUpdated: '2022',
    updateFrequency: 'Every 5 years (EU Directive)',
    source: 'Lärmkartierung NRW 2022 (LANUV/Münster Open Data)'
  },
  { 
    id: 'greenCoverage', 
    label: 'Green Coverage', 
    emoji: '🌿', 
    description: 'Green spaces + tree canopy coverage',
    freshness: 'Recent',
    freshnessColor: 'bg-blue-500 text-white',
    lastUpdated: '2024',
    updateFrequency: 'Annual updates',
    source: 'Grünflächen WFS + Baumkataster WFS (Stadt Münster Open Data)'
  },
  { 
    id: 'urbanHeat', 
    label: 'Urban Heat', 
    emoji: '🌡️', 
    description: 'Heat island resilience score',
    freshness: 'Recent',
    freshnessColor: 'bg-blue-500 text-white',
    lastUpdated: '2025',
    updateFrequency: 'On data refresh',
    source: 'Multi-factor UHI Model (Green Coverage + Distance + Density proxy)'
  }
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
    const adjustment = 100 - currentTotal
    // Only adjust indicators that can handle the adjustment
    // (i.e., those not at 0 if adjustment is negative)
    const adjustableIds = otherIds.filter(id => {
      return adjustment >= 0 || localWeights.value[id] > 0
    })
    
    if (adjustableIds.length > 0) {
      const perIndicatorAdjustment = adjustment / adjustableIds.length
      adjustableIds.forEach(id => {
        localWeights.value[id] = Math.max(0, localWeights.value[id] + perIndicatorAdjustment)
      })
    } else if (adjustment < 0) {
      // Edge case: no adjustable indicators but total > 100
      // This can happen if user set changed indicator too high and all others are at 0
      // Clamp the changed indicator to bring total to 100
      localWeights.value[changedId] = Math.max(0, localWeights.value[changedId] + adjustment)
    }
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
    // When checking, distribute weights equally among all checked indicators
    const checkedIds = indicators
      .filter(i => localFilters.value[i.id])
      .map(i => i.id)
    
    if (checkedIds.length > 0) {
      const weightPerIndicator = 100 / checkedIds.length
      indicators.forEach(i => {
        if (checkedIds.includes(i.id)) {
          localWeights.value[i.id] = weightPerIndicator
        } else {
          localWeights.value[i.id] = 0
        }
      })
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

// Apply preset configurations (now with 4 indicators)
const applyPreset = async (preset) => {
  const presets = {
    balanced: {
      air: 25,
      noise: 25,
      greenCoverage: 25,
      urbanHeat: 25,
    },
    health: {
      air: 40,
      noise: 30,
      greenCoverage: 20,
      urbanHeat: 10,
    },
    nature: {
      air: 20,
      noise: 15,
      greenCoverage: 45,
      urbanHeat: 20,
    },
    cooling: {
      air: 15,
      noise: 15,
      greenCoverage: 35,
      urbanHeat: 35,
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