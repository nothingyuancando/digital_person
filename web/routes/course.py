#课程相关接口

from flask import Blueprint, request, current_app
from models import Course, CourseFile, KnowledgeGraph
from utils.response import success_response, error_response
from services.file_service import process_uploaded_file
import os

bp = Blueprint('course', __name__, url_prefix='/api/course')

@bp.route('/upload', methods=['POST'])
def file_upload():
    # 参数校验
    if 'file' not in request.files:
        return error_response("未上传文件", 400)
    if 'courseId' not in request.form:
        return error_response("缺少课程ID参数", 400)

    file = request.files['file']
    course_id = request.form['courseId']

    # 验证课程存在
    course = Course.query.get(course_id)
    if not course:
        return error_response("课程不存在", 404)

    # 保存文件
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    except Exception as e:
        return error_response("文件保存失败", 500)

    # 创建文件记录
    new_file = CourseFile(
        course_id=course_id,
        file_path=file_path,
        status='processing'
    )
    db.session.add(new_file)
    db.session.commit()

    # 启动异步处理
    process_uploaded_file.delay(new_file.file_id)

    return success_response({
        "processId": new_file.process_id
    }, "文件上传成功，处理已启动")

@bp.route('/knowledge-graph', methods=['GET'])
def get_knowledge_graph():
    course_id = request.args.get('courseId')
    if not course_id:
        return error_response("缺少课程ID参数", 400)

    # 查询知识图谱数据
    knowledge_points = KnowledgeGraph.query.filter_by(
        course_id=course_id
    ).all()

    if not knowledge_points:
        return error_response("未找到知识图谱数据", 404)

    data = [{
        "title": kp.title,
        "content": kp.content
    } for kp in knowledge_points]

    return success_response(data)

@bp.route('/info', methods=['GET'])
def get_course_info():
    course_id = request.args.get('courseId')
    if not course_id:
        return error_response("缺少课程ID参数", 400)

    course = Course.query.get(course_id)
    if not course:
        return error_response("课程不存在", 404)

    data = {
        "courseId": course.course_id,
        "courseName": course.course_name,
        "description": course.description
    }
    return success_response(data)