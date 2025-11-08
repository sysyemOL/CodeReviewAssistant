"""
文件模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class File(Base):
    """文件模型"""
    
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_id = Column(String(50), unique=True, index=True, nullable=False, comment="文件唯一标识")
    session_id = Column(String(50), ForeignKey("sessions.session_id"), nullable=False, comment="所属会话ID")
    filename = Column(String(255), nullable=False, comment="文件名")
    filepath = Column(String(500), nullable=False, comment="文件路径")
    file_type = Column(String(20), nullable=True, comment="文件类型")
    file_size = Column(Integer, nullable=False, default=0, comment="文件大小（字节）")
    content = Column(Text, nullable=True, comment="文件内容")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    
    # 关系
    session = relationship("Session", back_populates="files")
    
    def __repr__(self):
        return f"<File(id={self.id}, filename={self.filename}, session_id={self.session_id})>"

