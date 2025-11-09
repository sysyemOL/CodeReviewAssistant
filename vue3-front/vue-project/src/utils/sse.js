/**
 * SSE (Server-Sent Events) 客户端工具
 * 用于处理流式数据传输
 */

/**
 * SSE 连接类
 */
export class SSEClient {
  constructor(url, options = {}) {
    this.url = url
    this.options = options
    this.eventSource = null
    this.listeners = new Map()
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = options.maxReconnectAttempts || 3
    this.reconnectDelay = options.reconnectDelay || 1000
    this.abortController = null  // 用于中断请求
    this.reader = null  // 保存reader引用
  }

  /**
   * 连接到 SSE 端点
   */
  connect(data) {
    return new Promise((resolve, reject) => {
      try {
        // 使用 fetch + EventSource 模拟 (因为浏览器 EventSource 不支持 POST)
        // 我们使用 fetch 的 ReadableStream
        this._connectWithFetch(data, resolve, reject)
      } catch (error) {
        reject(error)
      }
    })
  }

  /**
   * 使用 Fetch API 连接
   */
  async _connectWithFetch(data, resolve, reject) {
    try {
      // 创建 AbortController 用于中断请求
      this.abortController = new AbortController()
      
      const response = await fetch(this.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream'
        },
        body: JSON.stringify(data),
        signal: this.abortController.signal
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      this.reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      resolve() // 连接成功

      // 读取流
      const readStream = async () => {
        try {
          while (true) {
            const { done, value } = await this.reader.read()
            
            if (done) {
              this._emit('close', null)
              break
            }

            // 解码数据
            buffer += decoder.decode(value, { stream: true })
            
            // 处理 SSE 消息
            const lines = buffer.split('\n')
            buffer = lines.pop() || '' // 保留未完成的行

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = line.slice(6) // 移除 'data: ' 前缀
                try {
                  const jsonData = JSON.parse(data)
                  this._handleMessage(jsonData)
                } catch (e) {
                  console.error('解析 SSE 数据失败:', e, data)
                }
              }
            }
          }
        } catch (error) {
          // 如果是主动中断，不触发error事件
          if (error.name === 'AbortError') {
            console.log('SSE 流已被用户中断')
            this._emit('abort', null)
          } else {
            console.error('读取流失败:', error)
            this._emit('error', error)
          }
        }
      }

      readStream()
    } catch (error) {
      console.error('连接失败:', error)
      this._emit('error', error)
      reject(error)
    }
  }

  /**
   * 处理消息
   */
  _handleMessage(data) {
    const { type } = data
    this._emit(type, data)
    this._emit('message', data) // 触发通用消息事件
  }

  /**
   * 监听事件
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  /**
   * 移除事件监听
   */
  off(event, callback) {
    if (!this.listeners.has(event)) return
    
    const callbacks = this.listeners.get(event)
    const index = callbacks.indexOf(callback)
    if (index > -1) {
      callbacks.splice(index, 1)
    }
  }

  /**
   * 触发事件
   */
  _emit(event, data) {
    if (!this.listeners.has(event)) return
    
    const callbacks = this.listeners.get(event)
    callbacks.forEach(callback => {
      try {
        callback(data)
      } catch (error) {
        console.error('事件回调执行失败:', error)
      }
    })
  }

  /**
   * 中断连接
   */
  abort() {
    if (this.abortController) {
      this.abortController.abort()
      this.abortController = null
    }
    if (this.reader) {
      this.reader.cancel()
      this.reader = null
    }
  }

  /**
   * 关闭连接
   */
  close() {
    this.abort()
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
    }
    this.listeners.clear()
  }
}

/**
 * 创建 SSE 连接
 * @param {string} url - SSE 端点 URL
 * @param {object} data - 请求数据
 * @param {object} callbacks - 事件回调 { onStart, onContent, onDone, onError }
 * @returns {SSEClient} - SSE 客户端实例
 */
export function createSSEConnection(url, data, callbacks = {}) {
  const client = new SSEClient(url)

  // 注册回调
  if (callbacks.onStart) {
    client.on('start', callbacks.onStart)
  }
  if (callbacks.onContent) {
    client.on('content', callbacks.onContent)
  }
  if (callbacks.onDone) {
    client.on('done', callbacks.onDone)
  }
  if (callbacks.onError) {
    client.on('error', callbacks.onError)
  }
  if (callbacks.onUserMessage) {
    client.on('user_message', callbacks.onUserMessage)
  }
  if (callbacks.onClose) {
    client.on('close', callbacks.onClose)
  }
  if (callbacks.onAbort) {
    client.on('abort', callbacks.onAbort)
  }
  if (callbacks.onThinking) {
    client.on('thinking', callbacks.onThinking)
  }

  // 连接
  client.connect(data).catch(error => {
    console.error('SSE 连接失败:', error)
    if (callbacks.onError) {
      callbacks.onError({ error: error.message })
    }
  })

  return client
}

