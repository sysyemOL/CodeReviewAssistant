import request from './request'

export const messageAPI = {
  // 创建消息
  createMessage(data) {
    return request({
      url: '/messages/',
      method: 'post',
      data
    })
  },
  
  // 获取会话的所有消息
  getSessionMessages(sessionId) {
    return request({
      url: `/messages/session/${sessionId}`,
      method: 'get'
    })
  },
  
  // 获取单个消息
  getMessage(messageId) {
    return request({
      url: `/messages/${messageId}`,
      method: 'get'
    })
  },
  
  // 更新消息
  updateMessage(messageId, data) {
    return request({
      url: `/messages/${messageId}`,
      method: 'patch',
      data
    })
  },
  
  // 删除消息
  deleteMessage(messageId) {
    return request({
      url: `/messages/${messageId}`,
      method: 'delete'
    })
  }
}

