"""
对话聊天 API - 支持流式输出
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session as DBSession
from app.db.database import get_db
from app.models.message import Message
from app.models.session import Session as SessionModel
from app.schemas.chat import ChatRequest
from app.services.review_chain import review_chain
from app.models.file import File
import json
import asyncio
import uuid
import os
from datetime import datetime

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


async def generate_stream_response(
    user_message: str,
    session_id: str,
    file_ids: list,
    db: DBSession
):
    """
    生成流式响应
    """
    try:
        # 1. 保存用户消息
        user_msg_id = f"msg_{uuid.uuid4().hex[:16]}"
        user_message_obj = Message(
            message_id=user_msg_id,
            session_id=session_id,
            role='user',
            content=user_message
        )
        db.add(user_message_obj)
        db.commit()
        
        # 自动设置会话标题（如果是默认标题）
        session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
        if session and session.title == "新对话":
            # 使用用户消息的前6个字符作为标题
            title = user_message.strip()[:6]
            if len(user_message.strip()) > 6:
                title += "..."
            session.title = title
            db.commit()
        
        # 发送用户消息确认
        yield f"data: {json.dumps({'type': 'user_message', 'message_id': user_msg_id, 'content': user_message}, ensure_ascii=False)}\n\n"
        
        # 2. 准备代码内容（如果有文件）
        code_context = ""
        if file_ids:
            for file_id in file_ids:
                file = db.query(File).filter(File.file_id == file_id).first()
                if file and os.path.exists(file.filepath):
                    with open(file.filepath, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                        language = _get_language_from_filename(file.filename)
                        code_context += f"\n\n**文件**: {file.filename}\n```{language}\n{code_content}\n```\n"
        
        # 3. 构建完整的用户消息（包含代码上下文）
        full_message = user_message
        if code_context:
            full_message += code_context
        
        # 4. 调用 Agent 进行流式生成
        # 先创建 AI 消息对象并保存到数据库（内容为空）
        ai_msg_id = f"msg_{uuid.uuid4().hex[:16]}"
        ai_content = ""
        thinking_process = ""  # 收集思考过程
        
        # 立即保存空消息到数据库，以便中断时可以更新
        ai_message_obj = Message(
            message_id=ai_msg_id,
            session_id=session_id,
            role='assistant',
            content='',
            thinking_process=None
        )
        db.add(ai_message_obj)
        db.commit()
        
        # 发送开始信号
        yield f"data: {json.dumps({'type': 'start', 'message_id': ai_msg_id}, ensure_ascii=False)}\n\n"
        
        # 调用 Agent（流式）
        try:
            # 使用 astream_events 方法进行流式调用（LangChain 1.0 推荐）
            async for event in review_chain.agent.astream_events(
                {"messages": [{"role": "user", "content": full_message}]},
                version="v1"
            ):
                kind = event.get("event")
                
                # 处理工具调用（作为思考过程）
                if kind == "on_tool_start":
                    tool_name = event.get("name", "")
                    tool_input = event.get("data", {}).get("input", {})
                    thinking_text = f"🔧 正在使用工具: {tool_name}\n"
                    if tool_input:
                        thinking_text += f"输入: {str(tool_input)[:100]}...\n"
                    thinking_process += thinking_text  # 收集思考过程
                    yield f"data: {json.dumps({'type': 'thinking', 'delta': thinking_text}, ensure_ascii=False)}\n\n"
                    await asyncio.sleep(0.01)
                
                # 处理工具输出（作为思考过程）
                elif kind == "on_tool_end":
                    tool_name = event.get("name", "")
                    output = event.get("data", {}).get("output", "")
                    thinking_text = f"✅ {tool_name} 完成\n输出: {str(output)[:200]}...\n\n"
                    thinking_process += thinking_text  # 收集思考过程
                    yield f"data: {json.dumps({'type': 'thinking', 'delta': thinking_text}, ensure_ascii=False)}\n\n"
                    await asyncio.sleep(0.01)
                
                # 处理 LLM 流式输出
                elif kind == "on_chat_model_stream":
                    content = event.get("data", {}).get("chunk", {})
                    if hasattr(content, "content"):
                        delta = content.content
                        if delta:
                            ai_content += delta
                            # 发送增量内容
                            yield f"data: {json.dumps({'type': 'content', 'delta': delta}, ensure_ascii=False)}\n\n"
                            await asyncio.sleep(0.01)
        
        except Exception as e:
            error_msg = f"AI 响应错误: {str(e)}"
            print(f"Agent 流式调用错误: {e}")
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'error': error_msg}, ensure_ascii=False)}\n\n"
            ai_content = error_msg
        
        # 5. 更新 AI 消息内容和思考过程
        ai_message_obj.content = ai_content
        ai_message_obj.thinking_process = thinking_process if thinking_process else None
        
        # 更新会话的最后消息
        session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
        if session:
            session.updated_at = datetime.utcnow()
        
        db.commit()
        
        # 6. 发送完成信号
        yield f"data: {json.dumps({'type': 'done', 'message_id': ai_msg_id}, ensure_ascii=False)}\n\n"
        
    except Exception as e:
        error_msg = f"流式响应错误: {str(e)}"
        print(f"流式响应错误: {e}")
        import traceback
        traceback.print_exc()
        
        # 即使出错也要保存部分内容
        try:
            if 'ai_message_obj' in locals():
                db.commit()
        except:
            db.rollback()
        
        yield f"data: {json.dumps({'type': 'error', 'error': error_msg}, ensure_ascii=False)}\n\n"


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    db: DBSession = Depends(get_db)
):
    """
    流式对话接口
    
    支持 Server-Sent Events (SSE) 流式输出
    """
    # 验证会话是否存在
    session = db.query(SessionModel).filter(
        SessionModel.session_id == request.session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 返回流式响应
    return StreamingResponse(
        generate_stream_response(
            user_message=request.message,
            session_id=request.session_id,
            file_ids=request.file_ids or [],
            db=db
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 禁用 nginx 缓冲
        }
    )


@router.post("/send")
async def chat_send(
    request: ChatRequest,
    db: DBSession = Depends(get_db)
):
    """
    普通对话接口（非流式）
    
    用于兼容不支持 SSE 的场景
    """
    try:
        # 验证会话是否存在
        session = db.query(SessionModel).filter(
            SessionModel.session_id == request.session_id
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 1. 保存用户消息
        user_msg_id = f"msg_{uuid.uuid4().hex[:16]}"
        user_message_obj = Message(
            message_id=user_msg_id,
            session_id=request.session_id,
            role='user',
            content=request.message
        )
        db.add(user_message_obj)
        db.commit()
        
        # 自动设置会话标题（如果是默认标题）
        if session and session.title == "新对话":
            # 使用用户消息的前6个字符作为标题
            title = request.message.strip()[:6]
            if len(request.message.strip()) > 6:
                title += "..."
            session.title = title
            db.commit()
        
        # 2. 准备代码内容（如果有文件）
        code_context = ""
        if request.file_ids:
            for file_id in request.file_ids:
                file = db.query(File).filter(File.file_id == file_id).first()
                if file and os.path.exists(file.filepath):
                    with open(file.filepath, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                        language = _get_language_from_filename(file.filename)
                        code_context += f"\n\n**文件**: {file.filename}\n```{language}\n{code_content}\n```\n"
        
        # 3. 构建完整的用户消息
        full_message = request.message
        if code_context:
            full_message += code_context
        
        # 4. 调用 Agent
        result = await review_chain.agent.ainvoke({
            "messages": [{"role": "user", "content": full_message}]
        })
        
        # 提取 AI 回复
        ai_content = ""
        if result and "messages" in result:
            last_message = result["messages"][-1]
            if hasattr(last_message, "content"):
                ai_content = last_message.content
            elif isinstance(last_message, dict):
                ai_content = last_message.get("content", "")
        
        # 5. 保存 AI 消息
        ai_msg_id = f"msg_{uuid.uuid4().hex[:16]}"
        ai_message_obj = Message(
            message_id=ai_msg_id,
            session_id=request.session_id,
            role='assistant',
            content=ai_content
        )
        db.add(ai_message_obj)
        
        # 更新会话时间
        session.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "user_message_id": user_msg_id,
                "ai_message_id": ai_msg_id,
                "content": ai_content
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")

