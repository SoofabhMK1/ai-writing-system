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
          <button type="button" class="btn-cancel" @click="close">取消</button>
          <button type="submit" class="btn-create">创建项目</button>
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
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 500px;
}

.modal-card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 500;
  text-align: center;
}

.create-form input,
.create-form textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  margin-bottom: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.create-form input:focus,
.create-form textarea:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
}

.create-form textarea {
  min-height: 100px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-create, .btn-cancel {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-create {
  background-color: #4a90e2;
  color: white;
}

.btn-create:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.btn-cancel {
  background-color: #f0f0f0;
  color: #333;
}

.btn-cancel:hover {
  background-color: #e0e0e0;
}
</style>
