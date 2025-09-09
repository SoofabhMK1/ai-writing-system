<!-- frontend/src/components/ProjectInfoPanel.vue -->
<template>
  <div class="creation-core card">
    <h3 class="panel-title">项目核心信息 ({{ modelValue.name }})</h3>
    <div class="form-group">
      <label for="bookTitle">书名</label>
      <input id="bookTitle" type="text" :value="modelValue.book_title" @input="$emit('update:modelValue', { ...modelValue, book_title: $event.target.value })" @blur="$emit('save')" placeholder="请输入小说的正式名称" />
    </div>
    <div class="form-group">
      <label for="coreConcept">核心构想 (Seed)</label>
      <textarea id="coreConcept" :value="modelValue.core_concept" @input="$emit('update:modelValue', { ...modelValue, core_concept: $event.target.value })" @blur="$emit('save')" rows="5" placeholder="请详细描述您的故事核心创意、主要情节、角色和主题..."></textarea>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

defineEmits(['update:modelValue', 'save']);
</script>

<style scoped>
.card { background-color: #ffffff; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }
.creation-core { flex-shrink: 0; }
.panel-title { margin: 0 0 1.5rem 0; font-size: 1.3rem; font-weight: 600; border-bottom: 1px solid #e8e8e8; padding-bottom: 1rem; }
.form-group { margin-bottom: 1rem; }
.form-group:last-child { margin-bottom: 0; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #333; }
.form-group input, .form-group textarea { width: 100%; padding: 0.8rem 1rem; border: 1px solid #e0e0e0; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
.form-group textarea { resize: vertical; }
</style>
