<template>
  <div class="message-item" :class="message.role">
    <div class="avatar">
      <el-avatar v-if="message.role === 'user'" :size="36">
        <el-icon><User /></el-icon>
      </el-avatar>
      <el-avatar v-else :size="36" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <el-icon><Cpu /></el-icon>
      </el-avatar>
    </div>

    <div class="content">
      <div class="role-name">
        {{ message.role === 'user' ? '你' : 'AI助手' }}
      </div>
      
      <!-- 思考过程展示 (仅AI消息) -->
      <div v-if="message.role === 'assistant' && (message.streaming || message.thinking_process || (message.message_id === messageStore.streamingMessage?.message_id && messageStore.thinkingProcess))" class="thinking-section">
        <div class="thinking-header" @click="toggleThinking">
          <el-icon><el-icon-view v-if="showThinking" /><el-icon-hide v-else /></el-icon>
          <span>思考过程</span>
          <el-icon class="toggle-icon" :class="{ collapsed: !showThinking }">
            <ArrowDown />
          </el-icon>
        </div>
        <div v-if="showThinking && thinkingContent" class="thinking-content">
          {{ thinkingContent }}
        </div>
      </div>
      
      <div class="message-content">
        <!-- 流式消息且内容为空：显示加载状态 -->
        <div v-if="message.role === 'assistant' && message.streaming && !message.content" class="loading-indicator">
          <el-icon class="rotating"><Loading /></el-icon>
          <span>正在思考中...</span>
        </div>
        <!-- 流式展示使用打字机效果 -->
        <TypewriterText 
          v-else-if="message.role === 'assistant' && message.streaming" 
          :content="message.content"
          :enable-typewriter="false"
        />
        <!-- 非流式展示使用 Markdown 渲染 -->
        <MarkdownRenderer 
          v-else 
          :content="message.content" 
          :dark-mode="false" 
        />
      </div>
      
      <div class="message-actions">
        <span class="time">{{ formatTime(message.created_at) }}</span>
        
        <!-- 停止按钮（仅在流式输出时显示） -->
        <el-button
          v-if="message.streaming && message.role === 'assistant'"
          link
          :icon="CircleClose"
          size="small"
          type="danger"
          @click="handleStop"
        >
          停止生成
        </el-button>
        
        <el-button
          v-else
          link
          :icon="DocumentCopy"
          size="small"
          @click="handleCopy"
        >
          复制
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { User, Cpu, DocumentCopy, Loading, CircleClose, ArrowDown, View as ElIconView, Hide as ElIconHide } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { formatTime } from '@/utils/format'
import { useMessageStore } from '@/stores/message'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'
import TypewriterText from './TypewriterText.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

const messageStore = useMessageStore()
const showThinking = ref(true)

// 获取思考过程内容（优先使用消息自带的，否则使用store中的）
const thinkingContent = computed(() => {
  // 如果是当前正在流式输出的消息，使用store中的实时思考过程
  if (props.message.message_id === messageStore.streamingMessage?.message_id && messageStore.thinkingProcess) {
    return messageStore.thinkingProcess
  }
  // 否则使用消息中保存的思考过程
  return props.message.thinking_process
})

const toggleThinking = () => {
  showThinking.value = !showThinking.value
}

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(props.message.content)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const handleStop = () => {
  messageStore.abortStreaming()
}
</script>

<style scoped>
.message-item {
  display: flex;
  gap: 12px;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.avatar {
  flex-shrink: 0;
}

.content {
  flex: 1;
  min-width: 0;
}

.role-name {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.message-content {
  background: #fff;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  word-wrap: break-word;
}

.message-item.assistant .message-content {
  background: #f5f7fa;
}

.message-actions {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.time {
  font-size: 12px;
  color: #909399;
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
}

.loading-indicator .rotating {
  animation: rotate 1s linear infinite;
  font-size: 18px;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 思考过程样式 */
.thinking-section {
  margin-bottom: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
  background: #f0f9ff;
}

.thinking-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #e0f2fe;
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.thinking-header:hover {
  background: #bae6fd;
}

.thinking-header span {
  flex: 1;
  font-size: 13px;
  font-weight: 500;
  color: #0369a1;
}

.thinking-header .toggle-icon {
  transition: transform 0.3s;
  color: #0369a1;
}

.thinking-header .toggle-icon.collapsed {
  transform: rotate(-90deg);
}

.thinking-content {
  padding: 12px 16px;
  font-size: 13px;
  line-height: 1.6;
  color: #475569;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 200px;
  overflow-y: auto;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 200px;
  }
}
</style>

