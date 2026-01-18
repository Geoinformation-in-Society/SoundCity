<template>
  <div class="min-h-screen bg-gray-50 pb-12">
    <!-- Loading State -->
    <div v-if="store.loading" class="flex items-center justify-center h-screen">
      <div class="text-center">
        <div class="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-600 mb-4"></div>
        <p class="text-gray-700 font-medium">Loading neighborhood details...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="store.error" class="flex items-center justify-center h-screen">
      <div class="text-center max-w-md">
        <div class="text-6xl mb-4">😕</div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">Oops! Something went wrong</h2>
        <p class="text-gray-600 mb-4">{{ store.error }}</p>
        <button
          @click="router.push('/')"
          class="bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition"
        >
          Back to Map
        </button>
      </div>
    </div>

    <!-- Content -->
    <div v-else-if="neighborhood">
      <!-- Header -->
      <div class="bg-gradient-to-r from-emerald-600 to-emerald-700 text-white px-8 py-12 shadow-lg">
        <div class="max-w-6xl mx-auto">
          <button
            @click="router.push('/')"
            class="flex items-center gap-2 text-emerald-100 hover:text-white mb-4 transition"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to Map
          </button>
          <h1 class="text-4xl font-bold mb-2">{{ neighborhood.name }}</h1>
          <div class="flex items-center gap-4">
            <span class="text-emerald-100 text-lg">Münster, Germany</span>
            <span class="text-emerald-100 text-lg">•</span>
            <span class="text-emerald-100 text-lg">Overall Score: {{ neighborhood.livability_score }}/10</span>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="max-w-6xl mx-auto px-8 -mt-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Left Column: Scores -->
          <div class="bg-white rounded-2xl shadow-xl p-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">📊 Livability Breakdown</h2>

            <div class="space-y-6">
              <!-- Air Quality -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="font-semibold text-gray-700 flex items-center gap-2">
                    <span>💨</span>
                    Air Quality
                  </span>
                  <span class="text-gray-500 text-sm">{{ neighborhood.air_quality }}/5</span>
                </div>
                <div class="flex gap-1">
                  <div
                    v-for="n in 5"
                    :key="n"
                    class="h-3 flex-1 rounded"
                    :class="n <= Math.round(neighborhood.air_quality) ? 'bg-emerald-500' : 'bg-gray-200'"
                  ></div>
                </div>
                <p class="text-xs text-gray-600 mt-1">
                  {{ getAirQualityDescription(neighborhood.air_quality) }}
                </p>
              </div>

              <!-- Noise Level -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="font-semibold text-gray-700 flex items-center gap-2">
                    <span>🔊</span>
                    Noise Level
                  </span>
                  <span class="text-gray-500 text-sm">{{ neighborhood.noise_level }}/5</span>
                </div>
                <div class="flex gap-1">
                  <div
                    v-for="n in 5"
                    :key="n"
                    class="h-3 flex-1 rounded"
                    :class="n <= Math.round(neighborhood.noise_level) ? 'bg-emerald-500' : 'bg-gray-200'"
                  ></div>
                </div>
                <p class="text-xs text-gray-600 mt-1">
                  {{ getNoiseLevelDescription(neighborhood.noise_level) }}
                </p>
              </div>

              <!-- Green Coverage -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="font-semibold text-gray-700 flex items-center gap-2">
                    <span>🌿</span>
                    Green Coverage
                  </span>
                  <span class="text-gray-500 text-sm">{{ neighborhood.green_coverage }}/5</span>
                </div>
                <div class="flex gap-1">
                  <div
                    v-for="n in 5"
                    :key="n"
                    class="h-3 flex-1 rounded"
                    :class="n <= Math.round(neighborhood.green_coverage) ? 'bg-emerald-500' : 'bg-gray-200'"
                  ></div>
                </div>
                <p class="text-xs text-gray-600 mt-1">
                  {{ getGreenCoverageDescription(neighborhood.green_coverage) }}
                </p>
              </div>

              <!-- Urban Heat -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="font-semibold text-gray-700 flex items-center gap-2">
                    <span>☀️</span>
                    Urban Heat
                  </span>
                  <span class="text-gray-500 text-sm">{{ neighborhood.urban_heat }}/5</span>
                </div>
                <div class="flex gap-1">
                  <div
                    v-for="n in 5"
                    :key="n"
                    class="h-3 flex-1 rounded"
                    :class="n <= Math.round(neighborhood.urban_heat) ? 'bg-emerald-500' : 'bg-gray-200'"
                  ></div>
                </div>
                <p class="text-xs text-gray-600 mt-1">
                  {{ getUrbanHeatDescription(neighborhood.urban_heat) }}
                </p>
              </div>
            </div>

            <!-- Overall Score Display -->
            <div class="mt-8 pt-8 border-t">
              <div class="text-center">
                <p class="text-gray-600 mb-2">Overall Livability Score</p>
                <div
                  class="inline-flex items-center justify-center w-24 h-24 rounded-full text-3xl font-bold text-white"
                  :style="{ backgroundColor: getScoreColor(neighborhood.livability_score) }"
                >
                  {{ neighborhood.livability_score }}
                </div>
                <p class="text-sm text-gray-600 mt-2">
                  {{ getScoreLabel(neighborhood.livability_score) }}
                </p>
              </div>
            </div>
          </div>

          <!-- Right Column: Map & Insights -->
          <div class="space-y-8">
            <!-- Mini Map -->
            <div class="bg-white rounded-2xl shadow-xl p-8">
              <h2 class="text-xl font-bold text-gray-800 mb-4">🗺️ Location</h2>
              <div id="detail-map" class="h-64 bg-gradient-to-br from-blue-100 to-green-100 rounded-lg"></div>
              <div class="mt-4 text-sm text-gray-600">
                <p>📍 Coordinates: {{ neighborhood.latitude.toFixed(4) }}, {{ neighborhood.longitude.toFixed(4) }}</p>
              </div>
            </div>

            <!-- Insights -->
            <div class="bg-gradient-to-br from-blue-50 to-emerald-50 rounded-2xl shadow-xl p-8 border-2 border-emerald-200">
              <h2 class="text-xl font-bold text-gray-800 mb-4">💬 Insights</h2>
              <p class="text-gray-700 leading-relaxed">{{ neighborhood.insights }}</p>
            </div>

            <!-- Metadata -->
            <div v-if="neighborhood.metadata" class="bg-white rounded-2xl shadow-xl p-8">
              <h2 class="text-xl font-bold text-gray-800 mb-4">ℹ️ Additional Information</h2>
              <dl class="space-y-2 text-sm">
                <div v-if="neighborhood.metadata.description">
                  <dt class="font-semibold text-gray-700">Description:</dt>
                  <dd class="text-gray-600">{{ neighborhood.metadata.description }}</dd>
                </div>
                <div v-if="neighborhood.metadata.population">
                  <dt class="font-semibold text-gray-700">Population:</dt>
                  <dd class="text-gray-600">{{ neighborhood.metadata.population.toLocaleString() }}</dd>
                </div>
                <div v-if="neighborhood.metadata.area_km2">
                  <dt class="font-semibold text-gray-700">Area:</dt>
                  <dd class="text-gray-600">{{ neighborhood.metadata.area_km2 }} km²</dd>
                </div>
                <div v-if="neighborhood.metadata.last_updated">
                  <dt class="font-semibold text-gray-700">Data Updated:</dt>
                  <dd class="text-gray-600">{{ formatDate(neighborhood.metadata.last_updated) }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>

        <!-- Visual Radar Chart -->
        <div class="bg-white rounded-2xl shadow-xl p-8 mt-8">
          <h2 class="text-xl font-bold text-gray-800 mb-6">📊 Environmental Indicators Overview</h2>
          <div class="flex justify-center">
            <div class="w-full max-w-xl">
              <RadarChart :datasets="radarDataset" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNeighborhoodStore } from '@/stores/neighborhoods'
