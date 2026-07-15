<template>
  <header class="catalog-header">
    <div class="brand-controls-group">
      <q-btn v-if="route.path.startsWith('/product/')"
             flat
             round
             dense
             icon="arrow_back"
             color="primary"
             @click="router.push('/catalog')"
             class="q-mr-xs" />

      <div class="brand" @click="goToHome" style="cursor: pointer;">
        <h2>FEFU<span>STORE</span></h2>
      </div>

      <div v-if="showFilter && !minimal" class="header-controls">
        <q-input :model-value="searchQuery"
                 @update:model-value="$emit('update:searchQuery', $event)"
                 outlined
                 dense
                 label="Поиск товаров..."
                 clearable
                 bg-color="white"
                 class="search-input">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-select :model-value="selectedCategorySlug"
                  @update:model-value="$emit('update:selectedCategorySlug', $event)"
                  :options="categoryOptions"
                  outlined
                  dense
                  emit-value
                  map-options
                  bg-color="white"
                  class="category-select" />
      </div>
    </div>

    <div class="header-actions">
      <q-btn v-if="route.path === '/cart' || route.path === '/orders'"
             flat
             dense
             icon="storefront"
             label="В каталог"
             color="primary"
             to="/catalog"
             class="q-mr-md" />

      <div v-if="authStore.isAuthenticated && !authStore.isStaff && !minimal" class="user-buttons q-mr-md">
        <q-btn flat round dense icon="shopping_cart" color="primary" to="/cart" class="q-mr-xs">
          <q-badge v-if="cartStore.cartCount > 0" floating color="cyan-8" rounded class="cart-badge">
            {{ cartStore.cartCount }}
          </q-badge>
          <q-tooltip>Корзина</q-tooltip>
        </q-btn>

        <q-btn flat dense icon="list_alt" label="Мои заказы" color="secondary" to="/orders" />
      </div>

      <q-btn v-if="authStore.isAuthenticated && authStore.isStaff && !minimal"
             flat dense icon="dashboard" label="Админка" color="deep-orange" to="/admin" class="q-mr-md" />

      <button v-if="authStore.isAuthenticated" @click="$emit('logout')" class="btn-logout">
        Выйти из аккаунта
      </button>
      <button v-else-if="!minimal" @click="goToLogin" class="btn-login">
        Войти
      </button>
    </div>
  </header>
</template>

<script setup>
  import { useRoute, useRouter } from 'vue-router'
  import { useAuthStore } from '../stores/auth'
  import { useCartStore } from '../stores/cart'

  const route = useRoute()
  const router = useRouter()
  const authStore = useAuthStore()
  const cartStore = useCartStore()

  defineProps({
    searchQuery: String,
    selectedCategorySlug: [String, null],
    categoryOptions: Array,
    showFilter: {
      type: Boolean,
      default: true
    },
    minimal: {
      type: Boolean,
      default: false
    }
  })

  defineEmits([
    'update:searchQuery',
    'update:selectedCategorySlug',
    'logout'
  ])

  const goToHome = () => {
    if (authStore.isStaff) {
      router.push('/admin')
    } else {
      router.push('/catalog')
    }
  }

  const goToLogin = () => router.push('/login')
</script>

<style scoped>
  .catalog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    border-bottom: 1px solid #e2e8f0;
    gap: 20px;
  }

  .brand-controls-group {
    display: flex;
    align-items: center;
    gap: 24px;
    flex-grow: 1;
    max-width: 850px;
  }

  .brand h2 {
    font-size: 24px;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin: 0;
    color: #0f172a;
  }

    .brand h2 span {
      color: #00b4d8;
    }

  .header-controls {
    display: flex;
    gap: 16px;
    flex-grow: 1;
  }

  .search-input {
    flex-grow: 2;
  }

  .category-select {
    flex-grow: 1;
    min-width: 200px;
  }

  .header-actions {
    display: flex;
    align-items: center;
  }

  .btn-logout, .btn-login {
    padding: 10px 18px;
    background: transparent;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    color: #64748b;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

    .btn-logout:hover {
      background: #fff1f2;
      border-color: #fda4af;
      color: #e11d48;
    }

  .btn-login {
    border-color: #00b4d8;
    color: #00b4d8;
  }

    .btn-login:hover {
      background: #e0f2fe;
      color: #0369a1;
    }

  .cart-badge {
    font-weight: 700;
    padding: 3px 6px;
  }

  @media (max-width: 800px) {
    .catalog-header {
      flex-direction: column;
      align-items: stretch;
    }

    .brand-controls-group {
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 16px;
    }

    .header-controls {
      flex-direction: column;
      gap: 10px;
      width: 100%;
    }

    .category-select {
      width: 100%;
    }

    .header-actions {
      flex-direction: column;
      gap: 10px;
      width: 100%;
    }

    .user-buttons {
      display: flex;
      width: 100%;
      justify-content: space-between;
      margin-right: 0 !important;
    }

    .btn-logout, .btn-login {
      width: 100%;
    }
  }
</style>
