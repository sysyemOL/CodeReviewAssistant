# AI代码Review助手 - 项目企划书

## 📋 项目概述

### 项目名称
AI Code Review Assistant（AI代码审查助手）

### 项目背景
随着AI技术的快速发展，将大语言模型应用于代码审查场景，可以大幅提升开发效率和代码质量。本项目旨在开发一个基于LangChain和大语言模型的智能代码审查助手，为开发者提供即时、专业的代码审查建议。

### 项目目标
- **短期目标（5天）**：完成MVP版本，实现Python代码的智能审查功能
- **中期目标**：支持多语言代码审查（JavaScript、Java、Go等）
- **长期目标**：集成到CI/CD流程，提供企业级代码审查解决方案

### 核心价值
1. 即时反馈：上传代码即刻获得审查意见
2. 多维度分析：代码质量、性能、安全性、最佳实践
3. 交互式改进：支持对话式优化和代码修改
4. 学习助手：帮助开发者提升编码能力

---

## 🛠 技术栈选型

### 前端技术栈
| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| Vue 3 | 3.3+ | 前端框架 | 组合式API，性能优秀，生态丰富 |
| Vite | 4.0+ | 构建工具 | 快速开发，HMR体验好 |
| Element Plus | 2.4+ | UI组件库 | 企业级组件，设计专业 |
| Monaco Editor | 0.44+ | 代码编辑器 | VSCode同款，功能强大 |
| Axios | 1.6+ | HTTP客户端 | 易用的请求库 |
| Pinia | 2.1+ | 状态管理 | Vue 3官方推荐 |
| Vue Router | 4.2+ | 路由管理 | 单页应用必备 |

### 后端技术栈
| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| Python | 3.10+ | 开发语言 | AI生态丰富 |
| FastAPI | 0.104+ | Web框架 | 高性能，自动API文档 |
| LangChain | 0.1+ | AI框架 | 强大的LLM编排能力 |
| OpenAI API | - | 大语言模型 | GPT-4性能优秀 |
| Pydantic | 2.5+ | 数据验证 | 类型安全，自动验证 |
| SQLAlchemy | 2.0+ | ORM | 数据持久化 |
| SQLite | 3.0+ | 数据库 | 轻量级，易部署 |
| python-multipart | - | 文件上传 | 处理文件上传 |

### AI相关技术
| 技术 | 用途 |
|------|------|
| LangChain | LLM应用框架，提供Prompt模板、链式调用、记忆管理 |
| OpenAI GPT-4 | 代码理解和审查的核心模型 |
| Tree-sitter | 代码解析器（可选），提供AST分析 |
| Pylint/Flake8 | 静态代码分析工具，辅助LLM审查 |

---

## 📊 功能需求分析

### 功能模块划分

#### 1. 用户界面模块（前端）

**1.1 历史对话区（左侧边栏）**
- 功能需求：
  - 展示历史会话列表
  - 支持会话创建/删除/重命名
  - 会话点击切换
  - 按时间分组显示（今天、昨天、7天内、更早）
  - 搜索历史会话
- 技术实现：
  - 使用虚拟滚动优化长列表
  - LocalStorage + 后端数据库双重存储

**1.2 对话交互区（中间主区域）**
- 功能需求：
  - 消息流展示（用户消息 + AI回复）
  - 支持Markdown渲染
  - 代码块语法高亮
  - 流式输出（打字机效果）
  - 消息操作：复制、重新生成、点赞/踩
- 技术实现：
  - SSE（Server-Sent Events）实现流式输出
  - Marked.js + highlight.js渲染消息

**1.3 输入区域（底部）**
- 功能需求：
  - 文本输入框（支持换行）
  - 文件上传按钮
  - 拖拽上传区域
  - 支持单文件/多文件/文件夹上传
  - 文件类型过滤（.py, .js, .java等）
  - 快捷键支持（Enter发送，Shift+Enter换行）
- 技术实现：
  - HTML5 File API
  - 拖拽事件监听
  - FormData文件上传

**1.4 代码展示/编辑区（右侧）**
- 功能需求：
  - 代码编辑器（Monaco Editor）
  - 语法高亮
  - 代码折叠
  - 行号显示
  - 支持代码修改
  - 代码对比功能（原始版本 vs 修改建议）
  - 一键应用AI建议
  - 文件tab切换（多文件上传时）
