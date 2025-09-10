<template>
  <div class="chat-input-area">
    <textarea
      v-model="prompt"
      @keydown.enter.exact.prevent="handleSend"
      class="chat-textarea"
      rows="3"
      placeholder="Type your message... (Shift+Enter for new line)"
    ></textarea>
    <button @click="handleSend" class="send-button" :disabled="isLoading">
      Send
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { useConversationStore } from '../store/conversation';

const prompt = ref('');
const conversationStore = useConversationStore();
const { promptForInput, isLoading } = storeToRefs(conversationStore);

// This is a placeholder. In a real app, you'd get this from a settings store or component.
const AI_MODEL_ID = 1; 

const handleSend = () => {
  if (!prompt.value.trim() || isLoading.value) return;
  conversationStore.sendMessage(prompt.value, AI_MODEL_ID);
  prompt.value = '';
};

watch(promptForInput, (newValue) => {
  if (newValue) {
    prompt.value = newValue;
    // Reset the store value after consuming it
    conversationStore.promptForInput = '';
  }
});

</script>

<style scoped>
.chat-input-area {
  flex-shrink: 0;
  padding: 1rem;
  background-color: #f1f3f5;
  border-top: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.chat-textarea {
  flex-grow: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  overflow-y: auto; /* Show scrollbar when content overflows */
  max-height: 150px; /* Limit max height */
}
.send-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  background-color: #4a90e2;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}
.send-button:hover {
  background-color: #357abd;
}
.send-button:disabled {
  background-color: #a0c7e8;
  cursor: not-allowed;
}
</style>
