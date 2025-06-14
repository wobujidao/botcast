import api from './api';

export const botService = {
  async getAll() {
    const response = await api.get('/bots/');
    return response.data;
  },

  async getById(id) {
    const response = await api.get(`/bots/${id}`);
    return response.data;
  },

  async create(botData) {
    const response = await api.post('/bots/', botData);
    return response.data;
  },

  async update(id, botData) {
    const response = await api.put(`/bots/${id}`, botData);
    return response.data;
  },

  async delete(id) {
    await api.delete(`/bots/${id}`);
  },

  async start(id) {
    const response = await api.post(`/bots/${id}/start`);
    return response.data;
  },

  async stop(id) {
    const response = await api.post(`/bots/${id}/stop`);
    return response.data;
  },

  async getStatus(id) {
    const response = await api.get(`/bots/${id}/status`);
    return response.data;
  }
};
