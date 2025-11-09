<template>
  <div class="message-list">
    <div v-if="messages.length === 0 && !isLoading" class="empty-state">
      <el-empty description="开始你的代码审查之旅吧！">
        <template #image>
          <el-icon :size="100" color="#909399">
            <ChatDotRound />
          </el-icon>
        </template>
      </el-empty>
    </div>

    <div v-else class="messages">
      <MessageItem
        v-for="message in messages"
        :key="message.message_id"
        :message="message"
      />
      
      <!-- 加载状态 -->
      <div v-if="isStreaming" class="loading-message">
        <div class="avatar">
          <el-avatar :size="36" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <el-icon><Cpu /></el-icon>
          </el-avatar>
        </div>
        <div class="content">
          <div class="role-name">AI助手</div>
          <div class="loading-indicator">
            <el-icon class="rotating"><Loading /></el-icon>
            <span>正在思考中...</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ChatDotRound, Cpu, Loading } from '@element-plus/icons-vue'
import { useMessageStore } from '@/stores/message'
import MessageItem from './MessageItem.vue'

const props = defineProps({
  sessionId: {
    type: String,
    default: null
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const messageStore = useMessageStore()

const messages = computed(() => {
  if (!props.sessionId) return []
  return messageStore.getSessionMessages(props.sessionId).value
})

const isStreaming = computed(() => {
  return messageStore.isStreaming
})
</script>

<style scoped>
.message-list {
  height: 100%;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 加载状态样式 */
.loading-message {
  display: flex;
  gap: 12px;
  animation: fadeIn 0.3s ease-in;
}

.loading-message .avatar {
  flex-shrink: 0;
}

.loading-message .content {
  flex: 1;
  min-width: 0;
}

.loading-message .role-name {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
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
</style>

