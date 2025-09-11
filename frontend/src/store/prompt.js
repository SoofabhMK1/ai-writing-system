// frontend/src/store/prompt.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePromptStore = defineStore('prompt', () => {
  const isOpen = ref(false)
  const title = ref('')
  const message = ref('')
  const defaultValue = ref('')

  let resolvePromise = null
  let rejectPromise = null

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

  return { isOpen, title, message, defaultValue, show, confirm, cancel }
})
