<template>
  <div class="editable-json">
    <div v-for="(value, key) in editableData" :key="key" class="json-row">
      <input
        type="text"
        :value="key"
        @input="updateKey(key, $event.target.value)"
        class="form-control json-key-input"
        placeholder="Key"
      />
      <input
        type="text"
        :value="formatValueForInput(value)"
        @change="updateValue(key, $event.target.value)"
        class="form-control json-value-input"
        placeholder="Value"
      />
      <button @click="removeField(key)" class="btn btn-danger remove-btn">
        &times;
      </button>
    </div>
    <button @click="addField" class="btn add-btn">+ 添加字段</button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update:modelValue'])

const editableData = ref({})

watch(
  () => props.modelValue,
  (newValue) => {
    // Only update from props if the data is actually different.
    // This breaks the infinite loop.
    if (JSON.stringify(newValue) !== JSON.stringify(editableData.value)) {
      editableData.value = { ...newValue }
    }
  },
  { immediate: true, deep: true },
)

watch(
  editableData,
  (newValue) => {
    emit('update:modelValue', newValue)
  },
  { deep: true },
)

const formatValueForInput = (value) => {
  if (Array.isArray(value) || (typeof value === 'object' && value !== null)) {
    return JSON.stringify(value)
  }
  return value
}

const updateValue = (key, stringValue) => {
  try {
    // Try to parse it as JSON (for arrays/objects)
    editableData.value[key] = JSON.parse(stringValue)
  } catch {
    // If it fails, treat it as a plain string
    editableData.value[key] = stringValue
  }
}

const addField = () => {
  const newKey = `new_key_${Object.keys(editableData.value).length + 1}`
  editableData.value[newKey] = 'new_value'
}

const removeField = (key) => {
  delete editableData.value[key]
}

const updateKey = (oldKey, newKey) => {
  if (
    newKey &&
    oldKey !== newKey &&
    !Object.prototype.hasOwnProperty.call(editableData.value, newKey)
  ) {
    const value = editableData.value[oldKey]
    delete editableData.value[oldKey]
    editableData.value[newKey] = value
  }
}
</script>

<style scoped>
.editable-json {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}
.json-row {
  display: flex;
  gap: var(--spacing-3);
  align-items: center;
}
.json-key-input {
  width: 200px;
  flex-shrink: 0;
}
.json-value-input {
  flex-grow: 1;
}
.remove-btn {
  padding: var(--spacing-2) var(--spacing-3);
  line-height: 1;
}
.add-btn {
  margin-top: var(--spacing-2);
  align-self: flex-start;
}
</style>
