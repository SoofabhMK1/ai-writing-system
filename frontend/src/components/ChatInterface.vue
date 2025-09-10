<template>
  <div class="chat-interface" ref="chatContainer">
    <div v-if="!messages.length" class="empty-chat">
      <p>Start the conversation by typing below.</p>
    </div>
    <div v-else>
      <div v-for="(message, index) in messages" :key="index" class="message-group" :class="`role-${message.role}`">
        <div class="avatar">
          {{ message.role === 'user' ? 'U' : 'AI' }}
        </div>
        <div class="message-content prose" v-html="renderMarkdown(message.content)"></div>
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
import { ref, watch, nextTick } from 'vue';
import { storeToRefs } from 'pinia';
import { useConversationStore } from '../store/conversation';
import { marked } from 'marked';

const chatContainer = ref(null);
const conversationStore = useConversationStore();
const { messages, isLoading } = storeToRefs(conversationStore);

const renderMarkdown = (content) => {
  return marked.parse(content || '');
};

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
};

watch(messages, () => {
  scrollToBottom();
}, { deep: true });

watch(isLoading, (newValue) => {
  if (newValue) {
    scrollToBottom();
  }
});
</script>

<style scoped>
.chat-interface {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1.5rem;
}
.empty-chat {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #888;
  font-size: 1.2rem;
}
.message-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  color: white;
  flex-shrink: 0;
}
.role-user .avatar {
  background-color: #6c757d;
}
.role-assistant .avatar {
  background-color: #4a90e2;
}
.message-content {
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  max-width: 80%;
}
.role-user .message-content {
  background-color: #f1f3f5;
}
.role-assistant .message-content {
  background-color: #e7f3ff;
}
/* Styling for markdown content */
.prose {
  max-width: none;
}
:deep(.prose p) {
  margin: 0;
}
:deep(.prose pre) {
  background-color: #2d3748;
  color: #e2e8f0;
  padding: 1rem;
  border-radius: 8px;
  white-space: pre-wrap; /* Ensure preformatted text wraps */
}

:deep(.message-content *) {
  overflow-wrap: break-word;
}
</style>
