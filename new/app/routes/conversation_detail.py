# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from app.models.db_manager import DatabaseManager
from app.routes.conversations_record import conv_bp
detail_bp = Blueprint('details', __name__, url_prefix='/api/details')


@detail_bp.route('/', methods=['POST'])
def create_detail():
    """创建对话详情"""
    data = request.json
    try:
        # 参数校验
        required_fields = ['record_id', 'conversation_no', 'question']
        if not all(field in data for field in required_fields):
            raise ValueError("缺少必填字段: record_id, conversation_no, question")

        # 创建详情
        detail = DatabaseManager.create_conversation_detail(
            record_id=data['record_id'],
            conversation_no=data['conversation_no'],
            question=data['question'],
            student_answer=data.get('student_answer'),
            reference_answer=data.get('reference_answer'),
            score=data.get('score')
        )

        return jsonify({
            'code': 200,
            'data': {
                'detail_id': detail.detail_id,
                'record_id': detail.record_id,
                'conversation_no': detail.conversation_no
            }
        }), 201
    except ValueError as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400
    except Exception as e:
        return jsonify({'code': 500, 'msg': f"服务器错误: {str(e)}"}), 500

@detail_bp.route('/<int:detail_id>', methods=['GET'])
def get_detail(detail_id):
    """获取单个对话详情"""
    try:
        detail = DatabaseManager.get_conversation_detail(detail_id)
        if not detail:
            return jsonify({'code': 404, 'msg': '详情不存在'}), 404

        return jsonify({
            'code': 200,
            'data': {
                'detail_id': detail.detail_id,
                'record_id': detail.record_id,
                'conversation_no': detail.conversation_no,
                'question': detail.question,
                'student_answer': detail.student_answer,
                'reference_answer': detail.reference_answer,
                'score': float(detail.score) if detail.score else None
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@detail_bp.route('/<int:detail_id>', methods=['PUT'])
def update_detail(detail_id):
    """更新对话详情"""
    data = request.json
    try:
        # 过滤允许更新的字段
        allowed_fields = {
            'conversation_no': int,
            'question': str,
            'student_answer': str,
            'reference_answer': str,
            'score': float,
            'record_id': str
        }
        update_data = {}
        for field, field_type in allowed_fields.items():
            if field in data:
                update_data[field] = field_type(data[field]) if data[field] is not None else None

        # 执行更新
        DatabaseManager.update_conversation_detail(detail_id, **update_data)
        return jsonify({'code': 200, 'msg': '更新成功'})
    except ValueError as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@detail_bp.route('/<int:detail_id>', methods=['DELETE'])
def delete_detail(detail_id):
    """删除对话详情"""
    try:
        success = DatabaseManager.delete_conversation_detail(detail_id)
        if not success:
            return jsonify({'code': 404, 'msg': '详情不存在'}), 404
        return jsonify({'code': 200, 'msg': '删除成功'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

# 在 conversation_record 路由中添加关联查询
# @conv_bp.route('/<string:record_id>/details', methods=['GET'])
# def get_record_details(record_id):
#     """获取对话记录的所有详情"""
#     try:
#         details = DatabaseManager.get_all_details_for_record(record_id)
#         return jsonify({
#             'code': 200,
#             'data': [{
#                 'detail_id': d.detail_id,
#                 'conversation_no': d.conversation_no,
#                 'question': d.question,
#                 'score': float(d.score) if d.score else None
#             } for d in details]
#         })
#     except Exception as e:
#         return jsonify({'code': 500, 'msg': str(e)}), 500