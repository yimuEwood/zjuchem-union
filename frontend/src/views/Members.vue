<template>
  <div class="members-page">
    <div class="page-heading-row">
      <h3>成员管理</h3>
      <el-button type="primary" @click="showCreate = true">添加成员</el-button>
    </div>

    <!-- 部门分组展示 -->
    <el-card v-for="dept in depts" :key="dept" shadow="never" style="margin-bottom:16px">
      <template #header>
        <span class="dept-title">{{ dept }}</span>
        <el-tag size="small" style="margin-left:8px">{{ deptMembers(dept).length }}人</el-tag>
      </template>
      <el-row :gutter="16">
        <el-col :span="8" v-for="m in deptMembers(dept)" :key="m.id">
          <div class="member-card">
            <el-avatar :size="48" icon="UserFilled" />
            <div class="member-info">
              <div class="member-name">{{ m.name }} <el-tag size="small" :type="m.role === '部长' ? 'danger' : m.role === '副部长' ? 'warning' : ''">{{ m.role }}</el-tag></div>
              <div class="member-meta">{{ m.phone }} · {{ m.email }}</div>
            </div>
          </div>
        </el-col>
        <el-col v-if="!deptMembers(dept).length" :span="24">
          <el-empty description="暂无成员" :image-size="40" />
        </el-col>
      </el-row>
    </el-card>

    <!-- 添加成员弹窗（简化版） -->
    <el-dialog v-model="showCreate" title="添加成员" width="450px">
      <el-form :model="memberForm" label-width="80px">
        <el-form-item label="姓名" required>
          <el-input v-model="memberForm.name" />
        </el-form-item>
        <el-form-item label="部门" required>
          <el-select v-model="memberForm.department" style="width:100%">
            <el-option v-for="d in depts" :key="d" :label="d" :value="d" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="memberForm.role" style="width:100%">
            <el-option label="干事" value="干事" />
            <el-option label="副部长" value="副部长" />
            <el-option label="部长" value="部长" />
          </el-select>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="memberForm.phone" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="memberForm.email" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreate = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { getMembers } from '@/api/members'
import { ElMessage } from 'element-plus'

const depts = ['主席团', '办公室', '宣传部', '学术部', '外联部', '文体部']
const members = ref([])
const showCreate = ref(false)

const memberForm = reactive({
  name: '', department: '', role: '干事', phone: '', email: '',
})

onMounted(async () => {
  members.value = await getMembers()
})

function deptMembers(dept) {
  return members.value.filter((m) => m.department === dept)
}

function handleAdd() {
  // 这里调用 API 添加成员 — 后续实现
  ElMessage.success('添加成功（功能待完整实现）')
  showCreate.value = false
}
</script>

<style scoped>
.page-heading-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.page-heading-row h3 {
  margin: 0;
}
.dept-title {
  font-weight: 600;
  color: #303133;
}
.member-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: #fafafa;
  margin-bottom: 8px;
}
.member-name {
  font-weight: 500;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 6px;
}
.member-meta {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>
