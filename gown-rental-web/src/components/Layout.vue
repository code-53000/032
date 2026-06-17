<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="aside">
      <div class="logo">👰 婚纱馆</div>
      <el-menu
        :default-active="route.path"
        router
        background-color="#2c3e50"
        text-color="#ecf0f1"
        active-text-color="#f39c12"
      >
        <el-menu-item index="/gowns">
          <el-icon><Goods /></el-icon>
          <span>礼服浏览</span>
        </el-menu-item>
        <el-menu-item index="/my-appointments">
          <el-icon><Calendar /></el-icon>
          <span>我的试纱</span>
        </el-menu-item>
        <el-menu-item index="/my-rentals">
          <el-icon><Document /></el-icon>
          <span>我的租赁</span>
        </el-menu-item>
        <template v-if="userStore.isConsultant">
          <el-divider style="margin: 12px 0; border-color: #5d6d7e" />
          <el-menu-item index="/manage/gowns">
            <el-icon><Box /></el-icon>
            <span>礼服档案</span>
          </el-menu-item>
          <el-menu-item index="/manage/appointments">
            <el-icon><Timer /></el-icon>
            <span>试纱档期</span>
          </el-menu-item>
          <el-menu-item index="/manage/rentals">
            <el-icon><List /></el-icon>
            <span>租赁管理</span>
          </el-menu-item>
          <el-menu-item index="/manage/cares">
            <el-icon><MagicStick /></el-icon>
            <span>洗护流转</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span class="header-title">婚纱馆租赁管理系统</span>
        <div class="header-right">
          <el-tag :type="userStore.isConsultant ? 'warning' : 'success'" effect="dark" size="small">
            {{ userStore.isConsultant ? '顾问' : '新娘' }}
          </el-tag>
          <span class="user-name">{{ userStore.user?.name }}</span>
          <el-button type="danger" text size="small" @click="handleLogout">退出</el-button>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.aside {
  background-color: #2c3e50;
  overflow-y: auto;
}
.logo {
  color: #f39c12;
  font-size: 22px;
  font-weight: bold;
  text-align: center;
  padding: 20px 0 10px;
  letter-spacing: 2px;
}
.header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}
.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.user-name {
  color: #606266;
  font-size: 14px;
}
.main {
  background: #f5f7fa;
  overflow-y: auto;
}
</style>
