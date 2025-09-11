<template>
  <div class="page-container">
    <div class="left-panel">
      <button @click="isModalOpen = true" class="create-button">Create New Character</button>
    </div>
    <div class="right-panel">
      <CharacterList />
    </div>
    <CreateCharacterModal v-if="isModalOpen" @close="isModalOpen = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CharacterList from '@/components/CharacterList.vue';
import CreateCharacterModal from '@/components/CreateCharacterModal.vue';

const isModalOpen = ref(false);
</script>

<style scoped>
.page-container {
  display: flex;
  height: calc(100vh - 60px); /* Full height minus navbar */
}

.left-panel {
  width: 350px;
  padding: 20px;
  background-color: #f9fafb;
  border-right: 1px solid #e5e7eb;
  overflow-y: auto;
}

.create-button {
  width: 100%;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s;
}

.create-button:hover {
  background-color: #357abd;
}

.right-panel {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #ffffff;
}
</style>
