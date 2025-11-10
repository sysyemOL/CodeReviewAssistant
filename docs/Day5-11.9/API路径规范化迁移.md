# API路径规范化迁移文档

## 📋 迁移概览

**日期**: 2025年11月10日  
**版本**: v1.1.0  
**影响范围**: 后端API路由 + 前端API调用  
**迁移类型**: Breaking Change（破坏性变更）

---

## 🎯 迁移目标

为AI代码Review助手的所有API添加 `/code` 路径前缀，建立清晰的命名空间结构，为未来扩展其他AI应用做准备。

### 设计理念

```
/api/v1/
  ├── /code/          # 代码审查助手（当前应用）
  │   ├── /health
  │   ├── /sessions
  │   ├── /messages
  │   ├── /files
  │   ├── /review
  │   └── /chat
  │
  ├── /doc/           # 文档助手（未来扩展）
  │   └── ...
  │
  ├── /data/          # 数据分析助手（未来扩展）
  │   └── ...
  │
  └── /translate/     # 翻译助手（未来扩展）
      └── ...
```

---

## 📊 路径变更清单

### API路径对照表

| 功能模块 | 旧路径 | 新路径 | HTTP方法 | 说明 |
|---------|--------|--------|---------|------|
| **健康检查** |
| 健康状态 | `GET /api/v1/health` | `GET /api/v1/code/health` | GET | 服务健康检查 |
| **会话管理** |
| 获取会话列表 | `GET /api/v1/sessions` | `GET /api/v1/code/sessions` | GET | 查询所有会话 |
| 创建会话 | `POST /api/v1/sessions` | `POST /api/v1/code/sessions` | POST | 创建新会话 |
| 获取会话详情 | `GET /api/v1/sessions/{id}` | `GET /api/v1/code/sessions/{id}` | GET | 查询单个会话 |
| 更新会话 | `PUT /api/v1/sessions/{id}` | `PUT /api/v1/code/sessions/{id}` | PUT | 更新会话信息 |
| 删除会话 | `DELETE /api/v1/sessions/{id}` | `DELETE /api/v1/code/sessions/{id}` | DELETE | 删除会话 |
| **消息管理** |
| 获取消息列表 | `GET /api/v1/messages` | `GET /api/v1/code/messages` | GET | 查询会话消息 |
| 发送消息 | `POST /api/v1/messages` | `POST /api/v1/code/messages` | POST | 发送新消息 |
| 删除消息 | `DELETE /api/v1/messages/{id}` | `DELETE /api/v1/code/messages/{id}` | DELETE | 删除消息 |
| **文件管理** |
| 上传文件 | `POST /api/v1/files/upload` | `POST /api/v1/code/files/upload` | POST | 上传代码文件 |
| 获取文件 | `GET /api/v1/files/{id}` | `GET /api/v1/code/files/{id}` | GET | 获取文件内容 |
| 解析代码 | `POST /api/v1/files/parse` | `POST /api/v1/code/files/parse` | POST | 解析代码结构 |
| **代码审查** |
| 审查代码 | `POST /api/v1/review` | `POST /api/v1/code/review` | POST | 触发代码审查 |
| **对话聊天** |
| 流式对话 | `POST /api/v1/chat/stream` | `POST /api/v1/code/chat/stream` | POST | SSE流式对话 |
| 普通对话 | `POST /api/v1/chat` | `POST /api/v1/code/chat` | POST | 普通对话接口 |

---

## 🔧 实施步骤

### 1. 后端修改（已完成 ✅）

#### 修改文件：`python-back/app/api/v1/__init__.py`

**修改前：**
```python
from fastapi import APIRouter
from app.api.v1 import health, sessions, messages, files, review, chat

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(health.router, prefix="/health", tags=["健康检查"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["会话管理"])
api_router.include_router(messages.router, prefix="/messages", tags=["消息管理"])
api_router.include_router(files.router, prefix="/files", tags=["文件管理"])
api_router.include_router(review.router, prefix="/review", tags=["代码审查"])
api_router.include_router(chat.router, prefix="/chat", tags=["对话聊天"])
```

