<!-- frontend/src/views/ProjectListView.vue -->
<template>
  <WorkspaceLayout>
    <template #left>
      <div class="left-panel-inner">
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
    </template>
    <template #right>
      <OutlineEditor :project="selectedProject" />
    </template>
  </WorkspaceLayout>
  <!-- Create Project Modal -->
  <CreateProjectModal
    :show="showCreateModal"
    @close="showCreateModal = false"
    @project-created="onProjectCreated"
  />
</template>

<script setup>
import { ref, watch } from 'vue'
import { useModalStore } from '@/store/modal'
import WorkspaceLayout from '@/components/layout/WorkspaceLayout.vue'
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
.left-panel-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.left-panel-header {
  padding: var(--spacing-6);
  border-bottom: var(--border-width) solid var(--color-border);
}

.btn-add-project {
  width: 100%;
}

.project-list-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: var(--spacing-6);
}

.right-panel {
  flex-grow: 1;
}
</style>
