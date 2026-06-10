import http from './http'

export function getDocuments(params) {
  return http.get('/documents', { params })
}

export function uploadDocument(formData, onProgress) {
  return http.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (e) => {
      if (onProgress) onProgress(Math.round((e.loaded * 100) / e.total))
    },
  })
}

export function downloadDocument(id) {
  return http.get(`/documents/${id}/download`, { responseType: 'blob' })
}

export function deleteDocument(id) {
  return http.delete(`/documents/${id}`)
}
