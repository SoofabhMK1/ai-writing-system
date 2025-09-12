import { defineStore } from 'pinia'
import conversationService from '../services/conversationService'
import { ref } from 'vue'
import { useModalStore } from './modal'
import { prepareMessagesForApi } from '../utils/messageBuilder.js'
import { handleStreamedChat } from '../services/aiStreamService.js'

export const useConversationStore = defineStore('conversation', () => {
  const currentConversationId = ref(null)
  const messages = ref([])
  const historyList = ref([])
  const isLoading = ref(false)
  const cachedInitialPrompt = ref('')
  const promptForInput = ref('')
  const previewBeforeSending = ref(false)
  const selectedAiModel = ref(null)
  const selectedPresetId = ref(null)

  const modal = useModalStore()

  function setCachedInitialPrompt(prompt) {
    cachedInitialPrompt.value = prompt
  }

  function fillInputWithCachedPrompt() {
    if (cachedInitialPrompt.value) {
      promptForInput.value = cachedInitialPrompt.value
      cachedInitialPrompt.value = '' // Clear after use
    }
  }

  async function _performStreamedChat(aiModelId) {
    isLoading.value = true
    const assistantMessage = { role: 'assistant', thinking: '', content: '' }
    messages.value.push(assistantMessage)

    const messagesForApi = prepareMessagesForApi(
      messages.value.slice(0, -1)
    )

    const callbacks = {
      onReasoning: (chunk) => {
        assistantMessage.thinking += chunk
      },
      onContent: (chunk) => {
        assistantMessage.content += chunk
      },
      onError: (error) => {
        console.error('Stream error:', error)
        assistantMessage.content += `\n\nError: ${error}`
      },
    }

    try {
      await handleStreamedChat(aiModelId, messagesForApi, callbacks)
    } catch (error) {
      console.error('Error setting up chat stream:', error)
      assistantMessage.content =
        'An error occurred while setting up the connection.'
    } finally {
      isLoading.value = false
    }
  }

  async function sendMessage(prompt, aiModelId) {
    if (!prompt || isLoading.value) return false

    const userMessage = { role: 'user', content: prompt }

    if (previewBeforeSending.value) {
      try {
        const messagesForPreview = prepareMessagesForApi(
          [...messages.value, userMessage]
        )
        // Construct the full content to be sent
        const fullContent = messagesForPreview
          .map((m) => `## ${m.role}\n\n${m.content}`)
          .join('\n\n---\n\n')

        await modal.showPreview(fullContent)

        // If user confirms, proceed
        messages.value.push(userMessage)
        await _performStreamedChat(aiModelId)
        return true // Message sent after preview
      } catch (error) {
        if (error.isCanceled) {
          // User canceled the preview
          return false // Message not sent
        }
        // Handle other potential errors from modal
        console.error('Error during preview modal:', error)
        return false
      }
    } else {
      // No preview needed, send directly
      messages.value.push(userMessage)
      await _performStreamedChat(aiModelId)
      return true // Message sent directly
    }
  }

  async function loadConversationHistory() {
    try {
      const response = await conversationService.getAll()
      historyList.value = response.data
    } catch (error) {
      console.error('Failed to load conversation history:', error)
    }
  }

  async function loadConversation(conversationId) {
    try {
      const response = await conversationService.get(conversationId)
      currentConversationId.value = response.data.id
      messages.value = response.data.messages
    } catch (error) {
      console.error('Failed to load conversation:', error)
    }
  }

    async function saveCurrentConversation() {
    if (!messages.value.length) return

    const conversationData = {
      title: messages.value[0].content.substring(0, 50),
      messages: messages.value.map(({ role, content, thinking }) => ({ role, content, thinking })),
    }

    try {
      let response
      if (currentConversationId.value) {
        response = await conversationService.update(
          currentConversationId.value,
          conversationData,
        )
      } else {
        response = await conversationService.create(conversationData)
      }
      currentConversationId.value = response.data.id
      await loadConversationHistory()
    } catch (error) {
      console.error('Failed to save conversation:', error)
    }
  }


  function startNewConversation() {
    currentConversationId.value = null
    messages.value = []
    selectedPresetId.value = null
  }

  async function deleteConversation(conversationId) {
    try {
      await conversationService.delete(conversationId)
      historyList.value = historyList.value.filter(
        (c) => c.id !== conversationId,
      )
      if (currentConversationId.value === conversationId) {
        startNewConversation()
      }
    } catch (error) {
      console.error('Failed to delete conversation:', error)
    }
  }

  return {
    currentConversationId,
    messages,
    historyList,
    isLoading,
    cachedInitialPrompt,
    promptForInput,
    previewBeforeSending,
    selectedAiModel,
    selectedPresetId,
    setCachedInitialPrompt,
    fillInputWithCachedPrompt,
    sendMessage,
    loadConversationHistory,
    loadConversation,
    saveCurrentConversation,
    startNewConversation,
    deleteConversation,
  }
})
