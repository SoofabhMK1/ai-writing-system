import { defineStore } from 'pinia';
import conversationService from '../services/conversationService';
import { ref } from 'vue';

export const useConversationStore = defineStore('conversation', () => {
  const currentConversationId = ref(null);
  const messages = ref([]);
  const historyList = ref([]);
  const isLoading = ref(false);
  const cachedInitialPrompt = ref('');
  const promptForInput = ref('');

  function setCachedInitialPrompt(prompt) {
    cachedInitialPrompt.value = prompt;
  }

  function fillInputWithCachedPrompt() {
    if (cachedInitialPrompt.value) {
      promptForInput.value = cachedInitialPrompt.value;
      cachedInitialPrompt.value = ''; // Clear after use
    }
  }

  async function sendMessage(prompt, aiModelId) {
    if (!prompt || isLoading.value) return;

    isLoading.value = true;
    messages.value.push({ role: 'user', content: prompt });

    const assistantMessage = { role: 'assistant', content: '' };
    messages.value.push(assistantMessage);

    try {
      const res = await fetch('/api/v1/ai/chat-stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ai_model_id: aiModelId,
          messages: messages.value.slice(0, -1).map(({ role, content }) => ({ role, content })),
        }),
      });

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep the last, possibly incomplete line

        for (const line of lines) {
          if (line.startsWith('data:')) {
            const dataStr = line.substring(5).trim();
            try {
              const data = JSON.parse(dataStr);
              if (data.chunk) {
                assistantMessage.content += data.chunk;
              }
            } catch (e) {
              console.error('Failed to parse SSE data:', dataStr, e);
            }
          }
        }
      }
    } catch (error) {
      console.error('Error during chat stream:', error);
      assistantMessage.content = 'An error occurred. Please try again.';
    } finally {
      isLoading.value = false;
    }
  }

  async function loadConversationHistory(projectId) {
    try {
      const response = await conversationService.getByProject(projectId);
      historyList.value = response.data;
    } catch (error) {
      console.error('Failed to load conversation history:', error);
    }
  }

  async function loadConversation(conversationId) {
    try {
      const response = await conversationService.get(conversationId);
      currentConversationId.value = response.data.id;
      messages.value = response.data.messages;
    } catch (error) {
      console.error('Failed to load conversation:', error);
    }
  }

  async function saveCurrentConversation(projectId) {
    if (!messages.value.length) return;

    const conversationData = {
      project_id: projectId,
      title: messages.value[0].content.substring(0, 50),
      messages: messages.value.map(({ role, content }) => ({ role, content })),
    };

    try {
      let response;
      if (currentConversationId.value) {
        response = await conversationService.update(currentConversationId.value, conversationData);
      } else {
        response = await conversationService.create(conversationData);
      }
      currentConversationId.value = response.data.id;
      await loadConversationHistory(projectId);
    } catch (error) {
      console.error('Failed to save conversation:', error);
    }
  }

  function startNewConversation() {
    currentConversationId.value = null;
    messages.value = [];
  }

  async function deleteConversation(conversationId, projectId) {
    try {
      await conversationService.delete(conversationId);
      historyList.value = historyList.value.filter(c => c.id !== conversationId);
      if (currentConversationId.value === conversationId) {
        startNewConversation();
      }
    } catch (error) {
      console.error('Failed to delete conversation:', error);
    }
  }

  return {
    currentConversationId,
    messages,
    historyList,
    isLoading,
    cachedInitialPrompt,
    promptForInput,
    setCachedInitialPrompt,
    fillInputWithCachedPrompt,
    sendMessage,
    loadConversationHistory,
    loadConversation,
    saveCurrentConversation,
    startNewConversation,
    deleteConversation,
  };
});
