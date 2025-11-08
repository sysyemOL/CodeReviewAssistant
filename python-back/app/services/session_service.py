"""
会话服务
"""
import uuid
from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate, SessionUpdate


def generate_session_id() -> str:
    """生成唯一的会话ID"""
    return f"sess_{uuid.uuid4().hex[:16]}"


def create_session(db: Session, session_data: SessionCreate) -> SessionModel:
    """创建新会话"""
    db_session = SessionModel(
        session_id=generate_session_id(),
        title=session_data.title
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_session(db: Session, session_id: str) -> SessionModel:
    """根据ID获取会话"""
    return db.query(SessionModel).filter(SessionModel.session_id == session_id).first()


def get_sessions(db: Session, skip: int = 0, limit: int = 100) -> list:
    """获取会话列表"""
    return db.query(SessionModel).order_by(SessionModel.updated_at.desc()).offset(skip).limit(limit).all()


def get_session_count(db: Session) -> int:
    """获取会话总数"""
    return db.query(SessionModel).count()


def update_session(db: Session, session_id: str, session_data: SessionUpdate) -> SessionModel:
    """更新会话"""
    db_session = get_session(db, session_id)
    if not db_session:
        return None
    
    update_data = session_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_session, key, value)
    
    db.commit()
    db.refresh(db_session)
    return db_session


def delete_session(db: Session, session_id: str) -> bool:
    """删除会话"""
    db_session = get_session(db, session_id)
    if not db_session:
        return False
    
    db.delete(db_session)
    db.commit()
    return True

