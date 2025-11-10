/**
 * 代码差异对比页面 - 终极修复脚本
 * 
 * 这个脚本会强制修复所有可能的高度问题
 * 
 * 使用方法：
 * 1. 打开代码审查页面
 * 2. 点击"查看代码差异"按钮（让对话框显示出来）
 * 3. 按F12打开Console
 * 4. 复制此脚本并粘贴执行
 */

(function ultimateFix() {
  console.log('========================================')
  console.log('🔧 终极修复脚本开始')
  console.log('========================================\n')
  
  // 1. 找到对话框（class在同一个元素上，不是嵌套）
  let dialog = document.querySelector('.el-dialog.diff-dialog-wrapper')
  if (!dialog) {
    // 备选：只按 diff-dialog-wrapper 查找
    dialog = document.querySelector('.diff-dialog-wrapper')
  }
  if (!dialog) {
    console.error('❌ 未找到对话框，请先点击"查看代码差异"按钮')
    return
  }
  console.log('✅ 找到对话框:', {
    classes: dialog.className,
    width: dialog.offsetWidth,
    height: dialog.offsetHeight
  })
  
  // 2. 强制设置对话框高度
  dialog.style.height = '90vh'
  dialog.style.minHeight = '700px'
  console.log('📐 设置对话框高度:', dialog.style.height)
  
  // 3. 找到并设置dialog body高度
  const body = dialog.querySelector('.el-dialog__body')
  if (body) {
    body.style.height = 'calc(100% - 60px)'
    body.style.minHeight = '640px'
    body.style.display = 'flex'
    body.style.flexDirection = 'column'
    console.log('📐 设置body高度:', body.style.height)
  }
  
  // 4. 找到并设置Monaco容器高度
  const monacoWrapper = document.querySelector('.monaco-diff-editor')
  if (monacoWrapper) {
    monacoWrapper.style.height = '100%'
    monacoWrapper.style.minHeight = '600px'
    monacoWrapper.style.display = 'flex'
    monacoWrapper.style.flexDirection = 'column'
    console.log('📐 设置Monaco wrapper高度:', monacoWrapper.style.minHeight)
  }
  
  const container = document.querySelector('.diff-editor-container')
  if (container) {
    container.style.flex = '1'
    container.style.height = '100%'
    container.style.minHeight = '500px'
    container.style.overflow = 'hidden'
    console.log('📐 设置容器高度:', container.style.minHeight)
  }
  
  // 5. 检查最终结果
  console.log('\n========================================')
  console.log('📊 最终尺寸检查')
  console.log('========================================')
  
  console.log('对话框尺寸:', {
    width: dialog.offsetWidth,
    height: dialog.offsetHeight,
    display: getComputedStyle(dialog).display
  })
  
  if (body) {
    console.log('Body尺寸:', {
      width: body.offsetWidth,
      height: body.offsetHeight,
      display: getComputedStyle(body).display
    })
  }
  
  if (container) {
    console.log('Monaco容器尺寸:', {
      width: container.offsetWidth,
      height: container.offsetHeight,
      display: getComputedStyle(container).display
    })
  }
  
  // 6. 强制触发Monaco布局更新
  console.log('\n🔄 触发Monaco布局更新...')
  
  // 方法1：通过容器引用直接调用layout
  if (container && container.__monacoEditor) {
    const dims = {
      width: container.offsetWidth,
      height: container.offsetHeight
    }
    console.log('📐 通过容器引用更新Monaco:', dims)
    container.__monacoEditor.layout(dims)
  }
  
  // 方法2：触发window resize事件
  window.dispatchEvent(new Event('resize'))
  
  setTimeout(() => {
    if (container && container.__monacoEditor) {
      container.__monacoEditor.layout()
    }
    window.dispatchEvent(new Event('resize'))
    console.log('✅ 第二次布局更新完成')
  }, 200)
  
  setTimeout(() => {
    if (container && container.__monacoEditor) {
      container.__monacoEditor.layout()
    }
    window.dispatchEvent(new Event('resize'))
    console.log('✅ 第三次布局更新完成')
    
    // 最终检查Monaco编辑器的实际高度
    const monacoEditors = document.querySelectorAll('.monaco-editor')
    console.log(`\n📊 找到 ${monacoEditors.length} 个Monaco编辑器实例`)
    monacoEditors.forEach((editor, index) => {
      console.log(`   编辑器 ${index + 1}: ${editor.offsetWidth}x${editor.offsetHeight}`)
    })
  }, 500)
  
  console.log('\n========================================')
  console.log('✅ 修复完成！')
  console.log('========================================')
  console.log('')
  console.log('如果现在还看不到代码，请：')
  console.log('1. 关闭对话框')
  console.log('2. 刷新页面 (Ctrl+F5)')
  console.log('3. 重新点击"查看代码差异"')
  console.log('')
  
  return {
    success: true,
    dialogHeight: dialog.offsetHeight,
    containerHeight: container?.offsetHeight
  }
})()

