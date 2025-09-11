<template>
  <div class="editable-json">
    <div v-for="(value, key) in editableData" :key="key" class="json-row">
      <input type="text" :value="key" @input="updateKey(key, $event.target.value)" class="json-key-input" />
      <input 
        type="text" 
        :value="formatValueForInput(value)" 
        @change="updateValue(key, $event.target.value)" 
        class="json-value-input" 
      />
      <button @click="removeField(key)" class="remove-btn">&times;</button>
    </div>
    <button @click="addField" class="add-btn">+ Add Field</button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({}),
  },
});

const emit = defineEmits(['update:modelValue']);

const editableData = ref({});

watch(() => props.modelValue, (newValue) => {
  // Only update from props if the data is actually different.
  // This breaks the infinite loop.
  if (JSON.stringify(newValue) !== JSON.stringify(editableData.value)) {
    editableData.value = { ...newValue };
  }
}, { immediate: true, deep: true });

watch(editableData, (newValue) => {
  emit('update:modelValue', newValue);
}, { deep: true });

const formatValueForInput = (value) => {
  if (Array.isArray(value) || typeof value === 'object' && value !== null) {
    return JSON.stringify(value);
  }
  return value;
};

const updateValue = (key, stringValue) => {
  try {
    // Try to parse it as JSON (for arrays/objects)
    editableData.value[key] = JSON.parse(stringValue);
  } catch (e) {
    // If it fails, treat it as a plain string
    editableData.value[key] = stringValue;
  }
};

const addField = () => {
  const newKey = `new_key_${Object.keys(editableData.value).length + 1}`;
  editableData.value[newKey] = 'new_value';
};

const removeField = (key) => {
  delete editableData.value[key];
};

const updateKey = (oldKey, newKey) => {
  if (newKey && oldKey !== newKey && !editableData.value.hasOwnProperty(newKey)) {
    const value = editableData.value[oldKey];
    delete editableData.value[oldKey];
    editableData.value[newKey] = value;
  }
};
</script>

<style scoped>
.editable-json { display: flex; flex-direction: column; gap: 10px; }
.json-row { display: flex; gap: 10px; align-items: center; }
.json-key-input, .json-value-input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-family: monospace; }
.json-key-input { width: 150px; }
.json-value-input { flex-grow: 1; }
.remove-btn, .add-btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; }
.remove-btn { background-color: #fdd; color: #c53030; }
.add-btn { background-color: #e6fffa; color: #2c7a7b; margin-top: 10px; align-self: flex-start; }
</style>
