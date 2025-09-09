<!-- frontend/src/components/ConfirmationModal.vue -->
<template>
  <transition name="modal-fade">
    <div v-if="modal.isOpen" class="modal-backdrop" @click="modal.cancel">
      <div class="modal-content" @click.stop>
        <h3>{{ modal.title }}</h3>
        <p>{{ modal.message }}</p>
        <div class="modal-actions">
          <button @click="modal.cancel" class="btn btn-secondary">取消</button>
          <button @click="modal.confirm" class="btn btn-danger">确认</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useModalStore } from '@/store/modal.js';
const modal = useModalStore();
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
  max-width: 400px;
  text-align: center;
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.modal-content p {
  margin-bottom: 2rem;
  color: #666;
  font-size: 1.1rem;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ccc;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}

.btn-danger {
  background-color: #e94b3c;
  color: white;
}

.btn-danger:hover {
  background-color: #d93a2b;
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
