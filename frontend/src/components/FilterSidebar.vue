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
        
        <!-- Info Icon with Popover -->
        <div class="relative group">
          <button 
            type="button"
            class="flex items-center justify-center w-5 h-5 rounded-full bg-blue-500 text-white hover:bg-blue-600 transition-colors cursor-help"
            @click.stop
          >
            <svg class="w-3 h-3 font-bold" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
          </button>
          
          <!-- Popover Content -->
          <div class="absolute right-full top-1/2 -translate-y-1/2 mr-3 w-64 bg-white rounded-lg shadow-xl border border-gray-200 p-3 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 pointer-events-none z-[9999]">
            <div class="text-xs space-y-2">
              <div class="font-semibold text-gray-800 border-b pb-1">
                {{ indicator.label }} {{ indicator.emoji }}
              </div>
              
              <div class="flex items-center gap-2">
                <span :class="indicator.freshnessColor" class="px-2 py-0.5 rounded-full text-[10px] font-semibold">{{ indicator.freshness }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">Last Updated:</span>
                <span class="font-medium text-gray-800">{{ indicator.lastUpdated }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">Update Frequency:</span>
                <span class="font-medium text-gray-800">{{ indicator.updateFrequency }}</span>
              </div>
              
              <div class="border-t pt-2">
                <div class="text-gray-600 mb-1">Data Source:</div>
                <div class="text-gray-800">{{ indicator.dataSource }}</div>
              </div>
              
              <div class="border-t pt-2 text-[10px] text-gray-500">
                ℹ️ {{ indicator.description }}
              </div>
            </div>
            
            <!-- Arrow pointer -->
            <div class="absolute right-0 top-1/2 translate-x-full -translate-y-1/2 w-0 h-0 border-t-[6px] border-b-[6px] border-l-[6px] border-transparent border-l-white"></div>
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
          🌿 Nature & Recreation
        </button>
        <button
          @click="applyPreset('climateResilience')"
          class="text-xs py-2 px-3 rounded bg-gray-100 hover:bg-gray-200 transition font-medium"
        >
          🌳 Climate Resilience
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

// Define all livability indicators
const indicators = [
  { 
    id: 'air', 
    label: 'Air Quality', 
    emoji: '💨', 
    description: 'PM2.5 and pollutants measurement',
    freshness: 'Live',
    freshnessColor: 'bg-green-500 text-white',
    lastUpdated: 'Real-time',
    updateFrequency: 'Hourly',
    dataSource: 'LUQS NRW stations + Sensor.Community'
  },
  { 
    id: 'noise', 
    label: 'Noise Pollution', 
    emoji: '🔊', 
    description: 'Traffic and ambient noise levels',
    freshness: 'Old',
    freshnessColor: 'bg-blue-500 text-white',
    lastUpdated: '2022',
    updateFrequency: 'Every 5 years (EU Directive)',
    dataSource: 'Lärmkartierung NRW 2022 (LANUV/Münster Open Data)'
  },
  { 
    id: 'greenSpaces', 
    label: 'Green Environment', 
    emoji: '🌳', 
    description: 'Parks, vegetation & tree coverage',
    freshness: 'Recent',
    freshnessColor: 'bg-emerald-500 text-white',
    lastUpdated: '2024',
    updateFrequency: 'Annually',
    dataSource: 'Münster Grünflächen + Baumkataster'
  },
  { 
    id: 'urbanHeat', 
    label: 'Urban Heat', 
    emoji: '🌡️', 
    description: 'Heat island resilience score',
    freshness: 'Recent',
    freshnessColor: 'bg-orange-500 text-white',
    lastUpdated: '2025',
    updateFrequency: 'On data updates',
    dataSource: 'Multi-factor UHI Model (Green Coverage + Distance + Density proxy)'
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

// Apply preset configurations
const applyPreset = async (preset) => {
  const presets = {
    balanced: {
      air: 25,
      noise: 25,
      greenSpaces: 25,
      urbanHeat: 25,
    },
    health: {
      air: 40,
      noise: 30,
      greenSpaces: 20,
      urbanHeat: 10,
    },
    nature: {
      air: 15,
      noise: 15,
      greenSpaces: 45,
      urbanHeat: 25,
    },
    climateResilience: {
      air: 15,
      noise: 10,
      greenSpaces: 35,
      urbanHeat: 40,
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