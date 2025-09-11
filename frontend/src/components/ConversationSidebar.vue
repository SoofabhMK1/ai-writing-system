<template>
  <div class="sidebar-container">
    <div class="sidebar-header">
      <button @click="startNewConversation" class="btn btn-primary">
        新对话
      </button>
      <button
        v-if="cachedInitialPrompt"
        @click="fillInputWithCachedPrompt"
        class="btn"
      >
        使用初始 Prompt
      </button>
      <div class="preview-toggle-container">
        <input
          type="checkbox"
          id="preview-toggle"
          v-model="previewBeforeSending"
          class="custom-checkbox"
        />
        <label for="preview-toggle">发送前预览</label>
      </div>
      <div class="model-selector-container">
        <label for="model-selector">AI 模型:</label>
        <select id="model-selector" v-model="selectedAiModel" class="custom-select">
          <option v-for="model in aiModels" :key="model.id" :value="model.id">
            {{ model.name }}
          </option>
        </select>
      </div>
      <div class="model-selector-container">
        <label for="prefix-selector">系统前缀:</label>
        <select id="prefix-selector" v-model="selectedSystemPrefix" class="custom-select">
          <option :value="null">无</option>
          <option v-for="prefix in systemPrefixes" :key="prefix.id" :value="prefix.template_text">
            {{ prefix.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="history-section">
      <button @click="isHistoryVisible = !isHistoryVisible" class="history-toggle-btn">
        历史对话
        <span :class="['arrow', { rotated: !isHistoryVisible }]">▼</span>
      </button>
      <ul v-show="isHistoryVisible" class="history-list">
        <li
          v-for="item in historyList"
          :key="item.id"
          class="history-item"
          :class="{ active: item.id === currentConversationId }"
        >
          <span @click="loadConversation(item.id)" class="history-item-title">{{
            item.title || '未命名对话'
          }}</span>
          <button @click.stop="handleDelete(item.id)" class="btn-delete">
            ×
          </button>
        </li>
      </ul>
    </div>
    <div class="sidebar-footer">
      <button @click="handleSave" class="btn btn-success">保存对话</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useConversationStore } from '../store/conversation'
import { useModalStore } from '../store/modal'
import { aiModelService, promptTemplateService } from '../services/settingService'

const conversationStore = useConversationStore()
const modal = useModalStore()
const {
  historyList,
  currentConversationId,
  cachedInitialPrompt,
  previewBeforeSending,
  selectedAiModel,
  selectedSystemPrefix,
} = storeToRefs(conversationStore)
const {
  loadConversationHistory,
  loadConversation,
  startNewConversation,
  saveCurrentConversation,
  fillInputWithCachedPrompt,
  deleteConversation,
} = conversationStore

const aiModels = ref([])
const promptTemplates = ref([])
const isHistoryVisible = ref(true)

const systemPrefixes = computed(() =>
  promptTemplates.value.filter((p) => p.category === '系统前缀'),
)

const handleSave = () => {
  saveCurrentConversation()
}

const handleDelete = async (conversationId) => {
  try {
    await modal.show(
      'Confirm Deletion',
      'Are you sure you want to delete this conversation?',
    )
    await deleteConversation(conversationId)
  } catch (err) {
    if (err.isCanceled) {
      // User canceled the deletion
    } else {
      // Handle other errors if needed
      console.error('Deletion failed:', err)
    }
  }
}

onMounted(async () => {
  await loadConversationHistory()
  try {
    const response = await aiModelService.getAll()
    aiModels.value = response.data
    if (aiModels.value.length > 0 && !selectedAiModel.value) {
      // Set a default model if none is selected
      conversationStore.selectedAiModel = aiModels.value[0].id
    }
    const templatesResponse = await promptTemplateService.getAll()
    promptTemplates.value = templatesResponse.data
  } catch (error) {
    console.error('Failed to fetch settings:', error)
  }
})
</script>

<style scoped>
.sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}
.sidebar-header {
  padding: var(--spacing-6);
  border-bottom: var(--border-width) solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}
.preview-toggle-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  padding: var(--spacing-2) 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}
.preview-toggle-container label {
  cursor: pointer;
}
.custom-checkbox {
  appearance: none;
  background-color: var(--color-background);
  border: var(--border-width) solid var(--color-border);
  width: 1.25em;
  height: 1.25em;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  position: relative;
  transition: var(--transition-base);
}
.custom-checkbox:checked {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
}
.custom-checkbox:checked::after {
  content: '✔';
  position: absolute;
  color: white;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.8em;
}

.model-selector-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.custom-select {
  width: 100%;
  padding: var(--spacing-2) var(--spacing-3);
  background-color: var(--color-background);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-md);
  color: var(--color-text);
  font-size: var(--font-size-sm);
}
.history-section {
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.history-toggle-btn {
  background: none;
  border: none;
  padding: var(--spacing-4);
  width: 100%;
  text-align: left;
  font-size: var(--font-size-base);
  font-weight: 600;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--color-text);
  border-bottom: var(--border-width) solid var(--color-border);
}
.arrow {
  transition: transform 0.2s;
}
.arrow.rotated {
  transform: rotate(-90deg);
}
.history-list {
  overflow-y: auto;
  padding: var(--spacing-4);
  list-style: none;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}
.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-3) var(--spacing-4);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: var(--transition-base);
  color: var(--color-text-muted);
}
.history-item-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-grow: 1;
}
.btn-delete {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  font-weight: bold;
  font-size: 1.2em;
  padding: 0 var(--spacing-2);
  border-radius: var(--border-radius-full);
  flex-shrink: 0;
  margin-left: var(--spacing-3);
  visibility: hidden;
  opacity: 0;
  transition: var(--transition-base);
}
.history-item:hover .btn-delete {
  visibility: visible;
  opacity: 1;
}
.btn-delete:hover {
  color: var(--color-danger);
  background-color: rgba(239, 68, 68, 0.1);
}
.history-item:hover {
  background-color: var(--color-background);
  color: var(--color-text);
}
.history-item.active {
  background-color: var(--color-primary);
  color: white;
  font-weight: 500;
}
.history-item.active .history-item-title {
  color: white;
}
.sidebar-footer {
  padding: var(--spacing-6);
  border-top: var(--border-width) solid var(--color-border);
}
.btn {
  width: 100%;
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
