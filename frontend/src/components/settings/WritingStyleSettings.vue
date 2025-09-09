<!-- frontend/src/components/settings/WritingStyleSettings.vue -->
<template>
  <div class="setting-card">
    <div class="setting-header">
      <h3 class="setting-title">文风设定</h3>
      <button @click="handleAddNew" class="btn-add-new">＋ 添加新文风</button>
    </div>
    <p class="setting-description">
      定义不同的写作风格，例如“幽默”、“严肃”或“诗意”。这些设定可以帮助 AI 在生成内容时保持一致的语调。
    </p>
    
    <div v-if="loading" class="loading-info">正在加载...</div>
    <div v-if="error" class="error-info">{{ error }}</div>

    <!-- List of existing writing styles -->
    <div v-if="writingStyles.length > 0" class="setting-item-list">
      <div v-for="style in writingStyles" :key="style.id" class="setting-item">
        <div class="item-content">
          <h4>{{ style.name }}</h4>
          <p>{{ style.description || '暂无描述' }}</p>
        </div>
        <div class="item-actions">
          <button @click="handleEdit(style)" class="btn-edit">编辑</button>
          <button @click="handleDelete(style.id)" class="btn-delete">删除</button>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="empty-info">
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
/* Using similar styles for consistency */
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