- 技术实现：
  - Monaco Editor集成
  - Diff编辑器模式

#### 2. 后端API模块

**2.1 会话管理API**
- `POST /api/sessions` - 创建新会话
- `GET /api/sessions` - 获取会话列表
- `GET /api/sessions/{id}` - 获取会话详情
- `PUT /api/sessions/{id}` - 更新会话
- `DELETE /api/sessions/{id}` - 删除会话

**2.2 代码审查API**
- `POST /api/review/analyze` - 提交代码审查请求
- `POST /api/review/stream` - 流式代码审查（SSE）
- `POST /api/review/chat` - 对话式交互

**2.3 文件处理API**
- `POST /api/files/upload` - 文件上传
- `GET /api/files/{id}` - 获取文件内容
- `POST /api/files/parse` - 解析代码结构

#### 3. AI审查引擎模块

**3.1 代码分析器**
- 静态代码分析（Pylint/Flake8）
- 代码复杂度计算
- 安全漏洞检测
- 代码风格检查

**3.2 LangChain审查链**
- Prompt模板管理
- 审查维度：
  - 代码质量（命名、结构、可读性）
  - 性能优化（算法复杂度、资源使用）
  - 安全性（注入攻击、权限控制）
  - 最佳实践（设计模式、编码规范）
  - Bug风险识别
- 记忆管理（上下文保持）

**3.3 建议生成器**
- 问题优先级排序
- 修改建议生成
- 示例代码生成

---

