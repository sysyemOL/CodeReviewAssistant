"""
代码审查API
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.file import File
from app.models.message import Message
from app.schemas.review import (
    CodeReviewRequest,
    MultiFileReviewRequest,
    CodeReviewResponse
)
from app.services.review_chain import review_chain
from app.core.response import success_response
import os

router = APIRouter()


def _get_language_from_filename(filename: str) -> str:
    """从文件名获取编程语言"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.go': 'go',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.hpp': 'cpp',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.vue': 'vue',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.less': 'less'
    }
    
    ext = os.path.splitext(filename)[1].lower()
    return ext_map.get(ext, 'plaintext')


@router.post("/single", response_model=dict)
async def review_single_file(
    request: CodeReviewRequest,
    db: Session = Depends(get_db)
):
    """审查单个文件"""
    try:
        # 获取文件信息
        file = db.query(File).filter(File.file_id == request.file_id).first()
        if not file:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 读取文件内容（使用 filepath 字段）
        file_path = file.filepath
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="文件内容不存在")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # 执行代码审查
        language = _get_language_from_filename(file.filename)
        review_result = await review_chain.review_code(
            code=code_content,
            filename=file.filename,
            language=language,
            user_question=request.user_question
        )

        # 保存审查结果为AI消息
        import uuid
        message_id = f"msg_{uuid.uuid4().hex[:16]}"

        ai_message = Message(
            message_id=message_id,
            session_id=request.session_id,
            role='assistant',
            content=review_result
        )
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)
        
        return success_response(
            data={
                "session_id": request.session_id,
                "review_result": review_result,
                "message_id": ai_message.message_id
            },
            message="代码审查完成"
        )
        
    except HTTPException:
        raise
    except ConnectionError as e:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail=f"无法连接到 OpenAI API。请检查网络连接和 API 配置。\n详细错误: {str(e)}"
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=401,
            detail=f"OpenAI API 认证失败。请检查 OPENAI_API_KEY 配置。\n详细错误: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        print(f"代码审查失败: {error_msg}")
        raise HTTPException(
            status_code=500,
            detail=f"代码审查失败: {error_msg}"
        )


@router.post("/multiple", response_model=dict)
async def review_multiple_files(
    request: MultiFileReviewRequest,
    db: Session = Depends(get_db)
):
    """审查多个文件"""
    try:
        # 获取所有文件信息
        files_data = []
        for file_id in request.file_ids:
            file = db.query(File).filter(File.file_id == file_id).first()
            if not file:
                raise HTTPException(status_code=404, detail=f"文件不存在: {file_id}")
            
            # 读取文件内容（使用 filepath 字段）
            file_path = file.filepath
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail=f"文件内容不存在: {file.filename}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            files_data.append({
                'filename': file.filename,
                'code': code_content,
                'language': _get_language_from_filename(file.filename)
            })
        
        # 执行多文件代码审查
        review_result = await review_chain.review_multiple_files(
            files=files_data,
            user_question=request.user_question
        )

        # 保存审查结果为AI消息
        import uuid
        message_id = f"msg_{uuid.uuid4().hex[:16]}"

        ai_message = Message(
            message_id=message_id,
            session_id=request.session_id,
            role='assistant',
            content=review_result
        )
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)
        
        return success_response(
            data={
                "session_id": request.session_id,
                "review_result": review_result,
                "message_id": ai_message.message_id
            },
            message="多文件代码审查完成"
        )
        
    except HTTPException:
        raise
    except ConnectionError as e:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail=f"无法连接到 OpenAI API。请检查网络连接和 API 配置。\n详细错误: {str(e)}"
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=401,
            detail=f"OpenAI API 认证失败。请检查 OPENAI_API_KEY 配置。\n详细错误: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        print(f"多文件代码审查失败: {error_msg}")
        raise HTTPException(
            status_code=500,
            detail=f"代码审查失败: {error_msg}"
        )

