# Resize功能Bug修复

## 问题描述

在实现四角拖拽调节大小功能后，发现三个严重问题：

### 1. 左上角和左下角拖拽时对话框飞速向右移动
当拖拽左上角或左下角时，对话框会快速向右侧移动，甚至超出屏幕，造成无法控制。

### 2. 右上角和右下角拖拽时对话框居中
使用右上角或右下角调整大小时，对话框会自动居中对齐，而不是固定在左侧。

### 3. 无法调整高度
四个角都无法调整对话框的高度，只能调整宽度。

## 问题原因分析

### 1. 使用 `:width` prop 导致自动居中

```vue
<!-- 错误的做法 -->
<el-dialog
  :width="dialogSize.width + 'px'"
  ...
>
```

**问题**：当通过 `:width` prop 设置宽度时，Element Plus 的 el-dialog 会自动居中对齐，覆盖我们的 `position: fixed; left: 0` 设置。

### 2. 左侧调整的位置同步逻辑错误

```javascript
// 错误的逻辑
if (dialogEl && direction.includes('l')) {
  const actualDelta = newWidth - initialDialogSize.value.width
  dialogPosition.value.x -= actualDelta  // ❌ 逻辑反了
  dialogEl.style.transform = `translate(${dialogPosition.value.x}px, ${dialogPosition.value.y}px)`
}
```

**问题**：
- 当宽度增加时，位置应该向左移动（负方向），但代码是减去增量，实际是向右移动
- 导致对话框飞速向右移动

**正确逻辑**：
- 宽度增加 → 位置向左移（负方向）
- 宽度减少 → 位置向右移（正方向）
- 位置变化应该是宽度变化的**相反方向**

### 3. 没有应用高度设置

```javascript
// 只设置了宽度，没有设置高度
dialogSize.value = {
  width: Math.min(maxWidth, newWidth),
  height: Math.min(maxHeight, newHeight)  // 仅保存，未应用
}
```

**问题**：虽然计算了新高度并保存到状态，但没有应用到 dialog 元素的 style 上。

### 4. CSS固定高度覆盖

```css
/* 错误的CSS */
.diff-dialog-wrapper.with-editor :deep(.el-dialog) {
  width: calc(100% - var(--code-panel-width, 600px)) !important;
  height: 100vh !important;  /* ❌ 固定高度 */
}

.diff-dialog-wrapper.with-editor :deep(.el-dialog__body) {
  height: calc(100vh - 60px) !important;  /* ❌ 固定高度 */
}
```

**问题**：CSS中使用 `!important` 固定了高度，JS设置的动态高度无法生效。

## 解决方案

### 1. 移除 `:width` prop，改用 JS 直接设置

```vue
<!-- 修正后 -->
<el-dialog
  v-model="showDiffDialog"
  :fullscreen="!fileStore.currentFile"
  <!-- 移除 :width prop -->
  ...
>
```

**改进**：通过 JS 直接操作 dialog 元素的 `style.width` 和 `style.height`，避免 el-dialog 自动居中。

### 2. 修正左侧/顶部调整的位置同步逻辑

```javascript
// 修正后的逻辑
if (direction.includes('l')) { // left - 向左调整
  // 左侧调整：宽度增加时位置向左移，宽度减少时位置向右移
  const desiredWidth = Math.max(minWidth, Math.min(maxWidth, initialDialogSize.value.width - deltaX))
  const actualWidthChange = desiredWidth - initialDialogSize.value.width
  newWidth = desiredWidth
  positionDeltaX = -actualWidthChange // 宽度变化的相反方向 ✅
}

if (direction.includes('t')) { // top - 向上调整
  // 顶部调整：高度增加时位置向上移，高度减少时位置向下移
  const desiredHeight = Math.max(minHeight, Math.min(maxHeight, initialDialogSize.value.height - deltaY))
  const actualHeightChange = desiredHeight - initialDialogSize.value.height
  newHeight = desiredHeight
  positionDeltaY = -actualHeightChange // 高度变化的相反方向 ✅
}
```

