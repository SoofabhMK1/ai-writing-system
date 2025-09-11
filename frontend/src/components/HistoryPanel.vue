<!-- frontend/src/components/HistoryPanel.vue -->
<template>
  <div class="history-panel card">
    <h3 class="panel-title">大纲历史版本</h3>
    <div v-if="loading" class="status-info">正在加载...</div>
    <ul v-else-if="history.length > 0" class="history-list">
      <li v-for="item in history" :key="item.id" class="history-item">
        <div class="history-item-info">
          <span>{{ item.version_name || `版本 ${item.id}` }}</span>
          <small>{{ new Date(item.created_at).toLocaleString() }}</small>
        </div>
        <div class="history-item-actions">
          <button @click="$emit('preview', item)" class="btn btn-sm">
            预览
          </button>
          <button
            @click="$emit('delete', item.id)"
            class="btn btn-sm btn-danger"
          >
            删除
          </button>
        </div>
      </li>
    </ul>
    <div v-else class="status-info">暂无历史版本</div>
  </div>
</template>

<script setup>
defineProps({
  history: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['preview', 'delete'])
</script>

<style scoped>
.history-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.panel-title {
  margin: 0 0 var(--spacing-6) 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text);
  padding-bottom: var(--spacing-4);
  border-bottom: var(--border-width) solid var(--color-border);
}
.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  flex-grow: 1;
}
.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-3) var(--spacing-4);
  border-radius: var(--border-radius-md);
  transition: var(--transition-base);
}
.history-item:hover {
  background-color: var(--color-background);
}
.history-item-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-1);
}
.history-item-info span {
  font-weight: 500;
  color: var(--color-text);
}
.history-item-info small {
  color: var(--color-text-muted);
  font-size: var(--font-size-xs);
}
.history-item-actions {
  display: flex;
  gap: var(--spacing-2);
}
.btn-sm {
  padding: var(--spacing-1) var(--spacing-2);
  font-size: var(--font-size-xs);
}
.status-info {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-align: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-base);
  flex-grow: 1;
}
</style>
