import { defineStore } from 'pinia';
import characterService from '@/services/characterService';

export const useCharacterStore = defineStore('character', {
  state: () => ({
    characters: [],
    isLoading: false,
  }),
  actions: {
    async fetchCharacters() {
      this.isLoading = true;
      try {
        const response = await characterService.getCharacters();
        this.characters = response.data;
      } catch (error) {
        console.error('Failed to fetch characters:', error);
        // You might want to dispatch a notification here
      } finally {
        this.isLoading = false;
      }
    },
    async createCharacter(characterData) {
      this.isLoading = true;
      try {
        const response = await characterService.createCharacter(characterData);
        this.characters.push(response.data);
      } catch (error) {
        console.error('Failed to create character:', error);
        // You might want to dispatch a notification here
      } finally {
        this.isLoading = false;
      }
    },
  },
});
