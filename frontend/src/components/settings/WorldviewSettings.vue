<!-- frontend/src/components/settings/WorldviewSettings.vue -->
<template>
  <div class="setting-card">
    <div class="setting-header">
      <h3 class="setting-title">世界观设定</h3>
      <button @click="handleAddNew" class="btn btn-primary">＋ 添加新世界观</button>
    </div>
    <p class="setting-description">
      管理和编辑多个世界观。每个世界观都可以有详细的描述和规则，方便在不同项目中复用。
    </p>
    
    <div v-if="loading" class="status-info">正在加载...</div>
    <div v-if="error" class="status-info error">{{ error }}</div>

    <!-- List of existing worldviews -->
    <div v-if="worldviews.length > 0" class="setting-item-list">
      <div v-for="worldview in worldviews" :key="worldview.id" class="setting-item">
        <div class="item-content">
          <h4>{{ worldview.name }}</h4>
          <p>{{ worldview.description || '暂无描述' }}</p>
        </div>
        <div class="item-actions">
          <button @click="handleEdit(worldview)" class="btn">编辑</button>
          <button @click="handleDelete(worldview.id)" class="btn btn-danger">删除</button>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="status-info">
      还没有任何世界观设定，点击右上角添加一个吧！
    </div>

    <SettingsFormModal
      :show="isModalOpen"
      :title="modalTitle"
      :fields="modalFields"
      :initial-data="currentWorldview"
      @close="closeModal"
      @save="saveWorldview"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { worldviewService } from '@/services/settingService';
import { useModalStore } from '@/store/modal';
import { useNotificationStore } from '@/store/notification';
import SettingsFormModal from './SettingsFormModal.vue';

const modalStore = useModalStore();
const notification = useNotificationStore();

const worldviews = ref([]);
const loading = ref(true);
const error = ref(null);
const isModalOpen = ref(false);
const currentWorldview = ref(null);
const isEditing = ref(false);

const modalTitle = computed(() => isEditing.value ? '编辑世界观' : '添加新世界观');

const modalFields = [
  { key: 'name', label: '名称', placeholder: '例如：赛博朋克未来' },
  { key: 'description', label: '描述', type: 'textarea', placeholder: '对这个世界观进行简短的描述' },
  { key: 'genre', label: '类型', placeholder: '例如：科幻、奇幻' },
  { key: 'time_period', label: '时代', placeholder: '例如：23世纪、中世纪' },
  { key: 'technology_level', label: '技术水平', placeholder: '例如：信息时代、星际时代' },
  { key: 'magic_system', label: '魔法体系', type: 'textarea', placeholder: '描述魔法的规则和特点' },
  { key: 'additional_details', label: '额外细节 (JSON)', type: 'json', placeholder: '输入 JSON 格式的额外信息' },
];

const fetchWorldviews = async () => {
  try {
    loading.value = true;
    const response = await worldviewService.getAll();
    worldviews.value = response.data;
  } catch (err) {
    error.value = '加载世界观失败，请稍后重试。';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };

const handleAddNew = () => {
  isEditing.value = false;
  currentWorldview.value = { 
    name: '', 
    description: '', 
    genre: '', 
    time_period: '', 
    technology_level: '', 
    magic_system: '',
    additional_details: {} 
  };
  openModal();
};

const handleEdit = (worldview) => {
  isEditing.value = true;
  currentWorldview.value = { ...worldview };
  openModal();
};

const saveWorldview = async (data) => {
  try {
    if (isEditing.value) {
      const response = await worldviewService.update(currentWorldview.value.id, data);
      const index = worldviews.value.findIndex(w => w.id === currentWorldview.value.id);
      if (index !== -1) {
        worldviews.value[index] = response.data;
      }
      notification.show('世界观已更新', 'success');
    } else {
      const response = await worldviewService.create(data);
      worldviews.value.unshift(response.data);
      notification.show('世界观已创建', 'success');
    }
  } catch (err) {
    notification.show(isEditing.value ? '更新失败' : '创建失败', 'error');
  }
};

const handleDelete = async (id) => {
  try {
    await modalStore.show('确认删除', '你确定要删除这个世界观吗？');
    await worldviewService.delete(id);
    worldviews.value = worldviews.value.filter(w => w.id !== id);
    notification.show('世界观已删除', 'success');
  } catch (err) {
    if (err.isCanceled) {
      notification.show('删除操作已取消', 'info');
    } else {
      notification.show('删除失败', 'error');
    }
  }
};

onMounted(() => {
  fetchWorldviews();
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
