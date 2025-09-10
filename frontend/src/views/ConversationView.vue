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
import ConversationSidebar from '../components/ConversationSidebar.vue';
import ChatInterface from '../components/ChatInterface.vue';
import ChatInput from '../components/ChatInput.vue';
</script>

<style scoped>
.conversation-workspace {
  display: flex;
  height: calc(100vh - 100px); /* 60px for NavBar + 40px for main container padding */
  gap: 1rem;
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
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}
</style>
