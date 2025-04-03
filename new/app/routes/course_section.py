# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from app.models.db_manager import DatabaseManager

section_bp = Blueprint('sections', __name__, url_prefix='/api/courses/<string:course_id>/sections')

@section_bp.route('/', methods=['POST'])
def create_section(course_id):
    data = request.json
    try:
        section = DatabaseManager.create_section(
            section_id=data['section_id'],
            course_id=course_id,
            section_name=data['section_name']
        )
        return jsonify({
            'code': 201,
            'data': {
                'section_id': section.section_id,
                'section_name': section.section_name
            }
        }), 201
    except Exception as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400

@section_bp.route('/', methods=['GET'])
def get_all_sections(course_id):
    try:
        sections = DatabaseManager.get_sections_by_course(course_id)
        return jsonify({
            'code': 200,
            'data': [{
                'section_id': s.section_id,
                'section_name': s.section_name
            } for s in sections]
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@section_bp.route('/<string:section_id>', methods=['GET'])
def get_section(course_id, section_id):
    try:

        section = DatabaseManager.get_section(section_id)


        if not section or section.course_id != course_id:
            return jsonify({'code': 404, 'msg': '小节不存在'}), 404
        return jsonify({
            'code': 200,
            'data': {
                'section_id': section.section_id,
                'section_name': section.section_name,
                'course_id': section.course_id
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

# 其他方法类似，保持与course路由一致的风格
@section_bp.route('/<string:section_id>', methods=['PUT'])
def update_section(course_id, section_id):
    """更新章节信息（支持跨课程移动）"""
    data = request.json
    try:
        section = DatabaseManager.get_section(section_id)
        if not section or section.course_id != course_id:
            return jsonify({'code': 404, 'msg': '章节不存在'}), 404

        # 验证新课程是否存在（如果修改课程）


        new_course_id = data.get('course_id', course_id)

        if new_course_id != course_id and not DatabaseManager.get_course(new_course_id):
            return jsonify({'code': 404, 'msg': '目标课程不存在'}), 404


        updated = DatabaseManager.update_section(
            section_id=section_id,
            section_name=data.get('section_name'),
            course_id=new_course_id
        )
        return jsonify({
            'code': 200,
            'data': {
                'section_id': updated.section_id,
                'new_course_id': new_course_id
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@section_bp.route('/<string:section_id>', methods=['DELETE'])
def delete_section(course_id, section_id):
    """级联删除章节（包含知识点和问题）"""
    try:
        print("hhhhh")

        section = DatabaseManager.get_section(section_id)
        if not section or section.course_id != course_id:
            return jsonify({'code': 404, 'msg': '章节不存在'}), 404
        print(section_id)
        success = DatabaseManager.delete_section(section_id)
        print(success)
        return jsonify({
            'code': 200,
            'data': {
                'deleted_section': section_id,
                'related_deletions': {
                    'knowledge_points': len(section.knowledge_points),
                    'questions': len(section.questions)
                }
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500