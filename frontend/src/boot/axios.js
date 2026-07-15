import axios from 'axios'
import { useAuthStore } from '@/stores/auth' 
const api = axios.create({ baseURL: '/' })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

api.interceptors.response.use((response) => {
  return response
}, async (error) => {
  const originalRequest = error.config
  if (error.response?.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true
    const refreshToken = localStorage.getItem('refresh_token')

    if (refreshToken) {
      try {
        const response = await axios.post('/api/auth/token/refresh/', {
          refresh: refreshToken
        })

        const newAccessToken = response.data.access
        localStorage.setItem('access_token', newAccessToken)

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        return axios(originalRequest)
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('is_staff')
        window.location.href = '/login'
      }
    }
  }
  return Promise.reject(error)
})

export { axios, api }

export default ({ app, router }) => {
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api

  router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
      return next('/login')
    }

    if (to.meta.requiresAdmin) {
      if (!authStore.isAuthenticated) {
        return next('/login')
      }
      if (!authStore.isStaff) {
        return next('/catalog') 
      }
    }

    if (to.meta.requiresBuyer) {
      if (!authStore.isAuthenticated) {
        return next('/login')
      }
      if (authStore.isStaff) {
        return next('/admin')
      }
    }
    next()
  })
}
