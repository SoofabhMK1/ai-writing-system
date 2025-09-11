<template>
  <div class="tab-content">
    <div v-if="activeTab === '基本信息'">
      <EditableField label="姓名" v-model="editableCharacter.name" />
      <EditableField label="性别" v-model="editableCharacter.gender" />
      <EditableField label="年龄" v-model.number="editableCharacter.age" type="number" />
      <EditableField label="职业" v-model="editableCharacter.occupation" />
      <EditableField label="简介" v-model="editableCharacter.brief_introduction" type="textarea" />
    </div>
    <div v-if="activeTab === '外貌特征'">
      <EditableJson v-model="editableCharacter.physical_attributes" />
    </div>
    <div v-if="activeTab === '性格与背景'">
      <h3 class="json-subtitle">性格特质</h3>
      <EditableJson v-model="editableCharacter.personality_traits" />
      <h3 class="json-subtitle">背景故事</h3>
      <EditableJson v-model="editableCharacter.background_story" />
    </div>
    <div v-if="activeTab === '其他'">
      <EditableJson v-model="editableCharacter.custom_fields" />
    </div>
  </div>
</template>

<script setup>
import EditableField from './EditableField.vue';
import EditableJson from './EditableJson.vue';

defineProps({
  editableCharacter: {
    type: Object,
    required: true,
  },
  activeTab: {
    type: String,
    required: true,
  },
});
</script>

<style scoped>
.tab-content { padding: 30px; overflow-y: auto; flex-grow: 1; }
.json-subtitle { font-size: 1.2rem; font-weight: 600; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
</style>
