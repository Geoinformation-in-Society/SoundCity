<template>
  <!-- Floating Feedback Button -->
  <button
    v-if="!showModal"
    @click="showModal = true"
    class="fixed bottom-6 right-6 bg-emerald-600 text-white px-4 py-3 rounded-full shadow-lg hover:bg-emerald-700 transition-all hover:scale-105 z-50 flex items-center gap-2"
  >
    <span class="text-xl">💬</span>
    <span class="font-medium">Feedback</span>
  </button>

  <!-- Feedback Modal -->
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="showModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto"
        @click.self="closeModal"
      >
        <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 relative animate-slide-up my-8 max-h-[90vh] overflow-y-auto">
          <!-- Close Button -->
          <button
            @click="closeModal"
            class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Success State -->
          <div v-if="submitted" class="text-center py-8">
            <div class="text-6xl mb-4">🎉</div>
            <h2 class="text-2xl font-bold text-gray-800 mb-2">Thank You!</h2>
            <p class="text-gray-600 mb-6">Your feedback helps us improve SoundCity</p>
            <button
              @click="closeModal"
              class="bg-emerald-600 text-white px-6 py-2 rounded-lg hover:bg-emerald-700 transition"
            >
              Close
            </button>
          </div>

          <!-- Feedback Form -->
          <form v-else @submit.prevent="submitFeedback" class="space-y-6">
            <!-- Header -->
            <div class="text-center">
              <h2 class="text-2xl font-bold text-gray-800 flex items-center justify-center gap-2">
                <span>✨</span>
                Help Us Improve SoundCity
              </h2>
              <p class="text-sm text-gray-500 mt-1">Takes 30 seconds • Anonymous</p>
            </div>

            <!-- Most Useful Features (up to 2) -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Which features did you use during this session? <br>(Select up to 2)
              </label>
              <div class="space-y-2">
                <label
                  v-for="feature in features"
                  :key="feature.value"
                  class="flex items-center gap-3 p-3 rounded-lg border-2 cursor-pointer transition"
                  :class="feedback.useful_features.includes(feature.value)
                    ? 'border-emerald-600 bg-emerald-50' 
                    : 'border-gray-200 hover:border-gray-300'"
                >
                  <input
                    type="checkbox"
                    :value="feature.value"
                    :checked="feedback.useful_features.includes(feature.value)"
                    @change="toggleFeature(feature.value)"
                    :disabled="feedback.useful_features.length >= 2 && !feedback.useful_features.includes(feature.value)"
                    class="w-4 h-4 text-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  />
                  <span class="text-gray-700" :class="feedback.useful_features.length >= 2 && !feedback.useful_features.includes(feature.value) ? 'text-gray-400' : ''">{{ feature.label }}</span>
                </label>
              </div>
              <p class="text-xs text-gray-500 mt-2">{{ feedback.useful_features.length }}/2 selected</p>
            </div>

            <!-- Most Important Indicators (up to 2) -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Which indicators did you pay most attention to? <br>(Select up to 2)
              </label>
              <div class="grid grid-cols-2 gap-2">
                <label
                  v-for="indicator in indicators"
                  :key="indicator.value"
                  class="flex items-center gap-2 p-3 rounded-lg border-2 cursor-pointer transition"
                  :class="feedback.most_important_indicators.includes(indicator.value)
                    ? 'border-emerald-600 bg-emerald-50' 
                    : 'border-gray-200 hover:border-gray-300'"
                >
                  <input
                    type="checkbox"
                    :value="indicator.value"
                    :checked="feedback.most_important_indicators.includes(indicator.value)"
                    @change="toggleIndicator(indicator.value)"
                    :disabled="feedback.most_important_indicators.length >= 2 && !feedback.most_important_indicators.includes(indicator.value)"
                    class="w-4 h-4 text-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  />
                  <span class="text-sm" :class="feedback.most_important_indicators.length >= 2 && !feedback.most_important_indicators.includes(indicator.value) ? 'text-gray-400' : 'text-gray-700'">{{ indicator.label }}</span>
                </label>
              </div>
              <p class="text-xs text-gray-500 mt-2">{{ feedback.most_important_indicators.length }}/2 selected</p>
            </div>

            <!-- Housing Decision Support -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-3">
                To what extent could SoundCity support a housing-related decision?
              </label>
              <div class="space-y-2">
                <button
                  v-for="option in housingDecisionOptions"
                  :key="option.value"
                  type="button"
                  @click="feedback.housing_decision = option.value"
                  class="w-full py-2 px-3 rounded-lg border-2 font-medium transition-all text-sm"
                  :class="feedback.housing_decision === option.value
                    ? 'border-emerald-600 bg-emerald-600 text-white'
                    : 'border-gray-200 text-gray-700 hover:border-gray-300'"
                >
                  {{ option.label }}
                </button>
              </div>
            </div>

            <!-- Data Clarity -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-3">
                The way data and indicators are combined is clear.
              </label>
              <div class="space-y-2">
                <button
                  v-for="option in dataClarity"
                  :key="option.value"
                  type="button"
                  @click="feedback.data_clarity = option.value"
                  class="w-full py-2 px-3 rounded-lg border-2 font-medium transition-all text-sm"
                  :class="feedback.data_clarity === option.value
                    ? 'border-emerald-600 bg-emerald-600 text-white'
                    : 'border-gray-200 text-gray-700 hover:border-gray-300'"
                >
                  {{ option.label }}
                </button>
              </div>
            </div>

            <!-- Improvement Suggestion -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                What would you improve? (Optional)
              </label>
              <textarea
                v-model="feedback.improvement"
                rows="3"
                placeholder="Your suggestions..."
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-none"
              ></textarea>
            </div>

            <!-- Actions -->
            <div class="flex gap-3 pt-2">
              <button
                type="button"
                @click="closeModal"
                :disabled="loading"
                class="flex-1 border-2 border-gray-300 text-gray-700 py-3 rounded-lg hover:bg-gray-50 transition font-medium disabled:opacity-50"
              >
                Skip for now
              </button>
              <button
                type="submit"
                :disabled="!isValid || loading"
                class="flex-1 bg-emerald-600 text-white py-3 rounded-lg hover:bg-emerald-700 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ loading ? 'Submitting...' : 'Submit Feedback' }}
              </button>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="text-sm text-red-600 text-center">
              {{ error }}
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL
const route = useRoute()

