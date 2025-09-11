<template>
  <div class="character-list-container">
    <h2 class="list-title">Character Library</h2>
    <div v-if="characterStore.isLoading" class="loading">Loading...</div>
    <div v-else-if="characterStore.characters.length === 0" class="no-characters">
      No characters found. Create one to get started!
    </div>
    <div v-else class="grid">
      <div v-for="character in characterStore.characters" :key="character.id" class="character-card">
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

const characterStore = useCharacterStore();

onMounted(() => {
  characterStore.fetchCharacters();
});
</script>

<style scoped>
.character-list-container {
  padding: 20px;
}
.list-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 20px;
}
.loading, .no-characters {
  text-align: center;
  color: #666;
  font-size: 1.2rem;
  margin-top: 40px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}
.character-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: box-shadow 0.3s;
}
.character-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.character-name {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 10px;
}
.character-details {
  color: #6b7280;
  margin-bottom: 15px;
}
.character-intro {
  color: #374151;
}
</style>