## 🏗 系统架构设计

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         浏览器端                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ 历史对话 │  │  对话交互区   │  │   代码编辑器区       │  │
│  │   区域   │  │              │  │  (Monaco Editor)    │  │
│  │          │  │  - 消息流    │  │  - 语法高亮         │  │
│  │ - 会话   │  │  - Markdown  │  │  - 代码对比         │  │
│  │ - 搜索   │  │  - 流式输出  │  │  - 修改建议         │  │
│  └──────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            输入区 + 文件上传/拖拽                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Vue 3 + Vite + Element Plus + Monaco Editor + Pinia        │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/SSE
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI 后端服务                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  路由层      │  │  业务逻辑层   │  │   数据访问层    │   │
│  │              │  │              │  │                 │   │
│  │ - 会话管理   │→ │ - 会话服务   │→ │ - SQLAlchemy   │   │
│  │ - 代码审查   │→ │ - 文件服务   │→ │ - SQLite       │   │
│  │ - 文件上传   │→ │ - 审查服务   │→ │ - 文件系统     │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            AI 审查引擎 (LangChain)                    │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐   │   │
│  │  │ 静态分析器 │  │  LLM 链    │  │  建议生成器  │   │   │
│  │  │            │  │            │  │              │   │   │
│  │  │ - Pylint   │→ │ - Prompt   │→ │ - 优先级排序 │   │   │
│  │  │ - Flake8   │  │ - Memory   │  │ - 代码修复   │   │   │
│  │  └────────────┘  └────────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ API Call
┌─────────────────────────────────────────────────────────────┐
│                   OpenAI GPT-4 API                           │
└─────────────────────────────────────────────────────────────┘
```

### 数据流设计

**代码审查流程：**
1. 用户上传代码文件 → 前端
2. 前端发送文件到后端 → `/api/files/upload`
3. 后端保存文件并返回文件ID
4. 前端发起审查请求 → `/api/review/stream`（SSE）
5. 后端执行：
   - 读取代码文件
   - 运行静态分析工具（Pylint）
   - 构建LangChain审查链
   - 调用GPT-4分析代码
   - 流式返回审查结果
6. 前端实时展示审查结果（打字机效果）
7. 用户与AI对话优化代码
8. 前端展示修改建议（Diff模式）

---

## 📁 项目目录结构

### 后端目录结构（python-back/）

```
python-back/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI应用入口
│   ├── config.py                    # 配置文件（环境变量、API密钥）
│   ├── dependencies.py              # 依赖注入
│   │
│   ├── api/                         # API路由层
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── sessions.py          # 会话管理接口
│   │   │   ├── review.py            # 代码审查接口
│   │   │   ├── files.py             # 文件操作接口
│   │   │   └── chat.py              # 对话交互接口
│   │
│   ├── core/                        # 核心模块
│   │   ├── __init__.py
│   │   ├── security.py              # 安全相关（未来扩展）
│   │   └── events.py                # 事件处理（SSE）
│   │
│   ├── services/                    # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── session_service.py       # 会话管理服务
│   │   ├── file_service.py          # 文件处理服务
│   │   ├── review_service.py        # 代码审查服务
│   │   └── ai_service.py            # AI服务封装
│   │
│   ├── ai/                          # AI审查引擎
│   │   ├── __init__.py
│   │   ├── langchain_engine.py      # LangChain引擎
│   │   ├── prompts/                 # Prompt模板
│   │   │   ├── __init__.py
│   │   │   ├── python_review.py     # Python审查模板
│   │   │   └── general_review.py    # 通用审查模板
│   │   ├── analyzers/               # 静态分析器
│   │   │   ├── __init__.py
│   │   │   ├── python_analyzer.py   # Python分析器
│   │   │   └── base_analyzer.py     # 基础分析器
│   │   └── chains/                  # LangChain链
│   │       ├── __init__.py
│   │       ├── review_chain.py      # 审查链
│   │       └── chat_chain.py        # 对话链
│   │
│   ├── models/                      # 数据模型
│   │   ├── __init__.py
│   │   ├── database.py              # 数据库连接
│   │   ├── session.py               # 会话模型
│   │   ├── message.py               # 消息模型
│   │   └── file.py                  # 文件模型
│   │
│   ├── schemas/                     # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── session.py               # 会话schema
│   │   ├── message.py               # 消息schema
│   │   ├── review.py                # 审查结果schema
│   │   └── file.py                  # 文件schema
│   │
│   └── utils/                       # 工具函数
│       ├── __init__.py
│       ├── file_parser.py           # 文件解析工具
│       ├── code_analyzer.py         # 代码分析工具
│       └── logger.py                # 日志工具
│
├── uploads/                         # 上传文件存储
├── data/                            # 数据库文件
│   └── app.db                       # SQLite数据库
├── tests/                           # 测试文件
│   ├── __init__.py
│   ├── test_api.py
│   └── test_services.py
├── requirements.txt                 # Python依赖
├── .env.example                     # 环境变量示例
├── .env                             # 环境变量（不提交）
├── README.md                        # 项目说明
└── run.py                           # 启动脚本
```

### 前端目录结构（vue3-front/vue-project/）

```
vue3-front/vue-project/
├── public/
│   └── favicon.ico
│
├── src/
│   ├── assets/                      # 静态资源
│   │   ├── styles/
│   │   │   ├── common.css           # 公共样式
│   │   │   └── variables.css        # CSS变量
│   │   └── images/
│   │       └── logo.png
│   │
│   ├── components/                  # 公共组件
│   │   ├── common/
│   │   │   ├── CodeEditor.vue       # Monaco代码编辑器组件
│   │   │   ├── CodeDiffViewer.vue   # 代码对比组件
│   │   │   ├── FileUploader.vue     # 文件上传组件
│   │   │   └── MarkdownRenderer.vue # Markdown渲染组件
│   │   │
│   │   ├── chat/
│   │   │   ├── MessageList.vue      # 消息列表
│   │   │   ├── MessageItem.vue      # 消息项
│   │   │   ├── InputBox.vue         # 输入框
│   │   │   └── StreamingText.vue    # 流式文本组件
│   │   │
│   │   └── sidebar/
│   │       ├── SessionList.vue      # 会话列表
│   │       ├── SessionItem.vue      # 会话项
│   │       └── SessionSearch.vue    # 会话搜索
│   │
│   ├── views/                       # 页面视图
│   │   ├── Home.vue                 # 主页
│   │   ├── ReviewWorkspace.vue      # 代码审查工作区（主界面）
│   │   └── About.vue                # 关于页面
│   │
│   ├── layouts/                     # 布局组件
│   │   └── MainLayout.vue           # 主布局（三栏布局）
│   │
│   ├── api/                         # API请求封装
│   │   ├── request.js               # Axios封装
│   │   ├── session.js               # 会话API
│   │   ├── review.js                # 审查API
│   │   ├── file.js                  # 文件API
│   │   └── sse.js                   # SSE处理
│   │
│   ├── stores/                      # Pinia状态管理
│   │   ├── session.js               # 会话状态
│   │   ├── message.js               # 消息状态
│   │   ├── file.js                  # 文件状态
│   │   └── app.js                   # 应用全局状态
│   │
│   ├── router/                      # 路由配置
│   │   └── index.js
│   │
│   ├── utils/                       # 工具函数
│   │   ├── format.js                # 格式化工具
│   │   ├── file.js                  # 文件处理工具
│   │   └── storage.js               # 本地存储工具
│   │
│   ├── composables/                 # 组合式函数
│   │   ├── useChat.js               # 聊天相关逻辑
│   │   ├── useCodeEditor.js         # 编辑器相关逻辑
│   │   └── useFileUpload.js         # 文件上传逻辑
│   │
│   ├── App.vue                      # 根组件
│   └── main.js                      # 入口文件
│
├── index.html
├── package.json
├── vite.config.js
├── .env.development                 # 开发环境变量
├── .env.production                  # 生产环境变量
├── .gitignore
└── README.md
```

---

## 📅 5天实施计划

### Day 1: 环境搭建 + 基础架构

**后端任务：**
- [x] 项目结构初始化
- [ ] 安装依赖（FastAPI, LangChain, SQLAlchemy等）
- [ ] 配置管理（config.py, .env）
- [ ] 数据库模型设计（Session, Message, File）
- [ ] 基础API框架搭建
- [ ] 测试基础接口

**前端任务：**
- [ ] 安装依赖（Element Plus, Monaco Editor等）
- [ ] 配置Vite
- [ ] 创建基础布局组件（三栏布局）
- [ ] 配置路由和状态管理
- [ ] 配置Axios请求封装

**预期产出：**
- 前后端项目框架搭建完成
- 可以运行基础的Hello World接口

---

### Day 2: 核心功能开发 - 会话管理 + 文件上传

**后端任务：**
- [ ] 实现会话管理API（CRUD）
- [ ] 实现文件上传API
- [ ] 文件存储和管理逻辑
- [ ] 数据库操作测试

**前端任务：**
- [ ] 左侧边栏 - 会话列表组件
- [ ] 文件上传组件（拖拽上传）
- [ ] 会话API集成
- [ ] 基础UI样式调整

**预期产出：**
- 可以创建/切换会话
- 可以上传文件

---

### Day 3: AI审查引擎开发

**后端任务：**
- [ ] 集成LangChain
- [ ] 配置OpenAI API
- [ ] 设计Python代码审查Prompt模板
- [ ] 实现静态代码分析（Pylint集成）
- [ ] 实现审查链（review_chain.py）
- [ ] 实现代码审查API（同步版本）

**前端任务：**
- [ ] Monaco Editor集成
- [ ] 代码展示区域实现
- [ ] 消息列表组件
- [ ] 消息渲染（Markdown + 代码高亮）

**预期产出：**
- 上传Python代码后可以获得AI审查结果
- 前端可以展示审查结果

---

### Day 4: 流式输出 + 对话交互

**后端任务：**
- [ ] 实现SSE流式输出
- [ ] 实现流式代码审查API
- [ ] 实现对话API（支持上下文）
- [ ] LangChain记忆管理
- [ ] 优化Prompt模板

**前端任务：**
- [ ] SSE客户端实现
- [ ] 流式文本展示（打字机效果）
- [ ] 输入框组件
- [ ] 对话交互逻辑
- [ ] 消息发送/接收

**预期产出：**
- 流式输出效果
- 可以与AI对话讨论代码

---

### Day 5: 代码编辑 + 优化完善

**后端任务：**
- [ ] 代码修改建议生成
- [ ] 返回格式优化
- [ ] 错误处理完善
- [ ] API文档补充
- [ ] 性能优化

**前端任务：**
- [ ] 代码Diff对比功能
- [ ] 一键应用建议功能
- [ ] 多文件Tab切换
- [ ] UI/UX优化
- [ ] 错误提示优化
- [ ] 响应式适配

**预期产出：**
- 完整的MVP demo
- 基本的用户体验
- 可演示的功能流程

---

## 🔧 技术可行性分析

### 1. LangChain + GPT-4 代码审查

**可行性：高 ✅**

**理由：**
- LangChain提供了完善的LLM应用框架
- GPT-4对代码理解能力强，可以识别复杂的代码问题
- 已有大量成功案例（GitHub Copilot, Amazon CodeWhisperer）

**实现要点：**
```python
# 示例：LangChain审查链伪代码
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# 1. 定义Prompt模板
review_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位资深的Python代码审查专家..."),
    ("user", "请审查以下代码：\n{code}\n\n静态分析结果：\n{static_analysis}")
])

