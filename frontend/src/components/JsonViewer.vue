<template>
  <pre class="json-viewer">{{ formattedJson }}</pre>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
});

const formattedJson = computed(() => {
  if (!props.data || Object.keys(props.data).length === 0) {
    return 'No data available.';
  }
  return JSON.stringify(props.data, null, 2);
});
</script>

<style scoped>
.json-viewer {
  background-color: var(--color-background);
  color: var(--color-text);
  padding: var(--spacing-4);
  border-radius: var(--border-radius-md);
  border: var(--border-width) solid var(--color-border);
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'Courier New', Courier, monospace;
  font-size: var(--font-size-sm);
}
</style>
