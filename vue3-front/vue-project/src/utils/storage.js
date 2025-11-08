/**
 * LocalStorage工具函数
 */

const STORAGE_PREFIX = 'ai_code_review_'

/**
 * 设置LocalStorage
 */
export function setStorage(key, value) {
  try {
    const fullKey = STORAGE_PREFIX + key
    localStorage.setItem(fullKey, JSON.stringify(value))
    return true
  } catch (error) {
    console.error('存储失败:', error)
    return false
  }
}

/**
 * 获取LocalStorage
 */
export function getStorage(key, defaultValue = null) {
  try {
    const fullKey = STORAGE_PREFIX + key
    const value = localStorage.getItem(fullKey)
    return value ? JSON.parse(value) : defaultValue
  } catch (error) {
    console.error('读取失败:', error)
    return defaultValue
  }
}

/**
 * 删除LocalStorage
 */
export function removeStorage(key) {
  try {
    const fullKey = STORAGE_PREFIX + key
    localStorage.removeItem(fullKey)
    return true
  } catch (error) {
    console.error('删除失败:', error)
    return false
  }
}

/**
 * 清空所有LocalStorage
 */
export function clearStorage() {
  try {
    const keys = Object.keys(localStorage)
    keys.forEach(key => {
      if (key.startsWith(STORAGE_PREFIX)) {
        localStorage.removeItem(key)
      }
    })
    return true
  } catch (error) {
    console.error('清空失败:', error)
    return false
  }
}

