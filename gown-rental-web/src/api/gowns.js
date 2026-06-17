import api from './index'

export function getGowns(params) {
  return api.get('/gowns/', { params })
}

export function getGown(id) {
  return api.get(`/gowns/${id}`)
}

export function createGown(data) {
  return api.post('/gowns/', data)
}

export function updateGown(id, data) {
  return api.put(`/gowns/${id}`, data)
}

export function retireGown(id) {
  return api.delete(`/gowns/${id}`)
}

export function checkAvailability(id, targetDate) {
  return api.get(`/gowns/${id}/availability`, { params: { target_date: targetDate } })
}
