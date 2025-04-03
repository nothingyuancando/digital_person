# -*- coding: utf-8 -*-  # 添加文件编码声明
'''
封装特点说明
分层架构：
模型层：继承自 BaseModel 提供基础 CRUD 方法
服务层：通过 DatabaseManager 提供业务相关操作
核心功能：
自动事务管理（包含回滚机制）
批量操作支持（如对话记录+详情的原子操作）
关联数据验证（创建记录时检查学生/课程存在性）
常用查询模式封装（带关联的查询、统计查询）
扩展建议：
添加分页查询功能
增加缓存机制（如 Redis）
添加更复杂的统计查询
实现软删除（添加 is_deleted 标志字段）
错误处理：
统一捕获 SQLAlchemy 异常
自定义业务异常（如学生不存在时抛出）
使用时只需导入 DatabaseManager 类即可进行所有数据库操作，保持业务代码的简洁性。
'''
from datetime import datetime
from email._header_value_parser import Section

from sqlalchemy.exc import SQLAlchemyError
from app.__init__ import db

# -------------------- 基础模型类 --------------------
class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        try:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

# -------------------- 具体模型 --------------------
class Student(BaseModel):
    __tablename__ = 'student'
    student_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    conversations = db.relationship('ConversationRecord', backref='student', lazy=True)

    @classmethod
    def get_by_id(cls, student_id):
        return cls.query.get(student_id)

    @classmethod
    def search_by_name(cls, name_keyword):
        return cls.query.filter(cls.name.ilike(f"%{name_keyword}%")).all()

class Course(BaseModel):
    __tablename__ = 'course'
    course_id = db.Column(db.String(50), primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    conversations = db.relationship('ConversationRecord', backref='course', lazy=True)
    sections = db.relationship('CourseSection', backref='course', cascade='all, delete-orphan', lazy=True)
    @classmethod
    def get_by_id(cls, course_id):
        return cls.query.get(course_id)

class ConversationRecord(BaseModel):
    __tablename__ = 'conversation_record'
    record_id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.String(50), db.ForeignKey('course.course_id'), nullable=False)
    conversation_time = db.Column(db.DateTime, default=datetime.utcnow)
    keyword = db.Column(db.String(100))
    average_score = db.Column(db.Numeric(5, 2))
    grade = db.Column(db.String(5))
    analysis_report = db.Column(db.Text)
    details = db.relationship('ConversationDetail', backref='record', cascade="all, delete-orphan")

    @classmethod
    def get_with_details(cls, record_id):
        return cls.query.options(
            db.joinedload(cls.details)
        ).get(record_id)

class ConversationDetail(BaseModel):
    __tablename__ = 'conversation_detail'
    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.String(50), db.ForeignKey('conversation_record.record_id'), nullable=False)
    conversation_no = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    student_answer = db.Column(db.Text)
    reference_answer = db.Column(db.Text)
    score = db.Column(db.Numeric(5, 2))

class CourseSection(BaseModel):
    __tablename__ = 'course_section'
    section_id = db.Column(db.String(50), primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('course.course_id'), nullable=False)
    section_name = db.Column(db.String(100), nullable=False)
    knowledge_points = db.relationship('KnowledgePoint', backref='section', cascade="all, delete-orphan")
    questions = db.relationship('Question', backref='section', cascade="all, delete-orphan")

    @classmethod
    def get_by_section(cls,section_id):
        return cls.query.get(section_id)

    @classmethod
    def get_by_course(cls, course_id):
        return cls.query.filter_by(course_id=course_id).order_by(cls.section_id).all()

