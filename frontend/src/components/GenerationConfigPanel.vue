<!-- frontend/src/components/GenerationConfigPanel.vue -->
<template>
  <div class="left-panel card">
    <h3 class="panel-title">生成配置</h3>
    <div class="config-scroll-area">
      <div class="form-group-inline">
        <label for="worldview">世界观</label>
        <select id="worldview" :value="modelValue.worldview_id" @change="$emit('update:modelValue', { ...modelValue, worldview_id: $event.target.value })">
          <option :value="null">-- 选择 --</option>
          <option v-for="w in worldviews" :key="w.id" :value="w.id">{{ w.name }}</option>
        </select>
      </div>
      <div class="form-group-inline">
        <label for="writingStyle">文风</label>
        <select id="writingStyle" :value="modelValue.writing_style_id" @change="$emit('update:modelValue', { ...modelValue, writing_style_id: $event.target.value })">
          <option :value="null">-- 选择 --</option>
          <option v-for="s in writingStyles" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
      </div>
      <div class="form-group-inline">
        <label for="aiModel">AI 模型</label>
        <select id="aiModel" :value="modelValue.ai_model_id" @change="$emit('update:modelValue', { ...modelValue, ai_model_id: $event.target.value })">
          <option :value="null">-- 选择 --</option>
          <option v-for="m in aiModels" :key="m.id" :value="m.id">{{ m.name }}</option>
        </select>
      </div>
      <div class="form-group-inline">
        <label for="wordCount">目标总字数</label>
        <input id="wordCount" type="number" :value="modelValue.target_word_count" @input="$emit('update:modelValue', { ...modelValue, target_word_count: $event.target.value })" placeholder="例如：100000" />
      </div>
    </div>
    <button @click="$emit('generate')" class="btn-generate" :disabled="isGenerating">
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
.card { background-color: #ffffff; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }
.left-panel {
  width: 400px;
  min-width: 350px;
  display: flex;
  flex-direction: column;
}
.config-scroll-area {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 10px;
  margin-right: -10px;
}
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
</style>
