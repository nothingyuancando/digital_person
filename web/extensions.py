"""
扩展组件初始化模块
集中管理第三方扩展
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

# 数据库扩展
db = SQLAlchemy()
migrate = Migrate()

# Celery扩展
celery = Celery(__name__, include=['services.file_service', 'services.digital_person_service'])