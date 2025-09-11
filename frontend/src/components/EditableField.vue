<template>
  <div class="form-group">
    <label>{{ label }}</label>
    <textarea v-if="type === 'textarea'" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" class="form-control"></textarea>
    <input v-else :type="type || 'text'" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" class="form-control">
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
.form-group {
  margin-bottom: var(--spacing-5);
}
.form-group label {
  display: block;
  font-weight: 500;
  color: var(--color-text);
  margin-bottom: var(--spacing-2);
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
  min-height: 100px;
}
</style>
