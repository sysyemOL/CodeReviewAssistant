import { ElMessage, ElNotification } from 'element-plus'

/**
 * 错误类型枚举
 */
export const ErrorType = {
  NETWORK: 'network',
  AUTH: 'auth',
  VALIDATION: 'validation',
  SERVER: 'server',
  CLIENT: 'client',
  UNKNOWN: 'unknown'
}

/**
 * 错误消息映射
 */
const errorMessages = {
  // 网络错误
  'Network Error': '网络连接失败，请检查您的网络设置',
  'timeout': '请求超时，请稍后再试',
  
  // 认证错误
  401: '未授权，请重新登录',
  403: '权限不足，无法执行此操作',
  
  // 客户端错误
  400: '请求参数错误，请检查输入内容',
  404: '请求的资源不存在',
  
  // 服务器错误
  500: '服务器内部错误，请稍后再试',
  502: '网关错误，服务暂时不可用',
  503: '服务暂时不可用，请稍后再试',
  
  // 文件相关错误
  'FILE_TOO_LARGE': '文件大小超过限制（最大10MB）',
  'FILE_TYPE_NOT_SUPPORTED': '不支持的文件类型',
  'FILE_UPLOAD_FAILED': '文件上传失败，请重试',
  
  // 会话相关错误
  'SESSION_NOT_FOUND': '会话不存在或已过期',
  'SESSION_EXPIRED': '会话已过期，请刷新页面',
  
  // AI相关错误
  'AI_SERVICE_ERROR': 'AI服务暂时不可用，请稍后再试',
  'RATE_LIMIT_EXCEEDED': '请求过于频繁，请稍后再试',
  'INVALID_API_KEY': 'API密钥无效，请联系管理员'
}

/**
 * 获取友好的错误消息
 * @param {Error|string|number} error 错误对象、消息或状态码
 * @returns {string} 友好的错误消息
 */
export function getFriendlyErrorMessage(error) {
  // 如果是字符串，直接查找映射
  if (typeof error === 'string') {
    return errorMessages[error] || error
  }
  
  // 如果是数字（状态码），查找映射
  if (typeof error === 'number') {
    return errorMessages[error] || `请求失败 (${error})`
  }
  
  // 如果是Error对象
  if (error instanceof Error) {
    // 首先检查错误消息是否在映射中
    if (errorMessages[error.message]) {
      return errorMessages[error.message]
    }
    
    // 检查响应状态码
    if (error.response?.status) {
      const status = error.response.status
      if (errorMessages[status]) {
        return errorMessages[status]
      }
    }
    
    // 检查错误代码
    if (error.code && errorMessages[error.code]) {
      return errorMessages[error.code]
    }
    
    // 返回原始错误消息
    return error.message || '操作失败，请稍后重试'
  }
  
  return '未知错误，请稍后重试'
}

/**
 * 确定错误类型
 * @param {Error} error 错误对象
 * @returns {string} 错误类型
 */
export function getErrorType(error) {
  if (error.message === 'Network Error' || error.code === 'ECONNABORTED') {
    return ErrorType.NETWORK
  }
  
  const status = error.response?.status
  if (status === 401 || status === 403) {
    return ErrorType.AUTH
  }
  
  if (status >= 400 && status < 500) {
    return ErrorType.CLIENT
  }
  
  if (status >= 500) {
    return ErrorType.SERVER
  }
  
  return ErrorType.UNKNOWN
}

/**
 * 显示错误消息（轻量级，用于一般错误）
 * @param {Error|string} error 错误对象或消息
 * @param {string} title 标题（可选）
 */
export function showError(error, title = '操作失败') {
  const message = typeof error === 'string' ? error : getFriendlyErrorMessage(error)
  
  ElMessage({
    type: 'error',
    message,
    duration: 3000,
    showClose: true
  })
}

/**
 * 显示错误通知（重要错误，包含更多信息）
 * @param {Error|string} error 错误对象或消息
 * @param {string} title 标题
 * @param {Object} options 额外选项
 */
export function showErrorNotification(error, title = '操作失败', options = {}) {
  const message = typeof error === 'string' ? error : getFriendlyErrorMessage(error)
  const errorType = typeof error === 'object' ? getErrorType(error) : ErrorType.UNKNOWN
  
  // 根据错误类型添加建议
  let suggestion = ''
  switch (errorType) {
    case ErrorType.NETWORK:
      suggestion = '建议：检查网络连接后重试'
      break
    case ErrorType.AUTH:
      suggestion = '建议：请重新登录后再试'
      break
    case ErrorType.SERVER:
      suggestion = '建议：服务器繁忙，请稍后再试'
      break
    case ErrorType.CLIENT:
      suggestion = '建议：检查输入内容是否正确'
      break
  }
  
  ElNotification({
    title,
    message: suggestion ? `${message}\n\n${suggestion}` : message,
    type: 'error',
    duration: 5000,
    ...options
  })
}

/**
 * 显示成功消息
 * @param {string} message 消息内容
 * @param {number} duration 显示时长
 */
export function showSuccess(message, duration = 3000) {
  ElMessage({
    type: 'success',
    message,
    duration,
    showClose: true
  })
}

/**
 * 显示警告消息
 * @param {string} message 消息内容
 * @param {number} duration 显示时长
 */
export function showWarning(message, duration = 3000) {
  ElMessage({
    type: 'warning',
    message,
    duration,
    showClose: true
  })
}

/**
 * 显示信息消息
 * @param {string} message 消息内容
 * @param {number} duration 显示时长
 */
export function showInfo(message, duration = 3000) {
  ElMessage({
    type: 'info',
    message,
    duration,
    showClose: true
  })
}

/**
 * 全局错误处理器
 * @param {Error} error 错误对象
 * @param {string} context 错误上下文
 */
export function handleError(error, context = '') {
  console.error(`[错误] ${context}:`, error)
  
  const errorType = getErrorType(error)
  
  // 根据错误类型决定使用Message还是Notification
  if (errorType === ErrorType.NETWORK || errorType === ErrorType.AUTH || errorType === ErrorType.SERVER) {
    showErrorNotification(error, context || '操作失败')
  } else {
    showError(error, context)
  }
}

export default {
  ErrorType,
  getFriendlyErrorMessage,
  getErrorType,
  showError,
  showErrorNotification,
  showSuccess,
  showWarning,
  showInfo,
  handleError
}

