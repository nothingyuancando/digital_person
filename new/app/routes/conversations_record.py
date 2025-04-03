# -*- coding: utf-8 -*-  # 添加文件编码声明
from flask import Blueprint, request, jsonify
from app.models.db_manager import DatabaseManager

conv_bp = Blueprint('conversations', __name__, url_prefix='/api/conversations')


@conv_bp.route('/', methods=['POST'])
def create_conversation():
    data = request.json
    try:
        record_data = {
            'record_id': data['record_id'],
            'student_id': data['student_id'],
            'course_id': data['course_id'],
            'keyword': data.get('keyword'),
            'average_score': data.get('average_score'),
            'grade': data.get('grade'),
            'analysis_report': data.get('analysis_report'),


        }

        details_data = data.get('details', [])

        record = DatabaseManager.create_conversation_record(
            record_data=record_data,
            details_data=details_data
        )

        return jsonify({
            'code': 200,
            'data': {
                'record_id': record.record_id,
                'conversation_time': record.conversation_time.isoformat()
            }
        }), 201
    except Exception as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400


@conv_bp.route('/<string:record_id>', methods=['GET'])
def get_full_conversation(record_id):
    try:
        record = DatabaseManager.get_conversation_record(record_id)
        if not record:
            return jsonify({'code': 404, 'msg': '记录不存在'}), 404

        return jsonify({
            'code': 200,
            'data': {
                'record_id': record.record_id,
                'details': [{
                    'question': d.question,
                    'score': float(d.score) if d.score else None
                } for d in record.details]
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500


# convenience路由补全部分
@conv_bp.route('/', methods=['GET'])
def get_all_conversations():
    try:
        records = DatabaseManager.get_all_conversation_records()
        return jsonify({
            'code': 200,
            'data': [{
                'record_id': r.record_id,
                'student_id': r.student_id,
                'course_id': r.course_id,
                'conversation_time': r.conversation_time.isoformat()
            } for r in records]
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500


@conv_bp.route('/<string:record_id>', methods=['PUT'])
def update_conversation(record_id):
    data = request.json
    try:
        update_data = {
            'keyword': data.get('keyword'),
            'average_score': data.get('average_score'),
            'grade': data.get('grade'),
            'analysis_report': data.get('analysis_report')
        }
        details_data = data.get('details')

        success = DatabaseManager.update_conversation_record(
            record_id=record_id,
            record_data=update_data,
            details_data=details_data
        )
        if not success:
            return jsonify({'code': 404, 'msg': '记录不存在'}), 404
        return jsonify({'code': 200, 'msg': '更新成功'})
    except ValueError as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500


@conv_bp.route('/<string:record_id>', methods=['DELETE'])
def delete_conversation(record_id):
    try:
        success = DatabaseManager.delete_conversation_record(record_id)
        if not success:
            return jsonify({'code': 404, 'msg': '记录不存在'}), 404
        return jsonify({'code': 200, 'msg': '删除成功'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500