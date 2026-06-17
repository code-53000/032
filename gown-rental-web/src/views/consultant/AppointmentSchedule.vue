<template>
  <div class="appointment-schedule">
    <h2>试纱档期管理</h2>
    <el-table :data="appointments" stripe style="margin-top:16px">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="礼服" width="120">
        <template #default="{ row }">礼服 #{{ row.gown_id }}</template>
      </el-table-column>
      <el-table-column label="新娘" width="120">
        <template #default="{ row }">新娘 #{{ row.bride_id }}</template>
      </el-table-column>
      <el-table-column prop="appointment_date" label="日期" width="120" />
      <el-table-column label="时段" width="140">
        <template #default="{ row }">{{ row.start_time?.slice(0,5) }} - {{ row.end_time?.slice(0,5) }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="aptStatusTag(row.status)" size="small">{{ aptStatusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="notes" label="备注" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" size="small" type="success" text @click="confirmApt(row.id)">确认</el-button>
          <el-button v-if="row.status === 'confirmed'" size="small" type="primary" text @click="completeApt(row.id)">完成</el-button>
          <el-button v-if="row.status !== 'cancelled' && row.status !== 'completed'" size="small" type="danger" text @click="cancelApt(row.id)">取消</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getAppointments, updateAppointment } from '../../api/appointments'

const appointments = ref([])

onMounted(() => loadAppointments())

async function loadAppointments() {
  const res = await getAppointments({ limit: 100 })
  appointments.value = res.data
}

async function confirmApt(id) {
  await updateAppointment(id, { status: 'confirmed' })
  ElMessage.success('已确认')
  loadAppointments()
}

async function completeApt(id) {
  await updateAppointment(id, { status: 'completed' })
  ElMessage.success('已完成')
  loadAppointments()
}

async function cancelApt(id) {
  await updateAppointment(id, { status: 'cancelled' })
  ElMessage.success('已取消')
  loadAppointments()
}

function aptStatusTag(s) {
  const m = { pending: 'warning', confirmed: 'success', cancelled: 'info', completed: '' }
  return m[s] || 'info'
}
function aptStatusText(s) {
  const m = { pending: '待确认', confirmed: '已确认', cancelled: '已取消', completed: '已完成' }
  return m[s] || s
}
</script>

<style scoped>
h2 { margin: 0; color: #2c3e50; }
</style>
