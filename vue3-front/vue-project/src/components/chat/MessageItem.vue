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
        
        <template v-else>
          <!-- 查看差异按钮（仅AI消息且包含代码建议时显示） -->
          <el-button
            v-if="message.role === 'assistant' && hasCodeSuggestions"
            link
            :icon="Switch"
            size="small"
            type="primary"
            @click="handleShowDiff"
          >
            查看代码差异
          </el-button>
          
          <!-- 智能应用按钮（仅当有结构化修改指令时显示） -->
          <el-button
            v-if="message.role === 'assistant' && hasStructuredInstructions"
            link
            :icon="CircleCheck"
            size="small"
            type="success"
            @click="handleApplyInstructions"
            title="智能应用修改指令（不替换整个文件）"
          >
            智能应用
          </el-button>
          
          <el-button
            link
            :icon="DocumentCopy"
            size="small"
            @click="handleCopy"
          >
            复制
          </el-button>
        </template>
      </div>
    </div>
    
    <!-- 代码差异对话框 -->
    <el-dialog
      v-model="showDiffDialog"
      :fullscreen="!fileStore.currentFile"
      :close-on-click-modal="false"
      :show-close="false"
      :z-index="2100"
      class="diff-dialog-wrapper"
      :class="{ 'with-editor': fileStore.currentFile, 'resizing': isResizing }"
    >
      <template #header>
        <div class="dialog-header-content">
          <span class="dialog-title">代码差异对比</span>
          <span v-if="fileStore.currentFile" class="drag-hint">可拖拽 · 双击重置</span>
        </div>
      </template>
      <MonacoDiffEditor
        v-if="showDiffDialog && currentCodePair"
        :file-name="currentCodePair.fileName"
        :original-code="currentCodePair.original"
        :modified-code="currentCodePair.modified"
        :language="currentCodePair.language"
        :theme="editorTheme"
        @apply="handleApplySuggestion"
        @close="handleCloseDiff"
      />
    </el-dialog>

    <!-- 全局浮动关闭按钮 - 固定在页面左下角 -->
    <el-button 
      v-if="showDiffDialog"
      :icon="Close"
      type="danger"
      circle
      size="large"
      @click="handleCloseDiff"
      class="global-floating-close-button"
      title="关闭差异视图 (ESC)"
    />
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { User, Cpu, DocumentCopy, Loading, CircleClose, ArrowDown, View as ElIconView, Hide as ElIconHide, Switch, Close, CircleCheck } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatTime } from '@/utils/format'
import { useMessageStore } from '@/stores/message'
import { useFileStore } from '@/stores/file'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'
import TypewriterText from './TypewriterText.vue'
import MonacoDiffEditor from '@/components/common/MonacoDiffEditor.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

const messageStore = useMessageStore()
const fileStore = useFileStore()
const showThinking = ref(true)
const showDiffDialog = ref(false)
const currentCodePair = ref(null)
const editorTheme = ref('vs')

// 拖拽相关状态
const isDragging = ref(false)
const dialogPosition = ref({ x: 0, y: 0 })
const dragStartPos = ref({ x: 0, y: 0 })

// Resize相关状态
const isResizing = ref(false)
const resizeDirection = ref('')
const resizeStartPos = ref({ x: 0, y: 0 })
const dialogSize = ref({ width: 0, height: 0 })
const initialDialogSize = ref({ width: 0, height: 0 })

// 初始化对话框大小 - 设置一个合理的初始大小
const initDialogSize = () => {
  const codePanelWidth = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--code-panel-width') || '600')
  // 初始宽度为可用宽度的80%，最小800px
  const availableWidth = window.innerWidth - codePanelWidth
  const width = Math.max(800, Math.min(availableWidth * 0.8, availableWidth - 40))
  // 减小初始高度，让代码区域更紧凑：视口高度的75%，最小600px
  const height = Math.max(600, Math.min(window.innerHeight * 0.75, window.innerHeight - 100))
  
  console.log('🎨 初始化对话框大小:', { width, height })
  
  dialogSize.value = { width, height }
  initialDialogSize.value = { width, height }
}

