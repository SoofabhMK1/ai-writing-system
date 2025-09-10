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
        <ProjectInfoPanel
          v-model="editableProject"
          @save="updateProject"
        />
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

    <AIGenerationModal
      :show="isGenerationModalOpen"
      :initial-prompt="generationModalPrompt"
      :generation-params="{ project_id: project?.id, ...generationConfig }"
      @close="isGenerationModalOpen = false"
      @save="saveGeneratedOutline"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { worldviewService, writingStyleService, generatedOutlineService, aiModelService, aiGenerationService } from '@/services/settingService';
import projectService from '@/services/projectService';
import { useNotificationStore } from '@/store/notification';
import { useModalStore } from '@/store/modal';
import AIGenerationModal from './AIGenerationModal.vue';
import GenerationResultModal from './GenerationResultModal.vue';
import GenerationConfigPanel from './GenerationConfigPanel.vue';
import ProjectInfoPanel from './ProjectInfoPanel.vue';
import HistoryPanel from './HistoryPanel.vue';

const notification = useNotificationStore();
const modal = useModalStore();

const props = defineProps({
  project: {
    type: Object,
    default: null,
  },
});

const editableProject = ref({});
const generationConfig = ref({
  worldview_id: null,
  writing_style_id: null,
  ai_model_id: null,
  target_word_count: 5000,
});

const worldviews = ref([]);
const writingStyles = ref([]);
const aiModels = ref([]);
const outlineHistory = ref([]);

const isGenerating = ref(false);
const historyLoading = ref(false);

// State for the AI Generation Modal
const isGenerationModalOpen = ref(false);
const generationModalPrompt = ref('');
const generationModalRef = ref(null);

// State for the History Preview Modal
const isResultModalOpen = ref(false);
const modalContent = ref({});
const modalTitle = ref('');
const isReadOnlyModal = ref(false);

const openResultModal = () => { isResultModalOpen.value = true; };
const closeResultModal = () => { isResultModalOpen.value = false; };

const fetchData = async () => {
  try {
    const [wvRes, wsRes, amRes] = await Promise.all([
      worldviewService.getAll(),
      writingStyleService.getAll(),
      aiModelService.getAll(),
    ]);
    worldviews.value = wvRes.data;
    writingStyles.value = wsRes.data;
    aiModels.value = amRes.data;
  } catch (error) {
    console.error("Failed to fetch settings:", error);
  }
};

const fetchHistory = async (projectId) => {
  if (!projectId) return;
  historyLoading.value = true;
  try {
    const response = await generatedOutlineService.getAllForProject(projectId);
    outlineHistory.value = response.data;
  } catch (error) {
    console.error("Failed to fetch outline history:", error);
    outlineHistory.value = [];
  } finally {
    historyLoading.value = false;
  }
};

watch(() => props.project, (newProject) => {
  if (newProject) {
    editableProject.value = { ...newProject };
    fetchHistory(newProject.id);
  } else {
    editableProject.value = {};
    outlineHistory.value = [];
  }
}, { immediate: true });

const updateProject = async () => {
  if (!props.project || !editableProject.value.id) return;
  try {
    // The backend expects the full ProjectBase model, including the name.
    await projectService.updateProject(props.project.id, {
      name: editableProject.value.name,
      book_title: editableProject.value.book_title,
      core_concept: editableProject.value.core_concept,
      description: editableProject.value.description,
    });
    notification.show('项目信息已保存', 'success', { duration: 2000 });
  } catch (error) {
    console.error("Failed to update project:", error);
    notification.show('项目信息保存失败', 'error');
  }
};

const handleGenerate = async () => {
  if (!generationConfig.value.ai_model_id) {
    notification.show('请先选择一个 AI 模型', 'error');
    return;
  }
  if (!editableProject.value.core_concept) {
    notification.show('请先填写核心构想', 'error');
    return;
  }

  try {
    const requestBody = {
      project_id: props.project.id,
      ...generationConfig.value,
    };
    const response = await aiGenerationService.getInitialPrompt(requestBody);
    generationModalPrompt.value = response.data;
    isGenerationModalOpen.value = true;
  } catch (error) {
    notification.show('获取 Prompt 失败', 'error');
    console.error("Failed to get initial prompt:", error);
  }
};

