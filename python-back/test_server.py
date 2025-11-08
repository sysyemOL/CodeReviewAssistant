"""
测试服务器启动
"""
import sys
print("正在启动FastAPI服务器...")
print(f"Python版本: {sys.version}")

try:
    import uvicorn
    print("✅ uvicorn导入成功")
    
    from app.main import app
    print("✅ FastAPI应用加载成功")
    
    print("\n🚀 启动服务器在 http://127.0.0.1:8000")
    print("📚 API文档: http://127.0.0.1:8000/docs\n")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
except Exception as e:
    print(f"❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()

