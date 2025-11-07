import request from './request'

export const sessionAPI = {
  // 获取会话列表
  getSessions() {
    return request({
      url: '/sessions',
      method: 'get'
    })
  },
  
  // 创建会话
  createSession(data) {
    return request({
      url: '/sessions',
      method: 'post',
      data
    })
  },
  
  // 获取会话详情
  getSession(sessionId) {
    return request({
      url: `/sessions/${sessionId}`,
      method: 'get'
    })
  },
  
  // 更新会话
  updateSession(sessionId, data) {
    return request({
      url: `/sessions/${sessionId}`,
      method: 'put',
      data
    })
  },
  
  // 删除会话
  deleteSession(sessionId) {
    return request({
      url: `/sessions/${sessionId}`,
      method: 'delete'
    })
  }
}

