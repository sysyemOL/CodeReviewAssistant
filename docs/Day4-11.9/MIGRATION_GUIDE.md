# 🔄 迁移指南：从 Chain 模式到 Agent 模式

## 📝 概述

本指南将帮助你理解从传统的 LangChain Chain 模式迁移到 LangChain 1.0 Agent 模式的变化，以及如何更新你的代码。

## 🎯 为什么要迁移？

### Agent 模式的优势

1. **智能工具调用**: Agent 自动决定何时调用哪些工具
2. **更好的扩展性**: 动态添加新工具，无需修改核心逻辑
3. **自适应流程**: 根据代码特点灵活调整审查流程
4. **多步推理**: 支持复杂的多步推理和决策
5. **官方推荐**: LangChain 1.0 的官方推荐模式

## 📦 环境准备

### 1. 更新依赖

```bash
# 安装新依赖
pip install --upgrade langchain langchain-openai langgraph
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

### 2. 验证安装

```python
import langchain
print(langchain.__version__)  # 应该是 1.0.0 或更高
```

## 🔍 代码对比

### 旧版实现 (Chain 模式)

```python
# 旧版 review_chain.py (简化版)
class CodeReviewChain:
    def __init__(self):
        self.llm = ChatOpenAI(...)
        
        # 创建提示模板
        self.review_prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("user", self._get_user_prompt_template())
        ])
        
        # 创建审查链
        self.review_chain = (
            self.review_prompt
            | self.llm
            | StrOutputParser()
        )
    
    async def review_code(self, code, filename, language):
        # 手动执行静态分析
        static_analysis = await self._run_pylint(code, filename)
        
        # 构建输入
        input_data = {
            "code": code,
            "filename": filename,
            "language": language,
            "static_analysis": static_analysis
        }
        
        # 执行固定流程
        result = await self.review_chain.ainvoke(input_data)
        return result
    
    async def _run_pylint(self, code, filename):
        # 手动实现 Pylint 调用
        # ...
```

**问题**:
- ❌ 硬编码的工具调用流程
- ❌ 难以添加新工具
- ❌ 缺乏灵活性
- ❌ 所有语言都执行相同流程

### 新版实现 (Agent 模式)

```python
# 新版 review_chain.py (简化版)
class CodeReviewChain:
    def __init__(self):
        self.llm = ChatOpenAI(...)
        
        # 定义工具
        self.tools = [
            PylintAnalysisTool(),
            CodeComplexityTool(),
            SecurityCheckTool(),
        ]
        
        # 创建 Agent
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self._get_system_prompt(),
            name="CodeReviewAgent"
        )
    
    async def review_code(self, code, filename, language, user_question=None):
        # 构建用户消息
        user_message = f"""请审查以下代码：
        
**文件名**: {filename}
**编程语言**: {language}
**代码内容**:
```{language}
{code}
```

{f"**用户问题**: {user_question}" if user_question else ""}

请使用你的工具对代码进行全面分析，并给出详细的审查报告。"""
        
        # Agent 自动决策和执行
        result = await self.agent.ainvoke({
            "messages": [{"role": "user", "content": user_message}]
        })
        
        # 提取结果
        return result["messages"][-1].content
```

**优势**:
- ✅ Agent 自动选择工具
- ✅ 轻松添加新工具
- ✅ 根据代码类型自适应
- ✅ 支持复杂推理

## 🛠️ 工具封装

### 旧版：内部方法

```python
async def _run_pylint(self, code: str, filename: str) -> Optional[str]:
    """内部方法，难以复用和扩展"""
    try:
        # Pylint 逻辑
        ...
    except Exception as e:
        return None
```

### 新版：独立工具类

```python
class PylintAnalysisTool(BaseTool):
    """可复用、可测试、可扩展的工具"""
    name: str = "pylint_analysis"
    description: str = """对 Python 代码进行静态分析..."""
    args_schema: type[BaseModel] = PylintAnalysisInput
    
    def _run(self, code: str, filename: str = "temp.py") -> str:
        """工具实现"""
        try:
            # Pylint 逻辑
            ...
        except Exception as e:
            return f"⚠️ Pylint 分析失败: {str(e)}"
```

**优势**:
- ✅ 符合 LangChain 工具规范
- ✅ 可在其他 Agent 中复用
- ✅ 更好的错误处理
- ✅ 支持类型检查

## 🔧 API 变化

### 1. 初始化变化

```python
# 旧版
review_chain = CodeReviewChain()

