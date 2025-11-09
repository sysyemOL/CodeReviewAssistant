import { createRouter, createWebHistory } from 'vue-router'
import PortalPage from '@/views/PortalPage.vue'
import ReviewWorkspace from '@/views/ReviewWorkspace.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'portal',
      component: PortalPage,
      meta: {
        title: "Liu Shuo's 雷客AI应用研发挑战赛作品"
      }
    },
    {
      path: '/workspace',
      name: 'workspace',
      component: ReviewWorkspace,
      meta: {
        title: 'AI代码Review助手'
      }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router

