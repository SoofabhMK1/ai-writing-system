<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-backdrop" @click="cancel">
      <div class="modal-content" @click.stop>
        <h3>确认发送内容</h3>
        <div class="preview-content">
          <pre>{{ content }}</pre>
        </div>
        <div class="modal-actions">
          <button @click="cancel" class="btn">取消</button>
          <button @click="confirm" class="btn btn-primary">继续</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  isOpen: Boolean,
  content: String,
  confirm: Function,
  cancel: Function,
});
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background-color: var(--color-surface);
  padding: var(--spacing-8);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  max-height: 80vh;
  border: var(--border-width) solid var(--color-border);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: var(--spacing-6);
  font-size: var(--font-size-xl);
  color: var(--color-text);
  text-align: center;
}

.preview-content {
  flex-grow: 1;
  overflow-y: auto;
  background-color: var(--color-background);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-4);
  margin-bottom: var(--spacing-6);
}

.preview-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
  font-family: 'Courier New', Courier, monospace;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-4);
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
