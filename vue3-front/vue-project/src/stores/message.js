import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { messageAPI } from '@/api/message'

export const useMessageStore = defineStore('message', () => {
  // 状态
  const messages = ref({}) // { sessionId: [messages] }
  const streamingMessage = ref(null) // 当前正在流式输出的消息
  const isStreaming = ref(false)
  const sseClient = ref(null) // SSE客户端实例，用于停止流
  const thinkingProcess = ref('') // AI思考过程
  const showThinkingProcess = ref(true) // 是否显示思考过程
  
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
  
  const startStreamingMessage = (sessionId, messageId = null) => {
    streamingMessage.value = {
      message_id: messageId || `msg_temp_${Date.now()}`,
      role: 'assistant',
      content: '',
      streaming: true,
      created_at: new Date().toISOString()
    }
    isStreaming.value = true
    thinkingProcess.value = '' // 重置思考过程
    showThinkingProcess.value = true // 默认展开思考过程
    addMessage(sessionId, streamingMessage.value)
    return streamingMessage.value
  }
  
  const updateStreamingMessageId = (messageId) => {
    if (streamingMessage.value) {
      streamingMessage.value.message_id = messageId
    }
  }
  
  const appendToStreamingMessage = (chunk) => {
    if (streamingMessage.value) {
      streamingMessage.value.content += chunk
    }
  }
  
  const endStreamingMessage = () => {
    if (streamingMessage.value) {
      streamingMessage.value.streaming = false
    }
    streamingMessage.value = null
    isStreaming.value = false
  }
  
  const clearSessionMessages = (sessionId) => {
    messages.value[sessionId] = []
  }
  
  const loadSessionMessages = (sessionId, messageList) => {
    messages.value[sessionId] = messageList
  }
  
  // 设置SSE客户端
  const setSSEClient = (client) => {
    sseClient.value = client
  }
  
  // 停止流式输出并保存部分内容
  const abortStreaming = async () => {
    if (sseClient.value) {
      sseClient.value.abort()
      sseClient.value = null
    }
    
    // 保存当前部分内容和思考过程到后端
    if (streamingMessage.value && streamingMessage.value.message_id) {
      try {
        await messageAPI.updateMessage(streamingMessage.value.message_id, {
          content: streamingMessage.value.content || '',
          thinking_process: thinkingProcess.value || null
        })
        console.log('已保存中断时的消息内容')
      } catch (error) {
        console.error('保存中断消息失败:', error)
      }
    }
    
    endStreamingMessage()
  }
  
  // 添加思考过程内容
  const appendToThinkingProcess = (chunk) => {
    thinkingProcess.value += chunk
  }
  
  // 切换思考过程显示/隐藏
  const toggleThinkingProcess = () => {
    showThinkingProcess.value = !showThinkingProcess.value
  }
  
  return {
    messages,
    streamingMessage,
    isStreaming,
    sseClient,
    thinkingProcess,
    showThinkingProcess,
    getSessionMessages,
    addMessage,
    addUserMessage,
    fetchSessionMessages,
    startStreamingMessage,
    updateStreamingMessageId,
    appendToStreamingMessage,
    endStreamingMessage,
    clearSessionMessages,
    loadSessionMessages,
    setSSEClient,
    abortStreaming,
    appendToThinkingProcess,
    toggleThinkingProcess
  }
})

