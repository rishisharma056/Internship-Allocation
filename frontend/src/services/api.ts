import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000', // Update with your backend URL
});
api.defaults.headers.post['Content-Type'] = 'application/json';
api.defaults.headers.post['Accept'] = 'application/json';
api.defaults.withCredentials = true;
api.defaults.timeout = 10000; // 10 seconds timeout
api.interceptors.response.use(
    (    response: any) => response,
    (    error: { code: string; }) => {
        if (error.code === 'ECONNABORTED') {
            console.error('Request timed out');
            return Promise.reject(new Error('Request timed out. Please try again.'));
        }
        return Promise.reject(error);
    }
);
export async function fetchInternships() {
  try {
    const response = await api.get('/internships');
    return response.data;
  } catch (error) {
    console.error('Error fetching internships:', error);
    throw error;
  }
}

export async function fetchStudents() {
  try {
    const response = await api.get('/students');
    return response.data;
  } catch (error) {
    console.error('Error fetching students:', error);
    throw error;
  }
}