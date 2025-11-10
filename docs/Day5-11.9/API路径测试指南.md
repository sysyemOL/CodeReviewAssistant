# API路径变更测试指南

## 🧪 快速测试步骤

### 第1步：启动后端服务

```bash
# 在项目根目录
cd python-back
E:/anaconda/envs/langchain/python.exe run.py
```

**预期输出：**
```
🚀 Starting AI Code Review Assistant v1.0.0
📚 API文档: http://localhost:8000/docs
✅ 数据库初始化成功
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000
```

### 第2步：验证Swagger文档

1. 浏览器打开：`http://localhost:8000/docs`
2. 检查所有API路径是否包含 `/code` 前缀
3. 确认API标签显示为"代码审查-XX"

**预期看到的API路径：**
- `GET /api/v1/code/health`
- `GET /api/v1/code/sessions`
- `POST /api/v1/code/files/upload`
- `POST /api/v1/code/review`
- `POST /api/v1/code/chat/stream`

### 第3步：测试健康检查

```bash
# 方法1：使用curl
curl http://localhost:8000/api/v1/code/health

# 方法2：浏览器访问
# 打开: http://localhost:8000/api/v1/code/health

# 预期返回：
# {"status": "ok", "timestamp": "..."}
```

### 第4步：测试根路径

```bash
curl http://localhost:8000/

# 预期返回：
# {
#   "message": "Welcome to AI Code Review Assistant API",
#   "version": "1.0.0",
#   "docs": "/docs",
#   "health": "/api/v1/code/health",
#   "applications": {
#     "code_review": "/api/v1/code/*"
#   }
# }
```

### 第5步：启动前端服务

```bash
# 新开一个终端窗口
cd vue3-front/vue-project
npm run dev
```

**预期输出：**
```
VITE v7.1.11  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### 第6步：测试前端集成

1. 浏览器打开：`http://localhost:5173`
2. 打开浏览器开发者工具（F12）
3. 切换到"Network"标签

#### 测试清单

- [ ] **创建会话**
  - 点击"新建会话"
  - Network中应看到：`POST http://localhost:5173/api/v1/code/sessions`
  - 返回状态：200 OK

- [ ] **上传文件**
  - 上传一个Python文件
  - Network中应看到：`POST http://localhost:5173/api/v1/code/files/upload`
  - 返回状态：200 OK

- [ ] **触发代码审查**
  - 发送消息："请审查这段代码"
  - Network中应看到：`POST http://localhost:5173/api/v1/code/chat/stream`
  - 应该有SSE流式响应

- [ ] **查看会话列表**
  - 刷新页面
  - Network中应看到：`GET http://localhost:5173/api/v1/code/sessions`
  - 返回状态：200 OK

### 第7步：检查控制台错误

打开浏览器控制台（F12 → Console），确认：
- ✅ 无404错误
- ✅ 无CORS错误
- ✅ 无网络错误

---

## 🐛 常见问题排查

### 问题1：404 Not Found

**现象：**
```
GET http://localhost:5173/api/v1/sessions 404 (Not Found)
```

**原因：** 前端还在使用旧路径

**解决方案：**
1. 检查 `src/api/request.js` 的 `baseURL`
2. 应该是 `/api/v1/code`，而不是 `/api/v1`
3. 强制刷新浏览器：`Ctrl + F5`
4. 或清除缓存后重新加载

### 问题2：CORS错误

**现象：**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/v1/code/sessions' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**原因：** 后端CORS配置问题或代理配置问题

**解决方案：**
1. 确认后端 `app/core/config.py` 的 `BACKEND_CORS_ORIGINS` 包含 `http://localhost:5173`
2. 确认 `vite.config.js` 的代理配置正确
3. 重启前后端服务

### 问题3：连接超时

**现象：**
```
timeout of 30000ms exceeded
```

**原因：** 后端服务未启动或端口不对

**解决方案：**
1. 确认后端服务正在运行
2. 访问 `http://localhost:8000/docs` 验证
3. 检查端口8000是否被占用

### 问题4：前端显示旧API路径

**现象：** Network标签显示的还是 `/api/v1/sessions`

**原因：** 浏览器缓存

**解决方案：**
```bash
# 1. 停止前端服务 (Ctrl+C)

# 2. 清除浏览器缓存
#    Chrome: Ctrl + Shift + Delete

# 3. 重新启动前端
npm run dev

# 4. 硬刷新页面
#    Ctrl + F5
```

---

## ✅ 成功标志

如果以下所有检查都通过，说明API路径迁移成功：

**后端：**
- ✅ 后端启动无错误
- ✅ Swagger文档路径包含 `/code`
- ✅ 访问 `http://localhost:8000/api/v1/code/health` 返回200

**前端：**
- ✅ 前端启动无错误
- ✅ 页面加载正常
- ✅ 控制台无404错误

**集成：**
- ✅ 会话创建成功
- ✅ 文件上传成功
- ✅ 代码审查正常工作
- ✅ SSE流式对话正常
- ✅ Network中所有API路径包含 `/code`

---

## 📊 快速检查表

复制到终端执行，快速验证所有API：

```bash
# 后端API测试脚本
echo "Testing Code Review Assistant API..."
echo ""

echo "1. Root endpoint:"
curl -s http://localhost:8000/ | jq

echo ""
echo "2. Health check:"
curl -s http://localhost:8000/api/v1/code/health | jq

echo ""
echo "3. Sessions endpoint (should return empty list initially):"
curl -s http://localhost:8000/api/v1/code/sessions | jq

echo ""
echo "All API paths should contain '/code' prefix!"
```

**注意：** 需要安装 `jq` 工具来格式化JSON输出：
```bash
# Windows (使用Chocolatey)
choco install jq

# 或者不使用jq，直接查看原始JSON
curl http://localhost:8000/api/v1/code/health
```

---

## 🎯 性能测试（可选）

如果想测试API性能，可以使用以下工具：

### 使用Apache Bench (ab)

```bash
# 测试健康检查端点
ab -n 1000 -c 10 http://localhost:8000/api/v1/code/health

# 参数说明：
# -n 1000：总共发送1000个请求
# -c 10：并发10个请求
```

### 使用wrk

```bash
# 测试健康检查端点（持续10秒）
wrk -t4 -c100 -d10s http://localhost:8000/api/v1/code/health

# 参数说明：
# -t4：使用4个线程
# -c100：保持100个HTTP连接
# -d10s：持续10秒
```

---

## 📝 测试报告模板

测试完成后，可以记录以下信息：

```markdown
## API路径迁移测试报告

**测试日期**: 2025-11-10
**测试人员**: [你的名字]

### 后端测试
- [ ] 后端启动成功
- [ ] Swagger文档正确显示
- [ ] 健康检查API正常
- [ ] 所有API路径包含 /code 前缀

### 前端测试
- [ ] 前端启动成功
- [ ] 页面加载正常
- [ ] 无控制台错误
- [ ] 所有API调用使用新路径

### 集成测试
- [ ] 会话创建
- [ ] 文件上传
- [ ] 代码审查
- [ ] 流式对话
- [ ] 消息持久化

### 性能测试
- 健康检查QPS: ____ req/s
- 平均响应时间: ____ ms
- 错误率: ____%

### 问题记录
1. [如有问题，记录在此]

### 结论
- [ ] 测试通过，可以发布
- [ ] 测试失败，需要修复：[问题列表]
```

---

**测试指南版本**: v1.0  
**创建时间**: 2025年11月10日

