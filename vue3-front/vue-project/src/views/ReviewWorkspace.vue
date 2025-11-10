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
      
      <!-- 返回门户按钮 -->
      <div class="back-to-portal">
        <el-button 
          :icon="HomeFilled" 
          circle
          class="portal-btn"
          @click="goBackToPortal"
          title="返回门户"
        />
      </div>
    </aside>

    <!-- 中间：对话交互区 -->
    <main class="main-content">
      <div class="chat-header">
        <h2>{{ currentSessionTitle }}</h2>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <!-- 初始化加载状态 -->
        <div v-if="isInitializing" class="loading-state">
          <el-skeleton :rows="5" animated />
        </div>
        
        <!-- 消息列表 -->
        <transition name="fade" mode="out-in">
          <MessageList v-if="!isInitializing" :session-id="sessionStore.currentSessionId" />
        </transition>
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
      :class="{ 
        hidden: !fileStore.currentFile,
        'no-transition': isResizing 
      }" 
      :style="!fileStore.currentFile ? { display: 'none' } : (codePanelWidth ? { width: codePanelWidth + 'px', flex: 'none' } : {})"
    >
      <div class="code-header">
        <div class="file-tabs-container">
          <el-icon 
            class="tab-scroll-btn left" 
            @click="scrollTabs('left')" 
            v-if="showScrollButtons"
            tabindex="-1"
            aria-hidden="true"
          >
            <ArrowLeft />
          </el-icon>
          
          <div class="file-tabs" ref="fileTabsRef" role="tablist">
            <div 
              v-for="(file, index) in fileStore.uploadedFiles" 
              :key="file.file_id"
              class="file-tab"
              :class="{ active: file.file_id === fileStore.currentFileId }"
              @click="fileStore.setCurrentFile(file.file_id)"
              @keydown.enter="fileStore.setCurrentFile(file.file_id)"
              @keydown.space.prevent="fileStore.setCurrentFile(file.file_id)"
              @keydown.delete.prevent="handleRemoveFile(file.file_id)"
              @keydown.backspace.prevent="handleRemoveFile(file.file_id)"
              :title="`${file.filename} - 按 Ctrl+${index + 1} 切换 | Delete 关闭`"
              tabindex="0"
              role="tab"
              :aria-selected="file.file_id === fileStore.currentFileId"
            >
              <el-icon class="file-icon" :style="{ color: getFileIconColor(file.filename) }">
                <component :is="getFileIcon(file.filename)" />
              </el-icon>
              <span class="file-name">{{ file.filename }}</span>
              <el-icon 
                class="close-icon" 
                @click.stop="handleRemoveFile(file.file_id)"
                tabindex="-1"
                role="button"
                :aria-label="`关闭 ${file.filename}`"
              >
                <Close />
              </el-icon>
            </div>
          </div>
          
          <el-icon 
            class="tab-scroll-btn right" 
            @click="scrollTabs('right')" 
            v-if="showScrollButtons"
            tabindex="-1"
            aria-hidden="true"
          >
            <ArrowRight />
          </el-icon>
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
          <!-- 上传中状态 -->
          <div v-if="isUploadingFile" class="uploading-state">
            <el-icon class="is-loading upload-icon">
              <Upload />
            </el-icon>
            <p>正在上传文件...</p>
          </div>
          
          <!-- 空状态 -->
          <div v-else class="empty-state">
            <el-icon class="empty-icon">
              <Document />
            </el-icon>
            <h3>暂无文件</h3>
            <p>上传代码文件开始审查</p>
            <el-button type="primary" :icon="Upload" @click="handleFileUpload">
              上传文件
            </el-button>
          </div>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Plus, Expand, Fold, Close, Upload, Picture, Delete, HomeFilled, ArrowLeft, ArrowRight, Document, DocumentCopy } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
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
import { sendMessageStream } from '@/api/chat'
import { sessionAPI } from '@/api/session'
import { showError, showSuccess, showWarning, showErrorNotification, handleError } from '@/utils/errorHandler'

const router = useRouter()
const appStore = useAppStore()
const sessionStore = useSessionStore()
const messageStore = useMessageStore()
const fileStore = useFileStore()

