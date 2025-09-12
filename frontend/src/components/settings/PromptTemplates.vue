<!-- frontend/src/components/settings/PromptTemplates.vue -->
<template>
  <div class="setting-card">
    <div class="setting-header">
      <h3 class="setting-title">AI 提示词模板</h3>
      <button @click="handleAddNew" class="btn btn-primary">
        ＋ 添加新模板
      </button>
    </div>
    <p class="setting-description">
      创建和管理常用的 AI 提示词模板，方便在写作时快速调用，提高效率。
    </p>

    <div v-if="loading" class="status-info">正在加载...</div>
    <div v-if="error" class="status-info error">{{ error }}</div>

    <!-- List of existing prompt templates -->
    <div v-if="promptTemplates.length > 0" class="setting-item-list">
      <div
        v-for="template in promptTemplates"
        :key="template.id"
        class="setting-item"
      >
        <div class="item-content">
          <h4>{{ template.name }}</h4>
          <p>{{ template.description || '暂无描述' }}</p>
        </div>
        <div class="item-actions">
          <button @click="handleEdit(template)" class="btn">编辑</button>
          <button @click="handleDelete(template.id)" class="btn btn-danger">
            删除
          </button>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="status-info">
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
import { ref, onMounted, computed } from 'vue'
import { promptTemplateService } from '@/services/settingService'
import { useModalStore } from '@/store/modal'
import { useNotificationStore } from '@/store/notification'
import SettingsFormModal from './SettingsFormModal.vue'

const modalStore = useModalStore()
const notification = useNotificationStore()

const promptTemplates = ref([])
const loading = ref(true)
const error = ref(null)
const isModalOpen = ref(false)
const currentTemplate = ref(null)
const isEditing = ref(false)

const modalTitle = computed(() => (isEditing.value ? '编辑模板' : '添加新模板'))

const modalFields = [
  { key: 'name', label: '名称', placeholder: '例如：角色对话' },
  {
    key: 'description',
    label: '描述',
    type: 'textarea',
    placeholder: '对这个模板进行简短的描述',
  },
  { 
    key: 'category', 
    label: '分类', 
    type: 'select',
    options: [
      { value: 'SYSTEM_PROMPT', text: '系统提示' },
      { value: 'CHARACTER_PROMPT', text: '角色提示' },
      { value: 'PROJECT_PROMPT', text: '项目提示' },
    ]
  },
  {
    key: 'template_text',
    label: '模板内容',
    type: 'textarea',
    placeholder: '输入你的提示词模板，使用 [占位符] 表示变量',
  },
  {
    key: 'variables',
    label: '模板变量 (JSON)',
    type: 'json',
    placeholder: '输入 JSON 格式的变量定义',
  },
]

const fetchPromptTemplates = async () => {
  try {
    loading.value = true
    const response = await promptTemplateService.getAll()
    promptTemplates.value = response.data
  } catch (err) {
    error.value = '加载模板失败，请稍后重试。'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const openModal = () => {
  isModalOpen.value = true
}
const closeModal = () => {
  isModalOpen.value = false
}

const handleAddNew = () => {
  isEditing.value = false
  currentTemplate.value = {
    name: '',
    description: '',
    category: '',
    template_text: '',
    variables: {},
  }
  openModal()
}

const handleEdit = (template) => {
  isEditing.value = true
  currentTemplate.value = { ...template }
  openModal()
}

const saveTemplate = async (data) => {
  try {
    if (isEditing.value) {
      const response = await promptTemplateService.update(
        currentTemplate.value.id,
        data,
      )
      const index = promptTemplates.value.findIndex(
        (t) => t.id === currentTemplate.value.id,
      )
      if (index !== -1) {
        promptTemplates.value[index] = response.data
      }
      notification.show('模板已更新', 'success')
    } else {
      const response = await promptTemplateService.create(data)
      promptTemplates.value.unshift(response.data)
      notification.show('模板已创建', 'success')
    }
  } catch {
    notification.show(isEditing.value ? '更新失败' : '创建失败', 'error')
  }
}

const handleDelete = async (id) => {
  try {
    await modalStore.show('确认删除', '你确定要删除这个模板吗？')
    await promptTemplateService.delete(id)
    promptTemplates.value = promptTemplates.value.filter((t) => t.id !== id)
    notification.show('模板已删除', 'success')
  } catch (error) {
    if (error.isCanceled) {
      notification.show('删除操作已取消', 'info')
    } else {
      notification.show('删除失败', 'error')
    }
  }
}

onMounted(() => {
  fetchPromptTemplates()
})
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
