import { defineStore } from 'pinia'
import { api } from '../boot/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || null,
    isStaff: localStorage.getItem('is_staff') === 'true'
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async login(username, password) {
      try {
        const response = await api.post('/api/auth/login/', { username, password })

        this.token = response.data.access
        localStorage.setItem('access_token', this.token)

        if (response.data.refresh) {
          localStorage.setItem('refresh_token', response.data.refresh)
        }

        this.isStaff = response.data.is_staff || response.data.user?.is_staff || false
        localStorage.setItem('is_staff', String(this.isStaff))

        return { success: true }
      } catch (error) {
        console.error('Ошибка стора при входе:', error.response?.data)

        let msg = 'Неверный логин или пароль'
        const serverDetail = error.response?.data?.detail

        if (serverDetail === 'No active account found with the given credentials') {
          msg = 'Неверное имя пользователя или пароль.'
        } else if (serverDetail) {
          msg = serverDetail
        }

        return {
          success: false,
          message: msg
        }
      }
    },

    logout() {
      this.token = null
      this.isStaff = false

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('is_staff')
    }
  }
})
