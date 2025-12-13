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

      <h3 class="font-semibold text-gray-800 mb-4">📍 Livability Score Legend</h3>

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
          Blue<br><span class="font-normal text-gray-500 text-[10px]">Very high</span>
        </div>
        <div class="text-center w-1/5">
          Green<br><span class="font-normal text-gray-500 text-[10px]">High</span>
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
    <div class="neighborhood-popup" style="min-width: 220px;">
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
      </div>
      <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #e5e7eb;">
        <div style="text-align: center; font-size: 0.75rem; color: #6b7280;">
          Click polygon to view full details
        </div>
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
  font-size: 25px;
  padding: 5px 8px;
}
</style>