<template>
  <div class="modal-overlay">
    <div class="modal-content" v-if="character">
      <div class="modal-header">
        <h2 class="modal-title">{{ character.name }}</h2>
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
        <div v-if="activeTab === '基本信息'">
          <DetailItem label="姓名" :value="character.name" />
          <DetailItem label="性别" :value="character.gender" />
          <DetailItem label="年龄" :value="character.age" />
          <DetailItem label="职业" :value="character.occupation" />
          <DetailItem label="简介" :value="character.brief_introduction" type="textarea" />
        </div>
        <div v-if="activeTab === '外貌特征'">
          <JsonViewer :data="character.physical_attributes" />
        </div>
        <div v-if="activeTab === '性格与背景'">
          <h3 class="json-subtitle">性格特质</h3>
          <JsonViewer :data="character.personality_traits" />
          <h3 class="json-subtitle">背景故事</h3>
          <JsonViewer :data="character.background_story" />
        </div>
        <div v-if="activeTab === '其他'">
          <JsonViewer :data="character.custom_fields" />
        </div>
      </div>

      <div class="modal-actions">
        <button @click="handleDelete" class="delete-button">删除</button>
        <button class="update-button" disabled title="更新功能将在未来版本中提供">更新</button>
      </div>
    </div>
    <div v-else class="loading">Loading...</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCharacterStore } from '@/store/character';
import { useModalStore } from '@/store/modal';
import DetailItem from './DetailItem.vue';
import JsonViewer from './JsonViewer.vue';

const props = defineProps({
  characterId: {
    type: Number,
    required: true,
  },
});
const emit = defineEmits(['close']);

const characterStore = useCharacterStore();
const modalStore = useModalStore();

const character = computed(() => characterStore.selectedCharacter);
const activeTab = ref('基本信息');
const tabs = ['基本信息', '外貌特征', '性格与背景', '其他'];

onMounted(() => {
  characterStore.fetchCharacter(props.characterId);
});

const handleDelete = async () => {
  try {
    await modalStore.show(
      '确认删除',
      `你确定要删除角色“${character.value.name}”吗？此操作不可撤销。`
    );
    // If the promise resolves, it means user confirmed.
    await characterStore.deleteCharacter(props.characterId);
    emit('close');
  } catch (error) {
    // If the promise rejects, it means user canceled.
    if (!error.isCanceled) {
      console.error('An error occurred during deletion:', error);
    }
  }
};
</script>

<style scoped>
/* Basic Modal Styles */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: #fff; border-radius: 12px; width: 90%; max-width: 800px; height: 100vh; max-height: 700px; display: flex; flex-direction: column; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 30px; border-bottom: 1px solid #eee; }
.modal-title { font-size: 1.8rem; font-weight: 600; margin: 0; }
.close-button { background: none; border: none; font-size: 2rem; cursor: pointer; color: #888; }
.loading { color: white; font-size: 1.5rem; }

/* Tabs */
.tabs { display: flex; padding: 0 30px; border-bottom: 1px solid #eee; }
.tab-button { padding: 15px 20px; border: none; background: none; cursor: pointer; font-size: 1rem; color: #555; position: relative; }
.tab-button.active { color: #4a90e2; font-weight: 600; }
.tab-button.active::after { content: ''; position: absolute; bottom: -1px; left: 0; right: 0; height: 3px; background: #4a90e2; }

/* Content */
.tab-content { padding: 30px; overflow-y: auto; flex-grow: 1; }
.detail-item { margin-bottom: 15px; }
.detail-label { font-weight: 600; color: #333; margin-right: 10px; }
.detail-value { color: #555; }
.detail-value-long { background: #f9f9f9; border-radius: 6px; padding: 10px; margin-top: 5px; white-space: pre-wrap; }
.json-subtitle { font-size: 1.2rem; font-weight: 600; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
.json-viewer { background: #f4f4f4; border-radius: 6px; padding: 15px; white-space: pre-wrap; font-family: 'Courier New', Courier, monospace; font-size: 0.9rem; }

/* Actions */
.modal-actions { display: flex; justify-content: flex-end; gap: 15px; padding: 20px 30px; border-top: 1px solid #eee; }
.delete-button, .update-button { padding: 10px 25px; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; font-weight: 500; }
.delete-button { background-color: #e53e3e; color: white; }
.update-button { background-color: #ccc; color: #666; cursor: not-allowed; }
</style>
