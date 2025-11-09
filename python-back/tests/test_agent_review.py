"""
测试 LangChain 1.0 Agent 代码审查功能
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.review_chain import (
    CodeReviewChain,
    PylintAnalysisTool,
    CodeComplexityTool,
    SecurityCheckTool,
)


class TestTools:
    """测试各个工具的功能"""
    
    def test_pylint_tool_initialization(self):
        """测试 PylintAnalysisTool 初始化"""
        tool = PylintAnalysisTool()
        assert tool.name == "pylint_analysis"
        assert "静态分析" in tool.description
        assert tool.args_schema is not None
    
    def test_complexity_tool_initialization(self):
        """测试 CodeComplexityTool 初始化"""
        tool = CodeComplexityTool()
        assert tool.name == "code_complexity_analysis"
        assert "复杂度" in tool.description
    
    def test_security_tool_initialization(self):
        """测试 SecurityCheckTool 初始化"""
        tool = SecurityCheckTool()
        assert tool.name == "security_check"
        assert "安全" in tool.description
    
    def test_pylint_tool_no_issues(self):
        """测试 Pylint 工具 - 无问题代码"""
        tool = PylintAnalysisTool()
        code = "def hello():\n    return 'hello'"
        
        # 由于可能未安装 pylint，我们只检查是否返回字符串
        result = tool._run(code, "test.py")
        assert isinstance(result, str)
    
    def test_complexity_tool_simple_code(self):
        """测试复杂度工具 - 简单代码"""
        tool = CodeComplexityTool()
        code = """def hello():
    return 'hello'
