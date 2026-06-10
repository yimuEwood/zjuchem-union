<template>
  <div class="docs-page">
    <div class="page-heading-row">
      <h3>文件管理</h3>
      <el-button type="primary" @click="triggerUpload">上传文件</el-button>
    </div>

    <!-- 部门筛选 -->
    <el-card shadow="never" class="filter-bar">
      <el-radio-group v-model="deptFilter" size="default">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button v-for="d in depts" :key="d" :value="d">{{ d }}</el-radio-button>
      </el-radio-group>
    </el-card>

    <!-- 文件列表 -->
    <el-card shadow="never" style="margin-top:16px">
      <el-table :data="filteredDocs" style="width:100%" v-loading="loading">
        <el-table-column prop="filename" label="文件名" min-width="240">
          <template #default="{ row }">
            <el-icon :size="18"><Document /></el-icon>
            <span style="margin-left:6px; vertical-align:middle">{{ row.filename }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="department" label="部门" width="100" />
        <el-table-column prop="size" label="大小" width="100" />
        <el-table-column prop="uploader" label="上传者" width="100" />
        <el-table-column prop="createdAt" label="上传时间" width="160" sortable />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button text size="small" @click="handleDownload(row.id)">下载</el-button>
            <el-button text size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!loading && !filteredDocs.length" description="暂无文件" />
    </el-card>

    <!-- 隐藏的文件上传 input -->
    <input ref="fileInput" type="file" style="display:none" @change="handleFileChange" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getDocuments, uploadDocument, deleteDocument, downloadDocument } from '@/api/documents'
import { ElMessage, ElMessageBox } from 'element-plus'

const depts = ['办公室', '宣传部', '学术部', '外联部', '文体部']
const deptFilter = ref('')
const loading = ref(false)
const docs = ref([])
const fileInput = ref(null)

onMounted(() => fetchDocs())

async function fetchDocs() {
  loading.value = true
  try {
    docs.value = await getDocuments({ department: deptFilter.value || undefined })
  } finally {
    loading.value = false
  }
}

const filteredDocs = computed(() => {
  if (!deptFilter.value) return docs.value
  return docs.value.filter((d) => d.department === deptFilter.value)
})

function triggerUpload() {
  fileInput.value.click()
}

async function handleFileChange(e) {
  const file = e.target.files[0]
  if (!file) return
  const formData = new FormData()
  formData.append('file', file)
  await uploadDocument(formData)
  ElMessage.success('上传成功')
  fileInput.value.value = ''
  fetchDocs()
}

async function handleDownload(id) {
  const blob = await downloadDocument(id)
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = ''
  a.click()
  URL.revokeObjectURL(url)
}

async function handleDelete(id) {
  await ElMessageBox.confirm('确定删除该文件？', '提示', { type: 'warning' })
  await deleteDocument(id)
  ElMessage.success('已删除')
  fetchDocs()
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
</style>
