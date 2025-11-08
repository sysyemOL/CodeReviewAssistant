/**
 * 格式化时间
 */
export function formatTime(timestamp) {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour
  
  if (diff < minute) {
    return '刚刚'
  } else if (diff < hour) {
    return `${Math.floor(diff / minute)}分钟前`
  } else if (diff < day) {
    return `${Math.floor(diff / hour)}小时前`
  } else if (diff < 7 * day) {
    return `${Math.floor(diff / day)}天前`
  } else {
    return date.toLocaleDateString()
  }
}

/**
 * 格式化文件大小
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

/**
 * 根据文件名获取语言
 */
export function getLanguageFromFilename(filename) {
  const ext = filename.split('.').pop().toLowerCase()
  const languageMap = {
    'py': 'python',
    'js': 'javascript',
    'ts': 'typescript',
    'jsx': 'javascript',
    'tsx': 'typescript',
    'java': 'java',
    'go': 'go',
    'rs': 'rust',
    'cpp': 'cpp',
    'c': 'c',
    'cs': 'csharp',
    'php': 'php',
    'rb': 'ruby',
    'swift': 'swift',
    'kt': 'kotlin',
    'vue': 'html'  // Vue文件使用HTML语法高亮
  }
  return languageMap[ext] || 'plaintext'
}

