import http from './http'

export function getTasks() {
  return http.get('/tasks')
}

export function createTask(data) {
  return http.post('/tasks', data)
}

export function updateTask(id, data) {
  return http.put(`/tasks/${id}`, data)
}

export function deleteTask(id) {
  return http.delete(`/tasks/${id}`)
}

export function updateTaskStatus(id, status) {
  return http.patch(`/tasks/${id}/status`, { status })
}
