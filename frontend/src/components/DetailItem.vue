<template>
  <div class="detail-item">
    <strong class="detail-label">{{ label }}:</strong>
    <p v-if="type === 'textarea'" class="detail-value-long">{{ value || 'N/A' }}</p>
    <span v-else class="detail-value">{{ value || 'N/A' }}</span>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  type: String,
});
</script>

<style scoped>
.detail-item { margin-bottom: 15px; line-height: 1.6; }
.detail-label { font-weight: 600; color: #333; margin-right: 10px; }
.detail-value { color: #555; }
.detail-value-long { background: #f9f9f9; border-radius: 6px; padding: 10px; margin-top: 5px; white-space: pre-wrap; word-break: break-word; }
</style>
