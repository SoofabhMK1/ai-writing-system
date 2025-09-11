<template>
  <div class="chat-interface" ref="chatContainer">
    <div v-if="!messages.length" class="empty-chat">
      <p>Start the conversation by typing below.</p>
    </div>
    <div v-else>
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="message-group"
        :class="`role-${message.role}`"
      >
        <div class="avatar">
          {{ message.role === 'user' ? 'U' : 'AI' }}
        </div>
        <div
          class="message-content prose"
          v-html="renderMarkdown(message.content)"
        ></div>
      </div>
      <div v-if="isLoading" class="message-group role-assistant">
        <div class="avatar">AI</div>
        <div class="message-content prose">
          <p>Thinking...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useConversationStore } from '../store/conversation'
import { marked } from 'marked'

const chatContainer = ref(null)
const conversationStore = useConversationStore()
const { messages, isLoading } = storeToRefs(conversationStore)

const renderMarkdown = (content) => {
  return marked.parse(content || '')
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

watch(
  messages,
  () => {
    scrollToBottom()
  },
  { deep: true },
)

watch(isLoading, (newValue) => {
  if (newValue) {
    scrollToBottom()
  }
})
</script>

<style scoped>
.chat-interface {
  flex-grow: 1;
  overflow-y: auto;
  padding: var(--spacing-8);
}
.empty-chat {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: var(--color-text-muted);
  font-size: var(--font-size-lg);
}
.message-group {
  display: flex;
  gap: var(--spacing-4);
  margin-bottom: var(--spacing-6);
  max-width: 90%;
}
.avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-full);
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
  font-size: var(--font-size-sm);
}
.role-user {
  justify-content: flex-end;
  margin-left: auto;
}
.role-user .avatar {
  background-color: var(--color-secondary);
  order: 2;
}
.role-user .message-content {
  background-color: var(--color-primary);
  color: white;
  border-radius: var(--border-radius-lg) var(--border-radius-lg) 0
    var(--border-radius-lg);
  order: 1;
}
.role-assistant .avatar {
  background-color: var(--color-primary);
}
.message-content {
  padding: var(--spacing-3) var(--spacing-5);
  border-radius: var(--border-radius-lg);
  background-color: var(--color-background);
  border: var(--border-width) solid var(--color-border);
  line-height: 1.6;
}
/* Styling for markdown content */
.prose {
  max-width: none;
}
:deep(.prose > *:first-child) {
  margin-top: 0;
}
:deep(.prose > *:last-child) {
  margin-bottom: 0;
}
:deep(.prose p) {
  margin-bottom: 1em;
}
:deep(.prose pre) {
  background-color: var(--color-background);
  color: var(--color-text);
  padding: var(--spacing-4);
  border-radius: var(--border-radius-md);
  border: var(--border-width) solid var(--color-border);
  white-space: pre-wrap;
}
:deep(.prose code) {
  background-color: rgba(128, 128, 128, 0.15);
  padding: 0.2em 0.4em;
  border-radius: var(--border-radius-sm);
  font-size: 0.9em;
}
:deep(.prose pre code) {
  background-color: transparent;
  padding: 0;
}
:deep(.message-content *) {
  overflow-wrap: break-word;
  max-width: 100%;
}
</style>
