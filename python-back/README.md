# AI Code Review Assistant - Backend

基于 FastAPI + LangChain 的AI代码审查助手后端服务

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

重要配置项：
- `OPENAI_API_KEY`: 你的OpenAI API密钥
- `DATABASE_URL`: 数据库连接URL
- `PORT`: 服务端口（默认8000）

### 4. 启动服务

```bash
# 方式1: 使用run.py
python run.py

# 方式2: 直接使用uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 5. 访问API文档

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 📁 项目结构

```
python-back/
├── app/
│   ├── api/
│   │   └── v1/              # API路由
│   │       ├── health.py    # 健康检查
│   │       ├── sessions.py  # 会话管理
│   │       ├── messages.py  # 消息管理
│   │       └── files.py     # 文件管理
│   ├── core/
│   │   └── config.py        # 配置管理
│   ├── db/
│   │   └── database.py      # 数据库连接
│   ├── models/              # SQLAlchemy模型
│   │   ├── session.py
│   │   ├── message.py
│   │   └── file.py
│   ├── schemas/             # Pydantic模型
│   │   ├── session.py
│   │   ├── message.py
│   │   ├── file.py
│   │   └── common.py
│   ├── services/            # 业务逻辑
│   │   └── session_service.py
│   ├── utils/               # 工具函数
│   └── main.py              # FastAPI应用
├── tests/                   # 测试
├── .env.example             # 环境变量示例
├── .gitignore
├── requirements.txt         # 依赖列表
├── run.py                   # 启动脚本
└── README.md
```

## 🔧 开发说明

### 数据库模型

- **Session**: 会话模型，存储对话会话信息
- **Message**: 消息模型，存储会话中的消息
- **File**: 文件模型，存储上传的代码文件

### API端点

#### 健康检查
- `GET /api/v1/health/` - 健康检查
- `GET /api/v1/health/ping` - Ping测试

#### 会话管理
- `POST /api/v1/sessions/` - 创建会话
- `GET /api/v1/sessions/` - 获取会话列表
- `GET /api/v1/sessions/{session_id}` - 获取会话详情
- `PUT /api/v1/sessions/{session_id}` - 更新会话
- `DELETE /api/v1/sessions/{session_id}` - 删除会话

## 🧪 测试

```bash
# 运行测试
pytest

# 带覆盖率
pytest --cov=app tests/
```

## 📝 技术栈

- **FastAPI**: 现代、高性能的Web框架
- **SQLAlchemy**: ORM框架
- **Pydantic**: 数据验证
- **LangChain**: AI应用框架
- **OpenAI**: 大语言模型
- **Uvicorn**: ASGI服务器

## 📄 License

MIT

