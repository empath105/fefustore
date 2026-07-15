<template>
  <div class="catalog-page">
    <div class="catalog-container">
      <TopBar v-model:searchQuery="searchQuery"
                  v-model:selectedCategorySlug="selectedCategorySlug"
                  :category-options="categoryOptions"
                  @logout="handleLogout" />

      <section class="welcome-banner">
        <h1>Добро пожаловать в FEFU STORE</h1>
        <p>Выбирай лучшие товары с доставкой прямо на кампус Русского острова.</p>
      </section>

      <div v-if="productStore.loading" class="loading-grid">
        <div v-for="n in 4" :key="n" class="skeleton-card">
          <div class="skeleton-image"></div>
          <div class="skeleton-text line-1"></div>
          <div class="skeleton-text line-2"></div>
        </div>
      </div>

      <div v-else-if="productStore.error" class="error-container">
        <div class="error-icon">⚠️</div>
        <h3>Не удалось обновить каталог</h3>
        <p>{{ productStore.error }}</p>
        <button @click="loadCatalogData" class="btn-retry">
          Повторить попытку
        </button>
      </div>

      <main v-else-if="productStore.products && productStore.products.length > 0" class="products-grid">
        <ProductCard v-for="product in productStore.products"
                     :key="product.id"
                     :product="product"
                     @add-to-cart="addToCart" />
      </main>

      <div v-else class="empty-catalog-container">
        <q-icon name="sentiment_dissatisfied" size="64px" color="grey-6" />
        <div class="text-h6 text-grey-6 q-mt-md">Товары не найдены</div>
        <p class="text-grey-5">Попробуйте изменить параметры поиска или фильтр</p>
      </div>

    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '../stores/auth'
  import { useProductStore } from '../stores/products'
  import ProductCard from '../components/ProductCard.vue'
  import TopBar from '../components/TopBar.vue'

  const router = useRouter()
  const authStore = useAuthStore()
  const productStore = useProductStore()

  const searchQuery = ref('')
  const selectedCategorySlug = ref(null)

  const categoryOptions = computed(() => {
    const options = [{ label: 'Все категории', value: null }]
    if (productStore.categories && Array.isArray(productStore.categories)) {
      productStore.categories.forEach(cat => {
        options.push({ label: cat.name, value: cat.slug })
      })
    }
    return options
  })

  const fetchFilteredProducts = async () => {
    const params = {}

    if (selectedCategorySlug.value) {
      params.category = selectedCategorySlug.value
    }

    if (searchQuery.value && searchQuery.value.trim() !== '') {
      params.search = searchQuery.value.trim()
    }

    await productStore.fetchProducts(params)
  }

  watch([searchQuery, selectedCategorySlug], () => {
    fetchFilteredProducts()
  })

  const loadCatalogData = async () => {
    try {
      if (typeof productStore.fetchCategories === 'function') {
        await productStore.fetchCategories()
      }
    } catch (e) {
      console.error('Не удалось загрузить категории в стор:', e)
    }
    await fetchFilteredProducts()
  }

  onMounted(() => {
    loadCatalogData()
  })

  const handleLogout = () => {
    authStore.logout()
    router.push('/login')
  }

  const addToCart = (product) => {
    console.log(`Добавлено: ${product.name}`)
  }
</script>

<style scoped>
  .catalog-page {
    width: 100%;
    min-height: 100vh;
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    padding: 35px 25px;
  }

  .catalog-container {
    max-width: 1200px;
    margin: 0 auto;
  }

  .welcome-banner {
    margin-top: 15px;
    margin-bottom: 25px;
  }

  .welcome-banner h1 {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0;
    color: #0f172a;
  }

  .welcome-banner p {
    font-size: 16px;
    color: #64748b;
    margin: 0;
  }

  .products-grid, .loading-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 24px;
  }

  @media (min-width: 1024px) {
    .products-grid, .loading-grid {
      grid-template-columns: repeat(4, 1fr);
    }
  }

  .skeleton-card {
    background: #ffffff;
    border: 1px solid #eef2f6;
    border-radius: 16px;
    padding: 12px;
    display: flex;
    flex-direction: column;
  }

  .skeleton-image {
    height: 240px;
    background: #f1f5f9;
    border-radius: 10px;
    margin-bottom: 12px;
  }

  .skeleton-text {
    background: #f1f5f9;
    border-radius: 4px;
    margin-bottom: 8px;
  }

    .skeleton-text.line-1 {
      width: 75%;
      height: 16px;
    }

    .skeleton-text.line-2 {
      width: 45%;
      height: 14px;
      margin-top: auto;
    }

  .error-container, .empty-catalog-container {
    text-align: center;
    padding: 60px;
    background: #ffffff;
    border-radius: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
    border: 1px solid #eef2f6;
    max-width: 500px;
    margin: 40px auto;
  }

  .error-icon {
    font-size: 40px;
    margin-bottom: 16px;
  }

  .error-container h3 {
    margin: 0 0 8px 0;
    font-size: 20px;
  }

  .error-container p, .empty-catalog-container p {
    color: #64748b;
    margin: 0 0 24px 0;
  }

  .btn-retry {
    padding: 12px 24px;
    background: #0f172a;
    color: #fff;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
  }

  .btn-retry:hover {
    background: #00b4d8;
  }

</style>
