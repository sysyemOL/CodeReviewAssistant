"""
初始化数据库脚本 - 确保使用最新的模型定义
"""
from sqlalchemy import inspect
from app.db.database import Base, engine

# 强制导入所有模型（确保使用最新定义）
from app.models.session import Session
from app.models.message import Message, MessageRole
from app.models.file import File

if __name__ == "__main__":
    print("正在初始化数据库...")
    print(f"数据库路径: {engine.url}")
    
    # 先删除所有表
    print("删除旧表...")
    Base.metadata.drop_all(bind=engine)
    
    # 创建所有表
    print("创建新表...")
    Base.metadata.create_all(bind=engine)
    
    print("\n数据库初始化完成！")
    print("=" * 50)

    # 验证表结构
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        print(f"\n表 {table_name} 的列:")
        for column in inspector.get_columns(table_name):
            print(f"  - {column['name']}: {column['type']}")
    
    print("\n" + "=" * 50)
    print("验证完成！")