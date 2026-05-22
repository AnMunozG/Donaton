import api from './api';

export const donacionesService = {
  getAll: (params) => api.get('/donaciones', { params }),
  getById: (id) => api.get(`/donaciones/${id}`),
  create: (data) => api.post('/donaciones', data),
  update: (id, data) => api.put(`/donaciones/${id}`, data),
  delete: (id) => api.delete(`/donaciones/${id}`),
  getByCentro: (centroId) => api.get(`/donaciones/centro/${centroId}`),
};
