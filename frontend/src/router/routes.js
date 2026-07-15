import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    redirect: () => {
      const authStore = useAuthStore()

      if (authStore.isStaff) {
        return '/admin'
      }
      return '/catalog'
    }
  },
  {
    path: '/login',
    component: () => import('@/pages/AuthPage.vue'),
    props: { defaultIsLogin: true }
  },
  {
    path: '/register',
    component: () => import('@/pages/AuthPage.vue'),
    props: { defaultIsLogin: false }
  },
  {
    path: '/admin',
    component: () => import('@/pages/AdminPage.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/catalog',
    component: () => import('@/pages/CatalogPage.vue'),
  },
  {
    path: '/product/:id',
    component: () => import('@/pages/ProductPage.vue'),
    name: 'product-detail',
    meta: { disallowStaff: true } 
  },
  {
    path: '/cart',
    component: () => import('@/pages/CartPage.vue'),
    meta: { requiresBuyer: true } 
  },
  {
    path: '/checkout',
    component: () => import('@/pages/CheckoutPage.vue'),
    meta: { requiresBuyer: true } 
  },
  {
    path: '/orders',
    component: () => import('@/pages/OrdersPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('@/pages/ErrorNotFound.vue'),
  }
]

export default routes
