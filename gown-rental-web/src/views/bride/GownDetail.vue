<template>
  <div class="gown-detail" v-if="gown">
    <el-page-header @back="$router.back()" content="礼服详情" />
    <el-row :gutter="30" style="margin-top:20px">
      <el-col :span="10">
        <img :src="gown.image_url" class="detail-img" :alt="gown.name" />
      </el-col>
      <el-col :span="14">
        <h2>{{ gown.name }}</h2>
        <el-descriptions :column="2" border style="margin-top:16px">
          <el-descriptions-item label="设计师">{{ gown.designer }}</el-descriptions-item>
          <el-descriptions-item label="款式">{{ styleLabel(gown.style) }}</el-descriptions-item>
          <el-descriptions-item label="颜色">{{ gown.color }}</el-descriptions-item>
          <el-descriptions-item label="尺码">{{ gown.size }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="statusTag(gown.status)">{{ statusLabel(gown.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="日租金">
            <span class="price">¥{{ gown.rental_price }}</span>
          </el-descriptions-item>
        </el-descriptions>
        <p class="desc-text">{{ gown.description }}</p>

        <el-divider>预约试纱</el-divider>
        <el-form :model="aptForm" label-width="80px" inline>
          <el-form-item label="日期">
            <el-date-picker v-model="aptForm.date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" />
          </el-form-item>
          <el-form-item label="开始">
            <el-time-select v-model="aptForm.start" :max-time="aptForm.end" start="09:00" step="00:30" end="20:00" placeholder="开始时间" />
          </el-form-item>
          <el-form-item label="结束">
            <el-time-select v-model="aptForm.end" :min-time="aptForm.start" start="09:00" step="00:30" end="20:00" placeholder="结束时间" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="bookAppointment" :disabled="gown.status === 'retired'">预约试纱</el-button>
          </el-form-item>
        </el-form>

        <el-divider>租赁下单</el-divider>
        <el-form :model="rentalForm" label-width="80px" inline>
          <el-form-item label="取纱日期">
            <el-date-picker v-model="rentalForm.pickup" type="date" placeholder="取纱日期" value-format="YYYY-MM-DD" />
          </el-form-item>
          <el-form-item label="还纱日期">
            <el-date-picker v-model="rentalForm.return_" type="date" placeholder="还纱日期" value-format="YYYY-MM-DD" />
          </el-form-item>
          <el-form-item>
            <el-button type="warning" @click="createRental" :disabled="gown.status === 'retired'">租赁下单</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getGown } from '../../api/gowns'
import { createAppointment } from '../../api/appointments'
import { createRentalOrder } from '../../api/rentalOrders'

const route = useRoute()
const gown = ref(null)
const aptForm = ref({ date: '', start: '', end: '' })
const rentalForm = ref({ pickup: '', return_: '' })

onMounted(async () => {
  const res = await getGown(route.params.id)
  gown.value = res.data
})

async function bookAppointment() {
  if (!aptForm.value.date || !aptForm.value.start || !aptForm.value.end) {
    return ElMessage.warning('请填写完整的试纱时间')
  }
  await createAppointment({
    gown_id: gown.value.id,
    appointment_date: aptForm.value.date,
    start_time: aptForm.value.start,
    end_time: aptForm.value.end,
  })
  ElMessage.success('预约成功！')
  aptForm.value = { date: '', start: '', end: '' }
}

async function createRental() {
  if (!rentalForm.value.pickup || !rentalForm.value.return_) {
    return ElMessage.warning('请选择取还日期')
  }
  await createRentalOrder({
    gown_id: gown.value.id,
    pickup_date: rentalForm.value.pickup,
    return_date: rentalForm.value.return_,
  })
  ElMessage.success('租赁下单成功！')
  rentalForm.value = { pickup: '', return_: '' }
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
.detail-img { width: 100%; border-radius: 10px; }
h2 { margin: 0; color: #2c3e50; }
.price { color: #e74c3c; font-weight: 600; font-size: 18px; }
.desc-text { color: #606266; line-height: 1.8; margin-top: 16px; }
</style>