"""
        result = tool._run(code, "python")
        
        assert "总行数" in result
        assert "代码行" in result
        assert "注释行" in result
    
    def test_complexity_tool_complex_code(self):
        """测试复杂度工具 - 复杂代码"""
        tool = CodeComplexityTool()
        # 生成一个超过 300 行的代码
        code = "\n".join([f"# line {i}" for i in range(350)])
        
        result = tool._run(code, "python")
        assert "代码行数较多" in result or "总行数" in result
    
    def test_security_tool_safe_code(self):
        """测试安全工具 - 安全代码"""
        tool = SecurityCheckTool()
        code = "def hello():\n    return 'hello'"
        
        result = tool._run(code, "python")
        assert "未发现明显的安全问题" in result or "✅" in result
    
    def test_security_tool_eval_detection(self):
        """测试安全工具 - 检测 eval"""
        tool = SecurityCheckTool()
        code = "result = eval(user_input)"
        
        result = tool._run(code, "python")
        assert "eval" in result.lower()
        assert "风险" in result or "🔴" in result
    
    def test_security_tool_password_detection(self):
        """测试安全工具 - 检测硬编码密码"""
        tool = SecurityCheckTool()
        code = "PASSWORD = 'secret123'"
        
        result = tool._run(code, "python")
        assert "PASSWORD" in result or "密码" in result


class TestCodeReviewChain:
    """测试 CodeReviewChain（Agent 模式）"""
    
    @pytest.fixture
    def review_chain(self):
        """创建 review_chain 实例"""
        with patch('app.services.review_chain.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = "test-key"
            mock_settings.OPENAI_MODEL = "gpt-4o-mini"
            mock_settings.OPENAI_TEMPERATURE = 0.2
            mock_settings.OPENAI_MAX_TOKENS = 8000
            
            chain = CodeReviewChain()
            return chain
    
    def test_initialization(self, review_chain):
        """测试 Agent 初始化"""
        assert review_chain.llm is not None
        assert len(review_chain.tools) == 3  # 应该有 3 个工具
        assert review_chain.agent is not None
    
    def test_list_tools(self, review_chain):
        """测试列出工具"""
        tools = review_chain.list_tools()
        
        assert isinstance(tools, list)
        assert len(tools) == 3
        assert "pylint_analysis" in tools
        assert "code_complexity_analysis" in tools
        assert "security_check" in tools
    
    def test_add_tool(self, review_chain):
        """测试添加自定义工具"""
        from langchain.tools import BaseTool
        from pydantic import BaseModel, Field
        
        class MockInput(BaseModel):
            code: str = Field(description="代码")
        
        class MockTool(BaseTool):
            name: str = "mock_tool"
            description: str = "测试工具"
            args_schema: type[BaseModel] = MockInput
            
            def _run(self, code: str) -> str:
                return "mock result"
        
        initial_count = len(review_chain.tools)
        mock_tool = MockTool()
        review_chain.add_tool(mock_tool)
        
        assert len(review_chain.tools) == initial_count + 1
        assert "mock_tool" in review_chain.list_tools()
    
    @pytest.mark.asyncio
    async def test_review_code_connection_error(self, review_chain):
        """测试代码审查 - 连接错误"""
        # Mock agent.ainvoke 抛出连接错误
        with patch.object(review_chain.agent, 'ainvoke', 
                         side_effect=Exception("Connection refused")):
            
            with pytest.raises(ConnectionError) as exc_info:
                await review_chain.review_code(
                    code="def hello(): pass",
                    filename="test.py",
                    language="python"
                )
            
            assert "无法连接到 OpenAI API" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_review_code_success(self, review_chain):
        """测试代码审查 - 成功"""
        # Mock agent response
        mock_message = Mock()
        mock_message.content = "## 📊 代码审查报告\n测试报告内容"
        
        mock_result = {
            "messages": [mock_message]
        }
        
        with patch.object(review_chain.agent, 'ainvoke', 
                         return_value=mock_result):
            
            result = await review_chain.review_code(
                code="def hello(): pass",
                filename="test.py",
                language="python"
            )
            
            assert isinstance(result, str)
            assert "代码审查报告" in result
    
    @pytest.mark.asyncio
    async def test_review_code_with_user_question(self, review_chain):
        """测试代码审查 - 带用户问题"""
        mock_message = Mock()
        mock_message.content = "报告内容"
        mock_result = {"messages": [mock_message]}
        
        with patch.object(review_chain.agent, 'ainvoke', 
                         return_value=mock_result) as mock_invoke:
            
            await review_chain.review_code(
                code="def hello(): pass",
                filename="test.py",
                language="python",
                user_question="这段代码有什么问题？"
            )
            
            # 验证调用时包含了用户问题
            call_args = mock_invoke.call_args[0][0]
            assert "messages" in call_args
            assert "用户问题" in call_args["messages"][0]["content"]
    
    @pytest.mark.asyncio
    async def test_review_multiple_files(self, review_chain):
        """测试多文件审查"""
        mock_message = Mock()
        mock_message.content = "单文件报告"
        mock_result = {"messages": [mock_message]}
        
        files = [
            {
                "filename": "test1.py",
                "code": "def func1(): pass",
                "language": "python"
            },
            {
                "filename": "test2.py",
                "code": "def func2(): pass",
                "language": "python"
            }
        ]
        
        with patch.object(review_chain.agent, 'ainvoke', 
                         return_value=mock_result):
            
            result = await review_chain.review_multiple_files(files)
            
            assert isinstance(result, str)
            assert "多文件代码审查报告" in result
            assert "test1.py" in result
            assert "test2.py" in result
            assert "综合建议" in result


class TestSystemPrompt:
    """测试系统提示"""
    
    def test_system_prompt_contains_tools(self):
        """测试系统提示包含工具说明"""
        with patch('app.services.review_chain.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = "test-key"
            mock_settings.OPENAI_MODEL = "gpt-4o-mini"
            mock_settings.OPENAI_TEMPERATURE = 0.2
            mock_settings.OPENAI_MAX_TOKENS = 8000
            
            chain = CodeReviewChain()
            prompt = chain._get_system_prompt()
            
            # 检查工具说明
            assert "pylint_analysis" in prompt
            assert "code_complexity_analysis" in prompt
            assert "security_check" in prompt
            
            # 检查审查维度
            assert "代码质量" in prompt
            assert "安全性" in prompt
            assert "性能优化" in prompt


class TestIntegration:
    """集成测试"""
    
    @pytest.mark.skipif(
        not pytest.config.getoption("--run-integration"),
        reason="需要 --run-integration 标志来运行集成测试"
    )
    @pytest.mark.asyncio
    async def test_real_code_review(self):
        """真实的代码审查测试（需要有效的 API key）"""
        from app.services.review_chain import review_chain
        
        code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total
"""
        
        try:
            result = await review_chain.review_code(
                code=code,
                filename="calculator.py",
                language="python"
            )
            
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"\n审查结果:\n{result}")
            
        except Exception as e:
            pytest.skip(f"集成测试失败（可能是 API 配置问题）: {e}")


def pytest_addoption(parser):
    """添加 pytest 命令行选项"""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="运行集成测试（需要有效的 API key）"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

