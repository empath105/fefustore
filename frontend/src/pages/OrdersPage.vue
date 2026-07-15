<template>
  <div class="orders-page-wrapper q-pa-md" style="min-height: 100vh; background: #fafafa;">
    <div class="orders-container">
      <TopBar :show-filter="false" :minimal="false" />

      <div class="orders-header q-my-xl">
        <h1 class="text-h4 text-weight-bold text-dark q-my-none">Мои заказы</h1>
        <p class="text-subtitle1 text-grey-7 q-mt-xs">История ваших покупок в магазине</p>
      </div>
      <div v-if="loading" class="text-center q-pa-xl">
        <q-spinner-dots color="primary" size="40px" />
        <p class="text-grey-6 q-mt-md">Загрузка истории заказов...</p>
      </div>
      <div v-else-if="orders.length === 0" class="empty-orders text-center q-pa-xl bg-white rounded-card bordered-card">
        <q-icon name="receipt_long" size="64px" color="grey-4" />
        <div class="text-h6 text-weight-bold text-dark q-mt-md">Вы еще ничего не заказывали</div>
        <p class="text-grey-6 q-mb-md">Самое время заглянуть в наш каталог!</p>
        <q-btn label="Перейти в каталог" color="primary" unelevated to="/catalog" class="rounded-btn px-lg" />
      </div>
      <div v-else class="orders-list">
        <q-card v-for="order in orders" :key="order.id" flat bordered class="q-mb-md rounded-card order-card">
          <q-expansion-item>
            <template v-slot:header>
              <q-item-section>
                <div class="row items-center justify-between q-col-gutter-sm">
                  <div>
                    <span class="text-weight-bold text-subtitle1 text-dark">Заказ #{{ order.id }}</span>
                    <span class="text-grey-6 text-caption q-ml-md">{{ formatDate(order.created_at || order.created) }}</span>
                  </div>
                  <div class="row items-center gap-md">
                    <q-badge :color="getStatusColor(order.status)" class="q-py-xs q-px-sm text-weight-medium">
                      {{ getStatusLabel(order.status) }}
                    </q-badge>
                    <span class="text-weight-bold text-subtitle1 text-dark text-right min-width-price">
                      {{ order.total_price }} ₽
                    </span>
                  </div>
                </div>
              </q-item-section>
            </template>

            <q-card-section class="bg-grey-1 q-pa-md border-top-divider">
              <div class="text-weight-bold q-mb-sm text-grey-8">Содержимое заказа:</div>

              <div class="order-items-box bg-white q-pa-md rounded-card bordered-card">
                <div v-for="item in order.items" :key="item.id" class="order-item-row q-py-md">
                  <div class="row justify-between items-center no-wrap">
                    <div class="ellipsis q-pr-md">
                      <span class="text-body2 text-weight-medium text-dark">
                        {{ item.product?.name || `Товар #${item.product}` }}
                      </span>
                      <span class="text-grey-5 text-caption q-ml-md">x{{ item.quantity }}</span>
                    </div>
                    <span class="text-body2 text-weight-bold text-dark text-no-wrap">
                      {{ item.price * item.quantity }} ₽
                    </span>
                  </div>
                </div>
              </div>

              <div v-if="currentUserIsStaff" class="admin-actions q-mt-md q-pa-sm bg-amber-1 rounded-card row items-center justify-between">
                <span class="text-caption text-amber-9 text-weight-medium">Панель менеджера:</span>
                <q-btn-dropdown size="sm" color="amber-9" flat label="Изменить статус" icon="edit">
                  <q-list dense>
                    <q-item clickable v-close-popup @click="updateStatus(order.id, 'new')">
                      <q-item-section>Новый</q-item-section>
                    </q-item>
                    <q-item clickable v-close-popup @click="updateStatus(order.id, 'processing')">
                      <q-item-section>В обработке</q-item-section>
                    </q-item>
                    <q-item clickable v-close-popup @click="updateStatus(order.id, 'completed')">
                      <q-item-section>Доставлен</q-item-section>
                    </q-item>
                    <q-item clickable v-close-popup @click="updateStatus(order.id, 'canceled')">
                      <q-item-section>Отменен</q-item-section>
                    </q-item>
                  </q-list>
                </q-btn-dropdown>
              </div>

            </q-card-section>
          </q-expansion-item>
        </q-card>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api } from '../boot/axios'
import TopBar from '../components/TopBar.vue'

const $q = useQuasar()
const loading = ref(true)
const orders = ref([])
const currentUserIsStaff = ref(false)

const fetchOrders = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/orders/')
    orders.value = response.data

  } catch (error) {
    console.error(error)
    $q.notify({ type: 'negative', message: 'Ошибка при чтении истории заказов' })
  } finally {
    loading.value = false
  }
}

const updateStatus = async (orderId, newStatus) => {
  try {
    const response = await api.patch(`/api/orders/${orderId}/`, { status: newStatus })
    const index = orders.value.findIndex(o => o.id === orderId)
    if (index !== -1) {
      orders.value[index].status = response.data.status
    }
    $q.notify({ type: 'positive', message: 'Статус заказа обновлен' })
  } catch (error) {
    $q.notify({ type: 'negative', message: error.response?.data?.error || 'Не удалось изменить статус' })
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'Дата не указана'
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusLabel = (status) => {
  const labels = {
    'new': 'Новый',
    'processing': 'В обработке',
    'completed': 'Выполнен',
    'canceled': 'Отменен'
  }
  return labels[status] || status || 'Обрабатывается'
}

const getStatusColor = (status) => {
  const colors = {
    'new': 'blue',
    'processing': 'orange',
    'completed': 'green',
    'canceled': 'red'
  }
  return colors[status] || 'grey-7'
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
  .orders-container {
    max-width: 1000px;
    margin: 0 auto;
  }

  .rounded-card {
    border-radius: 12px;
  }

  .bordered-card {
    border: 1px solid #eef2f6;
  }

  .order-card {
    overflow: hidden;
    transition: box-shadow 0.2s;
  }

    .order-card:hover {
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }

  .border-top-divider {
    border-top: 1px solid #f1f5f9;
  }

  .order-item-row {
    border-bottom: 1px dashed #f1f5f9;
  }

    .order-item-row:last-child {
      border-bottom: none;
    }

  .min-width-price {
    min-width: 80px;
  }

  .gap-md {
    gap: 12px;
  }
</style>
