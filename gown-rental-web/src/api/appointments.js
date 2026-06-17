import api from './index'

export function getAppointments(params) {
  return api.get('/appointments/', { params })
}

export function getAppointment(id) {
  return api.get(`/appointments/${id}`)
}

export function createAppointment(data) {
  return api.post('/appointments/', data)
}

export function updateAppointment(id, data) {
  return api.put(`/appointments/${id}`, data)
}

export function cancelAppointment(id) {
  return api.delete(`/appointments/${id}`)
}
