import { createRouter, createWebHistory } from 'vue-router';
import { useLoginStore } from '../stores/counter';

import loginVue from '../views/logIn.vue';
import userInfoVue from '../views/userInfo.vue';
import materialManagementVue from '@/views/materialManagement.vue';
import equipmentManagementVue from '@/views/equipmentManagement.vue';
import projectShowVue from '@/views/projectShow.vue';
import projetWriteVue from '@/views/projectWrite.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'login',
      component: loginVue,
    },
    {
      path: '/userInfo',
      name: 'userInfo',
      component: userInfoVue,
    },
    {
      path: '/materialManagement',
      name: 'materialManagement',
      component: materialManagementVue
    },
    {
      path: '/equipmentManagement',
      name: 'equipmentManagement',
      component: equipmentManagementVue
    },
    {
      path: '/projectShow',
      name: 'projectShow',
      component: projectShowVue
    },
    {
      path: '/projetWrite',
      name: 'projetWrite',
      component: projetWriteVue
    },

    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
})


router.beforeEach((to) => {
  const isLogin = useLoginStore().notarizeLogin()
  if (to.path === '/login') {
    if (isLogin) {
      return { path: '/userInfo' }
    }
  }
  if (to.path === '/userInfo') {
    if (isLogin === false) {
      return { path: '/login' }
    }
  }
})

export default router
