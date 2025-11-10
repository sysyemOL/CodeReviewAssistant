# 🤖 AI Code Review Assistant

<div align="center">

**基于 LangChain 和 GPT-4 的智能代码审查助手**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.0-green.svg)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue-3.5.22-brightgreen.svg)](https://vuejs.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1.0.0-orange.svg)](https://python.langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [架构说明](#-架构说明) • [API 文档](#-api-文档) • [贡献指南](#-贡献指南)

</div>

---

## 📖 项目简介

AI Code Review Assistant 是一个基于大语言模型（LLM）的智能代码审查助手，旨在为开发者提供即时、专业、多维度的代码审查服务。通过结合静态代码分析和 AI 智能审查，帮助开发者提升代码质量、发现潜在问题、学习最佳实践。

### 🎯 核心价值

- **💡 即时反馈**：上传代码即刻获得审查意见，无需等待人工审查
- **📊 多维度分析**：代码质量、性能优化、安全性、最佳实践全方位评估
- **🔄 交互式改进**：支持对话式优化和实时代码修改建议
- **📚 学习助手**：通过 AI 解释和示例代码帮助开发者提升编码能力

---

## ✨ 功能特性

### 🔍 智能代码审查
- **多维度分析**：代码质量、性能、安全性、可维护性全方位评估
- **静态分析集成**：结合 Pylint、Flake8 等工具提供量化指标
- **优先级排序**：智能识别关键问题，按优先级给出修改建议
- **实时预览**：Monaco Editor 提供代码对比和修改建议可视化

### 💬 对话式交互
- **上下文理解**：基于 LangChain 的记忆机制保持对话连贯性
- **追问优化**：支持针对特定问题深入讨论和优化
- **流式输出**：打字机效果实时展示 AI 回复，提升交互体验
- **Markdown 渲染**：美观的消息格式和代码高亮

### 📝 会话管理
- **历史记录**：自动保存所有审查会话，支持随时回溯
- **智能分组**：按时间自动分类（今天、昨天、7天内、更早）
- **快速搜索**：支持会话标题和内容搜索
- **批量操作**：支持会话导出、删除、重命名

### 🛠️ 代码编辑器
- **Monaco Editor**：VSCode 同款编辑器，功能强大
- **语法高亮**：支持多种编程语言
- **代码对比**：原始代码 vs AI 建议并排展示
- **智能应用**：一键应用 AI 的结构化修改指令
- **实时验证**：修改后即时验证代码语法

### 🎨 现代化 UI/UX
- **响应式设计**：完美适配桌面和移动设备
- **暗色主题**：护眼的暗色模式，支持主题切换
- **流畅动画**：细腻的交互反馈和过渡效果
- **拖拽上传**：支持文件拖拽上传，操作便捷

---

## 🛠 技术栈

### 前端技术栈
```
Vue 3 (3.5.22)           - 前端框架，组合式 API
Vite (7.1.11)            - 构建工具，快速 HMR
Element Plus (2.4.4)     - UI 组件库
Monaco Editor (0.44.0)   - 代码编辑器（VSCode 内核）
Pinia (2.1.7)            - 状态管理
Vue Router (4.2.5)       - 路由管理
Axios (1.6.2)            - HTTP 客户端
Marked (11.0.0)          - Markdown 渲染
Highlight.js (11.9.0)    - 代码高亮
```

### 后端技术栈
```
Python (3.11+)           - 开发语言
FastAPI (0.121.0)        - Web 框架
Uvicorn (0.38.0)         - ASGI 服务器
LangChain (1.0.0)        - LLM 应用框架
OpenAI (1.108.0)         - GPT-4 API 客户端
SQLAlchemy (2.0.43)      - ORM 框架
Pydantic (2.12.4)        - 数据验证
Pylint (4.0.2)           - 代码质量分析
Flake8 (7.3.0)           - 代码风格检查
```

---

## 🚀 快速开始

### 前置要求

- **Python**: 3.11 或更高版本
- **Node.js**: 20.19.0 或更高版本
- **OpenAI API Key**: 需要有效的 OpenAI API 密钥

### 1. 克隆项目

```bash
git clone https://github.com/sysyemOL/CodeReviewAssistant.git
cd CodeReviewAssistant
```

### 2. 后端配置

#### 2.1 创建 Python 虚拟环境

```bash
# 使用 conda（推荐）
conda create -n langchain python=3.11
conda activate langchain

# 或使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### 2.2 安装依赖

```bash
cd python-back
pip install -r requirements.txt
```

#### 2.3 配置环境变量

在 `python-back` 目录创建 `.env` 文件：

```env
# OpenAI 配置
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
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

# API 配置
API_V1_PREFIX=/api/v1
```

#### 2.4 启动后端服务

```bash
python run.py
```

后端服务将在 `http://127.0.0.1:8000` 运行

### 3. 前端配置

#### 3.1 安装依赖

```bash
cd vue3-front/vue-project
npm install
```

#### 3.2 启动前端开发服务器

```bash
npm run dev
```

前端服务将在 `http://localhost:5173` 运行

### 4. 访问应用

打开浏览器访问：
- **应用地址**: http://localhost:5173
- **API 文档**: http://127.0.0.1:8000/docs
- **API 健康检查**: http://127.0.0.1:8000/api/v1/code/health

---

## 🏗 架构说明

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                         浏览器端                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ 历史对话 │  │  对话交互区   │  │   代码编辑器区       │  │
│  │   区域   │  │              │  │  (Monaco Editor)    │  │
│  │          │  │  - 消息流    │  │  - 语法高亮         │  │
│  │ - 会话   │  │  - Markdown  │  │  - 代码对比         │  │
│  │ - 搜索   │  │  - 流式输出  │  │  - 智能应用         │  │
│  └──────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            输入区 + 文件上传/拖拽                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Vue 3 + Vite + Element Plus + Monaco Editor + Pinia        │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/SSE
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI 后端服务                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │  路由层     │  │  服务层       │  │  数据访问层     │    │
│  │             │  │              │  │                 │    │
│  │ - Sessions  │→ │ - Review     │→ │ - SQLAlchemy   │    │
│  │ - Messages  │  │ - Chat       │  │ - Models       │    │
│  │ - Files     │  │ - Analysis   │  │ - CRUD         │    │
│  │ - Review    │  │              │  │                 │    │
│  └─────────────┘  └──────────────┘  └─────────────────┘    │
│                           ↕                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              AI 审查引擎 (LangChain)                 │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │    │
│  │  │ 静态分析     │  │  LLM审查链   │  │ 建议生成 │  │    │
│  │  │ - Pylint    │→ │  - Prompt    │→ │ - 优先级 │  │    │
│  │  │ - Flake8    │  │  - Memory    │  │ - 示例   │  │    │
│  │  │ - 复杂度    │  │  - Chain     │  │ - 格式化 │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ↕                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 SQLite 数据库                        │    │
│  │  - sessions (会话)                                   │    │
│  │  - messages (消息)                                   │    │
│  │  - files (文件)                                      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      OpenAI GPT-4 API                        │
└─────────────────────────────────────────────────────────────┘
```

### 后端分层架构

```
python-back/
├── app/
│   ├── main.py                    # 应用入口
│   ├── api/                       # API 路由层
│   │   └── v1/
│   │       ├── __init__.py        # 路由注册（/api/v1/code 前缀）
│   │       ├── sessions.py        # 会话管理 API
│   │       ├── messages.py        # 消息管理 API
│   │       ├── files.py           # 文件管理 API
│   │       ├── review.py          # 代码审查 API
│   │       └── chat.py            # 对话交互 API
│   ├── services/                  # 业务逻辑层
│   │   ├── review_service.py     # 审查服务
│   │   ├── review_chain.py       # LangChain 审查链
│   │   ├── code_analyzer.py      # 代码分析器
│   │   └── file_service.py       # 文件处理服务
│   ├── models/                    # 数据模型层
│   │   ├── session.py            # 会话模型
│   │   ├── message.py            # 消息模型
│   │   └── file.py               # 文件模型
│   ├── schemas/                   # Pydantic 模式
│   │   ├── session.py            # 会话模式
│   │   ├── message.py            # 消息模式
│   │   └── file.py               # 文件模式
│   ├── core/                      # 核心配置
│   │   ├── config.py             # 环境配置
│   │   └── database.py           # 数据库配置
│   └── utils/                     # 工具函数
│       ├── file_utils.py         # 文件工具
│       └── error_handler.py      # 错误处理
└── run.py                         # 启动脚本
```

### 前端架构

```
vue3-front/vue-project/
├── src/
│   ├── App.vue                    # 根组件
│   ├── main.js                    # 应用入口
│   ├── router/                    # 路由配置
│   │   └── index.js
│   ├── stores/                    # Pinia 状态管理
│   │   ├── session.js            # 会话状态
│   │   ├── message.js            # 消息状态
│   │   └── file.js               # 文件状态
│   ├── api/                       # API 封装
│   │   ├── request.js            # Axios 实例
│   │   ├── session.js            # 会话 API
│   │   ├── message.js            # 消息 API
│   │   ├── file.js               # 文件 API
│   │   └── review.js             # 审查 API
│   ├── components/                # 组件
│   │   ├── common/               # 通用组件
│   │   │   ├── MonacoDiffEditor.vue  # 代码对比编辑器
│   │   │   └── CodeHighlight.vue     # 代码高亮
│   │   ├── chat/                 # 聊天组件
│   │   │   ├── MessageList.vue   # 消息列表
│   │   │   ├── MessageItem.vue   # 消息项
│   │   │   └── InputArea.vue     # 输入区
│   │   └── session/              # 会话组件
│   │       ├── SessionList.vue   # 会话列表
│   │       └── SessionItem.vue   # 会话项
│   ├── views/                     # 页面视图
│   │   ├── PortalView.vue        # 门户页面
│   │   └── ReviewWorkspace.vue   # 审查工作区
│   └── utils/                     # 工具函数
│       ├── codeModifier.js       # 代码修改工具
│       ├── markdown.js           # Markdown 工具
│       └── errorHandler.js       # 错误处理
└── vite.config.js                 # Vite 配置
```

---

## 📚 功能介绍

### 1. 门户页面
<details>
<summary>点击展开详情</summary>

- **快速入口**：直接进入代码审查工作区
- **功能介绍**：展示核心功能和特性
- **使用指南**：帮助新用户快速上手
- **示例展示**：提供典型使用场景演示

</details>

### 2. 代码审查工作区
<details>
<summary>点击展开详情</summary>

#### 左侧边栏 - 会话管理
- **新建会话**：一键创建新的审查会话
- **历史列表**：按时间分组展示所有会话
- **快速搜索**：支持会话标题和内容搜索
- **批量操作**：删除、导出、重命名会话

#### 中间区域 - 对话交互
- **消息流**：清晰展示用户消息和 AI 回复
- **Markdown 渲染**：优雅的文本格式化
- **代码高亮**：自动识别和高亮代码块
- **流式输出**：实时展示 AI 思考过程
- **消息操作**：复制、重新生成、查看代码差异

#### 右侧区域 - 代码编辑器
- **Monaco Editor**：VSCode 级别的编辑体验
- **多语言支持**：Python、JavaScript、Java 等
- **代码对比**：原始版本 vs AI 建议并排展示
- **智能应用**：解析结构化修改指令并应用
- **实时预览**：修改后即时看到效果

#### 底部输入区
- **文本输入**：支持多行输入和快捷键
- **文件上传**：点击或拖拽上传代码文件
- **批量处理**：支持单文件或多文件审查
- **格式校验**：自动检查文件类型和大小

</details>

### 3. AI 审查能力
<details>
<summary>点击展开详情</summary>

#### 代码质量分析
- **命名规范**：检查变量、函数、类命名是否符合规范
- **代码结构**：评估代码组织和模块化程度
- **可读性**：分析代码的可读性和可维护性
- **注释质量**：检查文档字符串和注释的完整性

#### 性能优化建议
- **算法复杂度**：分析时间和空间复杂度
- **资源使用**：识别内存泄漏和资源浪费
- **并发性能**：评估并发和异步处理
- **数据库优化**：SQL 查询和 ORM 使用建议

#### 安全性检查
- **注入攻击**：检测 SQL 注入、命令注入风险
- **权限控制**：评估访问控制和权限验证
- **敏感信息**：识别硬编码密码和密钥
- **输入验证**：检查用户输入验证逻辑

#### 最佳实践建议
- **设计模式**：推荐适用的设计模式
- **编码规范**：符合 PEP8、ESLint 等标准
- **异常处理**：完善的错误处理机制
- **测试覆盖**：建议测试用例和覆盖率

</details>

### 4. 结构化修改指令
<details>
<summary>点击展开详情</summary>

AI 可以生成结构化的修改指令，前端智能解析并应用：

```markdown
#### 🔧 结构化修改指令

**修改1：添加模块文档字符串**
- 操作类型：INSERT
- 位置：1
- 内容：
\```python
'''
此模块提供数字计算相关功能
'''
\```

**修改2：优化函数逻辑**
- 操作类型：REPLACE
- 位置：10-15
- 内容：
\```python
def optimized_function():
    # 优化后的代码
    pass
\```
```

**支持的操作类型**：
- `INSERT`: 在指定行插入代码
- `REPLACE`: 替换指定行范围的代码
- `DELETE`: 删除指定行范围的代码

</details>

---

## 📡 API 文档

### API 路径规范

所有 API 统一使用 `/api/v1/code` 前缀，便于未来扩展其他应用模块。

### 主要 API 端点

#### 健康检查
```http
GET /api/v1/code/health
```

#### 会话管理
```http
POST   /api/v1/code/sessions          # 创建会话
GET    /api/v1/code/sessions          # 获取会话列表
GET    /api/v1/code/sessions/{id}     # 获取会话详情
PUT    /api/v1/code/sessions/{id}     # 更新会话
DELETE /api/v1/code/sessions/{id}     # 删除会话
```

#### 消息管理
```http
POST   /api/v1/code/messages          # 发送消息
GET    /api/v1/code/messages          # 获取消息列表
DELETE /api/v1/code/messages/{id}     # 删除消息
```

#### 文件管理
```http
POST   /api/v1/code/files/upload      # 上传文件
GET    /api/v1/code/files/{id}        # 获取文件内容
DELETE /api/v1/code/files/{id}        # 删除文件
```

#### 代码审查
```http
POST   /api/v1/code/review            # 提交审查请求
POST   /api/v1/code/chat              # 对话交互
```

### 完整 API 文档

启动后端服务后，访问自动生成的 Swagger 文档：
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📂 项目结构

```
CodeReviewAssistant/
├── python-back/                 # 后端服务
│   ├── app/                     # 应用代码
│   │   ├── api/                 # API 路由
│   │   ├── services/            # 业务逻辑
│   │   ├── models/              # 数据模型
│   │   ├── schemas/             # Pydantic 模式
│   │   ├── core/                # 核心配置
│   │   └── utils/               # 工具函数
│   ├── data/                    # 数据库文件
│   ├── uploads/                 # 上传文件存储
│   ├── requirements.txt         # Python 依赖
│   ├── run.py                   # 启动脚本
│   └── .env                     # 环境变量配置
│
├── vue3-front/                  # 前端应用
│   └── vue-project/
│       ├── src/                 # 源代码
│       │   ├── api/             # API 封装
│       │   ├── components/      # Vue 组件
│       │   ├── stores/          # Pinia 状态
│       │   ├── views/           # 页面视图
│       │   ├── router/          # 路由配置
│       │   ├── utils/           # 工具函数
│       │   └── assets/          # 静态资源
│       ├── public/              # 公共资源
│       ├── package.json         # npm 依赖
│       └── vite.config.js       # Vite 配置
│
├── docs/                        # 项目文档
│   ├── Day1-11.7/              # Day 1 开发文档
│   ├── Day2-11.8/              # Day 2 开发文档
│   ├── Day3-11.8/              # Day 3 开发文档
│   ├── Day4-11.9/              # Day 4 开发文档
│   └── Day5-11.9/              # Day 5 开发文档
│
├── 项目企划书_AI代码Review助手.md   # 项目企划书
└── README.md                    # 本文档
```

---

## ⚙️ 配置说明

### 后端环境变量

在 `python-back/.env` 文件中配置：

| 变量名 | 说明 | 示例值 | 必填 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | `sk-xxx...` | ✅ |
| `OPENAI_API_BASE` | API 基础地址 | `https://api.openai.com/v1` | ❌ |
| `OPENAI_MODEL` | 使用的模型 | `gpt-4` | ❌ |
| `OPENAI_TEMPERATURE` | 生成温度 | `0.3` | ❌ |
| `DATABASE_URL` | 数据库连接 | `sqlite:///./data/app.db` | ❌ |
| `UPLOAD_DIR` | 上传目录 | `./uploads` | ❌ |
| `MAX_FILE_SIZE` | 最大文件大小 | `10485760` (10MB) | ❌ |

### 前端代理配置

在 `vue3-front/vue-project/vite.config.js` 中配置代理：

```javascript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
```

---

## 🔧 开发指南

### 后端开发

#### 添加新的 API 端点

1. 在 `app/api/v1/` 创建路由文件
2. 在 `app/services/` 创建服务逻辑
3. 在 `app/schemas/` 定义请求/响应模式
4. 在 `app/api/v1/__init__.py` 注册路由

#### 数据库迁移

```bash
# 创建迁移
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

#### 代码质量检查

```bash
# Pylint 检查
pylint app/

# Flake8 检查
flake8 app/

# 自动格式化
autopep8 --in-place --recursive app/
```

### 前端开发

#### 添加新组件

```bash
# 通用组件放在 src/components/common/
# 功能组件放在 src/components/[feature]/
```

#### 代码格式化

```bash
# 格式化代码
npm run lint

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

---

## 🚢 部署说明

### Docker 部署（推荐）

<details>
<summary>点击查看 Docker 部署步骤</summary>

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

</details>

### 手动部署

<details>
<summary>点击查看手动部署步骤</summary>

#### 后端部署

```bash
# 安装生产依赖
pip install -r requirements.txt

# 设置环境变量
export APP_ENV=production
export DEBUG=False

# 使用 Gunicorn 运行
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### 前端部署

```bash
# 构建静态文件
npm run build

# 部署 dist 目录到 Nginx/Apache
cp -r dist/* /var/www/html/
```

</details>

---

## 🧪 测试

### 后端测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_review.py

# 生成覆盖率报告
pytest --cov=app tests/
```

### 前端测试

```bash
# 运行单元测试
npm run test:unit

# 运行 E2E 测试
npm run test:e2e
```

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 贡献流程

1. **Fork 项目**到你的 GitHub 账号
2. **克隆仓库**到本地：`git clone https://github.com/your-username/CodeReviewAssistant.git`
3. **创建特性分支**：`git checkout -b feature/amazing-feature`
4. **提交更改**：`git commit -m 'Add some amazing feature'`
5. **推送分支**：`git push origin feature/amazing-feature`
6. **提交 Pull Request**

### 代码规范

- **Python**: 遵循 PEP8 规范
- **JavaScript**: 遵循 ESLint 配置
- **提交信息**: 使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式

### 报告问题

使用 [GitHub Issues](https://github.com/sysyemOL/CodeReviewAssistant/issues) 报告 Bug 或提出功能建议。

---

## 📝 开发路线图

### ✅ 已完成（MVP v1.0）

- [x] 基础架构搭建（前后端分离）
- [x] 用户界面设计和实现
- [x] 会话管理功能
- [x] 代码上传和文件管理
- [x] LangChain 审查链集成
- [x] 静态代码分析（Pylint、Flake8）
- [x] Monaco Editor 代码对比
- [x] 对话式交互
- [x] 流式输出
- [x] 结构化修改指令
- [x] API 路径规范化（/api/v1/code 前缀）

### 🚧 进行中（v1.1）

- [ ] 多语言支持（JavaScript、Java、Go）
- [ ] 代码差异对话框布局优化
- [ ] 自动化测试覆盖
- [ ] 性能优化和缓存机制
- [ ] 用户认证和授权

### 🎯 计划中（v2.0）

- [ ] 多用户系统
- [ ] 团队协作功能
- [ ] CI/CD 集成
- [ ] Git 仓库集成
- [ ] 审查报告导出（PDF、HTML）
- [ ] 自定义审查规则
- [ ] 插件系统
- [ ] 企业版功能

---

## ❓ 常见问题

<details>
<summary><strong>Q: OpenAI API 调用失败怎么办？</strong></summary>

**A**: 请检查：
1. `.env` 文件中的 `OPENAI_API_KEY` 是否正确
2. API 密钥是否有余额
3. 网络是否能访问 OpenAI API
4. 是否设置了正确的 `OPENAI_API_BASE`

</details>

<details>
<summary><strong>Q: 前端无法连接后端？</strong></summary>

**A**: 请检查：
1. 后端服务是否正常运行（访问 http://127.0.0.1:8000/docs）
2. `vite.config.js` 中的代理配置是否正确
3. 浏览器控制台是否有 CORS 错误
4. 防火墙是否拦截了端口

</details>

<details>
<summary><strong>Q: 代码差异对话框显示空白？</strong></summary>

**A**: 这是已知问题，正在优化中。临时解决方案：
1. 刷新页面（Ctrl + F5）
2. 清除浏览器缓存
3. 检查浏览器控制台的错误信息

</details>

<details>
<summary><strong>Q: 如何更换 AI 模型？</strong></summary>

**A**: 在 `.env` 文件中修改 `OPENAI_MODEL`：
- `gpt-3.5-turbo`: 更快、更便宜
- `gpt-4`: 更智能、更准确（推荐）
- `gpt-4-turbo`: 平衡速度和质量

</details>

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 👥 联系方式

- **项目作者**: 刘硕
- **GitHub**: [@sysyemOL](https://github.com/sysyemOL)
- **Email**: your.email@example.com
- **问题反馈**: [GitHub Issues](https://github.com/sysyemOL/CodeReviewAssistant/issues)

---

## 🙏 致谢

感谢以下开源项目和工具：

- [LangChain](https://python.langchain.com/) - 强大的 LLM 应用框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Monaco Editor](https://microsoft.github.io/monaco-editor/) - VSCode 编辑器内核
- [Element Plus](https://element-plus.org/) - 优秀的 Vue 3 UI 组件库
- [OpenAI](https://openai.com/) - GPT 模型提供商

---

## ⭐ Star History

如果这个项目对你有帮助，请给它一个 ⭐️！

[![Star History Chart](https://api.star-history.com/svg?repos=sysyemOL/CodeReviewAssistant&type=Date)](https://star-history.com/#sysyemOL/CodeReviewAssistant&Date)

---

<div align="center">

**[⬆ 回到顶部](#-ai-code-review-assistant)**

Made with ❤️ by [刘硕](https://github.com/sysyemOL)

</div>