const showModal = ref(false)
const submitted = ref(false)
const loading = ref(false)
const error = ref(null)

// Session tracking
const sessionStartTime = ref(Date.now())
const modalOpenTime = ref(null)

onMounted(() => {
  sessionStartTime.value = Date.now()
})

// Lock body scroll when modal is open and track open time
watch(showModal, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
    modalOpenTime.value = Date.now()
  } else {
    document.body.style.overflow = ''
  }
})

const feedback = ref({
  useful_features: [],
  most_important_indicators: [],
  housing_decision: null,
  data_clarity: null,
  improvement: ''
})

const features = [
  { value: 'map', label: '🗺️ Interactive Map' },
  { value: 'comparison', label: '⚖️ Comparison Tool' },
  { value: 'filters', label: '🎯 Custom Filters' },
  { value: 'presets', label: '🛠️ Presets' },
  { value: 'charts', label: '📊 Radar Charts' },
  { value: 'none', label: '🤷 Did not use any extensively' }
]

const indicators = [
  { value: 'air', label: '💨 Air Quality' },
  { value: 'noise', label: '🔇 Noise Level' },
  { value: 'green', label: '🌳 Green Space' },
  { value: 'heat', label: '🌡️ Urban Heat' },
  { value: 'none', label: '🤷 None' }
]

const housingDecisionOptions = [
  { value: 'not_at_all', label: 'Not at all' },
  { value: 'slightly', label: 'Slightly' },
  { value: 'moderately', label: 'Moderately' },
  { value: 'largely', label: 'Largely' },
  { value: 'fully', label: 'Fully' }
]

