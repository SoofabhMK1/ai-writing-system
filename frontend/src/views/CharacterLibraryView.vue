<template>
  <WorkspaceLayout>
    <template #left>
      <div class="left-panel-inner">
        <button
          @click="isCreateModalOpen = true"
          class="btn btn-primary create-button"
        >
          创建新角色
        </button>
      </div>
    </template>
    <template #right>
      <div class="right-panel-inner">
        <CharacterList @view-character="handleViewCharacter" />
      </div>
    </template>
  </WorkspaceLayout>
  <CreateCharacterModal
    v-if="isCreateModalOpen"
    @close="isCreateModalOpen = false"
  />
  <CharacterDetailModal
    v-if="selectedCharacterId"
    :character-id="selectedCharacterId"
    @close="handleCloseDetailModal"
  />
</template>

<script setup>
import { ref, watch } from 'vue'
import { useCharacterStore } from '@/store/character'
import { useModalStore } from '@/store/modal'
import WorkspaceLayout from '@/components/layout/WorkspaceLayout.vue'
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
.left-panel-inner,
.right-panel-inner {
  padding: var(--spacing-6);
  height: 100%;
  overflow-y: auto;
}

.create-button {
  width: 100%;
}
</style>
