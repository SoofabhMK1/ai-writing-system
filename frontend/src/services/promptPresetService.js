import api from './api';

const BASE_URL = '/prompt-presets/';

export const promptPresetService = {
  getAll() {
    return api.get(BASE_URL);
  },

  getById(id) {
    return api.get(`${BASE_URL}/${id}`);
  },

  create(data) {
    return api.post(BASE_URL, data);
  },

  update(id, data) {
    return api.put(`${BASE_URL}/${id}`, data);
  },

  delete(id) {
    return api.delete(`${BASE_URL}/${id}`);
  },
};
