"""
会话管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse, SessionList
from app.schemas.common import ResponseModel
from app.services import session_service

router = APIRouter()


@router.post("/", response_model=ResponseModel[SessionResponse])
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db)
):
    """
    创建新会话
    """
    try:
        session = session_service.create_session(db, session_data)
        return ResponseModel(
            code=200,
            message="会话创建成功",
            data=SessionResponse.model_validate(session)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=ResponseModel[SessionList])
async def get_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取会话列表
    """
    try:
        sessions = session_service.get_sessions(db, skip=skip, limit=limit)
        total = session_service.get_session_count(db)
        
        return ResponseModel(
            code=200,
            message="获取会话列表成功",
            data=SessionList(
                total=total,
                items=[SessionResponse.model_validate(s) for s in sessions]
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}", response_model=ResponseModel[SessionResponse])
async def get_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    获取单个会话详情
    """
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return ResponseModel(
        code=200,
        message="获取会话成功",
        data=SessionResponse.model_validate(session)
    )


@router.put("/{session_id}", response_model=ResponseModel[SessionResponse])
async def update_session(
    session_id: str,
    session_data: SessionUpdate,
    db: Session = Depends(get_db)
):
    """
    更新会话
    """
    session = session_service.update_session(db, session_id, session_data)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return ResponseModel(
        code=200,
        message="会话更新成功",
        data=SessionResponse.model_validate(session)
    )


@router.delete("/{session_id}", response_model=ResponseModel)
async def delete_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    删除会话
    """
    success = session_service.delete_session(db, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return ResponseModel(
        code=200,
        message="会话删除成功",
        data={"session_id": session_id}
    )