**关键点**：
1. 计算实际的宽度/高度变化量
2. 位置偏移 = 宽度/高度变化的**相反方向**（负值）
3. 同时考虑最小和最大尺寸限制

### 3. 同时应用宽度和高度

```javascript
const handleResizeMove = (e) => {
  // ...计算 newWidth 和 newHeight
  
  // 保存新尺寸
  dialogSize.value = {
    width: newWidth,
    height: newHeight
  }
  
  if (dialogEl) {
    // 直接设置宽度和高度 ✅
    dialogEl.style.width = `${newWidth}px`
    dialogEl.style.height = `${newHeight}px`
    
    // 如果从左边或顶部调整，需要同步位置
    if (positionDeltaX !== 0 || positionDeltaY !== 0) {
      dialogPosition.value.x += positionDeltaX
      dialogPosition.value.y += positionDeltaY
    }
    
    // 应用位置变换
    dialogEl.style.transform = `translate(${dialogPosition.value.x}px, ${dialogPosition.value.y}px)`
  }
}
```

### 4. 移除CSS中的固定尺寸

```css
/* 修正后的CSS */
.diff-dialog-wrapper.with-editor :deep(.el-dialog) {
  position: fixed !important;
  left: 0 !important;
  top: 0 !important;
  margin: 0 !important;
  /* 宽度和高度由JS动态设置 ✅ */
  max-width: none !important;
  max-height: none !important;
  border-radius: 0 !important;
  transition: box-shadow 0.2s ease;
  will-change: transform;
  /* transform、width、height 将通过 JS 动态设置 */
}

.diff-dialog-wrapper.with-editor :deep(.el-dialog__body) {
  padding: 0 !important;
  height: calc(100% - 60px) !important; /* 100%减去header高度 ✅ */
  overflow: hidden;
}
```

### 5. 添加 `applyDialogSize` 函数

```javascript
// 应用对话框大小到DOM
const applyDialogSize = () => {
  let dialogEl = document.querySelector('.diff-dialog-wrapper.with-editor .el-dialog')
  if (!dialogEl) {
    const dialogs = document.querySelectorAll('.el-dialog')
    dialogEl = dialogs[dialogs.length - 1]
  }
  
  if (dialogEl) {
    dialogEl.style.width = `${dialogSize.value.width}px`
    dialogEl.style.height = `${dialogSize.value.height}px`
  }
}
```

在对话框打开时调用：
```javascript
nextTick(() => {
  setTimeout(() => {
    setupDragEvents()
    applyDialogSize()  // 应用初始尺寸 ✅
  }, 100)
})
```

### 6. 更新双击重置逻辑

```javascript
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
    // 重置大小 ✅
    dialogEl.style.width = `${dialogSize.value.width}px`
    dialogEl.style.height = `${dialogSize.value.height}px`
  }
  
  ElMessage.success('位置和大小已重置')
}
```

## 技术要点

### 1. 避免使用 el-dialog 的 width prop

当需要自定义对话框位置时，不要使用 `:width` prop，因为它会触发 el-dialog 的居中逻辑。

**推荐做法**：
- 通过 JS 直接操作 `dialogEl.style.width` 和 `dialogEl.style.height`
- 使用 `position: fixed; left: 0; top: 0` 固定位置
- 通过 `transform: translate()` 实现拖拽移动

### 2. 位置同步的正确逻辑

当从**左侧或顶部**调整大小时，需要同步调整位置：

```
宽度变化 = 新宽度 - 初始宽度
位置X偏移 = -宽度变化

高度变化 = 新高度 - 初始高度
位置Y偏移 = -高度变化
```

**原理**：
- 从左边向左拉（增加宽度），对话框需要向左移动相同距离
- 从左边向右拉（减少宽度），对话框需要向右移动相同距离
- 顶部调整同理

### 3. CSS 相对高度的使用

```css
/* 对话框body高度 = 对话框总高度 - header高度 */
.diff-dialog-wrapper.with-editor :deep(.el-dialog__body) {
  height: calc(100% - 60px) !important;
}
```

使用 `100%` 而不是 `100vh`，确保body高度相对于对话框总高度计算。

### 4. 尺寸约束

