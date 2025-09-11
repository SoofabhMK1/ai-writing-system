<template>
  <div class="tab-content">
    <div v-if="activeTab === '基本信息'">
      <EditableField label="姓名" :modelValue="editableCharacter.name" @update:modelValue="updateField('name', $event)" />
      <EditableField label="性别" :modelValue="editableCharacter.gender" @update:modelValue="updateField('gender', $event)" />
      <EditableField
        label="年龄"
        :modelValue="editableCharacter.age"
        @update:modelValue="updateField('age', $event)"
        type="number"
      />
      <EditableField label="职业" :modelValue="editableCharacter.occupation" @update:modelValue="updateField('occupation', $event)" />
      <EditableField
        label="简介"
        :modelValue="editableCharacter.brief_introduction"
        @update:modelValue="updateField('brief_introduction', $event)"
        type="textarea"
      />
    </div>
    <div v-if="activeTab === '外貌特征'">
      <EditableJson :modelValue="editableCharacter.physical_attributes" @update:modelValue="updateField('physical_attributes', $event)" />
    </div>
    <div v-if="activeTab === '性格与背景'">
      <h3 class="json-subtitle">性格特质</h3>
      <EditableJson :modelValue="editableCharacter.personality_traits" @update:modelValue="updateField('personality_traits', $event)" />
      <h3 class="json-subtitle">背景故事</h3>
      <EditableJson :modelValue="editableCharacter.background_story" @update:modelValue="updateField('background_story', $event)" />
    </div>
    <div v-if="activeTab === '其他'">
      <EditableJson :modelValue="editableCharacter.custom_fields" @update:modelValue="updateField('custom_fields', $event)" />
    </div>
  </div>
</template>

<script setup>
import EditableField from './EditableField.vue'
import EditableJson from './EditableJson.vue'

const props = defineProps({
  editableCharacter: {
    type: Object,
    required: true,
  },
  activeTab: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['update:editableCharacter'])

const updateField = (field, value) => {
  const updatedCharacter = { ...props.editableCharacter, [field]: value }
  emit('update:editableCharacter', updatedCharacter)
}
</script>

<style scoped>
.tab-content {
  padding: var(--spacing-8);
  overflow-y: auto;
  flex-grow: 1;
}
.json-subtitle {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text);
  margin-top: var(--spacing-8);
  margin-bottom: var(--spacing-4);
  padding-bottom: var(--spacing-2);
  border-bottom: var(--border-width) solid var(--color-border);
}
</style>
