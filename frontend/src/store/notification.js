// frontend/src/store/notification.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNotificationStore = defineStore('notification', () => {
  const items = ref([])
  let nextId = 0

  const show = (message, type = 'info', duration = 3000) => {
    const id = nextId++
    items.value.push({ id, message, type })

    setTimeout(() => {
      remove(id)
    }, duration)
  }

  const remove = (id) => {
    items.value = items.value.filter((item) => item.id !== id)
  }

  return { items, show, remove }
})