const messagesContainer = ref(null)
const fileTabsRef = ref(null)
const showScrollButtons = ref(false)

// 加载状态
const isInitializing = ref(true)
const isUploadingFile = ref(false)
const isSendingMessage = ref(false)

// 拖拽调整宽度相关
const codePanelWidth = ref(null)  // 初始为null，使用弹性布局
const isResizing = ref(false)
const startX = ref(0)
const startCodeWidth = ref(0)
let rafId = null  // requestAnimationFrame ID
let pendingWidth = null  // 待更新的宽度

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

// 返回门户页面
const goBackToPortal = () => {
  router.push('/')
}

const handleCreateSession = async () => {
  try {
    await sessionStore.createSession('新对话')
    showSuccess('创建会话成功')
  } catch (error) {
    handleError(error, '创建会话失败')
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
        
        // 先读取文件内容
        const fileContent = await readFileContent(file)
        
        // 调用后端 API 上传文件
        const uploadedFile = await fileAPI.uploadFile(formData, (progress) => {
          console.log(`上传进度: ${progress}%`)
        })
        
        // 添加到前端 fileStore
        fileStore.addFile({
          file_id: uploadedFile.file_id,
          filename: uploadedFile.filename,
          file_size: uploadedFile.file_size,
          file_type: uploadedFile.file_type,
          session_id: uploadedFile.session_id
        })
        
        // 存储文件内容到前端
        fileStore.setFileContent(uploadedFile.file_id, fileContent)
      }
      
      showSuccess(`成功上传 ${files.length} 个文件`)
    } catch (error) {
      console.error('文件上传失败:', error)
      handleError(error, '文件上传失败')
    } finally {
      fileStore.isUploading = false
    }
  }
  
  // 发送消息（流式）
  if (content) {
    await handleSendMessageWithStream(content)
  }
  
  // 滚动到底部
  scrollToBottom()
}

// 使用流式 API 发送消息
const handleSendMessageWithStream = async (content) => {
  try {
    // 获取关联的文件ID
    const fileIds = fileStore.uploadedFiles.map(f => f.file_id)
    
    // 添加用户消息到界面
    const userMessage = {
      message_id: `msg_temp_${Date.now()}`,
      role: 'user',
      content,
      created_at: new Date().toISOString()
    }
    messageStore.addMessage(sessionStore.currentSessionId, userMessage)
    scrollToBottom()
    
    // 启动流式响应
    messageStore.startStreamingMessage(sessionStore.currentSessionId)
    scrollToBottom()
    
    // 连接 SSE
    const sseClient = sendMessageStream(
      {
        session_id: sessionStore.currentSessionId,
        message: content,
        file_ids: fileIds.length > 0 ? fileIds : null
      },
      {
        onUserMessage: (data) => {
          // 更新用户消息 ID
          const messages = messageStore.messages[sessionStore.currentSessionId]
          if (messages) {
            const lastUserMsg = messages.find(m => m.message_id === userMessage.message_id)
            if (lastUserMsg) {
              lastUserMsg.message_id = data.message_id
            }
          }
        },
        onStart: (data) => {
          // AI 开始响应
          console.log('AI 开始响应:', data)
          messageStore.updateStreamingMessageId(data.message_id)
        },
        onThinking: (data) => {
          // AI 思考过程
          if (data.delta) {
            messageStore.appendToThinkingProcess(data.delta)
          }
        },
        onContent: (data) => {
          // 接收增量内容
          messageStore.appendToStreamingMessage(data.delta)
          scrollToBottom()
        },
        onDone: async (data) => {
          // 完成
          console.log('AI 响应完成:', data)
          messageStore.endStreamingMessage()
          scrollToBottom()
          
          // 刷新当前会话以更新标题
          try {
            const updatedSession = await sessionAPI.getSession(sessionStore.currentSessionId)
            // 直接更新 sessions 数组中的会话数据
            const index = sessionStore.sessions.findIndex(s => s.session_id === sessionStore.currentSessionId)
            if (index !== -1) {
              sessionStore.sessions[index] = updatedSession
            }
          } catch (error) {
            console.error('刷新会话失败:', error)
          }
        },
        onAbort: () => {
          // 用户中断
          console.log('用户中断流式输出')
          messageStore.endStreamingMessage()
          showInfo('已停止生成')
        },
        onError: (data) => {
          // 错误处理
          console.error('流式响应错误:', data)
          messageStore.endStreamingMessage()
          showErrorNotification(data.error || 'AI服务响应失败', 'AI响应错误')
        },
        onClose: () => {
          // 连接关闭
          messageStore.endStreamingMessage()
        }
      }
    )
    
    // 保存 SSE 客户端引用到 store，以便可以停止流
    messageStore.setSSEClient(sseClient)
    
  } catch (error) {
    console.error('发送消息失败:', error)
    handleError(error, '发送消息失败')
    messageStore.endStreamingMessage()
  }
}

