import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL 

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
})

// Request interceptor for logging
apiClient.interceptors.request.use(
  config => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`)
    return config
  },
  error => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      console.error('API Error:', error.response.status, error.response.data)
    } else if (error.request) {
      console.error('Network Error: No response received')
    } else {
      console.error('Error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default {
  /**
   * Get all neighborhoods with optional weight parameters
   * @param {Object} weights - Weight object with all indicators
   * @returns {Promise} API response with neighborhood list
   */
  getNeighborhoods(weights = {}) {
    const params = {
      air_weight: weights.air || 0.25,
      noise_weight: weights.noise || 0.25,
      green_space_weight: weights.greenSpaces || 0.25,
      urban_heat_weight: weights.urbanHeat || 0.25,
    }
    return apiClient.get('/neighborhoods', { params })
  },

  /**
   * Get detailed information for a specific neighborhood
   * @param {string} id - Neighborhood ID
   * @param {Object} weights - Weight object with all indicators
   * @returns {Promise} API response with neighborhood details
   */
  getNeighborhoodDetail(id, weights = {}) {
    const params = {
      air_weight: weights.air || 0.25,
      noise_weight: weights.noise || 0.25,
      green_space_weight: weights.greenSpaces || 0.25,
      urban_heat_weight: weights.urbanHeat || 0.25,
    }
    return apiClient.get(`/neighborhoods/${id}`, { params })
  },

  /**
   * Compare two neighborhoods
   * @param {string} id1 - First neighborhood ID
   * @param {string} id2 - Second neighborhood ID
   * @param {Object} weights - Weight object with all indicators
   * @returns {Promise} API response with comparison data
   */
  compareNeighborhoods(id1, id2, weights = {}) {
    const params = {
      air_weight: weights.air || 0.25,
      noise_weight: weights.noise || 0.25,
      green_space_weight: weights.greenSpaces || 0.25,
      urban_heat_weight: weights.urbanHeat || 0.25
    }
    return apiClient.get(`/neighborhoods/${id1}/compare/${id2}`, { params })
  }
}