# 新版（相同）
review_chain = CodeReviewChain()
```

### 2. 调用方式变化

```python
# 旧版和新版的调用方式保持兼容
result = await review_chain.review_code(
    code="def hello(): pass",
    filename="test.py",
    language="python"
)
```

### 3. 新增功能

```python
# 查看可用工具
tools = review_chain.list_tools()
print(tools)  # ['pylint_analysis', 'code_complexity_analysis', 'security_check']

# 动态添加工具
custom_tool = MyCustomTool()
review_chain.add_tool(custom_tool)
```

## 📊 性能对比

### 响应时间

| 模式 | 简单代码 | 复杂代码 | 多工具调用 |
|------|---------|---------|-----------|
| **Chain** | 2-3s | 3-5s | N/A |
| **Agent** | 3-5s | 5-8s | 8-12s |

> **注意**: Agent 模式可能稍慢，但提供了更智能和全面的分析

### 工具调用效率

- **Chain**: 固定调用所有检查，浪费 tokens
- **Agent**: 智能选择必要的工具，优化成本

## 🐛 常见问题

### Q1: 旧的 API 还能用吗？

**答**: 可以！我们保持了向后兼容，`review_code` 和 `review_multiple_files` 的接口保持不变。

### Q2: 如何迁移现有代码？

**答**: 大多数情况下不需要修改代码，只需更新依赖即可。如果你有自定义的静态分析逻辑，建议封装为工具。

### Q3: Agent 模式更贵吗？

**答**: 可能会稍微增加成本（多步推理），但通过智能工具选择可以优化 token 使用。

### Q4: 如何禁用某个工具？

**答**: 
```python
# 方法1: 初始化时不添加
review_chain.tools = [
    PylintAnalysisTool(),
    # 不添加 SecurityCheckTool
]

# 方法2: 从系统提示中移除工具说明
```

### Q5: 工具执行超时怎么办？

**答**: 每个工具都有内置的超时处理（如 Pylint 的 10 秒超时），会优雅降级。

## 🎓 最佳实践

### 1. 工具设计原则

```python
class GoodTool(BaseTool):
    """✅ 好的工具设计"""
    name: str = "descriptive_name"  # 清晰的名称
    description: str = """详细的描述，说明工具的用途、输入和输出"""
    args_schema: type[BaseModel] = WellDefinedInput  # 明确的输入模型
    
    def _run(self, **kwargs) -> str:
        try:
            # 核心逻辑
            result = self._process(**kwargs)
            return result
        except Exception as e:
            # 优雅的错误处理
            return f"⚠️ 工具执行失败: {str(e)}"
```

### 2. 系统提示优化

```python
def _get_system_prompt(self) -> str:
    """清晰地告诉 Agent 如何使用工具"""
    return """你是代码审查专家。

**可用工具**:
1. pylint_analysis: 用于 Python 代码静态分析
2. code_complexity_analysis: 用于分析代码复杂度

**工作流程**:
1. 先使用 pylint_analysis 检查 Python 代码
2. 使用 code_complexity_analysis 评估复杂度
3. 综合分析并给出报告
"""
```

### 3. 错误处理

```python
try:
    result = await review_chain.review_code(...)
except ConnectionError as e:
    # 处理连接错误
    print(f"API 连接失败: {e}")
except ValueError as e:
    # 处理认证错误
    print(f"认证失败: {e}")
except Exception as e:
    # 处理其他错误
    print(f"审查失败: {e}")
```

## 📚 进一步学习

### 官方资源

- [LangChain 1.0 Agent 文档](https://reference.langchain.com/python/langchain/agents/)
- [LangGraph 教程](https://langchain-ai.github.io/langgraph/)
- [自定义工具指南](https://python.langchain.com/docs/modules/tools/custom_tools)

### 项目文档

- [Agent 架构文档](./AGENT_ARCHITECTURE.md)
- [工具开发指南](./TOOL_DEVELOPMENT.md)

## 🤝 获取帮助

遇到问题？

1. 查看 [故障排除](./AGENT_ARCHITECTURE.md#故障排除)
2. 提交 Issue
3. 查看示例代码

## ✅ 迁移检查清单

- [ ] 更新依赖包 (`pip install -r requirements.txt`)
- [ ] 验证 LangChain 版本 (>= 1.0.0)
- [ ] 运行测试确保兼容性
- [ ] 测试旧 API 是否正常工作
- [ ] （可选）将自定义逻辑封装为工具
- [ ] （可选）优化系统提示
- [ ] 更新文档

---

**迁移完成！** 🎉

现在你可以享受 LangChain 1.0 Agent 模式带来的强大功能了！

