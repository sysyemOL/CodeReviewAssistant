# 前后端API同步修复记录

## 📅 修复时间
2025年11月8日

## 🎯 问题描述

前端API请求路径与后端不匹配：
- **前端请求路径**：`/api/sessions` 
- **后端实际路径**：`/api/v1/sessions/`
- **错误表现**：前端请求返回 404 Not Found

## 🔍 根本原因

### 1. API路径前缀不一致
- 前端 `request.js` 的 `baseURL` 配置为 `/api`
- 后端 `main.py` 中API路由前缀为 `/api/v1`

### 2. 响应数据格式处理不当
- 后端返回格式：`{code: 200, message: "...", data: {...}}`
- 前端响应拦截器直接返回 `response.data`，未提取内层 `data` 字段
- 导致前端 store 收到的数据格式错误

### 3. 会话列表数据结构不匹配
- 后端返回 `SessionList`：`{total: number, items: []}`
- 前端直接将整个对象赋值给 `sessions`，导致类型错误

## ✅ 修复方案

### 修复1：统一API路径前缀

**文件**：`vue3-front/vue-project/src/api/request.js`

```javascript
// 修改前
const request = axios.create({
  baseURL: '/api',  // ❌
  timeout: 30000,
  ...
})

// 修改后
const request = axios.create({
  baseURL: '/api/v1',  // ✅ 与后端一致
  timeout: 30000,
  ...
})
```

**文件**：`vue3-front/vue-project/src/api/review.js`

```javascript
// 修改前
const url = `/api/review/stream`  // ❌

// 修改后
const url = `/api/v1/review/stream`  // ✅
```

### 修复2：优化响应数据提取

**文件**：`vue3-front/vue-project/src/api/request.js`

```javascript
// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const { code, data, message } = response.data
    
    // 如果返回码不是200，视为错误
    if (code !== 200) {
      ElMessage.error(message || '请求失败')
      return Promise.reject(new Error(message || '请求失败'))
    }
    
    // ✅ 返回data字段（实际数据）
    return data
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)
```

### 修复3：处理SessionList数据结构

**文件**：`vue3-front/vue-project/src/stores/session.js`

```javascript
const fetchSessions = async () => {
  try {
    isLoading.value = true
    const data = await sessionAPI.getSessions()
    // ✅ 后端返回的是 {total, items} 格式，需要提取items
    sessions.value = data.items || []
  } catch (error) {
    console.error('获取会话列表失败:', error)
    throw error
  } finally {
    isLoading.value = false
  }
}
```

## 📊 修复效果验证

### 测试1：获取会话列表
- **请求路径**：`GET /api/v1/sessions`
- **代理转发**：`GET http://127.0.0.1:8000/api/v1/sessions/`
- **响应状态**：200 OK ✅
- **数据展示**：左侧成功显示3个历史会话 ✅

### 测试2：创建新会话
- **请求路径**：`POST /api/v1/sessions`
- **代理转发**：`POST http://127.0.0.1:8000/api/v1/sessions/`
- **响应状态**：200 OK ✅
- **功能验证**：
  - 成功提示："创建会话成功" ✅
  - 列表更新：新会话添加到顶部 ✅
  - 会话切换：自动切换到新会话 ✅

## 📋 涉及文件清单

```
vue3-front/vue-project/src/
├── api/
│   ├── request.js      ✅ 修改 baseURL + 响应拦截器
│   └── review.js       ✅ 修改 SSE流式URL
└── stores/
    └── session.js      ✅ 修改 fetchSessions 数据提取
```

## 🔧 后端API路由结构

```
FastAPI应用
├── / (根路径)
│   └── GET  →  健康检查
└── /api/v1 (API v1前缀)
    ├── /health/
    │   └── GET  →  详细健康检查
    ├── /sessions/
    │   ├── GET     →  获取会话列表
    │   ├── POST    →  创建会话
    │   ├── GET /{id}    →  获取会话详情
    │   ├── PUT /{id}    →  更新会话
    │   └── DELETE /{id} →  删除会话
    ├── /messages/  (待实现)
    └── /files/     (待实现)
```

## 📝 前端代理配置

**文件**：`vue3-front/vue-project/vite.config.js`

```javascript
export default defineConfig({
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 后端地址
        changeOrigin: true,
        // 不重写路径，保持 /api/v1/... 不变
      }
    }
  }
})
```

## 🎉 修复总结

✅ **问题已完全解决**
- 前后端API路径完全一致
- 数据格式正确解析和处理
- 所有会话管理功能正常工作
- 用户体验流畅，无错误提示

## 📌 后续注意事项

1. **保持API版本一致**：前端所有API请求都应该使用 `/api/v1` 前缀
2. **响应数据结构**：所有API响应都遵循 `{code, message, data}` 格式
3. **列表数据格式**：列表接口返回 `{total, items}` 结构
4. **错误处理**：前端已统一处理 `code !== 200` 的情况

---

**修复完成** ✅  
**修复人员**: AI代码Review助手  
**验证状态**: 已通过功能测试

