# 基于 Flask 的课程管理系统

一个基于 Flask 的课程管理系统，支持课程管理、知识点抽取、数字人对话、学生评分等功能。

---

## 功能特性

### 课程管理
- **课程信息维护**
- **课程文件上传与处理**
- **知识点自动抽取**
- **知识图谱展示**

### 数字人对话
- **实时语音对话**
- **语音转文字**
- **对话评分与分析**
- **历史对话记录**

### 学生管理
- **学生信息维护**
- **对话评分记录**
- **学习报告生成**

---

## 系统特性
- **模块化设计**
- **异步任务处理**
- **语音服务集成**
- **数据可视化**

---

## 技术栈
- **核心框架:** Flask
- **数据库:** PostgreSQL / MySQL / SQLite
- **异步任务:** Celery + Redis
- **语音服务:** Azure Cognitive Services
- **前端技术:** Vue.js + WebSocket
- **API 文档:** Swagger

---

## 项目结构

```bash
/course-system
├── app.py                 # 应用入口
├── config.py              # 配置文件
├── models.py              # 数据库模型
├── extensions.py          # 扩展组件
├── routes/                # 路由模块
│   ├── course.py          # 课程相关
│   ├── digital_person.py  # 数字人对话
│   ├── student.py         # 学生评分
│   └── history.py         # 历史记录
├── services/              # 业务服务
│   ├── file_service.py           # 文件处理
│   ├── conversation_service.py   # 对话分析
│   ├── digital_person_service.py # 数字人服务
│   └── speech_service.py         # 语音处理
└── utils/                 # 工具类
    └── response.py        # 统一响应工具
快速开始

1. 环境准备
确保已安装以下依赖：

Python 3.8+
Redis
PostgreSQL / MySQL (可选)
2. 安装依赖
pip install -r requirements.txt
3. 配置环境变量
复制 .env.example 为 .env 并填写配置：

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost/course_system

# Azure 语音服务
AZURE_SPEECH_KEY=your_azure_key
AZURE_REGION=your_region

# 数字人服务
DIGITAL_PERSON_API=https://your.digital-person.api
DIGITAL_PERSON_KEY=your_api_key

# Celery 配置
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
4. 初始化数据库
flask db init
flask db migrate
flask db upgrade
5. 启动服务
启动 Flask 应用：

flask run --cert=adhoc
启动 Celery Worker：

celery -A app.celery worker --loglevel=info
API 文档

访问 /swagger 查看完整的 API 文档。

主要 API 接口
课程管理

POST /api/course/upload - 上传课程文件
GET /api/course/knowledge-graph - 获取知识图谱
数字人对话

POST /api/digital-person/start - 启动对话
POST /api/digital-person/message - 发送消息
POST /api/digital-person/end - 结束对话
学生评分

GET /api/student/grade - 获取评分详情
GET /api/history/conversations - 获取历史记录
部署指南

生产环境部署
使用 Gunicorn 运行应用：

gunicorn -w 4 app:app
同时可配置 Nginx 反向代理，并使用 Supervisor 管理进程。

Docker 部署
docker-compose up -d
贡献指南

欢迎提交 Issue 和 PR，请遵循以下步骤：

Fork 项目
创建特性分支
git checkout -b feature/AmazingFeature
提交更改
git commit -m 'Add some AmazingFeature'
推送分支
git push origin feature/AmazingFeature
提交 Pull Request
许可证

本项目采用 MIT 许可证，详情请见 LICENSE 文件。

致谢

Flask 开发团队
Azure Cognitive Services
Celery 项目组
项目维护者: [Your Name]
联系方式: your.email@example.com
