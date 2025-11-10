/**
 * 代码差异对比页面为空 - 快速诊断脚本
 * 
 * 使用方法：
 * 1. 打开浏览器开发者工具 (F12)
 * 2. 切换到 Console 标签
 * 3. 复制整个脚本并粘贴到Console中
 * 4. 按Enter执行
 * 
 * 脚本会自动检查所有可能的问题并输出诊断报告
 */

(function diagnoseCodeDiff() {
  console.log('========================================')
  console.log('🔍 代码差异对比页面诊断工具')
  console.log('========================================\n')
  
  const issues = []
  const warnings = []
  const info = []
  
  try {
    // 1. 获取Vue实例
    const vueApp = window.__VUE_DEVTOOLS_GLOBAL_HOOK__?.apps?.[0]
    if (!vueApp) {
      issues.push('❌ 无法访问Vue应用实例，请确保页面已加载')
      throw new Error('Vue app not found')
    }
    info.push('✅ Vue应用实例已找到')
    
    // 2. 获取stores
    const ctx = vueApp._container?._vnode?.component?.appContext?.config?.globalProperties
    if (!ctx) {
      issues.push('❌ 无法访问全局属性')
      throw new Error('Global properties not accessible')
    }
    
    const fileStore = ctx.$fileStore
    const sessionStore = ctx.$sessionStore
    const messageStore = ctx.$messageStore
    
    if (!fileStore || !sessionStore || !messageStore) {
      issues.push('❌ 无法访问Pinia stores')
      throw new Error('Stores not found')
    }
    info.push('✅ Pinia stores已找到')
    
    console.log('\n📊 === 1. 会话状态检查 ===')
    console.log('当前会话ID:', sessionStore.currentSessionId)
    if (!sessionStore.currentSessionId) {
      issues.push('❌ 没有当前会话，请先创建会话')
    } else {
      info.push('✅ 当前会话: ' + sessionStore.currentSessionId)
    }
    
    console.log('\n📊 === 2. 文件状态检查 ===')
    console.log('已上传文件数:', fileStore.uploadedFiles?.length || 0)
    console.log('文件列表:', fileStore.uploadedFiles)
    
    if (!fileStore.uploadedFiles || fileStore.uploadedFiles.length === 0) {
      warnings.push('⚠️ 没有上传任何文件')
    } else {
      info.push(`✅ 已上传 ${fileStore.uploadedFiles.length} 个文件`)
    }
    
    console.log('当前选中文件ID:', fileStore.currentFileId)
    console.log('当前选中文件:', fileStore.currentFile)
    
    if (!fileStore.currentFile) {
      issues.push('❌ 没有选中文件，请先选择一个文件')
    } else {
      info.push(`✅ 当前文件: ${fileStore.currentFile.filename}`)
    }
    
    console.log('\n📊 === 3. 文件内容检查 ===')
    console.log('fileContents对象:', fileStore.fileContents)
    console.log('当前文件内容长度:', fileStore.currentFileContent?.length || 0)
    
    if (fileStore.currentFile) {
      const content = fileStore.currentFileContent
      if (!content || content.length === 0) {
        issues.push('❌ 当前文件内容为空！这是主要问题！')
        console.log('🔍 详细信息:')
        console.log('  - 文件ID:', fileStore.currentFileId)
        console.log('  - fileContents:', fileStore.fileContents)
        console.log('  - sessionFileContents:', fileStore.sessionFileContents)
        
        // 检查是否存储在localStorage中
        const stored = localStorage.getItem('file-store')
        if (stored) {
          const data = JSON.parse(stored)
          console.log('  - LocalStorage中的文件内容:', data.sessionFileContents?.[sessionStore.currentSessionId])
        }
      } else {
        info.push(`✅ 文件内容长度: ${content.length} 字符`)
        console.log('文件内容前100字符:', content.substring(0, 100))
      }
    }
    
    console.log('\n📊 === 4. 消息状态检查 ===')
    const messages = messageStore.messages?.[sessionStore.currentSessionId] || []
    console.log('当前会话消息数:', messages.length)
    
    if (messages.length === 0) {
      warnings.push('⚠️ 当前会话没有消息')
    } else {
      info.push(`✅ 当前会话有 ${messages.length} 条消息`)
      
      // 查找最后一条AI消息
      const lastAIMessage = [...messages].reverse().find(m => m.role === 'assistant')
      if (lastAIMessage) {
        console.log('最后一条AI消息长度:', lastAIMessage.content?.length || 0)
        console.log('是否包含代码块:', /```[\s\S]*?```/.test(lastAIMessage.content || ''))
        console.log('是否包含结构化修改指令:', /####\s*🔧\s*结构化修改指令/.test(lastAIMessage.content || ''))
        
        if (!lastAIMessage.content || lastAIMessage.content.length === 0) {
          warnings.push('⚠️ AI消息内容为空')
        } else {
          info.push('✅ 找到AI消息')
        }
      } else {
        warnings.push('⚠️ 没有AI回复消息')
      }
    }
    
    console.log('\n📊 === 5. DOM元素检查 ===')
    
    // 检查Monaco编辑器是否存在
    const monacoEditor = document.querySelector('.monaco-diff-editor')
    console.log('Monaco Diff Editor元素:', monacoEditor ? '✅ 存在' : '❌ 不存在')
    
    if (!monacoEditor) {
      warnings.push('⚠️ Monaco Diff Editor DOM元素未找到')
    }
    
    // 检查对话框
    const dialogWrapper = document.querySelector('.diff-dialog-wrapper')
    const elDialog = document.querySelector('.diff-dialog-wrapper .el-dialog')
    console.log('对话框包装器:', dialogWrapper ? '✅ 存在' : '❌ 不存在')
    console.log('Element Plus对话框:', elDialog ? '✅ 存在' : '❌ 不存在')
    
    if (elDialog) {
      console.log('对话框尺寸:', {
        width: elDialog.style.width || window.getComputedStyle(elDialog).width,
        height: elDialog.style.height || window.getComputedStyle(elDialog).height
      })
    }
    
    console.log('\n📊 === 6. localStorage检查 ===')
    const fileStoreData = localStorage.getItem('file-store')
    if (fileStoreData) {
      try {
        const data = JSON.parse(fileStoreData)
        console.log('localStorage中的会话文件:', Object.keys(data.sessionFiles || {}))
        console.log('localStorage中的文件内容:', Object.keys(data.sessionFileContents || {}))
        info.push('✅ localStorage数据存在')
      } catch (e) {
        warnings.push('⚠️ localStorage数据解析失败')
      }
    } else {
      warnings.push('⚠️ localStorage中没有文件数据')
    }
    
  } catch (error) {
    issues.push(`❌ 诊断过程中出错: ${error.message}`)
    console.error('诊断错误:', error)
  }
  
  // 输出诊断报告
  console.log('\n')
  console.log('========================================')
  console.log('📋 诊断报告')
  console.log('========================================\n')
  
  if (issues.length > 0) {
    console.log('❌ 发现 ' + issues.length + ' 个问题:')
    issues.forEach((issue, i) => console.log(`  ${i + 1}. ${issue}`))
  }
  
  if (warnings.length > 0) {
    console.log('\n⚠️  ' + warnings.length + ' 个警告:')
    warnings.forEach((warning, i) => console.log(`  ${i + 1}. ${warning}`))
  }
  
  if (info.length > 0) {
    console.log('\n✅ 正常状态:')
    info.forEach((i, idx) => console.log(`  ${idx + 1}. ${i}`))
  }
  
  // 提供解决方案
  console.log('\n========================================')
  console.log('💡 解决方案建议')
  console.log('========================================\n')
  
  if (issues.some(i => i.includes('文件内容为空'))) {
    console.log('🔧 主要问题：文件内容为空')
    console.log('')
    console.log('可能原因：')
    console.log('1. 文件上传后，内容没有被保存到fileStore')
    console.log('2. 页面刷新后，localStorage中的数据丢失或未正确加载')
    console.log('3. 文件ID不匹配，导致无法找到对应的内容')
    console.log('')
    console.log('解决步骤：')
    console.log('1. 尝试重新上传文件')
    console.log('2. 检查Console中是否有上传相关的错误')
    console.log('3. 如果问题依然存在，运行修复脚本（见下方）')
  }
  
  if (issues.some(i => i.includes('没有选中文件'))) {
    console.log('🔧 问题：没有选中文件')
    console.log('')
    console.log('解决方案：')
    console.log('1. 先上传一个代码文件')
    console.log('2. 点击文件Tab选中文件')
    console.log('3. 然后再点击"查看代码差异"')
  }
  
  if (warnings.some(w => w.includes('没有AI回复'))) {
    console.log('🔧 问题：没有AI回复')
    console.log('')
    console.log('解决方案：')
    console.log('1. 发送一条消息触发代码审查')
    console.log('2. 等待AI返回审查结果')
    console.log('3. 然后再点击"查看代码差异"')
  }
  
  console.log('\n========================================')
  console.log('🛠️  临时修复脚本')
  console.log('========================================\n')
  console.log('如果文件内容为空，可以运行以下修复脚本：')
  console.log('')
  console.log('// 复制以下代码到Console执行：')
  console.log('(function fixFileContent() {')
  console.log('  const ctx = window.__VUE_DEVTOOLS_GLOBAL_HOOK__.apps[0]._container._vnode.component.appContext.config.globalProperties')
  console.log('  const fileStore = ctx.$fileStore')
  console.log('  ')
  console.log('  const testCode = `def calculate_sum(numbers):')
  console.log('    total = 0')
  console.log('    for num in numbers:')
  console.log('        total += num')
  console.log('    return total`')
  console.log('  ')
  console.log('  if (fileStore.currentFileId) {')
  console.log('    fileStore.setFileContent(fileStore.currentFileId, testCode)')
  console.log('    console.log("✅ 已设置测试代码，长度:", testCode.length)')
  console.log('  } else {')
  console.log('    console.log("❌ 没有当前文件ID")')
  console.log('  }')
  console.log('})()')
  
  console.log('\n========================================')
  console.log('诊断完成！')
  console.log('========================================\n')
  
  // 返回诊断结果供进一步处理
  return {
    issues,
    warnings,
    info,
    hasIssues: issues.length > 0,
    hasWarnings: warnings.length > 0
  }
})()

