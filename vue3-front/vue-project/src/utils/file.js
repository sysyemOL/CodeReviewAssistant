/**
 * 读取文件内容
 */
export function readFileContent(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.onerror = (e) => reject(e)
    reader.readAsText(file)
  })
}

/**
 * 检查文件类型是否允许
 */
export function isAllowedFileType(filename) {
  const allowedExtensions = [
    '.py', '.js', '.jsx', '.ts', '.tsx',
    '.java', '.go', '.rs', '.cpp', '.c',
    '.cs', '.php', '.rb', '.swift', '.kt', '.vue'
  ]
  return allowedExtensions.some(ext => filename.toLowerCase().endsWith(ext))
}

/**
 * 检查文件大小
 */
export function isFileSizeValid(size, maxSize = 10 * 1024 * 1024) {
  return size <= maxSize
}

/**
 * 生成唯一文件ID
 */
export function generateFileId() {
  return `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

