<template>
  <div class="detail-item">
    <strong class="detail-label">{{ label }}:</strong>
    <p v-if="type === 'textarea'" class="detail-value-long">
      {{ value || 'N/A' }}
    </p>
    <span v-else class="detail-value">{{ value || 'N/A' }}</span>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  type: String,
})
</script>

<style scoped>
.detail-item {
  margin-bottom: var(--spacing-5);
  line-height: 1.6;
  font-size: var(--font-size-base);
}
.detail-label {
  font-weight: 600;
  color: var(--color-text);
  margin-right: var(--spacing-2);
}
.detail-value {
  color: var(--color-text-muted);
}
.detail-value-long {
  display: block;
  background: var(--color-background);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-3) var(--spacing-4);
  margin-top: var(--spacing-2);
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--color-text-muted);
  border: var(--border-width) solid var(--color-border);
}
</style>