// 保留旧的代码审查方法（作为备用，非流式）
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
      
      showSuccess('代码审查完成')
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
      
      showSuccess('多文件代码审查完成')
    }
    
  } catch (error) {
    console.error('代码审查失败:', error)
    handleError(error, '代码审查失败')
  } finally {
    messageStore.isStreaming = false
    scrollToBottom()
  }
}

const handleCodeUpdate = (fileId, newContent) => {
  fileStore.updateFileContent(fileId, newContent)
}

const handleRemoveFile = (fileId) => {
  const files = fileStore.uploadedFiles
  const removedIndex = files.findIndex(f => f.file_id === fileId)
  
  fileStore.removeFile(fileId)
  
  // 如果删除后还有文件，将焦点移到相邻的文件Tab
  nextTick(() => {
    const remainingFiles = fileStore.uploadedFiles
    if (remainingFiles.length > 0) {
      // 优先聚焦下一个，如果是最后一个则聚焦前一个
      const nextIndex = removedIndex < remainingFiles.length ? removedIndex : removedIndex - 1
      const tabs = fileTabsRef.value?.querySelectorAll('.file-tab')
      if (tabs && tabs[nextIndex]) {
        tabs[nextIndex].focus()
      }
    }
  })
}

// 触发文件上传
const handleFileUpload = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.multiple = true
  input.accept = '.py,.js,.ts,.jsx,.tsx,.vue,.java,.go,.rs,.cpp,.c,.cs,.php,.rb,.swift,.kt'
  input.onchange = async (e) => {
    const files = Array.from(e.target.files)
    if (files.length === 0) return
    
    isUploadingFile.value = true
    
    try {
      for (const file of files) {
        const content = await readFileContent(file)
        const fileId = generateFileId()
        
        // 上传文件到后端
        await fileAPI.uploadFile({
          session_id: sessionStore.currentSessionId,
          file_id: fileId,
          filename: file.name,
          content: content
        })
        
        // 添加到 store
        fileStore.addFile({
          file_id: fileId,
          filename: file.name
        })
        
        // 保存文件内容
        fileStore.setFileContent(fileId, content)
      }
      
      showSuccess(`成功上传 ${files.length} 个文件`)
    } catch (error) {
      console.error('文件上传失败:', error)
      handleError(error, '文件上传失败')
    } finally {
      isUploadingFile.value = false
    }
  }
  input.click()
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
  e.preventDefault()
  isResizing.value = true
  startX.value = e.clientX
  
  // 获取代码编辑器当前宽度
  const codeElement = document.querySelector('.code-panel')
  startCodeWidth.value = codePanelWidth.value || codeElement.offsetWidth
  
  // 使用 passive: false 以允许 preventDefault
  document.addEventListener('mousemove', handleResize, { passive: false })
  document.addEventListener('mouseup', stopResize)
  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'
  
  // 防止文本选择和拖拽
  document.body.style.webkitUserSelect = 'none'
  document.body.style.mozUserSelect = 'none'
  document.body.style.msUserSelect = 'none'
}