# 2. 创建LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 3. 创建审查链
review_chain = LLMChain(llm=llm, prompt=review_prompt)

# 4. 执行审查
result = review_chain.run(code=code_content, static_analysis=pylint_result)
```

**风险点：**
- OpenAI API成本（建议初期使用GPT-3.5降低成本）
- API调用速度（网络延迟）
- Token限制（大文件需分块处理）

**解决方案：**
- 提供API key配置选项
- 实现请求缓存机制
- 大文件自动分割策略

---

### 2. Monaco Editor集成

**可行性：高 ✅**

**理由：**
- Monaco Editor是VSCode底层编辑器，功能强大
- Vue 3有成熟的集成方案
- 支持Diff模式，完美契合需求

**实现要点：**
```bash
npm install monaco-editor
npm install @monaco-editor/loader
```

```vue
<!-- CodeEditor.vue 示例 -->
<template>
  <div ref="editorContainer" class="editor-container"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as monaco from 'monaco-editor'

const editorContainer = ref(null)
let editor = null

onMounted(() => {
  editor = monaco.editor.create(editorContainer.value, {
    value: props.code,
    language: 'python',
    theme: 'vs-dark',
    automaticLayout: true
  })
})
</script>
```

---

### 3. SSE流式输出

**可行性：高 ✅**

**理由：**
- FastAPI原生支持SSE
- 现代浏览器都支持EventSource
- 实现简单，效果好

**实现要点：**

后端（FastAPI）：
```python
from fastapi.responses import StreamingResponse
import asyncio

