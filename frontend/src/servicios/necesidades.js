import api from './api';

export const necesidadesService = {
  getAll: (params) => api.get('/necesidades', { params }),
  getById: (id) => api.get(`/necesidades/${id}`),
  create: (data) => api.post('/necesidades', data),
  update: (id, data) => api.put(`/necesidades/${id}`, data),
  delete: (id) => api.delete(`/necesidades/${id}`),
  asignar: (id, centroId) => api.post(`/necesidades/${id}/asignar`, { centroId }),
};