const handleResize = (e) => {
  if (!isResizing.value) return
  
  e.preventDefault()
  
  // 取消之前的 requestAnimationFrame
  if (rafId !== null) {
    cancelAnimationFrame(rafId)
  }
  
  // 计算新宽度
  const deltaX = e.clientX - startX.value
  const newCodeWidth = startCodeWidth.value - deltaX
  
  // 代码编辑器最小300px，最大不超过窗口宽度的60%
  const minCodeWidth = 300
  const maxCodeWidth = window.innerWidth * 0.6
  
  // 限制宽度范围
  const clampedWidth = Math.max(minCodeWidth, Math.min(newCodeWidth, maxCodeWidth))
  
  // 存储待更新的宽度
  pendingWidth = clampedWidth
  
  // 使用 requestAnimationFrame 更新 UI
  rafId = requestAnimationFrame(() => {
    if (pendingWidth !== null) {
      codePanelWidth.value = pendingWidth
      pendingWidth = null
    }
    rafId = null
  })
}

const stopResize = () => {
  isResizing.value = false
  
  // 取消待处理的 requestAnimationFrame
  if (rafId !== null) {
    cancelAnimationFrame(rafId)
    rafId = null
  }
  
  // 如果有待更新的宽度，立即应用
  if (pendingWidth !== null) {
    codePanelWidth.value = pendingWidth
    pendingWidth = null
  }
  
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
  document.body.style.cursor = ''
  document.body.style.userSelect = ''
  document.body.style.webkitUserSelect = ''
  document.body.style.mozUserSelect = ''
  document.body.style.msUserSelect = ''
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
          showWarning('图片大小不能超过5MB')
          return
        }
        const reader = new FileReader()
        reader.onload = (e) => {
          backgroundImage.value = e.target.result
          showSuccess('背景图片上传成功')
        }
        reader.readAsDataURL(file)
      }
    }
    input.click()
  } else if (command === 'clear') {
    // 清除背景图片
    backgroundImage.value = null
    showSuccess('背景图片已清除')
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

// 文件Tab相关功能
// 获取文件图标
const getFileIcon = (filename) => {
  const ext = filename.split('.').pop().toLowerCase()
  const iconMap = {
    'py': 'DocumentCopy',
    'js': 'DocumentCopy',
    'ts': 'DocumentCopy',
    'jsx': 'DocumentCopy',
    'tsx': 'DocumentCopy',
    'vue': 'DocumentCopy',
    'java': 'DocumentCopy',
    'go': 'DocumentCopy',
    'rs': 'DocumentCopy',
    'cpp': 'DocumentCopy',
    'c': 'DocumentCopy',
    'cs': 'DocumentCopy',
    'php': 'DocumentCopy',
    'rb': 'DocumentCopy',
    'swift': 'DocumentCopy',
    'kt': 'DocumentCopy'
  }
  return iconMap[ext] || 'Document'
}

// 获取文件图标颜色
const getFileIconColor = (filename) => {
  const ext = filename.split('.').pop().toLowerCase()
  const colorMap = {
    'py': '#3776ab',    // Python blue
    'js': '#f7df1e',    // JavaScript yellow
    'ts': '#3178c6',    // TypeScript blue
    'jsx': '#61dafb',   // React cyan
    'tsx': '#61dafb',   // React cyan
    'vue': '#42b883',   // Vue green
    'java': '#007396',  // Java blue
    'go': '#00add8',    // Go cyan
    'rs': '#ce422b',    // Rust orange
    'cpp': '#00599c',   // C++ blue
    'c': '#555555',     // C gray
    'cs': '#68217a',    // C# purple
    'php': '#777bb4',   // PHP purple
    'rb': '#cc342d',    // Ruby red
    'swift': '#f05138', // Swift orange
    'kt': '#7f52ff'     // Kotlin purple
  }
  return colorMap[ext] || '#909399'
}

// Tab滚动功能
const scrollTabs = (direction) => {
  if (!fileTabsRef.value) return
  
  const scrollAmount = 200
  const currentScroll = fileTabsRef.value.scrollLeft
  
  if (direction === 'left') {
    fileTabsRef.value.scrollTo({
      left: currentScroll - scrollAmount,
      behavior: 'smooth'
    })
  } else {
    fileTabsRef.value.scrollTo({
      left: currentScroll + scrollAmount,
      behavior: 'smooth'
    })
  }
}

// 检查是否需要显示滚动按钮
const checkScrollButtons = () => {
  if (!fileTabsRef.value) return
  
  const { scrollWidth, clientWidth } = fileTabsRef.value
  showScrollButtons.value = scrollWidth > clientWidth
}

// 快捷键支持
const handleKeyDown = (e) => {
  // Ctrl+数字键切换文件
  if (e.ctrlKey && e.key >= '1' && e.key <= '9') {
    e.preventDefault()
    const index = parseInt(e.key) - 1
    const files = fileStore.uploadedFiles
    if (files[index]) {
      fileStore.setCurrentFile(files[index].file_id)
    }
  }
  // Ctrl+W 关闭当前文件
  else if (e.ctrlKey && e.key === 'w') {
    e.preventDefault()
    if (fileStore.currentFileId) {
      handleRemoveFile(fileStore.currentFileId)
    }
  }
  // 左右箭头键切换文件Tab（仅当焦点在文件Tab上时）
  else if ((e.key === 'ArrowLeft' || e.key === 'ArrowRight') && 
           e.target.classList?.contains('file-tab')) {
    e.preventDefault()
    const files = fileStore.uploadedFiles
    const currentIndex = files.findIndex(f => f.file_id === fileStore.currentFileId)
    
    if (currentIndex === -1) return
    
    let nextIndex
    if (e.key === 'ArrowLeft') {
      // 向左切换
      nextIndex = currentIndex > 0 ? currentIndex - 1 : files.length - 1
    } else {
      // 向右切换
      nextIndex = currentIndex < files.length - 1 ? currentIndex + 1 : 0
    }
    
    fileStore.setCurrentFile(files[nextIndex].file_id)
    
    // 让新的Tab获得焦点
    nextTick(() => {
      const tabs = fileTabsRef.value?.querySelectorAll('.file-tab')
      if (tabs && tabs[nextIndex]) {
        tabs[nextIndex].focus()
      }
    })
  }
}

// 监听文件列表变化，更新滚动按钮
watch(() => fileStore.uploadedFiles.length, async () => {
  await nextTick()
  checkScrollButtons()
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
  // 添加快捷键监听
  document.addEventListener('keydown', handleKeyDown)
  
  // 检查滚动按钮
  await nextTick()
  checkScrollButtons()
  
  // 监听窗口大小变化
  window.addEventListener('resize', checkScrollButtons)
  
  // 创建ResizeObserver监听代码面板宽度变化，用于差异对话框定位
  const codePanelResizeObserver = new ResizeObserver((entries) => {
    for (const entry of entries) {
      if (entry.target.classList.contains('code-panel')) {
        const codePanelWidth = entry.contentRect.width
        document.documentElement.style.setProperty('--code-panel-width', `${codePanelWidth}px`)
      }
    }
  })
  
  // 等待DOM渲染后再监听代码面板
  await nextTick()
  const codePanel = document.querySelector('.code-panel')
  if (codePanel) {
    codePanelResizeObserver.observe(codePanel)
  }
  
  // 保存observer到组件实例，以便在onUnmounted中清理
  window.__codePanelResizeObserver__ = codePanelResizeObserver
  
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
    showErrorNotification(error, '初始化失败', {
      duration: 0,  // 不自动关闭
      message: '应用初始化失败，请刷新页面重试。如果问题持续存在，请检查网络连接或联系技术支持。'
    })
  } finally {
    // 初始化完成
    setTimeout(() => {
      isInitializing.value = false
    }, 500) // 延迟显示，确保骨架屏至少显示500ms
  }
})

