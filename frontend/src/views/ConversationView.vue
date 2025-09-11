<template>
  <div class="conversation-workspace">
    <ConversationSidebar class="sidebar-panel" />
    <div class="chat-panel">
      <ChatInterface />
      <ChatInput />
    </div>
  </div>
</template>

<script setup>
import ConversationSidebar from '../components/ConversationSidebar.vue'
import ChatInterface from '../components/ChatInterface.vue'
import ChatInput from '../components/ChatInput.vue'
</script>

<style scoped>
.conversation-workspace {
  display: flex;
  height: 100%;
  gap: var(--spacing-8);
}

.sidebar-panel {
  width: 320px;
  min-width: 280px;
  flex-shrink: 0;
}

.chat-panel {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  min-height: 0; /* Crucial for flex-grow to work in a flex column */
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}
</style>
