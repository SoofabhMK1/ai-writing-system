<!-- frontend/src/components/OutlineEditor.vue -->
<template>
  <div class="outline-editor-card">
    <div v-if="project">
      <div class="editor-header">
        <h2 class="editor-title">编辑大纲: {{ project.name }}</h2>
        <button @click="goToProjectDetail" class="btn-detail">进入项目详情</button>
      </div>
      <div class="editor-content">
        <!-- 大纲编辑功能将在这里实现 -->
        <p>这里是 {{ project.name }} 的大纲编辑区。</p>
        <p>即将推出强大的编辑功能！</p>
      </div>
    </div>
    <div v-else class="placeholder">
      <p>请从左侧选择一个项目以开始编辑大纲。</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  project: {
    type: Object,
    default: null,
  },
});

const router = useRouter();

const goToProjectDetail = () => {
  if (props.project && props.project.id) {
    router.push(`/projects/${props.project.id}`);
  }
};
</script>

<style scoped>
.outline-editor-card {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  height: 100%;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.editor-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 500;
  color: #333;
}

.btn-detail {
  padding: 0.6rem 1.2rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}

.btn-detail:hover {
  background-color: #218838;
  transform: translateY(-2px);
}

.editor-content {
  font-size: 1rem;
  color: #555;
}

.placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-align: center;
  color: #888;
  font-size: 1.2rem;
}
</style>
