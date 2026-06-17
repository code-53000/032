<template>
  <div class="login-page">
    <div class="login-card">
      <h2 class="login-title">👰 婚纱馆租赁管理系统</h2>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" @submit.prevent="handleLogin" label-position="top">
            <el-form-item label="用户名">
              <el-input v-model="loginForm.username" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password />
            </el-form-item>
            <el-button type="primary" :loading="loading" @click="handleLogin" style="width:100%">登 录</el-button>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="注册" name="register">
          <el-form :model="regForm" @submit.prevent="handleRegister" label-position="top">
            <el-form-item label="用户名">
              <el-input v-model="regForm.username" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item label="姓名">
              <el-input v-model="regForm.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="regForm.password" type="password" placeholder="请输入密码" show-password />
            </el-form-item>
            <el-form-item label="角色">
              <el-radio-group v-model="regForm.role">
                <el-radio value="bride">新娘</el-radio>
                <el-radio value="consultant">顾问</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-button type="primary" :loading="loading" @click="handleRegister" style="width:100%">注 册</el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      <div class="demo-hint">
        <el-divider>演示账号</el-divider>
        <p>新娘：bride_demo / 123456</p>
        <p>顾问：consultant_demo / 123456</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login, register } from '../api/auth'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const activeTab = ref('login')
const loading = ref(false)

const loginForm = ref({ username: '', password: '' })
const regForm = ref({ username: '', name: '', password: '', role: 'bride' })

async function handleLogin() {
  loading.value = true
  try {
    const res = await login(loginForm.value)
    userStore.setToken(res.data.access_token)
    await userStore.fetchUser()
    ElMessage.success('登录成功')
    router.push('/')
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  loading.value = true
  try {
    await register(regForm.value)
    ElMessage.success('注册成功，请登录')
    activeTab.value = 'login'
    loginForm.value.username = regForm.value.username
    loginForm.value.password = regForm.value.password
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  width: 400px;
  padding: 32px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
.login-title {
  text-align: center;
  margin-bottom: 24px;
  color: #2c3e50;
  font-size: 22px;
}
.demo-hint {
  margin-top: 16px;
  text-align: center;
  color: #909399;
  font-size: 13px;
}
.demo-hint p {
  margin: 4px 0;
}
</style>
