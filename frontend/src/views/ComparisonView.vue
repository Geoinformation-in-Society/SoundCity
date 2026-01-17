<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-800">⚖️ Compare Neighborhoods</h1>
            <p class="text-sm text-gray-600 mt-1">📊 Compare environmental indicators side-by-side</p>
          </div>
          <button
            @click="$router.push('/')"
            class="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
            Back to Map
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Neighborhood Selectors -->
      <div class="relative grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <!-- First Neighborhood Selector -->
        <div class="bg-white rounded-xl shadow-sm border p-6">
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            🏘️ First Neighborhood
          </label>
          <select
            v-model="selectedNeighborhood1"
            @change="onNeighborhoodSelect"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-800"
          >
            <option value="">Select a neighborhood...</option>
            <option
              v-for="neighborhood in availableNeighborhoods1"
              :key="neighborhood.id"
              :value="neighborhood.id"
            >
              {{ neighborhood.name }}
            </option>
          </select>
          
          <!-- Selected Neighborhood 1 Preview -->
          <div v-if="neighborhood1" class="mt-4 p-4 bg-emerald-50 rounded-lg">
            <div class="flex items-center justify-between mb-2">
              <span class="text-2xl font-bold text-emerald-700">{{ neighborhood1.livability_score }}/10</span>
              <span class="text-xs text-emerald-600 font-medium">✨ Livability Score</span>
            </div>
            <div class="text-xs text-gray-600 mb-3">{{ neighborhood1.name }}</div>
            
            <!-- Quick Actions -->
            <div class="flex gap-2">
              <button
                @click="$router.push(`/neighborhood/${neighborhood1.id}`)"
                class="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-medium rounded-lg transition"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Details
              </button>
              <button
                @click="$router.push('/')"
                class="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-white hover:bg-gray-50 text-emerald-700 text-xs font-medium rounded-lg border border-emerald-600 transition"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
                </svg>
                Map
              </button>
            </div>
          </div>
        </div>

        <!-- Swap Button -->
        <div v-if="selectedNeighborhood1 && selectedNeighborhood2" class="hidden md:flex absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-10">
          <button
            @click="swapNeighborhoods"
            class="group bg-white hover:bg-gray-50 shadow-lg border-2 border-gray-200 rounded-full p-3 transition-all duration-200 hover:shadow-xl hover:border-emerald-500"
            title="Swap neighborhoods"
          >
            <svg class="w-6 h-6 text-gray-600 group-hover:text-emerald-600 group-disabled:text-gray-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4M16 17H4m0 0l4 4m-4-4l4-4"/>
            </svg>
          </button>
        </div>

        <!-- Mobile Swap Button -->
        <div v-if="selectedNeighborhood1 && selectedNeighborhood2" class="md:hidden flex justify-center -my-3">
          <button
            @click="swapNeighborhoods"
            class="flex items-center gap-2 px-4 py-2 bg-white hover:bg-gray-50 shadow-md border border-gray-200 rounded-lg transition-all duration-200 hover:border-emerald-500"
          >
            <svg class="w-5 h-5 text-gray-600 group-hover:text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4M16 17H4m0 0l4 4m-4-4l4-4"/>
            </svg>
            <span class="text-sm font-medium text-gray-700">Swap</span>
          </button>
        </div>

        <!-- Second Neighborhood Selector -->
        <div class="bg-white rounded-xl shadow-sm border p-6">
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            🏘️ Second Neighborhood
          </label>
          <select
            v-model="selectedNeighborhood2"
            @change="onNeighborhoodSelect"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800"
          >
            <option value="">Select a neighborhood...</option>
            <option
              v-for="neighborhood in availableNeighborhoods2"
              :key="neighborhood.id"
              :value="neighborhood.id"
            >
              {{ neighborhood.name }}
            </option>
          </select>
          
          <!-- Selected Neighborhood 2 Preview -->
          <div v-if="neighborhood2" class="mt-4 p-4 bg-blue-50 rounded-lg">
            <div class="flex items-center justify-between mb-2">
              <span class="text-2xl font-bold text-blue-700">{{ neighborhood2.livability_score }}/10</span>
              <span class="text-xs text-blue-600 font-medium">✨ Livability Score</span>
            </div>
            <div class="text-xs text-gray-600 mb-3">{{ neighborhood2.name }}</div>
            
            <!-- Quick Actions -->
            <div class="flex gap-2">
              <button
                @click="$router.push(`/neighborhood/${neighborhood2.id}`)"
                class="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium rounded-lg transition"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Details
              </button>
              <button
                @click="$router.push('/')"
                class="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-white hover:bg-gray-50 text-blue-700 text-xs font-medium rounded-lg border border-blue-600 transition"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
                </svg>
                Map
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Comparison Results -->
      <div v-if="loading" class="bg-white rounded-xl shadow-sm border p-12 text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mb-4"></div>
        <h3 class="text-lg font-semibold text-gray-800 mb-2">⏳ Loading Comparison...</h3>
        <p class="text-gray-600">🔄 Calculating livability scores with current weights</p>
      </div>

      <div v-else-if="neighborhood1 && neighborhood2" class="space-y-6">
        <!-- Overall Score Comparison -->
        <div class="bg-white rounded-xl shadow-sm border p-6">
          <h2 class="text-lg font-bold text-gray-800 mb-4">🏆 Overall Livability Score</h2>
          <div class="flex items-center gap-8">
            <div class="flex-1">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-gray-700">{{ neighborhood1.name }}</span>
                <span class="text-2xl font-bold text-emerald-600">{{ neighborhood1.livability_score }}</span>
              </div>
              <div class="h-4 bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full bg-emerald-500 transition-all duration-500"
                  :style="{ width: `${(neighborhood1.livability_score / 10) * 100}%` }"
                ></div>
              </div>
            </div>
            
            <div class="flex-1">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-gray-700">{{ neighborhood2.name }}</span>
                <span class="text-2xl font-bold text-blue-600">{{ neighborhood2.livability_score }}</span>
              </div>
              <div class="h-4 bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full bg-blue-500 transition-all duration-500"
                  :style="{ width: `${(neighborhood2.livability_score / 10) * 100}%` }"
                ></div>
              </div>
            </div>
          </div>
          
          <!-- Winner Badge -->
          <div class="mt-4 p-3 bg-gray-50 rounded-lg text-center">
            <span class="text-sm text-gray-600">
              🎯 <span :class="winnerClass" class="font-bold">{{ winner }}</span>
              has a {{ scoreDifference }} point ({{ scorePercentDiff }}%) {{ scoreDifference == 1 ? 'advantage' : 'lead' }}
            </span>
          </div>
        </div>

        <!-- Environmental Indicators Comparison -->
        <div class="bg-white rounded-xl shadow-sm border p-6">
          <h2 class="text-lg font-bold text-gray-800 mb-6">🌍 Environmental Indicators</h2>
          
          <div class="space-y-6">
            <!-- Air Quality -->
            <ComparisonIndicator
              emoji="💨"
              label="Air Quality"
              :value1="neighborhood1.air_quality"
              :value2="neighborhood2.air_quality"
              :name1="neighborhood1.name"
              :name2="neighborhood2.name"
            />
            
            <!-- Noise Level -->
            <ComparisonIndicator
              emoji="🔊"
              label="Noise Level"
              :value1="neighborhood1.noise_level"
              :value2="neighborhood2.noise_level"
              :name1="neighborhood1.name"
              :name2="neighborhood2.name"
            />
            
            <!-- Green Spaces -->
            <ComparisonIndicator
              emoji="🌳"
              label="Green Spaces"
              :value1="neighborhood1.green_space"
              :value2="neighborhood2.green_space"
              :name1="neighborhood1.name"
              :name2="neighborhood2.name"
            />
            
            <!-- Tree Greenness -->
            <ComparisonIndicator
              emoji="🌲"
              label="Tree Greenness"
              :value1="neighborhood1.tree_greenness"
              :value2="neighborhood2.tree_greenness"
              :name1="neighborhood1.name"
              :name2="neighborhood2.name"
            />
            
            <!-- Urban Heat -->
            <ComparisonIndicator
              emoji="🌡️"
              label="Urban Heat"
              :value1="neighborhood1.urban_heat"
              :value2="neighborhood2.urban_heat"
              :name1="neighborhood1.name"
              :name2="neighborhood2.name"
            />
          </div>
        </div>

        <!-- Visual Radar Chart -->
        <div class="bg-white rounded-xl shadow-sm border p-6">
          <h2 class="text-lg font-bold text-gray-800 mb-4">📈 Visual Comparison</h2>
          <div class="flex justify-center">
            <div class="w-full max-w-2xl">
              <RadarChart :datasets="radarDatasets" />
            </div>
          </div>
        </div>

        <!-- Summary -->
        <div class="bg-gradient-to-br from-emerald-50 to-blue-50 rounded-xl shadow-sm border p-6">
          <h2 class="text-lg font-bold text-gray-800 mb-4">📊 Comparison Summary</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-white rounded-lg p-4">
              <div class="text-sm font-semibold text-emerald-700 mb-2">💪 {{ neighborhood1.name }} Strengths</div>
              <ul class="text-sm text-gray-700 space-y-1">
                <li v-for="strength in getStrengths(neighborhood1, neighborhood2)" :key="strength">
                  ✓ {{ strength }}
                </li>
              </ul>
            </div>
            <div class="bg-white rounded-lg p-4">
              <div class="text-sm font-semibold text-blue-700 mb-2">💪 {{ neighborhood2.name }} Strengths</div>
              <ul class="text-sm text-gray-700 space-y-1">
                <li v-for="strength in getStrengths(neighborhood2, neighborhood1)" :key="strength">
                  ✓ {{ strength }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!selectedNeighborhood1 || !selectedNeighborhood2" class="bg-white rounded-xl shadow-sm border p-12 text-center">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-lg font-semibold text-gray-800 mb-2">Select Two Neighborhoods to Compare</h3>
        <p class="text-gray-600">Choose neighborhoods from the dropdowns above to see a detailed comparison</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-white rounded-xl shadow-sm border p-12 text-center">
        <div class="text-6xl mb-4">⚠️</div>
        <h3 class="text-lg font-semibold text-gray-800 mb-2">Failed to Load Comparison</h3>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <button
          @click="fetchComparison"
          class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition"
        >
          Try Again
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, h } from 'vue'
import { useNeighborhoodStore } from '@/stores/neighborhoods'
import api from '@/services/api'
import RadarChart from '@/components/RadarChart.vue'

