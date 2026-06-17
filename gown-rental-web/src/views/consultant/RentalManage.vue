<template>
  <div class="rental-manage">
    <h2>租赁订单管理</h2>
    <el-table :data="orders" stripe style="margin-top:16px">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="礼服" width="120">
        <template #default="{ row }">礼服 #{{ row.gown_id }}</template>
      </el-table-column>
      <el-table-column label="新娘" width="120">
        <template #default="{ row }">新娘 #{{ row.bride_id }}</template>
      </el-table-column>
      <el-table-column prop="pickup_date" label="取纱日期" width="120" />
      <el-table-column prop="return_date" label="还纱日期" width="120" />
      <el-table-column prop="actual_return_date" label="实际归还" width="120">
        <template #default="{ row }">{{ row.actual_return_date || '-' }}</template>
      </el-table-column>
      <el-table-column prop="total_price" label="总价" width="100">
        <template #default="{ row }">¥{{ row.total_price }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="rentalStatusTag(row.status)" size="small">{{ rentalStatusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" size="small" type="success" text @click="activateOrder(row.id)">激活</el-button>
          <el-button v-if="row.status === 'active'" size="small" type="warning" text @click="returnOrder(row.id)">归还</el-button>
          <el-button v-if="row.status === 'active'" size="small" type="danger" text @click="markOverdue(row.id)">逾期</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getRentalOrders, updateRentalOrder } from '../../api/rentalOrders'

const orders = ref([])

onMounted(() => loadOrders())

async function loadOrders() {
  const res = await getRentalOrders({ limit: 100 })
  orders.value = res.data
}

async function activateOrder(id) {
  await updateRentalOrder(id, { status: 'active' })
  ElMessage.success('已激活')
  loadOrders()
}

async function returnOrder(id) {
  const today = new Date().toISOString().slice(0, 10)
  await updateRentalOrder(id, { status: 'returned', actual_return_date: today })
  ElMessage.success('已归还')
  loadOrders()
}

async function markOverdue(id) {
  await updateRentalOrder(id, { status: 'overdue' })
  ElMessage.success('已标记逾期')
  loadOrders()
}

function rentalStatusTag(s) {
  const m = { pending: 'warning', active: 'success', returned: 'info', overdue: 'danger' }
  return m[s] || 'info'
}
function rentalStatusText(s) {
  const m = { pending: '待取纱', active: '租借中', returned: '已归还', overdue: '逾期' }
  return m[s] || s
}
</script>

<style scoped>
h2 { margin: 0; color: #2c3e50; }
</style>
