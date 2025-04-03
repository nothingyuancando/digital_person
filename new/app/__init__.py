# -*- coding: utf-8 -*-  # 添加文件编码声明
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate


# 设置连接数据库的信息
HOSTNAME='127.0.0.1'
PORT=3306
USERNAME='root'
PASSWORD='123456'
DATABASE='aibot'

db = SQLAlchemy()  # 先创建实例但不绑定应用
migrate = Migrate()

from app.models import *

def create_app(config_class='config.DevConfig'):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.students import student_bp
    from app.routes.courses import course_bp
    from app.routes.conversations_record import conv_bp
    from app.routes.conversation_detail import detail_bp
    from app.routes.course_section import section_bp
    from app.routes.question import question_bp
    from app.routes.knowledge_point import kp_bp
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(conv_bp)
    app.register_blueprint(detail_bp)
    app.register_blueprint(section_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(kp_bp)

    # 确保在应用上下文中导入模型
    with app.app_context():
        from app.models.db_manager import (
            Student, Course, ConversationRecord,
            ConversationDetail, CourseSection,
            KnowledgePoint, Question
        )
        db.create_all()


    return app




