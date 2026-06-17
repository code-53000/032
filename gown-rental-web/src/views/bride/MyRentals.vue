<template>
  <div class="my-rentals">
    <h2>我的租赁订单</h2>
    <el-table :data="orders" stripe style="margin-top:16px">
      <el-table-column prop="id" label="编号" width="70" />
      <el-table-column label="礼服" width="140">
        <template #default="{ row }">礼服 #{{ row.gown_id }}</template>
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
      <el-table-column prop="notes" label="备注" />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" type="danger" size="small" text @click="cancelOrder(row.id)">取消</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getRentalOrders, cancelRentalOrder } from '../../api/rentalOrders'

const orders = ref([])

onMounted(() => loadOrders())

async function loadOrders() {
  const res = await getRentalOrders({ limit: 100 })
  orders.value = res.data
}

async function cancelOrder(id) {
  await ElMessageBox.confirm('确定取消该租赁订单？', '提示', { type: 'warning' })
  await cancelRentalOrder(id)
  ElMessage.success('已取消')
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
