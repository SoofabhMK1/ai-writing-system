<!-- frontend/src/components/ProjectList.vue -->
<template>
  <div v-if="loading" class="status-info loading">正在加载项目...</div>
  <div v-if="error" class="status-info error">加载失败: {{ error }}</div>

  <div v-if="projects.length > 0" class="project-grid">
    <div
      v-for="project in projects"
      :key="project.id"
      class="project-card"
      @click="$emit('project-selected', project)"
    >
      <div class="project-card-content">
        <h2>{{ project.name }}</h2>
        <p>{{ project.description || '暂无描述' }}</p>
      </div>
      <button @click.stop="handleDeleteProject(project.id)" class="btn-delete">删除</button>
    </div>
  </div>

  <div v-else-if="!loading" class="status-info no-projects">
    还没有项目，快创建一个开始吧！
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import projectService from '../services/projectService';
import { useModalStore } from '@/store/modal.js';
import { useNotificationStore } from '@/store/notification.js';

const emit = defineEmits(['project-selected', 'project-deleted']);

const modal = useModalStore();
const notification = useNotificationStore();

const projects = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchProjects = async () => {
  try {
    const response = await projectService.getProjects();
    projects.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = '无法连接到服务器或 API 出错。';
  } finally {
    loading.value = false;
  }
};

const handleDeleteProject = async (projectId) => {
  try {
    await modal.show('确认删除', '你确定要删除这个项目吗？此操作不可撤销。');
    try {
      await projectService.deleteProject(projectId);
      projects.value = projects.value.filter(p => p.id !== projectId);
      notification.show('项目已删除', 'success');
      emit('project-deleted', projectId); // Emit event on successful deletion
    } catch (err) {
      console.error(err);
      notification.show('删除项目失败！', 'error');
    }
  } catch (isCanceled) {
    console.log('删除操作已取消');
    notification.show('删除操作已取消', 'info');
  }
};

onMounted(() => {
  fetchProjects();
});

// Expose a method to be called by the parent
defineExpose({
  addProject(project) {
    projects.value.unshift(project);
  }
});
</script>

<style scoped>
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.project-card {
  position: relative;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
  cursor: pointer;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  border-color: #4a90e2;
}

.project-card-content {
  padding: 1.5rem;
}

.project-card h2 {
  margin-top: 0;
  margin-bottom: 0.75rem;
  font-size: 1.2rem;
  color: #333;
}

.project-card p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
}

.btn-delete {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.3rem 0.6rem;
  background-color: #e94b3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  opacity: 0;
  transform: scale(0.8);
  transition: opacity 0.3s, transform 0.3s;
}

.project-card:hover .btn-delete {
  opacity: 1;
  transform: scale(1);
}

.btn-delete:hover {
  background-color: #d93a2b;
}

.status-info {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #666;
}

.error {
  color: #e94b3c;
  background-color: rgba(233, 75, 60, 0.05);
  border: 1px solid rgba(233, 75, 60, 0.2);
  border-radius: 8px;
}
</style>
