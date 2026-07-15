<template>
  <div class="checkout-page-wrapper q-pa-md" style="min-height: 100vh; background: #fafafa;">
    <div class="checkout-container">

      <div class="checkout-header q-mb-lg">
        <h1 class="text-h4 text-weight-bold text-dark q-my-none">Оформление заказа</h1>
        <p class="text-subtitle1 text-grey-7 q-mt-xs">Пожалуйста, проверьте ваши данные перед отправкой</p>
      </div>

      <q-form @submit.prevent="onSubmit" class="row q-col-gutter-lg">

        <div class="col-12 col-md-8">
          <q-card flat bordered class="q-pa-md q-mb-md rounded-card">
            <q-card-section>
              <div class="text-h6 text-weight-bold q-mb-md">Данные получателя</div>

              <div class="row q-col-gutter-md">
                <q-input v-model="form.name"
                         label="Имя и фамилия *"
                         outlined
                         class="col-12 col-sm-6"
                         :rules="[val => !!val || 'Это поле обязательно для заполнения']" />
                <q-input v-model="form.phone"
                         label="Телефон *"
                         outlined
                         mask="+7 (###) ###-##-##"
                         unmasked-value
                         class="col-12 col-sm-6"
                         :rules="[
                         val=>
                  !!val || 'Это поле обязательно для заполнения',
                  val => val.length === 10 || 'Введите корректный номер телефона'
                  ]"
                  />
                  <q-input v-model="form.email"
                           label="Email *"
                           outlined
                           type="email"
                           class="col-12"
                           :rules="[
                           val=>
                    !!val || 'Это поле обязательно для заполнения',
                    val => /.+@.+\..+/.test(val) || 'Введите корректный email'
                    ]"
                    />
              </div>
            </q-card-section>
          </q-card>

          <q-card flat bordered class="q-pa-md q-mb-md rounded-card">
            <q-card-section>
              <div class="text-h6 text-weight-bold q-mb-md">Адрес доставки</div>

              <div class="row q-col-gutter-md">
                <q-input v-model="form.address"
                         label="Город, улица, дом, квартира *"
                         outlined
                         class="col-12"
                         :rules="[val => !!val || 'Укажите адрес доставки']" />
                <q-input v-model="form.postalCode"
                         label="Почтовый индекс"
                         outlined
                         mask="######"
                         class="col-12 col-sm-6" />
              </div>
            </q-card-section>
          </q-card>

          <q-card flat bordered class="q-pa-md rounded-card">
            <q-card-section>
              <div class="text-h6 text-weight-bold q-mb-sm">Способ оплаты</div>

              <q-option-group v-model="form.paymentMethod"
                              :options="paymentOptions"
                              color="primary"
                              class="payment-options-group" />
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-4">
          <div class="summary-sticky-card">
            <h3 class="summary-title">Ваш заказ</h3>

            <div class="checkout-items-list q-mb-md">
              <div v-for="item in cartStore.items" :key="item.id" class="checkout-item-mini">
                <div class="item-mini-info">
                  <span class="item-mini-name">{{ item.name }}</span>
                  <span class="item-mini-qty">x{{ item.quantity }}</span>
                </div>
                <span class="item-mini-price">{{ item.price * item.quantity }} ₽</span>
              </div>
            </div>

            <hr class="summary-divider" />

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

            <button type="submit" class="btn-confirm-order" :disabled="loading">
              <span v-if="loading">Оформление...</span>
              <span v-else>Подтвердить заказ</span>
            </button>
          </div>
        </div>

      </q-form>

      <q-dialog v-model="showSuccessDialog" persistent>
        <q-card class="dialog-success-card q-pa-lg text-center">
          <q-card-section class="q-pt-none">
            <div class="success-icon q-mx-auto q-mb-md">🎉</div>
            <div class="text-h5 text-weight-bold text-dark q-mb-sm">Заказ успешно оформлен!</div>
            <p class="text-body1 text-grey-7">Номер вашего заказа: <strong class="text-primary">#{{ successData.id }}</strong></p>
            <p class="text-body2 text-grey-6">Мы свяжемся с вами по указанному телефону для подтверждения деталей доставки.</p>
          </q-card-section>

          <q-card-actions align="center">
            <q-btn label="Вернуться на главную" color="primary" unelevated class="full-width rounded-btn" @click="goHome" />
          </q-card-actions>
        </q-card>
      </q-dialog>

    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useQuasar } from 'quasar' 
  import { useCartStore } from '../stores/cart'
  import { api } from '../boot/axios' 

  const router = useRouter()
  const $q = useQuasar() 
  const cartStore = useCartStore()

  const loading = ref(false)
  const showSuccessDialog = ref(false)
  const successData = ref({ id: '' })

  const form = ref({
    name: '',
    phone: '',
    email: '',
    address: '',
    postalCode: '',
    paymentMethod: 'card'
  })

  const paymentOptions = [
    { label: 'Оплата картой онлайн', value: 'card' },
    { label: 'Оплата при получении (наличные или карта)', value: 'cash_on_delivery' }
  ]

  const onSubmit = async () => {
    if (cartStore.items.length === 0) {
      $q.notify({
        type: 'warning',
        message: 'Ваша корзина пуста. Нечего оформлять!'
      })
      return
    }

    loading.value = true

    try {
      const orderPayload = {
        name: form.value.name,
        phone: form.value.phone,
        email: form.value.email,
        address: form.value.address,
        postal_code: form.value.postalCode,
        payment_method: form.value.paymentMethod,
        items: cartStore.items.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        }))
      }
      const response = await api.post('/api/orders/', orderPayload)

      const orderId = response.data.id || response.data.order_id || '777'
      successData.value = { id: orderId }

      showSuccessDialog.value = true

      if (typeof cartStore.clearCart === 'function') {
        cartStore.clearCart()
      } else {
        cartStore.items = []
      }

    } catch (error) {
      console.error('Ошибка создания заказа:', error)
      $q.notify({
        type: 'negative',
        message: error.response?.data?.detail || 'Ошибка при создании заказа. Проверьте адрес API.'
      })
    } finally { 
      loading.value = false
    }
  }

  const goHome = () => {
    showSuccessDialog.value = false
    router.push('/catalog')
  }
</script>

<style scoped>
  .checkout-container {
    max-width: 1200px;
    margin: 0 auto;
  }

  .rounded-card {
    border-radius: 16px;
  }

  .payment-options-group {
    font-size: 15px;
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

  .checkout-items-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    max-height: 200px;
    overflow-y: auto;
  }

  .checkout-item-mini {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
  }

  .item-mini-info {
    display: flex;
    gap: 8px;
    color: #475569;
  }

  .item-mini-name {
    font-weight: 500;
  }

  .item-mini-qty {
    color: #94a3b8;
  }

  .item-mini-price {
    font-weight: 600;
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

  .btn-confirm-order {
    width: 100%;
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

    .btn-confirm-order:hover:not(:disabled) {
      background: #00b4d8;
      box-shadow: 0 8px 24px rgba(0, 180, 216, 0.25);
    }

    .btn-confirm-order:disabled {
      background: #94a3b8;
      cursor: not-allowed;
    }

  .dialog-success-card {
    min-width: 400px;
    border-radius: 20px;
  }

  .success-icon {
    font-size: 64px;
    line-height: 1;
  }

  .rounded-btn {
    border-radius: 10px;
    padding: 10px 0;
  }
</style>
