import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { messageAPI } from '@/api/message'

export const useMessageStore = defineStore('message', () => {
  // 状态
  const messages = ref({}) // { sessionId: [messages] }
  const streamingMessage = ref(null) // 当前正在流式输出的消息
  const isStreaming = ref(false)
  
  // 计算属性
  const getSessionMessages = (sessionId) => {
    return computed(() => messages.value[sessionId] || [])
  }
  
  // 方法
  const addMessage = (sessionId, message) => {
    if (!messages.value[sessionId]) {
      messages.value[sessionId] = []
    }
    messages.value[sessionId].push(message)
  }
  
  const addUserMessage = async (sessionId, content) => {
    // 先添加到本地显示
    const localMessage = {
      message_id: `msg_${Date.now()}`,
      role: 'user',
      content,
      created_at: new Date().toISOString()
    }
    addMessage(sessionId, localMessage)
    
    // 异步保存到后端
    try {
      const backendMessage = await messageAPI.createMessage({
        session_id: sessionId,
        role: 'user',
        content
      })
      
      // 更新本地消息ID为后端返回的ID
      // 注意：response 拦截器已经提取了 data 字段
      const index = messages.value[sessionId].findIndex(m => m.message_id === localMessage.message_id)
      if (index !== -1) {
        messages.value[sessionId][index] = backendMessage
      }
      
      return backendMessage
    } catch (error) {
      console.error('保存消息到后端失败:', error)
      return localMessage
    }
  }
  
  // 从后端加载会话的所有消息
  const fetchSessionMessages = async (sessionId) => {
    try {
      const data = await messageAPI.getSessionMessages(sessionId)
      // 注意：response 拦截器已经提取了 data 字段，所以返回值是 { items: [...], total: N }
      messages.value[sessionId] = data.items || []
      return messages.value[sessionId]
    } catch (error) {
      console.error('加载会话消息失败:', error)
      messages.value[sessionId] = []
      return []
    }
  }
  
  const startStreamingMessage = (sessionId) => {
    streamingMessage.value = {
      message_id: `msg_${Date.now()}`,
      role: 'assistant',
      content: '',
      created_at: new Date().toISOString()
    }
    isStreaming.value = true
    addMessage(sessionId, streamingMessage.value)
  }
  
  const appendToStreamingMessage = (chunk) => {
    if (streamingMessage.value) {
      streamingMessage.value.content += chunk
    }
  }
  
  const endStreamingMessage = () => {
    streamingMessage.value = null
    isStreaming.value = false
  }
  
  const clearSessionMessages = (sessionId) => {
    messages.value[sessionId] = []
  }
  
  const loadSessionMessages = (sessionId, messageList) => {
    messages.value[sessionId] = messageList
  }
  
  return {
    messages,
    streamingMessage,
    isStreaming,
    getSessionMessages,
    addMessage,
    addUserMessage,
    fetchSessionMessages,
    startStreamingMessage,
    appendToStreamingMessage,
    endStreamingMessage,
    clearSessionMessages,
    loadSessionMessages
  }
})

