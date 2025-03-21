"""
数据库模型定义文件
包含课程管理、知识图谱、数字人对话、学生评分等核心业务的数据模型
"""

from datetime import datetime
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    """课程基本信息模型"""
    __tablename__ = 'course'
    
    course_id = db.Column(db.String(50), primary_key=True, comment='课程唯一标识')
    course_name = db.Column(db.String(100), nullable=False, comment='课程名称')
    description = db.Column(db.Text, comment='课程描述')

    # 关系字段
    files = db.relationship('CourseFile', backref='course', cascade='all, delete-orphan')
    knowledge_graphs = db.relationship('KnowledgeGraph', backref='course', cascade='all, delete-orphan')

class CourseFile(db.Model):
    """课程文件处理记录"""
    __tablename__ = 'course_file'
    
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='文件ID')
    course_id = db.Column(db.String(50), db.ForeignKey('course.course_id'), nullable=False, comment='所属课程ID')
    file_path = db.Column(db.String(255), nullable=False, comment='文件存储路径')
    process_id = db.Column(db.String(50), comment='异步处理任务ID')
    status = db.Column(db.String(20), nullable=False, default='processing', comment='处理状态')


class KnowledgeGraph(db.Model):
    """
    知识图谱数据表
    存储结构化知识点及其关联关系
    """
    __tablename__ = 'knowledge_graph'
    
    # 自增主键
    kg_id = db.Column(
        db.Integer, 
        primary_key=True,
        autoincrement=True,
        comment='自增知识图谱ID'
    )
    
    # 外键关联
    course_id = db.Column(
        db.String(50), 
        db.ForeignKey('course.course_id'), 
        nullable=False,
        comment='所属课程ID'
    )
    
    # 知识点内容字段
    title = db.Column(
        db.String(100), 
        nullable=False,
        comment='知识点标题（不超过100字符）'
    )
    content = db.Column(
        db.Text, 
        nullable=False,
        comment='知识点详细内容（Markdown格式）'
    )

class DigitalPersonSession(db.Model):
    """
    数字人对话会话表
    管理数字人对话窗口的会话信息
    """
    __tablename__ = 'digital_person_session'
    
    # 主键字段
    session_id = db.Column(
        db.String(50), 
        primary_key=True,
        comment='会话唯一标识（建议UUID格式）'
    )
    
    # 资源地址字段
    window_url = db.Column(
        db.String(255), 
        nullable=False,
        comment='对话窗口URL地址（有效期通常为24小时）'
    )

class Student(db.Model):
    """
    学生基本信息表
    存储学生的核心身份信息
    """
    __tablename__ = 'student'
    
    # 主键字段
    student_id = db.Column(
        db.String(50), 
        primary_key=True,
        comment='学生唯一标识（学号或系统生成ID）'
    )
    
    # 基本信息字段
    name = db.Column(
        db.String(100), 
        nullable=False,
        comment='学生姓名（支持多语言字符）'
    )
    
    # 关系字段
    conversations = db.relationship(
        'ConversationRecord', 
        backref='student', 
        lazy=True,
        comment='关联的对话记录（一对多关系）'
    )

class ConversationRecord(db.Model):
    """
    对话记录总表
    存储对话会话的元数据和汇总信息
    """
    __tablename__ = 'conversation_record'
    
    # 主键字段
    record_id = db.Column(
        db.String(50), 
        primary_key=True,
        comment='对话记录ID（建议格式：学生ID_时间戳）'
    )
    
    # 外键关联
    student_id = db.Column(
        db.String(50), 
        db.ForeignKey('student.student_id'), 
        nullable=False,
        comment='关联学生ID'
    )
    course_id = db.Column(
        db.String(50), 
        db.ForeignKey('course.course_id'), 
        nullable=False,
        comment='关联课程ID'
    )
    
    # 时间字段
    conversation_time = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow,
        comment='对话开始时间（UTC时区）'
    )
    
    # 分析结果字段
    keyword = db.Column(
        db.String(100),
        comment='自动提取的关键词（逗号分隔）'
    )
    average_score = db.Column(
        db.Numeric(5,2),
        comment='对话平均得分（范围0.00-100.00）'
    )
    grade = db.Column(
        db.String(5),
        comment='等级评分（A/B/C/D/E）'
    )
    analysis_report = db.Column(
        db.Text,
        comment='JSON格式的详细分析报告'
    )
    
    # 关系字段
    details = db.relationship(
        'ConversationDetail', 
        backref='record', 
        lazy=True,
        comment='关联的对话详情（一对多关系）'
    )

class ConversationDetail(db.Model):
    """
    对话详情表
    存储对话过程中的逐条交互记录
    """
    __tablename__ = 'conversation_detail'
    
    # 自增主键
    detail_id = db.Column(
        db.Integer, 
        primary_key=True,
        autoincrement=True,
        comment='自增详情ID'
    )
    
    # 外键关联
    record_id = db.Column(
        db.String(50), 
        db.ForeignKey('conversation_record.record_id'), 
        nullable=False,
        comment='关联对话记录ID'
    )
    
    # 对话顺序字段
    conversation_no = db.Column(
        db.Integer, 
        nullable=False,
        comment='对话顺序号（从1开始递增）'
    )
    
    # 对话内容字段
    question = db.Column(
        db.Text, 
        nullable=False,
        comment='系统提出的问题（包含上下文语境）'
    )
    student_answer = db.Column(
        db.Text,
        comment='学生的回答内容（可能包含富文本）'
    )
    reference_answer = db.Column(
        db.Text,
        comment='参考答案（评分依据）'
    )
    
    # 评分字段
    score = db.Column(
        db.Numeric(5,2),
        comment='当前对话得分（范围0.00-100.00）'
    )

# 数据库使用注意事项：
# 1. 所有模型变更后需要执行数据库迁移（推荐使用Flask-Migrate）
# 2. 数值字段建议使用Decimal类型进行操作以避免精度问题
# 3. 时间字段默认使用UTC时间，前端展示时需做时区转换
# 4. 关系字段的lazy参数可根据实际场景调整加载策略
# 5. 建议为常用查询字段（如course_id, student_id）添加数据库索引