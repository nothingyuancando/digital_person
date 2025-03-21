'''
��װ�ص�˵��
�ֲ�ܹ���
ģ�Ͳ㣺�̳��� BaseModel �ṩ���� CRUD ����
����㣺ͨ�� DatabaseManager �ṩҵ����ز���
���Ĺ��ܣ�
�Զ�������������ع����ƣ�
��������֧�֣���Ի���¼+�����ԭ�Ӳ�����
����������֤��������¼ʱ���ѧ��/�γ̴����ԣ�
���ò�ѯģʽ��װ���������Ĳ�ѯ��ͳ�Ʋ�ѯ��
��չ���飺
��ӷ�ҳ��ѯ����
���ӻ�����ƣ��� Redis��
��Ӹ����ӵ�ͳ�Ʋ�ѯ
ʵ����ɾ������� is_deleted ��־�ֶΣ�
������
ͳһ���� SQLAlchemy �쳣
�Զ���ҵ���쳣����ѧ��������ʱ�׳���
ʹ��ʱֻ�赼�� DatabaseManager �༴�ɽ����������ݿ����������ҵ�����ļ���ԡ�
'''

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.__init__ import db

# -------------------- ����ģ���� --------------------
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

# -------------------- ����ģ�� --------------------
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

# -------------------- �������װ --------------------
# -------------------- �������װ --------------------
class DatabaseManager:
    # ==================== ѧ������ ====================
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
            raise ValueError("ѧ��������")
        return student.update(**kwargs)

    @staticmethod
    def delete_student(student_id):
        student = Student.get_by_id(student_id)
        if not student:
            raise ValueError("ѧ��������")
        return student.delete()

    @staticmethod
    def get_all_students():
        return Student.query.all()

    # ==================== �γ̹��� ====================
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
            raise ValueError("�γ̲�����")
        return course.update(**kwargs)

    @staticmethod
    def delete_course(course_id):
        course = Course.get_by_id(course_id)
        if not course:
            raise ValueError("�γ̲�����")
        return course.delete()

    @staticmethod
    def get_all_courses():
        return Course.query.all()

    # ==================== �Ի���¼���� ====================
    @staticmethod
    def create_conversation_record(record_data, details_data):
        """
        :param record_data: dict �����Ի���¼�ֶ�
        :param details_data: list ��������Ի������ֵ�
        """
        try:
            # ������������
            if not Student.get_by_id(record_data['student_id']):
                raise ValueError("ѧ��������")
            if not Course.get_by_id(record_data['course_id']):
                raise ValueError("�γ̲�����")

            # ��������¼
            record = ConversationRecord.create(**record_data)

            # ������������
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
            raise ValueError("�Ի���¼������")

        # ������������
        if 'student_id' in kwargs:
            if not Student.get_by_id(kwargs['student_id']):
                raise ValueError("��ѧ��������")
        if 'course_id' in kwargs:
            if not Course.get_by_id(kwargs['course_id']):
                raise ValueError("�¿γ̲�����")

        return record.update(**kwargs)

    @staticmethod
    def delete_conversation_record(record_id):
        record = ConversationRecord.query.get(record_id)
        if not record:
            raise ValueError("�Ի���¼������")
        return record.delete()

    @staticmethod
    def get_all_conversation_records():
        return ConversationRecord.query.all()

    # ==================== �Ի�������� ====================
    @staticmethod
    def create_conversation_detail(record_id, **detail_data):
        if not ConversationRecord.query.get(record_id):
            raise ValueError("�Ի���¼������")
        return ConversationDetail.create(record_id=record_id, **detail_data)

    @staticmethod
    def get_conversation_detail(detail_id):
        return ConversationDetail.query.get(detail_id)

    @staticmethod
    def update_conversation_detail(detail_id, **kwargs):
        detail = ConversationDetail.query.get(detail_id)
        if not detail:
            raise ValueError("�Ի����鲻����")

        if 'record_id' in kwargs:
            if not ConversationRecord.query.get(kwargs['record_id']):
                raise ValueError("�¶Ի���¼������")

        return detail.update(**kwargs)

    @staticmethod
    def delete_conversation_detail(detail_id):
        detail = ConversationDetail.query.get(detail_id)
        if not detail:
            raise ValueError("�Ի����鲻����")
        return detail.delete()

    @staticmethod
    def get_all_details_for_record(record_id):
        return ConversationDetail.query.filter_by(record_id=record_id).all()

    # ==================== ͳ�Ʋ�ѯ������ԭ�й��ܣ� ====================
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