// 应用对话框大小到DOM并重置位置
const applyDialogSize = () => {
  let dialogEl = document.querySelector('.diff-dialog-wrapper.with-editor .el-dialog')
  if (!dialogEl) {
    const dialogs = document.querySelectorAll('.el-dialog')
    dialogEl = dialogs[dialogs.length - 1]
  }
  
  if (dialogEl) {
    console.log('📐 应用对话框尺寸:', dialogSize.value)
    
    // 应用尺寸
    dialogEl.style.width = `${dialogSize.value.width}px`
    dialogEl.style.height = `${dialogSize.value.height}px`
    
    console.log('✅ 对话框尺寸已应用:', {
      width: dialogEl.style.width,
      height: dialogEl.style.height,
      offsetWidth: dialogEl.offsetWidth,
      offsetHeight: dialogEl.offsetHeight
    })
    
    // 重置位置到(0,0)
    dialogEl.style.transform = 'translate(0px, 0px)'
    dialogPosition.value = { x: 0, y: 0 }
    
    // 强制触发Monaco Editor的布局更新
    setTimeout(() => {
      window.dispatchEvent(new Event('resize'))
      console.log('🔄 触发resize事件')
    }, 150)
  } else {
    console.error('❌ 未找到对话框元素')
  }
}


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

// 解析消息中的代码块
const parseCodeBlocks = (content) => {
  const codeBlockRegex = /```(\w+)\n([\s\S]*?)```/g
  const blocks = []
  let match
  
  while ((match = codeBlockRegex.exec(content)) !== null) {
    blocks.push({
      language: match[1],
      code: match[2].trim()
    })
  }
  
  return blocks
}

// 检测是否有代码建议
const hasCodeSuggestions = computed(() => {
  if (props.message.role !== 'assistant' || !props.message.content) return false
  
  const codeBlocks = parseCodeBlocks(props.message.content)
  // 如果有多个代码块，可能是原始代码和建议代码的对比
  return codeBlocks.length > 0 && fileStore.currentFile
})

// 是否包含结构化修改指令
const hasStructuredInstructions = computed(() => {
  if (props.message.role !== 'assistant' || !props.message.content) return false
  return /####\s*🔧\s*结构化修改指令/.test(props.message.content) && fileStore.currentFile
})

