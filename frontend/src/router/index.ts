import { createRouter, createWebHistory } from 'vue-router'

import Welcome from '@/views/Welcome.vue'
import Categories from '@/views/Categories.vue'
import Create from '@/views/CreateForm.vue'

const routes = [
  {
    path: '/',
    name: 'welcome',
    component: Welcome 
  },
  {
    path: '/categories',
    name: 'categories',
    replace: true,
   component: Categories
  },
  {
    path: '/create',
    name: 'create folders',
    replace: true,
    component: Create
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
