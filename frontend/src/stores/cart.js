import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/boot/axios'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])

  const cartCount = computed(() => items.value.length)

  const totalSum = computed(() => {
    return items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  })

  async function loadCart() {
    try {
      const response = await api.get('/api/cart/')
      console.log('Данные корзины от Django:', response.data)

      let rawItems = []

      if (response.data && Array.isArray(response.data.items)) {
        rawItems = response.data.items
      } else if (Array.isArray(response.data)) {
        rawItems = response.data
      }

      items.value = rawItems.map(item => ({
        id: item.id,
        productId: item.product?.id || item.product_id,
        name: item.product?.name || 'Товар',
        price: item.product?.price || 0,
        image: item.product?.image || '',
        quantity: item.quantity
      }))
    } catch (error) {
      console.error('Ошибка при загрузке корзины:', error)
    }
  }

  async function addToCart(product) {
    try {
      await api.post('/api/cart/', {
        product_id: product.id,
        quantity: 1
      })

      await loadCart()
    } catch (error) {
      console.error('Ошибка добавления в корзину на бэкенде:', error)
    }
  }

  async function incrementQty(itemId) {
    const item = items.value.find(i => i.id === itemId)
    if (item) {
      try {
        const newQty = item.quantity + 1

        await api.put(`/api/cart/${itemId}/`, { quantity: newQty })

        item.quantity = newQty
      } catch (error) {
        console.error('Ошибка изменения количества:', error)
      }
    }
  }

  async function decrementQty(itemId) {
    const item = items.value.find(i => i.id === itemId)
    if (item && item.quantity > 1) {
      try {
        const newQty = item.quantity - 1

        await api.put(`/api/cart/${itemId}/`, { quantity: newQty })

        item.quantity = newQty
      } catch (error) {
        console.error('Ошибка изменения количества:', error)
      }
    }
  }

  async function removeFromCart(itemId) {
    try {
      await api.delete(`/api/cart/${itemId}/`)
      items.value = items.value.filter(i => i.id !== itemId)
    } catch (error) {
      console.error('Ошибка удаления из корзины:', error)
    }
  }

  function clearCart() {
    items.value = []
  }

  return {
    items,
    cartCount,
    totalSum,
    loadCart,
    addToCart,
    incrementQty,
    decrementQty,
    removeFromCart,
    clearCart
  }
})
