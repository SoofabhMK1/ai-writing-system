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
          />
          <textarea
            v-if="field.type === 'textarea'"
            :id="field.key"
            v-model="editableData[field.key]"
            :placeholder="field.placeholder || ''"
            rows="4"
          ></textarea>
          <textarea
            v-if="field.type === 'json'"
            :id="field.key"
            :value="jsonString(editableData[field.key])"
            @input="updateJson(field.key, $event.target.value)"
            :class="{ 'invalid-json': jsonErrorField === field.key }"
            :placeholder="field.placeholder || 'Enter valid JSON'"
            rows="6"
          ></textarea>
          <p v-if="jsonErrorField === field.key" class="json-error-message">
            JSON 格式无效
          </p>
        </div>
        <div class="form-actions">
          <button type="button" class="btn-cancel" @click="close">取消</button>
          <button type="submit" class="btn-save">保存</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue';

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
});

const emit = defineEmits(['close', 'save']);

const editableData = ref({});

watch(() => props.initialData, (newData) => {
  // Create a fresh object for the form to bind to
  editableData.value = { ...newData };
}, { immediate: true, deep: true });

const close = () => {
  emit('close');
};

const jsonErrorField = ref(null);

const jsonString = (data) => {
  if (typeof data === 'object' && data !== null) {
    return JSON.stringify(data, null, 2);
  }
  return data || '';
};

const updateJson = (key, value) => {
  try {
    editableData.value[key] = value ? JSON.parse(value) : null;
    jsonErrorField.value = null;
  } catch (e) {
    // Don't update the data if JSON is invalid, but keep the raw string
    // in a temporary state or just mark the field as invalid.
    jsonErrorField.value = key;
  }
};

const handleSubmit = () => {
  if (jsonErrorField.value) {
    alert('无法保存，存在无效的 JSON 格式。');
    return;
  }
  emit('save', editableData.value);
  close();
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
  max-width: 600px;
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

.form-content {
  overflow-y: auto;
  padding-right: 1rem; /* For scrollbar */
  margin-right: -1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
  font-family: 'Courier New', Courier, monospace;
}

.invalid-json {
  border-color: #e94b3c;
  box-shadow: 0 0 0 3px rgba(233, 75, 60, 0.2);
}

.json-error-message {
  color: #e94b3c;
  font-size: 0.85rem;
  margin-top: 0.5rem;
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
