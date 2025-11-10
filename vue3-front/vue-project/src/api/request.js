import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const request = axios.create({
  // 使用 /code 前缀，为代码审查助手的专属API命名空间
  // 这样设计便于未来扩展其他AI应用（如文档助手、数据分析等）
  baseURL: '/api/v1/code',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 可以在这里添加token等
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const { code, data, message } = response.data
    
    // 如果返回码不是200，视为错误
    if (code !== 200) {
      ElMessage.error(message || '请求失败')
      return Promise.reject(new Error(message || '请求失败'))
    }
    
    // 返回data字段（实际数据）
    return data
  },
  (error) => {
    // 错误处理
    const message = error.response?.data?.message || error.message || '请求失败'
    
    ElMessage.error(message)
    
    return Promise.reject(error)
  }
)

export default request

