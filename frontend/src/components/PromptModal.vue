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
            class="prompt-input"
            required
          />
          <div class="modal-actions">
            <button type="button" @click="handleCancel" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary">确认</button>
          </div>
        </form>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import { usePromptStore } from '@/store/prompt.js';

const prompt = usePromptStore();
const inputValue = ref('');
const inputRef = ref(null);

// 当模态框打开时，自动聚焦到输入框
watch(() => prompt.isOpen, (isOpen) => {
  if (isOpen) {
    inputValue.value = prompt.defaultValue || '';
    nextTick(() => {
      inputRef.value?.focus();
    });
  }
});

const handleConfirm = () => {
  prompt.confirm(inputValue.value);
};

const handleCancel = () => {
  prompt.cancel();
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 450px;
  text-align: center;
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.modal-content p {
  margin-bottom: 1.5rem;
  color: #666;
}

.prompt-input {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1.5rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}

.prompt-input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}

.btn-primary {
  background-color: #4a90e2;
  color: white;
}

.btn-primary:hover {
  background-color: #357abd;
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