// 显示代码差异
const handleShowDiff = async () => {
  console.log('=== 开始查看代码差异 ===')
  console.log('当前文件:', fileStore.currentFile)
  console.log('当前文件ID:', fileStore.currentFileId)
  
  if (!fileStore.currentFile) {
    ElMessage.warning('请先选择一个文件')
    return
  }
  
  // 获取当前文件的原始代码
  const originalCode = fileStore.currentFileContent
  console.log('原始代码长度:', originalCode?.length || 0)
  console.log('原始代码前100字符:', originalCode?.substring(0, 100))
  
  if (!originalCode) {
    console.error('文件内容为空！文件ID:', fileStore.currentFileId)
    console.error('fileContents:', fileStore.fileContents)
    ElMessage.warning('无法获取当前文件内容，请确保文件已正确加载')
    return
  }
  
  const currentLanguage = getFileLanguage(fileStore.currentFile.filename)
  let modifiedCode = null
  
  // 动态导入代码修改工具
  const { parseModificationInstructions, applyModifications, hasModificationInstructions } = await import('@/utils/codeModifier')
  
  // 调试：输出消息内容的关键部分
  console.log('=== AI消息内容分析 ===')
  console.log('消息全文前1000字符:', props.message.content.substring(0, 1000))
  console.log('是否包含"结构化修改指令":', props.message.content.includes('结构化修改指令'))
  console.log('是否包含"修改"关键字:', props.message.content.includes('修改'))
  
  // 优先尝试解析结构化修改指令
  if (hasModificationInstructions(props.message.content)) {
    console.log('✅ 检测到结构化修改指令标题，使用智能应用模式')
    const instructions = parseModificationInstructions(props.message.content)
    console.log('解析结果:', instructions)
    
    if (instructions.length > 0) {
      console.log(`✅ 成功解析 ${instructions.length} 个修改指令`)
      modifiedCode = applyModifications(originalCode, instructions)
    } else {
      console.warn('⚠️ 找到标题但未解析到具体修改指令')
    }
  } else {
    console.log('❌ 未检测到结构化修改指令标题')
  }
  
  // 如果没有结构化修改指令，尝试传统代码块方式
  if (!modifiedCode) {
    console.log('使用传统代码块解析方式')
    const codeBlocks = parseCodeBlocks(props.message.content)
    console.log('解析到的代码块数量:', codeBlocks.length)
    console.log('代码块详情:', codeBlocks)
    
    if (codeBlocks.length === 0) {
      ElMessage.warning('没有找到代码建议')
      return
    }
    
    // 使用AI建议的第一个代码块作为修改后的代码
    // 如果有多个代码块，优先选择与当前文件语言匹配的
    console.log('当前文件语言:', currentLanguage)
    
    modifiedCode = codeBlocks.find(block => block.language === currentLanguage)?.code
    
    // 如果没有找到匹配的语言，使用第一个代码块
    if (!modifiedCode && codeBlocks.length > 0) {
      modifiedCode = codeBlocks[0].code
      console.log('未找到匹配语言，使用第一个代码块')
    }
  }
  
  console.log('修改后代码长度:', modifiedCode?.length || 0)
  
  if (!modifiedCode) {
    ElMessage.warning('没有找到有效的代码建议')
    return
  }
  
  currentCodePair.value = {
    fileName: fileStore.currentFile.filename,
    original: originalCode,
    modified: modifiedCode,
    language: currentLanguage
  }
  
  // 重置对话框位置和大小
  dialogPosition.value = { x: 0, y: 0 }
  
  // 初始化对话框大小
  initDialogSize()
  
  showDiffDialog.value = true
  
  // 等待对话框渲染完成后绑定拖拽事件并应用初始尺寸
  nextTick(() => {
    setTimeout(() => {
      setupDragEvents()
      applyDialogSize()  // 这会同时重置位置和应用尺寸
    }, 100)
  })
}

// 设置拖拽事件
const setupDragEvents = () => {
  // 只有当编辑器打开时才启用拖拽
  if (!fileStore.currentFile) {
    console.log('没有打开文件，不启用拖拽')
    return
  }
  
  // 尝试多种选择器策略
  let dialogEl = document.querySelector('.diff-dialog-wrapper.with-editor .el-dialog')
  if (!dialogEl) {
    // 备用选择器：查找所有对话框
    const dialogs = document.querySelectorAll('.el-dialog')
    console.log('找到的对话框数量:', dialogs.length)
    // 取最后一个（最新打开的）
    dialogEl = dialogs[dialogs.length - 1]
  }
  
  if (!dialogEl) {
    console.warn('未找到对话框元素')
    return
  }
  
  console.log('找到对话框元素:', dialogEl)
  
  const headerEl = dialogEl.querySelector('.el-dialog__header')
  if (!headerEl) {
    console.warn('未找到对话框头部元素')
    return
  }
  
  console.log('找到对话框头部，设置拖拽')
  
  // 设置鼠标样式，表示可拖拽
  headerEl.style.cursor = 'move'
  headerEl.style.userSelect = 'none'
  
  // 添加事件监听
  headerEl.onmousedown = handleDragStart
  headerEl.ondblclick = handleDoubleClick
}

// 双击标题栏重置位置和大小
const handleDoubleClick = () => {
  dialogPosition.value = { x: 0, y: 0 }
  
  // 重置大小
  initDialogSize()
  
  let dialogEl = document.querySelector('.diff-dialog-wrapper.with-editor .el-dialog')
  if (!dialogEl) {
    const dialogs = document.querySelectorAll('.el-dialog')
    dialogEl = dialogs[dialogs.length - 1]
  }
  
  if (dialogEl) {
    // 重置位置
    dialogEl.style.transform = 'translate(0px, 0px)'
    // 重置大小
    dialogEl.style.width = `${dialogSize.value.width}px`
    dialogEl.style.height = `${dialogSize.value.height}px`
  }
  
  ElMessage.success('位置和大小已重置')
}

