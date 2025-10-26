import { createRouter, createWebHistory } from "vue-router";
import Home from '@/views/Home'
import Login from '@/views/Login'
import Payed from '@/views/Payed'
import Payment from '@/views/Payment'
import Product from '@/views/Product'

//define the routes
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/product',
    name: 'Product',
    component: Product,
  },
  {
    path: '/payment',
    name: 'Payment',
    component: Payment,
    meta: { requiresAuth: true }
  },
  {
    path: '/payed',
    name: 'Payed',
    component: Payed,
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
})



// navigation guard to check authentication before each route change
router.beforeEach(async (to, _from, next) => {
  const isAuthenticated = store.getters.isAuthenticated

  // if not authenticated but token exists, try to fetch user data
  if (!isAuthenticated && localStorage.getItem('token')) {
    try {
      await store.dispatch('Me') // Fetch current user info from API
    } catch (e) {
      console.warn('Failed to fetch user info with Me():', e)
    }
  }

  // update authentication status after possible user fetch
  const updatedAuth = store.getters.isAuthenticated;

  // If route requires auth and user is not authenticated, redirect to login
  if (to.matched.some(record => record.meta.requiresAuth) && !updatedAuth) {
    return next('/login')
  }
  next()
})


export default router