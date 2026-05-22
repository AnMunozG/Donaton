import api from './api';

export const centrosService = {
  getAll: (params) => api.get('/centros', { params }),
  getById: (id) => api.get(`/centros/${id}`),
  create: (data) => api.post('/centros', data),
  update: (id, data) => api.put(`/centros/${id}`, data),
  delete: (id) => api.delete(`/centros/${id}`),
  getInventario: (id) => api.get(`/centros/${id}/inventario`),
};
