import { defineStore } from 'pinia'
import api from '@/services/api'

export const useNeighborhoodStore = defineStore('neighborhoods', {
  state: () => ({
    neighborhoods: [],
    selectedNeighborhood: null,
    compareNeighborhood1: null,
    compareNeighborhood2: null,
    filters: {
      air: true,
      noise: true,
      greenSpaces: true,
      urbanHeat: true,
    },
    weights: {
      air: 25,
      noise: 25,
      greenSpaces: 25,
      urbanHeat: 25,
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
     * Get weight values as decimals (0-1) - always normalized to sum to 1
     */
    normalizedWeights: (state) => {
      const total = Object.values(state.weights).reduce((a, b) => a + b, 0)
      const normalized = {}
      Object.entries(state.weights).forEach(([key, value]) => {
        // Always normalize to sum to 1.0 for scoring
        normalized[key] = total > 0 ? value / total : 0
      })
      return normalized
    },

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
        const response = await api.getNeighborhoods(weights)

        this.neighborhoods = response.data
      } catch (error) {
        this.error = 'Failed to fetch neighborhoods.'
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
        const response = await api.getNeighborhoodDetail(id, weights)

        this.selectedNeighborhood = response.data
      } catch (error) {
        this.error = 'Failed to fetch neighborhood details.'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * Update weight values and refresh data
     * @param {Object} weights - Weight object with all indicators
     */
    async updateWeights(weights) {
      this.weights = { ...this.weights, ...weights }
      await this.fetchNeighborhoods()
    },

    /**
     * Reset weights to default
     */
    async resetWeights() {
      this.weights = {
        air: 25,
        noise: 25,
        greenSpaces: 25,
        urbanHeat: 25,
      }
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