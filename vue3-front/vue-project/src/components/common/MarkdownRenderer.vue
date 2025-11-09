<template>
  <div class="markdown-renderer" :class="{ 'dark-theme': darkMode }" v-html="renderedContent"></div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  darkMode: {
    type: Boolean,
    default: false
  },
  codeTheme: {
    type: String,
    default: 'github-dark' // github-dark, monokai, atom-one-dark
  }
})

// 配置marked
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (error) {
        console.error('Highlight error:', error)
      }
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true,
  pedantic: false,
  smartLists: true,
  smartypants: true
})

const renderedContent = computed(() => {
  if (!props.content) return ''
  try {
    return marked(props.content)
  } catch (error) {
    console.error('Markdown parsing error:', error)
    return props.content
  }
})
</script>

<style scoped>
.markdown-renderer {
  font-size: 14px;
  line-height: 1.8;
  color: #303133;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.markdown-renderer.dark-theme {
  color: #e4e7ed;
}

/* 标题样式 */
.markdown-renderer :deep(h1),
.markdown-renderer :deep(h2),
.markdown-renderer :deep(h3),
.markdown-renderer :deep(h4),
.markdown-renderer :deep(h5),
.markdown-renderer :deep(h6) {
  margin: 24px 0 16px;
  font-weight: 600;
  line-height: 1.4;
}

.markdown-renderer :deep(h1) {
  font-size: 28px;
  border-bottom: 2px solid #e4e7ed;
  padding-bottom: 8px;
}

.markdown-renderer :deep(h2) {
  font-size: 24px;
  border-bottom: 1px solid #e4e7ed;
  padding-bottom: 6px;
}

.markdown-renderer :deep(h3) {
  font-size: 20px;
}

.markdown-renderer :deep(h4) {
  font-size: 18px;
}

.markdown-renderer :deep(h5) {
  font-size: 16px;
}

.markdown-renderer :deep(h6) {
  font-size: 14px;
  color: #606266;
}

/* 段落样式 */
.markdown-renderer :deep(p) {
  margin: 12px 0;
  line-height: 1.8;
}

/* 链接样式 */
.markdown-renderer :deep(a) {
  color: #409eff;
  text-decoration: none;
  transition: color 0.2s;
}

.markdown-renderer :deep(a:hover) {
  color: #66b1ff;
  text-decoration: underline;
}

/* 列表样式 */
.markdown-renderer :deep(ul),
.markdown-renderer :deep(ol) {
  padding-left: 28px;
  margin: 12px 0;
}

.markdown-renderer :deep(li) {
  margin: 6px 0;
}

.markdown-renderer :deep(ul li) {
  list-style-type: disc;
}

.markdown-renderer :deep(ol li) {
  list-style-type: decimal;
}

/* 引用块样式 */
.markdown-renderer :deep(blockquote) {
  margin: 16px 0;
  padding: 12px 20px;
  border-left: 4px solid #409eff;
  background: #f5f7fa;
  color: #606266;
  border-radius: 4px;
}

.markdown-renderer.dark-theme :deep(blockquote) {
  background: #2c3e50;
  border-left-color: #67c23a;
}

/* 代码块样式 */
.markdown-renderer :deep(pre) {
  margin: 16px 0;
  padding: 16px;
  background: #1e1e1e;
  border-radius: 8px;
  overflow-x: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.markdown-renderer :deep(pre code) {
  display: block;
  padding: 0;
  background: transparent;
  border: none;
  color: #d4d4d4;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
}

/* 行内代码样式 */
.markdown-renderer :deep(code) {
  padding: 2px 6px;
  background: #f5f7fa;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  color: #e83e8c;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
}

.markdown-renderer.dark-theme :deep(code) {
  background: #2c3e50;
  border-color: #4a5568;
  color: #ff79c6;
}

/* 表格样式 */
.markdown-renderer :deep(table) {
  margin: 16px 0;
  border-collapse: collapse;
  width: 100%;
  overflow: auto;
  display: block;
}

.markdown-renderer :deep(table th) {
  background: #f5f7fa;
  font-weight: 600;
  padding: 12px;
  border: 1px solid #e4e7ed;
  text-align: left;
}

.markdown-renderer :deep(table td) {
  padding: 12px;
  border: 1px solid #e4e7ed;
}

.markdown-renderer :deep(table tr:hover) {
  background: #fafbfc;
}

.markdown-renderer.dark-theme :deep(table th) {
  background: #2c3e50;
  border-color: #4a5568;
}

.markdown-renderer.dark-theme :deep(table td) {
  border-color: #4a5568;
}

.markdown-renderer.dark-theme :deep(table tr:hover) {
  background: #34495e;
}

/* 分割线样式 */
.markdown-renderer :deep(hr) {
  margin: 24px 0;
  border: none;
  border-top: 2px solid #e4e7ed;
}

.markdown-renderer.dark-theme :deep(hr) {
  border-top-color: #4a5568;
}

/* 图片样式 */
.markdown-renderer :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 任务列表样式 */
.markdown-renderer :deep(input[type="checkbox"]) {
  margin-right: 8px;
}

/* 强调样式 */
.markdown-renderer :deep(strong) {
  font-weight: 600;
  color: #303133;
}

.markdown-renderer.dark-theme :deep(strong) {
  color: #ffffff;
}

.markdown-renderer :deep(em) {
  font-style: italic;
}

/* 删除线样式 */
.markdown-renderer :deep(del) {
  text-decoration: line-through;
  color: #909399;
}

/* 滚动条样式 */
.markdown-renderer :deep(pre::-webkit-scrollbar) {
  height: 8px;
}

.markdown-renderer :deep(pre::-webkit-scrollbar-track) {
  background: #2d2d2d;
  border-radius: 4px;
}

.markdown-renderer :deep(pre::-webkit-scrollbar-thumb) {
  background: #555;
  border-radius: 4px;
}

.markdown-renderer :deep(pre::-webkit-scrollbar-thumb:hover) {
  background: #666;
}
</style>

