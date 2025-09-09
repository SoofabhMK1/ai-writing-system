// src/services/api.js
import axios from 'axios';

const apiClient = axios.create({
    baseURL: '/api/v1', // 使用相对路径，以便 Vite 代理
    headers: {
        'Content-Type': 'application/json'
    }
});

export default apiClient;
