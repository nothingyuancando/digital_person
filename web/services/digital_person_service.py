"""
数字人对话服务模块
集成第三方数字人API实现智能对话
"""

import requests
from celery import shared_task
from extensions import db, celery
from models import ConversationDetail

class DigitalPersonEngine:
    """数字人引擎封装类"""
    
    def __init__(self, config):
        self.base_url = config['DIGITAL_PERSON_API']
        self.headers = {'Authorization': f'Bearer {config['DIGITAL_PERSON_KEY']}'}
    
    def generate_response(self, text):
        """生成数字人响应"""
        try:
            response = requests.post(
                f"{self.base_url}/v1/dialog",
                json={"message": text},
                headers=self.headers
            )
            return response.json()
        except Exception as e:
            current_app.logger.error(f"数字人API调用失败: {str(e)}")
            return None

@celery.task
def process_digital_response(detail_id, student_text):
    """异步处理数字人响应"""
    with db.app.app_context():
        try:
            detail = ConversationDetail.query.get(detail_id)
            engine = DigitalPersonEngine(current_app.config)
            
            # 调用数字人服务
            response = engine.generate_response(student_text)
            
            # 更新对话记录
            if response:
                detail.reference_answer = response.get('answer')
                detail.score = response.get('score')
                db.session.commit()
            
            return True
        except Exception as e:
            current_app.logger.error(f"处理失败: {str(e)}")
            return False