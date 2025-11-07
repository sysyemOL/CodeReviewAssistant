import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 应用状态
  const isLoading = ref(false)
  const theme = ref('light')
  const sidebarCollapsed = ref(false)
  
  // 设置加载状态
  const setLoading = (loading) => {
    isLoading.value = loading
  }
  
  // 切换主题
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }
  
  // 切换侧边栏
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
  
  return {
    isLoading,
    theme,
    sidebarCollapsed,
    setLoading,
    toggleTheme,
    toggleSidebar
  }
})

