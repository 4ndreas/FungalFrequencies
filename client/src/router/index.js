import { createRouter, createWebHistory } from 'vue-router'
import home from '../components/home.vue'
import single from '../components/single.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    { path: '/single', component: single },
  ]
})

export default router
