<template>
  <div class="workspace-container">
    <div class="left-panel">
      <slot name="left"></slot>
    </div>
    <div class="right-panel">
      <slot name="right"></slot>
    </div>
  </div>
</template>

<script setup>
// This component is for layout only, so no script logic is needed.
</script>

<style scoped>
.workspace-container {
  display: flex;
  height: 100%;
  gap: var(--spacing-8);
}

.left-panel {
  width: 280px;
  min-width: 240px;
  flex-shrink: 0;
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.right-panel {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  min-height: 0; /* Crucial for flex-grow to work in a flex column */
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}
</style>
