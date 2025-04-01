from flask import Blueprint, request, jsonify
from puweb.new.app.services.dbmanage.db_manager_plus import DatabaseManager


course_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


@course_bp.route('/', methods=['POST'])
def create_course():
    data = request.json
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
            return jsonify({'code': 404, 'msg': '�γ̲�����'}), 404

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

# ������������ѧ��·��ʵ��...