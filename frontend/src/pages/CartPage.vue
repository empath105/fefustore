<template>
  <div class="cart-page-wrapper">
    <div class="cart-container">

      <CatalogHeader :show-filter="false" @logout="handleLogout" />

      <div v-if="cartStore.items.length === 0" class="empty-cart-view">
        <div class="empty-illustration">🛒</div>
        <h2>В корзине пока ничего нет</h2>
        <p>Не знаете с чего начать? Загляните в каталог, там много интересного.</p>
        <router-link to="/catalog" class="btn-back-to-shop">Перейти в каталог</router-link>
      </div>

      <div v-else class="cart-content-grid">

        <div class="cart-items-column">
          <div v-for="item in cartStore.items" :key="item.id" class="cart-page-item">

            <div class="item-main-info">
              <div class="item-img-box">
                <img v-if="item.image" :src="item.image.replace('http://127.0.0.1:8000', '')" alt="product" />
                <div v-else class="item-stub">FS</div>
              </div>

              <div class="item-meta">
                <h3 class="item-title">{{ item.name }}</h3>
              </div>
            </div>

            <div class="item-actions-zone">
              <div class="quantity-selector">
                <button @click="cartStore.decrementQty(item.id)" :disabled="item.quantity <= 1">−</button>
                <span class="quantity-value">{{ item.quantity }}</span>
                <button @click="cartStore.incrementQty(item.id)">+</button>
              </div>

              <div class="price-calculations">
                <span class="item-final-price">{{ item.price * item.quantity }} ₽</span>
                <span v-if="item.quantity > 1" class="price-per-unit">{{ item.price }} ₽ / шт.</span>
              </div>

              <button class="btn-delete-item" @click="cartStore.removeFromCart(item.id)" title="Удалить товар">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
              </button>
            </div>

          </div>
        </div>

        <div class="cart-summary-column">
          <div class="summary-sticky-card">
            <h3 class="summary-title">Условия заказа</h3>

            <div class="summary-rows">
              <div class="summary-row">
                <span>Товары ({{ cartStore.cartCount }})</span>
                <span>{{ cartStore.totalSum }} ₽</span>
              </div>
              <div class="summary-row">
                <span>Доставка</span>
                <span class="free-delivery-text">Бесплатно</span>
              </div>
            </div>

            <hr class="summary-divider" />

            <div class="summary-total">
              <span>Итого</span>
              <span class="total-sum-value">{{ cartStore.totalSum }} ₽</span>
            </div>

            <button class="btn-place-order" @click="handleGoToCheckout">
              <span>Перейти к оформлению</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </button>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
  import { useRouter } from 'vue-router'
  import { useCartStore } from '../stores/cart'
  import { useAuthStore } from '../stores/auth'
  import CatalogHeader from '../components/TopBar.vue'

  const router = useRouter()
  const cartStore = useCartStore()
  const authStore = useAuthStore()

  const handleGoToCheckout = () => {
    router.push('/checkout')
  }

  const handleLogout = async () => {
    try {
      await authStore.logout()
      router.push('/login')
    } catch (e) {
      console.error('Ошибка при выходе:', e)
    }
  }
</script>

<style scoped>
  .cart-page-wrapper {
    background: #fafafa;
    min-height: 100vh;
    padding: 40px 0;
  }

  .cart-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    flex-direction: column;
    gap: 32px;
  }

  .cart-content-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 32px;
    align-items: start;
  }

  @media (min-width: 1024px) {
    .cart-content-grid {
      grid-template-columns: 7fr 3fr;
    }
  }

  .cart-items-column {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .cart-page-item {
    display: flex;
    flex-direction: column;
    background: #ffffff;
    border: 1px solid #eef2f6;
    border-radius: 16px;
    padding: 20px;
    gap: 20px;
  }

  @media (min-width: 640px) {
    .cart-page-item {
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
    }
  }

  .item-main-info {
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
  }

  .item-img-box {
    width: 90px;
    height: 90px;
    background: #f8fafc;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

    .item-img-box img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

  .item-stub {
    font-size: 14px;
    font-weight: 700;
    color: #94a3b8;
  }

  .item-title {
    font-size: 16px;
    font-weight: 600;
    color: #0f172a;
    margin: 0;
    line-height: 1.4;
  }

  .item-actions-zone {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
  }

  @media (min-width: 640px) {
    .item-actions-zone {
      justify-content: flex-end;
    }
  }

  .quantity-selector {
    display: flex;
    align-items: center;
    background: #f1f5f9;
    border-radius: 10px;
    padding: 3px;
  }

    .quantity-selector button {
      background: transparent;
      border: none;
      width: 32px;
      height: 32px;
      font-size: 18px;
      color: #475569;
      cursor: pointer;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }

      .quantity-selector button:hover:not(:disabled) {
        background: #ffffff;
        color: #0f172a;
      }

  .quantity-value {
    font-size: 14px;
    font-weight: 600;
    min-width: 32px;
    text-align: center;
    color: #0f172a;
  }

  .price-calculations {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    min-width: 100px;
  }

  .item-final-price {
    font-size: 18px;
    font-weight: 700;
    color: #0f172a;
  }

  .price-per-unit {
    font-size: 12px;
    color: #64748b;
    margin-top: 2px;
  }

  .btn-delete-item {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    padding: 8px;
    border-radius: 50%;
    display: flex;
    transition: all 0.2s;
  }

    .btn-delete-item:hover {
      background: #fef2f2;
      color: #ef4444;
    }

  .summary-sticky-card {
    background: #ffffff;
    border: 1px solid #eef2f6;
    border-radius: 16px;
    padding: 24px;
    position: sticky;
    top: 24px;
  }

  .summary-title {
    margin: 0 0 20px 0;
    font-size: 18px;
    font-weight: 700;
    color: #0f172a;
  }

  .summary-rows {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .summary-row {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: #64748b;
  }

  .free-delivery-text {
    color: #10b981;
    font-weight: 600;
  }

  .summary-divider {
    border: 0;
    border-top: 1px solid #f1f5f9;
    margin: 16px 0;
  }

  .summary-total {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 24px;
  }

    .summary-total span:first-child {
      font-size: 16px;
      font-weight: 600;
      color: #0f172a;
    }

  .total-sum-value {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
  }

  .btn-place-order {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px;
    background: #0f172a;
    border: none;
    border-radius: 12px;
    color: #ffffff;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

    .btn-place-order:hover {
      background: #00b4d8;
      box-shadow: 0 8px 24px rgba(0, 180, 216, 0.25);
    }

    .btn-place-order svg {
      transition: transform 0.2s ease;
    }

    .btn-place-order:hover svg {
      transform: translateX(4px);
    }

  .empty-cart-view {
    background: #ffffff;
    border: 1px solid #eef2f6;
    border-radius: 16px;
    padding: 60px 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .empty-illustration {
    font-size: 56px;
    margin-bottom: 16px;
  }

  .empty-cart-view h2 {
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 8px 0;
  }

  .empty-cart-view p {
    color: #64748b;
    font-size: 14px;
    max-width: 320px;
    margin: 0 0 24px 0;
    line-height: 1.5;
  }

  .btn-back-to-shop {
    display: inline-block;
    background: #0f172a;
    color: #ffffff;
    text-decoration: none;
    padding: 12px 24px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
    transition: background 0.2s;
  }

    .btn-back-to-shop:hover {
      background: #00b4d8;
    }
</style>