onUnmounted(() => {
  // 清理快捷键监听
  document.removeEventListener('keydown', handleKeyDown)
  // 清理窗口大小监听
  window.removeEventListener('resize', checkScrollButtons)
  // 清理ResizeObserver
  if (window.__codePanelResizeObserver__) {
    window.__codePanelResizeObserver__.disconnect()
    window.__codePanelResizeObserver__ = null
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
  /* CSS变量：代码面板宽度，用于差异对话框定位 */
  --code-panel-width: 600px;
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
  padding: 16px 0;
}

.sidebar.collapsed .sidebar-header .header-left {
  display: none;
}

/* 收缩后的操作按钮 */
.collapsed-actions {
  padding: 16px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}

/* 返回门户按钮 */
.back-to-portal {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
}

.portal-btn {
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%) !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
  transition: all 0.3s ease;
}

.portal-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
}

.portal-btn:active {
  transform: scale(0.95);
}

/* 收缩状态下的返回按钮位置调整 */
.sidebar.collapsed .back-to-portal {
  left: 50%;
}

/* 拖拽手柄 */
.resize-handle {
  width: 4px;
  cursor: col-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
  flex-shrink: 0;
  position: relative;
  z-index: 10;
  margin: 0 -3px;  /* 缩小与两侧的间隔 */
  will-change: background;  /* GPU 加速 */
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
  transition: all 0.2s ease;
  will-change: transform;  /* GPU 加速 */
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
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  overflow: hidden;
  margin-left: -3px;  /* 缩小与对话区域的间隔 */
  will-change: width;  /* GPU 加速宽度变化 */
  position: relative;
  z-index: 1;  /* 确保在正常层级，但低于对话框(2100) */
  /* 拖拽时不使用过渡动画，提高性能 */
}