// Comparison Indicator Component
const ComparisonIndicator = (props) => {
  const difference = Math.abs(props.value1 - props.value2)
  const percentDiff = props.value1 > 0 || props.value2 > 0 
    ? ((difference / Math.max(props.value1, props.value2)) * 100).toFixed(0)
    : 0
  
  const diffText = difference === 0 
    ? 'No difference'
    : props.value1 > props.value2
      ? `↑ ${percentDiff}% better`
      : `↓ ${percentDiff}% lower`
  
  const diffColor = difference === 0
    ? 'text-gray-500'
    : props.value1 > props.value2
      ? 'text-emerald-600'
      : 'text-blue-600'
  
  return h('div', { class: 'border-b pb-4 last:border-b-0' }, [
    h('div', { class: 'flex items-center justify-between mb-3' }, [
      h('div', { class: 'flex items-center gap-2' }, [
        h('span', { class: 'text-xl' }, props.emoji),
        h('span', { class: 'font-semibold text-gray-800' }, props.label)
      ]),
      h('div', { class: `text-xs font-semibold px-2 py-1 rounded ${diffColor} bg-opacity-10` }, diffText)
    ]),
    h('div', { class: 'grid grid-cols-2 gap-4' }, [
      // First neighborhood
      h('div', {}, [
        h('div', { class: 'flex items-center justify-between mb-1' }, [
          h('span', { class: 'text-xs text-gray-600' }, props.name1),
          h('span', { 
            class: `text-sm font-bold ${props.value1 > props.value2 ? 'text-emerald-600' : props.value1 === props.value2 ? 'text-gray-700' : 'text-gray-600'}` 
          }, `${props.value1}/5`)
        ]),
        h('div', { class: 'flex gap-0.5' }, 
          Array.from({ length: 5 }, (_, i) => 
            h('div', { 
              class: `flex-1 h-2 rounded-sm ${i < Math.round(props.value1) ? 'bg-emerald-500' : 'bg-gray-200'}` 
            })
          )
        )
      ]),
      // Second neighborhood
      h('div', {}, [
        h('div', { class: 'flex items-center justify-between mb-1' }, [
          h('span', { class: 'text-xs text-gray-600' }, props.name2),
          h('span', { 
            class: `text-sm font-bold ${props.value2 > props.value1 ? 'text-blue-600' : props.value1 === props.value2 ? 'text-gray-700' : 'text-gray-600'}` 
          }, `${props.value2}/5`)
        ]),
        h('div', { class: 'flex gap-0.5' }, 
          Array.from({ length: 5 }, (_, i) => 
            h('div', { 
              class: `flex-1 h-2 rounded-sm ${i < Math.round(props.value2) ? 'bg-blue-500' : 'bg-gray-200'}` 
            })
          )
        )
      ])
    ])
  ])
}

