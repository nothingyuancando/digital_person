# -*- coding: utf-8 -*-  # 添加文件编码声明
from flask import Blueprint, request, jsonify
from app.models.db_manager import DatabaseManager


course_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


@course_bp.route('/', methods=['POST'])
def create_course():
    data = request.json
    print(f"hh{data}")
    try:
        course = DatabaseManager.create_course(
            course_id=data['course_id'],
            course_name=data['course_name'],
            description=data.get('description')
        )
        return jsonify({
            'code': 200,
            'data': {
                'course_id': course.course_id,
                'course_name': course.course_name
            }
        }), 201
    except Exception as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400


@course_bp.route('/<string:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        course = DatabaseManager.get_course(course_id)
        if not course:
            return jsonify({'code': 404, 'msg': '课程不存在'}), 404

        return jsonify({
            'code': 200,
            'data': {
                'course_id': course.course_id,
                'course_name': course.course_name,
                'description': course.description
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

# course路由补全部分
@course_bp.route('/', methods=['GET'])
def get_all_courses():
    try:
        courses = DatabaseManager.get_all_courses()
        return jsonify({
            'code': 200,
            'data': [{
                'course_id': c.course_id,
                'course_name': c.course_name,
                'description': c.description
            } for c in courses]
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@course_bp.route('/<string:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.json
    try:
        updated = DatabaseManager.update_course(
            course_id=course_id,
            course_name=data.get('course_name'),
            description=data.get('description')
        )
        if not updated:
            return jsonify({'code': 404, 'msg': '课程不存在'}), 404
        return jsonify({'code': 200, 'msg': '更新成功'})
    except ValueError as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@course_bp.route('/<string:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        success = DatabaseManager.delete_course(course_id)
        if not success:
            return jsonify({'code': 404, 'msg': '课程不存在'}), 404
        return jsonify({'code': 200, 'msg': '删除成功'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500