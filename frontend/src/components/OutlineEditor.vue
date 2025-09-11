<!-- frontend/src/components/OutlineEditor.vue -->
<template>
  <div class="editor-container">
    <div v-if="project" class="workspace">
      <GenerationConfigPanel
        v-model="generationConfig"
        :worldviews="worldviews"
        :writing-styles="writingStyles"
        :ai-models="aiModels"
        :is-generating="isGenerating"
        @generate="handleGenerate"
      />

      <div class="right-panel">
        <ProjectInfoPanel v-model="editableProject" @save="updateProject" />
        <HistoryPanel
          :history="outlineHistory"
          :loading="historyLoading"
          @preview="previewHistory"
          @delete="deleteHistory"
        />
      </div>
    </div>
    <div v-else class="placeholder">
      <p>请从左侧选择一个项目以开始编辑大纲。</p>
    </div>

    <GenerationResultModal
      :show="isResultModalOpen"
      :title="modalTitle"
      :content="modalContent"
      :is-read-only="isReadOnlyModal"
      @close="closeResultModal"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  worldviewService,
  writingStyleService,
  generatedOutlineService,
  aiModelService,
  aiGenerationService,
} from '@/services/settingService'
import projectService from '@/services/projectService'
import { useNotificationStore } from '@/store/notification'
import { useModalStore } from '@/store/modal'
import { useConversationStore } from '@/store/conversation'
import GenerationResultModal from './GenerationResultModal.vue'
import GenerationConfigPanel from './GenerationConfigPanel.vue'
import ProjectInfoPanel from './ProjectInfoPanel.vue'
import HistoryPanel from './HistoryPanel.vue'

const notification = useNotificationStore()
const modal = useModalStore()
const router = useRouter()
const conversationStore = useConversationStore()

const props = defineProps({
  project: {
    type: Object,
    default: null,
  },
})

const editableProject = ref({})
const generationConfig = ref({
  worldview_id: null,
  writing_style_id: null,
  ai_model_id: null,
  target_word_count: 100000,
})

const worldviews = ref([])
const writingStyles = ref([])
const aiModels = ref([])
const outlineHistory = ref([])

const isGenerating = ref(false)
const historyLoading = ref(false)

// State for the History Preview Modal
const isResultModalOpen = ref(false)
const modalContent = ref({})
const modalTitle = ref('')
const isReadOnlyModal = ref(false)

const openResultModal = () => {
  isResultModalOpen.value = true
}
const closeResultModal = () => {
  isResultModalOpen.value = false
}

const fetchData = async () => {
  try {
    const [wvRes, wsRes, amRes] = await Promise.all([
      worldviewService.getAll(),
      writingStyleService.getAll(),
      aiModelService.getAll(),
    ])
    worldviews.value = wvRes.data
    writingStyles.value = wsRes.data
    aiModels.value = amRes.data
  } catch (error) {
    console.error('Failed to fetch settings:', error)
  }
}

const fetchHistory = async (projectId) => {
  if (!projectId) return
  historyLoading.value = true
  try {
    const response = await generatedOutlineService.getAllForProject(projectId)
    outlineHistory.value = response.data
  } catch (error) {
    console.error('Failed to fetch outline history:', error)
    outlineHistory.value = []
  } finally {
    historyLoading.value = false
  }
}

watch(
  () => props.project,
  (newProject) => {
    if (newProject) {
      editableProject.value = { ...newProject }
      fetchHistory(newProject.id)
    } else {
      editableProject.value = {}
      outlineHistory.value = []
    }
  },
  { immediate: true },
)

const updateProject = async () => {
  if (!props.project || !editableProject.value.id) return
  try {
    // The backend expects the full ProjectBase model, including the name.
    await projectService.updateProject(props.project.id, {
      name: editableProject.value.name,
      book_title: editableProject.value.book_title,
      core_concept: editableProject.value.core_concept,
      description: editableProject.value.description,
    })
    notification.show('项目信息已保存', 'success', { duration: 2000 })
  } catch (error) {
    console.error('Failed to update project:', error)
    notification.show('项目信息保存失败', 'error')
  }
}

const handleGenerate = async () => {
  if (!generationConfig.value.ai_model_id) {
    notification.show('请先选择一个 AI 模型', 'error')
    return
  }
  if (!editableProject.value.core_concept) {
    notification.show('请先填写核心构想', 'error')
    return
  }

  try {
    const requestBody = {
      project_id: props.project.id,
      ...generationConfig.value,
    }
    const response = await aiGenerationService.getInitialPrompt(requestBody)
    const initialPrompt = response.data

    conversationStore.startNewConversation()
    conversationStore.setCachedInitialPrompt(initialPrompt)

    router.push({
      name: 'Conversation',
      params: { projectId: props.project.id },
    })
  } catch (error) {
    notification.show('获取 Prompt 失败', 'error')
    console.error('Failed to get initial prompt:', error)
  }
}


const previewHistory = (item) => {
  modalTitle.value = `预览历史版本: ${item.version_name || item.id}`
  modalContent.value = item.outline_data
  isReadOnlyModal.value = true
  openResultModal()
}

const deleteHistory = async (id) => {
  try {
    await modal.show('确认删除', '你确定要删除这个历史版本吗？')
    await generatedOutlineService.delete(id)
    outlineHistory.value = outlineHistory.value.filter((item) => item.id !== id)
    notification.show('历史版本已删除', 'success')
  } catch (err) {
    if (err.isCanceled) {
      notification.show('删除操作已取消', 'info')
    } else {
      notification.show('删除失败', 'error')
    }
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.editor-container {
  height: 100%;
}
.workspace {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: var(--spacing-8);
  height: 100%;
}
.right-panel {
  display: grid;
  grid-template-rows: auto 1fr;
  gap: var(--spacing-8);
  min-height: 0;
}
.placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-align: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-lg);
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
}
</style>
