import api from './api';

export const necesidadesService = {
  getAll: (params) => api.get('/necesidades', { params }),
  getById: (id) => api.get(`/necesidades/${id}`),
  create: (data) => api.post('/necesidades', data),
  update: (id, data) => api.put(`/necesidades/${id}`, data),
  delete: (id) => api.delete(`/necesidades/${id}`),
  activar: (id, urgencia) => api.post(`/necesidades/${id}/activar`, { urgencia }),
};
