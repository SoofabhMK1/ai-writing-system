<!-- frontend/src/components/ProjectList.vue -->
<template>
  <StatusIndicator
    :loading="loading"
    :error="error"
    :empty="!loading && !error && projects.length === 0"
    center
  >
    还没有项目，快创建一个开始吧！
  </StatusIndicator>

  <div v-if="!loading && !error && projects.length > 0" class="project-grid">
    <div
      v-for="project in projects"
      :key="project.id"
      class="project-panel"
      @click="$emit('project-selected', project)"
    >
      <div class="project-panel-content">
        <h2>{{ project.name }}</h2>
        <p>{{ project.description || '暂无描述' }}</p>
      </div>
      <div class="card-actions">
        <button
          @click.stop="goToProjectDetail(project.id)"
          class="btn btn-secondary btn-sm"
        >
          详情
        </button>
        <button
          @click.stop="handleDeleteProject(project.id)"
          class="btn btn-danger btn-sm"
        >
          删除
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import projectService from '../services/projectService'
import StatusIndicator from './common/StatusIndicator.vue'
import { useModalStore } from '@/store/modal.js'
import { useNotificationStore } from '@/store/notification.js'

const emit = defineEmits(['project-selected', 'project-deleted'])
const router = useRouter()
const modal = useModalStore()
const notification = useNotificationStore()

const projects = ref([])
const loading = ref(true)
const error = ref(null)

const fetchProjects = async () => {
  try {
    const response = await projectService.getProjects()
    projects.value = response.data
  } catch (err) {
    console.error(err)
    error.value = '无法连接到服务器或 API 出错。'
  } finally {
    loading.value = false
  }
}

const goToProjectDetail = (projectId) => {
  router.push(`/projects/${projectId}`)
}

const handleDeleteProject = async (projectId) => {
  try {
    await modal.show('确认删除', '你确定要删除这个项目吗？此操作不可撤销。')
    try {
      await projectService.deleteProject(projectId)
      projects.value = projects.value.filter((p) => p.id !== projectId)
      notification.show('项目已删除', 'success')
      emit('project-deleted', projectId) // Emit event on successful deletion
    } catch (err) {
      console.error(err)
      notification.show('删除项目失败！', 'error')
    }
  } catch {
    console.log('删除操作已取消')
    notification.show('删除操作已取消', 'info')
  }
}

onMounted(() => {
  fetchProjects()
})

// Expose a method to be called by the parent
defineExpose({
  addProject(project) {
    projects.value.unshift(project)
  },
})
</script>

<style scoped>
.project-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-6);
}

.project-panel {
  position: relative;
  background-color: var(--color-surface);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: var(--transition-base);
  cursor: pointer;
}

.project-panel:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
}

.project-panel-content {
  padding: var(--spacing-6);
}

.project-panel h2 {
  margin-top: 0;
  margin-bottom: var(--spacing-2);
  font-size: var(--font-size-lg);
  color: var(--color-text);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-panel p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  line-height: 1.5;
}

.card-actions {
  position: absolute;
  top: var(--spacing-4);
  right: var(--spacing-4);
  display: flex;
  gap: var(--spacing-2);
  opacity: 0;
  transform: translateY(4px);
  transition: var(--transition-base);
}

.project-panel:hover .card-actions {
  opacity: 1;
  transform: translateY(0);
}

.btn-sm {
  padding: var(--spacing-1) var(--spacing-2);
  font-size: var(--font-size-xs);
}

</style>
