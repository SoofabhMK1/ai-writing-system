<!-- frontend/src/components/settings/WorldviewSettings.vue -->
<template>
  <div class="setting-card">
    <div class="setting-header">
      <h3 class="setting-title">世界观设定</h3>
      <button @click="handleAddNew" class="btn-add-new">＋ 添加新世界观</button>
    </div>
    <p class="setting-description">
      管理和编辑多个世界观。每个世界观都可以有详细的描述和规则，方便在不同项目中复用。
    </p>
    
    <div v-if="loading" class="loading-info">正在加载...</div>
    <div v-if="error" class="error-info">{{ error }}</div>

    <!-- List of existing worldviews -->
    <div v-if="worldviews.length > 0" class="setting-item-list">
      <div v-for="worldview in worldviews" :key="worldview.id" class="setting-item">
        <div class="item-content">
          <h4>{{ worldview.name }}</h4>
          <p>{{ worldview.description || '暂无描述' }}</p>
        </div>
        <div class="item-actions">
          <button @click="handleEdit(worldview)" class="btn-edit">编辑</button>
          <button @click="handleDelete(worldview.id)" class="btn-delete">删除</button>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="empty-info">
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
.setting-card {
  max-width: 900px;
}

.setting-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
}

.setting-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.btn-add-new {
  padding: 0.6rem 1.2rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-add-new:hover {
  background-color: #218838;
  transform: translateY(-2px);
}

.setting-description {
  font-size: 1rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.setting-item-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  background-color: #fafafa;
  transition: box-shadow 0.3s;
}

.setting-item:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.item-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #444;
}

.item-content p {
  margin: 0;
  font-size: 0.95rem;
  color: #777;
}

.item-actions {
  display: flex;
  gap: 0.8rem;
}

.item-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn-edit {
  background-color: #4a90e2;
  color: white;
}

.btn-edit:hover {
  background-color: #357abd;
}

.btn-delete {
  background-color: #e94b3c;
  color: white;
}

.btn-delete:hover {
  background-color: #d93a2b;
}

.loading-info, .error-info, .empty-info {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #888;
}

.error-info {
  color: #e94b3c;
}
</style>
