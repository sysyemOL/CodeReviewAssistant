import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useFileStore = defineStore('file', () => {
  // 状态 - 按会话存储文件
  const sessionFiles = ref({}) // { sessionId: [files] }
  const sessionFileContents = ref({}) // { sessionId: { fileId: content } }
  const currentFileIds = ref({}) // { sessionId: currentFileId }
  const isUploading = ref(false)
  
  // 当前会话ID（需要从外部设置）
  const currentSessionId = ref(null)
  
  // 计算属性 - 获取当前会话的文件
  const uploadedFiles = computed(() => {
    if (!currentSessionId.value) return []
    return sessionFiles.value[currentSessionId.value] || []
  })
  
  const currentFileId = computed(() => {
    if (!currentSessionId.value) return null
    return currentFileIds.value[currentSessionId.value] || null
  })
  
  const fileContents = computed(() => {
    if (!currentSessionId.value) return {}
    return sessionFileContents.value[currentSessionId.value] || {}
  })
  
  const currentFile = computed(() => {
    return uploadedFiles.value.find(f => f.file_id === currentFileId.value)
  })
  
  const currentFileContent = computed(() => {
    const contents = fileContents.value
    return contents[currentFileId.value] || ''
  })
  
  // 方法
  const setCurrentSession = (sessionId) => {
    currentSessionId.value = sessionId
  }
  
  const addFile = (file) => {
    if (!currentSessionId.value) return
    
    if (!sessionFiles.value[currentSessionId.value]) {
      sessionFiles.value[currentSessionId.value] = []
    }
    
    sessionFiles.value[currentSessionId.value].push(file)
    
    // 如果是第一个文件，自动选中
    if (!currentFileIds.value[currentSessionId.value] && sessionFiles.value[currentSessionId.value].length === 1) {
      currentFileIds.value[currentSessionId.value] = file.file_id
    }
    
    // 保存到 LocalStorage
    saveToLocalStorage()
  }
  
  const removeFile = (fileId) => {
    if (!currentSessionId.value) return
    
    const files = sessionFiles.value[currentSessionId.value]
    if (!files) return
    
    const index = files.findIndex(f => f.file_id === fileId)
    if (index !== -1) {
      files.splice(index, 1)
      
      // 删除文件内容
      if (sessionFileContents.value[currentSessionId.value]) {
        delete sessionFileContents.value[currentSessionId.value][fileId]
      }
      
      // 如果删除的是当前文件，选择下一个
      if (currentFileIds.value[currentSessionId.value] === fileId) {
        currentFileIds.value[currentSessionId.value] = files[0]?.file_id || null
      }
      
      // 保存到 LocalStorage
      saveToLocalStorage()
    }
  }
  
  const setCurrentFile = (fileId) => {
    if (!currentSessionId.value) return
    currentFileIds.value[currentSessionId.value] = fileId
    saveToLocalStorage()
  }
  
  const setFileContent = (fileId, content) => {
    if (!currentSessionId.value) return
    
    if (!sessionFileContents.value[currentSessionId.value]) {
      sessionFileContents.value[currentSessionId.value] = {}
    }
    
    sessionFileContents.value[currentSessionId.value][fileId] = content
    saveToLocalStorage()
  }
  
  const updateFileContent = (fileId, content) => {
    setFileContent(fileId, content)
  }
  
  const clearFiles = () => {
    if (!currentSessionId.value) return
    
    sessionFiles.value[currentSessionId.value] = []
    currentFileIds.value[currentSessionId.value] = null
    if (sessionFileContents.value[currentSessionId.value]) {
      sessionFileContents.value[currentSessionId.value] = {}
    }
    
    saveToLocalStorage()
  }
  
  const clearSessionFiles = (sessionId) => {
    delete sessionFiles.value[sessionId]
    delete sessionFileContents.value[sessionId]
    delete currentFileIds.value[sessionId]
    saveToLocalStorage()
  }
  
  // LocalStorage 持久化
  const saveToLocalStorage = () => {
    try {
      localStorage.setItem('file-store', JSON.stringify({
        sessionFiles: sessionFiles.value,
        sessionFileContents: sessionFileContents.value,
        currentFileIds: currentFileIds.value
      }))
    } catch (error) {
      console.error('Failed to save files to localStorage:', error)
    }
  }
  
  const loadFromLocalStorage = () => {
    try {
      const stored = localStorage.getItem('file-store')
      if (stored) {
        const data = JSON.parse(stored)
        sessionFiles.value = data.sessionFiles || {}
        sessionFileContents.value = data.sessionFileContents || {}
        currentFileIds.value = data.currentFileIds || {}
      }
    } catch (error) {
      console.error('Failed to load files from localStorage:', error)
    }
  }
  
  // 初始化时加载数据
  loadFromLocalStorage()
  
  return {
    // 状态
    uploadedFiles,
    currentFileId,
    fileContents,
    isUploading,
    currentFile,
    currentFileContent,
    currentSessionId,
    
    // 方法
    setCurrentSession,
    addFile,
    removeFile,
    setCurrentFile,
    setFileContent,
    updateFileContent,
    clearFiles,
    clearSessionFiles,
    loadFromLocalStorage
  }
})

