<template>
  <div class="typewriter-text">
    <div class="content" v-html="renderedContent"></div>
    <span v-if="isTyping" class="cursor">▋</span>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  speed: {
    type: Number,
    default: 30 // 打字速度（毫秒/字符）
  },
  enableTypewriter: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['complete'])

const displayedContent = ref('')
const isTyping = ref(false)
const currentIndex = ref(0)
let typewriterTimer = null

// 配置 marked
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {
        console.error('代码高亮失败:', err)
      }
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

// 渲染 Markdown
const renderedContent = computed(() => {
  if (!displayedContent.value) return ''
  try {
    return marked(displayedContent.value)
  } catch (error) {
    console.error('Markdown 渲染失败:', error)
    return displayedContent.value
  }
})

// 打字机效果
const startTypewriter = () => {
  if (!props.enableTypewriter || !props.content) {
    displayedContent.value = props.content
    emit('complete')
    return
  }

  isTyping.value = true
  currentIndex.value = 0
  displayedContent.value = ''

  const type = () => {
    if (currentIndex.value < props.content.length) {
      // 逐字添加
      displayedContent.value = props.content.substring(0, currentIndex.value + 1)
      currentIndex.value++
      
      typewriterTimer = setTimeout(type, props.speed)
    } else {
      // 打字完成
      isTyping.value = false
      emit('complete')
    }
  }

  type()
}

// 停止打字机
const stopTypewriter = () => {
  if (typewriterTimer) {
    clearTimeout(typewriterTimer)
    typewriterTimer = null
  }
  isTyping.value = false
  displayedContent.value = props.content
  currentIndex.value = props.content.length
  emit('complete')
}

// 跳过动画，立即显示全部内容
const skipAnimation = () => {
  stopTypewriter()
}

// 监听内容变化
watch(() => props.content, (newVal, oldVal) => {
  // 如果是增量更新（流式传输）
  if (newVal && newVal.startsWith(oldVal)) {
    // 直接追加新内容
    displayedContent.value = newVal
    currentIndex.value = newVal.length
  } else {
    // 完全新的内容，重新开始打字机效果
    if (typewriterTimer) {
      clearTimeout(typewriterTimer)
    }
    startTypewriter()
  }
})

onMounted(() => {
  if (props.content) {
    if (props.enableTypewriter) {
      startTypewriter()
    } else {
      displayedContent.value = props.content
    }
  }
})

// 暴露方法供外部调用
defineExpose({
  skipAnimation,
  stopTypewriter
})
</script>

<style scoped>
.typewriter-text {
  position: relative;
  display: inline-block;
  width: 100%;
}

.content {
  display: inline;
  line-height: 1.8;
  word-wrap: break-word;
  word-break: break-word;
}

.content :deep(h1),
.content :deep(h2),
.content :deep(h3),
.content :deep(h4),
.content :deep(h5),
.content :deep(h6) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.4;
}

.content :deep(h1) {
  font-size: 24px;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 8px;
}

.content :deep(h2) {
  font-size: 22px;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 6px;
}

.content :deep(h3) {
  font-size: 20px;
}

.content :deep(p) {
  margin-bottom: 16px;
  line-height: 1.8;
}

.content :deep(code) {
  padding: 2px 6px;
  margin: 0 2px;
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 3px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
}

.content :deep(pre) {
  margin: 16px 0;
  padding: 16px;
  background: #f6f8fa;
  border-radius: 6px;
  overflow-x: auto;
}

.content :deep(pre code) {
  padding: 0;
  margin: 0;
  background: transparent;
  border-radius: 0;
  font-size: 14px;
  line-height: 1.6;
}

.content :deep(ul),
.content :deep(ol) {
  padding-left: 24px;
  margin-bottom: 16px;
}

.content :deep(li) {
  margin-bottom: 8px;
  line-height: 1.8;
}

.content :deep(blockquote) {
  margin: 16px 0;
  padding: 8px 16px;
  border-left: 4px solid #dfe2e5;
  background: #f6f8fa;
  color: #6a737d;
}

.content :deep(table) {
  border-collapse: collapse;
  margin: 16px 0;
  width: 100%;
}

.content :deep(table th),
.content :deep(table td) {
  border: 1px solid #dfe2e5;
  padding: 8px 12px;
}

.content :deep(table th) {
  background: #f6f8fa;
  font-weight: 600;
}

.content :deep(a) {
  color: #0366d6;
  text-decoration: none;
}

.content :deep(a:hover) {
  text-decoration: underline;
}

.cursor {
  display: inline-block;
  margin-left: 2px;
  color: #409eff;
  animation: blink 1s infinite;
  font-weight: bold;
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}
</style>

