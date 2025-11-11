/**
 * 聊天对话 API
 */
import request from './request'
import { createSSEConnection } from '@/utils/sse'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * 发送聊天消息（流式）
 * @param {object} data - { session_id, message, file_ids }
 * @param {object} callbacks - { onStart, onContent, onDone, onError }
 * @returns {SSEClient} - SSE 客户端实例
 */
export function sendMessageStream(data, callbacks) {
  const url = `${BASE_URL}/api/v1/code/chat/stream`
  return createSSEConnection(url, data, callbacks)
}

/**
 * 发送聊天消息（非流式）
 * @param {object} data - { session_id, message, file_ids }
 * @returns {Promise}
 */
export function sendMessage(data) {
  return request({
    url: '/chat/send',
    method: 'post',
    data
  })
}

