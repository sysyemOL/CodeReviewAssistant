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
          <span>{{ file.name }}</span>
          <el-icon class="remove-icon" @click="removeFile(index)">
            <Close />
          </el-icon>
        </div>
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
              accept=".py,.js,.jsx,.ts,.tsx,.java,.go,.rs,.cpp,.c,.cs,.php,.rb,.swift,.kt"
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

const emit = defineEmits(['send'])

const inputText = ref('')
const uploadedFiles = ref([])
const isDragging = ref(false)
const isSending = ref(false)
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
  ElMessage.info('文件夹上传功能开发中...')
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
  try {
    emit('send', content, files)
    
    // 清空输入
    inputText.value = ''
    uploadedFiles.value = []
  } catch (error) {
    ElMessage.error('发送失败')
  } finally {
    isSending.value = false
  }
}
</script>

<style scoped>
.input-box {
  padding: 16px 24px;
}

.upload-area {
  border: 2px dashed transparent;
  border-radius: 8px;
  transition: all 0.3s;
}

.upload-area.dragging {
  border-color: #409eff;
  background: #ecf5ff;
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
  background: #f5f7fa;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  font-size: 13px;
  color: #606266;
}

.file-tag .remove-icon {
  cursor: pointer;
  font-size: 14px;
}

.file-tag .remove-icon:hover {
  color: #f56c6c;
}

.input-container {
  background: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  padding: 12px;
  transition: border-color 0.3s;
}

.input-container:focus-within {
  border-color: #409eff;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.left-actions {
  display: flex;
  gap: 8px;
}

.tips {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  display: flex;
  justify-content: space-between;
}
</style>

