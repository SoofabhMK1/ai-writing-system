<template>
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
</template>

<script setup>
import DetailItem from './DetailItem.vue';
import JsonViewer from './JsonViewer.vue';

defineProps({
  character: {
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
