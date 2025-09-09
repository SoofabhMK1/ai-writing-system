<!-- src/views/ProjectListView.vue -->
<template>
  <div class="page-container">

    <!-- 创建新项目的表单 -->
    <div class="form-card">
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
        <button type="submit" class="btn-create">创建项目</button>
      </form>
    </div>

    <div v-if="loading" class="status-info loading">正在加载项目...</div>
    <div v-if="error" class="status-info error">加载失败: {{ error }}</div>

    <!-- 项目网格布局 -->
    <div v-if="projects.length > 0" class="project-grid">
      <div v-for="project in projects" :key="project.id" class="project-card">
        <router-link :to="`/projects/${project.id}`" class="project-card-link">
          <div class="project-card-content">
            <h2>{{ project.name }}</h2>
            <p>{{ project.description || '暂无描述' }}</p>
          </div>
        </router-link>
        <button @click="handleDeleteProject(project.id)" class="btn-delete">删除</button>
      </div>
    </div>
    
    <div v-else-if="!loading" class="status-info no-projects">
      还没有项目，快创建一个开始吧！
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import projectService from '../services/projectService';
import { useModalStore } from '@/store/modal.js';
import { useNotificationStore } from '@/store/notification.js';

const modal = useModalStore();
const notification = useNotificationStore();

// --- 现有状态 ---
const projects = ref([]);
const loading = ref(true);
const error = ref(null);

// --- 新增状态：用于表单输入 ---
const newProjectName = ref('');
const newProjectDescription = ref('');

// --- 获取项目列表的函数 (无变化) ---
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

// --- 新增函数：处理项目创建 ---
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
    projects.value.unshift(response.data);
    newProjectName.value = '';
    newProjectDescription.value = '';
    notification.show('项目创建成功！', 'success');
  } catch (err) {
    console.error(err);
    notification.show('创建项目失败！', 'error');
  }
};

// --- 新增函数：处理项目删除 ---
const handleDeleteProject = async (projectId) => {
  try {
    await modal.show('确认删除', '你确定要删除这个项目吗？此操作不可撤销。');
    try {
      await projectService.deleteProject(projectId);
      projects.value = projects.value.filter(p => p.id !== projectId);
      notification.show('项目已删除', 'success');
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
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 2rem; /* 移除顶部的 padding */
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f7f8fa;
}

/* .page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #333;
  font-weight: 600;
} */

/* 创建表单卡片 */
.form-card {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 3rem;
}

.form-card h3 {
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
  min-height: 80px;
  resize: vertical;
}

.btn-create {
  width: 100%;
  padding: 0.9rem 1.5rem;
  background-color: #4a90e2; /* 直接使用颜色值 */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-create:hover {
  background-color: #357abd; /* 直接使用颜色值 */
  transform: translateY(-2px);
}

/* 项目网格 */
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

/* 项目卡片 */
.project-card {
  position: relative;
  background-color: #ffffff;
  border: 1px solid #e0e0e0; /* 添加边框 */
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.project-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.project-card-link {
  text-decoration: none;
  color: inherit;
  flex-grow: 1;
  display: flex;
}

.project-card-content {
  padding: 1.5rem;
  flex-grow: 1;
}

.project-card h2 {
  margin-top: 0;
  margin-bottom: 0.75rem;
  font-size: 1.3rem;
  color: #333;
  transition: color 0.3s;
}

.project-card:hover h2 {
  color: #4a90e2;
}

.project-card p {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}

.btn-delete {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.4rem 0.8rem;
  background-color: #e94b3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  opacity: 0; /* 默认隐藏 */
  transform: scale(0.8);
  transition: opacity 0.3s, transform 0.3s;
}

.project-card:hover .btn-delete {
  opacity: 1; /* 悬停时显示 */
  transform: scale(1);
}

.btn-delete:hover {
  background-color: #d93a2b;
}

/* 状态信息 */
.status-info {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
}

.error {
  color: #e94b3c;
  background-color: rgba(233, 75, 60, 0.05);
  border: 1px solid rgba(233, 75, 60, 0.2);
  border-radius: 8px;
}
</style>
