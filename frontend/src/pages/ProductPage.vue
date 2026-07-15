<template>
  <div class="product-page-layout">
    <div class="center-content-wrapper">

      <CatalogHeader :show-filter="false" @logout="handleLogout" />

      <div v-if="loading" class="podium-card-3d loading-state">
        <div class="store-spinner"></div>
      </div>

      <div v-else-if="product" class="podium-card-3d product-showcase">

        <div class="preview-zone-cover">
          <span class="category-badge-custom">{{ product.category_name || 'Товар' }}</span>

          <div class="cover-image-container">
            <img v-if="product.image && !imageError"
                 :src="product.image.replace('http://127.0.0.1:8000', '')"
                 @error="handleImageError"
                 alt="Изображение товара"
                 class="full-cover-img" />
            <div v-else class="no-image-stub-cover">
              <span class="image-placeholder-custom">FEFU STORE</span>
            </div>
          </div>
        </div>

        <div class="details-zone">
          <div class="main-info">
            <h1 class="item-title">{{ product.name }}</h1>

            <div class="stock-status" :class="{ 'out-of-stock': !product.is_active }">
              <span class="status-dot"></span>
              {{ product.is_active ? 'В наличии на кампусе' : 'Нет в наличии' }}
            </div>

            <p class="item-description">
              {{ product.description || 'Прекрасный выбор для учебы и жизни на кампусе.' }}
            </p>
          </div>

          <div class="action-bar">
            <div class="price-container">
              <span class="price-label-custom">Цена</span>
              <span class="product-price-custom">{{ product.price }} ₽</span>
            </div>

            <button class="btn-add"
                    :disabled="!product.is_active"
                    @click="cartStore.addToCart(product)">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1" /><circle cx="20" cy="21" r="1" /><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" /></svg>
              Купить
            </button>
          </div>
        </div>

      </div>

      <div v-else class="podium-card-3d error-state">
        <h2>Товар не найден</h2>
        <p>Пожалуйста, вернитесь в каталог.</p>
      </div>

      <div class="surface-shadow-glow"></div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { api } from '../boot/axios'
  import { useCartStore } from '../stores/cart'
  import { useAuthStore } from '../stores/auth'
  import CatalogHeader from '../components/TopBar.vue'

  const route = useRoute()
  const router = useRouter()
  const cartStore = useCartStore()
  const authStore = useAuthStore()

  const product = ref(null)
  const loading = ref(true)
  const imageError = ref(false)

  const loadProductData = async () => {
    try {
      loading.value = true
      const response = await api.get(`/api/products/${route.params.id}/`)
      product.value = response.data
    } catch (e) {
      console.error('Ошибка при получении товара:', e)
    } finally {
      loading.value = false
    }
  }

  const handleImageError = () => {
    imageError.value = true
  }

  const handleLogout = async () => {
    try {
      await authStore.logout()
      router.push('/login')
    } catch (e) {
      console.error('Ошибка при выходе из системы:', e)
    }
  }

  onMounted(() => {
    loadProductData()
  })
</script>

<style scoped>
  .product-page-layout {
    position: relative;
    width: 100%;
    min-height: 100vh;
    background: #f8fafc;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 50px 20px;
    box-sizing: border-box;
  }

  .center-content-wrapper {
    position: relative;
    width: 100%;
    max-width: 900px;
    display: flex;
    flex-direction: column;
    gap: 32px;
    transform: perspective(1200px) rotateX(1deg);
  }

  .podium-card-3d {
    position: relative;
    z-index: 2;
    background: #ffffff;
    border: 1px solid #eef2f6;
    border-radius: 24px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
    overflow: hidden;
  }

  .surface-shadow-glow {
    position: absolute;
    bottom: -25px;
    left: 8%;
    width: 84%;
    height: 35px;
    background: radial-gradient(ellipse at center, rgba(15, 23, 42, 0.12) 0%, rgba(15, 23, 42, 0) 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
    filter: blur(10px);
  }

  .product-showcase {
    display: grid;
    grid-template-columns: 50% 50%;
    min-height: 520px;
  }

  @media (max-width: 768px) {
    .product-showcase {
      grid-template-columns: 1fr;
    }
  }

  .preview-zone-cover {
    position: relative;
    background: #f8fafc;
    overflow: hidden;
  }

  .cover-image-container {
    width: 100%;
    height: 100%;
    display: flex;
  }

  .full-cover-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }

  .no-image-stub-cover {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  }

  .image-placeholder-custom {
    color: #94a3b8;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 2px;
  }

  .category-badge-custom {
    position: absolute;
    top: 24px;
    left: 24px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(4px);
    padding: 6px 14px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    z-index: 3;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  }

  .details-zone {
    padding: 40px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #ffffff;
  }

  .item-title {
    color: #0f172a;
    font-size: 26px;
    font-weight: 700;
    margin: 0 0 12px 0;
    line-height: 1.3;
  }

  .stock-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: #10b981;
    font-weight: 500;
    margin-bottom: 24px;
  }

    .stock-status.out-of-stock {
      color: #ef4444;
    }

  .status-dot {
    width: 7px;
    height: 7px;
    background-color: currentColor;
    border-radius: 50%;
  }

  .item-description {
    color: #64748b;
    font-size: 15px;
    line-height: 1.6;
    margin: 0;
  }

  .action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #f1f5f9;
  }

  .price-container {
    display: flex;
    flex-direction: column;
  }

  .price-label-custom {
    font-size: 11px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
  }

  .product-price-custom {
    color: #0f172a;
    font-size: 26px;
    font-weight: 800;
  }

  .btn-add {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 22px;
    background: #0f172a;
    border: none;
    border-radius: 14px;
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

    .btn-add:hover:not(:disabled) {
      background: #00b4d8;
      box-shadow: 0 8px 20px rgba(0, 180, 216, 0.3);
    }

    .btn-add svg {
      transition: transform 0.3s ease;
    }

    .btn-add:hover:not(:disabled) svg {
      transform: scale(1.1);
    }

    .btn-add:disabled {
      background: #cbd5e1;
      color: #94a3b8;
      cursor: not-allowed;
    }

  .loading-state, .error-state {
    height: 380px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .store-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #f1f5f9;
    border-left-color: #0f172a;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
