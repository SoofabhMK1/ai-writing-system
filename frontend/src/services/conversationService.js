import api from './api'

const BASE_URL = '/conversations'

const conversationService = {
  create(conversationData) {
    return api.post(BASE_URL + '/', conversationData)
  },

  getByProject(projectId) {
    return api.get(`${BASE_URL}/project/${projectId}`)
  },

  get(id) {
    return api.get(`${BASE_URL}/${id}`)
  },

  update(id, conversationData) {
    return api.put(`${BASE_URL}/${id}`, conversationData)
  },

  delete(id) {
    return api.delete(`${BASE_URL}/${id}`)
  },

  // Note: The chat stream is handled separately, not in this service.
  // It will be called directly from the store using the browser's fetch API
  // to handle the streaming response correctly.
}

export default conversationService
