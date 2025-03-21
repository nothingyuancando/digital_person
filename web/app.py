"""
Flask应用工厂主入口
配置应用并注册所有组件
"""

from flask import Flask
from config import Config
from extensions import db, migrate, celery
from routes import course, digital_person, student, history

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    celery.conf.update(app.config)

    # 注册蓝图
    app.register_blueprint(course.bp)
    app.register_blueprint(digital_person.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(history.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(ssl_context='adhoc')  # 启用HTTPS