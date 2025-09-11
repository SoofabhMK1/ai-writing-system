import { defineStore } from 'pinia'
import characterService from '@/services/characterService'

export const useCharacterStore = defineStore('character', {
  state: () => ({
    characters: [],
    isLoading: false,
    selectedCharacter: null,
  }),
  actions: {
    async fetchCharacters() {
      this.isLoading = true
      try {
        const response = await characterService.getCharacters()
        this.characters = response.data
      } catch (error) {
        console.error('Failed to fetch characters:', error)
        // You might want to dispatch a notification here
      } finally {
        this.isLoading = false
      }
    },
    async createCharacter(characterData) {
      this.isLoading = true
      try {
        const response = await characterService.createCharacter(characterData)
        this.characters.push(response.data)
      } catch (error) {
        console.error('Failed to create character:', error)
        // You might want to dispatch a notification here
      } finally {
        this.isLoading = false
      }
    },
    async fetchCharacter(id) {
      this.isLoading = true
      try {
        const response = await characterService.getCharacterById(id)
        this.selectedCharacter = response.data
      } catch (error) {
        console.error('Failed to fetch character:', error)
        this.selectedCharacter = null
      } finally {
        this.isLoading = false
      }
    },
    async deleteCharacter(id) {
      this.isLoading = true
      try {
        await characterService.deleteCharacter(id)
        this.characters = this.characters.filter((c) => c.id !== id)
        if (this.selectedCharacter && this.selectedCharacter.id === id) {
          this.selectedCharacter = null
        }
      } catch (error) {
        console.error('Failed to delete character:', error)
      } finally {
        this.isLoading = false
      }
    },
    async updateCharacter({ id, data }) {
      this.isLoading = true
      try {
        const response = await characterService.updateCharacter(id, data)
        // Update the selected character details
        this.selectedCharacter = response.data
        // Update the character in the list
        const index = this.characters.findIndex((c) => c.id === id)
        if (index !== -1) {
          this.characters[index] = response.data
        }
      } catch (error) {
        console.error('Failed to update character:', error)
        // Optionally, re-fetch the original data to revert changes on failure
        if (this.selectedCharacter && this.selectedCharacter.id === id) {
          this.fetchCharacter(id)
        }
      } finally {
        this.isLoading = false
      }
    },
    clearSelectedCharacter() {
      this.selectedCharacter = null
    },
  },
})
