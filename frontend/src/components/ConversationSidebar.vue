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
        <input type="checkbox" id="preview-toggle" v-model="previewBeforeSending" class="custom-checkbox" />
        <label for="preview-toggle">发送前预览</label>
      </div>
    </div>
    <ul class="history-list">
      <li 
        v-for="item in historyList" 
        :key="item.id"
        class="history-item"
        :class="{ 'active': item.id === currentConversationId }"
      >
        <span @click="loadConversation(item.id)" class="history-item-title">{{ item.title || '未命名对话' }}</span>
        <button @click.stop="handleDelete(item.id)" class="btn-delete">×</button>
      </li>
    </ul>
    <div class="sidebar-footer">
      <button @click="handleSave" class="btn btn-success">
        保存对话
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useConversationStore } from '../store/conversation';
import { useModalStore } from '../store/modal';
import { useRoute } from 'vue-router';

const route = useRoute();
const conversationStore = useConversationStore();
const modal = useModalStore();
const { historyList, currentConversationId, cachedInitialPrompt, previewBeforeSending } = storeToRefs(conversationStore);
const { 
  loadConversationHistory, 
  loadConversation, 
  startNewConversation, 
  saveCurrentConversation,
  fillInputWithCachedPrompt,
  deleteConversation
} = conversationStore;

const handleSave = () => {
  saveCurrentConversation(route.params.projectId);
};

const handleDelete = async (conversationId) => {
  try {
    await modal.show('Confirm Deletion', 'Are you sure you want to delete this conversation?');
    await deleteConversation(conversationId, route.params.projectId);
  } catch (err) {
    if (err.isCanceled) {
      // User canceled the deletion
    } else {
      // Handle other errors if needed
      console.error("Deletion failed:", err);
    }
  }
};

onMounted(() => {
  loadConversationHistory(route.params.projectId);
});
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
.history-list {
  flex-grow: 1;
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
