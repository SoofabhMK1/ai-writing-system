<!-- frontend/src/components/CreateProjectModal.vue -->
<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-card">
      <h3>创建新项目</h3>
      <form @submit.prevent="handleCreateProject" class="create-form">
        <input
          v-model="newProjectName"
          type="text"
          placeholder="项目名称"
          required
        />
        <textarea
          v-model="newProjectDescription"
          placeholder="项目描述 (可选)"
        ></textarea>
        <div class="form-actions">
          <button type="button" class="btn" @click="close">取消</button>
          <button type="submit" class="btn btn-primary">创建项目</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import projectService from '../services/projectService';
import { useNotificationStore } from '@/store/notification.js';

const emit = defineEmits(['project-created', 'close']);
const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
});

const notification = useNotificationStore();
const newProjectName = ref('');
const newProjectDescription = ref('');

const close = () => {
  emit('close');
};

const handleCreateProject = async () => {
  if (!newProjectName.value.trim()) {
    notification.show('项目名称不能为空！', 'error');
    return;
  }
  try {
    const projectData = {
      name: newProjectName.value,
      description: newProjectDescription.value,
    };
    const response = await projectService.createProject(projectData);
    emit('project-created', response.data);
    newProjectName.value = '';
    newProjectDescription.value = '';
    notification.show('项目创建成功！', 'success');
    close();
  } catch (err) {
    console.error(err);
    notification.show('创建项目失败！', 'error');
  }
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

.modal-card {
  background-color: var(--color-surface);
  padding: var(--spacing-8);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 500px;
  border: var(--border-width) solid var(--color-border);
}

.modal-card h3 {
  margin-top: 0;
  margin-bottom: var(--spacing-6);
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text);
  text-align: center;
}

.create-form input,
.create-form textarea {
  width: 100%;
  padding: var(--spacing-3) var(--spacing-4);
  margin-bottom: var(--spacing-4);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  background-color: var(--color-background);
  color: var(--color-text);
  transition: var(--transition-base);
  box-sizing: border-box;
}

.create-form input:focus,
.create-form textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary), 0.2);
}

.create-form textarea {
  min-height: 120px;
  resize: vertical;
  font-family: inherit;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-4);
  margin-top: var(--spacing-6);
}
</style>
