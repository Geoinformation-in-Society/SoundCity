<template>
  <div class="relative h-full w-full">
    <!-- Map Container -->
    <div id="map" class="h-full w-full"></div>

    <!-- Loading Overlay -->
    <div
      v-if="store.loading"
      class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center z-[1000]"
    >
      <div class="text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mb-4"></div>
        <p class="text-gray-700 font-medium">Loading neighborhoods...</p>
      </div>
    </div>

    <!-- Legend -->
    <div class="absolute bottom-6 left-6 bg-white rounded-lg shadow-lg p-4 z-[1000] w-[340px]">

      <div class="flex items-center justify-between mb-4">
        <h3 class="font-semibold text-gray-800">📍 Livability Score Legend</h3>
        
        <!-- Info Icon with Popover -->
        <div class="relative group">
          <button class="flex items-center justify-center w-6 h-6 rounded-full bg-blue-500 text-white hover:bg-blue-600 transition-colors cursor-help shadow-md">
            <svg class="w-4 h-4 font-bold" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
          </button>
          
          <!-- Popover Content -->
          <div class="absolute bottom-full right-0 mb-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 p-3 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 pointer-events-none z-[2000]">
            <div class="text-xs space-y-2">
              <div class="font-semibold text-gray-800 border-b pb-1">Data Information</div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">Last Updated:</span>
                <span class="font-medium text-gray-800">{{ getLastUpdateDate() }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-gray-600">Update Frequency:</span>
                <span class="font-medium text-gray-800">Daily</span>
              </div>
              
              <div class="border-t pt-2">
                <div class="text-gray-600 mb-1">Data Sources:</div>
                <ul class="text-gray-800 space-y-0.5 ml-2">
                  <li>• Air Quality: LUQS NRW stations + Sensor.Community</li>
                  <li>• Noise: Münster Lärmkartierung</li>
                  <li>• Green Environment: Münster Grünflächen + Baumkataster</li>
                  <li>• Heat: Landsat 8</li>
                </ul>
              </div>
              
              <div class="border-t pt-2 text-[10px] text-gray-500">
                ℹ️ Scores are calculated using real-time environmental data
              </div>
            </div>
            
            <!-- Arrow pointer -->
            <div class="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-white" style="margin-top: -1px;"></div>
          </div>
        </div>
      </div>

      <!-- Category labels -->
      <div class="flex justify-between text-xs font-semibold text-gray-700 mb-2">
        <div class="text-center w-1/5">
          Red<br><span class="font-normal text-gray-500 text-[10px]">Very low</span>
        </div>
        <div class="text-center w-1/5">
          Orange<br><span class="font-normal text-gray-500 text-[10px]">Low</span>
        </div>
        <div class="text-center w-1/5">
          Yellow<br><span class="font-normal text-gray-500 text-[10px]">Moderate</span>
        </div>
        <div class="text-center w-1/5">
          Green<br><span class="font-normal text-gray-500 text-[10px]">High</span>
        </div>
        <div class="text-center w-1/5">
          Blue<br><span class="font-normal text-gray-500 text-[10px]">Very high</span>
        </div>
      </div>

      <!-- Gradient scale -->
      <div class="grid grid-cols-10 h-4 rounded overflow-hidden border border-gray-200">
        <div class="bg-red-600"></div>
        <div class="bg-red-500"></div>

        <div class="bg-orange-500"></div>
        <div class="bg-orange-400"></div>

        <div class="bg-yellow-300"></div>
        <div class="bg-yellow-200"></div>

        <div class="bg-green-300"></div>
        <div class="bg-green-400"></div>

        <div class="bg-blue-500"></div>
        <div class="bg-blue-600"></div>
      </div>

      <!-- Percentage labels -->
      <div class="grid grid-cols-10 text-[10px] text-gray-500 mt-1">
        <div class="text-center">(0–5%)</div>
        <div class="text-center">(5–10%)</div>
        <div class="text-center">(10–20%)</div>
        <div class="text-center">(20–30%)</div>
        <div class="text-center">(30–40%)</div>
        <div class="text-center">(40–50%)</div>
        <div class="text-center">(50–65%)</div>
        <div class="text-center">(65–75%)</div>
        <div class="text-center">(75–90%)</div>
        <div class="text-center">(90–100%)</div>
      </div>

      <p class="text-xs text-gray-500 mt-3">Click a neighborhood for details</p>
    </div>

  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useNeighborhoodStore } from '@/stores/neighborhoods'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const router = useRouter()