// 开始拖拽
const handleDragStart = (e) => {
  // 只允许左键拖拽
  if (e.button !== 0) return
  
  isDragging.value = true
  dragStartPos.value = {
    x: e.clientX - dialogPosition.value.x,
    y: e.clientY - dialogPosition.value.y
  }
  
  // 添加拖拽中的样式
  let dialogEl = document.querySelector('.diff-dialog-wrapper.with-editor .el-dialog')
  if (!dialogEl) {
    const dialogs = document.querySelectorAll('.el-dialog')
    dialogEl = dialogs[dialogs.length - 1]
  }
  
  if (dialogEl) {
    dialogEl.classList.add('dragging')
  }
  
  // 添加全局事件监听
  document.addEventListener('mousemove', handleDragMove)
  document.addEventListener('mouseup', handleDragEnd)
  
  // 阻止默认行为和事件冒泡
  e.preventDefault()
  e.stopPropagation()
}

// 拖拽中
const handleDragMove = (e) => {
  if (!isDragging.value) return
  
  const newX = e.clientX - dragStartPos.value.x
  const newY = e.clientY - dragStartPos.value.y
  
  // 获取对话框元素
  let dialogEl = document.querySelector('.diff-dialog-wrapper.with-editor .el-dialog')
  if (!dialogEl) {
    const dialogs = document.querySelectorAll('.el-dialog')
    dialogEl = dialogs[dialogs.length - 1]
  }
  if (!dialogEl) return
  
  // 计算可用空间（确保准确）
  const codePanelWidth = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--code-panel-width') || '600')
  const availableWidth = window.innerWidth - codePanelWidth
  const availableHeight = window.innerHeight
  
  // 使用getBoundingClientRect获取准确的对话框尺寸
  const rect = dialogEl.getBoundingClientRect()
  const dialogWidth = rect.width
  const dialogHeight = rect.height
  
  // 边界限制：对话框完全在可视区域内
  const minX = 0
  const maxX = Math.max(0, availableWidth - dialogWidth)
  const minY = 0
  const maxY = Math.max(0, availableHeight - dialogHeight)
  
  // 限制在边界内
  const clampedX = Math.max(minX, Math.min(maxX, newX))
  const clampedY = Math.max(minY, Math.min(maxY, newY))
  
  dialogPosition.value = {
    x: clampedX,
    y: clampedY
  }
  
  // 应用位置
  dialogEl.style.transform = `translate(${clampedX}px, ${clampedY}px)`
  
  e.preventDefault()
}

// 结束拖拽
const handleDragEnd = () => {
  isDragging.value = false
  
  // 移除拖拽中的样式
  let dialogEl = document.querySelector('.diff-dialog-wrapper.with-editor .el-dialog')
  if (!dialogEl) {
    const dialogs = document.querySelectorAll('.el-dialog')
    dialogEl = dialogs[dialogs.length - 1]
  }
  
  if (dialogEl) {
    dialogEl.classList.remove('dragging')
  }
  
  // 移除全局事件监听
  document.removeEventListener('mousemove', handleDragMove)
  document.removeEventListener('mouseup', handleDragEnd)
}

// 应用代码建议
const handleApplySuggestion = (modifiedCode) => {
  if (!fileStore.currentFile) return
  
  // 更新文件内容
  fileStore.updateFileContent(fileStore.currentFileId, modifiedCode)
  
  showDiffDialog.value = false
  ElMessage.success('代码建议已应用到当前文件')
}

