from models import db, ConversationRecord, ConversationDetail
from .speech_service import generate_audio_response
from llm import generate_digital_response, evaluate_response

class DigitalChatProcessor:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.context = {}
        
    def initialize_dialog(self):
        """初始化数字人对话"""
        welcome_text = "欢迎参加本次学习对话，请准备好开始了吗？"
        return self._build_response(welcome_text)
    
    async def process_message(self, user_input: str):
        """处理用户输入"""
        # 调用AI生成响应
        ai_response = await generate_digital_response(
            user_input=user_input,
            context=self.context
        )
        
        # 评估学生回答
        evaluation = evaluate_response(
            question=ai_response['current_question'],
            answer=user_input
        )
        
        # 保存对话记录
        self._save_conversation(
            user_input=user_input,
            ai_response=ai_response,
            evaluation=evaluation
        )
        
        return self._build_response(ai_response['text'])
    
    def _build_response(self, text: str) -> dict:
        """构建响应结构"""
        audio_url = generate_audio_response(text)
        return {
            "text": text,
            "audioUrl": audio_url,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _save_conversation(self, user_input: str, ai_response: dict, evaluation: dict):
        """保存对话记录"""
        # 主记录
        record = ConversationRecord(
            session_id=self.session_id,
            question=ai_response['current_question'],
            average_score=evaluation['score'],
            analysis_report=evaluation['report']
        )
        db.session.add(record)
        db.session.commit()
        
        # 对话详情
        detail = ConversationDetail(
            record_id=record.record_id,
            student_answer=user_input,
            reference_answer=ai_response['reference_answer'],
            score=evaluation['score']
        )
        db.session.add(detail)
        db.session.commit()