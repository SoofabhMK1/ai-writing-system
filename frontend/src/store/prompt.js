// frontend/src/store/prompt.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { promptTemplateService } from '@/services/settingService'

export const usePromptStore = defineStore('prompt', () => {
  // State for the generic prompt modal
  const isOpen = ref(false)
  const title = ref('')
  const message = ref('')
  const defaultValue = ref('')

  let resolvePromise = null
  let rejectPromise = null

  // State for prompt templates
  const templates = ref([])
  const isLoading = ref(false)
  const categoryBlacklist = ['SYSTEM_PROMPT']; // Category blacklist

  const groupedTemplates = computed(() => {
    const filteredTemplates = templates.value.filter(t => t.category && !categoryBlacklist.includes(t.category));
    const grouped = filteredTemplates.reduce((acc, template) => {
      const category = template.category;
      if (!acc[category]) {
        acc[category] = [];
      }
      acc[category].push(template);
      return acc;
    }, {});
    console.log('Grouped Templates:', grouped);
    return grouped;
  })

  const fetchTemplates = async () => {
    if (templates.value.length > 0) return // Avoid re-fetching
    isLoading.value = true
    try {
      const response = await promptTemplateService.getAll()
      templates.value = response.data
    } catch (error) {
      console.error('Failed to fetch prompt templates:', error)
      // Optionally, use a notification store to show an error to the user
    } finally {
      isLoading.value = false
    }
  }

  const show = (newTitle, newMessage, initialValue = '') => {
    title.value = newTitle
    message.value = newMessage
    defaultValue.value = initialValue
    isOpen.value = true

    return new Promise((resolve, reject) => {
      resolvePromise = resolve
      rejectPromise = reject
    })
  }

  const confirm = (value) => {
    if (resolvePromise) {
      resolvePromise(value) // 解析 Promise，并返回输入值
    }
    isOpen.value = false
  }

  const cancel = () => {
    if (rejectPromise) {
      rejectPromise(new Error('Prompt was canceled by the user.')) // 拒绝 Promise
    }
    isOpen.value = false
  }

  return {
    // Generic prompt modal
    isOpen,
    title,
    message,
    defaultValue,
    show,
    confirm,
    cancel,

    // Prompt templates
    templates,
    groupedTemplates,
    isLoading,
    fetchTemplates,
  }
})