class KnowledgePoint(BaseModel):
    __tablename__ = 'knowledge_point'
    point_id = db.Column(db.String(50), primary_key=True)
    section_id = db.Column(db.String(50), db.ForeignKey('course_section.section_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    @classmethod
    def get_by_point(cls, point_id):
        return cls.query.get(point_id)

    @classmethod
    def get_by_section(cls, section_id):
        return cls.query.filter_by(section_id=section_id).order_by(cls.point_id).all()

class Question(BaseModel):
    __tablename__ = 'question'
    question_id = db.Column(db.String(50), primary_key=True)
    section_id = db.Column(db.String(50), db.ForeignKey('course_section.section_id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    @classmethod
    def get_by_question(cls, question_id):
        return cls.query.get(question_id)
    @classmethod
    def get_by_section(cls,section_id):

        return cls.query.filter_by(section_id=section_id).order_by(cls.question_id).all()

# -------------------- 服务类封装 --------------------
class DatabaseManager:
    # ==================== 学生管理 ====================
    @staticmethod
    def create_student(student_id, name):
        return Student.create(student_id=student_id, name=name)

    @staticmethod
    def get_student(student_id):
        return Student.get_by_id(student_id)

    @staticmethod
    def update_student(student_id, **kwargs):
        student = Student.get_by_id(student_id)
        if not student:
            raise ValueError("学生不存在")
        return student.update(**kwargs)

    @staticmethod
    def delete_student(student_id):
        student = Student.get_by_id(student_id)
        if not student:
            raise ValueError("学生不存在")
        return student.delete()

    @staticmethod
    def get_all_students():
        return Student.query.all()

    # ==================== 课程管理 ====================
    @staticmethod
    def create_course(course_id, course_name, description=None):
        return Course.create(
            course_id=course_id,
            course_name=course_name,
            description=description
        )

    @staticmethod
    def get_course(course_id):
        return Course.get_by_id(course_id)

    @staticmethod
    def update_course(course_id, **kwargs):
        course = Course.get_by_id(course_id)
        if not course:
            raise ValueError("课程不存在")
        return course.update(**kwargs)

    @staticmethod
    def delete_course(course_id):
        course = Course.get_by_id(course_id)
        if not course:
            raise ValueError("课程不存在")
        return course.delete()

    @staticmethod
    def get_all_courses():
        return Course.query.all()

    # ==================== 对话记录管理 ====================
    @staticmethod
    def create_conversation_record(record_data, details_data):
        """
        :param record_data: dict 包含对话记录字段
        :param details_data: list 包含多个对话详情字典
        """
        try:
            # 检查关联存在性
            if not Student.get_by_id(record_data['student_id']):
                raise ValueError("学生不存在")
            if not Course.get_by_id(record_data['course_id']):
                raise ValueError("课程不存在")

            # 创建主记录
            record = ConversationRecord.create(**record_data)

            # 批量创建详情
            for detail in details_data:
                ConversationDetail.create(record_id=record.record_id, **detail)

            return record
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_conversation_record(record_id):
        return ConversationRecord.get_with_details(record_id)

    @staticmethod
    def update_conversation_record(record_id, **kwargs):
        record = ConversationRecord.query.get(record_id)
        if not record:
            raise ValueError("对话记录不存在")

        # 检查关联存在性
        if 'student_id' in kwargs:
            if not Student.get_by_id(kwargs['student_id']):
                raise ValueError("新学生不存在")
        if 'course_id' in kwargs:
            if not Course.get_by_id(kwargs['course_id']):
                raise ValueError("新课程不存在")

        return record.update(**kwargs)

    @staticmethod
    def delete_conversation_record(record_id):
        record = ConversationRecord.query.get(record_id)
        if not record:
            raise ValueError("对话记录不存在")
        return record.delete()

    @staticmethod
    def get_all_conversation_records():
        return ConversationRecord.query.all()

    # ==================== 对话详情管理 ====================
    @staticmethod
    def create_conversation_detail(record_id, **detail_data):
        if not ConversationRecord.query.get(record_id):
            raise ValueError("对话记录不存在")
        return ConversationDetail.create(record_id=record_id, **detail_data)

    @staticmethod
    def get_conversation_detail(detail_id):
        return ConversationDetail.query.get(detail_id)

    @staticmethod
    def update_conversation_detail(detail_id, **kwargs):
        detail = ConversationDetail.query.get(detail_id)
        if not detail:
            raise ValueError("对话详情不存在")

        if 'record_id' in kwargs:
            if not ConversationRecord.query.get(kwargs['record_id']):
                raise ValueError("新对话记录不存在")

        return detail.update(**kwargs)

    @staticmethod
    def delete_conversation_detail(detail_id):
        detail = ConversationDetail.query.get(detail_id)
        if not detail:
            raise ValueError("对话详情不存在")
        return detail.delete()

    # @staticmethod
    # def get_all_details_for_record(record_id):
    #     return ConversationDetail.query.filter_by(record_id=record_id).all()

    # ==================== 课程章节管理 ====================
    @staticmethod
    def get_section(section_id):

        return CourseSection.get_by_section(section_id)

    @staticmethod
    def create_section(section_id,course_id, section_name):
        """创建课程章节"""
        if not Course.get_by_id(course_id):
            raise ValueError("所属课程不存在")
        return CourseSection.create(section_id=section_id,course_id=course_id, section_name=section_name)

    @staticmethod
    def update_section(section_id, **kwargs):
        """更新章节信息"""

        section = CourseSection.get_by_section(section_id)
        if not section:
            raise ValueError("章节不存在")

        # 检查课程存在性（如果更新课程ID）

        if 'course_id' in kwargs and not Course.get_by_id(kwargs['course_id']):
            raise ValueError("新课程不存在")

        kwargs['section_id'] = section_id
        return section.update(**kwargs)

    @staticmethod
    def delete_section(section_id):
        """删除章节及其关联数据"""
        section = CourseSection.get_by_section(section_id)
        if not section:
            raise ValueError("章节不存在")
        return section.delete()

    @staticmethod
    def get_sections_by_course(course_id):
        """获取指定课程的所有章节"""
        return CourseSection.get_by_course(course_id)

    # ==================== 知识点管理 ====================
    @staticmethod
    def get_knowledge_point(point_id):
        return KnowledgePoint.get_by_point(point_id)

    @staticmethod
    def create_knowledge_point(point_id,section_id, title, content):
        """创建知识点"""
        if not CourseSection.get_by_section(section_id):
            raise ValueError("所属章节不存在")
        return KnowledgePoint.create(point_id=point_id,section_id=section_id, title=title, content=content)

    @staticmethod
    def update_knowledge_point(point_id, **kwargs):
        """更新知识点"""
        point = KnowledgePoint.get_by_point(point_id)
        if not point:
            raise ValueError("知识点不存在")

        # 检查章节存在性（如果更新章节ID）
        if 'section_id' in kwargs and not CourseSection.get_by_section(kwargs['section_id']):
            raise ValueError("新章节不存在")
        kwargs['point_id'] = point_id
        return point.update(**kwargs)

    @staticmethod
    def delete_knowledge_point(point_id):
        """删除知识点"""
        point = KnowledgePoint.get_by_point(point_id)
        if not point:
            raise ValueError("知识点不存在")
        return point.delete()

    @staticmethod
    def get_points_by_section(section_id):
        """获取指定章节的所有知识点"""
        return KnowledgePoint.get_by_section(section_id)

    # ==================== 问题管理 ====================
    @staticmethod
    def get_question(question_id):
        return Question.get_by_question(question_id)


    @staticmethod
    def create_question(question_id,section_id, question_text,answer_text):
        """创建问题"""
        if not CourseSection.get_by_section(section_id):
            raise ValueError("所属章节不存在")
        return Question.create(question_id=question_id,section_id=section_id, question=question_text,answer=answer_text)

    @staticmethod
    def update_question(question_id, **kwargs):
        """更新问题"""

        question = Question.get_by_question(question_id)
        if not question:
            raise ValueError("问题不存在")

        # 检查章节存在性（如果更新章节ID）
        if 'section_id' in kwargs and not CourseSection.get_by_section(kwargs['section_id']):
            raise ValueError("新章节不存在")
        kwargs['question_id'] = question_id

        return question.update(**kwargs)

    @staticmethod
    def delete_question(question_id):
        """删除问题及其关联答案"""
        question = Question.get_by_question(question_id)
        if not question:
            raise ValueError("问题不存在")
        return question.delete()

    @staticmethod
    def get_questions_by_section(section_id):
        """获取指定章节的所有问题"""

        return Question.get_by_section(section_id)



