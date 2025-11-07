import request from './request'

export const reviewAPI = {
  // 代码审查（非流式）
  analyzeCode(data) {
    return request({
      url: '/review/analyze',
      method: 'post',
      data
    })
  },
  
  // 对话交互
  chat(data) {
    return request({
      url: '/review/chat',
      method: 'post',
      data
    })
  }
}

// SSE流式审查
export function createReviewStream(data, onMessage, onError, onComplete) {
  const url = `/api/review/stream`
  const eventSource = new EventSource(url)
  
  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage && onMessage(data)
    } catch (error) {
      console.error('解析SSE数据失败:', error)
    }
  }
  
  eventSource.onerror = (error) => {
    console.error('SSE连接错误:', error)
    eventSource.close()
    onError && onError(error)
  }
  
  // 监听完成事件
  eventSource.addEventListener('complete', () => {
    eventSource.close()
    onComplete && onComplete()
  })
  
  return {
    close: () => eventSource.close()
  }
}

