<template>
  <div class="character-list-container">
    <h2 class="list-title">Character Library</h2>
    <div v-if="characterStore.isLoading" class="loading">Loading...</div>
    <div v-else-if="characterStore.characters.length === 0" class="no-characters">
      No characters found. Create one to get started!
    </div>
    <div v-else class="grid">
      <div 
        v-for="character in characterStore.characters" 
        :key="character.id" 
        class="character-card"
        @click="viewCharacter(character.id)"
      >
        <h3 class="character-name">{{ character.name }}</h3>
        <p class="character-details">{{ character.age }} | {{ character.occupation }}</p>
        <p class="character-intro">{{ character.brief_introduction }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useCharacterStore } from '@/store/character';

const emit = defineEmits(['view-character']);
const characterStore = useCharacterStore();

onMounted(() => {
  characterStore.fetchCharacters();
});

const viewCharacter = (id) => {
  emit('view-character', id);
};
</script>

<style scoped>
.character-list-container {
  height: 100%;
}
.list-title {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--spacing-6);
  padding-bottom: var(--spacing-4);
  border-bottom: var(--border-width) solid var(--color-border);
}
.loading, .no-characters {
  text-align: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-base);
  margin-top: var(--spacing-12);
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-6);
}
.character-card {
  background: var(--color-surface);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-base);
  cursor: pointer;
}
.character-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-4px);
  border-color: var(--color-primary);
}
.character-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--spacing-2);
}
.character-details {
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  margin-bottom: var(--spacing-4);
}
.character-intro {
  color: var(--color-text);
  font-size: var(--font-size-sm);
  line-height: 1.6;
}
</style>
