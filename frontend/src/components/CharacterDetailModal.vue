<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content" v-if="character">
      <div class="modal-header">
        <h2 class="modal-title">
          {{ isEditing ? '编辑角色' : character.name }}
        </h2>
        <button @click="$emit('close')" class="close-button">&times;</button>
      </div>

      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab"
          :class="['tab-button', { active: activeTab === tab }]"
          @click="activeTab = tab"
        >
          {{ tab }}
        </button>
      </div>

      <CharacterDetailDisplay
        v-if="!isEditing"
        :character="character"
        :active-tab="activeTab"
      />
      <CharacterDetailEdit
        v-else
        :editable-character="editableCharacter"
        :active-tab="activeTab"
        @update:editable-character="editableCharacter = $event"
      />

      <div class="modal-actions">
        <template v-if="!isEditing">
          <button @click="handleDelete" class="btn btn-danger">删除</button>
          <button @click="enterEditMode" class="btn btn-primary">更新</button>
        </template>
        <template v-else>
          <button @click="cancelEdit" class="btn">取消</button>
          <button @click="saveChanges" class="btn btn-success">保存</button>
        </template>
      </div>
    </div>
    <div v-else class="loading">正在加载...</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCharacterStore } from '@/store/character'
import { useModalStore } from '@/store/modal'
import CharacterDetailDisplay from './CharacterDetailDisplay.vue'
import CharacterDetailEdit from './CharacterDetailEdit.vue'

const props = defineProps({ characterId: { type: Number, required: true } })
const emit = defineEmits(['close'])

const characterStore = useCharacterStore()
const modalStore = useModalStore()

const character = computed(() => characterStore.selectedCharacter)
const isEditing = ref(false)
const editableCharacter = ref(null)
const activeTab = ref('基本信息')
const tabs = ['基本信息', '外貌特征', '性格与背景', '其他']

onMounted(() => {
  characterStore.fetchCharacter(props.characterId)
})

watch(
  character,
  (newChar) => {
    if (newChar) {
      editableCharacter.value = JSON.parse(JSON.stringify(newChar))
    }
  },
  { deep: true, immediate: true },
)

const enterEditMode = () => {
  isEditing.value = true
}

const cancelEdit = () => {
  editableCharacter.value = JSON.parse(JSON.stringify(character.value))
  isEditing.value = false
}

const saveChanges = async () => {
  await characterStore.updateCharacter({
    id: props.characterId,
    data: editableCharacter.value,
  })
  isEditing.value = false
}

const handleDelete = async () => {
  try {
    await modalStore.show(
      '确认删除',
      `你确定要删除角色“${character.value.name}”吗？此操作不可撤销。`,
    )
    await characterStore.deleteCharacter(props.characterId)
    emit('close')
  } catch (error) {
    if (!error.isCanceled) console.error('Deletion error:', error)
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}
.modal-content {
  background: var(--color-surface);
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 800px;
  height: 85vh;
  max-height: 800px;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-lg);
  border: var(--border-width) solid var(--color-border);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-5) var(--spacing-8);
  border-bottom: var(--border-width) solid var(--color-border);
}
.modal-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
}
.close-button {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: var(--color-text-muted);
  transition: var(--transition-base);
}
.close-button:hover {
  color: var(--color-text);
}
.loading {
  color: var(--color-text);
  font-size: var(--font-size-lg);
}
.tabs {
  display: flex;
  padding: 0 var(--spacing-8);
  border-bottom: var(--border-width) solid var(--color-border);
  gap: var(--spacing-6);
}
.tab-button {
  padding: var(--spacing-4) 0;
  border: none;
  background: none;
  cursor: pointer;
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
  position: relative;
  border-bottom: 2px solid transparent;
  transition: var(--transition-base);
}
.tab-button:hover {
  color: var(--color-text);
}
.tab-button.active {
  color: var(--color-primary);
  font-weight: 600;
  border-bottom-color: var(--color-primary);
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-4);
  padding: var(--spacing-5) var(--spacing-8);
  border-top: var(--border-width) solid var(--color-border);
  background-color: var(--color-background);
}
.btn-success {
  background-color: var(--color-success);
  color: #ffffff;
  border-color: var(--color-success);
}
.btn-success:hover:not(:disabled) {
  opacity: 0.9;
}
</style>
