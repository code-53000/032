<template>
  <div class="gown-manage">
    <div class="page-header">
      <h2>礼服档案管理</h2>
      <el-button type="primary" @click="showDialog()">新增礼服</el-button>
    </div>
    <el-table :data="gowns" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="名称" width="130" />
      <el-table-column prop="designer" label="设计师" width="130" />
      <el-table-column prop="style" label="款式" width="100">
        <template #default="{ row }">{{ styleLabel(row.style) }}</template>
      </el-table-column>
      <el-table-column prop="color" label="颜色" width="90" />
      <el-table-column prop="size" label="尺码" width="70" />
      <el-table-column prop="rental_price" label="日租金" width="90">
        <template #default="{ row }">¥{{ row.rental_price }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusTag(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" text type="primary" @click="showDialog(row)">编辑</el-button>
          <el-button size="small" text type="danger" @click="retire(row.id)">退役</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editingGown ? '编辑礼服' : '新增礼服'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="设计师"><el-input v-model="form.designer" /></el-form-item>
        <el-form-item label="款式">
          <el-select v-model="form.style">
            <el-option label="A字裙" value="A-line" />
            <el-option label="蓬蓬裙" value="ball_gown" />
            <el-option label="鱼尾裙" value="mermaid" />
            <el-option label="修身裙" value="sheath" />
            <el-option label="喇叭裙" value="trumpet" />
            <el-option label="帝国线" value="empire" />
            <el-option label="茶歇裙" value="tea_length" />
          </el-select>
        </el-form-item>
        <el-form-item label="颜色"><el-input v-model="form.color" /></el-form-item>
        <el-form-item label="尺码"><el-input v-model="form.size" /></el-form-item>
        <el-form-item label="日租金"><el-input-number v-model="form.rental_price" :min="0" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveGown">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getGowns, createGown, updateGown, retireGown } from '../../api/gowns'

const gowns = ref([])
const dialogVisible = ref(false)
const editingGown = ref(null)
const form = ref({ name: '', designer: '', style: 'A-line', color: '白色', size: 'M', rental_price: 3000, description: '' })

onMounted(() => loadGowns())

async function loadGowns() {
  const res = await getGowns({ limit: 100 })
  gowns.value = res.data
}

function showDialog(gown = null) {
  editingGown.value = gown
  if (gown) {
    form.value = { name: gown.name, designer: gown.designer, style: gown.style, color: gown.color, size: gown.size, rental_price: gown.rental_price, description: gown.description }
  } else {
    form.value = { name: '', designer: '', style: 'A-line', color: '白色', size: 'M', rental_price: 3000, description: '' }
  }
  dialogVisible.value = true
}

async function saveGown() {
  if (editingGown.value) {
    await updateGown(editingGown.value.id, form.value)
    ElMessage.success('更新成功')
  } else {
    await createGown(form.value)
    ElMessage.success('添加成功')
  }
  dialogVisible.value = false
  loadGowns()
}

async function retire(id) {
  await ElMessageBox.confirm('确定将该礼服退役？', '提示', { type: 'warning' })
  await retireGown(id)
  ElMessage.success('已退役')
  loadGowns()
}

function styleLabel(s) {
  const m = { 'A-line': 'A字裙', ball_gown: '蓬蓬裙', mermaid: '鱼尾裙', sheath: '修身裙', trumpet: '喇叭裙', empire: '帝国线', tea_length: '茶歇裙' }
  return m[s] || s
}
function statusTag(s) {
  const m = { available: 'success', rented: 'danger', cleaning: 'warning', repair: 'info', retired: 'info' }
  return m[s] || 'info'
}
function statusLabel(s) {
  const m = { available: '可租', rented: '已租', cleaning: '清洗中', repair: '维修中', retired: '已退役' }
  return m[s] || s
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h2 { margin: 0; color: #2c3e50; }
</style>
