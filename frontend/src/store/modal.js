import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useModalStore = defineStore('modal', () => {
  // State for the original ConfirmationModal
  const isOpen = ref(false)
  const title = ref('')
  const message = ref('')
  let resolvePromise = null
  let rejectPromise = null

  // State for the new PreviewSendModal
  const isPreviewOpen = ref(false)
  const previewContent = ref('')
  let previewResolve = null
  let previewReject = null

  // --- Generic Modal State ---
  const activeModals = ref(0)
  const isAnyModalOpen = computed(() => activeModals.value > 0)

  const setActive = (isActive) => {
    if (isActive) {
      activeModals.value++
    } else {
      activeModals.value--
    }
  }

  // --- Methods for ConfirmationModal ---

  const show = (newTitle, newMessage) => {
    title.value = newTitle
    message.value = newMessage
    isOpen.value = true
    setActive(true)

    return new Promise((resolve, reject) => {
      resolvePromise = resolve
      rejectPromise = reject
    })
  }

  const confirm = () => {
    if (resolvePromise) {
      resolvePromise(true)
    }
    isOpen.value = false
    setActive(false)
    resetConfirmationState()
  }

  const cancel = () => {
    if (rejectPromise) {
      const error = new Error('Operation canceled by user.')
      error.isCanceled = true
      rejectPromise(error)
    }
    isOpen.value = false
    setActive(false)
    resetConfirmationState()
  }

  function resetConfirmationState() {
    resolvePromise = null
    rejectPromise = null
  }

  // --- Methods for PreviewSendModal ---

  const showPreview = (content) => {
    previewContent.value = content
    isPreviewOpen.value = true
    setActive(true)

    return new Promise((resolve, reject) => {
      previewResolve = resolve
      previewReject = reject
    })
  }

  const confirmPreview = () => {
    if (previewResolve) {
      previewResolve(true)
    }
    isPreviewOpen.value = false
    setActive(false)
    resetPreviewState()
  }

  const cancelPreview = () => {
    if (previewReject) {
      const error = new Error('Sending canceled by user.')
      error.isCanceled = true
      previewReject(error)
    }
    isPreviewOpen.value = false
    setActive(false)
    resetPreviewState()
  }

  function resetPreviewState() {
    previewContent.value = ''
    previewResolve = null
    previewReject = null
  }

  return {
    // For ConfirmationModal
    isOpen,
    title,
    message,
    show,
    confirm,
    cancel,

    // For PreviewSendModal
    isPreviewOpen,
    previewContent,
    showPreview,
    confirmPreview,
    cancelPreview,

    // For Generic Modal State
    isAnyModalOpen,
    setActive,
  }
})
