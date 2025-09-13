<template>
  <WorkspaceLayout>
    <template #left>
      <ConversationSidebar />
    </template>
    <template #right>
      <div class="right-panel-inner">
        <ChatInterface />
        <ChatInput />
      </div>
    </template>
  </WorkspaceLayout>
</template>

<script setup>
import WorkspaceLayout from '@/components/layout/WorkspaceLayout.vue'
import ConversationSidebar from '../components/ConversationSidebar.vue'
import ChatInterface from '../components/ChatInterface.vue'
import ChatInput from '../components/ChatInput.vue'
</script>

<style scoped>
.right-panel-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>
