import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

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
  
  const addUserMessage = (sessionId, content) => {
    const message = {
      message_id: `msg_${Date.now()}`,
      role: 'user',
      content,
      created_at: new Date().toISOString()
    }
    addMessage(sessionId, message)
    return message
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
    startStreamingMessage,
    appendToStreamingMessage,
    endStreamingMessage,
    clearSessionMessages,
    loadSessionMessages
  }
})