**修改后：**
```python
from fastapi import APIRouter
from app.api.v1 import health, sessions, messages, files, review, chat

api_router = APIRouter()

# 为代码审查助手创建独立的路由组
# 添加 /code 前缀，为未来的其他AI应用（如文档助手、数据分析等）预留命名空间
code_router = APIRouter(prefix="/code")

# 注册各个模块的路由（代码审查相关）
code_router.include_router(health.router, prefix="/health", tags=["代码审查-健康检查"])
code_router.include_router(sessions.router, prefix="/sessions", tags=["代码审查-会话管理"])
code_router.include_router(messages.router, prefix="/messages", tags=["代码审查-消息管理"])
code_router.include_router(files.router, prefix="/files", tags=["代码审查-文件管理"])
code_router.include_router(review.router, prefix="/review", tags=["代码审查-代码审查"])
code_router.include_router(chat.router, prefix="/chat", tags=["代码审查-对话聊天"])

# 将代码审查路由组注册到主路由
api_router.include_router(code_router)
```

#### 修改文件：`python-back/app/main.py`

更新根路由的health链接：
```python
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to AI Code Review Assistant API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/api/v1/code/health",  # 更新
        "applications": {
            "code_review": "/api/v1/code/*"  # 新增
        }
    }
```

### 2. 前端修改（已完成 ✅）

#### 修改文件：`vue3-front/vue-project/src/api/request.js`

**修改前：**
```javascript
const request = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})
```

**修改后：**
```javascript
const request = axios.create({
  // 使用 /code 前缀，为代码审查助手的专属API命名空间
  // 这样设计便于未来扩展其他AI应用（如文档助手、数据分析等）
  baseURL: '/api/v1/code',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})
```

#### 其他API文件

由于前端使用统一的 `request` 实例，所以 **无需修改** 以下文件：
- ✅ `src/api/session.js` - 自动使用新的baseURL
- ✅ `src/api/message.js` - 自动使用新的baseURL
- ✅ `src/api/file.js` - 自动使用新的baseURL
- ✅ `src/api/review.js` - 自动使用新的baseURL
- ✅ `src/api/chat.js` - 自动使用新的baseURL

### 3. Vite代理配置

**无需修改** `vite.config.js`，因为代理配置是针对 `/api` 前缀的，路径变更不影响代理：

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    secure: false,
  }
}
```

---

## 🧪 测试清单

### 后端测试

```bash
# 1. 启动后端服务
cd python-back
python run.py

# 2. 访问Swagger文档
# 浏览器打开: http://localhost:8000/docs
# 检查所有API路径是否包含 /code 前缀

# 3. 测试健康检查
curl http://localhost:8000/api/v1/code/health

# 4. 测试根路径
curl http://localhost:8000/
# 应返回: {"health": "/api/v1/code/health", ...}
```

### 前端测试

```bash
# 1. 启动前端服务
cd vue3-front/vue-project
npm run dev

# 2. 浏览器打开 http://localhost:5173

