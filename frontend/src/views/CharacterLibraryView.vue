<template>
  <div class="page-container">
    <div class="left-panel">
      <button @click="isCreateModalOpen = true" class="create-button">Create New Character</button>
    </div>
    <div class="right-panel">
      <CharacterList @view-character="handleViewCharacter" />
    </div>
    <CreateCharacterModal v-if="isCreateModalOpen" @close="isCreateModalOpen = false" />
    <CharacterDetailModal 
      v-if="selectedCharacterId" 
      :character-id="selectedCharacterId" 
      @close="handleCloseDetailModal" 
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useCharacterStore } from '@/store/character';
import { useModalStore } from '@/store/modal';
import CharacterList from '@/components/CharacterList.vue';
import CreateCharacterModal from '@/components/CreateCharacterModal.vue';
import CharacterDetailModal from '@/components/CharacterDetailModal.vue';

const characterStore = useCharacterStore();
const modalStore = useModalStore();
const isCreateModalOpen = ref(false);
const selectedCharacterId = ref(null);

watch(isCreateModalOpen, (newValue) => {
  modalStore.setActive(newValue);
});

watch(selectedCharacterId, (newValue) => {
  modalStore.setActive(!!newValue);
});

const handleViewCharacter = (id) => {
  selectedCharacterId.value = id;
};

const handleCloseDetailModal = () => {
  selectedCharacterId.value = null;
  characterStore.clearSelectedCharacter();
};
</script>

<style scoped>
.page-container {
  display: flex;
  height: calc(100vh - 60px); /* 假设 NavBar 高度为 60px */
  background-color: #f7f8fa;
  padding: 1rem;
  gap: 1rem;
}

.left-panel {
  width: 280px;
  flex-shrink: 0; /* Prevent this panel from shrinking */
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.create-button {
  width: 100%;
  padding: 0.8rem 1.5rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}

.create-button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.right-panel {
  flex-grow: 1;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow-y: auto;
}
</style>
