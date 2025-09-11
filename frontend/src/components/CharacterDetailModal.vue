<template>
  <div class="modal-overlay">
    <div class="modal-content" v-if="character">
      <div class="modal-header">
        <h2 class="modal-title">{{ isEditing ? 'Edit Character' : character.name }}</h2>
        <button @click="$emit('close')" class="close-button">&times;</button>
      </div>
      
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab"
          :class="['tab-button', { active: activeTab === tab }]"
          @click="activeTab = tab"
        >
          {{ tab }}
        </button>
      </div>

      <div class="tab-content">
        <!-- Basic Info Tab -->
        <div v-if="activeTab === '基本信息'">
          <template v-if="!isEditing">
            <DetailItem label="姓名" :value="character.name" />
            <DetailItem label="性别" :value="character.gender" />
            <DetailItem label="年龄" :value="character.age" />
            <DetailItem label="职业" :value="character.occupation" />
            <DetailItem label="简介" :value="character.brief_introduction" type="textarea" />
          </template>
          <template v-else>
            <EditableField label="姓名" v-model="editableCharacter.name" />
            <EditableField label="性别" v-model="editableCharacter.gender" />
            <EditableField label="年龄" v-model.number="editableCharacter.age" type="number" />
            <EditableField label="职业" v-model="editableCharacter.occupation" />
            <EditableField label="简介" v-model="editableCharacter.brief_introduction" type="textarea" />
          </template>
        </div>
        <!-- Other Tabs -->
        <div v-if="activeTab === '外貌特征'">
          <JsonViewer v-if="!isEditing" :data="character.physical_attributes" />
          <EditableJson v-else v-model="editableCharacter.physical_attributes" />
        </div>
        <div v-if="activeTab === '性格与背景'">
          <h3 class="json-subtitle">性格特质</h3>
          <JsonViewer v-if="!isEditing" :data="character.personality_traits" />
          <EditableJson v-else v-model="editableCharacter.personality_traits" />
          <h3 class="json-subtitle">背景故事</h3>
          <JsonViewer v-if="!isEditing" :data="character.background_story" />
          <EditableJson v-else v-model="editableCharacter.background_story" />
        </div>
        <div v-if="activeTab === '其他'">
          <JsonViewer v-if="!isEditing" :data="character.custom_fields" />
          <EditableJson v-else v-model="editableCharacter.custom_fields" />
        </div>
      </div>

      <div class="modal-actions">
        <template v-if="!isEditing">
          <button @click="handleDelete" class="delete-button">删除</button>
          <button @click="enterEditMode" class="update-button-active">更新</button>
        </template>
        <template v-else>
          <button @click="cancelEdit" class="cancel-button">取消</button>
          <button @click="saveChanges" class="save-button">保存</button>
        </template>
      </div>
    </div>
    <div v-else class="loading">Loading...</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useCharacterStore } from '@/store/character';
import { useModalStore } from '@/store/modal';
import DetailItem from './DetailItem.vue';
import JsonViewer from './JsonViewer.vue';
import EditableJson from './EditableJson.vue';
import EditableField from './EditableField.vue';

const props = defineProps({ characterId: { type: Number, required: true } });
const emit = defineEmits(['close']);

const characterStore = useCharacterStore();
const modalStore = useModalStore();

const character = computed(() => characterStore.selectedCharacter);
const isEditing = ref(false);
const editableCharacter = ref(null);
const activeTab = ref('基本信息');
const tabs = ['基本信息', '外貌特征', '性格与背景', '其他'];

onMounted(() => {
  characterStore.fetchCharacter(props.characterId);
});

watch(character, (newChar) => {
  if (newChar) {
    editableCharacter.value = JSON.parse(JSON.stringify(newChar));
  }
}, { deep: true });

const enterEditMode = () => {
  isEditing.value = true;
};

const cancelEdit = () => {
  editableCharacter.value = JSON.parse(JSON.stringify(character.value));
  isEditing.value = false;
};

const saveChanges = async () => {
  await characterStore.updateCharacter({
    id: props.characterId,
    data: editableCharacter.value,
  });
  isEditing.value = false;
};

const handleDelete = async () => {
  try {
    await modalStore.show('确认删除', `你确定要删除角色“${character.value.name}”吗？此操作不可撤销。`);
    await characterStore.deleteCharacter(props.characterId);
    emit('close');
  } catch (error) {
    if (!error.isCanceled) console.error('Deletion error:', error);
  }
};
</script>

<style scoped>
/* Using existing styles and adding new ones */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: #fff; border-radius: 12px; width: 90%; max-width: 800px; height: 80vh; max-height: 700px; display: flex; flex-direction: column; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 30px; border-bottom: 1px solid #eee; }
.modal-title { font-size: 1.8rem; font-weight: 600; margin: 0; }
.close-button { background: none; border: none; font-size: 2rem; cursor: pointer; color: #888; }
.loading { color: white; font-size: 1.5rem; }
.tabs { display: flex; padding: 0 30px; border-bottom: 1px solid #eee; }
.tab-button { padding: 15px 20px; border: none; background: none; cursor: pointer; font-size: 1rem; color: #555; position: relative; }
.tab-button.active { color: #4a90e2; font-weight: 600; }
.tab-button.active::after { content: ''; position: absolute; bottom: -1px; left: 0; right: 0; height: 3px; background: #4a90e2; }
.tab-content { padding: 30px; overflow-y: auto; flex-grow: 1; }
.json-subtitle { font-size: 1.2rem; font-weight: 600; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 15px; padding: 20px 30px; border-top: 1px solid #eee; }
.delete-button, .update-button-active, .cancel-button, .save-button { padding: 10px 25px; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; font-weight: 500; }
.delete-button { background-color: #e53e3e; color: white; }
.update-button-active { background-color: #4a90e2; color: white; }
.cancel-button { background-color: #f0f0f0; }
.save-button { background-color: #28a745; color: white; }

/* EditableField styles */
.editable-field { margin-bottom: 15px; }
.editable-field label { display: block; margin-bottom: 5px; font-weight: 600; }
.editable-field input, .editable-field textarea { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
.editable-field textarea { min-height: 80px; resize: vertical; }
</style>
