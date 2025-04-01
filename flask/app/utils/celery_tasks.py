from celery import Celery
from models import db, CourseFile
from your_ai_module import extract_knowledge, generate_questions  # 替换为实际AI模块

celery = Celery(__name__, broker='redis://localhost:6379/0')


@celery.task
def process_file_task(process_id):
    """增加错误处理的异步任务"""
    with db.app.app_context():
        record = CourseFile.query.get(process_id)
        if not record:
            app.logger.error(f"无效处理ID: {process_id}")
            return

        try:
            record.status = 'processing'
            db.session.commit()
            
            # 模拟处理进度
            for i in range(1, 101):
                record.progress = i
                if i % 10 == 0:
                    db.session.commit()
                time.sleep(0.1)
                
            record.status = 'success'
            db.session.commit()
            
        except Exception as e:
            record.status = 'failed'
            record.progress = 0
            db.session.commit()
            app.logger.error(f"处理失败: {str(e)}")