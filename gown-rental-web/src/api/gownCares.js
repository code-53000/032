import api from './index'

export function getGownCares(params) {
  return api.get('/gown-cares/', { params })
}

export function createGownCare(data) {
  return api.post('/gown-cares/', data)
}

export function updateGownCare(id, data) {
  return api.put(`/gown-cares/${id}`, data)
}
