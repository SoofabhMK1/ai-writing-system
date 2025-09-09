<!-- frontend/src/views/SettingsView.vue -->
<template>
  <div class="settings-container">
    <!-- Left Panel: Navigation -->
    <div class="settings-nav">
      <h2 class="nav-title">设定集</h2>
      <ul>
        <li 
          @click="activeTab = 'worldview'" 
          :class="{ active: activeTab === 'worldview' }">
          世界观设定
        </li>
        <li 
          @click="activeTab = 'style'" 
          :class="{ active: activeTab === 'style' }">
          文风设定
        </li>
        <li 
          @click="activeTab = 'templates'" 
          :class="{ active: activeTab === 'templates' }">
          AI 提示词模板
        </li>
      </ul>
    </div>

    <!-- Right Panel: Editor -->
    <div class="settings-content">
      <WorldviewSettings v-if="activeTab === 'worldview'" />
      <WritingStyleSettings v-if="activeTab === 'style'" />
      <PromptTemplates v-if="activeTab === 'templates'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import WorldviewSettings from '../components/settings/WorldviewSettings.vue';
import WritingStyleSettings from '../components/settings/WritingStyleSettings.vue';
import PromptTemplates from '../components/settings/PromptTemplates.vue';

const activeTab = ref('worldview'); // Default active tab
</script>

<style scoped>
.settings-container {
  display: flex;
  height: calc(100vh - 60px); /* Adjust based on NavBar height */
  background-color: #f7f8fa;
  padding: 1rem;
  gap: 1rem;
}

.settings-nav {
  width: 280px;
  min-width: 240px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.nav-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 2rem 0;
  text-align: center;
}

.settings-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.settings-nav li {
  padding: 1rem 1.5rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  color: #555;
  transition: background-color 0.3s, color 0.3s;
}

.settings-nav li:hover {
  background-color: #f0f5ff;
}

.settings-nav li.active {
  background-color: #4a90e2;
  color: white;
  font-weight: 600;
}

.settings-content {
  flex-grow: 1;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 2rem;
  overflow-y: auto;
}

.setting-card {
  max-width: 800px;
}

.setting-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
}

.setting-card p {
  font-size: 1rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.setting-item-placeholder {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.setting-item-placeholder span {
  font-weight: 500;
}

.setting-item-placeholder button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  background-color: #4a90e2;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.setting-item-placeholder button:hover {
  background-color: #357abd;
}
</style>
