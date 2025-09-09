<!-- frontend/src/components/OutlineEditor.vue -->
<template>
  <div class="editor-container">
    <div v-if="project" class="workspace">
      <!-- Top Section: Creation Core -->
      <div class="creation-core card">
        <div class="form-group">
          <label for="bookTitle">书名</label>
          <input id="bookTitle" type="text" v-model="editableProject.book_title" @blur="updateProject" placeholder="请输入小说的正式名称" />
        </div>
        <div class="form-group">
          <label for="coreConcept">核心构想 (Seed)</label>
          <textarea id="coreConcept" v-model="editableProject.core_concept" @blur="updateProject" rows="5" placeholder="请详细描述您的故事核心创意、主要情节、角色和主题..."></textarea>
        </div>
      </div>

      <div class="panels-container">
        <!-- Left Panel: Generation Config -->
        <div class="generation-config card">
          <h3 class="panel-title">生成配置</h3>
          <div class="config-scroll-area">
            <div class="form-group">
              <label for="worldview">世界观</label>
              <select id="worldview" v-model="generationConfig.worldview_id">
                <option :value="null">-- 选择一个世界观 --</option>
                <option v-for="w in worldviews" :key="w.id" :value="w.id">{{ w.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="writingStyle">文风</label>
              <select id="writingStyle" v-model="generationConfig.writing_style_id">
                <option :value="null">-- 选择一个文风 --</option>
                <option v-for="s in writingStyles" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="aiModel">AI 模型</label>
              <select id="aiModel" v-model="generationConfig.ai_model_id">
                <option :value="null">-- 选择一个 AI 模型 --</option>
                <option v-for="m in aiModels" :key="m.id" :value="m.id">{{ m.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="wordCount">目标总字数</label>
              <input id="wordCount" type="number" v-model.number="generationConfig.target_word_count" placeholder="例如：100000" />
            </div>
          </div>
          <button @click="handleGenerate" class="btn-generate" :disabled="isGenerating">
            {{ isGenerating ? '正在生成中...' : '生成大纲' }}
          </button>
        </div>

        <!-- Right Panel: History -->
        <div class="history-panel card">
          <h3 class="panel-title">大纲历史版本</h3>
          <div v-if="historyLoading" class="loading-info">正在加载历史版本...</div>
          <ul v-else-if="outlineHistory.length > 0" class="history-list">
            <li v-for="item in outlineHistory" :key="item.id" class="history-item">
              <div class="history-item-info">
                <span>{{ item.version_name || `版本 ${item.id}` }}</span>
                <small>{{ new Date(item.created_at).toLocaleString() }}</small>
              </div>
              <div class="history-item-actions">
                <button @click="previewHistory(item)" class="btn-action btn-preview">预览</button>
                <button @click="deleteHistory(item.id)" class="btn-action btn-delete">删除</button>
              </div>
            </li>
          </ul>
          <div v-else class="empty-info">暂无历史版本</div>
        </div>
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
import GenerationResultModal from './GenerationResultModal.vue';

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
  target_word_count: 100000,
});

const worldviews = ref([]);
const writingStyles = ref([]);
const aiModels = ref([]);
const outlineHistory = ref([]);

const isGenerating = ref(false);
const historyLoading = ref(false);

const isResultModalOpen = ref(false);
const modalContent = ref({});
const modalTitle = ref('');
const isReadOnlyModal = ref(false);
const lastGeneratedOutline = ref(null);

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
    await projectService.updateProject(props.project.id, {
      book_title: editableProject.value.book_title,
      core_concept: editableProject.value.core_concept,
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
  isGenerating.value = true;
  notification.show('正在生成大纲，请稍候...', 'info');
  try {
    const requestBody = { project_id: props.project.id, ...generationConfig.value };
    const response = await aiGenerationService.generateOutline(requestBody);
    const outlineData = JSON.parse(response.data.outline);
    
    const worldview = worldviews.value.find(w => w.id === generationConfig.value.worldview_id);
    const writingStyle = writingStyles.value.find(s => s.id === generationConfig.value.writing_style_id);
    const aiModel = aiModels.value.find(m => m.id === generationConfig.value.ai_model_id);

    lastGeneratedOutline.value = {
      project_id: props.project.id,
      version_name: `版本 ${new Date().toLocaleString()}`,
      target_word_count: generationConfig.value.target_word_count,
      worldview_id: generationConfig.value.worldview_id,
      writing_style_id: generationConfig.value.writing_style_id,
      settings_snapshot: { worldview: worldview || null, writingStyle: writingStyle || null, aiModel: aiModel || null },
      outline_data: outlineData,
    };

    modalTitle.value = '生成成功！';
    modalContent.value = outlineData;
    isReadOnlyModal.value = false;
    openResultModal();

  } catch (error) {
    const detail = error.response?.data?.detail || '生成失败，请检查后台日志。';
    notification.show(`生成失败: ${detail}`, 'error', { duration: 5000 });
    console.error("Failed to generate outline:", error);
  } finally {
    isGenerating.value = false;
  }
};

const saveGeneratedOutline = async () => {
  if (!lastGeneratedOutline.value) return;
  try {
    const savedOutline = await generatedOutlineService.create(lastGeneratedOutline.value);
    outlineHistory.value.unshift(savedOutline.data);
    notification.show('大纲已保存', 'success');
    closeResultModal();
  } catch (error) {
    notification.show('保存失败', 'error');
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
.workspace { display: flex; flex-direction: column; gap: 1rem; height: 100%; }
.card { background-color: #ffffff; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }
.creation-core { flex-shrink: 0; }
.form-group { margin-bottom: 1rem; }
.form-group:last-child { margin-bottom: 0; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #333; }
.form-group input, .form-group textarea, .form-group select { width: 100%; padding: 0.8rem 1rem; border: 1px solid #e0e0e0; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
.form-group textarea { resize: vertical; }
.panels-container { display: flex; gap: 1rem; flex-grow: 1; min-height: 0; }
.generation-config, .history-panel { width: 50%; display: flex; flex-direction: column; }
.generation-config { overflow-y: auto; }
.config-scroll-area { flex-grow: 1; }
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
