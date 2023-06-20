import { createRouter, createWebHistory } from 'vue-router'

const KG = ()=> import('../views/KGView.vue')
const QA = ()=>import('../views/QAView.vue')

const routes = [
  { path: '/', redirect: '/kg' },
  { path: '/kg', component: KG },
  { path: '/qa', component: QA },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
