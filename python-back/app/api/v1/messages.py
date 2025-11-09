"""
消息管理API
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse
from app.core.response import success_response

router = APIRouter()


@router.post("/", response_model=dict)
async def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """创建消息"""
    try:
        # 生成消息ID
        import uuid
        message_id = f"msg_{uuid.uuid4().hex[:16]}"
        
        # 创建消息
        db_message = Message(
            message_id=message_id,
            session_id=message.session_id,
            role=message.role,
            content=message.content
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        return success_response(
            data=MessageResponse.model_validate(db_message),
            message="消息创建成功"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}", response_model=dict)
async def get_session_messages(
    session_id: str,
    db: Session = Depends(get_db)
):
    """获取会话的所有消息"""
    try:
        messages = db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.created_at.asc()).all()
        
        return success_response(
            data={
                "items": [MessageResponse.model_validate(msg) for msg in messages],
                "total": len(messages)
            },
            message="获取消息列表成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{message_id}", response_model=dict)
async def get_message(
    message_id: str,
    db: Session = Depends(get_db)
):
    """获取单个消息"""
    try:
        message = db.query(Message).filter(Message.message_id == message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="消息不存在")
        
        return success_response(
            data=MessageResponse.model_validate(message),
            message="获取消息成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{message_id}", response_model=dict)
async def delete_message(
    message_id: str,
    db: Session = Depends(get_db)
):
    """删除消息"""
    try:
        message = db.query(Message).filter(Message.message_id == message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="消息不存在")
        
        db.delete(message)
        db.commit()
        
        return success_response(message="消息删除成功")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

