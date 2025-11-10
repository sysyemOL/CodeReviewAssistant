<template>
  <div class="monaco-diff-editor">
    <div class="diff-header">
      <div class="header-left">
        <el-icon><Document /></el-icon>
        <span class="file-name">{{ fileName }}</span>
        <el-tag size="small" type="info">原始 vs 建议</el-tag>
      </div>
      <div class="header-right">
        <el-button 
          type="primary" 
          size="small" 
          :icon="Check"
          @click="handleApply"
        >
          应用建议
        </el-button>
      </div>
    </div>
    
    <div class="diff-editor-container" ref="diffEditorContainer"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { Document, Check } from '@element-plus/icons-vue'
import * as monaco from 'monaco-editor'
import { ElMessage } from 'element-plus'

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
  },
  theme: {
    type: String,
    default: 'vs'
  }
})

const emit = defineEmits(['apply', 'close'])

const diffEditorContainer = ref(null)
let diffEditor = null

onMounted(() => {
  console.log('🎨 MonacoDiffEditor onMounted 开始')
  console.log('  - 容器元素:', diffEditorContainer.value)
  console.log('  - 容器尺寸:', {
    offsetWidth: diffEditorContainer.value?.offsetWidth,
    offsetHeight: diffEditorContainer.value?.offsetHeight
  })
  console.log('  - 原始代码长度:', props.originalCode?.length || 0)
  console.log('  - 修改后代码长度:', props.modifiedCode?.length || 0)
  console.log('  - 语言:', props.language)
  
  if (!diffEditorContainer.value) {
    console.error('❌ 容器元素不存在！')
    return
  }

  // 使用 requestAnimationFrame 确保 DOM 完全渲染后再初始化
  requestAnimationFrame(() => {
    // 再增加一个延迟，确保 CSS 动画和布局完全稳定
    setTimeout(() => {
      console.log('⏱️ 延迟后的容器尺寸:', {
        offsetWidth: diffEditorContainer.value?.offsetWidth,
        offsetHeight: diffEditorContainer.value?.offsetHeight,
        clientWidth: diffEditorContainer.value?.clientWidth,
        clientHeight: diffEditorContainer.value?.clientHeight
      })
      
      // 检查容器高度是否合理
      const containerHeight = diffEditorContainer.value?.offsetHeight || 0
      if (containerHeight < 100) {
        console.warn('⚠️ 容器高度过小:', containerHeight, '尝试强制设置高度')
        diffEditorContainer.value.style.minHeight = '500px'
        diffEditorContainer.value.style.height = '100%'
      }
      
      try {
        console.log('🚀 开始创建Monaco Diff Editor...')
        
        // 创建 Diff Editor
        diffEditor = monaco.editor.createDiffEditor(diffEditorContainer.value, {
          automaticLayout: true,
          readOnly: false,
          renderSideBySide: true,
          originalEditable: false,
          minimap: {
            enabled: true
          },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          wordWrap: 'on',
          theme: props.theme,
          padding: {
            top: 16,
            bottom: 16
          }
        })
        
        // 保存引用到 DOM 元素，方便调试
        diffEditorContainer.value.__monacoEditor = diffEditor
        
        console.log('✅ Monaco Diff Editor创建成功')

        // 设置模型
        console.log('📝 创建代码模型...')
        const originalModel = monaco.editor.createModel(props.originalCode, props.language)
        const modifiedModel = monaco.editor.createModel(props.modifiedCode, props.language)
        
        console.log('✅ 模型创建成功')
        console.log('  - 原始模型行数:', originalModel.getLineCount())
        console.log('  - 修改后模型行数:', modifiedModel.getLineCount())

        diffEditor.setModel({
          original: originalModel,
          modified: modifiedModel
        })
        
        console.log('✅ 模型设置成功')
        
        // 多次强制布局更新，确保渲染正确
        const forceLayout = () => {
          if (diffEditor) {
            const dims = {
              width: diffEditorContainer.value?.offsetWidth || 800,
              height: diffEditorContainer.value?.offsetHeight || 500
            }
            console.log('🔄 强制布局更新:', dims)
            diffEditor.layout(dims)
          }
        }
        
        // 立即布局一次
        forceLayout()
        
        // 100ms 后再次布局
        setTimeout(forceLayout, 100)
        
        // 300ms 后最后一次布局
        setTimeout(() => {
          forceLayout()
          console.log('✅ 所有布局更新完成')
        }, 300)
        
      } catch (error) {
        console.error('❌ Monaco Editor初始化失败:', error)
      }
    }, 300) // 增加延迟到 300ms
  })
})

onUnmounted(() => {
  if (diffEditor) {
    const model = diffEditor.getModel()
    if (model) {
      model.original?.dispose()
      model.modified?.dispose()
    }
    diffEditor.dispose()
  }
})

// 监听props变化
watch(() => props.originalCode, (newCode) => {
  if (diffEditor) {
    const model = diffEditor.getModel()
    if (model?.original) {
      model.original.setValue(newCode)
    }
  }
})

watch(() => props.modifiedCode, (newCode) => {
  if (diffEditor) {
    const model = diffEditor.getModel()
    if (model?.modified) {
      model.modified.setValue(newCode)
    }
  }
})

watch(() => props.language, (newLanguage) => {
  if (diffEditor) {
    const model = diffEditor.getModel()
    if (model) {
      monaco.editor.setModelLanguage(model.original, newLanguage)
      monaco.editor.setModelLanguage(model.modified, newLanguage)
    }
  }
})

watch(() => props.theme, (newTheme) => {
  if (diffEditor) {
    monaco.editor.setTheme(newTheme)
  }
})

// 应用建议
const handleApply = () => {
  if (diffEditor) {
    const model = diffEditor.getModel()
    if (model?.modified) {
      const modifiedContent = model.modified.getValue()
      emit('apply', modifiedContent)
      ElMessage.success('代码建议已应用')
    }
  }
}

</script>

<style scoped>
.monaco-diff-editor {
  display: flex;
  flex-direction: column;
  flex: 1; /* 在flex容器中占满所有可用空间 */
  width: 100%;
  background: #fff;
  border-radius: 4px; /* 减小圆角 */
  overflow: hidden;
  border: 1px solid #e4e7ed;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08); /* 减小阴影 */
  margin: 0; /* 确保无外边距 */
}

.diff-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: linear-gradient(135deg, #f5f7fa 0%, #eef2f7 100%);
  border-bottom: 1px solid #e4e7ed;
  flex-shrink: 0; /* 防止header被压缩 */
  margin: 0; /* 确保无外边距 */
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
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

.diff-editor-container {
  flex: 1; /* 占满所有可用空间 */
  overflow: hidden;
  background: #f5f5f5;
  margin: 0; /* 确保无外边距 */
  padding: 0; /* 确保无内边距 */
}

</style>