ComparisonIndicator.props = ['emoji', 'label', 'value1', 'value2', 'name1', 'name2']

const store = useNeighborhoodStore()

const selectedNeighborhood1 = ref('')
const selectedNeighborhood2 = ref('')
const comparisonData = ref(null)
const loading = ref(false)
const error = ref(null)

// Swap neighborhoods function
const swapNeighborhoods = () => {
  const temp = selectedNeighborhood1.value
  selectedNeighborhood1.value = selectedNeighborhood2.value
  selectedNeighborhood2.value = temp
  
  // Re-fetch comparison with swapped values
  if (selectedNeighborhood1.value && selectedNeighborhood2.value) {
    fetchComparison()
  }
}

// Get neighborhoods from store for display
const neighborhood1 = computed(() => {
  if (!comparisonData.value) return null
  return comparisonData.value.neighborhood1
})

const neighborhood2 = computed(() => {
  if (!comparisonData.value) return null
  return comparisonData.value.neighborhood2
})

// Available neighborhoods (exclude the selected one from the other dropdown)
const availableNeighborhoods1 = computed(() => {
  return store.neighborhoods.filter(n => n.id !== selectedNeighborhood2.value)
})

const availableNeighborhoods2 = computed(() => {
  return store.neighborhoods.filter(n => n.id !== selectedNeighborhood1.value)
})