// 智能应用修改指令（直接应用到当前文件，不打开diff对话框）
const handleApplyInstructions = () => {
  if (!fileStore.currentFile) {
    ElMessage.warning('请先选择一个文件')
    return
  }
  
  // 导入代码修改工具
  import('@/utils/codeModifier').then(({ parseModificationInstructions, applyModifications, generateModificationPreview }) => {
    // 解析修改指令
    const instructions = parseModificationInstructions(props.message.content)
    
    if (instructions.length === 0) {
      ElMessage.warning('未找到有效的修改指令')
      return
    }
    
    // 生成预览信息
    const preview = generateModificationPreview(instructions)
    
    // 确认是否应用
    ElMessageBox.confirm(
      preview,
      '确认应用修改',
      {
        confirmButtonText: '应用',
        cancelButtonText: '取消',
        type: 'info',
        customClass: 'modification-preview-dialog'
      }
    ).then(() => {
      // 获取当前文件内容
      const originalCode = fileStore.currentFileContent
      
      if (!originalCode) {
        ElMessage.error('无法获取当前文件内容')
        return
      }
      
      // 应用修改
      const modifiedCode = applyModifications(originalCode, instructions)
      
      // 更新文件内容
      fileStore.updateFileContent(fileStore.currentFileId, modifiedCode)
      
      ElMessage.success(`成功应用 ${instructions.length} 个修改`)
    }).catch(() => {
      console.log('用户取消应用修改')
    })
  })
}

// Resize相关函数
// 开始调整大小
const startResize = (e, direction) => {
  e.preventDefault()
  e.stopPropagation()
  
  isResizing.value = true
  resizeDirection.value = direction
  resizeStartPos.value = { x: e.clientX, y: e.clientY }
  
  // 记录初始大小
  let dialogEl = document.querySelector('.diff-dialog-wrapper.with-editor .el-dialog')
  if (!dialogEl) {
    const dialogs = document.querySelectorAll('.el-dialog')
    dialogEl = dialogs[dialogs.length - 1]
  }
  
  if (dialogEl) {
    const rect = dialogEl.getBoundingClientRect()
    initialDialogSize.value = {
      width: rect.width,
      height: rect.height
    }
  }
  
  // 添加全局事件监听
  document.addEventListener('mousemove', handleResizeMove)
  document.addEventListener('mouseup', handleResizeEnd)
}

