/**
 * 简化版诊断脚本 - 适用于所有浏览器环境
 * 
 * 使用方法：
 * 1. 在代码审查页面点击任意位置
 * 2. 按F12打开Console
 * 3. 复制此脚本并粘贴执行
 */

(function simpleCheck() {
  console.log('========================================')
  console.log('🔍 简化版诊断工具')
  console.log('========================================\n')
  
  console.log('📋 步骤1：检查localStorage')
  console.log('------------------------------------')
  
  try {
    const fileStoreData = localStorage.getItem('file-store')
    const sessionStoreData = localStorage.getItem('session-store')
    
    console.log('文件存储数据存在:', !!fileStoreData)
    console.log('会话存储数据存在:', !!sessionStoreData)
    
    if (fileStoreData) {
      const data = JSON.parse(fileStoreData)
      console.log('\n文件存储详情:')
      console.log('  - 会话文件键:', Object.keys(data.sessionFiles || {}))
      console.log('  - 文件内容键:', Object.keys(data.sessionFileContents || {}))
      console.log('  - 当前文件ID:', Object.keys(data.currentFileIds || {}))
      
      // 检查每个会话的文件
      for (const sessionId in data.sessionFiles || {}) {
        const files = data.sessionFiles[sessionId]
        console.log(`\n  会话 ${sessionId.substring(0, 8)}...:`)
        console.log(`    - 文件数量: ${files.length}`)
        files.forEach(file => {
          console.log(`    - 文件: ${file.filename} (ID: ${file.file_id.substring(0, 8)}...)`)
        })
        
        // 检查文件内容
        const contents = data.sessionFileContents?.[sessionId] || {}
        console.log(`    - 已保存内容的文件: ${Object.keys(contents).length}`)
        for (const fileId in contents) {
          const content = contents[fileId]
          console.log(`      * ${fileId.substring(0, 8)}...: ${content.length} 字符`)
        }
      }
    }
    
    if (sessionStoreData) {
      const data = JSON.parse(sessionStoreData)
      console.log('\n会话存储详情:')
      console.log('  - 会话数量:', (data.sessions || []).length)
      console.log('  - 当前会话ID:', data.currentSessionId?.substring(0, 8) + '...' || 'null')
    }
    
  } catch (error) {
    console.error('❌ 读取localStorage失败:', error)
  }
  
  console.log('\n========================================')
  console.log('📋 步骤2：检查页面元素')
  console.log('------------------------------------')
  
  // 检查关键DOM元素
  const elements = {
    '文件Tab容器': document.querySelector('.file-tabs'),
    '代码编辑器': document.querySelector('.code-editor'),
    '消息列表': document.querySelector('.message-list'),
    'Monaco编辑器': document.querySelector('.monaco-editor'),
    '对话框': document.querySelector('.diff-dialog-wrapper')
  }
  
  for (const [name, el] of Object.entries(elements)) {
    console.log(`  ${name}:`, el ? '✅ 存在' : '❌ 不存在')
  }
  
  // 检查文件Tab
  const fileTabs = document.querySelectorAll('.file-tab')
  console.log(`\n  找到 ${fileTabs.length} 个文件Tab`)
  fileTabs.forEach((tab, i) => {
    console.log(`    ${i + 1}. ${tab.textContent.trim()} ${tab.classList.contains('active') ? '(当前)' : ''}`)
  })
  
  console.log('\n========================================')
  console.log('📋 步骤3：手动检查建议')
  console.log('------------------------------------')
  console.log('')
  console.log('请按照以下步骤手动检查：')
  console.log('')
  console.log('1️⃣ 检查是否有上传的文件')
  console.log('   - 查看页面右侧是否有文件Tab')
  console.log('   - 如果没有，请先上传一个代码文件')
  console.log('')
  console.log('2️⃣ 检查是否有AI回复')
  console.log('   - 查看聊天区域是否有AI的代码审查结果')
  console.log('   - 如果没有，请发送消息触发审查')
  console.log('')
  console.log('3️⃣ 点击"查看代码差异"时观察Console')
  console.log('   - 应该看到类似这样的日志：')
  console.log('   - "=== 开始查看代码差异 ===\"')
  console.log('   - "原始代码长度: XXX"')
  console.log('   - "修改后代码长度: XXX"')
  console.log('')
  console.log('4️⃣ 如果看到"原始代码长度: 0"')
  console.log('   - 说明文件内容没有被保存')
  console.log('   - 请继续执行步骤4')
  console.log('')
  
  console.log('\n========================================')
  console.log('📋 步骤4：临时修复（如果内容为空）')
  console.log('------------------------------------')
  console.log('')
  console.log('如果确认文件内容为空，请：')
  console.log('')
  console.log('方案A：重新上传文件（推荐）')
  console.log('  1. 删除当前文件（点击文件Tab的X）')
  console.log('  2. 重新上传文件')
  console.log('  3. 发送消息触发审查')
  console.log('')
  console.log('方案B：等待进一步诊断')
  console.log('  - 请截图当前页面')
  console.log('  - 并告诉我上述检查结果')
  console.log('')
  
  console.log('========================================')
  console.log('诊断完成！')
  console.log('========================================\n')
  
  return {
    success: true,
    message: '请查看上面的输出，并按建议操作'
  }
})()

