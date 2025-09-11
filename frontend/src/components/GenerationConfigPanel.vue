<!-- frontend/src/components/GenerationConfigPanel.vue -->
<template>
  <div class="config-panel card">
    <h3 class="panel-title">生成配置</h3>
    <div class="config-scroll-area">
      <div class="form-group">
        <label for="worldview">世界观</label>
        <select id="worldview" class="form-control" :value="modelValue.worldview_id" @change="$emit('update:modelValue', { ...modelValue, worldview_id: $event.target.value })">
          <option :value="null">-- 选择 --</option>
          <option v-for="w in worldviews" :key="w.id" :value="w.id">{{ w.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="writingStyle">文风</label>
        <select id="writingStyle" class="form-control" :value="modelValue.writing_style_id" @change="$emit('update:modelValue', { ...modelValue, writing_style_id: $event.target.value })">
          <option :value="null">-- 选择 --</option>
          <option v-for="s in writingStyles" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="aiModel">AI 模型</label>
        <select id="aiModel" class="form-control" :value="modelValue.ai_model_id" @change="$emit('update:modelValue', { ...modelValue, ai_model_id: $event.target.value })">
          <option :value="null">-- 选择 --</option>
          <option v-for="m in aiModels" :key="m.id" :value="m.id">{{ m.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="wordCount">目标总字数</label>
        <input id="wordCount" type="number" class="form-control" :value="modelValue.target_word_count" @input="$emit('update:modelValue', { ...modelValue, target_word_count: $event.target.value })" placeholder="例如：100000" />
      </div>
    </div>
    <button @click="$emit('generate')" class="btn btn-primary btn-generate" :disabled="isGenerating">
      {{ isGenerating ? '正在生成中...' : '生成大纲' }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  worldviews: {
    type: Array,
    default: () => [],
  },
  writingStyles: {
    type: Array,
    default: () => [],
  },
  aiModels: {
    type: Array,
    default: () => [],
  },
  isGenerating: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['update:modelValue', 'generate']);
</script>

<style scoped>
.config-panel {
  display: flex;
  flex-direction: column;
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
.config-scroll-area {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: var(--spacing-2); /* For scrollbar */
  margin-right: calc(-1 * var(--spacing-2));
}
.form-group {
  margin-bottom: var(--spacing-5);
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
select.form-control {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}
.btn-generate {
  margin-top: var(--spacing-4);
  width: 100%;
}
</style>
