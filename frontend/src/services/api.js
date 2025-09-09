// src/services/api.js
import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8001/api/v1', // 这是我们后端 API 的地址
    headers: {
        'Content-Type': 'application/json'
    }
});

export default apiClient;