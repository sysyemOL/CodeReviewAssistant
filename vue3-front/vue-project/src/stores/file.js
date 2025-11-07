import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useFileStore = defineStore('file', () => {
  // 状态
  const uploadedFiles = ref([]) // 当前上传的文件列表
  const currentFileId = ref(null) // 当前选中的文件ID
  const fileContents = ref({}) // 文件内容缓存 { fileId: content }
  const isUploading = ref(false)
  
  // 计算属性
  const currentFile = computed(() => {
    return uploadedFiles.value.find(f => f.file_id === currentFileId.value)
  })
  
  const currentFileContent = computed(() => {
    return fileContents.value[currentFileId.value] || ''
  })
  
  // 方法
  const addFile = (file) => {
    uploadedFiles.value.push(file)
    if (!currentFileId.value && uploadedFiles.value.length === 1) {
      currentFileId.value = file.file_id
    }
  }
  
  const removeFile = (fileId) => {
    const index = uploadedFiles.value.findIndex(f => f.file_id === fileId)
    if (index !== -1) {
      uploadedFiles.value.splice(index, 1)
      delete fileContents.value[fileId]
      
      if (currentFileId.value === fileId) {
        currentFileId.value = uploadedFiles.value[0]?.file_id || null
      }
    }
  }
  
  const setCurrentFile = (fileId) => {
    currentFileId.value = fileId
  }
  
  const setFileContent = (fileId, content) => {
    fileContents.value[fileId] = content
  }
  
  const updateFileContent = (fileId, content) => {
    fileContents.value[fileId] = content
  }
  
  const clearFiles = () => {
    uploadedFiles.value = []
    currentFileId.value = null
    fileContents.value = {}
  }
  
  return {
    uploadedFiles,
    currentFileId,
    fileContents,
    isUploading,
    currentFile,
    currentFileContent,
    addFile,
    removeFile,
    setCurrentFile,
    setFileContent,
    updateFileContent,
    clearFiles
  }
})