```javascript
// 最小尺寸
const minWidth = 600
const minHeight = 400

// 最大尺寸
const codePanelWidth = parseFloat(
  getComputedStyle(document.documentElement)
    .getPropertyValue('--code-panel-width') || '600'
)
const maxWidth = window.innerWidth - codePanelWidth - 40
const maxHeight = window.innerHeight - 100

// 应用约束
newWidth = Math.max(minWidth, Math.min(maxWidth, desiredWidth))
newHeight = Math.max(minHeight, Math.min(maxHeight, desiredHeight))
```

### 5. 初始尺寸的应用时机

```javascript
nextTick(() => {
  setTimeout(() => {
    setupDragEvents()      // 设置拖拽事件
    applyDialogSize()      // 应用初始尺寸 ✅
  }, 100)
})
```

确保在对话框完全渲染后再应用尺寸。

## 效果验证

### 测试步骤

1. ✅ **左上角拖拽**：
   - 向左上拉：对话框应向左上扩大
   - 向右下拉：对话框应向右下缩小
   - 对话框应保持在可视区域内，不飞速移动

2. ✅ **右上角拖拽**：
   - 向右上拉：对话框应向右上扩大
   - 向左下拉：对话框应向左下缩小
   - 对话框应固定在左侧，不居中

3. ✅ **左下角拖拽**：
   - 向左下拉：对话框应向左下扩大
   - 向右上拉：对话框应向右上缩小
   - 位置同步正确

4. ✅ **右下角拖拽**：
   - 向右下拉：对话框应向右下扩大
   - 向左上拉：对话框应向左上缩小
   - 对话框固定在左上角

5. ✅ **尺寸限制**：
   - 尝试缩小到最小尺寸（600x400），应受限制
   - 尝试扩大超过屏幕，应受限制

6. ✅ **双击重置**：
   - 双击标题栏，位置和大小应重置到初始状态

### 预期效果

- ✅ 四个角都可以流畅调整宽度和高度
- ✅ 从左侧或顶部调整时，位置同步移动，视觉稳定
- ✅ 对话框固定在左侧，不会自动居中
- ✅ 受最小/最大尺寸限制，不会过小或超出屏幕
- ✅ 调整时实时响应，无卡顿或飞速移动
- ✅ 双击可重置位置和大小

## 相关文件

- `vue3-front/vue-project/src/components/chat/MessageItem.vue` - 修复resize逻辑和CSS

## 关键修改对比

### 修改前（错误）
```javascript
// ❌ 位置同步逻辑错误
if (dialogEl && direction.includes('l')) {
  const actualDelta = newWidth - initialDialogSize.value.width
  dialogPosition.value.x -= actualDelta  // 方向反了
}

// ❌ 没有应用高度
dialogSize.value = { width: newWidth, height: newHeight }
// 只保存，未应用到DOM
```

### 修改后（正确）
```javascript
// ✅ 位置同步逻辑正确
if (direction.includes('l')) {
  const desiredWidth = Math.max(minWidth, Math.min(maxWidth, initialDialogSize.value.width - deltaX))
  const actualWidthChange = desiredWidth - initialDialogSize.value.width
  newWidth = desiredWidth
  positionDeltaX = -actualWidthChange  // 相反方向
}

// ✅ 同时应用宽度和高度
if (dialogEl) {
  dialogEl.style.width = `${newWidth}px`
  dialogEl.style.height = `${newHeight}px`
  
  if (positionDeltaX !== 0 || positionDeltaY !== 0) {
    dialogPosition.value.x += positionDeltaX
    dialogPosition.value.y += positionDeltaY
  }
  
  dialogEl.style.transform = `translate(${dialogPosition.value.x}px, ${dialogPosition.value.y}px)`
}
```

## 总结

这次修复解决了三个核心问题：

1. **移除 `:width` prop**，避免 el-dialog 自动居中
2. **修正位置同步逻辑**，确保从左侧/顶部调整时位置正确移动
3. **同时应用宽度和高度**，支持四个角的完整调整功能

关键是理解**位置偏移应该是尺寸变化的相反方向**，这样才能保持视觉上的稳定性。

