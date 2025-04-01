from celery import Celery
from models import db, Task, KnowledgePoint, Question, ReferenceAnswer
from utils.file_utils import read_file_content, split_string
from utils.knowledge_extract import knowledge_extract
from utils.question_ask import generate_questions

celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task(bind=True)
def process_uploaded_file(self, file_stream, task_id):
    try:
        task = Task.query.get(task_id)
        task.status = 'processing'
        
        # 保存临时文件
        filename = secure_filename(file_stream.filename)
        temp_path = f"/tmp/{filename}"
        file_stream.save(temp_path)
        
        # 分阶段更新进度
        task.message = "正在读取文件内容"
        db.session.commit()
        
        content = read_file_content(temp_path)
        task.progress = 30
        db.session.commit()

        # 知识点抽取
        task.message = "抽取知识点中..."
        knowledges = knowledge_extract(content)
        
        # 存储知识点
        for k in knowledges:
            new_kp = KnowledgePoint(
                title=k['title'],
                content=k['content'],
                task_id=task_id
            )
            db.session.add(new_kp)
        task.progress = 60
        db.session.commit()

        # 生成问题
        task.message = "生成测试问题..."
        subject, questions, answers = generate_questions(knowledges, 5)
        
        for q, a in zip(questions, answers):
            new_question = Question(
                content=q,
                task_id=task_id
            )
            db.session.add(new_question)
            new_answer = ReferenceAnswer(
                content=a,
                question=new_question
            )
            db.session.add(new_answer)
        
        task.status = 'completed'
        task.progress = 100
        db.session.commit()

    except Exception as e:
        task.status = 'failed'
        task.message = str(e)
        db.session.commit()