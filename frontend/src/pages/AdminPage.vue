<template>
  <div class="admin-page">
    <div class="admin-container">
      <TopBar minimal @logout="handleLogout" />

      <q-tabs v-model="activeTab"
              dense
              class="text-grey"
              active-color="primary"
              indicator-color="primary"
              align="left"
              narrow-indicator>
        <q-tab name="products" label="Управление товарами" />
        <q-tab name="categories" label="Управление категориями" />
        <q-tab name="orders" label="Управление заказами" />
      </q-tabs>
      <q-separator />
      <q-tab-panels v-model="activeTab" animated class="bg-transparent q-mt-md">
        <q-tab-panel name="products" class="q-pa-none">
          <div class="row justify-between items-center q-mb-md">
            <h3 class="text-h5 text-weight-bold q-my-none">Список товаров</h3>
            <q-btn color="primary" icon="add" label="Добавить товар" @click="openProductModal(null)" />
          </div>

          <q-table :rows="productStore.products"
                   :columns="productColumns"
                   row-key="id"
                   flat
                   bordered
                   :loading="productStore.loading">
            <template v-slot:body-cell-actions="props">
              <q-td :props="props" class="q-gutter-xs" align="center">
                <q-btn flat round dense color="blue" icon="edit" @click="openProductModal(props.row)" />
                <q-btn flat round dense color="negative" icon="delete" @click="handleDeleteProduct(props.row.id)" />
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>

        <q-tab-panel name="categories" class="q-pa-none">
          <div class="row justify-between items-center q-mb-md">
            <h3 class="text-h5 text-weight-bold q-my-none">Категории товаров</h3>
            <q-btn color="primary" icon="add" label="Добавить категорию" @click="openCategoryModal(null)" />
          </div>

          <q-table :rows="productStore.categories"
                   :columns="categoryColumns"
                   row-key="id"
                   flat
                   bordered
                   :loading="productStore.loading">
            <template v-slot:body-cell-actions="props">
              <q-td :props="props" class="q-gutter-xs" align="center">
                <q-btn flat round dense color="blue" icon="edit" @click="openCategoryModal(props.row)" />
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>

        <q-tab-panel name="orders" class="q-pa-none">
          <h3 class="text-h5 text-weight-bold q-mb-md">Поступившие заказы</h3>

          <q-table :rows="orders"
                   :columns="orderColumns"
                   row-key="id"
                   flat
                   bordered
                   :loading="ordersLoading">
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <q-select v-model="props.row.status"
                          :options="statusOptions"
                          dense
                          outlined
                          emit-value
                          map-options
                          @update:model-value="handleUpdateOrderStatus(props.row)"
                          style="min-width: 210px" />
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>

      </q-tab-panels>
    </div>

    <q-dialog v-model="productModal.show" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ productModal.isEdit ? 'Редактировать товар' : 'Новый товар' }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none q-gutter-md">
          <q-input v-model="productModal.form.name" label="Название товара" dense outlined :rules="[val => !!val || 'Название обязательно']" />
          <q-input v-model.number="productModal.form.price" type="number" label="Цена *" dense outlined prefix="₽" :rules="[val => val > 0 || 'Цена должна быть больше 0']" />
          <q-select v-model="productModal.form.category"
                    :options="categorySelectOptions"
                    option-value="value"
                    option-label="label"
                    emit-value
                    map-options
                    label="Категория *"
                    dense
                    outlined
                    :rules="[val => !!val || 'Выберите категорию']" />
          <q-input v-model="productModal.form.description"
                   type="textarea"
                   label="Описание товара"
                   dense
                   outlined
                   autogrow />
          <q-file v-model="productModal.imageFile"
                  label="Изображение товара"
                  outlined
                  dense
                  accept=".jpg, .jpeg, .png"
                  max-file-size="5242880">
            <template v-slot:prepend>
              <q-icon name="cloud_upload" />
            </template>
          </q-file>
          <q-toggle v-model="productModal.form.is_active"
                    label="Доступен для продажи"
                    color="green" />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Отмена" v-close-popup />
          <q-btn flat color="primary" label="Сохранить" @click="handleSaveProduct" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="categoryModal.show" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ categoryModal.isEdit ? 'Редактировать категорию' : 'Добавить категорию' }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none q-gutter-md">
          <q-input v-model="categoryModal.form.name" label="Название категории" dense outlined />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Отмена" v-close-popup />
          <q-btn flat color="primary" label="Сохранить" @click="handleSaveCategory" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useProductStore } from '../stores/products'
  import { api } from '../boot/axios' 
  import { useAuthStore } from '../stores/auth'
  import TopBar from '../components/TopBar.vue'

  const router = useRouter()
  const productStore = useProductStore()
  const authStore = useAuthStore()

  const activeTab = ref('products')
  const orders = ref([])
  const ordersLoading = ref(false)

  const handleLogout = () => {
    authStore.logout()
    router.push('/login')
  }

  const statusOptions = [
    { label: 'Новый', value: 'new' },
    { label: 'Собирается на складе', value: 'packing' },
    { label: 'Передан службе доставки', value: 'delivering' },
    { label: 'Доставлен', value: 'completed' },
    { label: 'Отменён', value: 'canceled' }
  ]

  const productColumns = [
    { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
    { name: 'name', label: 'Название', field: 'name', align: 'left', sortable: true },
    { name: 'price', label: 'Цена (₽)', field: 'price', align: 'left', sortable: true },
    { name: 'category', required: true, label: 'Категория', align: 'left', field: row => row.category?.name || row.category_name || 'Без категории', sortable: true },
    { name: 'actions', label: 'Действия', field: 'actions', align: 'center' }
  ]

  const categoryColumns = [
    { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
    { name: 'name', label: 'Название', field: 'name', align: 'left', sortable: true },
    { name: 'slug', label: 'Слаг (Slug)', field: 'slug', align: 'left' },
    { name: 'actions', label: 'Действия', field: 'actions', align: 'center' }
  ]

  const orderColumns = [
    { name: 'id', label: '№ Заказа', field: 'id', align: 'left', sortable: true },
    { name: 'user', label: 'Покупатель', field: row => row.user?.username || row.user_id, align: 'left' },
    { name: 'total', label: 'Сумма (₽)', field: 'total_price', align: 'left', sortable: true },
    { name: 'created_at', label: 'Дата заказа', field: row => new Date(row.created_at).toLocaleDateString('ru-RU'), align: 'left' },
    { name: 'status', label: 'Статус выполнения', field: 'status', align: 'center' }
  ]

  const categorySelectOptions = computed(() => {
    if (productStore.categories && Array.isArray(productStore.categories)) {
      return productStore.categories.map(cat => ({ label: cat.name, value: cat.id }))
    }
    return []
  })

  const productModal = ref({
    show: false, isEdit: false,
    form: { id: null, name: '', price: 0, category: null }
  })

  const categoryModal = ref({
    show: false, isEdit: false,
    imageFile: null,
    form: {id: null, name: '', category: null, price: 0, description: '', is_active: true}
  })

  const loadOrders = async () => {
    try {
      ordersLoading.value = true
      const response = await api.get('/api/orders/') 
      orders.value = response.data
    } catch (e) {
      console.error('Ошибка при загрузке списка заказов:', e)
    } finally {
      ordersLoading.value = false
    }
  }

  onMounted(async () => {
    if (typeof productStore.fetchProducts === 'function') await productStore.fetchProducts()
    if (typeof productStore.fetchCategories === 'function') await productStore.fetchCategories()
    await loadOrders()
  })

  const goToCatalog = () => router.push('/catalog')

  const openProductModal = (product = null) => {
    if (product) {
      productModal.value.isEdit = true
      productModal.value.form = { id: product.id, name: product.name, price: product.price, category: product.category?.id || product.category, description: product.description || '', is_active: product.is_active ?? true }
      productModal.value.imageFile = null
    } else {
      productModal.value.isEdit = false
      productModal.value.form = {
        id: null, name: '', price: null, category: null, description: '', is_active: true
      }
      productModal.value.imageFile = null
    }
    productModal.value.show = true
  }

  const handleSaveProduct = async () => {
    try {
      const formData = new FormData()

      formData.append('name', productModal.value.form.name)
      formData.append('category', productModal.value.form.category)
      formData.append('price', productModal.value.form.price)
      formData.append('description', productModal.value.form.description)
      formData.append('is_active', productModal.value.form.is_active)

      if (productModal.value.imageFile) {
        formData.append('image', productModal.value.imageFile)
      }

      if (productModal.value.isEdit) {
        await api.put(`/api/products/${productModal.value.form.id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      } else {
        await api.post('/api/products/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }

      productModal.value.show = false
      await productStore.fetchProducts() 

    } catch (error) {
      console.error('Ошибка сохранения товара:', error.response?.data || error)
    }
  }

  const handleDeleteProduct = async (id) => {
    if (confirm('Вы уверены, что хотите безвозвратно удалить этот товар?')) {
      try {
        await productStore.deleteProduct(id)
      } catch (e) {
        console.error('Не удалось удалить товар:', e)
      }
    }
  }

  const openCategoryModal = (category = null) => {
    if (category) {
      categoryModal.value.isEdit = true
      categoryModal.value.form = { ...category }
    } else {
      categoryModal.value.isEdit = false
      categoryModal.value.form = { id: null, name: '' }
    }
    categoryModal.value.show = true
  }

  const handleSaveCategory = async () => {
    try {
      if (categoryModal.value.isEdit) {
        await productStore.updateCategory(categoryModal.value.form.id, categoryModal.value.form)
      } else {
        await productStore.createCategory(categoryModal.value.form)
      }
      categoryModal.value.show = false
    } catch (e) {
      console.error('Ошибка сохранения категории:', e)
    }
  }

  const handleUpdateOrderStatus = async (order) => {
    try {
      await api.patch(`/api/orders/${order.id}/`, { status: order.status })
      console.log(`Статус заказа #${order.id} изменен на ${order.status}`)
    } catch (e) {
      console.error('Не удалось обновить статус заказа:', e)
    }
  }
</script>

<style scoped>
  .admin-page {
    width: 100%;
    min-height: 100vh;
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    color: #0f172a;
    padding: 35px 25px;
  }

  .admin-container {
    max-width: 1200px;
    margin: 0 auto;
  }

  .admin-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20px;
    margin-bottom: 15px;
    border-bottom: 1px solid #e2e8f0;
  }

  .brand h2 {
    font-size: 24px;
    font-weight: 900;
    margin: 0;
  }

    .brand h2 span {
      color: #00b4d8;
    }

  .btn-logout-admin {
    padding: 10px 18px;
    background: transparent;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    color: #64748b;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-logout-admin:hover {
    background: #f1f5f9;
    color: #0f172a;
  }
</style>
