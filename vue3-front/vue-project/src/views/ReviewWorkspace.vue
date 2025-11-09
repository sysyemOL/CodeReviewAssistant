<template>
  <div class="review-workspace">
    <!-- 左侧：历史会话列表 -->
    <aside class="sidebar" :class="{ collapsed: appStore.sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="header-left">
          <h3 v-if="!appStore.sidebarCollapsed">历史对话</h3>
          <el-button 
            :icon="Plus" 
            type="primary" 
            @click="handleCreateSession"
            :title="appStore.sidebarCollapsed ? '新对话' : ''"
            v-if="!appStore.sidebarCollapsed"
          >
            <span>新对话</span>
          </el-button>
        </div>
        
        <!-- 收缩/展开按钮移到顶部 -->
        <el-button 
          :icon="appStore.sidebarCollapsed ? Expand : Fold" 
          circle
          @click="appStore.toggleSidebar"
          class="toggle-btn"
          :title="appStore.sidebarCollapsed ? '展开侧边栏' : '收缩侧边栏'"
        />
      </div>
      
      <SessionList v-if="!appStore.sidebarCollapsed" />
      
      <!-- 收缩后只显示新对话按钮 -->
      <div class="collapsed-actions" v-if="appStore.sidebarCollapsed">
        <el-button 
          :icon="Plus" 
          circle
          type="primary"
          @click="handleCreateSession"
          title="新对话"
        />
      </div>
    </aside>

    <!-- 中间：对话交互区 -->
    <main class="main-content">
      <div class="chat-header">
        <h2>{{ currentSessionTitle }}</h2>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <MessageList :session-id="sessionStore.currentSessionId" />
      </div>
      
      <div class="chat-input">
        <InputBox @send="handleSendMessage" />
      </div>
    </main>

    <!-- 拖拽手柄 -->
    <div 
      v-if="fileStore.currentFile"
      class="resize-handle"
      @mousedown="startResize"
      :class="{ resizing: isResizing }"
    >
      <div class="resize-handle-line"></div>
    </div>

    <!-- 右侧：代码编辑器 -->
    <aside 
      class="code-panel" 
      :class="{ hidden: !fileStore.currentFile }" 
      :style="!fileStore.currentFile ? { display: 'none' } : (codePanelWidth ? { width: codePanelWidth + 'px', flex: 'none' } : {})"
    >
      <div class="code-header">
        <div class="file-tabs">
          <div 
            v-for="file in fileStore.uploadedFiles" 
            :key="file.file_id"
            class="file-tab"
            :class="{ active: file.file_id === fileStore.currentFileId }"
            @click="fileStore.setCurrentFile(file.file_id)"
          >
            <span>{{ file.filename }}</span>
            <el-icon class="close-icon" @click.stop="handleRemoveFile(file.file_id)">
              <Close />
            </el-icon>
          </div>
        </div>
        <div class="code-actions">
          <!-- 透明度滑轨（仅毛玻璃主题显示） -->
          <div v-if="isGlassTheme" class="opacity-control">
            <span class="opacity-label">透明度</span>
            <el-slider 
              v-model="glassOpacity" 
              :min="30" 
              :max="90" 
              :show-tooltip="true"
              :format-tooltip="(val) => `${val}%`"
              style="width: 120px;"
            />
          </div>
          
          <ThemeSelector v-model="editorTheme" />
          
          <!-- 背景管理按钮 -->
          <el-dropdown trigger="click" @command="handleBackgroundCommand">
            <el-button :icon="Picture" circle :title="backgroundImage ? '背景管理' : '上传背景图片'" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="upload">
                  <el-icon><Upload /></el-icon>
                  上传背景
                </el-dropdown-item>
                <el-dropdown-item v-if="backgroundImage" command="clear" divided>
                  <el-icon><Delete /></el-icon>
                  清除背景
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <div class="code-editor-wrapper">
        <FileTree 
          :files="fileStore.uploadedFiles"
          :current-file-id="fileStore.currentFileId"
          @select-file="fileStore.setCurrentFile"
          @toggle-collapse="handleFileTreeToggle"
        />
        <div 
          class="code-editor" 
          :class="{ 'glass-theme': isGlassTheme }"
          :style="getEditorStyle()"
        >
          <CodeEditor 
            v-if="fileStore.currentFile"
            :file-id="fileStore.currentFileId"
            :language="getFileLanguage(fileStore.currentFile.filename)"
            :content="fileStore.currentFileContent"
            :theme="editorTheme"
            @update="handleCodeUpdate"
          />
          <div v-else class="empty-state">
            <el-empty description="暂无文件" />
          </div>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Plus, Expand, Fold, Close, Upload, Picture, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useAppStore } from '@/stores/app'
