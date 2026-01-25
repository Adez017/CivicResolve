
import axios from 'axios';

const BASE_API_URL = 'http://localhost:5000/api';
export const IMG_BASE_URL = 'http://localhost:5000/data/images';

export const api = axios.create({
  baseURL: BASE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const endpoints = {
  ai: {
    predict: '/ai/predict',
  },
  citizen: {
    report: '/citizen/report',
  },
  admin: {
    reports: '/admin/reports',
  },
  workflow: {
    assign: '/workflow/tasks/assign',
    workerTasks: (workerId: string) => `/workflow/worker/my-tasks/${workerId}`,
    complete: '/workflow/worker/complete',
    verify: '/workflow/verify/verify',
  },
};
