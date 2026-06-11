import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' },
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '工作台', icon: 'Odometer' },
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('@/views/Tasks.vue'),
        meta: { title: '任务管理', icon: 'List' },
      },
      {
        path: 'documents',
        name: 'Documents',
        component: () => import('@/views/Documents.vue'),
        meta: { title: '文件管理', icon: 'Folder' },
      },
      {
        path: 'members',
        name: 'Members',
        component: () => import('@/views/Members.vue'),
        meta: { title: '成员管理', icon: 'User' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫 — 未登录跳转到登录页 (开发阶段暂时跳过)
// router.beforeEach((to, from, next) => {
//   const token = localStorage.getItem('token')
//   if (to.path !== '/login' && !token) {
//     next('/login')
//   } else {
//     next()
//   }
// })

export default router