import { useSessionStore } from '@/stores/session'
import { useMessageStore } from '@/stores/message'
import { useFileStore } from '@/stores/file'
import SessionList from '@/components/sidebar/SessionList.vue'
import MessageList from '@/components/chat/MessageList.vue'
import InputBox from '@/components/chat/InputBox.vue'
import CodeEditor from '@/components/common/CodeEditor.vue'
import ThemeSelector from '@/components/common/ThemeSelector.vue'
import FileTree from '@/components/common/FileTree.vue'
import { getLanguageFromFilename } from '@/utils/format'
import { readFileContent, generateFileId } from '@/utils/file'
import { fileAPI } from '@/api/file'
import { reviewAPI } from '@/api/review'

const appStore = useAppStore()
const sessionStore = useSessionStore()
const messageStore = useMessageStore()
const fileStore = useFileStore()

const messagesContainer = ref(null)

// 拖拽调整宽度相关
const codePanelWidth = ref(null)  // 初始为null，使用弹性布局
const isResizing = ref(false)
const startX = ref(0)
const startCodeWidth = ref(0)

// 编辑器主题和背景
const editorTheme = ref('pure-white')
const backgroundImage = ref(null)
const glassOpacity = ref(70)  // 毛玻璃透明度，30-90

// 判断是否为毛玻璃主题
const isGlassTheme = computed(() => {
  return editorTheme.value === 'white-glass' || editorTheme.value === 'dark-glass'
})

const currentSessionTitle = computed(() => {
  return sessionStore.currentSession?.title || 'AI代码Review助手'
})

const getFileLanguage = (filename) => {
  return getLanguageFromFilename(filename)
}

// 获取编辑器样式（背景图片 + 毛玻璃透明度）
const getEditorStyle = () => {
  const styles = {}
  
  // 应用背景图片
  if (backgroundImage.value) {
    styles.backgroundImage = `url(${backgroundImage.value})`
    styles.backgroundSize = 'cover'
    styles.backgroundPosition = 'center'
  }
  
  // 应用毛玻璃透明度（通过 CSS 变量）
  if (isGlassTheme.value) {
    // 将透明度百分比转换为 0-1 的值
    const opacityValue = glassOpacity.value / 100
    styles['--glass-opacity'] = opacityValue
  }
  
  return styles
}

const handleCreateSession = async () => {
  try {
    await sessionStore.createSession('新对话')
    ElMessage.success('创建会话成功')
  } catch (error) {
    ElMessage.error('创建会话失败')
  }
}

const handleSendMessage = async (content, files) => {
  if (!sessionStore.currentSessionId) {
    // 如果没有当前会话，先创建一个
    await handleCreateSession()
  }
  
  // 处理文件上传
  if (files && files.length > 0) {
    fileStore.isUploading = true
    try {
      for (const file of files) {
        // 创建 FormData
        const formData = new FormData()
        formData.append('file', file)
        formData.append('session_id', sessionStore.currentSessionId)
        
        // 调用后端 API 上传文件
        const uploadedFile = await fileAPI.uploadFile(formData, (progress) => {
          console.log(`上传进度: ${progress}%`)
        })
        
        // 注意：response 拦截器已经提取了 data 字段，所以直接使用返回值
        // 添加到前端 fileStore
        fileStore.addFile({
          file_id: uploadedFile.file_id,
          filename: uploadedFile.filename,
          file_size: uploadedFile.file_size,
          file_type: uploadedFile.file_type,
          session_id: uploadedFile.session_id
        })
        
        // 存储文件内容到前端
        const fileContent = await readFileContent(file)
        fileStore.setFileContent(uploadedFile.file_id, fileContent)
      }
      
      ElMessage.success(`成功上传 ${files.length} 个文件`)
    } catch (error) {
      console.error('文件上传失败:', error)
      ElMessage.error('文件上传失败: ' + (error.message || '未知错误'))
    } finally {
      fileStore.isUploading = false
    }
  }
  
  // 添加用户消息
  if (content) {
    await messageStore.addUserMessage(sessionStore.currentSessionId, content)
  }
  
  // 如果有文件且有用户消息，触发代码审查
  if (content && fileStore.uploadedFiles.length > 0) {
    await handleCodeReview(content)
  }
  
  // 滚动到底部
  scrollToBottom()
}

