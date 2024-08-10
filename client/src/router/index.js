import { createRouter, createWebHistory } from 'vue-router'
// import HelloWorld from '../components/HelloWorld.vue'
import home from '../components/home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
      // props: { sampletime: "-120" }
    }
  ]
})

export default router
