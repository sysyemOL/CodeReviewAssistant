# Day 4 流式对话使用示例

## 🚀 启动项目

### 后端启动
```bash
cd python-back
python run.py
# 或
uvicorn app.main:app --reload --host localhost --port 8000
```

### 前端启动
```bash
cd vue3-front/vue-project
npm run dev
```

---

## 💬 使用流程

### 1. 创建新对话
1. 点击左侧"新对话"按钮
2. 自动创建新会话并切换

### 2. 发送文本消息
1. 在底部输入框输入问题
   - 例如："请帮我审查这段代码"
   - 例如:"这个函数有什么性能问题？"
2. 按 `Enter` 发送（`Shift + Enter` 换行）
3. 观察 AI 流式响应，实时显示内容

### 3. 上传文件进行审查
1. 点击"上传文件"按钮选择代码文件
2. 或者直接拖拽文件到输入区域
3. 支持的文件类型：`.py, .js, .ts, .java, .go, .cpp, .vue` 等
4. 输入问题（可选）
5. 发送消息，AI 会自动分析代码

### 4. 查看审查结果
- 代码会在右侧编辑器中显示
- 审查结果在中间对话区以 Markdown 格式展示
- 支持代码高亮、表格、列表等格式

---

## 📝 示例对话

### 示例 1：代码质量审查
```
用户：请审查这段 Python 代码的质量

AI：[流式输出]
## 📊 代码审查报告

### 🔍 自动化分析结果

**Pylint 分析**:
发现 3 个问题：
- Line 5: [CONVENTION] Missing function docstring
- Line 12: [WARNING] Unused variable 'x'
...

### 📈 总体评分
代码质量: 7/10 分

### ✅ 优点
- 代码结构清晰
- 变量命名规范
...
```

### 示例 2：安全检查
```
用户：这段代码有安全问题吗？

AI：[流式输出]
## 🔒 安全检查发现以下问题：
- 🔴 发现 eval() 使用，存在代码注入风险
- 🟡 可能存在硬编码密码
...
```

### 示例 3：性能优化
```
用户：如何优化这个算法的性能？

AI：[流式输出]
## ⚡ 性能优化建议

### 当前问题
- 时间复杂度：O(n²)
- 存在重复计算
...

### 优化方案
使用哈希表优化查找...
```

---

## 🎯 高级用法

### 多轮对话
```
用户1：请审查这段代码
AI1：[审查结果...]

用户2：第12行的问题具体怎么修复？
AI2：[针对性解答，保持上下文...]
```

### 多文件审查
1. 上传多个文件（拖拽或选择）
2. 发送消息
3. AI 会逐个审查并给出综合建议

### 自定义问题
- "这个函数的时间复杂度是多少？"
- "如何重构这段代码？"
- "有没有更好的设计模式？"
- "哪些部分需要添加单元测试？"

---

## 🛠️ API 测试

### 使用 curl 测试流式 API
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -N \
  -d '{
    "session_id": "session_test123",
    "message": "Hello, AI!",
    "file_ids": null
  }'
```

### 预期输出
```
data: {"type":"user_message","message_id":"msg_xxx","content":"Hello, AI!"}

data: {"type":"start","message_id":"msg_yyy"}

data: {"type":"content","delta":"你好"}

data: {"type":"content","delta":"！我"}

data: {"type":"content","delta":"是"}

...

data: {"type":"done","message_id":"msg_yyy"}
```

### 使用 JavaScript 测试
```javascript
import { sendMessageStream } from '@/api/chat'

const client = sendMessageStream(
  {
    session_id: 'session_test123',
    message: 'Hello, AI!',
    file_ids: null
  },
  {
    onStart: (data) => console.log('开始:', data),
    onContent: (data) => console.log('内容:', data.delta),
    onDone: (data) => console.log('完成:', data),
    onError: (data) => console.error('错误:', data)
  }
)
```

---

## 🐛 故障排除

### 问题 1: 流式输出不显示
**可能原因**: 后端未启动或 API 地址错误

**解决方案**:
1. 检查后端是否运行: `http://localhost:8000/docs`
2. 检查 `.env` 中的 `VITE_API_BASE_URL`
3. 查看浏览器控制台错误信息

### 问题 2: OpenAI API 错误
**可能原因**: API Key 未配置或无效

**解决方案**:
1. 检查 `python-back/.env` 中的 `OPENAI_API_KEY`
2. 确认 API Key 有效且有额度
3. 查看后端日志

### 问题 3: 文件上传失败
**可能原因**: 文件类型不支持或大小超限

**解决方案**:
1. 检查文件类型是否在支持列表中
2. 确认文件大小 < 10MB
3. 查看错误提示信息

### 问题 4: 流式响应中断
**可能原因**: 网络不稳定或超时

**解决方案**:
1. 刷新页面重试
2. 检查网络连接
3. 查看后端是否有错误日志

---

## 📊 性能提示

### 优化建议
1. **小文件优先**: 单文件 < 500 行效果最佳
2. **清晰问题**: 具体的问题能获得更准确的回答
3. **分步询问**: 复杂问题分多轮对话
4. **网络环境**: 稳定的网络连接保证流式体验

### 响应时间
- 纯文本消息: 1-3 秒开始响应
- 小文件审查 (<200行): 3-8 秒
- 中等文件 (200-500行): 8-15 秒
- 大文件 (>500行): 15-30 秒

---

## 🎨 UI 提示

### 消息状态
- **用户消息**: 白色背景
- **AI 消息**: 浅灰背景
- **流式消息**: 右下角闪烁光标 ▋
- **加载中**: "正在思考中..." 提示

### 代码显示
- 语法高亮
- 行号显示
- 主题切换（纯白/毛玻璃/深色）
- 自定义背景图片

---

## 🎉 开始使用

1. 启动后端和前端
2. 打开浏览器访问 `http://localhost:5173`
3. 创建新对话
4. 上传代码文件或直接提问
5. 享受 AI 助手的实时响应！

---

**祝你使用愉快！** 🚀

