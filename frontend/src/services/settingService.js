// frontend/src/services/settingService.js
import api from './api'

const BASE_URL = '/settings'

// --- Worldview Service ---
const worldviewService = {
  getAll: () => api.get(`${BASE_URL}/worldviews/`),
  create: (data) => api.post(`${BASE_URL}/worldviews/`, data),
  update: (id, data) => api.put(`${BASE_URL}/worldviews/${id}`, data),
  delete: (id) => api.delete(`${BASE_URL}/worldviews/${id}`),
}

// --- Writing Style Service ---
const writingStyleService = {
  getAll: () => api.get(`${BASE_URL}/writing-styles/`),
  create: (data) => api.post(`${BASE_URL}/writing-styles/`, data),
  update: (id, data) => api.put(`${BASE_URL}/writing-styles/${id}`, data),
  delete: (id) => api.delete(`${BASE_URL}/writing-styles/${id}`),
}

// --- Prompt Template Service ---
const promptTemplateService = {
  getAll: () => api.get(`${BASE_URL}/prompt-templates/`),
  create: (data) => api.post(`${BASE_URL}/prompt-templates/`, data),
  update: (id, data) => api.put(`${BASE_URL}/prompt-templates/${id}`, data),
  delete: (id) => api.delete(`${BASE_URL}/prompt-templates/${id}`),
}

// --- Generated Outline Service ---
const generatedOutlineService = {
  getAllForProject: (projectId) =>
    api.get(`${BASE_URL}/generated-outlines/project/${projectId}`),
  create: (data) => api.post(`${BASE_URL}/generated-outlines/`, data),
  delete: (id) => api.delete(`${BASE_URL}/generated-outlines/${id}`),
}

// --- AI Model Service ---
const aiModelService = {
  getAll: () => api.get(`${BASE_URL}/ai-models/`),
  create: (data) => api.post(`${BASE_URL}/ai-models/`, data),
  update: (id, data) => api.put(`${BASE_URL}/ai-models/${id}`, data),
  delete: (id) => api.delete(`${BASE_URL}/ai-models/${id}`),
  testConnection: (id) =>
    api.post(`${BASE_URL}/ai-models/${id}/test-connection`),
}

// --- AI Generation Service ---
const aiGenerationService = {
  getInitialPrompt: (data) => api.post('/ai/get-initial-prompt', data),
  generateOutline: (data) => api.post('/ai/generate-outline', data),
  generateOutlineStream: (data) => {
    // Reverting to fetch for proper browser stream handling.
    return fetch('/api/v1/ai/generate-outline-stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
  },
}

export {
  worldviewService,
  writingStyleService,
  promptTemplateService,
  generatedOutlineService,
  aiModelService,
  aiGenerationService,
}
