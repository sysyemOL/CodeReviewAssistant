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
      
      <div class="message-content" v-html="renderedContent"></div>
      
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
import { computed } from 'vue'
import { User, Cpu, DocumentCopy } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'
import { formatTime } from '@/utils/format'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

// 配置marked
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

const renderedContent = computed(() => {
  return marked(props.message.content)
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
  font-size: 14px;
  line-height: 1.6;
  color: #303133;
  word-wrap: break-word;
}

.message-item.assistant .message-content {
  background: #f5f7fa;
}

.message-content :deep(pre) {
  margin: 12px 0;
  border-radius: 6px;
  overflow-x: auto;
}

.message-content :deep(code) {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
}

.message-content :deep(p) {
  margin: 8px 0;
}

.message-content :deep(ul),
.message-content :deep(ol) {
  padding-left: 24px;
  margin: 8px 0;
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

