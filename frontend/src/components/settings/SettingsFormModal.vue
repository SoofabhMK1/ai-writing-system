<!-- frontend/src/components/settings/SettingsFormModal.vue -->
<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-card">
      <h3>{{ title }}</h3>
      <form @submit.prevent="handleSubmit" class="form-content">
        <div v-for="field in fields" :key="field.key" class="form-group">
          <label :for="field.key">{{ field.label }}</label>
          <input
            v-if="field.type === 'text' || !field.type"
            :id="field.key"
            v-model="editableData[field.key]"
            type="text"
            :placeholder="field.placeholder || ''"
            class="form-control"
          />
          <select
            v-if="field.type === 'select'"
            :id="field.key"
            v-model="editableData[field.key]"
            class="form-control"
          >
            <option disabled value="">请选择一个分类</option>
            <option v-for="option in field.options" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
          <textarea
            v-if="field.type === 'textarea'"
            :id="field.key"
            v-model="editableData[field.key]"
            :placeholder="field.placeholder || ''"
            rows="4"
            class="form-control"
          ></textarea>
          <textarea
            v-if="field.type === 'json'"
            :id="field.key"
            :value="jsonString(editableData[field.key])"
            @input="updateJson(field.key, $event.target.value)"
            :class="{ 'invalid-json': jsonErrorField === field.key }"
            :placeholder="field.placeholder || 'Enter valid JSON'"
            rows="6"
            class="form-control"
          ></textarea>
          <p v-if="jsonErrorField === field.key" class="json-error-message">
            JSON 格式无效
          </p>
        </div>
        <div class="form-actions">
          <button type="button" class="btn" @click="close">取消</button>
          <button type="submit" class="btn btn-primary">保存</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  fields: {
    type: Array,
    required: true,
  },
  initialData: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['close', 'save'])

const editableData = ref({})

watch(
  () => props.initialData,
  (newData) => {
    // Deep copy the initial data to ensure the form works with a completely
    // isolated object, preventing any potential reactivity issues with props.
    editableData.value = JSON.parse(JSON.stringify(newData || {}))
  },
  { immediate: true, deep: true },
)

const close = () => {
  emit('close')
}

const jsonErrorField = ref(null)

const jsonString = (data) => {
  if (typeof data === 'object' && data !== null) {
    return JSON.stringify(data, null, 2)
  }
  return data || ''
}

const updateJson = (key, value) => {
  try {
    editableData.value[key] = value ? JSON.parse(value) : null
    jsonErrorField.value = null
  } catch {
    // Don't update the data if JSON is invalid, but keep the raw string
    // in a temporary state or just mark the field as invalid.
    jsonErrorField.value = key
  }
}

const handleSubmit = () => {
  if (jsonErrorField.value) {
    alert('无法保存，存在无效的 JSON 格式。')
    return
  }
  emit('save', editableData.value)
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
  max-width: 600px;
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

.form-content {
  overflow-y: auto;
  padding-right: var(--spacing-4);
  margin-right: calc(-1 * var(--spacing-4));
}

.form-group {
  margin-bottom: var(--spacing-5);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-2);
  font-weight: 500;
  color: var(--color-text);
  font-size: var(--font-size-sm);
}

.form-control {
  width: 100%;
  padding: var(--spacing-3) var(--spacing-4);
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

textarea.form-control {
  resize: vertical;
  min-height: 120px;
  font-family: inherit;
}

textarea.form-control[rows='6'] {
  min-height: 180px;
  font-family: 'Courier New', Courier, monospace;
}

.invalid-json {
  border-color: var(--color-danger);
}

.invalid-json:focus {
  box-shadow: 0 0 0 3px rgba(var(--color-danger), 0.2);
}

.json-error-message {
  color: var(--color-danger);
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-2);
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
