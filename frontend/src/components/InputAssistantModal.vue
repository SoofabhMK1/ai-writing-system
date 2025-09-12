<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2 class="modal-title">输入辅助</h2>
      <p class="modal-description">在此编辑您的输入内容，或从模板库中选择一个模板开始。</p>
      
      <div class="main-layout">
        <div class="editor-area">
          <textarea
            v-model="editedContent"
            class="main-textarea form-control"
            placeholder="在此输入或编辑内容..."
          ></textarea>
        </div>
        
        <div class="template-area">
          <div v-if="isLoading" class="loading-spinner">加载中...</div>
          <div v-else class="template-list">
            <div v-for="(templates, category) in groupedTemplates" :key="category" class="template-category">
              <h4 class="category-title" @click="toggleCategory(category)">
                <span>{{ category }}</span>
                <span class="collapse-icon">{{ collapsedCategories[category] ? '+' : '-' }}</span>
              </h4>
              <div v-if="!collapsedCategories[category]">
                <div
                  v-for="template in templates"
                  :key="template.id"
                  class="template-item"
                  @click="applyTemplate(template)"
                >
                  {{ template.name }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button @click="$emit('close')" class="btn">取消</button>
        <button @click="confirm" class="btn btn-primary">确认</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { usePromptStore } from '@/store/prompt';

const emit = defineEmits(['close', 'confirm']);
const promptStore = usePromptStore();
const { groupedTemplates, isLoading } = storeToRefs(promptStore);

const editedContent = ref('');
const collapsedCategories = ref({});

const toggleCategory = (category) => {
  collapsedCategories.value[category] = !collapsedCategories.value[category];
};

const applyTemplate = (template) => {
  editedContent.value = template.template_text;
};

onMounted(() => {
  promptStore.fetchTemplates();
});

const confirm = () => {
  emit('confirm', editedContent.value);
  emit('close');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background: var(--color-surface);
  padding: var(--spacing-8);
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 800px; /* Increased width for better layout */
  box-shadow: var(--shadow-lg);
  border: var(--border-width) solid var(--color-border);
  display: flex;
  flex-direction: column;
}

.modal-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--spacing-2);
}

.modal-description {
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
  margin-bottom: var(--spacing-6);
}

.main-layout {
  display: flex;
  gap: var(--spacing-6);
  flex-grow: 1;
}

.editor-area {
  flex: 3; /* Takes up more space */
  display: flex;
  flex-direction: column;
}

.main-textarea {
  width: 100%;
  height: 400px; /* Increased height */
  font-family: var(--font-family-base);
  font-size: var(--font-size-base);
  resize: vertical;
  flex-grow: 1;
}

.template-area {
  flex: 1;
  background-color: var(--color-surface-soft);
  padding: var(--spacing-4);
  border-radius: var(--border-radius-md);
  border: var(--border-width) solid var(--color-border);
  display: flex;
  flex-direction: column;
  max-height: 420px; /* Match textarea height */
}

.template-list {
  overflow-y: auto;
  flex-grow: 1;
}

.template-category {
  margin-bottom: var(--spacing-4);
}

.category-title {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0 var(--spacing-4);
  margin-bottom: var(--spacing-2);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-title:hover {
  color: var(--color-text);
}

.collapse-icon {
  font-weight: bold;
}

.template-item {
  padding: var(--spacing-3) var(--spacing-4);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  border-bottom: var(--border-width) solid var(--color-border);
}

.template-item:last-child {
  border-bottom: none;
}

.template-item:hover {
  background-color: var(--color-surface-hover);
  color: var(--color-text);
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: var(--color-text-muted);
}

.modal-actions {
  margin-top: var(--spacing-6);
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-4);
}
</style>