// 调整大小中
const handleResizeMove = (e) => {
  if (!isResizing.value) return
  
  const deltaX = e.clientX - resizeStartPos.value.x
  const deltaY = e.clientY - resizeStartPos.value.y
  
  const direction = resizeDirection.value
  
  // 最小尺寸限制
  const minWidth = 600
  const minHeight = 400
  
  // 计算可用空间（考虑代码面板）
  const codePanelWidth = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--code-panel-width') || '600')
  const availableWidth = window.innerWidth - codePanelWidth
  const availableHeight = window.innerHeight
  
  // 获取当前位置
  const currentX = dialogPosition.value.x
  const currentY = dialogPosition.value.y
  
  // 计算新的宽度、高度和位置
  let newWidth = initialDialogSize.value.width
  let newHeight = initialDialogSize.value.height
  let newX = currentX
  let newY = currentY
  
  // 根据方向调整
  if (direction.includes('r')) { // 右侧：只增加宽度
    newWidth = initialDialogSize.value.width + deltaX
    // 确保不超出右边界：currentX + newWidth <= availableWidth
    newWidth = Math.min(newWidth, availableWidth - currentX)
  }
  
  if (direction.includes('l')) { // 左侧：增加宽度并向左移动
    // 向左拖动：deltaX < 0，宽度增加，位置向左移
    const widthChange = -deltaX
    newWidth = initialDialogSize.value.width + widthChange
    newX = currentX - widthChange
    
    // 边界检查：不能超出左边界
    if (newX < 0) {
      newWidth = initialDialogSize.value.width + currentX
      newX = 0
    }
  }
  
  if (direction.includes('b')) { // 底部：只增加高度
    newHeight = initialDialogSize.value.height + deltaY
    // 确保不超出底边界：currentY + newHeight <= availableHeight
    newHeight = Math.min(newHeight, availableHeight - currentY)
  }
  
  if (direction.includes('t')) { // 顶部：增加高度并向上移动
    // 向上拖动：deltaY < 0，高度增加，位置向上移
    const heightChange = -deltaY
    newHeight = initialDialogSize.value.height + heightChange
    newY = currentY - heightChange
    
    // 边界检查：不能超出顶边界
    if (newY < 0) {
      newHeight = initialDialogSize.value.height + currentY
      newY = 0
    }
  }
  
  // 应用最小尺寸限制
  newWidth = Math.max(minWidth, newWidth)
  newHeight = Math.max(minHeight, newHeight)
  
  // 确保对话框完全在可视区域内
  // 1. 检查左边和上边
  newX = Math.max(0, newX)
  newY = Math.max(0, newY)
  
  // 2. 检查右边和下边
  if (newX + newWidth > availableWidth) {
    newWidth = Math.max(minWidth, availableWidth - newX)
  }
  if (newY + newHeight > availableHeight) {
    newHeight = Math.max(minHeight, availableHeight - newY)
  }
  
  // 3. 再次检查位置（如果尺寸限制后仍超出）
  newX = Math.min(newX, Math.max(0, availableWidth - newWidth))
  newY = Math.min(newY, Math.max(0, availableHeight - newHeight))
  
  // 保存新尺寸和位置
  dialogSize.value = { width: newWidth, height: newHeight }
  dialogPosition.value = { x: newX, y: newY }
  
  // 获取dialog元素并应用样式
  let dialogEl = document.querySelector('.diff-dialog-wrapper.with-editor .el-dialog')
  if (!dialogEl) {
    const dialogs = document.querySelectorAll('.el-dialog')
    dialogEl = dialogs[dialogs.length - 1]
  }
  
  if (dialogEl) {
    // 应用尺寸
    dialogEl.style.width = `${newWidth}px`
    dialogEl.style.height = `${newHeight}px`
    
    // 应用位置
    dialogEl.style.transform = `translate(${newX}px, ${newY}px)`
  }
}

// 结束调整大小
const handleResizeEnd = () => {
  isResizing.value = false
  resizeDirection.value = ''
  
  // 移除全局事件监听
  document.removeEventListener('mousemove', handleResizeMove)
  document.removeEventListener('mouseup', handleResizeEnd)
  
  // 🔧 关键修复：拖拽结束后，强制触发 Monaco Editor 重新布局
  nextTick(() => {
    // 方法1：通过容器引用直接调用 layout
    const container = document.querySelector('.diff-editor-container')
    if (container && container.__monacoEditor) {
      console.log('🔄 拖拽结束，触发Monaco Editor重新布局')
      // 延迟多次调用，确保布局正确
      setTimeout(() => {
        if (container.__monacoEditor) {
          container.__monacoEditor.layout()
          console.log('✅ Monaco Editor布局已更新')
        }
      }, 50)
      
      setTimeout(() => {
        if (container.__monacoEditor) {
          container.__monacoEditor.layout()
        }
      }, 150)
    }
    
    // 方法2：触发window resize事件作为备选
    window.dispatchEvent(new Event('resize'))
  })
}

// 关闭差异对话框
const handleCloseDiff = () => {
  showDiffDialog.value = false
}

// 监听对话框显示状态，防止页面滚动
watch(showDiffDialog, (newVal) => {
  if (newVal && fileStore.currentFile) {
    // 对话框打开时，阻止body滚动
    document.body.style.overflow = 'hidden'
  } else {
    // 对话框关闭时，恢复body滚动
    document.body.style.overflow = ''
  }
})

