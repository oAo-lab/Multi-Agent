import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export interface Task {
  id: string;
  name: string;
  status: 'created' | 'pending' | 'running' | 'completed' | 'error' | 'stopped';
  created_at: string;
  progress: string;
  agents: string;
}

export const fetchTasks = async (): Promise<Task[]> => {
  const response = await api.get('/tasks');
  return response.data;
};

export const createTask = async (taskData: { name: string; template: string }) => {
  const response = await api.post('/tasks', taskData);
  return response.data;
};

export const startTask = async (taskId: string) => {
  try {
    const response = await api.get(`/tasks/${taskId}/start`);
    return response.data;
  } catch (err: any) {
    const errorMessage = err.response?.data?.detail || err.message || 'Unknown error';
    throw new Error(`Failed to start task: ${errorMessage}`);
  }
};

export const stopTask = async (taskId: string) => {
  try {
    const response = await api.get(`/tasks/${taskId}/stop`);
    return response.data;
  } catch (err: any) {
    const errorMessage = err.response?.data?.detail || err.message || 'Unknown error';
    throw new Error(`Failed to stop task: ${errorMessage}`);
  }
};

export const deleteTask = async (taskId: string) => {
  return await api.delete(`/tasks/${taskId}`);
};

export const editTask = async (taskId: string, taskData: { name: string; description: string }) => {
  return await api.put(`/tasks/${taskId}`, taskData);
};

export const fetchTaskHistory = async (taskId: string) => {
  const response = await api.get(`/tasks/${taskId}/history`);
  return response.data;
};
