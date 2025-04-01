from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 设置连接数据库的信息
HOSTNAME='127.0.0.1'
PORT=3306
USERNAME='root'
PASSWORD='123456'
DATABASE='aibot'

db = SQLAlchemy()  # 先创建实例但不绑定应用

def create_app(config_class='config.DevConfig'):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    # 延迟绑定应用
    db.init_app(app)
    
    # 确保在应用上下文中导入模型
    with app.app_context():
        db.create_all()  # 创建表
    return app