async def review_stream(code: str):
    async for chunk in llm.astream(code):
        yield f"data: {chunk}\n\n"
        await asyncio.sleep(0.01)

@app.post("/api/review/stream")
async def stream_review(request: ReviewRequest):
    return StreamingResponse(
        review_stream(request.code),
        media_type="text/event-stream"
    )
```

前端（Vue 3）：
```javascript
const eventSource = new EventSource('/api/review/stream')
eventSource.onmessage = (event) => {
  messageContent.value += event.data
}
```

---

### 4. 文件上传和拖拽

**可行性：高 ✅**

**理由：**
- HTML5 File API成熟
- FastAPI支持multipart/form-data
- 实现简单

**实现要点：**
```vue
<template>
  <div 
    @drop.prevent="handleDrop"
    @dragover.prevent
  >
    <input type="file" @change="handleFileSelect" multiple>
  </div>
</template>

<script setup>
const handleDrop = (e) => {
  const files = Array.from(e.dataTransfer.files)
  uploadFiles(files)
}
</script>
```

---

### 5. 静态代码分析集成

**可行性：高 ✅**

**理由：**
- Pylint/Flake8是成熟的Python分析工具
- 可通过subprocess调用
- 结果易于解析

**实现要点：**
```python
import subprocess
import json

def analyze_python_code(file_path: str):
    # 运行Pylint
    result = subprocess.run(
        ['pylint', file_path, '--output-format=json'],
        capture_output=True,
        text=True
    )
    issues = json.loads(result.stdout)
    return issues
```

---

## 💡 核心功能Prompt设计

### Python代码审查Prompt模板

```python
PYTHON_REVIEW_PROMPT = """
你是一位资深的Python代码审查专家，拥有10年以上的开发经验。
请对以下代码进行全面审查，从以下维度进行分析：

**审查维度：**
1. **代码质量**
   - 命名规范（变量、函数、类名是否符合PEP 8）
   - 代码可读性
   - 代码结构和组织

2. **性能优化**
   - 算法时间复杂度
   - 不必要的循环或计算
   - 资源使用效率

3. **安全性**
   - 潜在的安全漏洞
   - 输入验证
   - 敏感信息处理

4. **最佳实践**
   - 是否遵循Python最佳实践
   - 设计模式应用
   - 代码复用性

5. **Bug风险**
   - 潜在的运行时错误
   - 边界条件处理
   - 异常处理

**代码内容：**
```python
{code}
```

**静态分析结果：**
{static_analysis}

**审查要求：**
1. 按严重程度排序（严重、警告、建议）
2. 对每个问题提供：
   - 问题描述
   - 所在行号
   - 影响分析
   - 具体修改建议
   - 示例代码（如适用）
3. 总结整体代码质量评分（1-10分）
4. 提供3-5条优化建议

请以Markdown格式输出，使用代码块展示示例。
"""
```

---

## 📊 数据库设计

### 表结构设计

#### 1. sessions表（会话表）
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(36) UNIQUE NOT NULL,  -- UUID
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT 0
);
```

