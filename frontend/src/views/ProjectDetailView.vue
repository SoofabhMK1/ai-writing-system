<template>
  <div class="project-detail-layout">
    <!-- 左栏：大纲编辑器 -->
    <div class="outline-panel">
      <div class="panel-header">
        <h3>大纲</h3>
        <button v-if="outline.length > 0" @click="handleAddNode(null)">添加顶级节点</button>
      </div>

      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="outline.length === 0" class="no-outline">
        <p>此项目还没有大纲。</p>
        <button @click="handleAddNode(null)">创建第一个节点</button>
      </div>
      <div v-else class="outline-tree">
        <OutlineNodeItem
          v-for="rootNode in outline"
          :key="rootNode.id"
          :node="rootNode"
          @add-child="handleAddNode"
          @delete-node="handleDeleteNode"
          @update-title="handleUpdateNode"
        />
      </div>
    </div>

    <!-- 右栏：内容工作区 -->
    <div class="content-panel">
      <!-- 1. 内容区 -->
      <div class="content-editor-wrapper">
        <textarea 
          class="content-textarea"
          placeholder="AI 生成的内容将显示在这里..."
        ></textarea>
      </div>

      <!-- 2. AI 指令设定区 -->
      <div class="ai-settings-wrapper">
        <div class="setting-item">
          <label for="word-count">目标字数</label>
          <input id="word-count" type="number" placeholder="例如: 800">
        </div>
        <div class="setting-item">
          <label for="brief">内容蓝图 / 写作指令</label>
          <textarea 
            id="brief"
            rows="5"
            placeholder="请输入对本小节的核心要求、关键词、写作风格等..."
          ></textarea>
        </div>
      </div>

      <!-- 3. 操作按钮区 -->
      <div class="action-buttons-wrapper">
        <button class="run-btn">运行</button>
        <button class="check-btn" disabled>检查 (暂不可用)</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import projectService from '../services/projectService';
import outlineNodeService from '../services/outlineNodeService';
import OutlineNodeItem from '../components/OutlineNodeItem.vue';
import { useModalStore } from '@/store/modal.js';
import { useNotificationStore } from '@/store/notification.js';
import { usePromptStore } from '@/store/prompt.js';

const route = useRoute();
const modal = useModalStore();
const notification = useNotificationStore();
const prompt = usePromptStore();
const project = ref(null);
const loading = ref(true);
const error = ref(null);

const outline = ref([]); // <-- 2. 创建一个新状态来存储大纲数据

const fetchProjectData = async () => {
  const projectId = route.params.projectId;
  // 进入加载状态
  loading.value = true; 
  error.value = null;
  try {
    const projectResponse = await projectService.getProject(projectId);
    project.value = projectResponse.data;
    const outlineResponse = await outlineNodeService.getOutlineForProject(projectId);
    outline.value = outlineResponse.data;
  } catch (err) {
    console.error(err);
    error.value = '加载项目失败。';
  } finally {
    loading.value = false;
  }
};

const handleAddNode = async (parentId) => {
  try {
    const title = await prompt.show('创建新节点', '请输入新节点的标题：', '新章节');
    
    if (title && title.trim()) {
      try {
        const newNodeData = {
          title: title,
          project_id: parseInt(route.params.projectId),
          parent_id: parentId
        };
        await outlineNodeService.createNode(newNodeData);
        fetchProjectData();
        notification.show('节点创建成功', 'success');
      } catch (err) {
        console.error(err);
        notification.show('创建节点失败！', 'error');
      }
    } else {
      notification.show('标题不能为空', 'error');
    }
  } catch (err) {
    // 用户点击了取消
    notification.show('操作已取消', 'info');
  }
};

const handleDeleteNode = async (nodeId) => {
  try {
    await modal.show('确认删除', '确定要删除这个节点及其所有子节点吗？此操作不可撤销。');
    // 用户确认后执行删除
    try {
      await outlineNodeService.deleteNode(nodeId);
      fetchProjectData();
      notification.show('节点已删除', 'success');
    } catch (err) {
      console.error(err);
      notification.show('删除节点失败！', 'error');
    }
  } catch (isCanceled) {
    // 用户取消
    notification.show('删除操作已取消', 'info');
  }
};

const handleUpdateNode = async (payload) => {
  // payload 是一个对象，例如 { id: 1, title: '新的标题' }
  try {
    await outlineNodeService.updateNode(payload.id, { title: payload.title });
    // 更新成功后，为了保证数据一致性，重新获取整个大纲
    // 这是一个简单可靠的策略
    fetchProjectData();
    notification.show('节点更新成功', 'success');
  } catch (err) {
    console.error(err);
    notification.show('更新节点失败！', 'error');
  }
};

onMounted(() => {
  fetchProjectData();
});
</script>

<style scoped>
.project-detail-layout {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.outline-panel {
  flex: 0 0 350px; /* 固定宽度侧边栏: 不放大，不缩小，基础宽度减小到350px */
  background-color: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  height: calc(100vh - 120px); /* 调整高度以适应padding */
  overflow-y: auto;
}

.content-panel {
  flex: 1 1 auto; /* 自适应主内容区: 放大，缩小，自动计算基础宽度 */
  min-width: 0; /* 防止内容溢出的关键 */
  background-color: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  /* 新增flex布局，让内部三块垂直排列 */
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: calc(100vh - 100px);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
  /* 让header不随滚动条滚动 */
  flex-shrink: 0;
}

.panel-header h3 {
  margin: 0;
}

/* === 右栏新增样式 === */
.content-editor-wrapper {
  flex-grow: 1; /* 占据所有剩余垂直空间 */
  display: flex; /* 使用flex布局让textarea充满容器 */
}

.content-textarea {
  width: 100%;
  height: 100%;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 1rem;
  font-size: 1rem;
  resize: none; /* 通常由父容器控制大小，禁用手动resize */
  box-sizing: border-box;
}

.ai-settings-wrapper {
  display: flex;
  flex-direction: column;
  gap: 15px;
  flex-shrink: 0; /* 不收缩 */
}

.setting-item label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.setting-item input,
.setting-item textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 1rem;
}

.action-buttons-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid #eee;
  padding-top: 1rem;
  margin-top: auto; /* 将按钮推到底部 */
  flex-shrink: 0; /* 不收缩 */
}

.action-buttons-wrapper button {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.run-btn {
  background-color: #007bff;
  color: white;
}
.run-btn:hover {
  background-color: #0056b3;
}

.check-btn {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
}

/* === 保留并调整的旧样式 === */
.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error {
  color: red;
}

.no-outline {
  text-align: center;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
}


</style>
