import apiClient from './api';

export default {
    getProjects(skip = 0, limit = 100) {
        return apiClient.get(`/projects/?skip=${skip}&limit=${limit}`);
    },
    createProject(projectData) {
        return apiClient.post('/projects/', projectData);
    },
    deleteProject(projectId) {
        return apiClient.delete(`/projects/${projectId}`);
    },

    getProject(projectId) {
        return apiClient.get(`/projects/${projectId}`);
    },
    updateProject(projectId, projectData) {
        return apiClient.put(`/projects/${projectId}`, projectData);
    },
};
