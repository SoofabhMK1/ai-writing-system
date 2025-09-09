<!-- frontend/src/components/settings/PromptTemplates.vue -->
<template>
  <div class="setting-card">
    <div class="setting-header">
      <h3 class="setting-title">AI 提示词模板</h3>
      <button @click="handleAddNew" class="btn-add-new">＋ 添加新模板</button>
    </div>
    <p class="setting-description">
      创建和管理常用的 AI 提示词模板，方便在写作时快速调用，提高效率。
    </p>
    
    <div v-if="loading" class="loading-info">正在加载...</div>
    <div v-if="error" class="error-info">{{ error }}</div>

    <!-- List of existing prompt templates -->
    <div v-if="promptTemplates.length > 0" class="setting-item-list">
      <div v-for="template in promptTemplates" :key="template.id" class="setting-item">
        <div class="item-content">
          <h4>{{ template.name }}</h4>
          <p>{{ template.description || '暂无描述' }}</p>
        </div>
        <div class="item-actions">
          <button @click="handleEdit(template)" class="btn-edit">编辑</button>
          <button @click="handleDelete(template.id)" class="btn-delete">删除</button>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="empty-info">
      还没有任何提示词模板，点击右上角添加一个吧！
    </div>

    <SettingsFormModal
      :show="isModalOpen"
      :title="modalTitle"
      :fields="modalFields"
      :initial-data="currentTemplate"
      @close="closeModal"
      @save="saveTemplate"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { promptTemplateService } from '@/services/settingService';
import { useModalStore } from '@/store/modal';
import { useNotificationStore } from '@/store/notification';
import SettingsFormModal from './SettingsFormModal.vue';

const modalStore = useModalStore();
const notification = useNotificationStore();

const promptTemplates = ref([]);
const loading = ref(true);
const error = ref(null);
const isModalOpen = ref(false);
const currentTemplate = ref(null);
const isEditing = ref(false);

const modalTitle = computed(() => isEditing.value ? '编辑模板' : '添加新模板');

const modalFields = [
  { key: 'name', label: '名称', placeholder: '例如：角色对话' },
  { key: 'description', label: '描述', type: 'textarea', placeholder: '对这个模板进行简短的描述' },
  { key: 'category', label: '分类', placeholder: '例如：角色、情节、世界观' },
  { key: 'template_text', label: '模板内容', type: 'textarea', placeholder: '输入你的提示词模板，使用 [占位符] 表示变量' },
  { key: 'variables', label: '模板变量 (JSON)', type: 'json', placeholder: '输入 JSON 格式的变量定义' },
];

const fetchPromptTemplates = async () => {
  try {
    loading.value = true;
    const response = await promptTemplateService.getAll();
    promptTemplates.value = response.data;
  } catch (err) {
    error.value = '加载模板失败，请稍后重试。';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };

const handleAddNew = () => {
  isEditing.value = false;
  currentTemplate.value = { 
    name: '', 
    description: '', 
    category: '', 
    template_text: '',
    variables: {} 
  };
  openModal();
};

const handleEdit = (template) => {
  isEditing.value = true;
  currentTemplate.value = { ...template };
  openModal();
};

const saveTemplate = async (data) => {
  try {
    if (isEditing.value) {
      const response = await promptTemplateService.update(currentTemplate.value.id, data);
      const index = promptTemplates.value.findIndex(t => t.id === currentTemplate.value.id);
      if (index !== -1) {
        promptTemplates.value[index] = response.data;
      }
      notification.show('模板已更新', 'success');
    } else {
      const response = await promptTemplateService.create(data);
      promptTemplates.value.unshift(response.data);
      notification.show('模板已创建', 'success');
    }
  } catch (err) {
    notification.show(isEditing.value ? '更新失败' : '创建失败', 'error');
  }
};

const handleDelete = async (id) => {
  try {
    await modalStore.show('确认删除', '你确定要删除这个模板吗？');
    await promptTemplateService.delete(id);
    promptTemplates.value = promptTemplates.value.filter(t => t.id !== id);
    notification.show('模板已删除', 'success');
  } catch (err) {
    if (err.isCanceled) {
      notification.show('删除操作已取消', 'info');
    } else {
      notification.show('删除失败', 'error');
    }
  }
};

onMounted(() => {
  fetchPromptTemplates();
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
