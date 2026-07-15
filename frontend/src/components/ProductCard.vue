<template>
  <div class="product-card" @click="router.push(`/product/${product.id}`)">
    <div class="product-image-wrapper">
      <div v-if="product.image && !imageError" class="product-image-container">
        <img :src="product.image ? product.image.replace('http://127.0.0.1:8000', '') : ''"
             @error="handleImageError"
             class="product-img" />
      </div>
      <div v-else class="product-image-bg">
        <span class="image-placeholder">FEFU STORE</span>
      </div>

      <span class="category-badge">{{ product.category_name || 'Товар' }}</span>
    </div>

    <div class="product-info">
      <h3 class="product-title" :title="product.name">{{ product.name }}</h3>

      <div class="product-footer">
        <div class="price-container">
          <span class="product-price">{{ product.price }} ₽</span>
        </div>
        <button @click.stop="cartStore.addToCart(product)" class="btn-add" title="Купить">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1" /><circle cx="20" cy="21" r="1" /><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" /></svg>
          <span>Купить</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useCartStore } from '../stores/cart'

  const router = useRouter()
  const cartStore = useCartStore()

  defineProps({
    product: { type: Object, required: true }
  })

  const imageError = ref(false)

  const handleImageError = () => {
    imageError.value = true
  }
</script>

<style scoped>
  .product-card {
    background: #ffffff;
    border: 1px solid #eef2f6;
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
    height: 100%;
  }

    .product-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 24px rgba(10, 37, 64, 0.06);
      border-color: #00b4d8;
    }

  .product-image-wrapper {
    position: relative;
    height: 240px;
    padding: 8px;
    overflow: hidden;
  }

  .product-image-container {
    width: 100%;
    height: 100%;
    background: #f8fafc;
    border-radius: 10px;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }

  .product-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .product-card:hover .product-img {
    transform: scale(1.03);
  }

  .product-image-bg {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .product-card:hover .product-image-bg {
    transform: scale(1.02);
  }

  .image-placeholder {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
  }

  .category-badge {
    position: absolute;
    top: 14px;
    left: 14px;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(4px);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 9px;
    font-weight: 700;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  }

  .product-info {
    padding: 12px 14px 14px 14px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: space-between;
  }

  .product-title {
    color: #0f172a;
    font-size: 15px;
    margin: 0 0 12px 0;
    font-weight: 600;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .product-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 10px;
    border-top: 1px solid #f8fafc;
  }

  .price-container {
    display: flex;
    flex-direction: column;
  }

  .product-price {
    color: #0f172a;
    font-size: 17px;
    font-weight: 700;
  }

  .btn-add {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    background: #0f172a;
    border: none;
    border-radius: 10px;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

    .btn-add:hover {
      background: #00b4d8;
      box-shadow: 0 4px 12px rgba(0, 180, 216, 0.2);
    }

    .btn-add svg {
      transition: transform 0.2s ease;
    }

    .btn-add:hover svg {
      transform: scale(1.05);
    }
</style>
