<!-- frontend/src/components/ProjectInfoPanel.vue -->
<template>
  <div class="info-panel card">
    <h3 class="panel-title">项目核心信息 ({{ modelValue.name }})</h3>
    <div class="form-group">
      <label for="bookTitle">书名</label>
      <input
        id="bookTitle"
        type="text"
        class="form-control"
        :value="modelValue.book_title"
        @input="
          $emit('update:modelValue', {
            ...modelValue,
            book_title: $event.target.value,
          })
        "
        @blur="$emit('save')"
        placeholder="请输入小说的正式名称"
      />
    </div>
    <div class="form-group">
      <label for="coreConcept">核心构想 (Seed)</label>
      <textarea
        id="coreConcept"
        class="form-control"
        :value="modelValue.core_concept"
        @input="
          $emit('update:modelValue', {
            ...modelValue,
            core_concept: $event.target.value,
          })
        "
        @blur="$emit('save')"
        rows="5"
        placeholder="请详细描述您的故事核心创意、主要情节、角色和主题..."
      ></textarea>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
})

defineEmits(['update:modelValue', 'save'])
</script>

<style scoped>
.info-panel {
  height: 100%;
}
.panel-title {
  margin: 0 0 var(--spacing-6) 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text);
  padding-bottom: var(--spacing-4);
  border-bottom: var(--border-width) solid var(--color-border);
}
.form-group {
  margin-bottom: var(--spacing-5);
}
.form-group:last-child {
  margin-bottom: 0;
}
.form-group label {
  display: block;
  font-weight: 500;
  color: var(--color-text);
  margin-bottom: var(--spacing-2);
  font-size: var(--font-size-sm);
}
.form-control {
  width: 100%;
  padding: var(--spacing-3) var(--spacing-4);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  background-color: var(--color-background);
  color: var(--color-text);
  transition: var(--transition-base);
  box-sizing: border-box;
}
.form-control:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary), 0.2);
}
textarea.form-control {
  resize: vertical;
  min-height: 120px;
}
</style>
