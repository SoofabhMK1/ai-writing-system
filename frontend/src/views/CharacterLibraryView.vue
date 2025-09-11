<template>
  <div class="workspace-container">
    <div class="left-panel">
      <button
        @click="isCreateModalOpen = true"
        class="btn btn-primary create-button"
      >
        创建新角色
      </button>
    </div>
    <div class="right-panel">
      <CharacterList @view-character="handleViewCharacter" />
    </div>
    <CreateCharacterModal
      v-if="isCreateModalOpen"
      @close="isCreateModalOpen = false"
    />
    <CharacterDetailModal
      v-if="selectedCharacterId"
      :character-id="selectedCharacterId"
      @close="handleCloseDetailModal"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useCharacterStore } from '@/store/character'
import { useModalStore } from '@/store/modal'
import CharacterList from '@/components/CharacterList.vue'
import CreateCharacterModal from '@/components/CreateCharacterModal.vue'
import CharacterDetailModal from '@/components/CharacterDetailModal.vue'

const characterStore = useCharacterStore()
const modalStore = useModalStore()
const isCreateModalOpen = ref(false)
const selectedCharacterId = ref(null)

watch(isCreateModalOpen, (newValue) => {
  modalStore.setActive(newValue)
})

watch(selectedCharacterId, (newValue) => {
  modalStore.setActive(!!newValue)
})

const handleViewCharacter = (id) => {
  selectedCharacterId.value = id
}

const handleCloseDetailModal = () => {
  selectedCharacterId.value = null
  characterStore.clearSelectedCharacter()
}
</script>

<style scoped>
.workspace-container {
  display: flex;
  height: 100%;
  gap: var(--spacing-8);
}

.left-panel {
  width: 280px;
  flex-shrink: 0;
  padding: var(--spacing-6);
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.create-button {
  width: 100%;
}

.right-panel {
  flex-grow: 1;
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  overflow-y: auto;
  padding: var(--spacing-6);
}
</style>