// 获取文件语言
const getFileLanguage = (filename) => {
  const ext = filename.split('.').pop().toLowerCase()
  const langMap = {
    'py': 'python',
    'js': 'javascript',
    'ts': 'typescript',
    'jsx': 'javascript',
    'tsx': 'typescript',
    'vue': 'vue',
    'java': 'java',
    'go': 'go',
    'rs': 'rust',
    'cpp': 'cpp',
    'c': 'c',
    'cs': 'csharp',
    'php': 'php',
    'rb': 'ruby',
    'swift': 'swift',
    'kt': 'kotlin'
  }
  return langMap[ext] || 'plaintext'
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

/* 差异对话框包装器 */
.diff-dialog-wrapper {
  z-index: 2100 !important;
}

/* 当右侧有代码编辑器时，对话框只占据左侧+中间区域 */
.diff-dialog-wrapper.with-editor :deep(.el-overlay) {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: calc(100% - var(--code-panel-width, 600px)) !important;
  height: 100vh !important;
  max-height: 100vh !important;
  z-index: 2100 !important;
  overflow: hidden !important;
}

.diff-dialog-wrapper.with-editor :deep(.el-dialog) {
  position: fixed !important;
  left: 0 !important;
  top: 0 !important;
  margin: 0 !important;
  display: flex !important; /* 使用flex布局 */
  flex-direction: column !important;
  /* 宽度和高度由JS动态设置 */
  max-width: 100% !important;
  max-height: 100vh !important;
  border-radius: 0 !important;
  transition: box-shadow 0.2s ease;
  will-change: transform;
  overflow: hidden !important;
  /* transform、width、height 将通过 JS 动态设置 */
}

/* 非拖拽状态下的平滑过渡 */
.diff-dialog-wrapper.with-editor :deep(.el-dialog:not(.dragging)) {
  transition: box-shadow 0.2s ease, transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* 对话框标题区域样式增强 */
.diff-dialog-wrapper.with-editor :deep(.el-dialog__header) {
  cursor: move;
  user-select: none;
  background: var(--el-bg-color);
  padding: 10px 16px;
  border-bottom: 1px solid var(--el-border-color);
  position: relative;
  flex-shrink: 0; /* 防止header被压缩 */
}

/* 添加拖拽提示图标 */
.diff-dialog-wrapper.with-editor :deep(.el-dialog__header::before) {
  content: '⋮⋮';
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  color: var(--el-text-color-secondary);
  opacity: 0.6;
  letter-spacing: -2px;
  pointer-events: none;
}

/* 鼠标悬停时提示更明显 */
.diff-dialog-wrapper.with-editor :deep(.el-dialog__header:hover::before) {
  opacity: 0.9;
}

/* 标题内容布局 */
.dialog-header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: calc(100% - 40px);
  margin-left: 20px;
  margin-right: 20px;
  gap: 16px;
}

.dialog-title {
  color: var(--el-text-color-primary);
  font-weight: 600;
  font-size: 16px;
}

.drag-hint {
  color: var(--el-text-color-secondary);
  font-size: 12px;
  font-weight: 400;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  flex-shrink: 0;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 鼠标悬停时提示文字变亮 */
.diff-dialog-wrapper.with-editor :deep(.el-dialog__header:hover) .drag-hint {
  color: rgba(255, 255, 255, 0.95);
}

/* 拖拽时的阴影效果 */
.diff-dialog-wrapper.with-editor :deep(.el-dialog.dragging) {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
}

.diff-dialog-wrapper.with-editor :deep(.el-dialog__body) {
  padding: 0 !important;
  flex: 1 !important; /* 在flex容器中占满剩余空间 */
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 全局浮动关闭按钮 - 固定在页面左下角 */
.global-floating-close-button {
  position: fixed !important;
  left: 24px;
  bottom: 24px;
  z-index: 2200;
  width: 56px;
  height: 56px;
  font-size: 24px;
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.4);
  transition: all 0.3s ease;
  animation: fadeInUp 0.3s ease;
}

.global-floating-close-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(245, 108, 108, 0.6);
}

.global-floating-close-button:active {
  transform: scale(0.95);
}

/* fadeInUp 动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Resize功能已禁用 - 如需启用，请恢复resize相关代码 */

/* 全屏时的对话框样式 */
.diff-dialog-wrapper :deep(.el-dialog__body) {
  padding: 0 !important;
}
</style>

