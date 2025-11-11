"""
代码审查链服务
使用 LangChain 1.0 Agent 模式进行代码审查
"""
from typing import Dict, List, Optional, Annotated
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from app.core.config import settings
import subprocess
import json
import tempfile
import os


# ==================== 工具定义 ====================

class PylintAnalysisInput(BaseModel):
    """Pylint 分析工具输入"""
    code: str = Field(description="需要分析的 Python 代码内容")
    filename: str = Field(default="temp.py", description="文件名（可选）")


class PylintAnalysisTool(BaseTool):
    """Pylint 静态代码分析工具"""
    name: str = "pylint_analysis"
    description: str = """对 Python 代码进行静态分析，检测潜在的代码质量问题、bug、代码风格问题等。
    输入：Python 代码字符串
    输出：Pylint 分析报告，包含问题列表及其严重程度"""
    args_schema: type[BaseModel] = PylintAnalysisInput
    
    def _run(self, code: str, filename: str = "temp.py") -> str:
        """执行 Pylint 分析"""
        try:
            # 将代码写入临时文件
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # 运行 Pylint
                result = subprocess.run(
                    ['pylint', temp_file, '--output-format=json'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # 解析 JSON 结果
                if result.stdout:
                    pylint_data = json.loads(result.stdout)
                    
                    if not pylint_data:
                        return "✅ 未发现静态分析问题"
                    
                    # 格式化输出
                    issues = []
                    for issue in pylint_data[:15]:  # 取前15个问题
                        issues.append(
                            f"- Line {issue.get('line', '?')}, "
                            f"Column {issue.get('column', '?')}: "
                            f"[{issue.get('type', 'unknown').upper()}] "
                            f"{issue.get('message', '')} "
                            f"({issue.get('symbol', '')})"
                        )
                    
                    return f"发现 {len(pylint_data)} 个问题（显示前15个）：\n" + "\n".join(issues)
                else:
                    return "✅ 未发现静态分析问题"
                    
            finally:
                # 删除临时文件
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except subprocess.TimeoutExpired:
            return "⚠️ Pylint 分析超时"
        except FileNotFoundError:
            return "⚠️ 未安装 Pylint，跳过静态分析。建议安装：pip install pylint"
        except Exception as e:
            return f"⚠️ Pylint 分析失败: {str(e)}"


class CodeComplexityInput(BaseModel):
    """代码复杂度分析工具输入"""
    code: str = Field(description="需要分析的代码内容")
    language: str = Field(default="python", description="编程语言")


class CodeComplexityTool(BaseTool):
    """代码复杂度分析工具（可扩展）"""
    name: str = "code_complexity_analysis"
    description: str = """分析代码的复杂度指标，包括函数长度、嵌套深度、圈复杂度等。
    帮助识别需要重构的复杂代码片段。"""
    args_schema: type[BaseModel] = CodeComplexityInput
    
    def _run(self, code: str, language: str = "python") -> str:
        """执行复杂度分析"""
        # 简单的复杂度分析实现
        lines = code.split('\n')
        total_lines = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        comment_lines = len([l for l in lines if l.strip().startswith('#')])
        blank_lines = len([l for l in lines if not l.strip()])
        
        # 计算最大嵌套深度
        max_indent = 0
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent // 4)
        
        report = f"""📊 代码复杂度分析：
- 总行数: {total_lines}
- 代码行: {code_lines}
- 注释行: {comment_lines}
- 空白行: {blank_lines}
- 最大嵌套深度: {max_indent}
- 注释率: {(comment_lines/total_lines*100):.1f}%"""
        
        # 给出建议
        suggestions = []
        if code_lines > 300:
            suggestions.append("⚠️ 代码行数较多，建议拆分为多个模块")
        if max_indent > 4:
            suggestions.append("⚠️ 嵌套层次过深，建议简化逻辑或提取函数")
        if comment_lines / total_lines < 0.1:
            suggestions.append("💡 注释较少，建议增加文档注释")
        
        if suggestions:
            report += "\n\n" + "\n".join(suggestions)
        else:
            report += "\n\n✅ 代码结构良好"
            
        return report


class SecurityCheckInput(BaseModel):
    """安全检查工具输入"""
    code: str = Field(description="需要检查的代码内容")
    language: str = Field(default="python", description="编程语言")


class SecurityCheckTool(BaseTool):
    """代码安全检查工具（可扩展）"""
    name: str = "security_check"
    description: str = """检查代码中的常见安全问题，如SQL注入、硬编码密钥、不安全的函数使用等。"""
    args_schema: type[BaseModel] = SecurityCheckInput
    
    def _run(self, code: str, language: str = "python") -> str:
        """执行安全检查"""
        issues = []
        
        # 简单的安全模式匹配
        security_patterns = {
            "eval(": "🔴 发现 eval() 使用，存在代码注入风险",
            "exec(": "🔴 发现 exec() 使用，存在代码注入风险",
            "pickle.loads": "🟡 发现 pickle.loads 使用，注意反序列化安全",
            "PASSWORD": "🟡 可能存在硬编码密码",
            "API_KEY": "🟡 可能存在硬编码 API 密钥",
            "SECRET": "🟡 可能存在硬编码敏感信息",
            "os.system": "🟡 发现 os.system 使用，可能存在命令注入风险",
            "subprocess.call": "🟡 发现 subprocess 使用，注意命令注入防护",
            "input(": "🟡 发现 input() 使用，注意输入验证",
        }
        
        for pattern, message in security_patterns.items():
            if pattern in code:
                issues.append(f"- {message}")
        
        if issues:
            return "🔒 安全检查发现以下问题：\n" + "\n".join(issues)
        else:
            return "✅ 未发现明显的安全问题"


# ==================== Agent 配置 ====================

class CodeReviewChain:
    """代码审查 Agent（基于 LangChain 1.0）"""
    
    def __init__(self):
        """初始化代码审查 Agent"""
        # 初始化 LLM（增加超时配置，防止长时间流式输出中断）
        import httpx
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            # 设置超时：连接5秒，读取300秒（5分钟），写入60秒
            timeout=httpx.Timeout(
                connect=5.0,    # 连接超时
                read=300.0,     # 读取超时（流式输出需要更长时间）
                write=60.0,     # 写入超时
                pool=5.0        # 连接池超时
            ),
            # 增加最大重试次数
            max_retries=2
        )
        
        # 定义可用工具
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
    
    def _get_system_prompt(self) -> str:
        """获取 Agent 系统提示"""
        return """你是一位经验丰富的代码审查专家，精通多种编程语言和最佳实践。

**你拥有以下工具**：
1. **pylint_analysis**: 对 Python 代码进行静态分析
2. **code_complexity_analysis**: 分析代码复杂度指标
3. **security_check**: 检查常见安全问题

**审查流程**：
1. 首先使用相应的工具对代码进行分析（Python代码使用pylint_analysis）
2. 使用 code_complexity_analysis 检查代码复杂度
3. 使用 security_check 检查安全问题
4. 综合工具分析结果和你的专业知识，给出全面的代码审查报告

**审查维度**：
- 代码质量：风格、命名、可读性
- 潜在问题：bug、逻辑错误、边界处理
- 性能优化：算法效率、资源使用
- 安全性：漏洞、输入验证、敏感信息
- 最佳实践：设计模式、代码复用、模块化
- 测试覆盖：测试完整性

**输出格式**（Markdown）：
## 📊 代码审查报告

### 🔍 自动化分析结果
[工具分析结果汇总]

### 📈 总体评分
代码质量: X/10 分

### ✅ 优点
- [列出代码的优点]

### ⚠️ 问题与风险
- [列出发现的问题]

### 💡 改进建议

#### 📝 文字说明
[概述性的改进建议说明]

#### 🔧 结构化修改指令

**关键要求**：必须严格按照以下格式输出，每个修改指令都要完整包含所有必需字段。

格式规范：
**修改1：[修改描述]**
- 操作类型：INSERT
- 位置：5
- 内容：
```python
[代码内容]
```

**修改2：[修改描述]**
- 操作类型：REPLACE
- 位置：10-12
- 内容：
```python
[代码内容]
```

**修改3：[修改描述]**
- 操作类型：DELETE
- 位置：15-16
- 内容：
```python
[要删除的代码（可选）]
```

完整示例：

**修改1：添加模块文档字符串**
- 操作类型：INSERT
- 位置：1
- 内容：
```python
'''
此模块提供数字计算相关功能
'''
```

**修改2：添加函数文档字符串**
- 操作类型：INSERT
- 位置：5
- 内容：
```python
    '''
    计算列表中所有数字的总和
    
    Args:
        numbers: 数字列表
        
    Returns:
        int: 所有数字的总和
    '''
```

**修改3：改进错误处理**
- 操作类型：REPLACE
- 位置：10-11
- 内容：
```python
    if not numbers:
        raise ValueError("输入列表不能为空")
    return sum(numbers)
```

关键规则（必须遵守）：
1. 操作类型必须是：INSERT、REPLACE、DELETE（全大写英文）
2. 位置必须是纯数字：单行用"5"，范围用"10-12"
3. 每个修改指令必须完整，不要省略任何字段
4. 代码块必须用三个反引号包裹，并指定语言
5. 位置指的是原始代码的行号
6. 尽量拆分成小步骤，一次修改不超过10行

### 🎯 优先级排序
1. [高优先级]
2. [中优先级]
3. [低优先级]

保持专业、友好，给出具体可操作的建议。"""
    
    async def review_code(
        self,
        code: str,
        filename: str,
        language: str = "python",
        user_question: Optional[str] = None
    ) -> str:
        """
        使用 Agent 模式审查代码
        
        Args:
            code: 代码内容
            filename: 文件名
            language: 编程语言
            user_question: 用户提出的具体问题
            
        Returns:
            审查结果（Markdown格式）
        """
        try:
            # 构建用户请求消息
            user_message = f"""请审查以下代码：

**文件名**: {filename}
**编程语言**: {language}

**代码内容**:
```{language}
{code}
```

{f"**用户问题**: {user_question}" if user_question else ""}

请使用你的工具对代码进行全面分析，并给出详细的审查报告。"""
            
            # 调用 Agent
            result = await self.agent.ainvoke({
                "messages": [{"role": "user", "content": user_message}]
            })
            
            # 提取最终响应
            if result and "messages" in result:
                # 获取最后一条消息（AI的最终回复）
                last_message = result["messages"][-1]
                if hasattr(last_message, "content"):
                    return last_message.content
                elif isinstance(last_message, dict):
                    return last_message.get("content", "未能生成审查报告")
            
            return "未能生成审查报告"
            
        except Exception as e:
            # 捕获并处理异常
            error_msg = str(e)
            print(f"代码审查失败: {error_msg}")
            
            # 检查是否是连接错误
            if "Connection" in error_msg or "connection" in error_msg.lower():
                raise ConnectionError(
                    f"无法连接到 OpenAI API。请检查：\n"
                    f"1. 网络连接是否正常\n"
                    f"2. OPENAI_API_KEY 是否正确配置\n"
                    f"3. API 服务是否可用\n"
                    f"原始错误: {error_msg}"
                )
            elif "API key" in error_msg.lower() or "authentication" in error_msg.lower():
                raise ValueError(
                    f"OpenAI API 认证失败。请检查 OPENAI_API_KEY 是否正确配置。\n"
                    f"原始错误: {error_msg}"
                )
            else:
                # 其他错误，抛出原始异常
                raise Exception(f"代码审查失败: {error_msg}")
    
    async def review_multiple_files(
        self,
        files: List[Dict[str, str]],
        user_question: Optional[str] = None
    ) -> str:
        """
        审查多个文件
        
        Args:
            files: 文件列表，每个文件包含 {filename, code, language}
            user_question: 用户提出的具体问题
            
        Returns:
            综合审查结果（Markdown格式）
        """
        results = []
        
        results.append("# 📝 多文件代码审查报告\n")
        
        # 逐个审查文件
        for i, file_info in enumerate(files, 1):
            results.append(f"\n## {i}. {file_info['filename']}\n")
            
            try:
                review_result = await self.review_code(
                    code=file_info['code'],
                    filename=file_info['filename'],
                    language=file_info.get('language', 'python'),
                    user_question=user_question 
                )
                results.append(review_result)
            except ConnectionError as e:
                # 连接错误，记录并继续处理其他文件
                error_msg = str(e)
                results.append(f"❌ **审查失败**：无法连接到 OpenAI API\n\n{error_msg}")
                print(f"文件 {file_info['filename']} 审查失败（连接错误）: {error_msg}")
            except Exception as e:
                # 其他错误，记录并继续处理其他文件
                error_msg = str(e)
                results.append(f"❌ **审查失败**：{error_msg}")
                print(f"文件 {file_info['filename']} 审查失败: {error_msg}")
            
            results.append("\n---\n")
        
        # 添加综合建议
        results.append("\n## 📋 综合建议\n")
        results.append("基于以上所有文件的审查结果，建议优先处理以下事项：\n")
        results.append("1. 首先修复所有**安全性**和**严重bug**问题\n")
        results.append("2. 然后优化**性能**相关的问题\n")
        results.append("3. 最后改善**代码质量**和**可维护性**\n")
        
        return "\n".join(results)
    
    def add_tool(self, tool: BaseTool) -> None:
        """
        添加新工具到 Agent（支持后续扩展）
        
        Args:
            tool: 新的工具实例
            
        Example:
            # 添加自定义工具
            custom_tool = MyCustomTool()
            review_chain.add_tool(custom_tool)
        """
        if tool not in self.tools:
            self.tools.append(tool)
            # 重新创建 Agent
            self.agent = create_agent(
                model=self.llm,
                tools=self.tools,
                system_prompt=self._get_system_prompt(),
                name="CodeReviewAgent"
            )
            print(f"✅ 工具 '{tool.name}' 已添加到 Agent")
    
    def list_tools(self) -> List[str]:
        """
        列出所有可用工具
        
        Returns:
            工具名称列表
        """
        return [tool.name for tool in self.tools]


# ==================== 可扩展工具示例 ====================
# 以下是可以后续添加的工具示例

class ESLintAnalysisTool(BaseTool):
    """ESLint 分析工具（JavaScript/TypeScript）"""
    name: str = "eslint_analysis"
    description: str = """对 JavaScript/TypeScript 代码进行静态分析"""
    args_schema: type[BaseModel] = PylintAnalysisInput  # 复用相同的输入结构
    
    def _run(self, code: str, filename: str = "temp.js") -> str:
        """执行 ESLint 分析"""
        # TODO: 实现 ESLint 分析逻辑
        return "⚠️ ESLint 分析功能待实现"


class PerformanceAnalysisTool(BaseTool):
    """性能分析工具"""
    name: str = "performance_analysis"
    description: str = """分析代码的性能特征，识别潜在的性能瓶颈"""
    args_schema: type[BaseModel] = CodeComplexityInput
    
    def _run(self, code: str, language: str = "python") -> str:
        """执行性能分析"""
        # TODO: 实现性能分析逻辑（如时间复杂度分析）
        return "⚠️ 性能分析功能待实现"


# 创建全局实例
review_chain = CodeReviewChain()


# ==================== 使用示例 ====================
"""
# 基本使用
result = await review_chain.review_code(
    code="def hello(): print('hello')",
    filename="test.py",
    language="python"
)

# 添加新工具
# eslint_tool = ESLintAnalysisTool()
# review_chain.add_tool(eslint_tool)

# 查看所有工具
# print(review_chain.list_tools())
"""

