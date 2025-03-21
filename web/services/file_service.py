#异步任务服务

from celery import Celery
from models import db, CourseFile, KnowledgeGraph

celery = Celery(__name__)

@celery.task
def process_uploaded_file(file_id):
    with app.app_context():
        try:
            file_record = CourseFile.query.get(file_id)
            if not file_record:
                return

            # 调用处理逻辑
            knowledge_points = extract_keypoints(file_record.file_path)

            # 保存知识图谱
            for kp in knowledge_points:
                kg = KnowledgeGraph(
                    course_id=file_record.course_id,
                    title=kp['title'],
                    content=kp['content']
                )
                db.session.add(kg)

            # 更新文件状态
            file_record.status = 'success'
            db.session.commit()

        except Exception as e:
            file_record.status = 'failed'
            db.session.commit()

def extract_keypoints(file_path):
    # 实际处理逻辑实现
    return []