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

            <!-- Satisfaction Rating -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-3">
                How satisfied are you with SoundCity?
              </label>
              <div class="flex justify-between gap-2">
                <button
                  v-for="rating in 5"
                  :key="rating"
                  type="button"
                  @click="feedback.satisfaction = rating"
                  class="flex-1 py-3 text-2xl rounded-lg border-2 transition-all"
                  :class="feedback.satisfaction === rating 
                    ? 'border-emerald-600 bg-emerald-50 scale-110' 
                    : 'border-gray-200 hover:border-gray-300'"
                >
                  {{ ['😞', '😐', '🙂', '😊', '🤩'][rating - 1] }}
                </button>
              </div>
              <div class="flex justify-between text-xs text-gray-500 mt-1 px-1">
                <span>Poor</span>
                <span>Excellent</span>
              </div>
            </div>

            <!-- Most Useful Feature -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Which feature do you find most useful?
              </label>
              <div class="space-y-2">
                <label
                  v-for="feature in features"
                  :key="feature.value"
                  class="flex items-center gap-3 p-3 rounded-lg border-2 cursor-pointer transition"
                  :class="feedback.useful_feature === feature.value 
                    ? 'border-emerald-600 bg-emerald-50' 
                    : 'border-gray-200 hover:border-gray-300'"
                >
                  <input
                    type="radio"
                    :value="feature.value"
                    v-model="feedback.useful_feature"
                    class="w-4 h-4 text-emerald-600"
                  />
                  <span class="text-gray-700">{{ feature.label }}</span>
                </label>
              </div>
            </div>

            <!-- Most Important Indicator -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Which indicator matters most to you?
              </label>
              <div class="grid grid-cols-2 gap-2">
                <button
                  v-for="indicator in indicators"
                  :key="indicator.value"
                  type="button"
                  @click="feedback.most_important_indicator = indicator.value"
                  class="py-3 px-4 rounded-lg border-2 font-medium transition-all text-sm"
                  :class="feedback.most_important_indicator === indicator.value
                    ? 'border-emerald-600 bg-emerald-600 text-white'
                    : 'border-gray-200 text-gray-700 hover:border-gray-300'"
                >
                  {{ indicator.label }}
                </button>
              </div>
            </div>

            <!-- Housing Decision -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Would you use this to make housing decisions?
              </label>
              <div class="flex gap-2">
                <button
                  v-for="option in housingDecisionOptions"
                  :key="option.value"
                  type="button"
                  @click="feedback.housing_decision = option.value"
                  class="flex-1 py-3 rounded-lg border-2 font-medium transition-all"
                  :class="feedback.housing_decision === option.value
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

            <!-- Recommendation -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Would you recommend SoundCity?
              </label>
              <div class="flex gap-3">
                <button
                  type="button"
                  @click="feedback.would_recommend = true"
                  class="flex-1 py-3 rounded-lg border-2 font-medium transition-all"
                  :class="feedback.would_recommend === true
                    ? 'border-emerald-600 bg-emerald-600 text-white'
                    : 'border-gray-200 text-gray-700 hover:border-gray-300'"
                >
                  👍 Yes
                </button>
                <button
                  type="button"
                  @click="feedback.would_recommend = false"
                  class="flex-1 py-3 rounded-lg border-2 font-medium transition-all"
                  :class="feedback.would_recommend === false
                    ? 'border-red-600 bg-red-600 text-white'
                    : 'border-gray-200 text-gray-700 hover:border-gray-300'"
                >
                  👎 No
                </button>
              </div>
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

const API_BASE_URL = 'https://soundcity.onrender.com/api/v1'
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
  satisfaction: null,
  useful_feature: null,
  most_important_indicator: null,
  housing_decision: null,
  improvement: '',
  would_recommend: null
})

const features = [
  { value: 'map', label: '🗺️ Interactive Map' },
  { value: 'comparison', label: '⚖️ Comparison Tool' },
  { value: 'filters', label: '🎯 Custom Filters' },
  { value: 'presets', label: '🛠️ Presets' },
  { value: 'charts', label: '📊 Radar Charts' }
]

const indicators = [
  { value: 'air', label: '💨 Air Quality' },
  { value: 'noise', label: '🔇 Noise Level' },
  { value: 'green', label: '🌳 Green Space' },
  { value: 'heat', label: '🌡️ Urban Heat' }
]

const housingDecisionOptions = [
  { value: 'definitely', label: '✅ Definitely' },
  { value: 'maybe', label: '🤔 Maybe' },
  { value: 'no', label: '❌ No' }
]

const isValid = computed(() => {
  return feedback.value.satisfaction !== null &&
         feedback.value.useful_feature !== null &&
         feedback.value.most_important_indicator !== null &&
         feedback.value.housing_decision !== null &&
         feedback.value.would_recommend !== null
})

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
      satisfaction: null,
      useful_feature: null,
      most_important_indicator: null,
      housing_decision: null,
      improvement: '',
      would_recommend: null
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
