<!-- frontend/src/components/GenerationResultModal.vue -->
<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-card">
      <h3>{{ title }}</h3>
      <div class="modal-content">
        <pre>{{ formattedContent }}</pre>
      </div>
      <div class="form-actions">
        <button type="button" class="btn-cancel" @click="close">关闭</button>
        <button v-if="!isReadOnly" type="button" class="btn-save" @click="save">保存</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    default: '生成结果',
  },
  content: {
    type: Object,
    required: true,
  },
  isReadOnly: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['close', 'save']);

const formattedContent = computed(() => {
  return JSON.stringify(props.content, null, 2);
});

const close = () => {
  emit('close');
};

const save = () => {
  emit('save');
};
</script>

<style scoped>
.modal-overlay {
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

.modal-card {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 500;
  text-align: center;
}

.modal-content {
  overflow-y: auto;
  background-color: #f7f8fa;
  border-radius: 8px;
  padding: 1rem;
}

.modal-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.btn-save, .btn-cancel {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-save {
  background-color: #4a90e2;
  color: white;
}

.btn-save:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.btn-cancel {
  background-color: #f0f0f0;
  color: #333;
}

.btn-cancel:hover {
  background-color: #e0e0e0;
}
</style>
