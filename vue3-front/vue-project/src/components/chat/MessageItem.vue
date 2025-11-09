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
      
      <div class="message-content">
        <MarkdownRenderer :content="message.content" :dark-mode="false" />
      </div>
      
      <div class="message-actions">
        <span class="time">{{ formatTime(message.created_at) }}</span>
        <el-button
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
import { User, Cpu, DocumentCopy } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { formatTime } from '@/utils/format'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(props.message.content)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
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
</style>

