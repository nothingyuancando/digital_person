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

# -------------------- 服务类封装 --------------------
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

    @staticmethod
    def get_all_details_for_record(record_id):
        return ConversationDetail.query.filter_by(record_id=record_id).all()

    # ==================== 统计查询（保持原有功能） ====================
    @staticmethod
    def get_student_conversations(student_id):
        return ConversationRecord.query.filter_by(student_id=student_id) \
            .options(db.joinedload(ConversationRecord.course)) \
            .order_by(ConversationRecord.conversation_time.desc()) \
            .all()

    @staticmethod
    def get_course_statistics(course_id):
        from sqlalchemy import func
        stats = db.session.query(
            func.avg(ConversationRecord.average_score).label('avg_score'),
            func.count(ConversationRecord.record_id).label('total_records')
        ).filter_by(course_id=course_id).first()
        return {
            'average_score': float(stats.avg_score) if stats.avg_score else 0,
            'total_records': stats.total_records
        }
