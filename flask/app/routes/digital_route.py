from flask import Blueprint, request, jsonify
from services.digital_person import chat_service, session_service
from utils.response import success_response, error_response

digital_bp = Blueprint('digital_person', __name__, url_prefix='/api/digital-person')

@digital_bp.route('/session', methods=['POST'])
def create_dialog_session():
    """创建新对话会话"""
    student_id = request.json.get('studentId')
    if not student_id:
        return error_response("需要学生ID", 400)
    
    session_data = session_service.create_session(student_id)
    return success_response(data=session_data)

@digital_bp.route('/message', methods=['POST'])
async def handle_user_message():
    """处理用户消息"""
    session_id = request.headers.get('X-Session-Id')
    message_type = request.headers.get('Content-Type')
    
    try:
        processor = chat_service.DigitalChatProcessor(session_id)
        
        if message_type == 'audio/wav':
            text = speech_service.process_audio_input(session_id, request.files['audio'])
        else:
            text = request.json.get('text')
        
        response = await processor.process_message(text)
        return success_response(data=response)
    
    except Exception as e:
        return error_response(str(e), 500)

@digital_bp.route('/session/<session_id>', methods=['DELETE'])
def end_dialog_session(session_id: str):
    """结束对话会话"""
    session_service.close_session(session_id)
    return success_response(message="会话已结束")