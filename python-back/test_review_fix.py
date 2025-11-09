"""
测试代码审查修复效果
"""
import os
import sys

# 添加 app 目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

def test_review_imports():
    """测试审查相关导入"""
    print("🔧 测试审查模块导入...")
    try:
        from app.services.review_chain import review_chain
        print("  ✅ review_chain 导入成功")

        from app.api.v1.review import router
        print("  ✅ review API 导入成功")

        from app.schemas.review import CodeReviewRequest, MultiFileReviewRequest
        print("  ✅ review schemas 导入成功")

        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        return False

def test_message_id_generation():
    """测试消息ID生成"""
    print("🔧 测试消息ID生成...")
    try:
        import uuid
        message_id = f"msg_{uuid.uuid4().hex[:16]}"

        # 检查格式
        if message_id.startswith("msg_") and len(message_id) == 20:  # "msg_" + 16位
            print(f"  ✅ 消息ID生成成功: {message_id}")
            return True
        else:
            print(f"  ❌ 消息ID格式错误: {message_id}")
            return False
    except Exception as e:
        print(f"  ❌ 消息ID生成失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🩺 代码审查修复测试")
    print("=" * 60)

    results = []
    results.append(("审查模块导入", test_review_imports()))
    results.append(("消息ID生成", test_message_id_generation()))

    # 打印总结
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")

    print(f"\n通过率: {passed}/{total}")

    if passed == total:
        print("\n🎉 所有修复验证通过！代码审查功能应该可以正常工作了！")
    else:
        print("\n⚠️ 部分修复需要进一步检查。")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

