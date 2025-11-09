"""
测试 LangChain 集成
"""
import os
import sys

# 添加 app 目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """测试导入"""
    print("📦 测试 LangChain 导入...")
    
    try:
        from langchain_openai import ChatOpenAI
        print("  ✅ langchain_openai 导入成功")
    except ImportError as e:
        print(f"  ❌ langchain_openai 导入失败: {e}")
        return False
    
    try:
        from langchain_core.prompts import ChatPromptTemplate
        print("  ✅ langchain_core.prompts 导入成功")
    except ImportError as e:
        print(f"  ❌ langchain_core.prompts 导入失败: {e}")
        return False
    
    try:
        from langchain_core.output_parsers import StrOutputParser
        print("  ✅ langchain_core.output_parsers 导入成功")
    except ImportError as e:
        print(f"  ❌ langchain_core.output_parsers 导入失败: {e}")
        return False
    
    return True


def test_config():
    """测试配置"""
    print("\n⚙️ 测试配置...")
    
    try:
        from app.core.config import settings
        print("  ✅ 配置模块导入成功")
        
        if settings.OPENAI_API_KEY:
            print(f"  ✅ OPENAI_API_KEY 已配置 (前4位: {settings.OPENAI_API_KEY[:4]}...)")
        else:
            print("  ⚠️ OPENAI_API_KEY 未配置（需要在 .env 文件中设置）")
        
        print(f"  ℹ️ OPENAI_MODEL: {settings.OPENAI_MODEL}")
        print(f"  ℹ️ OPENAI_TEMPERATURE: {settings.OPENAI_TEMPERATURE}")
        print(f"  ℹ️ OPENAI_MAX_TOKENS: {settings.OPENAI_MAX_TOKENS}")
        
        return True
    except Exception as e:
        print(f"  ❌ 配置测试失败: {e}")
        return False


def test_review_chain():
    """测试审查链"""
    print("\n🔗 测试审查链...")
    
    try:
        from app.services.review_chain import review_chain
        print("  ✅ 审查链导入成功")
        
        # 测试链的属性
        if hasattr(review_chain, 'llm'):
            print("  ✅ LLM 已初始化")
        else:
            print("  ❌ LLM 未初始化")
            return False
        
        if hasattr(review_chain, 'review_prompt'):
            print("  ✅ 审查 Prompt 已配置")
        else:
            print("  ❌ 审查 Prompt 未配置")
            return False
        
        if hasattr(review_chain, 'review_chain'):
            print("  ✅ 审查链已构建")
        else:
            print("  ❌ 审查链未构建")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ 审查链测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_schemas():
    """测试 API Schemas"""
    print("\n📋 测试 API Schemas...")
    
    try:
        from app.schemas.review import CodeReviewRequest, MultiFileReviewRequest
        print("  ✅ 审查 Schema 导入成功")
        
        # 测试创建请求
        request = CodeReviewRequest(
            session_id="test_session",
            file_id="test_file",
            user_question="测试问题"
        )
        print(f"  ✅ 成功创建 CodeReviewRequest: {request.session_id}")
        
        return True
    except Exception as e:
        print(f"  ❌ API Schema 测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🧪 LangChain 集成测试")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(("导入测试", test_imports()))
    results.append(("配置测试", test_config()))
    results.append(("审查链测试", test_review_chain()))
    results.append(("API Schema测试", test_api_schemas()))
    
    # 打印总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！LangChain 集成成功！")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查上述错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())

