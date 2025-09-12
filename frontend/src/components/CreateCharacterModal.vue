<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h2 class="modal-title">通过 JSON 创建角色</h2>
      <p class="modal-description">请在下方粘贴角色的 JSON 数据。</p>
      <textarea
        v-model="jsonInput"
        class="json-textarea form-control"
        placeholder='{
  "name": "角色姓名",
  "gender": "女性",
  "age": 28,
  "occupation": "侦探",
  "brief_introduction": "一位精明风趣的侦探。",
  "physical_attributes": {"身高": "170cm"},
  "body_details": {},
  "clothing_style_and_habits": {},
  "personality_traits": {"MBTI": "INTJ"},
  "background_story": {},
  "sexual_preferences_and_behaviors": {},
  "custom_fields": {}
}'
      ></textarea>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div class="modal-actions">
        <button @click="$emit('close')" class="btn">取消</button>
        <button @click="saveCharacter" class="btn btn-primary">保存</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCharacterStore } from '@/store/character'

const emit = defineEmits(['close'])
const characterStore = useCharacterStore()
const jsonInput = ref('')
const errorMessage = ref('')

const saveCharacter = async () => {
  try {
    const characterData = JSON.parse(jsonInput.value)
    errorMessage.value = ''
    await characterStore.createCharacter(characterData)
    emit('close')
  } catch (error) {
    errorMessage.value = 'Invalid JSON format. Please check your input.'
    console.error('JSON parsing error:', error)
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background: var(--color-surface);
  padding: var(--spacing-8);
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 600px;
  box-shadow: var(--shadow-lg);
  border: var(--border-width) solid var(--color-border);
}

.modal-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--spacing-2);
}

.modal-description {
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
  margin-bottom: var(--spacing-6);
}

.json-textarea {
  width: 100%;
  height: 300px;
  font-family: 'Courier New', Courier, monospace;
  font-size: var(--font-size-sm);
  resize: vertical;
}

.error-message {
  color: var(--color-danger);
  margin-top: var(--spacing-3);
  font-size: var(--font-size-sm);
}

.modal-actions {
  margin-top: var(--spacing-6);
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-4);
}
</style>
