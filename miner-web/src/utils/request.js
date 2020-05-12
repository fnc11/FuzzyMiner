import axios from 'axios';
import { Message } from 'element-ui';

// Create axios instance
const service = axios.create({
    baseURL: '/api',
    // withCredentials: true,
    timeout: 20000 // Request timeout
});

// Request intercepter
// service.interceptors.request.use(
//     config => {
//         return config;
//     },
//     error => {
//         // Do something with request error
//         console.log(error); // for debug
//         Promise.reject(error);
//     }
// );

// response pre-processing
service.interceptors.response.use(
    response => {
        return response.data;
    },
    error => {
        // handle error
        Message({
            message: error.message,
            type: 'error',
            duration: 5 * 1000,
        });
        return Promise.reject(error);
    },
);

export default service;
