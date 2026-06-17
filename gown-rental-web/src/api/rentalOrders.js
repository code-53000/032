import api from './index'

export function getRentalOrders(params) {
  return api.get('/rental-orders/', { params })
}

export function getRentalOrder(id) {
  return api.get(`/rental-orders/${id}`)
}

export function createRentalOrder(data) {
  return api.post('/rental-orders/', data)
}

export function updateRentalOrder(id, data) {
  return api.put(`/rental-orders/${id}`, data)
}

export function cancelRentalOrder(id) {
  return api.delete(`/rental-orders/${id}`)
}
