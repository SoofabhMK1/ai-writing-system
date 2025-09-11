<!-- frontend/src/components/GenerationResultModal.vue -->
<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <h3>{{ title }}</h3>
      <div class="modal-content">
        <pre>{{ formattedContent }}</pre>
      </div>
      <div class="form-actions">
        <button type="button" class="btn" @click="close">关闭</button>
        <button
          v-if="!isReadOnly"
          type="button"
          class="btn btn-primary"
          @click="save"
        >
          保存
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

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
})

const emit = defineEmits(['close', 'save'])

const formattedContent = computed(() => {
  return JSON.stringify(props.content, null, 2)
})

const close = () => {
  emit('close')
}

const save = () => {
  emit('save')
}
</script>

<style scoped>
.modal-overlay {
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

.modal-card {
  background-color: var(--color-surface);
  padding: var(--spacing-8);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  border: var(--border-width) solid var(--color-border);
}

.modal-card h3 {
  margin: 0 0 var(--spacing-6) 0;
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text);
  text-align: center;
}

.modal-content {
  flex-grow: 1;
  overflow-y: auto;
  background-color: var(--color-background);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-4);
  border: var(--border-width) solid var(--color-border);
}

.modal-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
  font-family: 'Courier New', Courier, monospace;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-4);
  margin-top: var(--spacing-6);
  padding-top: var(--spacing-6);
  border-top: var(--border-width) solid var(--color-border);
}
</style>