/* 拖拽时禁用过渡动画以提高性能 */
.code-panel.no-transition,
.code-panel.no-transition * {
  transition: none !important;
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

/* 文件Tab容器 */
.file-tabs-container {
  display: flex;
  align-items: center;
  height: 100%;
  position: relative;
  flex: 1;
  min-width: 0;
}

.file-tabs {
  display: flex;
  height: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  flex: 1;
  min-width: 0;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.file-tabs::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.tab-scroll-btn {
  flex-shrink: 0;
  width: 32px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8edf2 100%);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
  color: #606266;
  border-right: 1px solid #e4e7ed;
}

.tab-scroll-btn:hover {
  background: linear-gradient(135deg, #e8edf2 0%, #dce4ec 100%);
  color: #303133;
}

.tab-scroll-btn.left {
  border-right: 1px solid #e4e7ed;
}

.tab-scroll-btn.right {
  border-left: 1px solid #e4e7ed;
  border-right: none;
}

.file-tab {
  height: 100%;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  border-right: 1px solid #e4e7ed;
  background: #fafbfc;
  transition: all 0.2s ease;
  white-space: nowrap;
  font-size: 13px;
  color: #606266;
  position: relative;
  flex-shrink: 0;
  min-width: 120px;
  max-width: 200px;
}

.file-tab::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: transparent;
  transition: all 0.2s ease;
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
  background: linear-gradient(90deg, #409eff 0%, #66b1ff 100%);
}

/* Tab键焦点样式 */
.file-tab:focus {
  outline: none;
  box-shadow: inset 0 0 0 2px #409eff;
}

.file-tab:focus-visible {
  outline: 2px solid #409eff;
  outline-offset: -2px;
}

.file-tab .file-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.file-tab .file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-tab .close-icon {
  font-size: 14px;
  flex-shrink: 0;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s ease;
  border-radius: 4px;
}

.file-tab:hover .close-icon {
  opacity: 0.6;
}

.file-tab .close-icon:hover {
  opacity: 1;
  color: #f56c6c;
  transform: scale(1.2);
}

.file-tab .close-icon:focus {
  opacity: 1;
  outline: 2px solid #409eff;
  outline-offset: 2px;
}

.file-tab .close-icon:focus-visible {
  opacity: 1;
  background: #f0f2f5;
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

/* 加载状态样式 */
.loading-state {
  padding: 20px;
  height: 100%;
  overflow: hidden;
}

/* 上传状态样式 */
.uploading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #409eff;
  animation: fadeIn 0.3s ease;
}

.uploading-state .upload-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.uploading-state p {
  font-size: 14px;
  margin: 0;
}

/* 空状态样式优化 */
.empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fafbfc;
  animation: fadeIn 0.3s ease;
}

.empty-state .empty-icon {
  font-size: 64px;
  color: #dcdfe6;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 500;
  color: #606266;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  color: #909399;
  margin: 0 0 20px 0;
}

/* 淡入淡出过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 渐入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========================================
   响应式适配
   ======================================== */

/* 平板设备 (1024px以下) */
@media (max-width: 1024px) {
  .review-workspace {
    flex-direction: column;
  }
  
  .code-panel {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 1000;  /* 确保低于对话框(2100) */
    width: 100% !important;
    max-width: 100%;
    background: white;
    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.15);
  }
  
  .code-panel.hidden {
    transform: translateX(100%);
  }
  
  .resize-handle {
    display: none;
  }
  
  .main-content {
    flex: 1;
    min-width: 0;
  }
  
  .sidebar {
    max-width: 280px;
  }
  
  .file-tab {
    min-width: 100px;
    max-width: 150px;
    font-size: 12px;
  }
}

