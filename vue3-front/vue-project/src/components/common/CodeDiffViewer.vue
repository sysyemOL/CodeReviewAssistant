<template>
  <div class="code-diff-viewer">
    <div class="diff-header">
      <div class="header-left">
        <el-button 
          :icon="Close" 
          circle 
          size="small" 
          title="返回代码编辑器" 
          @click="handleClose"
          class="close-btn"
        />
        <el-icon><Document /></el-icon>
        <span class="file-name">{{ fileName }}</span>
      </div>
      <div class="header-right">
        <el-radio-group v-model="viewMode" size="small">
          <el-radio-button value="side-by-side">
            <el-icon><Grid /></el-icon>
            并排对比
          </el-radio-button>
          <el-radio-button value="inline">
            <el-icon><List /></el-icon>
            行内对比
          </el-radio-button>
        </el-radio-group>
        <el-button :icon="DocumentCopy" circle size="small" title="复制差异" @click="handleCopyDiff" />
        <el-button :icon="Download" circle size="small" title="下载差异" @click="handleDownloadDiff" />
      </div>
    </div>
    
    <div class="diff-content" v-html="diffHtml"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Document, Grid, List, DocumentCopy, Download, Close } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import * as Diff2Html from 'diff2html'
import 'diff2html/bundles/css/diff2html.min.css'

const props = defineProps({
  fileName: {
    type: String,
    default: 'code.py'
  },
  originalCode: {
    type: String,
    required: true
  },
  modifiedCode: {
    type: String,
    required: true
  },
  language: {
    type: String,
    default: 'python'
  }
})

const emit = defineEmits(['close'])

const viewMode = ref('side-by-side')

// 关闭差异视图
const handleClose = () => {
  emit('close')
}

// 生成unified diff格式
const generateUnifiedDiff = () => {
  const originalLines = props.originalCode.split('\n')
  const modifiedLines = props.modifiedCode.split('\n')
  
  // 简单的diff算法（实际应用中应使用更完善的diff算法）
  let diff = `--- a/${props.fileName}\n+++ b/${props.fileName}\n`
  diff += `@@ -1,${originalLines.length} +1,${modifiedLines.length} @@\n`
  
  const maxLines = Math.max(originalLines.length, modifiedLines.length)
  for (let i = 0; i < maxLines; i++) {
    const origLine = originalLines[i] || ''
    const modLine = modifiedLines[i] || ''
    
    if (origLine !== modLine) {
      if (origLine && i < originalLines.length) {
        diff += `-${origLine}\n`
      }
      if (modLine && i < modifiedLines.length) {
        diff += `+${modLine}\n`
      }
    } else {
      diff += ` ${origLine}\n`
    }
  }
  
  return diff
}

// 生成diff HTML
const diffHtml = computed(() => {
  const unifiedDiff = generateUnifiedDiff()
  
  const outputFormat = viewMode.value === 'side-by-side' 
    ? Diff2Html.OutputFormatType.SIDE_BY_SIDE 
    : Diff2Html.OutputFormatType.LINE_BY_LINE
  
  return Diff2Html.html(unifiedDiff, {
    drawFileList: false,
    matching: 'lines',
    outputFormat: outputFormat,
    highlight: true,
    renderNothingWhenEmpty: false
  })
})

// 复制差异
const handleCopyDiff = async () => {
  try {
    const diff = generateUnifiedDiff()
    await navigator.clipboard.writeText(diff)
    ElMessage.success('差异已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

// 下载差异
const handleDownloadDiff = () => {
  try {
    const diff = generateUnifiedDiff()
    const blob = new Blob([diff], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${props.fileName}.diff`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    ElMessage.success('差异文件已下载')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}
</script>

<style scoped>
.code-diff-viewer {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e4e7ed;
}

.diff-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.close-btn {
  margin-right: 4px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background-color: #f56c6c;
  color: white;
  border-color: #f56c6c;
}

.file-name {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.diff-content {
  flex: 1;
  overflow: auto;
  padding: 16px;
}

/* 优化diff2html样式 */
.diff-content :deep(.d2h-wrapper) {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
}

.diff-content :deep(.d2h-file-header) {
  background: #f5f7fa;
  padding: 8px 12px;
  border-radius: 4px 4px 0 0;
  font-weight: 600;
}

.diff-content :deep(.d2h-code-line) {
  padding: 4px 8px;
  line-height: 1.6;
}

.diff-content :deep(.d2h-ins) {
  background: #e6f7e6;
}

.diff-content :deep(.d2h-del) {
  background: #ffe6e6;
}

.diff-content :deep(.d2h-code-line-ctn) {
  word-wrap: break-word;
  white-space: pre-wrap;
}

/* 滚动条样式 */
.diff-content::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.diff-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.diff-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.diff-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>

