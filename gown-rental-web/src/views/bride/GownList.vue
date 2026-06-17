<template>
  <div class="gown-list">
    <div class="page-header">
      <h2>礼服浏览</h2>
      <div class="filters">
        <el-select v-model="filters.style" placeholder="款式筛选" clearable @change="loadGowns">
          <el-option label="A字裙" value="A-line" />
          <el-option label="蓬蓬裙" value="ball_gown" />
          <el-option label="鱼尾裙" value="mermaid" />
          <el-option label="修身裙" value="sheath" />
          <el-option label="喇叭裙" value="trumpet" />
          <el-option label="帝国线" value="empire" />
          <el-option label="茶歇裙" value="tea_length" />
        </el-select>
        <el-select v-model="filters.status" placeholder="状态筛选" clearable @change="loadGowns">
          <el-option label="可租" value="available" />
          <el-option label="已租" value="rented" />
          <el-option label="清洗中" value="cleaning" />
          <el-option label="维修中" value="repair" />
        </el-select>
      </div>
    </div>
    <el-row :gutter="20">
      <el-col :span="6" v-for="gown in gowns" :key="gown.id">
        <el-card class="gown-card" shadow="hover" @click="goDetail(gown.id)">
          <img :src="gown.image_url" class="gown-img" :alt="gown.name" />
          <div class="gown-info">
            <h3>{{ gown.name }}</h3>
            <p class="designer">{{ gown.designer }}</p>
            <div class="meta">
              <el-tag size="small" :type="statusTag(gown.status)">{{ statusLabel(gown.status) }}</el-tag>
              <span class="price">¥{{ gown.rental_price }}/天</span>
            </div>
            <p class="desc">{{ gown.description }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <div class="pagination">
      <el-pagination
        v-model:current-page="page"
        :page-size="20"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadGowns"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getGowns } from '../../api/gowns'

const router = useRouter()
const gowns = ref([])
const total = ref(0)
const page = ref(1)
const filters = ref({ style: '', status: '' })

onMounted(() => loadGowns())

async function loadGowns() {
  const params = { skip: (page.value - 1) * 20, limit: 20 }
  if (filters.value.style) params.style = filters.value.style
  if (filters.value.status) params.status = filters.value.status
  const res = await getGowns(params)
  gowns.value = res.data
  total.value = res.data.length >= 20 ? page.value * 20 + 1 : (page.value - 1) * 20 + res.data.length
}

function goDetail(id) {
  router.push(`/gowns/${id}`)
}

function statusTag(s) {
  const map = { available: 'success', rented: 'danger', cleaning: 'warning', repair: 'info', retired: 'info' }
  return map[s] || 'info'
}

function statusLabel(s) {
  const map = { available: '可租', rented: '已租', cleaning: '清洗中', repair: '维修中', retired: '已退役' }
  return map[s] || s
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-header h2 { margin: 0; color: #2c3e50; }
.filters { display: flex; gap: 12px; }
.gown-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}
.gown-card:hover { transform: translateY(-4px); }
.gown-img {
  width: 100%;
  height: 260px;
  object-fit: cover;
  border-radius: 6px;
}
.gown-info h3 { margin: 10px 0 4px; color: #2c3e50; font-size: 16px; }
.designer { color: #909399; font-size: 13px; margin: 0 0 8px; }
.meta { display: flex; justify-content: space-between; align-items: center; }
.price { color: #e74c3c; font-weight: 600; font-size: 15px; }
.desc { color: #606266; font-size: 13px; margin: 8px 0 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.pagination { text-align: center; margin-top: 20px; }
</style>
