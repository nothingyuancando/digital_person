"""
应用配置模块
包含敏感信息配置和功能开关
"""

import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///courses.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文件处理
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # 数字人服务
    DIGITAL_PERSON_API = os.getenv('DIGITAL_PERSON_API')
    DIGITAL_PERSON_KEY = os.getenv('DIGITAL_PERSON_KEY')

    # 语音服务 (Azure)
    AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
    AZURE_REGION = os.getenv('AZURE_REGION', 'eastus')

    # Celery配置
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')