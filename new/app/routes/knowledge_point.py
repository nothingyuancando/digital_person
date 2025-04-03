# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from app.models.db_manager import DatabaseManager
from app.routes.course_section import section_bp

kp_bp = Blueprint('knowledge_points', __name__, url_prefix='/api/sections/<string:section_id>/knowledge_points')


@kp_bp.route('/', methods=['POST'])
def create_knowledge_point(section_id):
    data = request.json
    try:

        kp = DatabaseManager.create_knowledge_point(
            point_id=data['point_id'],
            section_id=section_id,
            title=data['title'],
            content=data['content']
        )
        return jsonify({
            'code': 201,
            'data': {
                'point_id': kp.point_id,
                'title': kp.title
            }
        }), 201
    except Exception as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400

@kp_bp.route('/<string:point_id>', methods=['GET'])
def get_knowledge_points(section_id,point_id):
    try:
        points = DatabaseManager.get_knowledge_point(point_id)
        if not points:
            return jsonify({'code': 404, 'msg': '问题不存在'}), 404
        return jsonify({
            'code': 200,
            'data': {
                'point_id': points.point_id,
                'title': points.title,
                'content': points.content
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@kp_bp.route('/', methods=['GET'])
def get_knowledge_points_by_section(section_id):
    try:
        points = DatabaseManager.get_points_by_section(section_id)
        return jsonify({
            'code': 200,
            'data': [{
                'point_id': p.point_id,
                'title': p.title,
                'content': p.content
            } for p in points]
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

# 其他端点保持类似结构
@kp_bp.route('/<string:point_id>', methods=['PUT'])
def update_knowledge_point(section_id, point_id):
    """更新知识点（支持跨章节移动）"""
    data = request.json
    try:
        # 验证知识点存在性
        point = DatabaseManager.get_knowledge_point(point_id)
        if not point or point.section_id != section_id:
            return jsonify({'code': 404, 'msg': '知识点不存在'}), 404

        # 验证新章节存在性（如果修改章节）
        new_section_id = data.get('section_id', section_id)
        if new_section_id != section_id and not DatabaseManager.get_section(new_section_id):
            return jsonify({'code': 404, 'msg': '目标章节不存在'}), 404

        # 执行更新

        updated = DatabaseManager.update_knowledge_point(
            point_id=point_id,
            title=data.get('title'),
            content=data.get('content'),
            section_id=new_section_id
        )

        return jsonify({
            'code': 200,
            'data': {
                'point_id': updated.point_id,
                'new_section_id': new_section_id
            }
        })
    except KeyError as e:
        return jsonify({'code': 400, 'msg': f'缺少必要字段: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500


@kp_bp.route('/<string:point_id>', methods=['DELETE'])
def delete_knowledge_point(section_id, point_id):
    """删除知识点"""
    try:
        point = DatabaseManager.get_knowledge_point(point_id)
        if not point or point.section_id != section_id:
            return jsonify({'code': 404, 'msg': '知识点不存在'}), 404

        success = DatabaseManager.delete_knowledge_point(point_id)
        return jsonify({
            'code': 200,
            'data': {
                'deleted_point': point_id,
                'section_id': section_id
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500