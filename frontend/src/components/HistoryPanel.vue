<!-- frontend/src/components/HistoryPanel.vue -->
<template>
  <div class="history-panel card">
    <h3 class="panel-title">大纲历史版本</h3>
    <div v-if="loading" class="loading-info">正在加载...</div>
    <ul v-else-if="history.length > 0" class="history-list">
      <li v-for="item in history" :key="item.id" class="history-item">
        <div class="history-item-info">
          <span>{{ item.version_name || `版本 ${item.id}` }}</span>
          <small>{{ new Date(item.created_at).toLocaleString() }}</small>
        </div>
        <div class="history-item-actions">
          <button @click="$emit('preview', item)" class="btn-action btn-preview">预览</button>
          <button @click="$emit('delete', item.id)" class="btn-action btn-delete">删除</button>
        </div>
      </li>
    </ul>
    <div v-else class="empty-info">暂无历史版本</div>
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
});

defineEmits(['preview', 'delete']);
</script>

<style scoped>
.card { background-color: #ffffff; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }
.history-panel { flex-grow: 1; display: flex; flex-direction: column; min-height: 0; }
.panel-title { margin: 0 0 1.5rem 0; font-size: 1.3rem; font-weight: 600; border-bottom: 1px solid #e8e8e8; padding-bottom: 1rem; }
.history-list { list-style: none; padding: 0; margin: 0; overflow-y: auto; }
.history-item { display: flex; justify-content: space-between; align-items: center; padding: 0.8rem; border-radius: 6px; transition: background-color 0.2s; }
.history-item:hover { background-color: #f0f5ff; }
.history-item-info { display: flex; flex-direction: column; }
.history-item small { color: #888; font-size: 0.8rem; margin-top: 0.25rem; }
.history-item-actions { display: flex; gap: 0.5rem; }
.btn-action { padding: 0.4rem 0.8rem; font-size: 0.8rem; border: none; border-radius: 6px; cursor: pointer; }
.btn-preview { background-color: #6c757d; color: white; }
.btn-preview:hover { background-color: #5a6268; }
.btn-delete { background-color: #e94b3c; color: white; }
.btn-delete:hover { background-color: #d93a2b; }
.loading-info, .empty-info { display: flex; justify-content: center; align-items: center; height: 100%; text-align: center; color: #888; font-size: 1.2rem; }
</style>