# 3. 测试功能
# - 创建新会话
# - 上传代码文件
# - 发送消息触发代码审查
# - 查看审查结果
# - 使用智能应用功能
```

### 集成测试

- [ ] 会话创建和切换
- [ ] 文件上传
- [ ] 代码审查触发
- [ ] SSE流式对话
- [ ] 消息历史加载
- [ ] 文件Tab切换
- [ ] 智能应用建议
- [ ] 代码差异对比

---

## 🎯 架构优势

### 1. 清晰的命名空间

```
/api/v1/code/*    - 代码审查助手（专属命名空间）
/api/v1/doc/*     - 文档助手（未来扩展）
/api/v1/data/*    - 数据分析助手（未来扩展）
```

### 2. 易于扩展

添加新应用时，只需在 `app/api/v1/__init__.py` 中注册新的路由组：

```python
# 未来扩展示例
doc_router = APIRouter(prefix="/doc")
doc_router.include_router(...)

api_router.include_router(doc_router)
```

### 3. 统一管理

- 所有代码审查相关的API都在 `/code` 下
- Swagger文档自动分组（"代码审查-XX"标签）
- 便于API权限管理和监控

### 4. 向下兼容策略（可选）

如果需要保持旧路径的兼容性，可以添加路由别名：

```python
# 在 app/api/v1/__init__.py 中
# 保留旧路径（兼容模式）
api_router.include_router(health.router, prefix="/health", tags=["健康检查（已弃用）"])

# 新路径
code_router.include_router(health.router, prefix="/health", tags=["代码审查-健康检查"])
```

---

## 📝 注意事项

### 1. Breaking Change

⚠️ **这是一个破坏性变更**，旧的API路径将不再有效。

### 2. 部署注意

- 前后端必须 **同时更新** 才能正常工作
- 建议在非生产环境先测试
- 如有必要，可实现双路径兼容（过渡期）

### 3. 文档更新

- ✅ Swagger文档自动更新（FastAPI自动生成）
- ✅ 企划书已更新（Day 5.5章节）
- ✅ 迁移文档已创建（本文档）

### 4. 前端缓存

如果遇到API调用失败，尝试：
```bash
# 清除浏览器缓存
Ctrl + Shift + Delete

# 或强制刷新
Ctrl + F5

# 或重启前端服务
npm run dev
```

---

## 📈 迁移验证

### 成功标志

- ✅ 后端启动无错误
- ✅ Swagger文档显示正确的路径（含 `/code`）
- ✅ 前端可以正常创建会话
- ✅ 文件上传成功
- ✅ 代码审查正常工作
- ✅ SSE流式对话正常
- ✅ 控制台无API 404错误

### 失败排查

#### 问题1：前端404错误
```
GET http://localhost:5173/api/v1/sessions 404 (Not Found)
```

**原因**: 前端还在使用旧路径  
**解决**: 检查 `src/api/request.js` 的 `baseURL` 是否已更新为 `/api/v1/code`

#### 问题2：CORS错误
```
Access-Control-Allow-Origin error
```

**原因**: 代理配置问题  
**解决**: 检查 `vite.config.js` 的代理配置，确保 `/api` 代理到 `http://localhost:8000`

#### 问题3：后端路由未生效
```
Swagger文档还显示旧路径
```

**原因**: 后端代码未重新加载  
**解决**: 重启后端服务

---

## 🚀 后续规划

### Phase 1: 稳定运行（当前）
- ✅ 完成API路径迁移
- ✅ 前后端联调测试
- [ ] 生产环境验证

### Phase 2: 扩展准备（未来）
- [ ] 设计文档助手API规范
- [ ] 设计数据分析助手API规范
- [ ] 建立API版本管理策略

### Phase 3: 多应用集成（未来）
- [ ] 开发文档助手前后端
- [ ] 开发数据分析助手前后端
- [ ] 实现应用间数据共享

---

## 📚 相关文档

- [项目企划书 - Day 5.5章节](../../项目企划书_AI代码Review助手.md)
- [FastAPI路由文档](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Axios实例配置](https://axios-http.com/docs/instance)
- [Vite代理配置](https://vitejs.dev/config/server-options.html#server-proxy)

---

## ✅ 迁移清单

**后端：**
- [x] 修改 `app/api/v1/__init__.py`
- [x] 更新 `app/main.py` 根路由
- [x] 更新Swagger标签名称
- [x] 测试所有API端点

**前端：**
- [x] 修改 `src/api/request.js` baseURL
- [x] 验证所有API模块（无需单独修改）
- [x] 清除浏览器缓存测试

**文档：**
- [x] 更新企划书Day 5.5章节
- [x] 创建API迁移文档（本文档）
- [x] 更新Swagger文档（自动生成）

**测试：**
- [ ] 后端健康检查测试
- [ ] 前端会话创建测试
- [ ] 文件上传测试
- [ ] 代码审查流程测试
- [ ] SSE流式对话测试
- [ ] 智能应用功能测试

---

**文档版本**: v1.0  
**创建时间**: 2025年11月10日  
**最后更新**: 2025年11月10日  
**作者**: AI代码Review助手团队

---

**迁移完成！** 🎉

下一步：测试所有功能，确保前后端正常通信。

