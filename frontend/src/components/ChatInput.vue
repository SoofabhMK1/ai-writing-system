<template>
  <div class="chat-input-area">
    <textarea
      v-model="prompt"
      @keydown.enter.exact.prevent="handleSend"
      class="chat-textarea"
      rows="1"
      placeholder="输入消息... (Shift+Enter 换行)"
    ></textarea>
    <button
      @click="isAssistantModalVisible = true"
      class="btn"
      title="输入辅助"
    >
      辅助
    </button>
    <button
      @click="handleSend"
      class="btn btn-primary send-button"
      :disabled="isLoading"
    >
      发送
    </button>
  </div>
  <InputAssistantModal
    v-if="isAssistantModalVisible"
    @close="isAssistantModalVisible = false"
    @confirm="handleAssistantConfirm"
  />
</template>

<script setup>
import { ref, watch } from 'vue'
import InputAssistantModal from './InputAssistantModal.vue'
import { storeToRefs } from 'pinia'
import { useConversationStore } from '../store/conversation'

const prompt = ref('')
const isAssistantModalVisible = ref(false)
const conversationStore = useConversationStore()
const { promptForInput, isLoading, selectedAiModel } = storeToRefs(
  conversationStore,
)

const handleAssistantConfirm = (content) => {
  prompt.value = content
}

const handleSend = async () => {
  if (!prompt.value.trim() || isLoading.value) return

  const messageWasSent = await conversationStore.sendMessage(
    prompt.value,
    selectedAiModel.value,
  )

  if (messageWasSent) {
    prompt.value = ''
  }
}

watch(promptForInput, (newValue) => {
  if (newValue) {
    prompt.value = newValue
    // Reset the store value after consuming it
    conversationStore.promptForInput = ''
  }
})
</script>

<style scoped>
.chat-input-area {
  flex-shrink: 0;
  padding: var(--spacing-4);
  background-color: var(--color-background);
  border-top: var(--border-width) solid var(--color-border);
  display: flex;
  align-items: flex-end;
  gap: var(--spacing-2);
}
.chat-textarea {
  flex-grow: 1;
  padding: var(--spacing-3) var(--spacing-4);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  font-family: inherit;
  background-color: var(--color-surface);
  color: var(--color-text);
  resize: none;
  overflow-y: auto;
  max-height: 200px;
  line-height: 1.5;
  transition: var(--transition-base);
}
.chat-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary), 0.2);
}
.send-button {
  flex-shrink: 0;
}
</style>
