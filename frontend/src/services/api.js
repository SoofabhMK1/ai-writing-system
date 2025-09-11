import axios from 'axios';
import { useNotificationStore } from '@/store/notification';

const apiClient = axios.create({
    baseURL: '/api/v1', // 使用相对路径，以便 Vite 代理
    headers: {
        'Content-Type': 'application/json'
    }
});

// 响应拦截器
apiClient.interceptors.response.use(
    // 对响应数据做点什么
    response => response,
    // 对响应错误做点什么
    error => {
        const notificationStore = useNotificationStore();
        let message = '发生未知错误';

        if (error.response) {
            // 请求成功发出且服务器也响应了状态码，但状态代码超出了 2xx 的范围
            console.error('API Error Response:', error.response);
            message = error.response.data.detail || `服务器错误: ${error.response.status}`;
        } else if (error.request) {
            // 请求已经成功发起，但没有收到响应
            console.error('API No Response:', error.request);
            message = '网络错误，无法连接到服务器';
        } else {
            // 发送请求之前或者之后发生了错误
            console.error('API Error:', error.message);
            message = error.message;
        }

        notificationStore.show(message, 'error');

        return Promise.reject(error);
    }
);

export default apiClient;
