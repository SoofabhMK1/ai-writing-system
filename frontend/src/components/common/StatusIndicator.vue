<template>
  <div
    v-if="loading || error || empty"
    class="status-info"
    :class="{ 'is-centered': center }"
  >
    <div v-if="loading" class="loading">
      <!-- You could add a spinner icon here -->
      <p>Loading...</p>
    </div>
    <div v-else-if="error" class="error">
      <!-- You could add an error icon here -->
      <p>{{ error }}</p>
    </div>
    <div v-else-if="empty" class="empty">
      <!-- You could add an empty state icon here -->
      <p><slot>No data available.</slot></p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: null,
  },
  empty: {
    type: Boolean,
    default: false,
  },
  center: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.status-info {
  text-align: center;
  padding: var(--spacing-8);
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Default to top alignment */
  align-items: center;
  gap: var(--spacing-4);
}

.status-info.is-centered {
  justify-content: center;
  padding: var(--spacing-12) var(--spacing-8);
}

.error {
  color: var(--color-danger);
  background-color: color-mix(in srgb, var(--color-danger) 15%, transparent);
  border: var(--border-width) solid color-mix(in srgb, var(--color-danger) 30%, transparent);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-4);
  width: 100%;
}

.empty p,
.loading p,
.error p {
  margin: 0;
}
</style>
