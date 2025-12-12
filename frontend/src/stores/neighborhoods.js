import { defineStore } from 'pinia'
import api from '@/services/api'

export const useNeighborhoodStore = defineStore('neighborhoods', {
  state: () => ({
    neighborhoods: [],
    selectedNeighborhood: null,
    compareNeighborhood1: null,
    compareNeighborhood2: null,
    filters: {
      airQuality: true,
      noise: true
    },
    weights: {
      air: 50,
      noise: 50
    },
    loading: false,
    error: null
  }),

  getters: {
    /**
     * Get neighborhoods sorted by livability score
     */
    sortedNeighborhoods: (state) => {
      return [...state.neighborhoods].sort(
        (a, b) => b.livability_score - a.livability_score
      )
    },

    /**
     * Get weight values as decimals (0-1)
     */
    normalizedWeights: (state) => ({
      air: state.weights.air / 100,
      noise: state.weights.noise / 100
    }),

    /**
     * Check if data is loaded
     */
    hasData: (state) => state.neighborhoods.length > 0
  },

  actions: {
    /**
     * Fetch all neighborhoods from API
     */
    async fetchNeighborhoods() {
      this.loading = true
      this.error = null

      try {
        const weights = this.normalizedWeights
        console.log('Fetching neighborhoods with weights:', weights)
        const response = await api.getNeighborhoods(weights.air, weights.noise)
        console.log(response.data)
        this.neighborhoods = response.data
        console.log(`Loaded ${this.neighborhoods.length} neighborhoods`)
      } catch (error) {
        this.error = 'Failed to fetch neighborhoods. Please try again.'
        console.error('Error fetching neighborhoods:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Fetch detailed information for a specific neighborhood
     * @param {string} id - Neighborhood ID
     */
    async fetchNeighborhoodDetail(id) {
      this.loading = true
      this.error = null

      try {
        const weights = this.normalizedWeights
        const response = await api.getNeighborhoodDetail(id, weights.air, weights.noise)
        this.selectedNeighborhood = response.data
        console.log(`Loaded details for ${this.selectedNeighborhood.name}`)
      } catch (error) {
        this.error = 'Failed to fetch neighborhood details.'
        console.error('Error fetching neighborhood details:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Update weight values and refresh data
     * @param {number} air - Air quality weight (0-100)
     * @param {number} noise - Noise level weight (0-100)
     */
    async updateWeights(air, noise) {
      this.weights.air = air
      this.weights.noise = noise
      await this.fetchNeighborhoods()
    },

    /**
     * Reset weights to default (50/50)
     */
    async resetWeights() {
      this.weights.air = 50
      this.weights.noise = 50
      await this.fetchNeighborhoods()
    },

    /**
     * Update filter settings
     * @param {Object} newFilters - Filter object
     */
    updateFilters(newFilters) {
      this.filters = { ...this.filters, ...newFilters }
    },

    /**
     * Clear selected neighborhood
     */
    clearSelection() {
      this.selectedNeighborhood = null
    },

    /**
     * Clear any errors
     */
    clearError() {
      this.error = null
    }
  }
})