<!-- frontend/src/components/settings/AIModelSettings.vue -->
<template>
  <div class="setting-card">
    <div class="setting-header">
      <h3 class="setting-title">AI 模型设定</h3>
      <button @click="handleAddNew" class="btn-add-new">＋ 添加新模型</button>
    </div>
    <p class="setting-description">
      管理可用于生成内容的 AI 模型。所有模型都应与 OpenAI API 兼容。
    </p>
    
    <div v-if="loading" class="loading-info">正在加载...</div>
    <div v-if="error" class="error-info">{{ error }}</div>

    <div v-if="aiModels.length > 0" class="setting-item-list">
      <div v-for="model in aiModels" :key="model.id" class="setting-item">
        <div class="item-content">
          <h4>{{ model.name }}</h4>
          <p><strong>Model:</strong> {{ model.model_name }} | <strong>URL:</strong> {{ model.api_url }}</p>
        </div>
        <div class="item-actions">
          <button @click="handleTest(model)" class="btn-test">测试</button>
          <button @click="handleEdit(model)" class="btn-edit">编辑</button>
          <button @click="handleDelete(model.id)" class="btn-delete">删除</button>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="empty-info">
      还没有任何 AI 模型设定，点击右上角添加一个吧！
    </div>

    <SettingsFormModal
      :show="isModalOpen"
      :title="modalTitle"
      :fields="modalFields"
      :initial-data="currentModel"
      @close="closeModal"
      @save="saveModel"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { aiModelService } from '@/services/settingService';
import { useModalStore } from '@/store/modal';
import { useNotificationStore } from '@/store/notification';
import SettingsFormModal from './SettingsFormModal.vue';

const modalStore = useModalStore();
const notification = useNotificationStore();

const aiModels = ref([]);
const loading = ref(true);
const error = ref(null);
const isModalOpen = ref(false);
const currentModel = ref(null);
const isEditing = ref(false);

const modalTitle = computed(() => isEditing.value ? '编辑 AI 模型' : '添加新 AI 模型');

const modalFields = [
  { key: 'name', label: '设定名称', placeholder: '例如：DeepSeek' },
  { key: 'api_url', label: 'API 地址', placeholder: '例如：https://api.deepseek.com/v1' },
  { key: 'api_key', label: 'API Key', placeholder: '请输入您的 API Key' },
  { key: 'model_name', label: '模型名称', placeholder: '例如：deepseek-chat' },
];

const fetchAIModels = async () => {
  try {
    loading.value = true;
    const response = await aiModelService.getAll();
    aiModels.value = response.data;
  } catch (err) {
    error.value = '加载 AI 模型失败，请稍后重试。';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };

const handleAddNew = () => {
  isEditing.value = false;
  currentModel.value = { name: '', api_url: '', api_key: '', model_name: '' };
  openModal();
};

const handleEdit = (model) => {
  isEditing.value = true;
  currentModel.value = { ...model };
  openModal();
};

const saveModel = async (data) => {
  try {
    if (isEditing.value) {
      const response = await aiModelService.update(currentModel.value.id, data);
      const index = aiModels.value.findIndex(m => m.id === currentModel.value.id);
      if (index !== -1) {
        aiModels.value[index] = response.data;
      }
      notification.show('AI 模型已更新', 'success');
    } else {
      const response = await aiModelService.create(data);
      aiModels.value.unshift(response.data);
      notification.show('AI 模型已创建', 'success');
    }
  } catch (err) {
    notification.show(isEditing.value ? '更新失败' : '创建失败', 'error');
  }
};

const handleDelete = async (id) => {
  try {
    await modalStore.show('确认删除', '你确定要删除这个 AI 模型吗？');
    await aiModelService.delete(id);
    aiModels.value = aiModels.value.filter(m => m.id !== id);
    notification.show('AI 模型已删除', 'success');
  } catch (err) {
    if (err.isCanceled) {
      notification.show('删除操作已取消', 'info');
    } else {
      notification.show('删除失败', 'error');
    }
  }
};

const handleTest = async (model) => {
  notification.show(`正在测试 ${model.name}...`, 'info');
  try {
    const response = await aiModelService.testConnection(model.id);
    notification.show(`${model.name}: ${response.data.message}`, 'success');
  } catch (err) {
    const detail = err.response?.data?.detail || '未知错误';
    notification.show(`${model.name} 测试失败: ${detail}`, 'error', { duration: 5000 });
  }
};

onMounted(() => {
  fetchAIModels();
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
}
.item-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
}
.item-content p {
  margin: 0;
  font-size: 0.9rem;
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
}
.btn-test {
  background-color: #ffc107;
  color: #333;
}
.btn-edit {
  background-color: #4a90e2;
  color: white;
}
.btn-delete {
  background-color: #e94b3c;
  color: white;
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
