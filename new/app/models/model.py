from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from jinja2.runtime import exported

from app.__init__ import db


class Student(db.Model):
    __tablename__ = 'student'

    student_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # 与对话记录的一对多关系
    conversations = db.relationship('ConversationRecord', backref='student', lazy=True)

class Course(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.String(50), primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    # 与对话记录的关联关系（可选）
    conversations = db.relationship('ConversationRecord', backref='course', lazy=True)

class ConversationRecord(db.Model):
    __tablename__ = 'conversation_record'

    record_id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.student_id'), nullable=False)
    # 更新为正式的外键关联
    course_id = db.Column(db.String(50), db.ForeignKey('course.course_id'), nullable=False)  #
    conversation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    keyword = db.Column(db.String(100))
    average_score = db.Column(db.Numeric(5, 2))
    grade = db.Column(db.String(5))
    analysis_report = db.Column(db.Text)
    # 与对话详情的一对多关系
    details = db.relationship('ConversationDetail', backref='record', lazy=True)

class ConversationDetail(db.Model):
    __tablename__ = 'conversation_detail'

    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.String(50), db.ForeignKey('conversation_record.record_id'), nullable=False)
    conversation_no = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    student_answer = db.Column(db.Text)
    reference_answer = db.Column(db.Text)
    score = db.Column(db.Numeric(5, 2))