#### 2. messages表（消息表）
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id VARCHAR(36) UNIQUE NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

#### 3. files表（文件表）
```sql
CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id VARCHAR(36) UNIQUE NOT NULL,
    session_id VARCHAR(36),
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    language VARCHAR(50),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

#### 4. review_results表（审查结果表）
```sql
CREATE TABLE review_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_id VARCHAR(36) UNIQUE NOT NULL,
    file_id VARCHAR(36) NOT NULL,
    severity VARCHAR(20),  -- 'critical', 'warning', 'info'
    issue_type VARCHAR(50),
    line_number INTEGER,
    description TEXT,
    suggestion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);
```

---

## 🎨 UI设计参考

### 布局设计（仿豆包）

```
┌─────────────────────────────────────────────────────────────────┐
│  🤖 AI Code Review Assistant                          [用户] ⚙  │
├──────────┬──────────────────────────────┬───────────────────────┤
│          │                              │                       │
│ 📝 历史  │    💬 对话交互区              │   📄 代码编辑器        │
│  会话    │                              │                       │
│          │  ┌────────────────────────┐  │  ┌─────────────────┐ │
│ 🔍[搜索] │  │ 👤 User:               │  │  │ 📁 main.py  ✕   │ │
│          │  │ 请审查这段代码         │  │  ├─────────────────┤ │
│ 今天     │  │                        │  │  │  1 def calc(): │ │
│ • 审查   │  └────────────────────────┘  │  │  2   return x  │ │
│   main.py│                              │  │  3             │ │
│          │  ┌────────────────────────┐  │  │                 │ │
│ 昨天     │  │ 🤖 Assistant:          │  │  │ [原始] [修改]   │ │
│ • 代码   │  │ 我发现以下问题：       │  │  │                 │ │
│   优化   │  │ 1. 变量x未定义 ⚠️     │  │  │ [应用建议]      │ │
│          │  │ 2. ...                 │  │  └─────────────────┘ │
│ 7天内    │  └────────────────────────┘  │                       │
│ • ...    │                              │                       │
│          │                              │                       │
├──────────┤  ┌────────────────────────┐  │                       │
│          │  │ 💬 输入消息...         │  │                       │
│ [+新会话]│  │ 📎 [上传] [拖拽区域]   │  │                       │
│          │  └────────────────────────┘  │                       │
└──────────┴──────────────────────────────┴───────────────────────┘
```

### 颜色方案（参考）

```css
:root {
  /* 主色调 */
  --primary-color: #6366f1;        /* 靛蓝 */
  --primary-hover: #4f46e5;
  
  /* 背景色 */
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  
  /* 文字颜色 */
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-tertiary: #9ca3af;
  
  /* 边框颜色 */
  --border-color: #e5e7eb;
  
  /* 代码编辑器 */
  --editor-bg: #1e1e1e;
  
  /* 消息气泡 */
  --user-message-bg: #6366f1;
  --ai-message-bg: #f3f4f6;
}
```

---

## 🚀 部署方案

### 开发环境

**后端启动：**
```bash
cd python-back
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**前端启动：**
```bash
cd vue3-front/vue-project
npm install
npm run dev
```

### 生产环境（未来扩展）

- 后端：Docker + Gunicorn + Nginx
- 前端：静态文件部署（Vercel/Netlify）
- 数据库：PostgreSQL（替代SQLite）
- 缓存：Redis
- 监控：Prometheus + Grafana

---

## 📝 依赖清单

### 后端依赖（requirements.txt）