const handleCodeReview = async (userQuestion) => {
  try {
    // 显示加载状态
    messageStore.isStreaming = true
    
    const uploadedFiles = fileStore.uploadedFiles
    
    // 判断是单文件还是多文件审查
    if (uploadedFiles.length === 1) {
      // 单文件审查
      await reviewAPI.reviewSingleFile({
        session_id: sessionStore.currentSessionId,
        file_id: uploadedFiles[0].file_id,
        user_question: userQuestion
      })
      
      // 后端已经保存了消息，需要重新加载消息列表
      await messageStore.fetchSessionMessages(sessionStore.currentSessionId)
      
      ElMessage.success('代码审查完成')
    } else if (uploadedFiles.length > 1) {
      // 多文件审查
      const fileIds = uploadedFiles.map(f => f.file_id)
      await reviewAPI.reviewMultipleFiles({
        session_id: sessionStore.currentSessionId,
        file_ids: fileIds,
        user_question: userQuestion
      })
      
      // 后端已经保存了消息，需要重新加载消息列表
      await messageStore.fetchSessionMessages(sessionStore.currentSessionId)
      
      ElMessage.success('多文件代码审查完成')
    }
    
  } catch (error) {
    console.error('代码审查失败:', error)
    ElMessage.error('代码审查失败: ' + (error.message || '未知错误'))
  } finally {
    messageStore.isStreaming = false
    scrollToBottom()
  }
}

const handleCodeUpdate = (fileId, newContent) => {
  fileStore.updateFileContent(fileId, newContent)
}

const handleRemoveFile = (fileId) => {
  fileStore.removeFile(fileId)
}

const scrollToBottom = () => {
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }, 100)
}

// 拖拽调整宽度的函数
const startResize = (e) => {
  isResizing.value = true
  startX.value = e.clientX
  
  // 获取代码编辑器当前宽度
  const codeElement = document.querySelector('.code-panel')
  startCodeWidth.value = codePanelWidth.value || codeElement.offsetWidth
  
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'
}

const handleResize = (e) => {
  if (!isResizing.value) return
  
  const deltaX = e.clientX - startX.value
  const newCodeWidth = startCodeWidth.value - deltaX
  
  // 代码编辑器最小300px，最大不超过窗口宽度的60%
  const minCodeWidth = 300
  const maxCodeWidth = window.innerWidth * 0.6
  
  if (newCodeWidth >= minCodeWidth && newCodeWidth <= maxCodeWidth) {
    codePanelWidth.value = newCodeWidth
  }
}

const stopResize = () => {
  isResizing.value = false
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
  document.body.style.cursor = ''
  document.body.style.userSelect = ''
}

// 上传背景图片
// 背景管理命令处理
const handleBackgroundCommand = (command) => {
  if (command === 'upload') {
    // 上传背景图片
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.onchange = (e) => {
      const file = e.target.files[0]
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          ElMessage.error('图片大小不能超过5MB')
          return
        }
        const reader = new FileReader()
        reader.onload = (e) => {
          backgroundImage.value = e.target.result
          ElMessage.success('背景图片上传成功')
        }
        reader.readAsDataURL(file)
      }
    }
    input.click()
  } else if (command === 'clear') {
    // 清除背景图片
    backgroundImage.value = null
    ElMessage.success('背景图片已清除')
  }
}

// 文件树折叠/展开
const handleFileTreeToggle = (collapsed) => {
  // 可以在这里保存状态到localStorage
  console.log('File tree collapsed:', collapsed)
}

// 监听会话切换，同步文件存储的当前会话
watch(() => sessionStore.currentSessionId, async (newSessionId, oldSessionId) => {
  if (newSessionId !== oldSessionId && newSessionId) {
    // 同步 fileStore 的当前会话ID
    fileStore.setCurrentSession(newSessionId)
    
    // 从后端加载该会话的消息
    try {
      await messageStore.fetchSessionMessages(newSessionId)
    } catch (error) {
      console.error('加载会话消息失败:', error)
    }
    
    // 如果新会话没有文件，重置布局宽度
    if (oldSessionId !== null && fileStore.uploadedFiles.length === 0) {
      codePanelWidth.value = null
    }
  }
}, { immediate: true }) // 立即执行，确保初始化时也能同步

// 监听文件变化，当没有文件时重置布局
watch(() => fileStore.uploadedFiles.length, (newLength) => {
  if (newLength === 0) {
    // 没有文件时重置宽度，恢复弹性布局
    codePanelWidth.value = null
  }
})

// 监听消息变化，自动滚动到底部
watch(() => {
  if (sessionStore.currentSessionId) {
    return messageStore.getSessionMessages(sessionStore.currentSessionId).value.length
  }
  return 0
}, () => {
  // 新消息到达时自动滚动到底部
  scrollToBottom()
}, { flush: 'post' }) // 在 DOM 更新后执行

onMounted(async () => {
  // 初始化：获取会话列表
  try {
    await sessionStore.fetchSessions()
    if (sessionStore.sessions.length === 0) {
      // 如果没有会话，创建一个默认会话
      await handleCreateSession()
    } else {
      // 选择第一个会话
      sessionStore.setCurrentSession(sessionStore.sessions[0].session_id)
    }
  } catch (error) {
    console.error('初始化失败:', error)
  }
})
</script>

