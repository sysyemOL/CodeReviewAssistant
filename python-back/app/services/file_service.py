"""
文件服务
"""
import os
import uuid
import shutil
from typing import Optional, List
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.models.file import File as FileModel
from app.core.config import settings


def generate_file_id() -> str:
    """生成唯一的文件ID"""
    return f"file_{uuid.uuid4().hex[:16]}"


def get_upload_dir() -> Path:
    """获取上传目录路径"""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def get_session_upload_dir(session_id: str) -> Path:
    """获取会话专属上传目录"""
    session_dir = get_upload_dir() / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def is_allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in settings.ALLOWED_EXTENSIONS


def save_upload_file(
    upload_file: UploadFile,
    session_id: str,
    file_id: str
) -> tuple[str, int]:
    """
    保存上传的文件到本地
    
    返回：(文件路径, 文件大小)
    """
    session_dir = get_session_upload_dir(session_id)
    
    # 生成唯一的文件名：file_id + 原始文件名
    filename = f"{file_id}_{upload_file.filename}"
    filepath = session_dir / filename
    
    # 保存文件
    file_size = 0
    with open(filepath, "wb") as f:
        while chunk := upload_file.file.read(1024 * 1024):  # 每次读取1MB
            f.write(chunk)
            file_size += len(chunk)
    
    return str(filepath), file_size


async def read_file_content(filepath: str) -> Optional[str]:
    """读取文件内容"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        return None


def create_file_record(
    db: Session,
    file_id: str,
    session_id: str,
    filename: str,
    filepath: str,
    file_type: str,
    file_size: int,
    content: Optional[str] = None
) -> FileModel:
    """创建文件记录"""
    db_file = FileModel(
        file_id=file_id,
        session_id=session_id,
        filename=filename,
        filepath=filepath,
        file_type=file_type,
        file_size=file_size,
        content=content
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


async def upload_file(
    db: Session,
    upload_file: UploadFile,
    session_id: str,
    save_content: bool = True
) -> FileModel:
    """
    上传文件
    
    Args:
        db: 数据库会话
        upload_file: 上传的文件
        session_id: 会话ID
        save_content: 是否将文件内容保存到数据库
    
    Returns:
        文件模型
    """
    # 检查文件扩展名
    if not is_allowed_file(upload_file.filename):
        raise ValueError(f"不支持的文件类型: {upload_file.filename}")
    
    # 生成文件ID
    file_id = generate_file_id()
    
    # 保存文件到本地
    filepath, file_size = save_upload_file(upload_file, session_id, file_id)
    
    # 检查文件大小
    if file_size > settings.MAX_UPLOAD_SIZE:
        # 删除刚保存的文件
        os.remove(filepath)
        raise ValueError(f"文件大小超过限制: {file_size} > {settings.MAX_UPLOAD_SIZE}")
    
    # 读取文件内容（如果需要）
    content = None
    if save_content:
        content = await read_file_content(filepath)
    
    # 获取文件类型
    file_type = os.path.splitext(upload_file.filename)[1].lower()
    
    # 创建数据库记录
    db_file = create_file_record(
        db=db,
        file_id=file_id,
        session_id=session_id,
        filename=upload_file.filename,
        filepath=filepath,
        file_type=file_type,
        file_size=file_size,
        content=content
    )
    
    return db_file


def get_file(db: Session, file_id: str) -> Optional[FileModel]:
    """根据ID获取文件"""
    return db.query(FileModel).filter(FileModel.file_id == file_id).first()


def get_files_by_session(
    db: Session,
    session_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[FileModel]:
    """获取会话的所有文件"""
    return (
        db.query(FileModel)
        .filter(FileModel.session_id == session_id)
        .order_by(FileModel.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_file_count_by_session(db: Session, session_id: str) -> int:
    """获取会话的文件总数"""
    return db.query(FileModel).filter(FileModel.session_id == session_id).count()


def delete_file(db: Session, file_id: str) -> bool:
    """删除文件"""
    db_file = get_file(db, file_id)
    if not db_file:
        return False
    
    # 删除本地文件
    try:
        if os.path.exists(db_file.filepath):
            os.remove(db_file.filepath)
    except Exception as e:
        print(f"删除本地文件失败: {e}")
    
    # 删除数据库记录
    db.delete(db_file)
    db.commit()
    return True


def delete_session_files(db: Session, session_id: str) -> bool:
    """删除会话的所有文件"""
    db_files = get_files_by_session(db, session_id)
    
    # 删除所有文件
    for db_file in db_files:
        delete_file(db, db_file.file_id)
    
    # 删除会话目录
    session_dir = get_session_upload_dir(session_id)
    try:
        if session_dir.exists():
            shutil.rmtree(session_dir)
    except Exception as e:
        print(f"删除会话目录失败: {e}")
    
    return True


def get_file_content(db: Session, file_id: str) -> Optional[str]:
    """获取文件内容"""
    db_file = get_file(db, file_id)
    if not db_file:
        return None
    
    # 如果数据库中有内容，直接返回
    if db_file.content:
        return db_file.content
    
    # 否则从文件系统读取
    try:
        with open(db_file.filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"读取文件内容失败: {e}")
        return None

