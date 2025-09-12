<template>
  <div class="setting-card">
    <div class="setting-header">
      <h3 class="setting-title">对话预设</h3>
      <button @click="handleAddNew" class="btn btn-primary">
        ＋ 添加新预设
      </button>
    </div>
    <p class="setting-description">
      管理用于构建对话的预设模板。一个预设包含系统提示、COT指导和额外指令。
    </p>

    <div v-if="presetStore.isLoading" class="status-info">正在加载...</div>
    
    <div v-if="presets.length > 0" class="setting-item-list">
      <div
        v-for="preset in presets"
        :key="preset.id"
        class="setting-item"
      >
        <div class="item-content">
          <h4>{{ preset.name }}</h4>
          <p>{{ preset.system_prompt || '暂无系统提示' }}</p>
        </div>
        <div class="item-actions">
          <button @click="handleEdit(preset)" class="btn">编辑</button>
          <button @click="confirmDelete(preset)" class="btn btn-danger">
            删除
          </button>
        </div>
      </div>
    </div>
    <div v-else-if="!presetStore.isLoading" class="status-info">
      还没有任何对话预设，点击右上角添加一个吧！
    </div>

    <SettingsFormModal
      :show="isModalOpen"
      :title="modalTitle"
      :fields="modalFields"
      :initial-data="currentPreset"
      @close="closeModal"
      @save="savePreset"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { usePromptPresetStore } from '@/store/promptPreset';
import { useModalStore } from '@/store/modal';
import { storeToRefs } from 'pinia';
import SettingsFormModal from './SettingsFormModal.vue';

const presetStore = usePromptPresetStore();
const { presets } = storeToRefs(presetStore);
const modalStore = useModalStore();

const isModalOpen = ref(false);
const currentPreset = ref(null);
const isEditing = ref(false);

const modalTitle = computed(() =>
  isEditing.value ? '编辑对话预设' : '添加新对话预设',
);

const modalFields = [
  { key: 'name', label: '预设名称', placeholder: '例如：科幻小说家' },
  {
    key: 'system_prompt',
    label: '系统提示 (System Prompt)',
    type: 'textarea',
    placeholder: '定义 AI 的核心角色和行为。',
  },
  {
    key: 'cot_guidance',
    label: 'COT 指导 (COT Guidance)',
    type: 'textarea',
    placeholder: '指导 AI 如何进行思考，例如使用特定标签。',
  },
  {
    key: 'other_instructions',
    label: '其他指令 (Other Instructions)',
    type: 'textarea',
    placeholder: '提供一些额外的、全局性的指令。',
  },
];

onMounted(() => {
  if (presets.value.length === 0) {
    presetStore.fetchPresets();
  }
});

const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };

const handleAddNew = () => {
  isEditing.value = false;
  currentPreset.value = {
    name: '',
    system_prompt: '',
    cot_guidance: '',
    other_instructions: '',
  };
  openModal();
};

const handleEdit = (preset) => {
  isEditing.value = true;
  currentPreset.value = { ...preset };
  openModal();
};

const savePreset = async (data) => {
  if (isEditing.value) {
    await presetStore.updatePreset(currentPreset.value.id, data);
  } else {
    await presetStore.createPreset(data);
  }
};

const confirmDelete = (preset) => {
  modalStore.openModal('confirmation', {
    title: '确认删除',
    message: `您确定要删除预设 "${preset.name}" 吗？此操作无法撤销。`,
    onConfirm: () => presetStore.deletePreset(preset.id),
  });
};
</script>

<style scoped>
/* Styles are inherited from WorldviewSettings.vue via shared classes */
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
</style>
