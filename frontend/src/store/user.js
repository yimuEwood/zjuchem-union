import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  async function login(username, password) {
    const res = await loginApi(username, password)
    token.value = res.token
    localStorage.setItem('token', res.token)
    user.value = res.user
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      user.value = await getCurrentUser()
    } catch {
      // token 过期
      logout()
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { user, token, login, fetchUser, logout }
})
