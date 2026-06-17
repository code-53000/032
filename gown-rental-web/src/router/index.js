import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

import Layout from '../components/Layout.vue'
import Login from '../views/Login.vue'

import BrideGownList from '../views/bride/GownList.vue'
import BrideGownDetail from '../views/bride/GownDetail.vue'
import MyAppointments from '../views/bride/MyAppointments.vue'
import MyRentals from '../views/bride/MyRentals.vue'

import GownManage from '../views/consultant/GownManage.vue'
import AppointmentSchedule from '../views/consultant/AppointmentSchedule.vue'
import RentalManage from '../views/consultant/RentalManage.vue'
import CareManage from '../views/consultant/CareManage.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  {
    path: '/',
    component: Layout,
    redirect: '/gowns',
    children: [
      { path: 'gowns', name: 'GownList', component: BrideGownList },
      { path: 'gowns/:id', name: 'GownDetail', component: BrideGownDetail },
      { path: 'my-appointments', name: 'MyAppointments', component: MyAppointments },
      { path: 'my-rentals', name: 'MyRentals', component: MyRentals },
      { path: 'manage/gowns', name: 'GownManage', component: GownManage, meta: { consultant: true } },
      { path: 'manage/appointments', name: 'AppointmentSchedule', component: AppointmentSchedule, meta: { consultant: true } },
      { path: 'manage/rentals', name: 'RentalManage', component: RentalManage, meta: { consultant: true } },
      { path: 'manage/cares', name: 'CareManage', component: CareManage, meta: { consultant: true } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const store = useUserStore()
  if (to.path !== '/login' && !store.isLoggedIn) {
    return next('/login')
  }
  if (to.path === '/login' && store.isLoggedIn) {
    return next('/')
  }
  if (to.meta?.consultant && store.isBride) {
    return next('/gowns')
  }
  if (store.isLoggedIn && !store.user) {
    await store.fetchUser()
  }
  next()
})

export default router
