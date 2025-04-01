from flask import Blueprint, request, jsonify
from puweb.new.app.services.dbmanage.db_manager_plus import DatabaseManager

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
            'analysis_report': data.get('analysis_report')
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
        record = DatabaseManager.get_full_conversation(record_id)
        if not record:
            return jsonify({'code': 404, 'msg': '��¼������'}), 404

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

# ��������ʵ��...