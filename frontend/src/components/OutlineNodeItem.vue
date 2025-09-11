<template>
  <div class="node-item">
    <div class="node-content">
      <!-- 核心修改：根据 isEditing 状态显示 span 或 input -->
      <span v-if="!isEditing" @click="startEditing" class="node-title">{{ node.title }}</span>
      <input
        v-else
        ref="titleInput"
        v-model="editableTitle"
        @blur="saveEdit"
        @keydown.enter.prevent="saveEdit"
        @keydown.esc="cancelEdit"
        class="title-input"
      />

      <div class="node-actions">
        <button @click="emitAddChild(node.id)" class="btn btn-sm">＋</button>
        <button class="btn btn-sm btn-danger" @click="emitDeleteNode(node.id)">－</button>
      </div>
    </div>

    <div v-if="node.children && node.children.length > 0" class="node-children">
      <!-- 传递 update-title 事件 -->
      <OutlineNodeItem
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        @add-child="emitAddChild"
        @delete-node="emitDeleteNode"
        @update-title="emitUpdateTitle"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';

const props = defineProps({
  node: {
    type: Object,
    required: true
  }
});

// 子组件管理自己的事件冒泡
const emit = defineEmits(['addChild', 'deleteNode', 'updateTitle']);

// --- 新增状态和逻辑 ---
const isEditing = ref(false);
const editableTitle = ref(props.node.title);
const titleInput = ref(null); // 用于获取 input 元素的引用

const startEditing = async () => {
  isEditing.value = true;
  // nextTick 确保在 DOM 更新后执行，这样 input 才可见
  await nextTick();
  titleInput.value?.focus(); // 自动聚焦到输入框
};

const saveEdit = () => {
  // 只有在标题实际发生改变时才发出事件
  if (editableTitle.value !== props.node.title && editableTitle.value.trim() !== '') {
    emit('updateTitle', { id: props.node.id, title: editableTitle.value });
  }
  isEditing.value = false;
};

const cancelEdit = () => {
  editableTitle.value = props.node.title; // 恢复原始标题
  isEditing.value = false;
};

// --- 转发事件的函数 (无变化) ---
const emitAddChild = (parentId) => emit('addChild', parentId);
const emitDeleteNode = (nodeId) => emit('deleteNode', nodeId);
// --- 新增的转发函数 ---
const emitUpdateTitle = (payload) => emit('updateTitle', payload);

</script>

<style scoped>
.node-item {
  padding-left: var(--spacing-6);
  position: relative;
}
.node-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-3) var(--spacing-4);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-md);
  margin-top: var(--spacing-2);
  background-color: var(--color-surface);
  transition: var(--transition-base);
}
.node-content:hover {
  border-color: var(--color-primary);
  background-color: var(--color-background);
}
.node-title {
  font-weight: 500;
  cursor: pointer;
  flex-grow: 1;
  padding: var(--spacing-1) 0;
}
.node-actions {
  display: flex;
  gap: var(--spacing-2);
  opacity: 0;
  transition: var(--transition-base);
}
.node-content:hover .node-actions {
  opacity: 1;
}
.btn-sm {
  padding: var(--spacing-1) var(--spacing-2);
  font-size: var(--font-size-xs);
}
.node-children {
  border-left: 2px solid var(--color-border);
  margin-top: var(--spacing-2);
}
.title-input {
  font-weight: 500;
  font-size: 1em;
  padding: var(--spacing-1) 0;
  border: none;
  border-bottom: 2px solid var(--color-primary);
  background-color: transparent;
  color: var(--color-text);
  flex-grow: 1;
}
.title-input:focus {
  outline: none;
}
</style>
