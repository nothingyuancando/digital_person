from models import db, DigitalSession
from datetime import datetime
import uuid

def create_session(student_id: str) -> dict:
    """创建新对话会话"""
    session_id = str(uuid.uuid4())
    new_session = DigitalSession(
        session_id=session_id,
        student_id=student_id,
        start_time=datetime.utcnow(),
        status='active'
    )
    db.session.add(new_session)
    db.session.commit()
    return {
        "sessionId": session_id,
        "wsEndpoint": f"wss://api.example.com/digital-person/ws/{session_id}"
    }

def close_session(session_id: str):
    """结束对话会话"""
    session = DigitalSession.query.get(session_id)
    if session:
        session.end_time = datetime.utcnow()
        session.status = 'closed'
        db.session.commit()

def get_session_context(session_id: str) -> dict:
    """获取会话上下文"""
    session = DigitalSession.query.get(session_id)
    return {
        "studentId": session.student_id,
        "status": session.status,
        "startTime": session.start_time.isoformat()
    }