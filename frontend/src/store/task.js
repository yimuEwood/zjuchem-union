import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTasks } from '@/api/tasks'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref([])
  const loading = ref(false)

  async function fetchTasks() {
    loading.value = true
    try {
      tasks.value = await getTasks()
    } finally {
      loading.value = false
    }
  }

  return { tasks, loading, fetchTasks }
})
