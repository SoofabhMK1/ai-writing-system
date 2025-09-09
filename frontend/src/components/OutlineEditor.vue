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
              <span>{{ item.version_name || `版本 ${item.id}` }}</span>
              <small>{{ new Date(item.created_at).toLocaleString() }}</small>
            </li>
          </ul>
          <div v-else class="empty-info">暂无历史版本</div>
        </div>
      </div>
    </div>
    <div v-else class="placeholder">
      <p>请从左侧选择一个项目以开始编辑大纲。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { worldviewService, writingStyleService, generatedOutlineService, aiModelService } from '@/services/settingService';
import projectService from '@/services/projectService';

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

// Fetch data for dropdowns
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

// Fetch history for the current project
const fetchHistory = async (projectId) => {
  if (!projectId) return;
  historyLoading.value = true;
  try {
    const response = await generatedOutlineService.getAllForProject(projectId);
    outlineHistory.value = response.data;
  } catch (error) {
    console.error("Failed to fetch outline history:", error);
    outlineHistory.value = []; // Clear on error
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
    await projectService.update(props.project.id, {
      book_title: editableProject.value.book_title,
      core_concept: editableProject.value.core_concept,
    });
    // Maybe show a subtle notification on success
  } catch (error) {
    console.error("Failed to update project:", error);
  }
};

const handleGenerate = () => {
  console.log("Generating outline with config:", generationConfig.value);
  isGenerating.value = true;

  // Simulate AI generation
  setTimeout(async () => {
    isGenerating.value = false;
    const generatedData = {
      // This is a placeholder for the actual AI-generated outline
      "chapters": [
        { "title": "第一章：新的开始", "summary": "主角开始了新的生活。" },
        { "title": "第二章：风波再起", "summary": "遇到了新的挑战。" }
      ]
    };

    // Simulate a pop-up and save
    if (confirm("大纲生成成功！（模拟）\n\n是否保存此版本？")) {
      const worldview = worldviews.value.find(w => w.id === generationConfig.value.worldview_id);
      const writingStyle = writingStyles.value.find(s => s.id === generationConfig.value.writing_style_id);
      const aiModel = aiModels.value.find(m => m.id === generationConfig.value.ai_model_id);

      const newOutline = {
        project_id: props.project.id,
        version_name: `版本 ${new Date().toLocaleString()}`,
        target_word_count: generationConfig.value.target_word_count,
        worldview_id: generationConfig.value.worldview_id,
        writing_style_id: generationConfig.value.writing_style_id,
        settings_snapshot: {
          worldview: worldview || null,
          writingStyle: writingStyle || null,
          aiModel: aiModel || null,
        },
        outline_data: generatedData,
      };

      try {
        const response = await generatedOutlineService.create(newOutline);
        outlineHistory.value.unshift(response.data);
        // Maybe show a notification
      } catch (error) {
        console.error("Failed to save outline:", error);
        // Show an error notification
      }
    }
  }, 2000);
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.editor-container {
  height: 100%;
}
.workspace {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
}
.card {
  background-color: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
.creation-core {
  flex-shrink: 0;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group:last-child {
  margin-bottom: 0;
}
.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}
.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}
.form-group textarea {
  resize: vertical;
}
.panels-container {
  display: flex;
  gap: 1rem;
  flex-grow: 1;
  min-height: 0;
}
.generation-config, .history-panel {
  width: 50%;
  display: flex;
  flex-direction: column;
}
.panel-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.3rem;
  font-weight: 600;
  border-bottom: 1px solid #e8e8e8;
  padding-bottom: 1rem;
}
.btn-generate {
  margin-top: auto;
  padding: 0.8rem 1.5rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s;
}
.btn-generate:disabled {
  background-color: #a0c7e8;
  cursor: not-allowed;
}
.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
}
.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem;
  border-radius: 6px;
  transition: background-color 0.2s;
}
.history-item:hover {
  background-color: #f7f8fa;
}
.history-item small {
  color: #888;
}
.placeholder, .loading-info, .empty-info {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-align: center;
  color: #888;
  font-size: 1.2rem;
}
</style>
