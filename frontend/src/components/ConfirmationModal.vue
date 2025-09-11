<!-- frontend/src/components/ConfirmationModal.vue -->
<template>
  <transition name="modal-fade">
    <div v-if="modal.isOpen" class="modal-backdrop" @click="modal.cancel">
      <div class="modal-content" @click.stop>
        <h3>{{ modal.title }}</h3>
        <p>{{ modal.message }}</p>
        <div class="modal-actions">
          <button @click="modal.cancel" class="btn">取消</button>
          <button @click="modal.confirm" class="btn btn-danger">确认</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useModalStore } from '@/store/modal.js'
const modal = useModalStore()
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
  z-index: 1050; /* Ensure it's above other content */
}

.modal-content {
  background-color: var(--color-surface);
  padding: var(--spacing-8);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 420px;
  text-align: center;
  border: var(--border-width) solid var(--color-border);
  /* Add transition for the content itself */
  transition: all 0.3s ease;
  transform: scale(0.95);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: var(--spacing-3);
  font-size: var(--font-size-xl);
  color: var(--color-text);
}

.modal-content p {
  margin-bottom: var(--spacing-6);
  color: var(--color-text-muted);
  font-size: var(--font-size-base);
  line-height: 1.6;
}

.modal-actions {
  display: flex;
  justify-content: flex-end; /* Align buttons to the right for a more standard feel */
  gap: var(--spacing-3);
}

/* Use global button styles from style.css */
.btn-danger {
  background-color: var(--color-danger);
  color: #ffffff;
  border-color: var(--color-danger);
}
.btn-danger:hover:not(:disabled) {
  opacity: 0.9;
}

/* Transition classes */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
  transition: all 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
  transform: scale(0.9);
  opacity: 0;
}

.modal-fade-enter-to .modal-content {
  transform: scale(1);
}
</style>
