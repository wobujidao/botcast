import api from './api';

export const authService = {
  async register(email, password) {
    const response = await api.post('/auth/register', { email, password });
    return response.data;
  },

  async login(email, password) {
    const response = await api.post('/auth/login', { email, password });
    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    return response.data;
  },

  async getCurrentUser() {
    const response = await api.get('/users/me');
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  },

  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  }
};