// Winner calculation from API response
const winner = computed(() => {
  if (!comparisonData.value) return ''
  return comparisonData.value.winner
})

const winnerClass = computed(() => {
  if (!comparisonData.value || !neighborhood1.value || !neighborhood2.value) return ''
  return winner.value === neighborhood1.value.name ? 'text-emerald-600' : 'text-blue-600'
})

const scoreDifference = computed(() => {
  if (!neighborhood1.value || !neighborhood2.value) return 0
  return Math.abs(neighborhood1.value.livability_score - neighborhood2.value.livability_score).toFixed(1)
})

const scorePercentDiff = computed(() => {
  if (!neighborhood1.value || !neighborhood2.value) return 0
  const maxScore = Math.max(neighborhood1.value.livability_score, neighborhood2.value.livability_score)
  if (maxScore === 0) return 0
  const diff = Math.abs(neighborhood1.value.livability_score - neighborhood2.value.livability_score)
  return ((diff / maxScore) * 100).toFixed(0)
})

// Radar chart datasets
const radarDatasets = computed(() => {
  if (!neighborhood1.value || !neighborhood2.value) return []
  
  return [
    {
      label: neighborhood1.value.name,
      data: [
        neighborhood1.value.air_quality,
        neighborhood1.value.noise_level,
        neighborhood1.value.green_space,
        neighborhood1.value.tree_greenness,
        neighborhood1.value.urban_heat
      ],
      color: '#10b981' // emerald-500
    },
    {
      label: neighborhood2.value.name,
      data: [
        neighborhood2.value.air_quality,
        neighborhood2.value.noise_level,
        neighborhood2.value.green_space,
        neighborhood2.value.tree_greenness,
        neighborhood2.value.urban_heat
      ],
      color: '#3b82f6' // blue-500
    }
  ]
})

// Fetch comparison data from API
const fetchComparison = async () => {
  if (!selectedNeighborhood1.value || !selectedNeighborhood2.value) {
    comparisonData.value = null
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await api.compareNeighborhoods(
      selectedNeighborhood1.value,
      selectedNeighborhood2.value,
      store.normalizedWeights
    )

    comparisonData.value = response.data
  } catch (err) {
    error.value = 'Failed to load comparison data'
    console.error('Comparison error:', err)
  } finally {
    loading.value = false
  }
}

// Get strengths for a neighborhood
const getStrengths = (neighborhood, comparison) => {
  const strengths = []
  
  const indicators = [
    { key: 'air_quality', label: 'Better air quality' },
    { key: 'noise_level', label: 'Quieter environment' },
    { key: 'green_space', label: 'More green spaces' },
    { key: 'tree_greenness', label: 'Greener tree coverage' },
    { key: 'urban_heat', label: 'Cooler temperatures' }
  ]
  
  indicators.forEach(indicator => {
    if (neighborhood[indicator.key] > comparison[indicator.key]) {
      strengths.push(indicator.label)
    }
  })
  
  if (strengths.length === 0) {
    strengths.push('Competitive overall score')
  }
  
  return strengths
}

// Event handlers
const onNeighborhoodSelect = () => {
  fetchComparison()
}

// Watch for weight changes in store
watch(() => store.weights, () => {
  if (selectedNeighborhood1.value && selectedNeighborhood2.value) {
    fetchComparison()
  }
}, { deep: true })

// Lifecycle
onMounted(async () => {
  if (!store.hasData) {
    await store.fetchNeighborhoods()
  }
})
</script>

<style scoped>
select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}
</style>
