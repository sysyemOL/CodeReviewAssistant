"""
代码审查链服务
使用 LangChain 进行代码审查
"""
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.core.config import settings
import subprocess
import json


class CodeReviewChain:
    """代码审查链"""
    
    def __init__(self):
        """初始化审查链"""
        # 初始化 OpenAI 模型
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )
        
        # 创建审查提示模板
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
    
    def _get_system_prompt(self) -> str:
        """获取系统提示"""
        return """你是一位经验丰富的代码审查专家，精通多种编程语言和最佳实践。
你的任务是对提供的代码进行全面、专业的审查，并给出建设性的改进建议。

审查时请重点关注以下方面：
1. **代码质量**：代码风格、命名规范、可读性
2. **潜在问题**：bug、逻辑错误、边界条件处理
3. **性能优化**：算法效率、资源使用、性能瓶颈
4. **安全性**：安全漏洞、输入验证、敏感信息处理
5. **最佳实践**：设计模式、代码复用、模块化
6. **测试覆盖**：测试完整性、边界测试

请以结构化的 Markdown 格式输出审查结果，包括：
- 📊 **总体评分**：给出代码质量评分（1-10分）
- ✅ **优点**：代码中做得好的地方
- ⚠️ **问题**：发现的问题和风险
- 💡 **改进建议**：具体的改进建议和代码示例
- 🎯 **优先级排序**：按重要性排序改进项

保持专业、友好的语气，给出具体、可操作的建议。"""
    
    def _get_user_prompt_template(self) -> str:
        """获取用户提示模板"""
        return """请审查以下代码：

**文件名**：{filename}
**语言**：{language}
{static_analysis}

**代码内容**：
```{language}
{code}
```

{user_question}

请给出详细的审查结果。"""
    
    async def review_code(
        self,
        code: str,
        filename: str,
        language: str = "python",
        user_question: Optional[str] = None
    ) -> str:
        """
        审查代码
        
        Args:
            code: 代码内容
            filename: 文件名
            language: 编程语言
            user_question: 用户提出的具体问题
            
        Returns:
            审查结果（Markdown格式）
        """
        # 执行静态分析（如果是Python代码）
        static_analysis = ""
        if language.lower() == "python":
            pylint_result = await self._run_pylint(code, filename)
            if pylint_result:
                static_analysis = f"\n**静态分析结果（Pylint）**：\n```\n{pylint_result}\n```\n"
                
        # 准备输入数据
        input_data = {
            "code": code,
            "filename": filename,
            "language": language,
            "static_analysis": static_analysis,
            "user_question": f"\n**用户问题**：{user_question}\n" if user_question else ""
        }
        
        # 执行审查链
        try:
            result = await self.review_chain.ainvoke(input_data)
            return result
        except Exception as e:
            # 捕获连接错误和其他异常
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
    
    async def _run_pylint(self, code: str, filename: str) -> Optional[str]:
        """
        运行 Pylint 静态分析
        
        Args:
            code: 代码内容
            filename: 文件名
            
        Returns:
            Pylint 分析结果
        """
        try:
            # 将代码写入临时文件
            import tempfile
            import os
            
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
                    
                    # 格式化输出
                    issues = []
                    for issue in pylint_data[:10]:  # 只取前10个问题
                        issues.append(
                            f"- Line {issue.get('line', '?')}: "
                            f"[{issue.get('type', 'unknown')}] "
                            f"{issue.get('message', '')}"
                        )
                    
                    if issues:
                        return "\n".join(issues)
                    else:
                        return "✅ 未发现静态分析问题"
                
            finally:
                # 删除临时文件
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except Exception as e:
            print(f"Pylint 分析失败: {e}")
            return None
        
        return None
    
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
                    user_question=user_question if i == 1 else None  # 只在第一个文件显示用户问题
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


# 创建全局实例
review_chain = CodeReviewChain()

