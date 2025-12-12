import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NeighborhoodDetailView from '../views/NeighborhoodDetailView.vue'
import AboutView from '../views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: 'Sound City - Münster Livability Index' }
    },
    {
      path: '/neighborhood/:id',
      name: 'neighborhood-detail',
      component: NeighborhoodDetailView,
      meta: { title: 'Neighborhood Details - Sound City' }
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: { title: 'About - Sound City' }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

// Update page title
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Sound City'
  next()
})

export default router