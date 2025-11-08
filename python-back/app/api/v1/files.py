"""
文件管理API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.file import FileResponse, FileList
from app.schemas.common import ResponseModel
from app.services import file_service

router = APIRouter()


@router.post("/upload", response_model=ResponseModel[FileResponse])
async def upload_file(
    file: UploadFile = File(...),
    session_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    上传单个文件
    
    Args:
        file: 上传的文件
        session_id: 会话ID
    
    Returns:
        文件信息
    """
    try:
        db_file = await file_service.upload_file(
            db=db,
            upload_file=file,
            session_id=session_id,
            save_content=True  # 保存文件内容到数据库
        )
        
        return ResponseModel(
            code=200,
            message="文件上传成功",
            data=FileResponse.model_validate(db_file)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@router.post("/upload-batch", response_model=ResponseModel[List[FileResponse]])
async def upload_files(
    files: List[UploadFile] = File(...),
    session_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    批量上传文件
    
    Args:
        files: 上传的文件列表
        session_id: 会话ID
    
    Returns:
        文件信息列表
    """
    try:
        uploaded_files = []
        for file in files:
            db_file = await file_service.upload_file(
                db=db,
                upload_file=file,
                session_id=session_id,
                save_content=True
            )
            uploaded_files.append(FileResponse.model_validate(db_file))
        
        return ResponseModel(
            code=200,
            message=f"成功上传 {len(uploaded_files)} 个文件",
            data=uploaded_files
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量上传失败: {str(e)}")


@router.get("/session/{session_id}", response_model=ResponseModel[FileList])
async def get_session_files(
    session_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取会话的所有文件
    
    Args:
        session_id: 会话ID
        skip: 跳过的记录数
        limit: 返回的记录数
    
    Returns:
        文件列表
    """
    try:
        files = file_service.get_files_by_session(db, session_id, skip, limit)
        total = file_service.get_file_count_by_session(db, session_id)
        
        return ResponseModel(
            code=200,
            message="获取文件列表成功",
            data=FileList(
                total=total,
                items=[FileResponse.model_validate(f) for f in files]
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{file_id}", response_model=ResponseModel[FileResponse])
async def get_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """
    获取单个文件信息
    
    Args:
        file_id: 文件ID
    
    Returns:
        文件信息
    """
    db_file = file_service.get_file(db, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return ResponseModel(
        code=200,
        message="获取文件成功",
        data=FileResponse.model_validate(db_file)
    )


@router.get("/{file_id}/content", response_model=ResponseModel[dict])
async def get_file_content(
    file_id: str,
    db: Session = Depends(get_db)
):
    """
    获取文件内容
    
    Args:
        file_id: 文件ID
    
    Returns:
        文件内容
    """
    content = file_service.get_file_content(db, file_id)
    if content is None:
        raise HTTPException(status_code=404, detail="文件不存在或无法读取")
    
    return ResponseModel(
        code=200,
        message="获取文件内容成功",
        data={"file_id": file_id, "content": content}
    )


@router.delete("/{file_id}", response_model=ResponseModel)
async def delete_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """
    删除文件
    
    Args:
        file_id: 文件ID
    
    Returns:
        删除结果
    """
    success = file_service.delete_file(db, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return ResponseModel(
        code=200,
        message="文件删除成功",
        data={"file_id": file_id}
    )


@router.delete("/session/{session_id}", response_model=ResponseModel)
async def delete_session_files(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    删除会话的所有文件
    
    Args:
        session_id: 会话ID
    
    Returns:
        删除结果
    """
    try:
        file_service.delete_session_files(db, session_id)
        return ResponseModel(
            code=200,
            message="会话文件删除成功",
            data={"session_id": session_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
