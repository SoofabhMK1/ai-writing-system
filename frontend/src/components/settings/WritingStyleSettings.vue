<!-- frontend/src/components/settings/WritingStyleSettings.vue -->
<template>
  <div class="setting-card">
    <div class="setting-header">
      <h3 class="setting-title">文风设定</h3>
      <button @click="handleAddNew" class="btn btn-primary">＋ 添加新文风</button>
    </div>
    <p class="setting-description">
      定义不同的写作风格，例如“幽默”、“严肃”或“诗意”。这些设定可以帮助 AI 在生成内容时保持一致的语调。
    </p>
    
    <div v-if="loading" class="status-info">正在加载...</div>
    <div v-if="error" class="status-info error">{{ error }}</div>

    <!-- List of existing writing styles -->
    <div v-if="writingStyles.length > 0" class="setting-item-list">
      <div v-for="style in writingStyles" :key="style.id" class="setting-item">
        <div class="item-content">
          <h4>{{ style.name }}</h4>
          <p>{{ style.description || '暂无描述' }}</p>
        </div>
        <div class="item-actions">
          <button @click="handleEdit(style)" class="btn">编辑</button>
          <button @click="handleDelete(style.id)" class="btn btn-danger">删除</button>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="status-info">
      还没有任何文风设定，点击右上角添加一个吧！
    </div>

    <SettingsFormModal
      :show="isModalOpen"
      :title="modalTitle"
      :fields="modalFields"
      :initial-data="currentStyle"
      @close="closeModal"
      @save="saveStyle"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { writingStyleService } from '@/services/settingService';
import { useModalStore } from '@/store/modal';
import { useNotificationStore } from '@/store/notification';
import SettingsFormModal from './SettingsFormModal.vue';

const modalStore = useModalStore();
const notification = useNotificationStore();

const writingStyles = ref([]);
const loading = ref(true);
const error = ref(null);
const isModalOpen = ref(false);
const currentStyle = ref(null);
const isEditing = ref(false);

const modalTitle = computed(() => isEditing.value ? '编辑文风' : '添加新文风');

const modalFields = [
  { key: 'name', label: '名称', placeholder: '例如：轻松幽默' },
  { key: 'description', label: '描述', type: 'textarea', placeholder: '对这个文风进行简短的描述' },
  { key: 'tone', label: '基调', placeholder: '例如：正式, 严肃, 活泼 (用逗号分隔)' },
  { key: 'point_of_view', label: '视角', placeholder: '例如：第一人称、第三人称' },
  { key: 'reference_works', label: '参考作品', type: 'textarea', placeholder: '列出一些参考作品，如书籍、电影等' },
  { key: 'guidelines', label: '具体准则 (JSON)', type: 'json', placeholder: '输入 JSON 格式的准则' },
];

const fetchWritingStyles = async () => {
  try {
    loading.value = true;
    const response = await writingStyleService.getAll();
    writingStyles.value = response.data;
  } catch (err) {
    error.value = '加载文风失败，请稍后重试。';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };

const handleAddNew = () => {
  isEditing.value = false;
  currentStyle.value = { 
    name: '', 
    description: '', 
    tone: [], 
    point_of_view: '', 
    reference_works: '',
    guidelines: {} 
  };
  openModal();
};

const handleEdit = (style) => {
  isEditing.value = true;
  // Ensure tone is an array for the form
  const formData = { ...style, tone: Array.isArray(style.tone) ? style.tone.join(', ') : style.tone };
  currentStyle.value = formData;
  openModal();
};

const saveStyle = async (data) => {
  // Convert tone string back to array if needed
  const payload = { ...data };
  if (payload.tone && typeof payload.tone === 'string') {
    payload.tone = payload.tone.split(',').map(item => item.trim()).filter(Boolean);
  }

  try {
    if (isEditing.value) {
      const response = await writingStyleService.update(currentStyle.value.id, payload);
      const index = writingStyles.value.findIndex(s => s.id === currentStyle.value.id);
      if (index !== -1) {
        writingStyles.value[index] = response.data;
      }
      notification.show('文风已更新', 'success');
    } else {
      const response = await writingStyleService.create(payload);
      writingStyles.value.unshift(response.data);
      notification.show('文风已创建', 'success');
    }
  } catch (err) {
    notification.show(isEditing.value ? '更新失败' : '创建失败', 'error');
  }
};

const handleDelete = async (id) => {
  try {
    await modalStore.show('确认删除', '你确定要删除这个文风吗？');
    await writingStyleService.delete(id);
    writingStyles.value = writingStyles.value.filter(s => s.id !== id);
    notification.show('文风已删除', 'success');
  } catch (err) {
    if (err.isCanceled) {
      notification.show('删除操作已取消', 'info');
    } else {
      notification.show('删除失败', 'error');
    }
  }
};

onMounted(() => {
  fetchWritingStyles();
});
</script>

<style scoped>
.setting-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-4);
  border-bottom: var(--border-width) solid var(--color-border);
  padding-bottom: var(--spacing-4);
}
.setting-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
}
.setting-description {
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-bottom: var(--spacing-8);
}
.setting-item-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-5);
}
.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-5);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-lg);
  background-color: var(--color-background);
  transition: var(--transition-base);
}
.setting-item:hover {
  border-color: var(--color-primary);
}
.item-content h4 {
  margin: 0 0 var(--spacing-2) 0;
  font-size: var(--font-size-lg);
  color: var(--color-text);
}
.item-content p {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 400px;
}
.item-actions {
  display: flex;
  gap: var(--spacing-3);
}
.status-info {
  text-align: center;
  padding: var(--spacing-12) var(--spacing-8);
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
}
.status-info.error {
  color: var(--color-danger);
  background-color: rgba(239, 68, 68, 0.1);
  border: var(--border-width) solid rgba(239, 68, 68, 0.2);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-4);
}
</style>
