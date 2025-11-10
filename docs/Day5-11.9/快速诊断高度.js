// 快速诊断代码差异对话框的高度问题
// 在浏览器Console执行

(function diagnoseHeight() {
  console.log('========================================')
  console.log('📏 代码差异对话框高度诊断')
  console.log('========================================\n')
  
  const dialog = document.querySelector('.el-dialog.diff-dialog-wrapper') || document.querySelector('.diff-dialog-wrapper')
  const body = document.querySelector('.el-dialog__body')
  const monacoWrapper = document.querySelector('.monaco-diff-editor')
  const container = document.querySelector('.diff-editor-container')
  
  if (!dialog) {
    console.error('❌ 未找到对话框，请先打开"查看代码差异"')
    return
  }
  
  console.log('1️⃣ 对话框 (.el-dialog):')
  console.log('   - offsetHeight:', dialog.offsetHeight, 'px')
  console.log('   - clientHeight:', dialog.clientHeight, 'px')
  console.log('   - style.height:', dialog.style.height)
  console.log('   - computed height:', getComputedStyle(dialog).height)
  console.log('')
  
  if (body) {
    console.log('2️⃣ 对话框Body (.el-dialog__body):')
    console.log('   - offsetHeight:', body.offsetHeight, 'px')
    console.log('   - clientHeight:', body.clientHeight, 'px')
    console.log('   - style.height:', body.style.height || 'auto')
    console.log('   - computed height:', getComputedStyle(body).height)
    console.log('   - display:', getComputedStyle(body).display)
    console.log('   - flex-direction:', getComputedStyle(body).flexDirection)
    console.log('   - padding:', getComputedStyle(body).padding)
    console.log('')
  }
  
  if (monacoWrapper) {
    console.log('3️⃣ Monaco包装器 (.monaco-diff-editor):')
    console.log('   - offsetHeight:', monacoWrapper.offsetHeight, 'px')
    console.log('   - clientHeight:', monacoWrapper.clientHeight, 'px')
    console.log('   - computed height:', getComputedStyle(monacoWrapper).height)
    console.log('   - flex:', getComputedStyle(monacoWrapper).flex)
    console.log('   - flex-grow:', getComputedStyle(monacoWrapper).flexGrow)
    console.log('   - flex-shrink:', getComputedStyle(monacoWrapper).flexShrink)
    console.log('   - flex-basis:', getComputedStyle(monacoWrapper).flexBasis)
    console.log('   - margin:', getComputedStyle(monacoWrapper).margin)
    console.log('')
  }
  
  if (container) {
    console.log('4️⃣ 编辑器容器 (.diff-editor-container):')
    console.log('   - offsetHeight:', container.offsetHeight, 'px')
    console.log('   - clientHeight:', container.clientHeight, 'px')
    console.log('   - computed height:', getComputedStyle(container).height)
    console.log('   - flex:', getComputedStyle(container).flex)
    console.log('')
  }
  
  // 查找所有Monaco编辑器实例
  const monacoEditors = document.querySelectorAll('.monaco-editor')
  console.log('5️⃣ Monaco编辑器实例 (.monaco-editor):')
  console.log('   - 找到数量:', monacoEditors.length)
  monacoEditors.forEach((editor, index) => {
    console.log(`   - 编辑器 ${index + 1}:`, editor.offsetHeight, 'px')
  })
  console.log('')
  
  // 计算理论高度
  const dialogHeight = dialog.offsetHeight
  const bodyHeight = body?.offsetHeight || 0
  const monacoHeight = monacoWrapper?.offsetHeight || 0
  const containerHeight = container?.offsetHeight || 0
  
  console.log('========================================')
  console.log('📊 高度分析')
  console.log('========================================')
  console.log('对话框总高度:', dialogHeight, 'px')
  console.log('Body实际高度:', bodyHeight, 'px')
  console.log('Monaco包装器高度:', monacoHeight, 'px')
  console.log('编辑器容器高度:', containerHeight, 'px')
  console.log('')
  
  // 分析问题
  const headerEstimatedHeight = dialogHeight - bodyHeight
  console.log('Header估算高度:', headerEstimatedHeight, 'px')
  console.log('Body应该占比:', ((bodyHeight / dialogHeight) * 100).toFixed(1), '%')
  console.log('')
  
  if (bodyHeight < dialogHeight * 0.8) {
    console.warn('⚠️ Body高度过小，只占对话框的', ((bodyHeight / dialogHeight) * 100).toFixed(1), '%')
    console.warn('   建议检查 el-dialog__body 的 height 样式')
  }
  
  if (monacoHeight < bodyHeight * 0.8) {
    console.warn('⚠️ Monaco包装器高度过小，只占Body的', ((monacoHeight / bodyHeight) * 100).toFixed(1), '%')
    console.warn('   建议检查 .monaco-diff-editor 的 flex 样式')
  }
  
  console.log('\n========================================')
  console.log('✅ 诊断完成')
  console.log('========================================')
  
  return {
    dialogHeight,
    bodyHeight,
    monacoHeight,
    containerHeight
  }
})()

