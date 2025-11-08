<template>
  <div class="input-box">
    <div class="upload-area" 
         :class="{ dragging: isDragging }"
         @drop.prevent="handleDrop"
         @dragover.prevent="isDragging = true"
         @dragleave="isDragging = false"
    >
      <div v-if="uploadedFiles.length > 0" class="uploaded-files">
        <div v-for="(file, index) in uploadedFiles" :key="index" class="file-tag">
          <el-icon><Document /></el-icon>
          <span class="file-name">{{ file.name }}</span>
          <span class="file-size">{{ formatFileSize(file.size) }}</span>
          <el-icon class="remove-icon" @click="removeFile(index)">
            <Close />
          </el-icon>
        </div>
      </div>
      
      <!-- 上传进度 -->
      <div v-if="isUploading" class="upload-progress">
        <el-progress :percentage="uploadProgress" :show-text="false" />
        <span class="progress-text">上传中... {{uploadProgress}}%</span>
      </div>

      <div class="input-container">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="3"
          :placeholder="placeholder"
          @keydown.enter.exact.prevent="handleSend"
          @keydown.shift.enter.exact="handleNewLine"
          resize="none"
        />

        <div class="input-actions">
          <div class="left-actions">
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleFileSelect"
              :before-upload="beforeUpload"
              multiple
              accept=".py,.js,.jsx,.ts,.tsx,.java,.go,.rs,.cpp,.c,.cs,.php,.rb,.swift,.kt,.vue"
            >
              <el-button :icon="Paperclip" text>上传文件</el-button>
            </el-upload>
            
            <el-button :icon="FolderOpened" text @click="handleSelectFolder">
              选择文件夹
            </el-button>
          </div>

          <el-button
            type="primary"
            :icon="Promotion"
            :loading="isSending"
            :disabled="!canSend"
            @click="handleSend"
          >
            发送
          </el-button>
        </div>
      </div>
    </div>

    <div class="tips">
      <span>按 Enter 发送，Shift + Enter 换行</span>
      <span>支持拖拽文件上传</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Paperclip, FolderOpened, Promotion, Document, Close } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { isAllowedFileType, isFileSizeValid } from '@/utils/file'
import { formatFileSize } from '@/utils/format'

const emit = defineEmits(['send', 'uploading'])

const inputText = ref('')
const uploadedFiles = ref([])
const isDragging = ref(false)
const isSending = ref(false)
const isUploading = ref(false)
const uploadProgress = ref(0)
const uploadRef = ref(null)

const placeholder = computed(() => {
  if (isDragging.value) {
    return '松开鼠标上传文件...'
  }
  return '请输入消息或上传代码文件...'
})

const canSend = computed(() => {
  return (inputText.value.trim() !== '' || uploadedFiles.value.length > 0) && !isSending.value
})

const beforeUpload = (file) => {
  if (!isAllowedFileType(file.name)) {
    ElMessage.error('不支持的文件类型')
    return false
  }
  if (!isFileSizeValid(file.size)) {
    ElMessage.error('文件大小不能超过10MB')
    return false
  }
  return true
}

const handleFileSelect = (file) => {
  if (beforeUpload(file.raw)) {
    uploadedFiles.value.push(file.raw)
  }
}

const handleDrop = (e) => {
  isDragging.value = false
  const files = Array.from(e.dataTransfer.files)
  
  files.forEach(file => {
    if (beforeUpload(file)) {
      uploadedFiles.value.push(file)
    }
  })
}

const handleSelectFolder = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.webkitdirectory = true
  input.directory = true
  input.multiple = true
  
  input.onchange = async (e) => {
    const files = Array.from(e.target.files)
    const validFiles = []
    
    for (const file of files) {
      if (beforeUpload(file)) {
        validFiles.push(file)
      }
    }
    
    if (validFiles.length > 0) {
      uploadedFiles.value.push(...validFiles)
      ElMessage.success(`成功选择 ${validFiles.length} 个文件`)
    }
  }
  
  input.click()
}

const removeFile = (index) => {
  uploadedFiles.value.splice(index, 1)
}

const handleNewLine = (e) => {
  // Shift + Enter 换行，由textarea自己处理
}

const handleSend = async () => {
  if (!canSend.value) return

  const content = inputText.value.trim()
  const files = [...uploadedFiles.value]

  isSending.value = true
  isUploading.value = files.length > 0
  uploadProgress.value = 0
  
  try {
    // 模拟上传进度
    if (files.length > 0) {
      emit('uploading', true)
      for (let i = 0; i <= 100; i += 10) {
        uploadProgress.value = i
        await new Promise(resolve => setTimeout(resolve, 100))
      }
    }
    
    emit('send', content, files)
    
    // 清空输入
    inputText.value = ''
    uploadedFiles.value = []
    uploadProgress.value = 0
  } catch (error) {
    ElMessage.error('发送失败')
  } finally {
    isSending.value = false
    isUploading.value = false
    emit('uploading', false)
  }
}
</script>

<style scoped>
.input-box {
  padding: 20px 28px 24px;
  background: transparent;
}

.upload-area {
  border: 2px dashed transparent;
  border-radius: 12px;
  transition: all 0.3s;
}

.upload-area.dragging {
  border-color: #409eff;
  background: rgba(64, 158, 255, 0.05);
}

.uploaded-files {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.file-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(228, 231, 237, 0.6);
  border-radius: 6px;
  font-size: 13px;
  color: #606266;
  backdrop-filter: blur(4px);
}

.file-tag .file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-tag .file-size {
  font-size: 11px;
  color: #909399;
  margin-left: auto;
}

.file-tag .remove-icon {
  cursor: pointer;
  font-size: 14px;
  opacity: 0.6;
  transition: all 0.2s;
  margin-left: 4px;
}

.file-tag .remove-icon:hover {
  opacity: 1;
  color: #f56c6c;
}

.upload-progress {
  margin-bottom: 12px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 6px;
  backdrop-filter: blur(4px);
}

.upload-progress .progress-text {
  font-size: 12px;
  color: #606266;
  margin-top: 4px;
  display: inline-block;
}

.input-container {
  background: rgba(255, 255, 255, 0.7);
  border: none;
  border-radius: 12px;
  padding: 14px 16px;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.input-container:focus-within {
  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.15);
  transform: translateY(-1px);
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.left-actions {
  display: flex;
  gap: 8px;
}

.tips {
  margin-top: 10px;
  font-size: 12px;
  color: rgba(144, 147, 153, 0.8);
  display: flex;
  justify-content: space-between;
}
</style>

