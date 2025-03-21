# 基于 Flask 的课程管理系统

支持课程管理、知识点抽取、数字人对话、学生评分等功能。

## 功能特性

### 课程管理
- 课程信息维护
- 课程文件上传与处理
- 知识点自动抽取
- 知识图谱展示

### 数字人对话
- 实时语音对话
- 语音转文字
- 对话评分与分析
- 历史对话记录

### 学生管理
- 学生信息维护
- 对话评分记录
- 学习报告生成

## 系统特性
- 模块化设计
- 异步任务处理
- 语音服务集成
- 数据可视化

## 技术栈
- 核心框架: Flask
- 数据库: PostgreSQL / MySQL / SQLite
- 异步任务: Celery + Redis
- 语音服务: Azure Cognitive Services
- 前端技术: Vue.js + WebSocket
- API 文档: Swagger

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
│   ├── file_service.py    # 文件处理
│   ├── conversation_service.py # 对话分析
│   ├── digital_person_service.py # 数字人服务
│   └── speech_service.py  # 语音处理
└── utils/                 # 工具类
    └── response.py        # 统一响应工具
