import { defineStore } from 'pinia'
import { api } from '../boot/axios'

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    categories: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchProducts(params = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/api/products/', { params })
        this.products = response.data
      } catch (err) {
        console.error('Ошибка загрузки товаров:', err)
        this.error = 'Не удалось загрузить каталог товаров'
      } finally {
        this.loading = false
      }
    },

    async fetchCategories() {
      try {
        const response = await api.get('/api/categories/')
        this.categories = response.data
      } catch (err) {
        console.error('Ошибка загрузки категорий:', err)
      }
    },
    async createProduct(productData) {
      this.loading = true
      try {
        const response = await api.post('/api/products/', productData)
        this.products.push(response.data)
      } catch (err) {
        console.error('Ошибка при создании товара:', err)
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateProduct(id, productData) {
      try {
        const response = await api.put(`/api/products/${id}/`, productData)
        const updatedProduct = response.data.data || response.data

        const index = this.products.findIndex(p => p.id === id)
        if (index !== -1) {
          this.products[index] = updatedProduct
        }
      } catch (err) {
        console.error('Ошибка при обновлении товара:', err)
        throw err
      }
    },

    async deleteProduct(id) {
      try {
        await api.delete(`/api/products/${id}/`)
        this.products = this.products.filter(p => p.id !== id)
      } catch (err) {
        console.error('Ошибка при удалении товара:', err)
        throw err
      }
    },

    async createCategory(categoryData) {
      try {
        const response = await api.post('/api/categories/', categoryData)
        this.categories.push(response.data)
        this.categories.sort((a, b) => a.name.localeCompare(b.name))
      } catch (err) {
        console.error('Ошибка при создании категории:', err)
        throw err
      }
    },

    async updateCategory(id, categoryData) {
      try {
        const response = await api.put(`/api/categories/${id}/`, categoryData)
        const index = this.categories.findIndex(c => c.id === id)
        if (index !== -1) this.categories[index] = response.data
        return true
      } catch (error) {
        console.error('Ошибка при обновлении категории в сторе:', error)
        throw error
      }
    }
  }
})