const saveGeneratedOutline = async (generatedContent) => {
  if (!generatedContent) {
    notification.show('没有内容可保存', 'warn');
    return;
  }
  try {
    // The content from the modal is already clean JSON
    const outlineData = JSON.parse(generatedContent);

    const worldview = worldviews.value.find(w => w.id === generationConfig.value.worldview_id);
    const writingStyle = writingStyles.value.find(s => s.id === generationConfig.value.writing_style_id);
    const aiModel = aiModels.value.find(m => m.id === generationConfig.value.ai_model_id);

    const newOutline = {
      project_id: props.project.id,
      version_name: `版本 ${new Date().toLocaleString()}`,
      target_word_count: generationConfig.value.target_word_count,
      worldview_id: generationConfig.value.worldview_id,
      writing_style_id: generationConfig.value.writing_style_id,
      settings_snapshot: { worldview: worldview || null, writingStyle: writingStyle || null, aiModel: aiModel || null },
      outline_data: outlineData,
    };

    const savedOutline = await generatedOutlineService.create(newOutline);
    outlineHistory.value.unshift(savedOutline.data);
    notification.show('大纲已保存', 'success');
    isGenerationModalOpen.value = false;
  } catch (error) {
    notification.show('保存大纲失败', 'error');
    console.error("Failed to save outline:", error);
  }
};

const previewHistory = (item) => {
  modalTitle.value = `预览历史版本: ${item.version_name || item.id}`;
  modalContent.value = item.outline_data;
  isReadOnlyModal.value = true;
  openResultModal();
};

const deleteHistory = async (id) => {
  try {
    await modal.show('确认删除', '你确定要删除这个历史版本吗？');
    await generatedOutlineService.delete(id);
    outlineHistory.value = outlineHistory.value.filter(item => item.id !== id);
    notification.show('历史版本已删除', 'success');
  } catch (err) {
    if (err.isCanceled) {
      notification.show('删除操作已取消', 'info');
    } else {
      notification.show('删除失败', 'error');
    }
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.editor-container { height: 100%; }
.workspace { display: flex; gap: 1rem; height: 100%; }
.card { background-color: #ffffff; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }

.left-panel {
  width: 400px;
  min-width: 350px;
  display: flex;
  flex-direction: column;
}
.right-panel {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 0;
}

.generation-config {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.config-scroll-area {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 10px;
  margin-right: -10px;
}

.creation-core { flex-shrink: 0; }
.history-panel { flex-grow: 1; display: flex; flex-direction: column; min-height: 0; }

.form-group { margin-bottom: 1rem; }
.form-group:last-child { margin-bottom: 0; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #333; }
.form-group input, .form-group textarea { width: 100%; padding: 0.8rem 1rem; border: 1px solid #e0e0e0; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
.form-group textarea { resize: vertical; }

.form-group-inline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.form-group-inline label {
  flex-basis: 30%;
  margin-bottom: 0;
  font-weight: 500;
}
.form-group-inline select, .form-group-inline input {
  flex-basis: 68%;
  width: auto;
  padding: 0.6rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.9rem;
}

.panel-title { margin: 0 0 1.5rem 0; font-size: 1.3rem; font-weight: 600; border-bottom: 1px solid #e8e8e8; padding-bottom: 1rem; }
.btn-generate { margin-top: 1rem; padding: 0.8rem 1.5rem; background-color: #4a90e2; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; font-weight: 500; transition: background-color 0.3s; flex-shrink: 0; }
.btn-generate:disabled { background-color: #a0c7e8; cursor: not-allowed; }
.history-list { list-style: none; padding: 0; margin: 0; overflow-y: auto; }
.history-item { display: flex; justify-content: space-between; align-items: center; padding: 0.8rem; border-radius: 6px; transition: background-color 0.2s; }
.history-item:hover { background-color: #f0f5ff; }
.history-item-info { display: flex; flex-direction: column; }
.history-item small { color: #888; font-size: 0.8rem; margin-top: 0.25rem; }
.history-item-actions { display: flex; gap: 0.5rem; }
.btn-action { padding: 0.4rem 0.8rem; font-size: 0.8rem; border: none; border-radius: 6px; cursor: pointer; }
.btn-preview { background-color: #6c757d; color: white; }
.btn-preview:hover { background-color: #5a6268; }
.btn-delete { background-color: #e94b3c; color: white; }
.btn-delete:hover { background-color: #d93a2b; }
.placeholder, .loading-info, .empty-info { display: flex; justify-content: center; align-items: center; height: 100%; text-align: center; color: #888; font-size: 1.2rem; }
</style>
