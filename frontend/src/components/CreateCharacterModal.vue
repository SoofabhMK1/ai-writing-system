<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2 class="modal-title">Create Character via JSON</h2>
      <p class="modal-description">
        Paste your character data in JSON format below.
      </p>
      <textarea
        v-model="jsonInput"
        class="json-textarea"
        placeholder='{
  "name": "Character Name",
  "gender": "Female",
  "age": 28,
  "occupation": "Detective",
  "brief_introduction": "A sharp and witty detective.",
  "physical_attributes": {"height": "170cm"},
  "personality_traits": {"mbti": "INTJ"},
  "background_story": {},
  "custom_fields": {}
}'
      ></textarea>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div class="modal-actions">
        <button @click="$emit('close')" class="cancel-button">Cancel</button>
        <button @click="saveCharacter" class="save-button">Save</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCharacterStore } from '@/store/character';

const emit = defineEmits(['close']);
const characterStore = useCharacterStore();
const jsonInput = ref('');
const errorMessage = ref('');

const saveCharacter = async () => {
  try {
    const characterData = JSON.parse(jsonInput.value);
    errorMessage.value = '';
    await characterStore.createCharacter(characterData);
    emit('close');
  } catch (error) {
    errorMessage.value = 'Invalid JSON format. Please check your input.';
    console.error('JSON parsing error:', error);
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.modal-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.modal-description {
  font-size: 1rem;
  color: #666;
  margin-bottom: 20px;
}

.json-textarea {
  width: 100%;
  height: 300px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9rem;
  resize: vertical;
  box-sizing: border-box; /* Add this line */
}

.error-message {
  color: #e53e3e;
  margin-top: 10px;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.cancel-button, .save-button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
}

.cancel-button {
  background-color: #e2e8f0;
  color: #2d3748;
}

.save-button {
  background-color: #4a90e2;
  color: white;
}
</style>
