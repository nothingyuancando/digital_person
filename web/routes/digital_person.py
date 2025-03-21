#数字人对话接口

from flask import Blueprint, request
from models import DigitalPersonSession
from utils.response import success_response, error_response
import uuid

bp = Blueprint('digital_person', __name__, url_prefix='/api/digital-person')

@bp.route('/start', methods=['GET'])
def start_session():
    session_id = request.args.get('sessionId')
    
    if session_id:
        # 查找现有会话
        session = DigitalPersonSession.query.get(session_id)
        if not session:
            return error_response("会话不存在", 404)
    else:
        # 创建新会话
        session_id = str(uuid.uuid4())
        new_session = DigitalPersonSession(
            session_id=session_id,
            window_url=f"https://digital-person.example.com?sessionId={session_id}"
        )
        db.session.add(new_session)
        db.session.commit()

    return success_response({
        "windowUrl": new_session.window_url
    })