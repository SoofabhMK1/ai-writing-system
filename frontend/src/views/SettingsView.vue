<!-- frontend/src/views/SettingsView.vue -->
<template>
  <div class="settings-container">
    <!-- Left Panel: Navigation -->
    <div class="settings-nav">
      <h2 class="nav-title">设定集</h2>
      <ul>
        <li
          @click="activeTab = 'worldview'"
          :class="{ active: activeTab === 'worldview' }"
        >
          世界观设定
        </li>
        <li
          @click="activeTab = 'style'"
          :class="{ active: activeTab === 'style' }"
        >
          文风设定
        </li>
        <li
          @click="activeTab = 'templates'"
          :class="{ active: activeTab === 'templates' }"
        >
          AI 提示词模板
        </li>
        <li
          @click="activeTab = 'aimodels'"
          :class="{ active: activeTab === 'aimodels' }"
        >
          AI 模型设定
        </li>
        <li
          @click="activeTab = 'presets'"
          :class="{ active: activeTab === 'presets' }"
        >
          对话预设
        </li>
      </ul>
    </div>

    <!-- Right Panel: Editor -->
    <div class="settings-content">
      <WorldviewSettings v-if="activeTab === 'worldview'" />
      <WritingStyleSettings v-if="activeTab === 'style'" />
      <PromptTemplates v-if="activeTab === 'templates'" />
      <AIModelSettings v-if="activeTab === 'aimodels'" />
      <PromptPresets v-if="activeTab === 'presets'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import WorldviewSettings from '../components/settings/WorldviewSettings.vue'
import WritingStyleSettings from '../components/settings/WritingStyleSettings.vue'
import PromptTemplates from '../components/settings/PromptTemplates.vue'
import AIModelSettings from '../components/settings/AIModelSettings.vue'
import PromptPresets from '../components/settings/PromptPresets.vue'

const activeTab = ref('worldview') // Default active tab
</script>

<style scoped>
.settings-container {
  display: flex;
  height: 100%;
  gap: var(--spacing-8);
}

.settings-nav {
  width: 280px;
  min-width: 240px;
  flex-shrink: 0;
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-6);
}

.nav-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 var(--spacing-6) 0;
  padding-bottom: var(--spacing-4);
  border-bottom: var(--border-width) solid var(--color-border);
}

.settings-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.settings-nav li {
  padding: var(--spacing-3) var(--spacing-4);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--color-text-muted);
  transition: var(--transition-base);
}

.settings-nav li:hover {
  background-color: var(--color-background);
  color: var(--color-text);
}

.settings-nav li.active {
  background-color: var(--color-primary);
  color: #ffffff;
  font-weight: 600;
}

.settings-content {
  flex-grow: 1;
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  border: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-8);
  overflow-y: auto;
}
</style>
