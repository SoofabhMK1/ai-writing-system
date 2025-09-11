<template>
  <div class="editable-field">
    <label>{{ label }}</label>
    <textarea v-if="type === 'textarea'" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"></textarea>
    <input v-else :type="type || 'text'" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)">
  </div>
</template>

<script setup>
defineProps({
  label: String,
  modelValue: [String, Number],
  type: String,
});
defineEmits(['update:modelValue']);
</script>

<style scoped>
.editable-field { margin-bottom: 15px; }
.editable-field label { display: block; margin-bottom: 5px; font-weight: 600; }
.editable-field input, .editable-field textarea { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
.editable-field textarea { min-height: 80px; resize: vertical; }
</style>
