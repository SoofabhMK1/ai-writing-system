<template>
  <div class="project-detail-layout">
    <!-- 左栏：大纲编辑器 -->
    <div class="outline-panel card">
      <div class="panel-header">
        <h3>大纲</h3>
        <button
          v-if="outline.length > 0"
          @click="handleAddNode(null)"
          class="btn btn-sm"
        >
          添加顶级节点
        </button>
      </div>

      <div v-if="loading" class="status-info">加载中...</div>
      <div v-else-if="error" class="status-info error">{{ error }}</div>
      <div v-else-if="outline.length === 0" class="no-outline status-info">
        <p>此项目还没有大纲。</p>
        <button @click="handleAddNode(null)" class="btn btn-primary">
          创建第一个节点
        </button>
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
    <div class="content-panel card">
      <!-- 1. 内容区 -->
      <div class="content-editor-wrapper">
        <textarea
          class="content-textarea form-control"
          placeholder="AI 生成的内容将显示在这里..."
        ></textarea>
      </div>

      <!-- 2. AI 指令设定区 -->
      <div class="ai-settings-wrapper">
        <div class="setting-item">
          <label for="word-count">目标字数</label>
          <input
            id="word-count"
            type="number"
            class="form-control"
            placeholder="例如: 800"
          />
        </div>
        <div class="setting-item">
          <label for="brief">内容蓝图 / 写作指令</label>
          <textarea
            id="brief"
            rows="5"
            class="form-control"
            placeholder="请输入对本小节的核心要求、关键词、写作风格等..."
          ></textarea>
        </div>
      </div>

      <!-- 3. 操作按钮区 -->
      <div class="action-buttons-wrapper">
        <button class="btn btn-primary">运行</button>
        <button class="btn" disabled>检查 (暂不可用)</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import projectService from '../services/projectService'
import outlineNodeService from '../services/outlineNodeService'
import OutlineNodeItem from '../components/OutlineNodeItem.vue'
import { useModalStore } from '@/store/modal.js'
import { useNotificationStore } from '@/store/notification.js'
import { usePromptStore } from '@/store/prompt.js'

const route = useRoute()
const modal = useModalStore()
const notification = useNotificationStore()
const prompt = usePromptStore()
const project = ref(null)
const loading = ref(true)
const error = ref(null)

const outline = ref([]) // <-- 2. 创建一个新状态来存储大纲数据

const fetchProjectData = async () => {
  const projectId = route.params.projectId
  // 进入加载状态
  loading.value = true
  error.value = null
  try {
    const projectResponse = await projectService.getProject(projectId)
    project.value = projectResponse.data
    const outlineResponse =
      await outlineNodeService.getOutlineForProject(projectId)
    outline.value = outlineResponse.data
  } catch (err) {
    console.error(err)
    error.value = '加载项目失败。'
  } finally {
    loading.value = false
  }
}

const handleAddNode = async (parentId) => {
  try {
    const title = await prompt.show(
      '创建新节点',
      '请输入新节点的标题：',
      '新章节',
    )

    if (title && title.trim()) {
      try {
        const newNodeData = {
          title: title,
          project_id: parseInt(route.params.projectId),
          parent_id: parentId,
        }
        await outlineNodeService.createNode(newNodeData)
        fetchProjectData()
        notification.show('节点创建成功', 'success')
      } catch (err) {
        console.error(err)
        notification.show('创建节点失败！', 'error')
      }
    } else {
      notification.show('标题不能为空', 'error')
    }
  } catch {
    // 用户点击了取消
    notification.show('操作已取消', 'info')
  }
}

const handleDeleteNode = async (nodeId) => {
  try {
    await modal.show(
      '确认删除',
      '确定要删除这个节点及其所有子节点吗？此操作不可撤销。',
    )
    // 用户确认后执行删除
    try {
      await outlineNodeService.deleteNode(nodeId)
      fetchProjectData()
      notification.show('节点已删除', 'success')
    } catch (err) {
      console.error(err)
      notification.show('删除节点失败！', 'error')
    }
  } catch {
    // 用户取消
    notification.show('删除操作已取消', 'info')
  }
}

const handleUpdateNode = async (payload) => {
  // payload 是一个对象，例如 { id: 1, title: '新的标题' }
  try {
    await outlineNodeService.updateNode(payload.id, { title: payload.title })
    // 更新成功后，为了保证数据一致性，重新获取整个大纲
    // 这是一个简单可靠的策略
    fetchProjectData()
    notification.show('节点更新成功', 'success')
  } catch (err) {
    console.error(err)
    notification.show('更新节点失败！', 'error')
  }
}

onMounted(() => {
  fetchProjectData()
})
</script>

<style scoped>
.project-detail-layout {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: var(--spacing-8);
  height: 100%;
}

.outline-panel,
.content-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-4);
  padding-bottom: var(--spacing-4);
  border-bottom: var(--border-width) solid var(--color-border);
  flex-shrink: 0;
}

.panel-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
}

.outline-tree {
  overflow-y: auto;
  flex-grow: 1;
}

.content-panel {
  gap: var(--spacing-6);
}

.content-editor-wrapper {
  flex-grow: 1;
  display: flex;
}

.content-textarea {
  height: 100%;
  resize: none;
}

.ai-settings-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  flex-shrink: 0;
}

.setting-item label {
  display: block;
  font-weight: 500;
  margin-bottom: var(--spacing-2);
  font-size: var(--font-size-sm);
}

.action-buttons-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-4);
  border-top: var(--border-width) solid var(--color-border);
  padding-top: var(--spacing-6);
  margin-top: auto;
  flex-shrink: 0;
}

.status-info {
  text-align: center;
  padding: var(--spacing-12) var(--spacing-8);
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-4);
}

.status-info.error {
  color: var(--color-danger);
}

.no-outline {
  background-color: var(--color-background);
  border-radius: var(--border-radius-md);
}
</style>
