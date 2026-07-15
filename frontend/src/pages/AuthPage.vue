<template>
  <div class="background">
    <div class="background-decor">
      <div class="back-sphere sphere-1"></div>
      <div class="back-sphere sphere-2"></div>
    </div>

    <div class="card">
      <div class="fefu-logo">
        <h2>FEFU<span>STORE</span></h2>
        <p v-if="isLogin">Авторизация | Интернет-магазин</p>
        <p v-else>Регистрация нового покупателя</p>
      </div>

      <form v-if="isLogin" @submit.prevent="handleLogin" class="auth-form">
        <div class="input-group">
          <label>Логин</label>
          <input type="text" v-model="loginData.username" required placeholder="nonamelogin" />
        </div>

        <div class="input-group">
          <label>Пароль</label>
          <input type="password" v-model="loginData.password" required placeholder="••••••••" />
        </div>

        <div v-if="errorMessage" class="error-block">
          {{ errorMessage }}
        </div>
        <button type="submit" class="btn">Войти в аккаунт</button>

        <p class="toggle-text">
          Ещё нет аккаунта?
          <span @click="router.push('/register')">Создать аккаунт</span>
        </p>
      </form>

      <form v-else @submit.prevent="handleRegister" class="auth-form">
        <div class="input-group">
          <label>Логин</label>
          <input type="text" v-model="registerData.username" required placeholder="nonamelogin" />
        </div>

        <div class="input-group">
          <label>Email</label>
          <input type="email" v-model="registerData.email" required placeholder="noname@example.com" />
        </div>

        <div class="input-group-row">
          <div class="input-group">
            <label>Имя</label>
            <input type="text" v-model="registerData.first_name" placeholder="Noname" />
          </div>
          <div class="input-group">
            <label>Фамилия</label>
            <input type="text" v-model="registerData.last_name" placeholder="Nonameov" />
          </div>
        </div>

        <div class="input-group">
          <label>Пароль</label>
          <input type="password" v-model="registerData.password" required placeholder="••••••••" />
        </div>

        <div v-if="errorMessage" class="error-block">
          {{ errorMessage }}
        </div>
        <button type="submit" class="btn">Зарегистрироваться</button>

        <p class="toggle-text">
          Уже зарегистрированы?
          <span @click="router.push('/login')">Войти</span>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '../stores/auth'
  import { useCartStore } from '../stores/cart' 
  import { api } from '../boot/axios'

  const props = defineProps({
    defaultIsLogin: { type: Boolean, default: true }
  })

  const router = useRouter()
  const authStore = useAuthStore()
  const cartStore = useCartStore()

  const isLogin = ref(props.defaultIsLogin)
  const errorMessage = ref('')

  watch(() => props.defaultIsLogin, (newVal) => {
    isLogin.value = newVal
    errorMessage.value = ''
  })

  const loginData = ref({ username: '', password: '' })
  const registerData = ref({ username: '', email: '', first_name: '', last_name: '', password: '' })

  const handleLogin = async () => {
    errorMessage.value = ''
    const result = await authStore.login(loginData.value.username, loginData.value.password)

    if (result.success) {
      console.log('Вход успешен через Pinia store!')

      if (authStore.isStaff) {
        router.push('/admin')
      } else {
        await cartStore.loadCart()
        router.push('/catalog')
      }
    } else {
      errorMessage.value = result.message
    }
  }

  const handleRegister = async () => {
    errorMessage.value = ''
    try {
      await api.post('/api/auth/register/', registerData.value)
      console.log('Регистрация успешна!')

      const result = await authStore.login(registerData.value.username, registerData.value.password)
      if (result.success) {
        await cartStore.loadCart()
        router.push('/catalog')
      }
    } catch (error) {
      console.error('Ошибка регистрации:', error.response?.data)
      const errors = error.response?.data

      if (errors && typeof errors === 'object') {
        errorMessage.value = Object.values(errors).flat()[0]
      } else if (typeof errors === 'string') {
        errorMessage.value = errors
      } else {
        errorMessage.value = 'Ошибка при регистрации'
      }
    }
  }
</script>

<style scoped>
  .background {
    position: relative;
    width: 100%;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: radial-gradient(circle at center, #0a2540 0%, #020c1b 100%);
    overflow: hidden;
    font-family: sans-serif;
  }

  .background-decor {
    position: absolute;
    width: 100%;
    height: 100%;
  }

  .back-sphere {
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.4;
  }

  .sphere-1 {
    width: 300px;
    height: 300px;
    background: #00b4d8;
    top: 20%;
    left: 25%;
  }

  .sphere-2 {
    width: 250px;
    height: 250px;
    background: #90e0ef;
    bottom: 20%;
    right: 25%;
  }

  .card {
    position: relative;
    z-index: 10;
    width: 100%;
    max-width: 420px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 24px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
  }

  .fefu-logo {
    text-align: center;
    margin-bottom: 30px;
  }

  .fefu-logo h2 {
    color: #ffffff;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 0;
  }

  .fefu-logo h2 span {
    color: #00b4d8;
  }

  .fefu-logo p {
    color: rgba(255, 255, 255, 0.6);
    font-size: 13px;
    margin-top: 5px;
  }

  .auth-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .input-group-row {
    display: flex;
    gap: 15px;
  }

  .input-group-row .input-group {
    flex: 1;
  }

  .input-group label {
    color: rgba(255, 255, 255, 0.8);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .input-group input {
    width: 100%;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: #ffffff;
    font-size: 15px;
    outline: none;
    transition: all 0.3s ease;
  }

  .input-group input:focus {
    border-color: #00b4d8;
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 10px rgba(0, 180, 216, 0.2);
  }

  .input-group input::placeholder {
    color: rgba(255, 255, 255, 0.3);
  }

  .btn {
    width: 100%;
    padding: 14px;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: #ffffff;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(5px);
    margin-top: 10px;
  }

  .btn:hover {
    background: #00b4d8;
    border-color: #00b4d8;
    box-shadow: 0 0 15px rgba(0, 180, 216, 0.5);
    transform: translateY(-1px);
  }

  .btn:active {
    transform: translateY(1px);
  }

  .toggle-text {
    text-align: center;
    color: rgba(255, 255, 255, 0.5);
    font-size: 14px;
    margin: 0;
  }

  .toggle-text span {
    color: #00b4d8;
    cursor: pointer;
    font-weight: 600;
    text-decoration: underline;
  }

  .toggle-text span:hover {
    color: #90e0ef;
  }

  .error-block {
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #fca5a5;
    padding: 10px 14px;
    border-radius: 10px;
    font-size: 13px;
    text-align: center;
  }
</style>
