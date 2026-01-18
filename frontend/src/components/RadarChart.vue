<template>
  <div class="radar-chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import {
  Chart,
  RadarController,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js'

// Register Chart.js components
Chart.register(
  RadarController,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

const props = defineProps({
  datasets: {
    type: Array,
    required: true,
    // Expected format:
    // [
    //   {
    //     label: 'Neighborhood 1',
    //     data: [airQuality, noiseLevel, greenSpace, treeGreenness, urbanHeat],
    //     color: '#10b981' // emerald-500
    //   }
    // ]
  }
})

const chartCanvas = ref(null)
let chartInstance = null

const createChart = () => {
  if (!chartCanvas.value) return

  // Destroy existing chart if it exists
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')

  chartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['💨 Air Quality', '🔇 Noise Level', '🌿 Green Coverage', '🌡️ Urban Heat'],
      datasets: props.datasets.map(dataset => ({
        label: dataset.label,
        data: dataset.data,
        backgroundColor: dataset.color + '33', // 20% opacity
        borderColor: dataset.color,
        borderWidth: 2,
        pointBackgroundColor: dataset.color,
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: dataset.color,
        pointRadius: 4,
        pointHoverRadius: 6
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        r: {
          beginAtZero: true,
          min: 0,
          max: 5,
          ticks: {
            stepSize: 1,
            font: {
              size: 11
            },
            color: '#6b7280' // gray-500
          },
          grid: {
            color: '#e5e7eb' // gray-200
          },
          pointLabels: {
            font: {
              size: 12,
              weight: '600'
            },
            color: '#374151', // gray-700
            padding: 10
          }
        }
      },
      plugins: {
        legend: {
          display: props.datasets.length > 1,
          position: 'bottom',
          labels: {
            padding: 15,
            font: {
              size: 12,
              weight: '600'
            },
            color: '#374151',
            usePointStyle: true,
            pointStyle: 'circle'
          }
        },
        tooltip: {
          enabled: true,
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: 12,
          titleFont: {
            size: 13,
            weight: 'bold'
          },
          bodyFont: {
            size: 12
          },
          callbacks: {
            label: function(context) {
              return `${context.dataset.label}: ${context.parsed.r.toFixed(1)}/5`
            }
          }
        }
      },
      interaction: {
        mode: 'nearest',
        intersect: false
      }
    }
  })
}

onMounted(() => {
  nextTick(() => {
    createChart()
  })
})

// Watch for dataset changes and recreate chart
watch(() => props.datasets, () => {
  nextTick(() => {
    createChart()
  })
}, { deep: true })
</script>

<style scoped>
.radar-chart-container {
  position: relative;
  width: 100%;
  height: 100%;
}

canvas {
  max-height: 400px;
}
</style>