const dataClarity = [
  { value: 'strongly_disagree', label: 'Strongly disagree' },
  { value: 'disagree', label: 'Disagree' },
  { value: 'neutral', label: 'Neutral' },
  { value: 'agree', label: 'Agree' },
  { value: 'strongly_agree', label: 'Strongly agree' }
]

const isValid = computed(() => {
  return feedback.value.useful_features.length > 0 &&
         feedback.value.most_important_indicators.length > 0 &&
         feedback.value.housing_decision !== null &&
         feedback.value.data_clarity !== null
})

const toggleFeature = (featureValue) => {
  const index = feedback.value.useful_features.indexOf(featureValue)
  
  // Handle "none" as exclusive option
  if (featureValue === 'none') {
    if (index > -1) {
      // Deselect "none"
      feedback.value.useful_features.splice(index, 1)
    } else {
      // Select "none" and clear all other features
      feedback.value.useful_features = ['none']
    }
  } else {
    // Handle regular features
    if (index > -1) {
      // Remove if already selected
      feedback.value.useful_features.splice(index, 1)
    } else {
      // Remove "none" if selected, then add the new feature
      const noneIndex = feedback.value.useful_features.indexOf('none')
      if (noneIndex > -1) {
        feedback.value.useful_features.splice(noneIndex, 1)
      }
      
      // Add if less than 2 are selected
      if (feedback.value.useful_features.length < 2) {
        feedback.value.useful_features.push(featureValue)
      }
    }
  }
}

const toggleIndicator = (indicatorValue) => {
  const index = feedback.value.most_important_indicators.indexOf(indicatorValue)
  
  // Handle "none" as exclusive option
  if (indicatorValue === 'none') {
    if (index > -1) {
      // Deselect "none"
      feedback.value.most_important_indicators.splice(index, 1)
    } else {
      // Select "none" and clear all other indicators
      feedback.value.most_important_indicators = ['none']
    }
  } else {
    // Handle regular indicators
    if (index > -1) {
      // Remove if already selected
      feedback.value.most_important_indicators.splice(index, 1)
    } else {
      // Remove "none" if selected, then add the new indicator
      const noneIndex = feedback.value.most_important_indicators.indexOf('none')
      if (noneIndex > -1) {
        feedback.value.most_important_indicators.splice(noneIndex, 1)
      }
      
      // Add if less than 2 are selected
      if (feedback.value.most_important_indicators.length < 2) {
        feedback.value.most_important_indicators.push(indicatorValue)
      }
    }
  }
}

const submitFeedback = async () => {
  if (!isValid.value) return
  
  loading.value = true
  error.value = null
  
  try {
    // Calculate session duration
    const sessionDuration = Math.floor((Date.now() - sessionStartTime.value) / 1000) // in seconds
    const timeOnModal = modalOpenTime.value ? Math.floor((Date.now() - modalOpenTime.value) / 1000) : 0
    
    // Prepare feedback with session data
    const feedbackData = {
      ...feedback.value,
      session_data: {
        current_page: route.name || route.path,
        session_duration: sessionDuration,
        time_on_modal: timeOnModal,
        timestamp: new Date().toISOString(),
        screen_size: `${window.innerWidth}x${window.innerHeight}`,
        viewport_size: `${document.documentElement.clientWidth}x${document.documentElement.clientHeight}`
      }
    }
    
    await axios.post(`${API_BASE_URL}/feedback`, feedbackData)
    submitted.value = true
    
    // Auto-close after 3 seconds
    setTimeout(() => {
      closeModal()
    }, 3000)
  } catch (err) {
    error.value = 'Failed to submit feedback. Please try again.'
    console.error('Feedback submission error:', err)
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  showModal.value = false
  
  // Reset form after animation
  setTimeout(() => {
    submitted.value = false
    feedback.value = {
      useful_features: [],
      most_important_indicators: [],
      housing_decision: null,
      data_clarity: null,
      improvement: ''
    }
    error.value = null
  }, 300)
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .animate-slide-up {
  animation: slide-up 0.3s ease-out;
}

@keyframes slide-up {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
