import { defineStore } from 'pinia';
import { promptPresetService } from '@/services/promptPresetService';
import { useNotificationStore } from './notification';

export const usePromptPresetStore = defineStore('promptPreset', {
  state: () => ({
    presets: [],
    isLoading: false,
  }),
  actions: {
    async fetchPresets() {
      this.isLoading = true;
      try {
        const response = await promptPresetService.getAll();
        this.presets = response.data;
      } catch (error) {
        const notificationStore = useNotificationStore();
        notificationStore.show('Failed to fetch prompt presets.', 'error');
        console.error('Failed to fetch prompt presets:', error);
      } finally {
        this.isLoading = false;
      }
    },
    async createPreset(data) {
      try {
        const response = await promptPresetService.create(data);
        this.presets.push(response.data);
        const notificationStore = useNotificationStore();
        notificationStore.show('Preset created successfully.', 'success');
      } catch (error) {
        const notificationStore = useNotificationStore();
        notificationStore.show('Failed to create preset.', 'error');
        console.error('Failed to create preset:', error);
      }
    },
    async updatePreset(id, data) {
      try {
        const response = await promptPresetService.update(id, data);
        const index = this.presets.findIndex((p) => p.id === id);
        if (index !== -1) {
          this.presets[index] = response.data;
        }
        const notificationStore = useNotificationStore();
        notificationStore.show('Preset updated successfully.', 'success');
      } catch (error) {
        const notificationStore = useNotificationStore();
        notificationStore.show('Failed to update preset.', 'error');
        console.error('Failed to update preset:', error);
      }
    },
    async deletePreset(id) {
      try {
        await promptPresetService.delete(id);
        this.presets = this.presets.filter((p) => p.id !== id);
        const notificationStore = useNotificationStore();
        notificationStore.show('Preset deleted successfully.', 'success');
      } catch (error) {
        const notificationStore = useNotificationStore();
        notificationStore.show('Failed to delete preset.', 'error');
        console.error('Failed to delete preset:', error);
      }
    },
  },
});
