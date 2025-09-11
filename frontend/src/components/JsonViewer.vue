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
  background: #f4f4f4;
  border-radius: 6px;
  padding: 15px;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9rem;
  border: 1px solid #e0e0e0;
}
</style>
