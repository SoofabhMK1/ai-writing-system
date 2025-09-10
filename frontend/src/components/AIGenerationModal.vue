<!-- frontend/src/components/AIGenerationModal.vue -->
<template>
  <div v-if="show" class="modal-overlay" @click.self="handleClose">
    <div class="modal-card">
      <h3>{{ title }}</h3>
      
      <div class="modal-body">
        <div class="tab-navigation">
          <button @click="activeTab = 'result'" :class="{ active: activeTab === 'result' }">生成结果</button>
          <button @click="activeTab = 'reasoning'" :class="{ active: activeTab === 'reasoning' }" v-if="reasoningResult || isGenerating">AI 思维链</button>
          <button @click="activeTab = 'prompt'" :class="{ active: activeTab === 'prompt' }">Prompt</button>
        </div>

        <div class="tab-content">
          <!-- Prompt Editor -->
          <div v-if="activeTab === 'prompt'" class="prompt-section">
            <textarea 
              id="prompt-editor"
              v-model="editablePrompt" 
              :disabled="isGenerating"
              rows="15"
            ></textarea>
          </div>

          <!-- Reasoning Result -->
          <div v-if="activeTab === 'reasoning'" class="result-section">
            <div class="streaming-output reasoning-output">
              <pre>{{ reasoningResult }}</pre>
              <div v-if="isGenerating && !finalOutlineResult" class="blinking-cursor"></div>
            </div>
          </div>

          <!-- Streaming Result -->
          <div v-if="activeTab === 'result'" class="result-section">
            <div class="streaming-output" ref="outputArea">
              <pre>{{ finalOutlineResult }}</pre>
              <div v-if="isGenerating && !reasoningResult" class="blinking-cursor"></div>
            </div>
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
import { ref, watch } from 'vue';
import { useNotificationStore } from '@/store/notification';

const props = defineProps({
  show: { type: Boolean, required: true },
  title: { type: String, default: 'AI 生成' },
  initialPrompt: { type: String, default: '' },
  generationParams: { type: Object, required: true }
});

const emit = defineEmits(['close', 'save']);
const notificationStore = useNotificationStore();

const editablePrompt = ref('');
const reasoningResult = ref('');
const finalOutlineResult = ref('');
const isGenerating = ref(false);
const generationCompleted = ref(false);
const activeTab = ref('result');

watch(() => props.show, (newVal) => {
  if (newVal) {
    editablePrompt.value = props.initialPrompt;
    reasoningResult.value = '';
    finalOutlineResult.value = '';
    isGenerating.value = false;
    generationCompleted.value = false;
    activeTab.value = 'result'; // Reset to result tab on open
  }
});

const startGeneration = async () => {
  isGenerating.value = true;
  generationCompleted.value = false;
  reasoningResult.value = '';
  finalOutlineResult.value = '';
  activeTab.value = 'result'; // Switch to result tab on generation start

  const body = {
    ...props.generationParams,
    prompt: editablePrompt.value,
  };

  try {
    const response = await fetch('/api/v1/ai/generate-outline-stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split('\n\n');
      buffer = events.pop(); // Keep the last, possibly incomplete event for the next chunk

      for (const eventString of events) {
        if (!eventString) continue;
        
        let eventType = 'message';
        let eventData = '';

        for (const line of eventString.split('\n')) {
          if (line.startsWith('event:')) {
            eventType = line.substring(6).trim();
          } else if (line.startsWith('data:')) {
            eventData = line.substring(5).trim();
          }
        }

        if (eventData) {
          try {
            const data = JSON.parse(eventData);
            if (eventType === 'reasoning') {
              reasoningResult.value += data.chunk;
            } else if (eventType === 'content') {
              finalOutlineResult.value += data.chunk;
            } else if (eventType === 'error') {
              notificationStore.show(`AI Error: ${data.error}`, 'error');
            }
          } catch (e) {
            console.error('Failed to parse SSE data chunk:', eventData, e);
          }
        }
      }
    }
  } catch (error) {
    console.error('Streaming failed:', error);
    notificationStore.show('生成失败，请检查网络或联系管理员。', 'error');
  } finally {
    isGenerating.value = false;
    generationCompleted.value = true;
  }
};

const handleClose = () => {
  // In a real-world app with AbortController, you would abort the fetch here.
  emit('close');
};

const handleSave = () => {
  try {
    // Ensure the content is valid JSON before saving
    JSON.parse(finalOutlineResult.value);
    emit('save', finalOutlineResult.value);
  } catch (error) {
    console.error("Save failed: content is not valid JSON.", error);
    notificationStore.show("保存失败：生成的内容不是有效的JSON格式。", 'error');
  }
};
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
.modal-body { display: flex; flex-direction: column; overflow-y: auto; padding-top: 1rem; }

.tab-navigation {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 1.5rem;
  flex-shrink: 0;
}
.tab-navigation button {
  padding: 0.8rem 1.2rem;
  border: none;
  background-color: transparent;
  cursor: pointer;
  font-size: 1rem;
  color: #666;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}
.tab-navigation button.active {
  color: #4a90e2;
  border-bottom-color: #4a90e2;
  font-weight: 500;
}
.tab-navigation button:hover {
  background-color: #f7f8fa;
}

.tab-content {
  flex-grow: 1;
  min-height: 0;
}

.prompt-section, .result-section { 
  display: flex; 
  flex-direction: column; 
  height: 100%;
}

textarea {
  width: 100%;
  flex-grow: 1;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  font-size: 0.9rem;
  resize: none;
  font-family: 'Courier New', Courier, monospace;
}

.streaming-output {
  background-color: #f7f8fa;
  border-radius: 8px;
  padding: 1rem;
  flex-grow: 1;
  overflow-y: auto;
  position: relative;
  min-height: 250px;
}
.reasoning-output {
  background-color: #e9ecef;
  color: #495057;
  border: 1px solid #dee2e6;
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
