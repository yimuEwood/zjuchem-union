<template>
  <div class="tasks-page">
    <div class="page-heading-row">
      <h3>任务管理</h3>
      <el-button type="primary" @click="showCreate = true">新建任务</el-button>
    </div>

    <!-- 筛选栏 -->
    <el-card shadow="never" class="filter-bar">
      <el-form :inline="true" :model="filters" size="default">
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="全部" clearable style="width:130px">
            <el-option label="待开始" value="待开始" />
            <el-option label="进行中" value="进行中" />
            <el-option label="已完成" value="已完成" />
            <el-option label="已逾期" value="已逾期" />
          </el-select>
        </el-form-item>
        <el-form-item label="部门">
          <el-select v-model="filters.department" placeholder="全部" clearable style="width:130px">
            <el-option label="办公室" value="办公室" />
            <el-option label="宣传部" value="宣传部" />
            <el-option label="学术部" value="学术部" />
            <el-option label="外联部" value="外联部" />
            <el-option label="文体部" value="文体部" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="taskStore.fetchTasks()">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 任务列表 -->
    <el-card shadow="never" style="margin-top:16px">
      <el-table :data="filteredTasks" v-loading="taskStore.loading" style="width:100%">
        <el-table-column prop="title" label="任务名称" min-width="200" />
        <el-table-column prop="department" label="部门" width="100" />
        <el-table-column prop="assignee" label="负责人" width="100" />
        <el-table-column prop="deadline" label="截止日期" width="110" sortable />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTag(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="progress" label="进度" width="140">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" :stroke-width="6" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button text size="small" @click="editTask(row)">编辑</el-button>
            <el-button text size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新建/编辑弹窗 -->
    <el-dialog v-model="showCreate" :title="editing ? '编辑任务' : '新建任务'" width="550px">
      <el-form ref="taskFormRef" :model="taskForm" :rules="taskRules" label-width="80px">
        <el-form-item label="任务名称" prop="title">
          <el-input v-model="taskForm.title" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-select v-model="taskForm.department" style="width:100%">
            <el-option v-for="d in depts" :key="d" :label="d" :value="d" />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人" prop="assignee">
          <el-input v-model="taskForm.assignee" />
        </el-form-item>
        <el-form-item label="截止日期" prop="deadline">
          <el-date-picker v-model="taskForm.deadline" type="date" style="width:100%" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="taskForm.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreate = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useTaskStore } from '@/store/task'
import { createTask, updateTask, deleteTask } from '@/api/tasks'
import { ElMessage, ElMessageBox } from 'element-plus'

const taskStore = useTaskStore()
const showCreate = ref(false)
const editing = ref(null)
const taskFormRef = ref(null)

const filters = reactive({ status: '', department: '' })

const depts = ['办公室', '宣传部', '学术部', '外联部', '文体部']

const taskForm = reactive({
  title: '', department: '', assignee: '', deadline: '', description: '',
})

const taskRules = {
  title: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  department: [{ required: true, message: '请选择部门', trigger: 'change' }],
  assignee: [{ required: true, message: '请输入负责人', trigger: 'blur' }],
  deadline: [{ required: true, message: '请选择截止日期', trigger: 'change' }],
}

onMounted(() => taskStore.fetchTasks())

const filteredTasks = computed(() => {
  let list = taskStore.tasks
  if (filters.status) list = list.filter((t) => t.status === filters.status)
  if (filters.department) list = list.filter((t) => t.department === filters.department)
  return list
})

function editTask(row) {
  editing.value = row
  Object.assign(taskForm, row)
  showCreate.value = true
}

function resetForm() {
  editing.value = null
  Object.assign(taskForm, { title: '', department: '', assignee: '', deadline: '', description: '' })
}

async function handleSave() {
  const valid = await taskFormRef.value.validate().catch(() => false)
  if (!valid) return
  if (editing.value) {
    await updateTask(editing.value.id, taskForm)
    ElMessage.success('更新成功')
  } else {
    await createTask(taskForm)
    ElMessage.success('创建成功')
  }
  showCreate.value = false
  resetForm()
  taskStore.fetchTasks()
}

async function handleDelete(id) {
  await ElMessageBox.confirm('确定删除该任务？', '提示', { type: 'warning' })
  await deleteTask(id)
  ElMessage.success('已删除')
  taskStore.fetchTasks()
}

function statusTag(status) {
  const map = { '待开始': 'info', '进行中': 'warning', '已完成': 'success', '已逾期': 'danger' }
  return map[status] || 'info'
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
.filter-bar {
  padding: 4px 0 0;
}
</style>
