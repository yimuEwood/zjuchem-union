import http from './http'

export function getMembers() {
  return http.get('/members')
}
