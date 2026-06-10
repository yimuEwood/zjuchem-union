<template>
  <div class="dashboard">
    <h3 class="page-heading">工作台</h3>

    <!-- 快速入口 -->
    <el-row :gutter="20" class="quick-actions">
      <el-col :span="6" v-for="item in quickActions" :key="item.path">
        <div class="action-card" @click="router.push(item.path)">
          <el-icon :size="28"><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </div>
      </el-col>
    </el-row>

    <!-- 待办任务 + 统计 -->
    <el-row :gutter="20" class="content-row">
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>待办事项</span>
              <el-button text type="primary" @click="router.push('/tasks')">查看全部</el-button>
            </div>
          </template>
          <el-table :data="recentTasks" style="width: 100%" size="small" v-loading="taskStore.loading">
            <el-table-column prop="title" label="任务" />
            <el-table-column prop="assignee" label="负责人" width="100" />
            <el-table-column prop="deadline" label="截止日期" width="110" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="statusTag(row.status)" size="small">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="never" class="stats-card">
          <template #header><span>工作统计</span></template>
          <div class="stat-item">
            <div class="stat-num">{{ stats.total }}</div>
            <div class="stat-label">总任务数</div>
          </div>
          <div class="stat-item">
            <div class="stat-num" style="color:#67c23a">{{ stats.done }}</div>
            <div class="stat-label">已完成</div>
          </div>
          <div class="stat-item">
            <div class="stat-num" style="color:#e6a23c">{{ stats.doing }}</div>
            <div class="stat-label">进行中</div>
          </div>
          <div class="stat-item">
            <div class="stat-num" style="color:#f56c6c">{{ stats.overdue }}</div>
            <div class="stat-label">已逾期</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近文件 -->
    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="24">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>最近文件</span>
              <el-button text type="primary" @click="router.push('/documents')">文件库</el-button>
            </div>
          </template>
          <div class="recent-files">
            <div v-for="f in recentFiles" :key="f.name" class="file-item">
              <el-icon :size="20"><Document /></el-icon>
              <span class="file-name">{{ f.name }}</span>
              <span class="file-date">{{ f.updatedAt }}</span>
              <span class="file-dept"><el-tag size="small" type="info">{{ f.department }}</el-tag></span>
            </div>
            <el-empty v-if="!recentFiles.length" description="暂无文件" :image-size="60" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '@/store/task'

const router = useRouter()
const taskStore = useTaskStore()

onMounted(() => {
  taskStore.fetchTasks()
})

const quickActions = [
  { label: '新建任务', icon: 'Plus', path: '/tasks' },
  { label: '上传文件', icon: 'Upload', path: '/documents' },
  { label: '成员管理', icon: 'User', path: '/members' },
  { label: '我的任务', icon: 'Checked', path: '/tasks' },
]

const recentTasks = computed(() => taskStore.tasks.slice(0, 8))

const stats = computed(() => {
  const list = taskStore.tasks
  return {
    total: list.length,
    done: list.filter((t) => t.status === '已完成').length,
    doing: list.filter((t) => t.status === '进行中').length,
    overdue: list.filter((t) => t.status === '已逾期').length,
  }
})

const recentFiles = ref([])

function statusTag(status) {
  const map = { '待开始': 'info', '进行中': 'warning', '已完成': 'success', '已逾期': 'danger' }
  return map[status] || 'info'
}
</script>

<style scoped>
.page-heading {
  margin: 0 0 20px;
  font-size: 18px;
  color: #303133;
}
.quick-actions {
  margin-bottom: 20px;
}
.action-card {
  background: #fff;
  border-radius: 8px;
  padding: 24px 0;
  text-align: center;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #1a3a6b;
  transition: all 0.2s;
}
.action-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.stats-card .stat-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.stats-card .stat-item:last-child {
  border-bottom: none;
}
.stat-num {
  font-size: 24px;
  font-weight: 700;
  color: #409eff;
}
.stat-label {
  color: #909399;
  line-height: 32px;
}
.recent-files .file-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.file-name {
  flex: 1;
  color: #303133;
}
.file-date {
  color: #909399;
  font-size: 13px;
}
</style>
