<template>
  <div class="sidebar-container">
    <div class="sidebar-header">
      <button @click="startNewConversation" class="btn btn-primary">
        New Conversation
      </button>
      <button
        v-if="cachedInitialPrompt"
        @click="fillInputWithCachedPrompt"
        class="btn btn-secondary"
      >
        Use Initial Prompt
      </button>
    </div>
    <ul class="history-list">
      <li 
        v-for="item in historyList" 
        :key="item.id"
        class="history-item"
        :class="{ 'active': item.id === currentConversationId }"
      >
        <span @click="loadConversation(item.id)" class="history-item-title">{{ item.title || 'Untitled Conversation' }}</span>
        <button @click.stop="handleDelete(item.id)" class="btn-delete">X</button>
      </li>
    </ul>
    <div class="sidebar-footer">
      <button @click="handleSave" class="btn btn-success">
        Save Conversation
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
const { historyList, currentConversationId, cachedInitialPrompt } = storeToRefs(conversationStore);
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
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}
.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.history-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 0.5rem;
  list-style: none;
  margin: 0;
}
.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
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
  color: #aaa;
  cursor: pointer;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  flex-shrink: 0;
  margin-left: 0.5rem;
  visibility: hidden; /* Hide by default */
}
.history-item:hover .btn-delete {
  visibility: visible; /* Show on hover */
}
.btn-delete:hover {
  color: #e53e3e;
  background-color: #fed7d7;
}
.history-item:hover {
  background-color: #f0f5ff;
}
.history-item.active {
  background-color: #4a90e2;
  color: white;
  font-weight: 500;
}
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
}
.btn {
  width: 100%;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}
.btn:hover {
  transform: translateY(-2px);
}
.btn-primary {
  background-color: #4a90e2;
  color: white;
}
.btn-primary:hover {
  background-color: #357abd;
}
.btn-secondary {
  background-color: #f0ad4e;
  color: white;
}
.btn-secondary:hover {
  background-color: #ec971f;
}
.btn-success {
  background-color: #5cb85c;
  color: white;
}
.btn-success:hover {
  background-color: #449d44;
}
</style>