const store = useNeighborhoodStore()

let map = null
let polygonLayers = []

// Add global function for button click in popup
window.viewNeighborhoodDetails = (neighborhoodId) => {
  router.push(`/neighborhood/${neighborhoodId}`)
}

// Get color based on score
const getColor = (score) => {
  if (score >= 9.5) return '#2563eb'  // deep blue (95–100%)
  if (score >= 9.0) return '#3b82f6'  // blue (90–95%)
  if (score >= 8.5) return '#0ea5e9'  // cyan-green (85–90%)
  if (score >= 8.0) return '#14b8a6'  // teal-green (80–85%)

  if (score >= 7.5) return '#10b981'  // green (75–80%)
  if (score >= 7.0) return '#34d399'  // light green (70–75%)
  if (score >= 6.5) return '#6ee7b7'  // pale green (65–70%)
  if (score >= 6.0) return '#a7f3d0'  // very pale green (60–65%)

  if (score >= 5.5) return '#fef9c3'  // yellow (55–60%)
  if (score >= 5.0) return '#fef08a'  // light yellow (50–55%)
  if (score >= 4.5) return '#fde047'  // moderate yellow (45–50%)
  if (score >= 4.0) return '#facc15'  // deeper yellow (40–45%)

  if (score >= 3.5) return '#fbbf24'  // orange-yellow (35–40%)
  if (score >= 3.0) return '#fb923c'  // orange (30–35%)
  if (score >= 2.5) return '#f97316'  // deeper orange (25–30%)
  if (score >= 2.0) return '#ea580c'  // strong orange (20–25%)

  if (score >= 1.5) return '#f87171'  // light red (15–20%)
  if (score >= 1.0) return '#ef4444'  // red (10–15%)
  if (score >= 0.5) return '#dc2626'  // deep red (5–10%)
  return '#b91c1c'                   // very deep red (0–5%)
}

// Initialize map
const initMap = () => {
  if (map) return

  map = L.map('map', {
    center: [51.9607, 7.6261], // Münster coordinates
    zoom: 13,
    zoomControl: true
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18
  }).addTo(map)
}

// Create popup content
const createPopupContent = (neighborhood) => {
  return `
    <div class="neighborhood-popup" style="min-width: 220px; padding-top: 0.5rem; padding-bottom: 0.5rem;">
      <h3 style="font-weight: bold; font-size: 1.125rem; margin-bottom: 0.5rem; color: #1f2937;">
        ${neighborhood.name}
      </h3>
      <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.875rem; color: #4b5563;">Overall Score:</span>
          <span style="font-weight: bold; color: #059669; font-size: 1rem;">
            ${neighborhood.livability_score}/10
          </span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem;">
          <span style="color: #6b7280;">💨 Air Quality:</span>
          <span>${'★'.repeat(Math.round(neighborhood.air_quality))}${'☆'.repeat(5 - Math.round(neighborhood.air_quality))}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem;">
          <span style="color: #6b7280;">🔊 Noise Level:</span>
          <span>${'★'.repeat(Math.round(neighborhood.noise_level))}${'☆'.repeat(5 - Math.round(neighborhood.noise_level))}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem;">
          <span style="color: #6b7280;">🌳 Green Environment:</span>
          <span>${'★'.repeat(Math.round(neighborhood.green_space))}${'☆'.repeat(5 - Math.round(neighborhood.green_space))}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem;">
          <span style="color: #6b7280;">☀️ Urban Heat:</span>
          <span>${'★'.repeat(Math.round(neighborhood.urban_heat))}${'☆'.repeat(5 - Math.round(neighborhood.urban_heat))}</span>
      </div>
      <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #e5e7eb;">
        <button 
          onclick="window.viewNeighborhoodDetails('${neighborhood.id}')"
          style="width: 100%; background-color: #059669; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 500; border: none; cursor: pointer; transition: background-color 0.2s;"
          onmouseover="this.style.backgroundColor='#047857'"
          onmouseout="this.style.backgroundColor='#059669'"
        >
          View Details →
        </button>
      </div>
    </div>
  `
}

