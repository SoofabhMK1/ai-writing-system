<!-- frontend/src/views/ProjectListView.vue -->
<template>
  <div class="workspace-container">
    <!-- Left Panel -->
    <div class="left-panel">
      <div class="left-panel-header">
        <button
          @click="showCreateModal = true"
          class="btn btn-primary btn-add-project"
        >
          + 创建新项目
        </button>
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
import { ref, watch } from 'vue'
import { useModalStore } from '@/store/modal'
import CreateProjectModal from '../components/CreateProjectModal.vue'
import ProjectList from '../components/ProjectList.vue'
import OutlineEditor from '../components/OutlineEditor.vue'

const projectList = ref(null)
const selectedProject = ref(null)
const showCreateModal = ref(false)
const modalStore = useModalStore()

watch(showCreateModal, (newValue) => {
  modalStore.setActive(newValue)
})

const onProjectCreated = (newProject) => {
  if (projectList.value) {
    projectList.value.addProject(newProject)
  }
  // 自动选择新创建的项目
  onProjectSelected(newProject)
}

const onProjectSelected = (project) => {
  selectedProject.value = project
}

const onProjectDeleted = (deletedProjectId) => {
  if (selectedProject.value && selectedProject.value.id === deletedProjectId) {
    selectedProject.value = null
  }
}
</script>

<style scoped>
.workspace-container {
  display: flex;
  height: 100%; /* Fill the .main-content area */
  gap: var(--spacing-8);
}

.left-panel {
  width: 280px;
  min-width: 240px;
  display: flex;
  flex-direction: column;
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.left-panel-header {
  padding: var(--spacing-6);
  border-bottom: var(--border-width) solid var(--color-border);
}

.btn-add-project {
  /* This button now inherits from .btn and .btn-primary from style.css */
  width: 100%;
}

.project-list-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: var(--spacing-6);
}

.right-panel {
  flex-grow: 1;
  /* The OutlineEditor will sit here, it should have its own styling */
}
</style>