import L from 'leaflet'
import RadarChart from '@/components/RadarChart.vue'

const route = useRoute()
const router = useRouter()
const store = useNeighborhoodStore()

const neighborhood = computed(() => store.selectedNeighborhood)

// Radar chart dataset
const radarDataset = computed(() => {
  if (!neighborhood.value) return []
  
  return [
    {
      label: neighborhood.value.name,
      data: [
        neighborhood.value.air_quality,
        neighborhood.value.noise_level,
        neighborhood.value.green_coverage,
        neighborhood.value.urban_heat
      ],
      color: '#10b981' // emerald-500
    }
  ]
})

// Helper functions
const getScoreColor = (score) => {
  if (score >= 8.0) return '#4ade80'
  if (score >= 6.0) return '#fbbf24'
  return '#f87171'
}

const getScoreLabel = (score) => {
  if (score >= 8.0) return 'Excellent'
  if (score >= 6.0) return 'Good'
  return 'Fair'
}

const getAirQualityDescription = (score) => {
  if (score >= 4.0) return 'Clean air with minimal pollution'
  if (score >= 3.0) return 'Moderate air quality'
  return 'Higher pollution levels'
}

const getNoiseLevelDescription = (score) => {
  if (score >= 4.0) return 'Very quiet area'
  if (score >= 3.0) return 'Moderate noise levels'
  return 'Higher noise exposure'
}

const getGreenCoverageDescription = (score) => {
  if (score >= 4.0) return 'Excellent green spaces and tree coverage'
  if (score >= 3.0) return 'Moderate vegetation and parks'
  return 'Limited green coverage'
}

const getUrbanHeatDescription = (score) => {
  if (score >= 4.0) return 'Cool urban environment'
  if (score >= 3.0) return 'Moderate urban heat levels'
  return 'Higher urban heat effects'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Initialize mini map
const initDetailMap = () => {
  if (!neighborhood.value) return

  const detailMap = L.map('detail-map').setView(
    [neighborhood.value.latitude, neighborhood.value.longitude],
    14
  )

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(detailMap)

  const color = getScoreColor(neighborhood.value.livability_score)
  L.circleMarker(
    [neighborhood.value.latitude, neighborhood.value.longitude],
    {
      radius: 15,
      fillColor: color,
      color: '#fff',
      weight: 3,
      opacity: 1,
      fillOpacity: 0.8
    }
  ).addTo(detailMap)
}

// Load neighborhood on mount
onMounted(async () => {
  const neighborhoodId = route.params.id
  await store.fetchNeighborhoodDetail(neighborhoodId)
  
  // Initialize map after data loads
  setTimeout(() => {
    if (neighborhood.value) {
      initDetailMap()
    }
  }, 100)
})
</script>