// Update polygons on map
const updatePolygons = () => {
  if (!map) return

  // Clear existing polygons
  polygonLayers.forEach(layer => map.removeLayer(layer))
  polygonLayers = []

  // Add new polygons
  store.neighborhoods.forEach(neighborhood => {
    const color = getColor(neighborhood.livability_score)

    // Check if neighborhood has GeoJSON geometry
    if (neighborhood.geojson) {
      try {
      // Create polygon from GeoJSON
      const geoJsonLayer = L.geoJSON(neighborhood.geojson, {
        style: {
          fillColor: color,
          fillOpacity: 0.65,
          color: color,
          weight: 2,
          opacity: 0.9,
          lineCap: 'round',
          lineJoin: 'round'
        }
      }).addTo(map)

      // Bind popup
      const popupContent = createPopupContent(neighborhood)
      geoJsonLayer.bindPopup(popupContent, {
        maxWidth: 300,
        className: 'custom-popup'
      })

      // Add click handler - navigate to detail view
      geoJsonLayer.on('click', () => {
        console.log(`Clicked on ${neighborhood.name}`)
        router.push(`/neighborhood/${neighborhood.id}`)
      })

      // Add hover effects
      geoJsonLayer.on('mouseover', function(e) {
        const layer = e.target
        layer.setStyle({
          fillOpacity: 0.7,
          weight: 3,
          color: '#059669'
        })
        
        // Open popup on hover
        layer.openPopup()
      })

      geoJsonLayer.on('mouseout', function(e) {
        const layer = e.target
        layer.setStyle({
          fillOpacity: 0.5,
          weight: 2,
          color: '#ffffff'
        })
      })

      polygonLayers.push(geoJsonLayer)
    } catch (error) {
      console.error(`Error creating polygon for ${neighborhood.name}:`, error)
      // Fall back to marker
      createFallbackMarker(neighborhood, color)
    }
    } else {
      // Fallback: Use circle marker if no GeoJSON
      createFallbackMarker(neighborhood, color)
    }
  })

  // Fit map to show all polygons
  if (polygonLayers.length > 0) {
    const group = L.featureGroup(polygonLayers)
    map.fitBounds(group.getBounds().pad(0.1))
  }
}

// Fallback to circle marker if no polygon
const createFallbackMarker = (neighborhood, color) => {
  const marker = L.circleMarker(
    [neighborhood.latitude, neighborhood.longitude],
    {
      radius: 15,
      fillColor: color,
      color: '#fff',
      weight: 3,
      opacity: 1,
      fillOpacity: 0.8
    }
  ).addTo(map)

  const popupContent = createPopupContent(neighborhood)
  marker.bindPopup(popupContent)
  
  marker.on('click', () => {
    router.push(`/neighborhood/${neighborhood.id}`)
  })

  polygonLayers.push(marker)
}
// Get last update date
const getLastUpdateDate = () => {
  const today = new Date()
  return today.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
// Initialize map and load data
onMounted(async () => {
  initMap()
  
  if (!store.hasData) {
    await store.fetchNeighborhoods()
  }
  
  updatePolygons()
})

// Watch for neighborhood changes
watch(
  () => store.neighborhoods,
  () => {
    updatePolygons()
  },
  { deep: true }
)
</script>

<style scoped>
#map {
  height: 100%;
  width: 100%;
}

:deep(.custom-popup .leaflet-popup-content-wrapper) {
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
  padding: 0;
}

:deep(.custom-popup .leaflet-popup-content) {
  margin: 12px;
  min-width: 220px;
}

:deep(.custom-popup .leaflet-popup-tip) {
  background: white;
}

:deep(.leaflet-popup-close-button) {
  font-size: 24px !important;
  padding: 4px !important;
  line-height: 1 !important;
  color: #9ca3af !important;
  font-weight: 400 !important;
  right: 8px !important;
  top: 14px !important;
  width: 24px !important;
  height: 24px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

:deep(.leaflet-popup-close-button:hover) {
  color: #1f2937 !important;
  background-color: #f3f4f6 !important;
  border-radius: 4px !important;
}
</style>