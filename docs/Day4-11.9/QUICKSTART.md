# 🚀 快速开始：LangChain 1.0 Agent 代码审查

## 📋 目录

- [安装](#安装)
- [配置](#配置)
- [基本使用](#基本使用)
- [进阶使用](#进阶使用)
- [故障排除](#故障排除)

## 安装

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd CodeReviewAssistant/python-back
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证安装

```bash
python -c "import langchain; print(f'LangChain version: {langchain.__version__}')"
```

应该输出：`LangChain version: 1.0.0` 或更高版本

## 配置

### 1. 创建 `.env` 文件

在 `python-back` 目录下创建 `.env` 文件：

```env
# OpenAI API 配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.2
OPENAI_MAX_TOKENS=8000

# 服务器配置
HOST=localhost
PORT=8000
DEBUG=True

# 数据库配置
DATABASE_URL=sqlite:///./app.db
```

### 2. 配置说明

| 配置项 | 说明 | 推荐值 |
|--------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | 必填 |
| `OPENAI_MODEL` | 模型名称 | `gpt-4o-mini` (性价比高) |
| `OPENAI_TEMPERATURE` | 温度参数 | `0.2` (更确定性) |
| `OPENAI_MAX_TOKENS` | 最大 token 数 | `8000` |

## 基本使用

### 方式 1: 在 Python 代码中使用

创建 `test_review.py`：

```python
import asyncio
from app.services.review_chain import review_chain


async def main():
    # 准备要审查的代码
    code = """
def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n - 1)
"""
    
    # 执行代码审查
    result = await review_chain.review_code(
        code=code,
        filename="factorial.py",
        language="python"
    )
    
    # 打印结果
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

运行：

```bash
python test_review.py
```

### 方式 2: 启动 Web 服务

```bash
# 启动 FastAPI 服务
uvicorn app.main:app --reload --host localhost --port 8000
```

然后使用 API：

```bash
# 使用 curl 测试
curl -X POST "http://localhost:8000/api/v1/review" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"hello\")",
    "filename": "test.py",
    "language": "python"
  }'
```

## 进阶使用

### 1. 带用户问题的审查

```python
result = await review_chain.review_code(
    code=code,
    filename="test.py",
    language="python",
    user_question="这个函数的时间复杂度如何优化？"
)
```

### 2. 多文件审查

```python
files = [
    {
        "filename": "models.py",
        "code": "class User:\n    pass",
        "language": "python"
    },
    {
        "filename": "views.py",
        "code": "def get_user():\n    pass",
        "language": "python"
    }
]

result = await review_chain.review_multiple_files(
    files=files,
    user_question="整体架构是否合理？"
)
```

### 3. 查看可用工具

```python
# 列出所有工具
tools = review_chain.list_tools()
print(f"可用工具: {tools}")
# 输出: ['pylint_analysis', 'code_complexity_analysis', 'security_check']
```

### 4. 添加自定义工具

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


# 定义输入模型
class MyToolInput(BaseModel):
    code: str = Field(description="代码内容")


# 定义工具
class MyCustomTool(BaseTool):
    name: str = "my_custom_tool"
    description: str = """我的自定义分析工具"""
    args_schema: type[BaseModel] = MyToolInput
    
    def _run(self, code: str) -> str:
        # 实现你的分析逻辑
        return f"分析了 {len(code)} 字符的代码"


# 添加工具
custom_tool = MyCustomTool()
review_chain.add_tool(custom_tool)

# 验证
print(review_chain.list_tools())
# 输出: ['pylint_analysis', 'code_complexity_analysis', 'security_check', 'my_custom_tool']
```

## 示例输出

### 典型的审查报告

```markdown
## 📊 代码审查报告

### 🔍 自动化分析结果

**Pylint 分析**:
发现 3 个问题（显示前15个）：
- Line 5, Column 0: [CONVENTION] Missing function docstring (missing-function-docstring)
- Line 8, Column 4: [WARNING] Unused variable 'x' (unused-variable)
- Line 12, Column 0: [REFACTOR] Too many branches (too-many-branches)

**代码复杂度分析**:
📊 代码复杂度分析：
- 总行数: 50
- 代码行: 38
- 注释行: 5
- 空白行: 7
- 最大嵌套深度: 3
- 注释率: 10.0%

💡 注释较少，建议增加文档注释

**安全检查**:
✅ 未发现明显的安全问题

### 📈 总体评分
代码质量: 7/10 分

### ✅ 优点
- 代码结构清晰，逻辑流程易于理解
- 变量命名符合 Python 规范
- 无明显的安全漏洞

### ⚠️ 问题与风险
- 缺少函数文档字符串
- 存在未使用的变量
- 部分函数分支过多，建议重构

### 💡 改进建议

1. **添加文档字符串**
```python
def calculate_factorial(n):
    """
    计算阶乘
    
    Args:
        n: 非负整数
        
    Returns:
        n 的阶乘
    """
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n - 1)
```

2. **删除未使用的变量**
3. **简化复杂函数**

### 🎯 优先级排序
1. [高优先级] 添加文档字符串
2. [中优先级] 清理未使用的变量
3. [低优先级] 增加注释
```

## 故障排除

### 问题 1: "未安装 Pylint"

**错误信息**: 
```
⚠️ 未安装 Pylint，跳过静态分析。建议安装：pip install pylint
```

**解决方案**:
```bash
pip install pylint
```

### 问题 2: "无法连接到 OpenAI API"

**可能原因**:
1. API Key 未配置或错误
2. 网络连接问题
3. API 配额不足

**解决方案**:
```bash
# 1. 检查 .env 文件
cat .env | grep OPENAI_API_KEY

# 2. 测试网络连接
curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"

# 3. 检查 API 配额
# 访问 https://platform.openai.com/account/usage
```

### 问题 3: "Agent 没有调用工具"

**可能原因**:
1. 系统提示不够清晰
2. LLM 模型能力限制
3. 代码过于简单，不需要工具

**解决方案**:
- 使用更强大的模型（如 `gpt-4`）
- 优化系统提示，明确指示使用工具
- 在用户消息中明确要求工具分析

### 问题 4: "响应太慢"

**优化建议**:
1. 使用更快的模型（`gpt-4o-mini`）
2. 减少 `max_tokens`
3. 限制工具数量
4. 使用缓存（待实现）

### 问题 5: ImportError

**错误信息**:
```
ImportError: cannot import name 'create_agent'
```

**解决方案**:
```bash
# 确保安装了 LangChain 1.0
pip install --upgrade langchain langchain-openai langgraph

# 验证版本
python -c "import langchain; print(langchain.__version__)"
```

## 下一步

- 📖 阅读 [Agent 架构文档](./AGENT_ARCHITECTURE.md)
- 🔄 查看 [迁移指南](./MIGRATION_GUIDE.md)
- 🛠️ 学习 [工具开发](./AGENT_ARCHITECTURE.md#自定义工具开发)
- 🧪 运行测试: `pytest tests/test_agent_review.py -v`

## 获取帮助

- 📧 提交 Issue
- 💬 查看文档
- 🤝 贡献代码

---

祝你使用愉快！🎉

