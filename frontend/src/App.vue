<template>
  <div id="app-layout">
    <NavBar />
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
  <ConfirmationModal />
  <AppNotification />
  <PromptModal />
  <PreviewSendModal
    :is-open="isPreviewOpen"
    :content="previewContent"
    :confirm="modal.confirmPreview"
    :cancel="modal.cancelPreview"
  />
</template>

<script setup>
import { watch } from 'vue'
import { storeToRefs } from 'pinia'
import NavBar from './components/NavBar.vue'
import ConfirmationModal from './components/ConfirmationModal.vue'
import AppNotification from './components/AppNotification.vue'
import PromptModal from './components/PromptModal.vue'
import PreviewSendModal from './components/PreviewSendModal.vue'
import { useModalStore } from './store/modal'

const modal = useModalStore()
const { isPreviewOpen, previewContent, isAnyModalOpen } = storeToRefs(modal)

watch(isAnyModalOpen, (newValue) => {
  if (newValue) {
    document.body.classList.add('modal-open')
  } else {
    document.body.classList.remove('modal-open')
  }
})
</script>

<style scoped>
#app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: var(--spacing-8);
  width: 100%;
  max-width: 1400px; /* Optional: constrain max width for very large screens */
  margin: 0 auto;
  box-sizing: border-box;
}
</style>