<style scoped>
/* 动态渐变背景动画 */
@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes floatBubbles {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.review-workspace {
  display: flex;
  width: 100%;
  height: 100%;
  background: linear-gradient(-45deg, 
    rgba(240, 242, 255, 0.95) 0%, 
    rgba(255, 240, 250, 0.95) 25%,
    rgba(240, 248, 255, 0.95) 50%,
    rgba(255, 245, 250, 0.95) 75%,
    rgba(245, 240, 255, 0.95) 100%
  );
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  overflow: hidden;
  gap: 12px;
  padding: 12px;
  box-sizing: border-box;
  position: relative;
}

.review-workspace::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  right: -50%;
  bottom: -50%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(147, 197, 253, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(251, 207, 232, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(196, 181, 253, 0.15) 0%, transparent 50%);
  animation: floatBubbles 20s ease-in-out infinite;
  pointer-events: none;
  z-index: 0;
}

.review-workspace > * {
  position: relative;
  z-index: 1;
}

/* 左侧边栏 */
.sidebar {
  width: 280px;
  min-width: 280px;
  background: #ffffff;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.sidebar.collapsed {
  width: 70px;
  min-width: 70px;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
  gap: 12px;
}

.sidebar-header .header-left {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  min-width: 0;
}

.sidebar-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0;
  white-space: nowrap;
}

.sidebar-header .toggle-btn {
  flex-shrink: 0;
}

.sidebar.collapsed .sidebar-header {
  justify-content: center;
  padding: 16px 12px;
}

/* 收缩后的操作按钮 */
.collapsed-actions {
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}

/* 拖拽手柄 */
.resize-handle {
  width: 4px;
  cursor: col-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  flex-shrink: 0;
  position: relative;
  z-index: 10;
  margin: 0 -3px;  /* 缩小与两侧的间隔 */
}

.resize-handle:hover,
.resize-handle.resizing {
  background: rgba(64, 158, 255, 0.1);
}

.resize-handle-line {
  width: 2px;
  height: 40px;
  background: rgba(64, 158, 255, 0.3);
  border-radius: 1px;
  transition: all 0.2s;
}

.resize-handle:hover .resize-handle-line,
.resize-handle.resizing .resize-handle-line {
  height: 60px;
  background: rgba(64, 158, 255, 0.6);
}

/* 中间主内容区 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 400px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.chat-header {
  height: 64px;
  padding: 0 28px;
  background: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.04);
}

.chat-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #fafbfc;
}

.chat-input {
  background: rgba(255, 255, 255, 0.4);
  border-top: 1px solid rgba(240, 240, 240, 0.3);
  box-shadow: 0 -2px 12px 0 rgba(147, 197, 253, 0.1);
  backdrop-filter: blur(10px);
}

/* 右侧代码面板 */
.code-panel {
  flex: 1;  /* 默认使用弹性布局填充剩余空间 */
  min-width: 300px;
  background: #ffffff;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  overflow: hidden;
  margin-left: -3px;  /* 缩小与对话区域的间隔 */
}

.code-panel.hidden {
  width: 0;
  min-width: 0;
  opacity: 0;
  margin-left: -12px;
  box-shadow: none;
}

.code-header {
  height: 50px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
  box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.04);
  gap: 12px;
  padding: 0 12px;
}

.code-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.opacity-control {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 12px;
  border-right: 1px solid #e4e7ed;
}

.opacity-label {
  font-size: 12px;
  color: #606266;
  white-space: nowrap;
}

.file-tabs {
  display: flex;
  height: 100%;
}

.file-tab {
  height: 100%;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  border-right: 1px solid #f0f0f0;
  background: #fafbfc;
  transition: all 0.2s ease;
  white-space: nowrap;
  font-size: 14px;
  color: #606266;
  position: relative;
}

.file-tab::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: transparent;
  transition: background 0.2s ease;
}

.file-tab:hover {
  background: #f0f2f5;
  color: #303133;
}

.file-tab.active {
  background: #ffffff;
  color: #409eff;
  font-weight: 500;
}

.file-tab.active::after {
  background: #409eff;
}

.file-tab .close-icon {
  font-size: 14px;
  cursor: pointer;
  opacity: 0.6;
  transition: all 0.2s ease;
}

.file-tab .close-icon:hover {
  opacity: 1;
  color: #f56c6c;
  transform: scale(1.1);
}

.code-editor-wrapper {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.code-editor {
  flex: 1;
  overflow: hidden;
  background: #1e1e1e;
  position: relative;
}

/* 毛玻璃主题效果 */
.code-editor.glass-theme {
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* 使用 CSS 变量控制透明度 */
.code-editor.glass-theme::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, var(--glass-opacity, 0.7)), 
    rgba(240, 242, 255, var(--glass-opacity, 0.7))
  );
  pointer-events: none;
  z-index: 0;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafbfc;
}
</style>

