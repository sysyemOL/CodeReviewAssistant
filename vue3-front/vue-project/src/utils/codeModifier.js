/**
 * 代码修改工具
 * 用于解析AI的结构化修改指令并应用到代码上
 */

/**
 * 修改指令类型
 */
export const ModificationType = {
  INSERT: 'INSERT',
  REPLACE: 'REPLACE',
  DELETE: 'DELETE'
}

/**
 * 解析AI消息中的结构化修改指令
 * @param {string} content - AI消息内容
 * @returns {Array} 修改指令数组
 */
export function parseModificationInstructions(content) {
  const instructions = []
  
  // 查找"结构化修改指令"部分（更宽松的匹配）
  // 匹配多种可能的标题格式：### 、#### 、带不带emoji等
  const structuredSectionMatch = content.match(/#{3,4}\s*(?:🔧\s*)?结构化修改指令([\s\S]*?)(?=#{3}|$)/i)
  if (!structuredSectionMatch) {
    console.log('❌ 未找到"结构化修改指令"标题部分')
    console.log('尝试搜索的内容:', content.substring(0, 500))
    return instructions
  }
  
  const structuredSection = structuredSectionMatch[1]
  console.log('✅ 找到结构化修改指令部分，长度:', structuredSection.length)
  console.log('内容前500字符:', structuredSection.substring(0, 500))
  
  // 匹配每个修改指令（**修改N：...** 开头）
  // 分两步：先找所有修改指令块，再解析每个块的详细内容
  const modificationBlockRegex = /\*\*修改\s*\d+\s*[：:][^\n]*\*\*[\s\S]*?(?=\*\*修改\s*\d+\s*[：:]|\*\*注意|\#{3}|$)/gi
  
  let blockMatch
  let matchCount = 0
  
  while ((blockMatch = modificationBlockRegex.exec(structuredSection)) !== null) {
    const block = blockMatch[0]
    matchCount++
    console.log(`\n========== 正在解析第 ${matchCount} 个修改指令块 ==========`)
    console.log('块内容:', block.substring(0, 200) + '...')
    
    // 解析描述
    const descMatch = block.match(/\*\*修改\s*\d+\s*[：:]\s*([^\n*]+)\*\*/)
    const description = descMatch ? descMatch[1].trim() : '未知修改'
    
    // 解析操作类型
    const typeMatch = block.match(/-?\s*操作类型\s*[：:]\s*(插入|替换|删除|INSERT|REPLACE|DELETE)/i)
    if (!typeMatch) {
      console.warn('⚠️ 未找到操作类型，跳过此修改')
      continue
    }
    const operationType = typeMatch[1]
    
    // 解析位置
    const posMatch = block.match(/-?\s*位置\s*[：:]\s*第?\s*(\d+)\s*(?:[-到至~]\s*(\d+))?\s*行?/)
    if (!posMatch) {
      console.warn('⚠️ 未找到位置信息，跳过此修改')
      continue
    }
    const startLine = posMatch[1]
    const endLine = posMatch[2]
    
    // 解析代码内容
    const contentMatch = block.match(/-?\s*内容\s*[：:]\s*\n```[^\n]*\n([\s\S]*?)```/)
    const codeContent = contentMatch ? contentMatch[1] : ''
    
    console.log('📝 解析结果：')
    console.log('  - 描述:', description)
    console.log('  - 操作类型:', operationType)
    console.log('  - 起始行:', startLine)
    console.log('  - 结束行:', endLine || startLine)
    console.log('  - 代码内容长度:', codeContent.length)
    console.log('  - 代码内容前100字符:', codeContent.substring(0, 100))
    
    // 标准化操作类型
    let type = operationType.toUpperCase()
    if (type === '插入') type = ModificationType.INSERT
    else if (type === '替换') type = ModificationType.REPLACE
    else if (type === '删除') type = ModificationType.DELETE
    
    const instruction = {
      description: description.trim(),
      type,
      startLine: parseInt(startLine),
      endLine: endLine ? parseInt(endLine) : parseInt(startLine),
      language: '',
      content: codeContent.trimEnd() // 保留开头的缩进，只去掉末尾空白
    }
    
    instructions.push(instruction)
    console.log('✅ 解析成功，已添加到指令列表')
  }
  
  if (matchCount === 0) {
    console.warn('⚠️ 找到"结构化修改指令"标题，但未能解析出具体指令')
    console.log('可能的原因：')
    console.log('1. AI没有严格按照 "**修改N：描述**" 格式输出')
    console.log('2. 缺少必需的 "操作类型" 或 "位置" 字段')
    console.log('3. 格式使用了不支持的变体')
  }
  
  // 按行号排序（从后往前，这样修改时不会影响后续行号）
  instructions.sort((a, b) => b.startLine - a.startLine)
  
  console.log(`📊 最终解析结果：共 ${instructions.length} 条有效指令`)
  
  return instructions
}

/**
 * 应用修改指令到代码上
 * @param {string} originalCode - 原始代码
 * @param {Array} instructions - 修改指令数组
 * @returns {string} 修改后的代码
 */
export function applyModifications(originalCode, instructions) {
  if (!originalCode || !instructions || instructions.length === 0) {
    console.warn('⚠️ 原始代码或指令为空，无法应用修改')
    return originalCode
  }
  
  // 将代码分割成行
  const lines = originalCode.split('\n')
  
  console.log('\n========== 开始应用修改指令 ==========')
  console.log('原始代码行数:', lines.length)
  console.log('待应用指令数:', instructions.length)
  
  // 从后往前应用修改（避免行号偏移）
  for (let i = 0; i < instructions.length; i++) {
    const instruction = instructions[i]
    const { type, startLine, endLine, content, description } = instruction
    
    console.log(`\n--- 应用第 ${i + 1} 个修改 ---`)
    console.log('描述:', description)
    console.log('类型:', type)
    console.log('位置:', `${startLine}-${endLine}`)
    console.log('内容长度:', content.length)
    console.log('内容前50字符:', content.substring(0, 50).replace(/\n/g, '\\n'))
    
    // 将行号转换为数组索引（从0开始）
    const startIndex = startLine - 1
    const endIndex = endLine - 1
    
    switch (type) {
      case ModificationType.INSERT:
        // 在指定行之前插入
        if (startIndex >= 0 && startIndex <= lines.length) {
          if (!content) {
            console.warn('⚠️ 插入内容为空，跳过此操作')
            break
          }
          const insertLines = content.split('\n')
          lines.splice(startIndex, 0, ...insertLines)
          console.log(`✅ 插入了 ${insertLines.length} 行`)
          console.log('插入的内容:', insertLines.map(line => line.substring(0, 50)).join(' | '))
        } else {
          console.error(`❌ 插入位置 ${startLine} 超出范围 (0-${lines.length})`)
        }
        break
        
      case ModificationType.REPLACE:
        // 替换指定行范围
        if (startIndex >= 0 && endIndex < lines.length && startIndex <= endIndex) {
          if (!content) {
            console.warn('⚠️ 替换内容为空，跳过此操作')
            break
          }
          const replaceLines = content.split('\n')
          const deleteCount = endIndex - startIndex + 1
          console.log(`将删除 ${deleteCount} 行，插入 ${replaceLines.length} 行`)
          lines.splice(startIndex, deleteCount, ...replaceLines)
          console.log(`✅ 替换完成`)
        } else {
          console.error(`❌ 替换范围 ${startLine}-${endLine} 无效 (总行数: ${lines.length})`)
        }
        break
        
      case ModificationType.DELETE:
        // 删除指定行范围
        if (startIndex >= 0 && endIndex < lines.length && startIndex <= endIndex) {
          const deleteCount = endIndex - startIndex + 1
          const deletedLines = lines.slice(startIndex, endIndex + 1)
          console.log('将删除的行:', deletedLines.map(line => line.substring(0, 30)).join(' | '))
          lines.splice(startIndex, deleteCount)
          console.log(`✅ 删除了 ${deleteCount} 行`)
        } else {
          console.error(`❌ 删除范围 ${startLine}-${endLine} 无效 (总行数: ${lines.length})`)
        }
        break
        
      default:
        console.error(`❌ 未知的操作类型: ${type}`)
    }
    
    console.log('当前代码行数:', lines.length)
  }
  
  const modifiedCode = lines.join('\n')
  console.log('\n========== 修改完成 ==========')
  console.log('最终代码行数:', lines.length)
  console.log('最终代码前200字符:', modifiedCode.substring(0, 200))
  
  return modifiedCode
}

/**
 * 检查消息是否包含结构化修改指令
 * @param {string} content - AI消息内容
 * @returns {boolean}
 */
export function hasModificationInstructions(content) {
  return /####\s*🔧\s*结构化修改指令/.test(content)
}

/**
 * 生成修改预览信息
 * @param {Array} instructions - 修改指令数组
 * @returns {string} 预览文本
 */
export function generateModificationPreview(instructions) {
  if (!instructions || instructions.length === 0) {
    return '无修改指令'
  }
  
  const summary = instructions.map((inst, index) => {
    const { type, startLine, endLine, description } = inst
    let action = ''
    
    switch (type) {
      case ModificationType.INSERT:
        action = `在第${startLine}行插入代码`
        break
      case ModificationType.REPLACE:
        action = `替换第${startLine}-${endLine}行`
        break
      case ModificationType.DELETE:
        action = `删除第${startLine}-${endLine}行`
        break
      default:
        action = '未知操作'
    }
    
    return `${index + 1}. ${action}：${description}`
  }).join('\n')
  
  return `将执行 ${instructions.length} 个修改操作：\n\n${summary}`
}

