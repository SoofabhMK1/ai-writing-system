<!-- frontend/src/components/AIGenerationModal.vue -->
<template>
  <div v-if="show" class="modal-overlay" @click.self="handleClose">
    <div class="modal-card">
      <h3>{{ title }}</h3>
      
      <div class="modal-body">
        <!-- Prompt Editor -->
        <div class="prompt-section">
          <label for="prompt-editor">Prompt</label>
          <textarea 
            id="prompt-editor"
            v-model="editablePrompt" 
            :disabled="isGenerating"
            rows="10"
          ></textarea>
        </div>

        <!-- Streaming Result -->
        <div class="result-section">
          <label>生成结果</label>
          <div class="streaming-output" ref="outputArea">
            <pre>{{ streamingResult }}</pre>
            <div v-if="isGenerating" class="blinking-cursor"></div>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button type="button" class="btn-cancel" @click="handleClose" :disabled="isGenerating">
          {{ isGenerating ? '正在生成...' : '取消' }}
        </button>
        <button v-if="!isGenerating && !generationCompleted" type="button" class="btn-confirm" @click="startGeneration">
          确认并生成
        </button>
        <button v-if="generationCompleted" type="button" class="btn-save" @click="handleSave">
          保存
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';

const props = defineProps({
  show: { type: Boolean, required: true },
  title: { type: String, default: 'AI 生成' },
  initialPrompt: { type: String, default: '' },
});

const emit = defineEmits(['close', 'save', 'start-generation']);

const editablePrompt = ref('');
const streamingResult = ref('');
const isGenerating = ref(false);
const generationCompleted = ref(false);
const outputArea = ref(null);

watch(() => props.show, (newVal) => {
  if (newVal) {
    editablePrompt.value = props.initialPrompt;
    streamingResult.value = '';
    isGenerating.value = false;
    generationCompleted.value = false;
  }
});

// Public method to append data to the stream
const appendStream = (chunk) => {
  if (!isGenerating.value) isGenerating.value = true;
  streamingResult.value += chunk;
  nextTick(() => {
    if (outputArea.value) {
      outputArea.value.scrollTop = outputArea.value.scrollHeight;
    }
  });
};

// Public method to signal completion
const completeStream = () => {
  isGenerating.value = false;
  generationCompleted.value = true;
};

const startGeneration = () => {
  isGenerating.value = true;
  generationCompleted.value = false;
  streamingResult.value = '';
  emit('start-generation', editablePrompt.value);
};

const handleClose = () => {
  if (isGenerating.value) return;
  emit('close');
};

const handleSave = () => {
  emit('save', streamingResult.value);
};

// Expose public methods
defineExpose({
  appendStream,
  completeStream,
});
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background-color: rgba(0, 0, 0, 0.6); display: flex;
  justify-content: center; align-items: center; z-index: 1000;
}
.modal-card {
  background-color: #fff; padding: 2rem; border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.15); width: 90%;
  max-width: 800px; max-height: 90vh; display: flex; flex-direction: column;
}
.modal-card h3 {
  margin: 0 0 1.5rem; font-size: 1.5rem; font-weight: 500; text-align: center;
}
.modal-body { display: flex; flex-direction: column; gap: 1.5rem; overflow-y: auto; }
.prompt-section, .result-section { display: flex; flex-direction: column; }
label { margin-bottom: 0.5rem; font-weight: 500; color: #333; }
textarea {
  width: 100%; padding: 0.8rem 1rem; border: 1px solid #e0e0e0;
  border-radius: 8px; font-size: 0.9rem; resize: vertical;
  font-family: 'Courier New', Courier, monospace;
}
.streaming-output {
  background-color: #f7f8fa; border-radius: 8px; padding: 1rem;
  min-height: 150px; overflow-y: auto; position: relative;
}
.streaming-output pre { white-space: pre-wrap; word-wrap: break-word; font-family: 'Courier New', Courier, monospace; font-size: 0.9rem; margin: 0; }
.blinking-cursor {
  display: inline-block; width: 8px; height: 1rem; background-color: #333;
  animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }
.form-actions {
  display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem;
  padding-top: 1.5rem; border-top: 1px solid #e0e0e0;
}
.btn-confirm, .btn-save, .btn-cancel {
  padding: 0.8rem 1.5rem; border: none; border-radius: 8px; cursor: pointer;
  font-size: 1rem; font-weight: 500; transition: all 0.3s;
}
.btn-confirm { background-color: #28a745; color: white; }
.btn-confirm:hover { background-color: #218838; }
.btn-save { background-color: #4a90e2; color: white; }
.btn-save:hover { background-color: #357abd; }
.btn-cancel { background-color: #f0f0f0; color: #333; }
.btn-cancel:hover { background-color: #e0e0e0; }
.btn-cancel:disabled { background-color: #e9ecef; cursor: not-allowed; }
</style>
