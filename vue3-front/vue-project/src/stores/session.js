import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { sessionAPI } from '@/api/session'
import { setStorage, getStorage } from '@/utils/storage'

export const useSessionStore = defineStore('session', () => {
  // 从LocalStorage恢复状态
  const savedSessions = getStorage('sessions', [])
  const savedCurrentSessionId = getStorage('currentSessionId', null)
  
  // 状态
  const sessions = ref(savedSessions)
  const currentSessionId = ref(savedCurrentSessionId)
  const isLoading = ref(false)
  
  // 计算属性
  const currentSession = computed(() => {
    return sessions.value.find(s => s.session_id === currentSessionId.value)
  })
  
  const sortedSessions = computed(() => {
    return [...sessions.value].sort((a, b) => {
      return new Date(b.updated_at) - new Date(a.updated_at)
    })
  })
  
  // 方法
  const fetchSessions = async () => {
    try {
      isLoading.value = true
      const data = await sessionAPI.getSessions()
      // 后端返回的是 {total, items} 格式，需要提取items
      sessions.value = data.items || []
    } catch (error) {
      console.error('获取会话列表失败:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  const createSession = async (title = '新对话') => {
    try {
      const newSession = await sessionAPI.createSession({ title })
      sessions.value.unshift(newSession)
      currentSessionId.value = newSession.session_id
      return newSession
    } catch (error) {
      console.error('创建会话失败:', error)
      throw error
    }
  }
  
  const updateSession = async (sessionId, data) => {
    try {
      const updated = await sessionAPI.updateSession(sessionId, data)
      const index = sessions.value.findIndex(s => s.session_id === sessionId)
      if (index !== -1) {
        sessions.value[index] = updated
      }
      return updated
    } catch (error) {
      console.error('更新会话失败:', error)
      throw error
    }
  }
  
  const deleteSession = async (sessionId) => {
    try {
      await sessionAPI.deleteSession(sessionId)
      const index = sessions.value.findIndex(s => s.session_id === sessionId)
      if (index !== -1) {
        sessions.value.splice(index, 1)
      }
      if (currentSessionId.value === sessionId) {
        currentSessionId.value = sessions.value[0]?.session_id || null
      }
    } catch (error) {
      console.error('删除会话失败:', error)
      throw error
    }
  }
  
  const setCurrentSession = (sessionId) => {
    currentSessionId.value = sessionId
  }
  
  // 监听状态变化，自动保存到LocalStorage
  watch(sessions, (newSessions) => {
    setStorage('sessions', newSessions)
  }, { deep: true })
  
  watch(currentSessionId, (newId) => {
    setStorage('currentSessionId', newId)
  })
  
  return {
    sessions,
    currentSessionId,
    isLoading,
    currentSession,
    sortedSessions,
    fetchSessions,
    createSession,
    updateSession,
    deleteSession,
    setCurrentSession
  }
})