/* 小屏幕设备 (768px以下) */
@media (max-width: 768px) {
  .review-workspace {
    padding: 0;
  }
  
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 999;
    width: 280px;
    max-width: 80vw;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
  }
  
  .sidebar:not(.collapsed) {
    transform: translateX(0);
  }
  
  .main-content {
    width: 100%;
    padding: 0;
  }
  
  .chat-header {
    padding: 12px 16px;
  }
  
  .chat-header h2 {
    font-size: 16px;
  }
  
  .chat-messages {
    padding: 12px;
  }
  
  .chat-input {
    padding: 12px;
  }
  
  .file-tabs-container {
    overflow-x: auto;
  }
  
  .file-tab {
    min-width: 80px;
    max-width: 120px;
    padding: 0 12px;
    font-size: 11px;
  }
  
  .code-header {
    height: 44px;
  }
  
  /* 添加移动端遮罩 */
  .sidebar:not(.collapsed)::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: -1;
  }
}

/* 超小屏幕设备 (480px以下) */
@media (max-width: 480px) {
  .sidebar {
    width: 100%;
    max-width: 100%;
  }
  
  .sidebar-header {
    padding: 12px;
  }
  
  .sidebar-header h3 {
    font-size: 16px;
  }
  
  .chat-header h2 {
    font-size: 14px;
  }
  
  .file-tab {
    min-width: 60px;
    max-width: 100px;
    padding: 0 8px;
    font-size: 10px;
  }
  
  .file-tab .file-icon {
    font-size: 14px;
  }
  
  .tab-scroll-btn {
    width: 28px;
    font-size: 14px;
  }
  
  /* 按钮组在小屏幕上调整大小 */
  .el-button {
    padding: 8px 12px;
    font-size: 12px;
  }
  
  .el-button--circle {
    padding: 6px;
  }
  
  /* 空状态在小屏幕上调整 */
  .empty-state .empty-icon {
    font-size: 48px;
  }
  
  .empty-state h3 {
    font-size: 16px;
  }
  
  .empty-state p {
    font-size: 12px;
  }
}

/* 横屏平板 (768px - 1024px, 横向) */
@media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
  .review-workspace {
    flex-direction: row;
  }
  
  .sidebar {
    position: relative;
    transform: none;
    width: 260px;
  }
  
  .code-panel {
    position: relative;
    width: 40% !important;
  }
  
  .main-content {
    flex: 1;
    min-width: 0;
  }
}

/* 高分辨率屏幕优化 */
@media (min-width: 1920px) {
  .review-workspace {
    max-width: 2560px;
    margin: 0 auto;
  }
  
  .sidebar {
    width: 320px;
  }
  
  .chat-messages {
    padding: 24px;
  }
  
  .file-tab {
    min-width: 140px;
    max-width: 240px;
  }
}

/* 打印样式 */
@media print {
  .sidebar,
  .chat-input,
  .code-header,
  .resize-handle {
    display: none !important;
  }
  
  .main-content,
  .code-panel {
    width: 100% !important;
    max-width: 100% !important;
  }
  
  .chat-messages {
    height: auto !important;
    overflow: visible !important;
  }
}
</style>

