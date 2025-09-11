<!-- frontend/src/components/PromptModal.vue -->
<template>
  <transition name="modal-fade">
    <div v-if="prompt.isOpen" class="modal-backdrop" @click="handleCancel">
      <div class="modal-content" @click.stop>
        <h3>{{ prompt.title }}</h3>
        <p>{{ prompt.message }}</p>
        <form @submit.prevent="handleConfirm">
          <input
            ref="inputRef"
            v-model="inputValue"
            type="text"
            class="form-control"
            required
          />
          <div class="modal-actions">
            <button type="button" @click="handleCancel" class="btn">
              取消
            </button>
            <button type="submit" class="btn btn-primary">确认</button>
          </div>
        </form>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { usePromptStore } from '@/store/prompt.js'

const prompt = usePromptStore()
const inputValue = ref('')
const inputRef = ref(null)

// 当模态框打开时，自动聚焦到输入框
watch(
  () => prompt.isOpen,
  (isOpen) => {
    if (isOpen) {
      inputValue.value = prompt.defaultValue || ''
      nextTick(() => {
        inputRef.value?.focus()
      })
    }
  },
)

const handleConfirm = () => {
  prompt.confirm(inputValue.value)
}

const handleCancel = () => {
  prompt.cancel()
}
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
  max-width: 450px;
  text-align: center;
  border: var(--border-width) solid var(--color-border);
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
}

.form-control {
  width: 100%;
  padding: var(--spacing-3) var(--spacing-4);
  margin-bottom: var(--spacing-6);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  background-color: var(--color-background);
  color: var(--color-text);
  transition: var(--transition-base);
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary), 0.2);
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
