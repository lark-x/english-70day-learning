import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../features/home/HomeView.vue'
import TodayView from '../features/today/TodayView.vue'
import MaterialsView from '../features/materials/MaterialsView.vue'
import MistakesView from '../features/mistakes/MistakesView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/today',
      name: 'today',
      component: TodayView
    },
    {
      path: '/materials',
      name: 'materials',
      component: MaterialsView
    },
    {
      path: '/mistakes',
      name: 'mistakes',
      component: MistakesView
    }
  ]
})

export default router
