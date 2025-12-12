import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000 // 10 second timeout
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
   * @param {number} airWeight - Weight for air quality (0-1)
   * @param {number} noiseWeight - Weight for noise level (0-1)
   * @returns {Promise} API response with neighborhood list
   */
  getNeighborhoods(airWeight = 0.5, noiseWeight = 0.5) {
    return apiClient.get('/neighborhoods', {
      params: {
        air_weight: airWeight,
        noise_weight: noiseWeight
      }
    })
  },

  /**
   * Get detailed information for a specific neighborhood
   * @param {string} id - Neighborhood ID
   * @param {number} airWeight - Weight for air quality (0-1)
   * @param {number} noiseWeight - Weight for noise level (0-1)
   * @returns {Promise} API response with neighborhood details
   */
  getNeighborhoodDetail(id, airWeight = 0.5, noiseWeight = 0.5) {
    return apiClient.get(`/neighborhoods/${id}`, {
      params: {
        air_weight: airWeight,
        noise_weight: noiseWeight
      }
    })
  },

  /**
   * Compare two neighborhoods
   * @param {string} id1 - First neighborhood ID
   * @param {string} id2 - Second neighborhood ID
   * @param {number} airWeight - Weight for air quality (0-1)
   * @param {number} noiseWeight - Weight for noise level (0-1)
   * @returns {Promise} API response with comparison data
   */
  compareNeighborhoods(id1, id2, airWeight = 0.5, noiseWeight = 0.5) {
    return apiClient.get(`/neighborhoods/${id1}/compare/${id2}`, {
      params: {
        air_weight: airWeight,
        noise_weight: noiseWeight
      }
    })
  }
}