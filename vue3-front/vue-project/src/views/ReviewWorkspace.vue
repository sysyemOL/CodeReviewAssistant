<template>
  <div class="review-workspace">
    <!-- 左侧：历史会话列表 -->
    <aside class="sidebar" :class="{ collapsed: appStore.sidebarCollapsed }">
      <div class="sidebar-header">
        <h3 v-if="!appStore.sidebarCollapsed">历史对话</h3>
        <el-button 
          :icon="Plus" 
          type="primary" 
          @click="handleCreateSession"
          :title="appStore.sidebarCollapsed ? '新对话' : ''"
        >
          <span v-if="!appStore.sidebarCollapsed">新对话</span>
        </el-button>
      </div>
      
      <SessionList v-if="!appStore.sidebarCollapsed" />
      
      <div class="sidebar-footer">
        <el-button 
          :icon="appStore.sidebarCollapsed ? Expand : Fold" 
          circle
          @click="appStore.toggleSidebar"
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

    <!-- 右侧：代码编辑器 -->
    <aside class="code-panel" :class="{ hidden: !fileStore.currentFile }">
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
      </div>
      
      <div class="code-editor">
        <CodeEditor 
          v-if="fileStore.currentFile"
          :file-id="fileStore.currentFileId"
          :language="getFileLanguage(fileStore.currentFile.filename)"
          :content="fileStore.currentFileContent"
          @update="handleCodeUpdate"
        />
        <div v-else class="empty-state">
          <el-empty description="暂无文件" />
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus, Expand, Fold, Close } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useAppStore } from '@/stores/app'
import { useSessionStore } from '@/stores/session'
import { useMessageStore } from '@/stores/message'
import { useFileStore } from '@/stores/file'
import SessionList from '@/components/sidebar/SessionList.vue'
import MessageList from '@/components/chat/MessageList.vue'
import InputBox from '@/components/chat/InputBox.vue'
import CodeEditor from '@/components/common/CodeEditor.vue'
import { getLanguageFromFilename } from '@/utils/format'

const appStore = useAppStore()
const sessionStore = useSessionStore()
const messageStore = useMessageStore()
const fileStore = useFileStore()

const messagesContainer = ref(null)

const currentSessionTitle = computed(() => {
  return sessionStore.currentSession?.title || 'AI代码Review助手'
})

const getFileLanguage = (filename) => {
  return getLanguageFromFilename(filename)
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
  
  // 添加用户消息
  messageStore.addUserMessage(sessionStore.currentSessionId, content)
  
  // 处理文件上传
  if (files && files.length > 0) {
    // TODO: 实现文件上传逻辑
    console.log('上传文件:', files)
  }
  
  // 滚动到底部
  scrollToBottom()
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
.review-workspace {
  display: flex;
  width: 100vw;
  height: 100vh;
  background: #f0f2f5;
  overflow: hidden;
  gap: 12px;
  padding: 12px;
  box-sizing: border-box;
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
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
}

.sidebar-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: center;
  background: #fafbfc;
}

/* 中间主内容区 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
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
  background: #ffffff;
  border-top: 1px solid #f0f0f0;
  box-shadow: 0 -2px 8px 0 rgba(0, 0, 0, 0.04);
}

/* 右侧代码面板 */
.code-panel {
  width: 550px;
  min-width: 550px;
  background: #ffffff;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  overflow: hidden;
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
  overflow-x: auto;
  background: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
  box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.04);
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

.code-editor {
  flex: 1;
  overflow: hidden;
  background: #1e1e1e;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafbfc;
}
</style>

