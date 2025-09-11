<template>
  <NavBar />
  <main class="main-container">
    <router-view></router-view>
  </main>
  <ConfirmationModal />
  <Notification />
  <PromptModal />
  <PreviewSendModal 
    :is-open="isPreviewOpen"
    :content="previewContent"
    :confirm="modal.confirmPreview"
    :cancel="modal.cancelPreview"
  />
</template>

<script setup>
import { watch } from 'vue';
import { storeToRefs } from 'pinia';
import NavBar from './components/NavBar.vue';
import ConfirmationModal from './components/ConfirmationModal.vue';
import Notification from './components/Notification.vue';
import PromptModal from './components/PromptModal.vue';
import PreviewSendModal from './components/PreviewSendModal.vue';
import { useModalStore } from './store/modal';

const modal = useModalStore();
const { isPreviewOpen, previewContent, isAnyModalOpen } = storeToRefs(modal);

watch(isAnyModalOpen, (newValue) => {
  if (newValue) {
    document.body.classList.add('modal-open');
  } else {
    document.body.classList.remove('modal-open');
  }
});
</script>

<style>
/* 将样式移出 scoped，使其成为全局样式 */
body {
  margin: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #f4f7f9;
}

.main-container {
  width: 100%;
  box-sizing: border-box; /* 确保 padding 不会撑大容器 */
  margin: 0 auto;
  padding: 20px;
}
</style>
