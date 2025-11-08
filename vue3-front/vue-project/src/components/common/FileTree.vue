<template>
  <div class="file-tree-container" :style="{ width: (isCollapsed ? 48 : treeWidth) + 'px' }">
    <div class="file-tree" :class="{ collapsed: isCollapsed }">
      <!-- 文件树头部 -->
      <div class="tree-header">
        <div class="header-title" v-if="!isCollapsed">
          <el-icon><Folder /></el-icon>
          <span>文件浏览器</span>
        </div>
        <el-button 
          :icon="isCollapsed ? Expand : Fold" 
          circle 
          size="small"
          @click="toggleCollapse"
          :title="isCollapsed ? '展开文件树' : '折叠文件树'"
        />
      </div>

      <!-- 文件树内容 -->
      <div class="tree-content" v-if="!isCollapsed">
      <el-tree
        :data="treeData"
        :props="treeProps"
        node-key="id"
        :default-expand-all="true"
        :expand-on-click-node="false"
        @node-click="handleNodeClick"
        :highlight-current="true"
        :current-node-key="currentFileId"
      >
        <template #default="{ node, data }">
          <div class="tree-node">
            <el-icon v-if="data.type === 'folder'" class="node-icon folder-icon">
              <Folder />
            </el-icon>
            <el-icon v-else class="node-icon file-icon">
              <Document />
            </el-icon>
            <span class="node-label">{{ node.label }}</span>
            <span class="node-size" v-if="data.type === 'file' && data.size">
              {{ formatSize(data.size) }}
            </span>
          </div>
        </template>
      </el-tree>

      <!-- 空状态 -->
      <div v-if="treeData.length === 0" class="empty-tree">
        <el-icon><FolderOpened /></el-icon>
        <p>暂无文件</p>
      </div>
    </div>
    </div>
    
    <!-- 拖拽手柄 -->
    <div 
      v-if="!isCollapsed"
      class="tree-resize-handle"
      @mousedown="startResize"
      :class="{ resizing: isResizing }"
    >
      <div class="resize-line"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Folder, FolderOpened, Document, Expand, Fold } from '@element-plus/icons-vue'

const props = defineProps({
  files: {
    type: Array,
    default: () => []
  },
  currentFileId: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['selectFile', 'toggleCollapse'])

const isCollapsed = ref(false)
const treeWidth = ref(240)
const isResizing = ref(false)
const startX = ref(0)
const startWidth = ref(0)

const treeProps = {
  label: 'name',
  children: 'children'
}

// 构建树形结构
const treeData = computed(() => {
  const tree = []
  const folderMap = new Map()

  props.files.forEach(file => {
    const pathParts = file.filename.split('/').filter(Boolean)
    
    if (pathParts.length === 1) {
      // 根目录文件
      tree.push({
        id: file.file_id,
        name: file.filename,
        type: 'file',
        size: file.file_size,
        fileId: file.file_id
      })
    } else {
      // 有目录的文件
      let currentLevel = tree
      let currentPath = ''
      
      pathParts.forEach((part, index) => {
        currentPath += '/' + part
        
        if (index < pathParts.length - 1) {
          // 这是一个目录
          if (!folderMap.has(currentPath)) {
            const folder = {
              id: currentPath,
              name: part,
              type: 'folder',
              children: []
            }
            folderMap.set(currentPath, folder)
            currentLevel.push(folder)
          }
          currentLevel = folderMap.get(currentPath).children
        } else {
          // 这是文件
          currentLevel.push({
            id: file.file_id,
            name: part,
            type: 'file',
            size: file.file_size,
            fileId: file.file_id
          })
        }
      })
    }
  })

  return tree
})

const handleNodeClick = (data) => {
  if (data.type === 'file') {
    emit('selectFile', data.fileId)
  }
}

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
  // 折叠时保存当前宽度，展开时恢复或使用默认宽度
  if (!isCollapsed.value && treeWidth.value < 100) {
    treeWidth.value = 240  // 展开时如果宽度过小，恢复默认宽度
  }
  emit('toggleCollapse', isCollapsed.value)
}

const formatSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

// 拖拽调整宽度
const startResize = (e) => {
  isResizing.value = true
  startX.value = e.clientX
  startWidth.value = treeWidth.value
  
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'
}

const handleResize = (e) => {
  if (!isResizing.value) return
  
  const deltaX = e.clientX - startX.value
  const newWidth = startWidth.value + deltaX
  
  // 最小48px（与折叠宽度一致），最大500px
  if (newWidth >= 48 && newWidth <= 500) {
    treeWidth.value = newWidth
  }
}

const stopResize = () => {
  isResizing.value = false
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
  document.body.style.cursor = ''
  document.body.style.userSelect = ''
}
</script>

<style scoped>
.file-tree-container {
  display: flex;
  height: 100%;
  position: relative;
  flex-shrink: 0;
  transition: width 0.1s ease-out;
}

.file-tree {
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
}

.file-tree.collapsed {
  width: 48px;
}

.tree-resize-handle {
  width: 4px;
  cursor: col-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 10;
  transition: background 0.2s;
}

.tree-resize-handle:hover,
.tree-resize-handle.resizing {
  background: rgba(64, 158, 255, 0.1);
}

.resize-line {
  width: 2px;
  height: 40px;
  background: rgba(64, 158, 255, 0.3);
  border-radius: 1px;
  transition: all 0.2s;
}

.tree-resize-handle:hover .resize-line,
.tree-resize-handle.resizing .resize-line {
  height: 60px;
  background: rgba(64, 158, 255, 0.6);
}

.tree-header {
  height: 48px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e4e7ed;
  background: #ffffff;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  flex: 1;
  min-width: 0;
}

.header-title span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tree-content {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.tree-node {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 100%;
  padding: 4px 8px;
}

.node-icon {
  flex-shrink: 0;
}

.folder-icon {
  color: #f56c6c;
}

.file-icon {
  color: #909399;
}

.node-label {
  flex: 1;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.node-size {
  font-size: 11px;
  color: #909399;
  flex-shrink: 0;
}

.empty-tree {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #909399;
  text-align: center;
}

.empty-tree .el-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-tree p {
  font-size: 13px;
}

/* 自定义el-tree样式 */
:deep(.el-tree) {
  background: transparent;
}

:deep(.el-tree-node__content) {
  height: 32px;
  border-radius: 4px;
  margin: 0 8px;
}

:deep(.el-tree-node__content:hover) {
  background: rgba(64, 158, 255, 0.1);
}

:deep(.el-tree-node.is-current > .el-tree-node__content) {
  background: rgba(64, 158, 255, 0.2);
  color: #409eff;
}

:deep(.el-tree-node__content .el-tree-node__expand-icon) {
  color: #909399;
}
</style>

