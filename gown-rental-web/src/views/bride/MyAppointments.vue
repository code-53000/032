<template>
  <div class="my-appointments">
    <h2>我的试纱预约</h2>
    <el-table :data="appointments" stripe style="margin-top:16px">
      <el-table-column prop="id" label="编号" width="70" />
      <el-table-column label="礼服" width="140">
        <template #default="{ row }">礼服 #{{ row.gown_id }}</template>
      </el-table-column>
      <el-table-column prop="appointment_date" label="预约日期" width="120" />
      <el-table-column label="时段" width="140">
        <template #default="{ row }">{{ row.start_time?.slice(0,5) }} - {{ row.end_time?.slice(0,5) }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="aptStatusTag(row.status)" size="small">{{ aptStatusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="notes" label="备注" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending' || row.status === 'confirmed'" type="danger" size="small" text @click="cancelApt(row.id)">取消</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAppointments, cancelAppointment } from '../../api/appointments'

const appointments = ref([])

onMounted(() => loadAppointments())

async function loadAppointments() {
  const res = await getAppointments({ limit: 100 })
  appointments.value = res.data
}

async function cancelApt(id) {
  await ElMessageBox.confirm('确定取消该预约？', '提示', { type: 'warning' })
  await cancelAppointment(id)
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
