<!-- frontend/src/views/ProjectListView.vue -->
<template>
  <div class="workspace-container">
    <!-- Left Panel -->
    <div class="left-panel">
      <div class="left-panel-header">
        <button @click="showCreateModal = true" class="btn-add-project">+ 创建新项目</button>
      </div>
      <div class="project-list-container">
        <ProjectList 
          ref="projectList" 
          @project-selected="onProjectSelected"
          @project-deleted="onProjectDeleted"
        />
      </div>
    </div>

    <!-- Right Panel -->
    <div class="right-panel">
      <OutlineEditor :project="selectedProject" />
    </div>

    <!-- Create Project Modal -->
    <CreateProjectModal
      :show="showCreateModal"
      @close="showCreateModal = false"
      @project-created="onProjectCreated"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CreateProjectModal from '../components/CreateProjectModal.vue';
import ProjectList from '../components/ProjectList.vue';
import OutlineEditor from '../components/OutlineEditor.vue';

const projectList = ref(null);
const selectedProject = ref(null);
const showCreateModal = ref(false);

const onProjectCreated = (newProject) => {
  if (projectList.value) {
    projectList.value.addProject(newProject);
  }
  // 自动选择新创建的项目
  onProjectSelected(newProject);
};

const onProjectSelected = (project) => {
  selectedProject.value = project;
};

const onProjectDeleted = (deletedProjectId) => {
  if (selectedProject.value && selectedProject.value.id === deletedProjectId) {
    selectedProject.value = null;
  }
};
</script>

<style scoped>
.workspace-container {
  display: flex;
  height: calc(100vh - 60px); /* 假设 NavBar 高度为 60px */
  background-color: #f7f8fa;
  padding: 1rem;
  gap: 1rem;
}

.left-panel {
  width: 400px;
  min-width: 350px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.left-panel-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.btn-add-project {
  width: 100%;
  padding: 0.8rem 1.5rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-add-project:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.project-list-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 0 1.5rem 1.5rem;
}

.right-panel {
  flex-grow: 1;
}
</style>