```txt
# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0

# AI相关
langchain==0.1.0
langchain-openai==0.0.2
openai==1.6.0

# 数据库
sqlalchemy==2.0.23
alembic==1.13.0

# 静态代码分析
pylint==3.0.3
flake8==7.0.0
radon==6.0.1  # 复杂度分析

# 工具
python-dotenv==1.0.0
aiofiles==23.2.1
```

### 前端依赖（package.json）

```json
{
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "element-plus": "^2.4.4",
    "@element-plus/icons-vue": "^2.3.1",
    "monaco-editor": "^0.44.0",
    "@monaco-editor/loader": "^1.4.0",
    "axios": "^1.6.2",
    "marked": "^11.0.0",
    "highlight.js": "^11.9.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.7"
  }
}
```

---

## ⚠️ 风险与挑战

### 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| OpenAI API不稳定 | 高 | 添加重试机制，提供降级方案（GPT-3.5） |
| Token超限 | 中 | 实现代码分块策略，限制单次上传文件大小 |
| SSE连接中断 | 中 | 前端自动重连机制 |
| 大文件处理慢 | 低 | 异步处理 + 进度提示 |

### 进度风险

| 风险 | 概率 | 应对措施 |
|------|------|----------|
| 5天时间不足 | 中 | 采用敏捷开发，优先核心功能 |
| 依赖安装问题 | 低 | 提前准备Docker镜像 |
| UI开发耗时 | 中 | 使用Element Plus减少自定义组件 |

---

## 📈 未来扩展方向

### 短期（1-2周）
- [ ] 支持更多语言（JavaScript, Java, Go）
- [ ] 代码质量评分可视化
- [ ] 导出审查报告（PDF/Markdown）
- [ ] 用户设置（主题、字体大小）

### 中期（1-2月）
- [ ] 多人协作审查
- [ ] 审查历史对比
- [ ] 自定义审查规则
- [ ] 集成Git（从仓库拉取代码）
- [ ] 团队审查标准管理

### 长期（3-6月）
- [ ] CI/CD集成（GitHub Actions, GitLab CI）
- [ ] 企业版（私有化部署）
- [ ] 审查知识库（常见问题检索）
- [ ] 代码质量趋势分析
- [ ] AI训练微调（基于团队代码风格）

---

## 💰 成本估算

### 开发成本（5天MVP）
- 人力成本：1名全栈开发 × 5天
- OpenAI API测试费用：约$10-20（使用GPT-3.5）

### 运营成本（月）
- OpenAI API：$50-500（取决于使用量）
- 服务器：$5-20/月（VPS）
- 域名：$10/年

---

## ✅ 验收标准

### MVP版本必须实现的功能：

1. ✅ 用户可以创建/切换会话
2. ✅ 用户可以上传Python文件（拖拽或点击）
3. ✅ 系统自动进行代码审查并流式输出结果
4. ✅ 右侧Monaco编辑器展示代码
5. ✅ 用户可以与AI对话讨论代码
6. ✅ 历史消息持久化存储
7. ✅ 基本的UI/UX（参考豆包风格）
8. ✅ 错误处理和用户提示

### 性能要求：
- 代码审查响应时间 < 5秒（首字节）
- 文件上传 < 2秒（10MB以下）
- 界面加载 < 1秒

---

## 📞 项目联系

- 项目负责人：[待定]
- 技术负责人：[待定]
- 预期开始时间：立即
- 预期完成时间：5个工作日

---

## 📚 参考资料

1. [LangChain官方文档](https://python.langchain.com/)
2. [FastAPI文档](https://fastapi.tiangolo.com/)
3. [Vue 3官方文档](https://vuejs.org/)
4. [Monaco Editor文档](https://microsoft.github.io/monaco-editor/)
5. [OpenAI API文档](https://platform.openai.com/docs/)
6. [Element Plus组件库](https://element-plus.org/)

---

## 附录

### A. 环境变量配置示例（.env）

```env
# OpenAI配置
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=2000

# 数据库配置
DATABASE_URL=sqlite:///./data/app.db

# 文件上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# 应用配置
APP_ENV=development
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173

# API配置
API_V1_PREFIX=/api/v1
```

### B. 快速启动脚本（run.py）

```python
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "False") == "True"
    )
```

---

**文档版本：** v1.0  
**最后更新：** 2025-11-07  
**状态：** 待审批

---

*本企划书为AI代码Review助手项目的初步规划，具体实施过程中可能根据实际情况进行调整。*

