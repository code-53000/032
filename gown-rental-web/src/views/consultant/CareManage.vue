<template>
  <div class="care-manage">
    <div class="page-header">
      <h2>洗护流转管理</h2>
      <el-button type="primary" @click="showDialog()">新增洗护记录</el-button>
    </div>
    <el-table :data="cares" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="礼服" width="120">
        <template #default="{ row }">礼服 #{{ row.gown_id }}</template>
      </el-table-column>
      <el-table-column prop="care_type" label="类型" width="100">
        <template #default="{ row }">{{ careTypeText(row.care_type) }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="careStatusTag(row.status)" size="small">{{ careStatusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="started_at" label="开始时间" width="170">
        <template #default="{ row }">{{ row.started_at || '-' }}</template>
      </el-table-column>
      <el-table-column prop="completed_at" label="完成时间" width="170">
        <template #default="{ row }">{{ row.completed_at || '-' }}</template>
      </el-table-column>
      <el-table-column prop="cost" label="费用" width="90">
        <template #default="{ row }">¥{{ row.cost }}</template>
      </el-table-column>
      <el-table-column prop="notes" label="备注" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" size="small" type="primary" text @click="startCare(row.id)">开始</el-button>
          <el-button v-if="row.status === 'in_progress'" size="small" type="success" text @click="completeCare(row.id)">完成</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="新增洗护记录" width="450px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="礼服ID">
          <el-input-number v-model="form.gown_id" :min="1" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.care_type">
            <el-option label="清洗" value="cleaning" />
            <el-option label="维修" value="repair" />
            <el-option label="熨烫" value="ironing" />
            <el-option label="检查" value="inspection" />
          </el-select>
        </el-form-item>
        <el-form-item label="费用">
          <el-input-number v-model="form.cost" :min="0" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.notes" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCare">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getGownCares, createGownCare, updateGownCare } from '../../api/gownCares'

const cares = ref([])
const dialogVisible = ref(false)
const form = ref({ gown_id: 1, care_type: 'cleaning', cost: 0, notes: '' })

onMounted(() => loadCares())

async function loadCares() {
  const res = await getGownCares({ limit: 100 })
  cares.value = res.data
}

async function saveCare() {
  await createGownCare(form.value)
  ElMessage.success('添加成功')
  dialogVisible.value = false
  loadCares()
}

async function startCare(id) {
  await updateGownCare(id, { status: 'in_progress' })
  ElMessage.success('已开始')
  loadCares()
}

async function completeCare(id) {
  await updateGownCare(id, { status: 'completed' })
  ElMessage.success('已完成')
  loadCares()
}

function careTypeText(s) {
  const m = { cleaning: '清洗', repair: '维修', ironing: '熨烫', inspection: '检查' }
  return m[s] || s
}
function careStatusTag(s) {
  const m = { pending: 'warning', in_progress: '', completed: 'success' }
  return m[s] || 'info'
}
function careStatusText(s) {
  const m = { pending: '待处理', in_progress: '进行中', completed: '已完成' }
  return m[s] || s
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h2 { margin: 0; color: #2c3e50; }
</style>
